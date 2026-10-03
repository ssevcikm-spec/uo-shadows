extends SceneTree
## SONDA POHYBU: měří, po jakých osách se hráč posune, a porovná to s mapou.
##
## PROČ TO EXISTUJE: `player.gd` měl MRTVOU izometrickou větev
## (`if level.has_method("iso_position")` – `level.gd` ji nemá), takže se vždy
## použila větev `else` a hráč chodil **1:1 podle obrazovky**, zatímco dlaždice
## se kreslí **2:1**. Naměřeno 3. 10. 2026:
##
##   | směr            | PŘED (1:1)        | PO (izo osy)      |
##   |---|---|---|
##   | vpravo          | (2,167; 0) sklon 0 | (1,938; 0,969) sklon 0,5 |
##   | vlevo           | (−2,167; 0) sklon 0 | (−1,938; −0,969) sklon 0,5 |
##   | nahoru          | (0; −2,167) svisle | (1,938; −0,969) sklon 0,5 |
##   | vpravo+dolů     | (1,532; 1,532) 45° | (0; 2,167) svisle |
##
## Sklon 0,5 je TÝŽ jako osa dlaždice (`cell_center`: `(cx−cy)·w/2`,
## `(cx+cy)·h/2` → `(48, 24)`), takže hráč teď jde po mapě, ne po obrazovce.
## Rozhodnutí uživatele 3. 10. 2026: „izometrické osy 2:1 – hráč jde po
## dlaždicích".
##
## Sonda to ověřuje PROTI MAPĚ, ne proti zapsané konstantě: sklon si vezme
## z `level.cell_center` (skutečná funkce, kterou hra kreslí). Kdyby se změnil
## poměr dlaždic, sonda spadne – konstanta opsaná do testu by to nezachytila.
##
## Spuštění:
##   $env:APPDATA = "$PWD\_analyza\a-godot-user"
##   & orchestra\tools\godot\Godot_v4.7.2-stable_win64_console.exe --headless `
##       --path games\uo-shadows --script res://tests/_sonda-pohyb.gd

const SPEED := 130.0
const DELTA := 1.0 / 60.0

var _chyb := 0
var _kontrol := 0

const SMERY := [
	# „vpravo“ ve HŘE = izo osa +x dlaždic (ta míří na obrazovce VPRAVO DOLŮ,
	# protože dlaždice je kosočtverec). Naměřeno: (1,938; 0,969), sklon 0,5.
	["vpravo", Vector2(1, 0), Vector2(1, 0.5)],
	["vlevo", Vector2(-1, 0), Vector2(-1, -0.5)],
	["nahoru", Vector2(0, -1), Vector2(1, -0.5)],
	["dolu", Vector2(0, 1), Vector2(-1, 0.5)],
	["vpravo+dolu", Vector2(1, 1), Vector2(0, 1)],
]


func _initialize() -> void:
	var uroven = _uroven()
	if uroven == null:
		quit(2)
		return
	var player_sc = load("res://scripts/player.gd")
	if player_sc == null:
		print("[sonda] CHYBA: player.gd se nenactel")
		quit(2)
		return

	# Sklon si sonda bere Z MAPY – kdyby se dlaždice předělaly, spadne i ona.
	var osa: Vector2 = uroven.cell_center(1, 0) - uroven.cell_center(0, 0)
	var sklon_mapy: float = absf(osa.y / osa.x)
	print("[sonda] osa dlazdice %s -> sklon mapy %.4f" % [str(osa), sklon_mapy])
	_kontrola(is_equal_approx(sklon_mapy, 0.5),
		"mapa je izometrie 2:1 (sklon %.4f)" % sklon_mapy)

	print("[sonda] %-14s %-24s %-24s %s" % ["smer", "posun", "cekano (smer)", "vysledek"])
	for trojice in SMERY:
		var jmeno: String = trojice[0]
		var smer: Vector2 = trojice[1]
		var cekany_smer: Vector2 = trojice[2]

		var hrac = player_sc.new()
		root.add_child(hrac)
		hrac.level = uroven
		hrac.position = uroven.cell_center(2, 2)
		var start: Vector2 = hrac.position
		hrac.move(smer, DELTA)
		var posun: Vector2 = hrac.position - start
		hrac.free()

		var ok_smer: bool = posun.normalized().is_equal_approx(cekany_smer.normalized())
		var ok_delka: bool = is_equal_approx(posun.length(), SPEED * DELTA)
		_kontrola(ok_smer and ok_delka,
			"%s: posun %s (cekano smer %s), |posun| %.4f vs %.4f"
			% [jmeno, str(posun), str(cekany_smer), posun.length(), SPEED * DELTA])

	print("[sonda] %d kontrol, %d chyb" % [_kontrol, _chyb])
	uroven.free()
	quit(1 if _chyb > 0 else 0)


func _kontrola(podminka: bool, popis: String) -> void:
	_kontrol += 1
	if podminka:
		print("[sonda] OK   %s" % popis)
	else:
		_chyb += 1
		print("[sonda] FAIL %s" % popis)


func _uroven():
	"""Atrapa úrovně: mřížka 5×5 celá průchozí, projekce z `level.gd`.

	Musí být průchozí CELÁ, jinak by `_step()` mohl vrátit start a rozdíl
	nula by vznikl z docela jiného důvodu, než jaký sonda měří.
	Atrapa schválně NEMÁ `iso_position` – stejně jako skutečný `level.gd`.
	Právě proto se dřív vždycky použila větev `else` (mrtvá větev).
	"""
	var sc = load("res://scripts/level.gd")
	var lv = sc.new()
	root.add_child(lv)
	lv.cell_w = 96
	lv.cell_h = 48
	lv.projekce = "izometricka"
	lv.offset = Vector2(400, 60)
	lv.width = 5
	lv.height = 5
	lv.grid = PackedStringArray(["11111", "11111", "11111", "11111", "11111"])
	return lv
