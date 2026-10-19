extends Area2D
## Hráč: stav (hp/mana/cíl), inventář, pohyb a smrt.
##
## Záměrně nepoužívá vstupní akce z project.godot – pohyb se čte přímo
## z kláves, takže se projekt dá celý vygenerovat textem a nic se nerozbije
## chybějící definicí akce.
##
## ============================================================================
## SMĚR POHYBU JE IZOMETRICKÝ — A NENÍ TO VOLBA (rozhodnuto 3. 10. 2026)
##
## `move(dir)` bere směr ve HŘE („vpravo", „dolů") a převádí ho na izometrické
## osy: `(dx - dy, dx + dy)` zmenšené na 0,5 a 0,25. Ty konstanty NEJSOU druhé
## číslo mřížky – jsou to TYTÉŽ poměry, jaké má kreslení dlaždic v `level.gd`
## (`cell_center`: `x = (cx-cy)*cell_w/2`, `y = (cx+cy)*cell_h/2`) a jaké
## deklaruje `assets/spec.json` (izometrie 2:1). Kdyby hráč chodil 1:1, šel by
## po obrazovce jiným sklonem, než po jakém jsou poskládané dlaždice.
##
## Ověřeno měřením (osa dlaždic `(48, 24)`, hráč „vpravo" `(0,894; 0,447)`):
## `|dy/dx| = 0,50` u obojího. Sonda: `tests/_sonda-pohyb.gd`.
## ============================================================================
##
## CO TU BYLO A PROČ UŽ NENÍ (naměřeno 3. 10. 2026): `_physics_process` měl
## větev `if level.has_method("iso_position")` a v ní DRUHÝ přepočet izometrie.
## Ta větev byla MRTVÁ: `level.gd` metodu `iso_position` vůbec nemá (má ji jen
## `_retired/world.gd`) a v `_physics_process` vycházel výsledek větve `else`
## na TOTÉŽ – `(dir.x, dir.y)` po normalizaci je stejný směr jako
## `(dir.x-dir.y, dir.x+dir.y)` po normalizaci, protože izo přepočet je jen
## lineární zkosení. Byla to tedy slepá větev *a* nález o bráně: test, který
## ji „kryl", hledal v souboru řetězec `level.iso_position` a zakazoval tím
## legitimní kód (`AGENTS.md`: „brána může být nastražená").
##
## SMLOUVA JE TEDY `move(dir)` – a `_physics_process` ji VOLÁ. Nejsou to dvě
## cesty k témuž: rozhraní je jedno a jen jedno místo mění pozici.
##
## ============================================================================
## PLYNUÝ POHYB (M1 „entity.move.smooth“, dokončeno 19. 10. 2026)
##
## `move(dir, delta)` má DVĚ cesty a obě jsou součást smlouvy:
##   · `delta < 0` = TESTOVACÍ volání: přesně JEDEN plný krok `SPEED/60` po
##     izometrické ose (na tomhle stojí testy izometrie – zachovej to!).
##   · `delta >= 0` = skutečný tik: rychlost se plynule rozjíždí a brzdí
##     (`ACCEL`/`DECEL`), takže se hráč nerozjede skokem a nezastaví naráz.
##     Mrtvá zóna 12 px (jen když směr dodá vstupní komponenta `smer()`),
##     běh ubírá staminu, chůze ne; při vyčerpané stamině je rychlost poloviční.
##   Hráč nikdy neskončí ve zdi – poslední krok dělá `_step()`, který klouže
##   po jedné ose.
## ============================================================================

signal collected(what: String)
signal died()

const SPEED := 130.0
## Zrychlení/zpomalení v px/s². 130/650 ≈ 0,2 s do plné rychlosti,
## 130/900 ≈ 0,14 s do zastavení (GDD §6: doba musí být měřitelná číslem).
const ACCEL := 650.0
const DECEL := 900.0
## Mrtvá zóna kurzoru v px (GDD §6) — brání kmitání, když kurzor stojí na postavě.
const DEAD_ZONE := 12.0
## Od téhle vzdálenosti kurzoru od postavy se BĚŽÍ (a běh bere staminu).
const RUN_DISTANCE := 160.0
const MAX_STAMINA_DEFAULT := 100.0
const STAMINA_RUN_PER_S := 20.0
const STAMINA_REGEN_PER_S := 12.0
const WALK_FACTOR := 0.5

# Výchozí stav postavy. JEDINÉ místo, kde se stav mění, je níž – kdyby se
# `hp` měnilo na dvou místech, rozejde se to s tím, co ukazuje HUD.
const MAX_HP_DEFAULT := 100
const MAX_MANA_DEFAULT := 50

