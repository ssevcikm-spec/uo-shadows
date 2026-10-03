extends Node
## Zkušební kostra pro snímek: registr komponent (`component(id) -> Node`).
##
## Stejné rozhraní, jaké bude mít `scripts/game.gd` po granuli `engine.shell`
## (docs/ARCHITEKTURA.md:145). `hud.gd` i `save.gd` ho hledají na RODIČI.

var _komponenty := {}


func component(id: String):
	return _komponenty.get(id)


func pridej(id: String, uzel: Node) -> void:
	_komponenty[id] = uzel
