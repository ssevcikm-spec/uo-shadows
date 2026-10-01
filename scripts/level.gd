extends Node2D
## Mapa úrovně postavená z JSON, který vygeneroval `forge level`.
##
## PROČ JSON A NE .tscn: mapa musí být text, který se dá diffovat v gitu a který
## zvládne přečíst i AI agent (u binárních scén s UID se to nedaří). Uzel si
## z mřížky postaví dlaždice za běhu – a hlavně umí odpovědět na jednu otázku,
## na které stojí pohyb hráče: „je tohle políčko průchozí?"
##
## Mřížka je řádek na řádek, znak na buňku: 0 = zeď, 1 = podlaha místnosti,
## 2 = chodba. Konvence je stejná v Pythonu (pipeline/levels.py) i tady.
##
## ============================================================================
## IZOMETRICKÁ PROJEKCE 2:1 – a proč je v tomhle souboru
##
## Schéma (projekce, velikost dlaždice, viewport) se čte z `assets/spec.json`,
## tedy Z DAT HRY. V tomhle skriptu není žádné „96" ani „16" napevno – jiná hra
## s jinou projekcí použije tentýž skript bez úprav.
##
## Naměřeno 30. 9. 2026: dřív tu bylo `s.position = offset + Vector2(x*cell,
## y*cell)` se `scale` 1:1, tedy OSOVĚ ZAROVNANÝ ČTVEREC. `spec.json` přitom
## celou dobu deklaroval izometrii 2:1 a dlaždice byly 32×32 čtverce. Výsledek:
## izometrický pohled nemohl vzniknout, ať se sprity ladily jakkoli – a nikdo si
## toho nevšiml, protože se deklarace s kódem nikde neporovnávala.
## Od toho je brána `.forge/check-schema.py` (běží v CI před testy).
##
## SOUŘADNICE: dlaždice (cx, cy) se kreslí na
##     x = (cx - cy) * cell_w / 2
##     y = (cx + cy) * cell_h / 2
## a dlaždice se překrývají do poloviny výšky, takže se řady musí sázet po
## `cell_h / 2`. Kreslit je po `cell_h` (jak to dělá obdélníková mřížka) vede
## k děrám mezi řadami.
## ============================================================================

const SPEC_PATH := "res://assets/spec.json"
const TILE_DIR := "res://assets/tiles/"
const DEFAULT_TILES := {"0": "brick", "1": "stone", "2": "dirt"}

# Výchozí hodnoty jsou jen záchrana, když spec chybí – primární je spec.json.
const CELL_W_DEFAULT := 96
const CELL_H_DEFAULT := 48

var source := ""
var level_name := ""
var cell_w := CELL_W_DEFAULT
var cell_h := CELL_H_DEFAULT
var projekce := "izometricka"
var offset := Vector2.ZERO
var grid := PackedStringArray()
var width := 0
var height := 0
var tile_names := {}
var markers: Array = []
var spawn_cell := Vector2i.ZERO
var stats := {}

var _textures: Dictionary = {}


func _ready() -> void:
	_nacti_spec()


func _nacti_spec() -> bool:
	"""Načte schéma z assets/spec.json. Bez něj se použijí výchozí hodnoty."""
	if not FileAccess.file_exists(SPEC_PATH):
		push_warning("[level] %s není – používám výchozí schéma %d×%d"
			% [SPEC_PATH, CELL_W_DEFAULT, CELL_H_DEFAULT])
		return false
	var data: Variant = JSON.parse_string(FileAccess.get_file_as_string(SPEC_PATH))
	if not (data is Dictionary):
		push_error("[level] %s není platné JSON" % SPEC_PATH)
		return false

	var proj: Dictionary = data.get("projekce", {})
	var tile: Dictionary = data.get("tile", {})
	var w: Variant = proj.get("dlazdice_sirka", tile.get("sirka"))
	var h: Variant = proj.get("dlazdice_vyska", tile.get("vyska"))
	if w != null and h != null:
		cell_w = int(w)
		cell_h = int(h)
	if proj.has("typ"):
		projekce = str(proj["typ"])
	elif cell_w != cell_h:
		# Různá šířka a výška = kosočtverec = izometrie. Odvozuje se, aby hra
		# fungovala i se starším specem bez `projekce.typ`.
		projekce = "izometricka"
	else:
		projekce = "ctvercova"
	return true


