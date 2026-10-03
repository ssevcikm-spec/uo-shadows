extends CanvasLayer
# HUD — stavová lišta: HP, atributy, dovednosti, zlato, vybavená zbraň/zbroj.
#
# ODKUD BERE KOMPONENTY (rozhodnuto 2. 10. 2026): z registru kostry —
# `game.gd` vystavuje `component(id) -> Node` (docs/ARCHITEKTURA.md:145).
# Původní verze je hledala ve skupinách "attributes"/"skills"/"economy";
# ty v projektu NIKDO nezakládá (skupiny mají jen `player`, `level`, `coin`,
# `npc`, `chest`, `enemy`), takže lišta ukazovala samé nuly — a testy to
# nepoznaly, protože volají jen `has_method("update")`.
#
# Godot 4 (obojí naměřeno 2. 10. 2026, soubor se kvůli tomu vůbec nepřidal):
#   * `Control.margin_left` NEEXISTUJE → je to `offset_left`/`offset_top`
#     (v Godotu 3 se to jmenovalo `margin_*`). Přiřazení shodí `_ready()`.
#   * `has_property()` NEEXISTUJE → vlastnost se ptá přes `"jmeno" in uzel`.
#     Obejití `hp` přes `has_method("get_hp")` je OD 3. 10. 2026 ODSTRANĚNO:
#     hráč stav má, takže lišta čte `_player.hp` přímo (dřív ukazovala HP: 0).

var _label: Label


func _ready() -> void:
	_label = Label.new()
	_label.name = "HUDLabel"
	_label.position = Vector2(10, 10)
	add_child(_label)
	update()


func update() -> void:
	# Komponenty se hledají při KAŽDÉM update() – ne jednou v `_ready()`.
	# Kdyby je kostra zaregistrovala až po HUDu (pořadí v registru je věc
	# `game.gd`), lišta by jinak zůstala navždy na nulách.
	var _player = _komponenta("Player")
	var _attributes = _komponenta("Attributes")
	var _skills = _komponenta("Skills")
	var _economy = _komponenta("Economy")

	var hp: int = 0
	var vybaveno := ""
	if _player != null:
		# PŘÍMÝ PŘÍSTUP, ŽÁDNÉ OBEJITÍ (od 3. 10. 2026). Do té doby tu byla
		# větev `has_method("get_hp")` a fallback `elif "hp" in _player:` →
		# `hp = 0`. Bylo to OBEJITÍ chybějícího stavu: `player.gd` `hp` neměl
		# (A4 zadání), a tak lišta tiše ukazovala **HP: 0** — což vypadá jako
		# naměřená nula, ale byla to nepřítomnost. `scripts/assist.gd` se
		# přitom na `player.hp` ptal přímo a dostával `SCRIPT ERROR`.
		# `player.gd` stav má, takže obejití jen schovávalo vadu (Úkol 1 bod 4).
		hp = _player.hp
		if _player.equipped != null:
			vybaveno = str(_player.equipped)

	var sila: int = 0
	var obratnost: int = 0
	var inteligence: int = 0
	if _attributes != null:
		sila = _attributes.Str
		obratnost = _attributes.Dex
		inteligence = _attributes.Int

	var tezba: int = 0
	var drevorubectvi: int = 0
	var kovarstvi: int = 0
	var boj: int = 0
	if _skills != null and _skills.has_method("hodnota"):
		tezba = _skills.hodnota("tezba")
		drevorubectvi = _skills.hodnota("drevorubectvi")
		kovarstvi = _skills.hodnota("kovarstvi")
		boj = _skills.hodnota("boj_na_blizko")

	var zlato: int = 0
	if _economy != null and _economy.has_method("gold"):
		zlato = _economy.gold(_player)

	_label.text = (
		"HP: %d\n" % hp
		+ "Str: %d  Dex: %d  Int: %d\n" % [sila, obratnost, inteligence]
		+ "Dovednosti – tezba: %d, drevorubectvi: %d, kovarstvi: %d, boj: %d\n"
			% [tezba, drevorubectvi, kovarstvi, boj]
		+ "Zlato: %d\n" % zlato
		+ "Vybaveno: %s" % (vybaveno if vybaveno != "" else "—")
	)


func _komponenta(id: String):
	"""Komponenta z registru kostry (rodič umí `component(id)`), jinak null.

	Bez kostry (např. když testy instancují HUD samostatně) se vrací null —
	lišta se vykreslí s nulami a nic nespadne."""
	var kostra := get_parent()
	if kostra != null and kostra.has_method("component"):
		return kostra.component(id)
	return null
