extends Node

var _telesa: Dictionary = {}
var _obsazene: Dictionary = {}
var _cell_w: int = 0
var _cell_h: int = 0
var _offset: Vector2 = Vector2.ZERO


func _ready() -> void:
	var level: Node = get_parent().component("level")
	if level != null:
		_cell_w = level.cell_w
		_cell_h = level.cell_h
		_offset = level.offset


func pridej(teleso: Node, bunka: Vector2i) -> void:
	"""Přidá těleso a jeho buňku do seznamu zabraných buněk."""
	if teleso == null:
		return
	_telesa[teleso] = bunka
	_obsazene[bunka] = teleso


func odeber(teleso: Node) -> void:
	"""Odebere těleso ze seznamu zabraných buněk."""
	if teleso == null or not _telesa.has(teleso):
		return
	var bunka: Vector2i = _telesa[teleso]
	_telesa.erase(teleso)
	_obsazene.erase(bunka)


func je_volno(bunka: Vector2i) -> bool:
	"""Vrátí true, pokud je buňka volná."""
	return not _obsazene.has(bunka)


func z_index_pro(bunka: Vector2i) -> int:
	"""Vrátí z_index pro buňku v izometrické projekci."""
	return (bunka.x + bunka.y) * 2