func load_file(path: String) -> bool:
	"""Načte úroveň ze souboru (např. res://assets/levels/main.json).
	Vrací false, když soubor chybí nebo je poškozený."""
	if not FileAccess.file_exists(path):
		return false
	var text := FileAccess.get_file_as_string(path)
	var data: Variant = JSON.parse_string(text)
	if not (data is Dictionary):
		push_error("[level] %s není platné JSON" % path)
		return false

	source = path
	level_name = str(data.get("name", ""))
	# Velikost buňky se bere ZE SPECU, ne z mapy: schéma je vlastnost hry, ne
	# jednotlivého levelu. Když to level deklaruje jinak, je to rozpor a ohlásí
	# ho `.forge/check-schema.py` – tady se jen použije platné schéma.
	_nacti_spec()
	width = int(data.get("width", 0))
	height = int(data.get("height", 0))
	grid = PackedStringArray(data.get("grid", []))
	markers = data.get("markers", [])
	stats = data.get("stats", {})
	tile_names = data.get("tiles", DEFAULT_TILES)

	var off: Array = data.get("offset", [])
	if off.size() >= 2:
		offset = Vector2(float(off[0]), float(off[1]))
	else:
		# Bez offsetu v datech se mapa VYSTŘEDÍ na spawn. Není to kosmetika:
		# bez toho je spawn (17,7) v izometrii na y = 576, tedy POD obrazovkou
		# (viewport je 540 vysoký) a hráč na začátku nevidí sám sebe.
		offset = Vector2.ZERO

	# Hlavička a mřížka si musí odpovídat – poškozený soubor se nesmí tiše použít.
	if width <= 0 or height <= 0 or grid.size() != height:
		push_error("[level] %s: mřížka nesedí s hlavičkou (%d řádků, čekáno %d)"
			% [path, grid.size(), height])
		return false
	for row in grid:
		if row.length() != width:
			push_error("[level] %s: řádek má %d znaků, čekáno %d" % [path, row.length(), width])
			return false

	for m: Variant in markers:
		if m is Dictionary and str(m.get("type", "")) == "spawn":
			var c: Array = m.get("cell", [0, 0])
			spawn_cell = Vector2i(int(c[0]), int(c[1]))
	return true


func je_izometricka() -> bool:
	return projekce.begins_with("izo")


func cell_center(cx: int, cy: int) -> Vector2:
	"""Střed dlaždice (cx, cy) v souřadnicích scény."""
	if je_izometricka():
		return offset + Vector2(
			float(cx - cy) * cell_w / 2.0,
			float(cx + cy) * cell_h / 2.0)
	# Obdélníková projekce – jiné hry (side-scroller, top-down čtverec).
	return offset + Vector2(cx * cell_w + cell_w / 2.0, cy * cell_h + cell_h / 2.0)


func cell_at(pos: Vector2) -> Vector2i:
	"""Zpětný převod: které políčko je na téhle pozici."""
	var p := pos - offset
	if je_izometricka():
		# Inverze k cell_center: x = (cx-cy)*w/2, y = (cx+cy)*h/2
		var a := p.x / (cell_w / 2.0)     # = cx - cy
		var b := p.y / (cell_h / 2.0)     # = cx + cy
		return Vector2i(int(floor((b + a) / 2.0)), int(floor((b - a) / 2.0)))
	return Vector2i(int(floor(p.x / float(cell_w))), int(floor(p.y / float(cell_h))))


func vystredni_na_spawn(viewport: Vector2) -> void:
	"""Posune mapu tak, aby byl spawn ve středu obrazovky.
	Volá se z `game.gd` po `load_file`, protože viewport zná až scéna."""
	if spawn_cell == Vector2i.ZERO and grid.size() == 0:
		return
	offset = viewport / 2.0 - cell_center_bez_offsetu(spawn_cell.x, spawn_cell.y)


func cell_center_bez_offsetu(cx: int, cy: int) -> Vector2:
	if je_izometricka():
		return Vector2(float(cx - cy) * cell_w / 2.0, float(cx + cy) * cell_h / 2.0)
	return Vector2(cx * cell_w + cell_w / 2.0, cy * cell_h + cell_h / 2.0)


