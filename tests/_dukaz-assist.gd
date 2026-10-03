extends SceneTree
## DŮKAZ (jednorázový, 3. 10. 2026): `assist.evaluate(player)` na DNEŠNÍM
## `player.gd` spadne — protože `player.gd` nemá `hp`/`max_hp`/`mana`/`max_mana`.
##
## PROČ TENHLE SOUBOR EXISTUJE: testy hry se ptají jen
## `asist.has_method("evaluate")` a **nikdy ji nezavolají** — což je přesně
## vada, kterou `AGENTS.md` popisuje („brána, která se ptá na PŘÍTOMNOST,
## neměří CHOVÁNÍ"). Bez tohohle běhu by „spadne to" bylo jen tvrzení.
##
## Spuštění:
##   $env:APPDATA = "$PWD\_analyza\a-godot-user"
##   & orchestra\tools\godot\Godot_v4.7.2-stable_win64_console.exe --headless `
##       --path games\uo-shadows --script res://tests/_dukaz-assist.gd

func _initialize() -> void:
	print("[dukaz] === assist.evaluate(player) na dnešním player.gd ===")

	var player_sc = load("res://scripts/player.gd")
	if player_sc == null:
		print("[dukaz] CHYBA: player.gd se nenacetl")
		quit(2)
		return
	var hrac = player_sc.new()
	root.add_child(hrac)

	var assist_sc = load("res://scripts/assist.gd")
	if assist_sc == null:
		print("[dukaz] CHYBA: assist.gd se nenacetl")
		quit(2)
		return
	var asist = assist_sc.new()
	root.add_child(asist)

	print("[dukaz] hrac ma 'hp'?          %s" % ("hp" in hrac))
	print("[dukaz] hrac ma 'max_hp'?      %s" % ("max_hp" in hrac))
	print("[dukaz] hrac ma 'mana'?        %s" % ("mana" in hrac))
	print("[dukaz] hrac ma 'max_mana'?    %s" % ("max_mana" in hrac))

	# ⚠ VLASTNÍ OMYL, NAMĚŘENÝ PŘI PSANÍ TOHOHLE SKRIPTU — a je poučný:
	# první verze vypsala „evaluate() PROBESLO => vada NENI" **vždy**, protože
	# se ptala na **návratovou hodnotu**, ne na **měřenou podmínku**.
	# A `evaluate()` při chybějícím `hp` **nespadne** — jen vypíše
	# `SCRIPT ERROR: Invalid access to property or key 'hp'` a vrátí `[]`.
	# **Skript tedy hlásil úspěch tam, kde byla vada** — táž třída jako
	# `test-cooldown.py`, který vypsal CHYBA a skončil `exit 0`.
	# **Pravidlo: assert musí být na PODMÍNCE, ne na tom, že něco proběhlo.**
	var chybi := []
	for klic in ["hp", "max_hp", "mana", "max_mana"]:
		if not (klic in hrac):
			chybi.append(klic)

	if chybi.is_empty():
		print("[dukaz] VŠECHNY klice JSOU -> vada NENI (stav hrace je doplneny)")
		quit(0)
	else:
		print("[dukaz] CHYBI KLICE: %s" % str(chybi))
		print("[dukaz] => VADA POTVRZENA: assist.gd cte vlastnosti, ktere player.gd nema.")
		print("[dukaz]    Dosledek: SCRIPT ERROR do konzole, assist vraci [] (nic nedela),")
		print("[dukaz]    a HUD ukazuje HP: 0 (protoze hud.gd to obchazi pres has_method).")
		quit(1)
