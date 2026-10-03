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
## ============================================================================

signal collected(what: String)
signal died()

const SPEED := 130.0

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
	# POHYB JE JEN TADY – jen se čtou klávesy a volá se smluvní `move()`.
	var dir := Vector2.ZERO
	if Input.is_key_pressed(KEY_LEFT) or Input.is_key_pressed(KEY_A):
		dir.x -= 1.0
	if Input.is_key_pressed(KEY_RIGHT) or Input.is_key_pressed(KEY_D):
		dir.x += 1.0
	if Input.is_key_pressed(KEY_UP) or Input.is_key_pressed(KEY_W):
		dir.y -= 1.0
	if Input.is_key_pressed(KEY_DOWN) or Input.is_key_pressed(KEY_S):
		dir.y += 1.0
	move(dir, delta)


func move(dir: Vector2, delta: float = -1.0) -> void:
	"""Posun hráče o směr `dir` (ve hře, ne v pixelech), za čas `delta`.

	Poslední krok dělá `_step(target)`, který drží hráče mimo zdi (klouzáním
	po jedné ose). Bez mapy se chodí volně – hra musí být hratelná i před
	vygenerováním úrovně.

	`delta < 0` znamená „posun o JEDEN krok" – to používají testy, které
	potřebují měřitelný posun, ale nesmějí čekat na snímek. Je to schválně
	viditelný default, ne skrytá konstanta: kdo volá `move(dir)` bez času,
	dostane přesně jeden krok `SPEED/60`.
	"""
	if delta < 0.0:
		delta = 1.0 / 60.0
	var d := dir
	if d != Vector2.ZERO:
		d = d.normalized()
	# Izometrické osy – viz hlavička souboru (týž poměr jako `level.cell_center`).
	var iso := Vector2((d.x - d.y) * 0.5, (d.x + d.y) * 0.25)
	if iso.length() > 0.0:
		iso = iso.normalized()
	velocity = iso * SPEED
	position = _step(position + velocity * delta)
	# drž hráče v obrazovce
	if is_inside_tree():
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
