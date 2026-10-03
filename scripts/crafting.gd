# Crafting system
# Provides functions to smelt, forge and repair items.
# Returns a GameItem instance for created items.
# Uses recipes defined in `assets/data/recipes.json`.
# Quality of crafted items grows with the "kovarstvi" skill:
#   quality = floor(skill_level / 20)
# After each successful craft the "kovarstvi" skill is increased by 1.

extends Node

# Load required scripts
const GameItem = preload("res://scripts/item.gd")
const SkillsScript = preload("res://scripts/skills.gd")
var skills = SkillsScript.new()

# Cache recipes after first load
var _recipes : Array = []

func _load_recipes() -> void:
    if _recipes.size() > 0:
        return
    var text := FileAccess.get_file_as_string("res://assets/data/recipes.json")
    if text.is_empty():
        push_error("recipes.json cannot be loaded")
        return
    var data: Variant = JSON.parse_string(text)
    if typeof(data) != TYPE_ARRAY:
        push_error("recipes.json is not an array")
        return
    _recipes = data

func _find_recipe(recipe_id: String) -> Dictionary:
    _load_recipes()
    for r in _recipes:
        if r.id == recipe_id:
            return r
    push_error("Recipe '%s' not found" % recipe_id)
    return {}

func _calc_quality() -> int:
    var skill_val = skills.hodnota("kovarstvi")
    return int(floor(skill_val / 20.0))

# Smelt: iron_ore -> iron_ingot
func smelt(recipe_id: String) -> Node:
    var recipe = _find_recipe(recipe_id)
    if recipe.is_empty():
        return null
    # Expect a single output
    var output = recipe.outputs[0]
    var item = GameItem.new()
    item.id = output.id
    item.kvalita = _calc_quality()
    # Increase crafting skill
    skills.add("kovarstvi", 1)
    return item

# Forge: ingot + wood -> sword OR ingots -> armor
func forge(recipe_id: String) -> Node:
    var recipe = _find_recipe(recipe_id)
    if recipe.is_empty():
        return null
    var output = recipe.outputs[0]
    var item = GameItem.new()
    item.id = output.id
    item.kvalita = _calc_quality()
    skills.add("kovarstvi", 1)
    return item

# Repair: restores durability using 1 iron_ingot (consumed implicitly)
func repair(item: Node) -> void:
    if not item:
        return
    # Restore durability to its default (handled in GameItem.repair())
    if "repair" in item:
        item.repair()
    else:
        push_error("Provided object does not support repair()")
