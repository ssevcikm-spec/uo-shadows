extends Area2D
## Hráč: pohyb klávesnicí, kolize s předměty řeší sama scéna.
##
## Záměrně nepoužívá vstupní akce z project.godot – pohyb se čte přímo
## z kláves, takže se projekt dá celý vygenerovat textem a nic se nerozbije
## chybějící definicí akce.

signal collected(what: String)

const SPEED := 130.0

var velocity := Vector2.ZERO
var level: Node2D
# Player state
var hp: int = 100
var max_hp: int = 100
var mana: int = 50
var max_mana: int = 50
var target: Node = null
var inventory: Array = []
var equipped: Node = null


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
	var dir := Vector2.ZERO
	if Input.is_key_pressed(KEY_LEFT) or Input.is_key_pressed(KEY_A):
		dir.x -= 1.0
	if Input.is_key_pressed(KEY_RIGHT) or Input.is_key_pressed(KEY_D):
		dir.x += 1.0
	if Input.is_key_pressed(KEY_UP) or Input.is_key_pressed(KEY_W):
		dir.y -= 1.0
	if Input.is_key_pressed(KEY_DOWN) or Input.is_key_pressed(KEY_S):
		dir.y += 1.0
	if dir != Vector2.ZERO:
		dir = dir.normalized()
	if level != null and level.has_method("iso_position"):
		var iso := Vector2((dir.x - dir.y) * 0.5, (dir.x + dir.y) * 0.25)
		if iso.length() > 0:
			iso = iso.normalized()
		velocity = iso * SPEED
	else:
		velocity = dir * SPEED
	position = _step(position + velocity * delta)
	# drž hráče v obrazovce
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

func flash() -> void:
	var original = modulate
	modulate = Color(1, 0, 0)
	await get_tree().create_timer(0.15).timeout
	modulate = original

# Move the player by a direction vector.
func move(dir: Vector2) -> void:
	var lvl = get_tree().get_first_node_in_group("level")
	var velocity: Vector2 = dir
	if lvl != null and lvl.has_method("is_walkable_at"):
		# Use walkability check; if blocked, keep original velocity logic.
		if not lvl.is_walkable_at(position + dir):
			if lvl.has_method("iso_position"):
				var iso := Vector2((dir.x - dir.y) * 0.5, (dir.x + dir.y) * 0.25)
				if iso.length() > 0:
					iso = iso.normalized()
				velocity = iso * SPEED
			else:
				velocity = dir * SPEED
	position = _step(position + velocity)

# Inventory management
func add_item(item: Node) -> void:
	inventory.append(item)

func remove_item(item: Node) -> void:
	inventory.erase(item)

# Handle player death
func die() -> void:
	var lvl = get_tree().get_first_node_in_group("level")
	if lvl == null:
		return
	# Create corpse node
	var corpse := Area2D.new()
	corpse.name = "Corpse"
	corpse.add_to_group("corpse")
	# Transfer inventory items to corpse
	for it in inventory:
		corpse.add_child(it)
	inventory.clear()
	# Transfer equipped item
	if equipped != null:
		corpse.add_child(equipped)
		equipped = null
	# Add corpse to the scene
	get_parent().add_child(corpse)
	# Move player to spawn cell
	if lvl.has_method("cell_center"):
		var spawn_pos = lvl.cell_center(lvl.spawn_cell.x, lvl.spawn_cell.y)
		position = spawn_pos
	# Reset health
	hp = 0
