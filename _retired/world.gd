extends Node

const cell: int = 32
const RESPAWN_TIME: float = 60.0

var resources: Array = []

func _ready() -> void:
    resources = [
        {"type": "iron_vein", "position": Vector2i(5, 5), "active": true},
        {"type": "tree", "position": Vector2i(10, 10), "active": true},
        {"type": "rock", "position": Vector2i(15, 15), "active": true}
    ]
    for resource in resources:
        var node = Area2D.new()
        node.name = resource["type"]
        node.position = iso_position(resource["position"].x, resource["position"].y)
        add_child(node)
func iso_position(cx: int, cy: int) -> Vector2:
    return Vector2((cx - cy) * cell / 2, (cx + cy) * cell / 4)

func cell_at(pos: Vector2) -> Vector2i:
    var x: int = int((pos.x / (cell / 2) + pos.y / (cell / 4)) / 2)
    var y: int = int((pos.y / (cell / 4) - pos.x / (cell / 2)) / 2)
    return Vector2i(x, y)

func gather(cell: Vector2i) -> bool:
    for resource in resources:
        if resource["position"] == cell and resource["active"]:
            resource["active"] = false
            var timer = Timer.new()
            timer.wait_time = RESPAWN_TIME
            timer.timeout.connect(_respawn_resource.bind(resource))
            add_child(timer)
            timer.start()
            return true
    return false

func _respawn_resource(resource: Dictionary) -> void:
    resource["active"] = true

func is_walkable(pos: Vector2) -> bool:
    var cell_pos = cell_at(pos)
    for resource in resources:
        if resource["position"] == cell_pos and resource["active"]:
            return false
    return true