func build() -> void:
	"""Postaví dlaždice jako Sprite2D. Bez vygenerovaných dlaždic zůstane jen
	mřížka (mapa se nevykreslí, ale logika průchodnosti funguje dál)."""
	for child in get_children():
		child.queue_free()

	for y in height:
		for x in width:
			var name := _tile_for(grid[y][x])
			var tex := _texture(name)
			if tex == null:
				continue
			var s := Sprite2D.new()
			s.name = "T%d_%d" % [x, y]
			s.texture = tex
			s.centered = true
			s.position = cell_center(x, y)
			s.scale = Vector2(float(cell_w) / float(tex.get_width()),
							  float(cell_h) / float(tex.get_height()))
			# IZOMETRICKÉ ŘAZENÍ: dlaždice blíž k divákovi (větší x+y) musí být
			# nakreslená POZDĚJI, jinak ji vzdálenější překryje.
			#
			# ZÁKLAD JE ZÁPORNÝ, a to je důležité: entity (hráč, mince) mají
			# `z_index` 0. Když dlaždice začínaly na nule a rostly, měl hráč
			# stejnou vrstvu jako první dlaždice a VŠECHNY ostatní ho překryly –
			# naměřeno na snímku: izometrická mapa byla vidět, ale hráč na ní
			# NEBYL (a přitom byl ve scéně). Posun o -2000 drží celou mapu pod
			# entitami a relativní řazení dlaždic mezi sebou zachová.
			s.z_index = (x + y) * 2 - 2000 + (0 if grid[y][x] != "0" else 1)
			add_child(s)
	print("[level] %s: %d×%d políček, %s %d×%d px, dlaždic: %d, značek: %d"
		% [level_name, width, height, projekce, cell_w, cell_h,
		   get_child_count(), markers.size()])


func _tile_for(znak: String) -> String:
	return str(tile_names.get(znak, DEFAULT_TILES.get(znak, "stone")))


func _texture(tile_name: String) -> Texture2D:
	if _textures.has(tile_name):
		return _textures[tile_name]
	var path := TILE_DIR + tile_name + ".png"
	var tex: Texture2D = load(path) if ResourceLoader.exists(path) else null
	_textures[tile_name] = tex
	return tex


# ------------------------------------------------------------- průchodnost ----
func is_walkable_cell(cx: int, cy: int) -> bool:
	"""Průchozí je jen políčko uvnitř mapy, které není zeď ("0")."""
	if cx < 0 or cy < 0 or cx >= width or cy >= height:
		return false
	return grid[cy][cx] != "0"


func is_walkable_at(pos: Vector2) -> bool:
	var c := cell_at(pos)
	return is_walkable_cell(c.x, c.y)


func markers_of(type: String) -> Array:
	var out: Array = []
	for m in markers:
		if str(m.get("type", "")) == type:
			out.append(m)
	return out


func marker_positions(type: String) -> Array:
	var out: Array = []
	for m in markers_of(type):
		var c: Array = m.get("cell", [0, 0])
		out.append(cell_center(int(c[0]), int(c[1])))
	return out


func walkable_count() -> int:
	var n := 0
	for y in height:
		for x in width:
			if grid[y][x] != "0":
				n += 1
	return n


func reachable_count(from_cell := Vector2i(-1, -1)) -> int:
	"""Spočítá dosažitelná políčka ze spawnu – stejné ověření jako v Pythonu,
	ale tady nad tím, co má hra skutečně načtené."""
	if from_cell.x < 0:
		from_cell = spawn_cell
	if not is_walkable_cell(from_cell.x, from_cell.y):
		return 0
	var seen := {from_cell: true}
	var front: Array[Vector2i] = [from_cell]
	while not front.is_empty():
		var c: Vector2i = front.pop_back()
		for d: Vector2i in [Vector2i(1, 0), Vector2i(-1, 0), Vector2i(0, 1), Vector2i(0, -1)]:
			var n: Vector2i = c + d
			if is_walkable_cell(n.x, n.y) and not seen.has(n):
				seen[n] = true
				front.append(n)
	return seen.size()
