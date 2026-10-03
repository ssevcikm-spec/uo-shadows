extends SceneTree
## SNÍMEK: HUD (`scripts/hud.gd`) ZOBRAZUJE SKUTEČNÉ `hp` SKUTEČNÉHO HRÁČE.
##
## PROČ TO EXISTUJE: `AGENTS.md` — „vizuální změnu ověř pohledem (`read_image`),
## ne jen testy. Naměřeno: při izometrické migraci byl hráč překrytý dlaždicemi
## — testy, schéma i assety zelené, chybu našel až snímek."
##
## CO JE NA TOM SNÍMKU SKUTEČNÉ: `level.gd` (SKUTEČNÝ soubor) načte SKUTEČNÝ
## `assets/levels/main.json`, `player.gd` je SKUTEČNÝ hráč a `hud.gd` je
## SKUTEČNÁ komponenta, která čte `hp` z registru. Skládá se jen KOSTRA
## (registr), protože `scripts/game.gd` je pořád monolit (granule
## `engine.shell` není hotová) — hra sama komponentu `hud.gd` neinstancuje.
## Snímek tedy dokládá „HUD zobrazuje HP", ne „hra jako celek je hotová".
##
## NAMĚŘENÁ PAST (první verze tohohle skriptu): `hud.gd` hledá komponenty přes
## `get_parent().component(id)`. Když jsem ho podstrčil pod HRÁČE, `_komponenta`
## vrátila null → `hp` zůstalo 0 a snímek by ukázal „HP: 0" jako hotovou věc.
## HUD musí sedět NAD registrem, ne nad hráčem.
##
## Spuštění:
##   $env:APPDATA = "$PWD\_analyza\a-godot-user"
##   & orchestra\tools\godot\Godot_v4.7.2-stable_win64_console.exe `
##       --path games\uo-shadows --rendering-driver opengl3 `
##       --resolution 960x540 --script res://tests/_snimek-hp.gd

var _kostra: Node = null
var _hud = null
var _snimku := 0
var _zkontrolovano := false
var _vystup := ""


func _initialize() -> void:
	# Cesta do WORKSPACE, ne do `user://` – do přesměrovaného tempu se výstup
	# umí ztratit bez chyby (skill `dsh-prostredi` §4).
	_vystup = ProjectSettings.globalize_path("res://../../_analyza/a-snimek-hp.png")

	var uroven = load("res://scripts/level.gd").new()
	uroven.name = "Level"
	uroven.add_to_group("level")

	_kostra = Node.new()
	_kostra.name = "Kostra"
	_kostra.set_script(load("res://tests/_kostra-snimku.gd"))
	root.add_child(_kostra)
	_kostra.add_child(uroven)

	if not uroven.load_file("res://assets/levels/main.json"):
		print("[snimek] CHYBA: main.json se nenacetl")
		quit(2)
		return
	uroven.vystredni_na_spawn(Vector2(960, 540))
	uroven.build()

	var hrac = load("res://scripts/player.gd").new()
	hrac.name = "Player"
	_kostra.add_child(hrac)
	hrac.position = uroven.cell_center(uroven.spawn_cell.x, uroven.spawn_cell.y)

	_kostra.pridej("Player", hrac)
	_kostra.pridej("Level", uroven)
	var atr = load("res://scripts/attributes.gd").new()
	atr.name = "Attributes"
	_kostra.add_child(atr)
	_kostra.pridej("Attributes", atr)
	var skl = load("res://scripts/skills.gd").new()
	skl.name = "Skills"
	_kostra.add_child(skl)
	_kostra.pridej("Skills", skl)
	var eko = load("res://scripts/economy.gd").new()
	eko.name = "Economy"
	_kostra.add_child(eko)
	_kostra.pridej("Economy", eko)

	_hud = load("res://scripts/hud.gd").new()
	_hud.name = "HudInfo"
	_kostra.add_child(_hud)


func _process(_delta: float) -> bool:
	# `--script` pracuje se stromem až v `_process()`, ne v `_initialize()`.
	_snimku += 1
	if _snimku < 4:
		return false

	if _hud == null:
		print("[snimek] CHYBA: HUD se nepostavil")
		quit(2)
		return true

	# Kontrola a výpis se dělají JEDNOU — bez příznaku se `_process()` volá
	# každý frame a tytéž řádky se vypsaly 5× (naměřeno v prvním běhu).
	if _zkontrolovano == false:
		_zkontrolovano = true
		var hrac = _kostra.get_node_or_null("Player")
		if hrac == null:
			print("[snimek] CHYBA: hrac ve scene neni")
			quit(2)
			return true
		_hud.update()
		var text: String = str(_hud._label.text)
		var prvni: String = text.split("\n")[0]
		print("[snimek] hrac.hp = %s (max_hp %s)" % [str(hrac.hp), str(hrac.max_hp)])
		print("[snimek] HUD prvni radek: %s" % prvni)
		if not prvni.contains("HP: %d" % hrac.hp):
			print("[snimek] CHYBA: HUD neukazuje hp hrace")
			quit(1)
			return true

	if _snimku < 8:
		return false

	var img: Image = root.get_texture().get_image()
	if img == null:
		print("[snimek] CHYBA: obrazek viewportu je null")
		quit(2)
		return true
	var err := img.save_png(_vystup)
	print("[snimek] ulozeno: %s (err=%d, %dx%d)"
		% [_vystup, err, img.get_width(), img.get_height()])
	quit(0 if err == OK else 1)
	return true