var max_hp: int = MAX_HP_DEFAULT
var hp: int = MAX_HP_DEFAULT
var max_mana: int = MAX_MANA_DEFAULT
var mana: int = MAX_MANA_DEFAULT
var target: Node = null

var inventory: Array = []
var equipped: Node = null

var velocity := Vector2.ZERO
var level: Node2D

## Stav plynulého pohybu (M1): stamina + příznak běhu. `_bezim` nastavuje
## `_physics_process`; testy ho smějí nastavit přímo (je to měřený vstup).
var max_stamina: float = MAX_STAMINA_DEFAULT
var stamina: float = MAX_STAMINA_DEFAULT
var _bezim: bool = false
var _vstup: Node = null


func _ready() -> void:
	add_to_group("player")
	var shape := CollisionShape2D.new()
	var rect := RectangleShape2D.new()
	rect.size = Vector2(10, 10)
	shape.shape = rect
	add_child(shape)
	# Mapa (když je) rozhoduje, kudy se dá chodit. Hledá se ve skupině, takže
	# na sobě hráč a mapa nejsou závislí jménem uzlu.
	level = get_tree().get_first_node_in_group("level")


func _physics_process(delta: float) -> void:
	# POHYB JE JEN TADY – jen se zjistí směr a zavolá se smluvní `move()`.
	var dir := _smer_vstupu()
	_bezim = _chce_bezet(dir)
	move(dir, delta)


func _vstupni_komponenta() -> Node:
	"""Vstupní komponenta (`scripts/input.gd`), když je ve scéně.

	Hledá se ve skupině `input` a pak jako sourozenec „Input" – hráč na ní
	nesmí být závislý jménem (kdyby ji scéna neměla, hra musí jít hrát dál).
	"""
	if _vstup != null and is_instance_valid(_vstup):
		return _vstup
	if not is_inside_tree():
		return null
	var ve_skupine: Node = get_tree().get_first_node_in_group("input")
	if ve_skupine != null:
		_vstup = ve_skupine
		return _vstup
	var rodic: Node = get_parent()
	if rodic != null:
		var uzel: Node = rodic.get_node_or_null("Input")
		if uzel != null and uzel.has_method("smer"):
			_vstup = uzel
		return _vstup
	return null


func _smer_vstupu() -> Vector2:
	"""Směr pohybu: z input komponenty (`smer()`), jinak záložní klávesy/myš."""
	var inp := _vstupni_komponenta()
	if inp != null and inp.has_method("smer"):
		return inp.smer()
	var dir := Vector2.ZERO
	if Input.is_key_pressed(KEY_LEFT) or Input.is_key_pressed(KEY_A):
		dir.x -= 1.0
	if Input.is_key_pressed(KEY_RIGHT) or Input.is_key_pressed(KEY_D):
		dir.x += 1.0
	if Input.is_key_pressed(KEY_UP) or Input.is_key_pressed(KEY_W):
		dir.y -= 1.0
	if Input.is_key_pressed(KEY_DOWN) or Input.is_key_pressed(KEY_S):
		dir.y += 1.0
	# Záložní myš: pravé tlačítko = jdu; mrtvá zóna brání kmitání na místě.
	if dir == Vector2.ZERO and Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT):
		var kurzor: Vector2 = get_global_mouse_position() - global_position
		if kurzor.length() >= DEAD_ZONE:
			dir = kurzor
	return dir


func _chce_bezet(dir: Vector2) -> bool:
	"""Běh: buď to řekne vstupní komponenta, nebo je kurzor daleko od hráče."""
	var inp := _vstupni_komponenta()
	if inp != null and inp.has_method("chce_krok"):
		return bool(inp.chce_krok()) and dir != Vector2.ZERO
	if dir == Vector2.ZERO:
		return false
	var kurzor: Vector2 = get_global_mouse_position() - global_position
	return kurzor.length() >= RUN_DISTANCE


