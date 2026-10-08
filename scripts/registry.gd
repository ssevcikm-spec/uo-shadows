extends Node
## Registr komponent, pevný tik simulace a fronty příkazů a událostí.
##
## CO TENHLE SOUBOR JE (docs/TDD.md §1.1–1.3, rozhodnutí `R-1`):
##   * **registr komponent** — `component(id)` je JEDINÁ cesta, jak se komponenty
##     hledají. `hud.gd`, `save.gd`, `combat.gd`, `mining.gd` i `offline.gd` volají
##     `get_parent().component(id)` (naměřeno) — proto musí být komponenty DĚTI
##     tohohle uzlu, jinak dostanou `null` a hra poběží s nulami.
##   * **pevný tik 50 ms** — čas vlastní JEN tenhle uzel. Žádná komponenta nesmí
##     mít vlastní časovač ani počítat čas v `_process`, jinak se budou hádat
##     o to, co se stalo dřív (naměřená past z 2. 10. 2026).
##   * **fronty** — simulace nikdy nesahá na obrazovku a zobrazení nikdy nemění
##     stav přímo: jde to přes `push_command()` (vstup → simulace) a
##     `push_event()` (simulace → zobrazení).
##
## PROČ SE AKUMULUJE V MILISEKUNDÁCH: `0.049 + 0.001` v plovoucí řádové čárce
## nemusí dát přesně `0.05`, takže by tik občas vypadl. V milisekundách je
## `49 + 1 = 50` přesně a test tím není plovoucí.
##
## POŘADÍ: `sim_tick(dt)` se volá v POŘADÍ REGISTRACE. Pořadí kroků tiku
## (vstup → příkazy → svět → důsledky → události → zobrazení) určuje kostra
## (`scripts/game.gd`), protože ta komponenty zná; registr jen drží čas.

signal ticked(dt: float)

const TICK_MS := 50
## Ochrana proti spirále smrti: po pauze (okno na pozadí) se dorovnají nejvýš
## tři tiky na snímek, ne stovky. Simulace se tím nezrychluje, jen nezasekne.
const MAX_TICKS_PER_FRAME := 3

var _components: Dictionary = {}
var _order: Array[String] = []
var _commands: Array = []
var _events: Array = []
var _accumulator_ms: float = 0.0
var _ticks: int = 0


# ------------------------------------------------------------------ registr ----
func register(id: String, node: Node) -> void:
	"""Zaregistruje komponentu pod jménem `id` (jména jsou anglicky, `R-3`)."""
	if id.is_empty():
		push_error("registry: register() bez id – komponentu neeviduji")
		return
	if node == null:
		push_error("registry: register(\"%s\") dostal null – neeviduji" % id)
		return
	if _components.has(id) and _components[id] != node:
		push_warning("registry: komponenta \"%s\" se přeregistrovává na jiný uzel" % id)
	if not _components.has(id):
		_order.append(id)
	_components[id] = node


func component(id: String) -> Node:
	"""Vrátí komponentu, nebo `null`. Uvolněná komponenta se OHLÁSÍ a zmizí.

	⚠ DVĚ PASTI, obě naměřené 8. 10. 2026 při psaní testů — a druhá z nich
	je horší, protože vypadá jako správné chování:
	  1. Uvolněný uzel se NESMÍ načítat do typované proměnné
	     (`var node: Node = _components.get(id)`) — Godot vypíše `Trying to assign
	     invalid previously freed instance`, přiřazení selže a proměnná zůstane null.
	  2. Uvolněný uzel se v Godotu 4 **ROVNÁ `null`** — takže test
	     `if hodnota == null: return null` ho „odchytí" dřív, než se stihne zjistit,
	     že je uvolněný. Komponenta by zůstala v registru navěky a nikdo by se
	     nedozvěděl, že zmizela. Proto se ptáme `is_instance_valid()` PRVNÍ
	     a `null` se neporovnává vůbec.
	"""
	if not _components.has(id):
		return null
	var hodnota: Variant = _components[id]
	if not is_instance_valid(hodnota):
		push_warning("registry: komponenta \"%s\" už neexistuje (uvolněná) – mažu ji" % id)
		_components.erase(id)
		_order.erase(id)
		return null
	return hodnota


func components() -> Dictionary:
	"""Kopie registru (volající si nesmí přepsat vnitřní stav)."""
	return _components.duplicate()


func registered_order() -> Array[String]:
	"""Id v pořadí registrace — v tom pořadí dostávají `sim_tick`."""
	return _order.duplicate()


# --------------------------------------------------------------------- tik ----
func advance(delta: float) -> int:
	"""Přičte čas a spustí tolik celých tiků, kolik se do něj vejde.

	Vrací počet provedených tiků. Testy tímhle můžou tiknout bez čekání na snímek
	(`advance(0.15)` = tři tiky), hra to volá z `_process` — čas je jen tady.
	"""
	var hotovo := 0
	if delta <= 0.0:
		return 0
	_accumulator_ms += delta * 1000.0
	while _accumulator_ms >= float(TICK_MS):
		_accumulator_ms -= float(TICK_MS)
		step()
		hotovo += 1
	return hotovo


func step(dt: float = float(TICK_MS) / 1000.0) -> void:
	"""Jeden tik: `sim_tick(dt)` na komponentách, které ho mají, pak signál."""
	for id: String in _order.duplicate():
		var node := component(id)          # hlídá i uvolněné komponenty
		if node != null and node.has_method("sim_tick"):
			node.sim_tick(dt)
	_ticks += 1
	ticked.emit(dt)


func ticks() -> int:
	"""Kolik tiků už proběhlo (měřitelné, ne odhadované)."""
	return _ticks


func _process(delta: float) -> void:
	var strop := float(TICK_MS) * float(MAX_TICKS_PER_FRAME) / 1000.0
	advance(minf(delta, strop))


# ------------------------------------------------------------------- fronty ----
func push_command(cmd: Dictionary) -> void:
	"""Vstup (myš, klávesy, UI) posílá PŘÍKAZ, ne rovnou mění stav."""
	_commands.append(cmd)


func commands() -> Array:
	"""Vrátí frontu příkazů a VYPRÁZDNÍ ji — druhý odběratel dostane prázdno."""
	var out := _commands.duplicate()
	_commands.clear()
	return out


func push_event(ev: Dictionary) -> void:
	"""Simulace hlásí, co se stalo (čísla pro HUD), ne jak to vykreslit."""
	_events.append(ev)


func events() -> Array:
	"""Vrátí frontu událostí a VYPRÁZDNÍ ji."""
	var out := _events.duplicate()
	_events.clear()
	return out
