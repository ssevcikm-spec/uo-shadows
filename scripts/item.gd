extends Node
class_name GameItem

var id: String
var nazev: String
var material: String
var trvanlivost: int = 20
var damage: int = 0
var armor_rating: int = 0
var kvalita: int = 0

func _ready() -> void:
    var text := FileAccess.get_file_as_string("res://assets/data/items.json")
    if text.is_empty():
        push_error("items.json nejde načíst")
        return
    var data: Variant = JSON.parse_string(text)
    if typeof(data) != TYPE_ARRAY:
        push_error("items.json není pole")
        return

    for item in data:
        if item.id == id:
            nazev = item.name
            material = item.material if "material" in item else ""
            trvanlivost = item.durability if "durability" in item else 20
            damage = item.damage if "damage" in item else 0
            armor_rating = item.armor_rating if "armor_rating" in item else 0
            kvalita = item.quality if "quality" in item else 0
            break

func use() -> void:
    trvanlivost = max(0, trvanlivost - 1)

func repair() -> void:
    trvanlivost = 20

func broken() -> bool:
    return trvanlivost == 0