func move(dir: Vector2, delta: float = -1.0) -> void:
	"""Posun hráče o směr `dir` (ve hře, ne v pixelech), za čas `delta`.

	Poslední krok dělá `_step(target)`, který drží hráče mimo zdi (klouzáním
	po jedné ose). Bez mapy se chodí volně – hra musí být hratelná i před
	vygenerováním úrovně.

	`delta < 0` znamená „posun o JEDEN krok" – to používají testy, které
	potřebují měřitelný posun, ale nesmějí čekat na snímek. Je to schválně
	viditelný default, ne skrytá konstanta: kdo volá `move(dir)` bez času,
	dostane přesně jeden krok `SPEED/60`.

	S `delta >= 0` se rychlost plynule rozjíždí/brzdí (`ACCEL`/`DECEL`),
	běh ubírá staminu a při vyčerpané stamině je maximální rychlost poloviční.
	"""
	var d := dir
	if d != Vector2.ZERO:
		d = d.normalized()
	# Izometrické osy – viz hlavička souboru (týž poměr jako `level.cell_center`).
	var iso := Vector2((d.x - d.y) * 0.5, (d.x + d.y) * 0.25)
	if iso.length() > 0.0:
		iso = iso.normalized()

	if delta < 0.0:
		# TESTOVACÍ cesta: jeden plný krok. Sem se nesmí dostat vyhlazení.
		velocity = iso * SPEED
		position = _step(position + velocity * (1.0 / 60.0))
		_drz_v_obrazovce()
		return

	# Skutečný tik: cílová rychlost podle chůze/běhu a stavu staminy.
	var cilova_rychlost := SPEED * (1.0 if _bezim else WALK_FACTOR)
	if stamina <= 0.0:
		cilova_rychlost *= 0.5
	var cilova := iso * cilova_rychlost
	# Běh ubírá staminu, chůze ji regeneruje.
	if _bezim and d != Vector2.ZERO:
		stamina = maxf(stamina - STAMINA_RUN_PER_S * delta, 0.0)
	else:
		stamina = minf(stamina + STAMINA_REGEN_PER_S * delta, max_stamina)
	var zmena := ACCEL if cilova.length() > velocity.length() else DECEL
	velocity = velocity.move_toward(cilova, zmena * delta)
	position = _step(position + velocity * delta)
	_drz_v_obrazovce()


func _drz_v_obrazovce() -> void:
	"""Hráč nesmí zmizet z obrazovky (kamera zatím není)."""
	if not is_inside_tree():
		return
	var vp := get_viewport_rect().size
	position.x = clampf(position.x, 8.0, vp.x - 8.0)
	position.y = clampf(position.y, 8.0, vp.y - 8.0)


func _step(target: Vector2) -> Vector2:
	"""Posun se zdi: když je cíl ve zdi, zkusí se projet po jedné ose (klouzání).
	Bez mapy se chodí volně – hra musí být hratelná i před vygenerováním úrovně."""
	if level == null or not level.has_method("is_walkable_at"):
		return target
	if level.is_walkable_at(target):
		return target
	if level.is_walkable_at(Vector2(target.x, position.y)):
		return Vector2(target.x, position.y)
	if level.is_walkable_at(Vector2(position.x, target.y)):
		return Vector2(position.x, target.y)
	return position


# ------------------------------------------------------------------ inventář ----
func add_item(item: Node) -> void:
	"""Vloží předmět do inventáře. Volá `scripts/economy.gd` (nákup)."""
	if item != null and not inventory.has(item):
		inventory.append(item)


func remove_item(item: Node) -> void:
	"""Vybere předmět z inventáře (i když tam není – volající to nemusí řešit).
	Volá `scripts/economy.gd` (prodej)."""
	inventory.erase(item)


func equip(item: Node) -> void:
	"""Nasadí předmět jako vybavený. `hud.gd` z něj čte `equipped`."""
	equipped = item
	add_item(item)


func unequip() -> Node:
	var stary = equipped
	equipped = null
	return stary


# ---------------------------------------------------------------------- smrt ----
func die() -> void:
	"""Smrt: na místě zůstane mrtvola se vším, co hráč nesl, a hráč se vrátí
	na spawn NALOHO (REQ-death: „smrt = ztráta všeho na těle").

	Mrtvola je `Area2D` ve skupině `corpse` – stejný tvar jako mince a truhly
	(`game.gd` je hledá ve skupinách), takže ji scéna najde bez znalosti jména.
	"""
	if not is_inside_tree():
		# Bez stromu není kam mrtvolu přidat a není odkud vzít spawn; stav
		# hráče se i tak vyprázdní, aby nezůstal nesmrtelný s plným inventářem.
		inventory.clear()
		equipped = null
		return

	var neboztik := Area2D.new()
	neboztik.name = "Corpse"
	neboztik.position = position
	neboztik.add_to_group("corpse")
	for item in inventory:
		if item is Node and item.get_parent() == null:
			neboztik.add_child(item)
	get_parent().add_child(neboztik)

	inventory.clear()
	equipped = null

	if level != null and "spawn_cell" in level and level.has_method("cell_center"):
		position = level.cell_center(level.spawn_cell.x, level.spawn_cell.y)

	died.emit()


func flash() -> void:
	var original = modulate
	modulate = Color(1, 0, 0)
	await get_tree().create_timer(0.15).timeout
	modulate = original
