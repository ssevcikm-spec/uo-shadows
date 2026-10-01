extends Node2D
## Hlavní scéna startovní šablony: hráč sbírá mince.
##
## Celá scéna se staví programově (žádné ukládané .tscn kromě main.tscn), protože
## tak ji umí agent vygenerovat a upravit jako text. Assety se načítají z
## res://assets – když v projektu ještě nejsou, použije se barevný obdélník,
## takže hra je hratelná i před vygenerováním grafiky.

const COIN_COUNT := 5
const SPRITE_DIR := "res://assets/sprites/"
const SFX_DIR := "res://assets/audio/sfx/"
const LEVEL_DIR := "res://assets/levels/"
const LEVEL_NAME := "main"

var score := 0
var coin_total := COIN_COUNT
var player: Area2D
var level: Node2D
var hud: Label
var dovednosti := {"tezba":0, "kovarstvi":0, "alchymie":0}
var suroviny := {"ruda":0, "ingot":0}
var sfx := {}
var zbran_trvanlivost := 20
var zbran_poskozeni := 5
var cas_dne := 0.25


func _ready() -> void:
	randomize()
	_load_sfx()
	_add_background()
	_add_music()
	_add_level()
	player = _make_player()
	add_child(player)

	var vp := get_viewport_rect().size
	var spots := _coin_spots(vp)
	coin_total = spots.size()
	for i in coin_total:
		add_child(_make_coin(i, spots[i]))

	var npc := _make_npc(vp)
	add_child(npc)
	_add_ui()
	_add_fps_label()
	print("[game] připraveno: hráč + %d mincí, zvuků načteno: %d, dlaždice: %s, úroveň: %s" % [
		coin_total, sfx.size(), "ano" if _texture("tiles/grass") else "ne",
		"%s %d×%d" % [level.level_name, level.width, level.height] if level else "ne"])


func _update_hud() -> void:
	if hud:
		hud.text = "Skóre: %d / %d" % [score, coin_total]
		hud.text += " HODNOTA: %d" % [_hodnota()]

func _add_fps_label() -> void:
	var fps_label := Label.new()
	fps_label.name = "Fps"
	fps_label.add_theme_font_size_override("font_size", 8)
	var vp := get_viewport_rect().size
	fps_label.position = Vector2(vp.x - 60, 4)
	add_child(fps_label)

func _process(delta: float) -> void:
	if has_node("Fps"):
		$Fps.text = "FPS: %d" % Engine.get_frames_per_second()

func _hodnota() -> int:
	return suroviny["ruda"] * 2 + suroviny["ingot"] * 8 + zbran_poskozeni * 5


# ----------------------------------------------------------------- assety ----
func _texture(rel: String) -> Texture2D:
	"""Načte texturu z res://assets/<rel>.png (např. "sprites/player", "tiles/grass")."""
	var path := "res://assets/%s.png" % rel
	if ResourceLoader.exists(path):
		return load(path)
	return null


func _add_background() -> void:
	"""Dlaždicová podlaha z assets/tiles. Bez ní zůstane jen jednolitá barva."""
	var tex := _texture("tiles/grass")
	if tex == null:
		return
	var vp := get_viewport_rect().size
	var bg := TextureRect.new()
	bg.name = "Background"
	bg.texture = tex
	# Pozadí je CELÁ obrazovka, takže musí být vespod (záporné z_index). Když
	# bylo na 0, překrylo mapu úrovně a ta se vůbec nevykreslila – testy přitom
	# prošly, protože dlaždice ve scéně byly. Odhalilo to až měření pixelů
	# (tools/verify-level-render.py): na snímku byla jen tráva.
	bg.z_index = -3
	# Dlaždice se opakuje přes celou obrazovku – proto se vyplatilo, že beze švu.
	bg.texture_repeat = CanvasItem.TEXTURE_REPEAT_ENABLED
	bg.stretch_mode = TextureRect.STRETCH_TILE
	# POZOR: rodič je Node2D, ne Control – anchory se proti němu nepočítají
	# a velikost zůstane nulová (ověřeno: pozadí se pak vůbec nevykreslilo).
	# Velikost se proto nastavuje natvrdo podle viewportu.
	bg.position = Vector2.ZERO
	bg.size = vp
	bg.show_behind_parent = true
	add_child(bg)
	move_child(bg, 0)


func _add_music() -> void:
	"""Hudba na pozadí. Smyčku nastavujeme v kódu, protože import .wav ji sám
	nezapne – a skladby z `forge music` jsou dělané přesně pro smyčku."""
	for track in ["theme", "chiptune", "calm"]:
		var path := "res://assets/audio/music/%s.wav" % track
		if not ResourceLoader.exists(path):
			continue
		var stream = load(path)
		if stream is AudioStreamWAV:
			# Konec smyčky se bere z DÉLKY, ne z velikosti dat: Godot umí .wav
			# importovat komprimovaně (IMA ADPCM), takže přepočet z bajtů vyjde
			# špatně – naměřeno 519 200 místo 1 283 050 vzorků, což by skladbu
			# uřízlo ve dvou pětinách.
			stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
			stream.loop_begin = 0
			stream.loop_end = int(stream.get_length() * stream.mix_rate)
		var player := AudioStreamPlayer.new()
		player.name = "Music"
		player.stream = stream
		player.volume_db = -9.0
		add_child(player)
		player.play()
		print("[game] hudba: %s" % track)
		return


func _clear_entities() -> void:
	"""Smaže všechny entity z mapy."""
	if level:
		# Fade out the current level
		var tween := create_tween()
		tween.tween_property(level, "modulate:a", 0.0, 0.5)
		tween.tween_property(hud, "modulate:a", 0.0, 0.5)
		tween.tween_callback(level.queue_free.bind(level))
	for group in ["coin", "enemy", "chest", "player"]:
		for entity in get_tree().get_nodes_in_group(group):
			entity.queue_free()

func _add_level() -> void:
	"""Postaví mapu z assets/levels/<nazev>.json (generuje `forge level`).
	Když úroveň v projektu není, hra se hraje na holé ploše – pořád hratelná."""
	_clear_entities()
	var path := LEVEL_DIR + LEVEL_NAME + ".json"
	if not FileAccess.file_exists(path):
		print("[game] úroveň %s není – hraju bez mapy" % path)
		return
	var script = load("res://scripts/level.gd")
	if script == null:
		return
	var node := Node2D.new()
	node.name = "Level"
	node.set_script(script)
	node.add_to_group("level")
	if not node.load_file(path):
		node.queue_free()
		return
	# Dlaždice kreslíme pod hráčem, ale NAD pozadím: zdi mají z_index 1 (aby
	# zakryly spáry mezi podlahou), takže hráč musí být výš než -1 + 1. Když
	# mapa skončila pod pozadím, hra vypadala jako prázdná tráva.
	node.z_index = -1
	level = node
	add_child(level)
	# POŘADÍ JE DŮLEŽITÉ: nejdřív se mapa vystředí na spawn a teprve pak se
	# staví dlaždice – `build()` kreslí na pozice, které offset už potřebují.
	# Mapa se vystředí na spawn: bez toho je spawn (17,7) v izometrii na
	# y = 576, tedy POD obrazovkou (viewport je 540), a hráč nevidí sám sebe.
	level.vystredni_na_spawn(get_viewport_rect().size)
	level.build()

	# Fade in the new level
	var tween := create_tween()
	tween.tween_property(level, "modulate:a", 1.0, 0.5)
	tween.tween_property(hud, "modulate:a", 1.0, 0.5)


func _coin_spots(vp: Vector2) -> Array:
	"""Mince stojí tam, kde je vyznačila mapa (středy místností – ověřeně
	průchozí). Bez mapy se rozhodí náhodně jako dřív."""
	var spots: Array = []
	if level:
		spots = level.marker_positions("coin")
	if spots.is_empty():
		for i in COIN_COUNT:
			spots.append(Vector2(randf_range(24.0, vp.x - 24.0), randf_range(24.0, vp.y - 24.0)))
	return spots


func _add_ui() -> void:
	"""HUD s panelem z assets/ui (devět řezů). Bez assetu zůstane holý text."""
	var panel_tex := _texture("ui/panel")
	if panel_tex:
		var panel := NinePatchRect.new()
		panel.name = "HudPanel"
		panel.texture = panel_tex
		panel.patch_margin_left = 4
		panel.patch_margin_top = 4
		panel.patch_margin_right = 4
		panel.patch_margin_bottom = 4
		panel.position = Vector2(4, 4)
		panel.size = Vector2(150, 26)
		panel.show_behind_parent = true
		add_child(panel)

	hud = Label.new()
	hud.name = "Hud"
	hud.position = Vector2(10, 8)
	add_child(hud)
	_update_hud()

	# Help label
	var help_label := Label.new()
	help_label.name = "HelpLabel"
	help_label.text = "E těžba rudy, C tavení, B kování, X použít zbraň, R oprava, M hudba (oddělovačem je středník nebo tečka)"
	help_label.add_theme_font_size_override("font_size", 8)
	var vp := get_viewport_rect().size
	help_label.position = Vector2(4, vp.y - 14)
	add_child(help_label)


func _visual(asset_name: String, fallback: Color, size: Vector2) -> Node2D:
	var holder := Node2D.new()
	var tex := _texture("sprites/%s" % asset_name)
	if tex:
		var s := Sprite2D.new()
		s.texture = tex
		holder.add_child(s)
	else:
		var rect := ColorRect.new()
		rect.color = fallback
		rect.size = size
		rect.position = -size / 2.0
		holder.add_child(rect)
	return holder


func _load_sfx() -> void:
	var dir := DirAccess.open(SFX_DIR)
	if dir == null:
		return
	for f in dir.get_files():
		if not f.ends_with(".wav"):
			continue
		var res_path := SFX_DIR + f
		if ResourceLoader.exists(res_path):
			sfx[f.get_basename()] = load(res_path)


func play_sfx(sfx_name: String) -> void:
	if not sfx.has(sfx_name):
		return
	var p := AudioStreamPlayer.new()
	p.stream = sfx[sfx_name]
	add_child(p)
	p.finished.connect(p.queue_free)
	p.play()


# ------------------------------------------------------------------ entity ----
func _make_player() -> Area2D:
	var p := Area2D.new()
	p.name = "Player"
	p.set_script(load("res://scripts/player.gd"))
	# Start z mapy (spawn), jinak střed obrazovky.
	if level:
		p.position = level.cell_center(level.spawn_cell.x, level.spawn_cell.y)
	else:
		p.position = get_viewport_rect().size / 2.0
	p.z_index = 5
	# Když existuje animace (vygenerovaná přes `forge anim`), hráč se hýbe.
	# Jinak se použije statický sprite, případně barevný obdélník.
	var anim := _animation_visual("walk")
	if anim:
		p.add_child(anim)
	else:
		p.add_child(_visual("player", Color(0.35, 0.85, 1.0), Vector2(10, 10)))
	return p


func _animation_visual(anim_name: String) -> Node2D:
	"""Načte SpriteFrames vygenerované pipeline (assets/<nazev>.tres)."""
	var res_path := "res://assets/%s.tres" % anim_name
	if not ResourceLoader.exists(res_path):
		return null
	var frames = load(res_path)
	if not (frames is SpriteFrames) or not frames.has_animation(anim_name):
		return null
	var s := AnimatedSprite2D.new()
	s.name = "Animation"
	s.sprite_frames = frames
	s.animation = anim_name
	s.play()
	return s


func _make_coin(index: int, pos: Vector2) -> Area2D:
	var c := Area2D.new()
	c.name = "Coin%d" % (index + 1)
	c.add_to_group("coin")
	var shape := CollisionShape2D.new()
	var circle := CircleShape2D.new()
	circle.radius = 5.0
	shape.shape = circle
	c.add_child(shape)
	c.add_child(_visual("coin", Color(1.0, 0.85, 0.2), Vector2(8, 8)))
	c.position = pos
	c.z_index = 3
	c.area_entered.connect(_on_coin_touched.bind(c))
	return c

func _make_npc(vp: Vector2) -> Area2D:
	var n := Area2D.new()
	n.name = "Npc"
	n.add_to_group("npc")
	var shape := CollisionShape2D.new()
	var rect := RectangleShape2D.new()
	rect.size = Vector2(12, 12)
	shape.shape = rect
	n.add_child(shape)
	n.add_child(_visual("player", Color(1.0, 0.84, 0.0), Vector2(12, 14)))
	n.position = vp / 2 + Vector2(60, 0)
	n.z_index = 4
	n.area_entered.connect(_on_npc_touched.bind(n))
	return n


func _on_coin_touched(other: Area2D, coin: Area2D) -> void:
	if other != player or not is_instance_valid(coin) or not coin.is_in_group("coin"):
		return
	score += 1
	play_sfx("coin")
	coin.remove_from_group("coin")
	coin.queue_free()
	_update_hud()
	if score >= coin_total:
		play_sfx("win")

func _on_npc_touched(other: Area2D, npc: Area2D) -> void:
	if other != player:
		return
	if suroviny["ruda"] < 3:
		return
	suroviny["ruda"] -= 3
	suroviny["ingot"] += 1
	play_sfx("click")
	_update_hud()

func _save_state() -> void:
	var cfg := ConfigFile.new()
	cfg.load("user://sandbox.cfg")
	cfg.set_value("stav", "tezba", dovednosti["tezba"])
	cfg.set_value("stav", "kovarstvi", dovednosti["kovarstvi"])
	cfg.set_value("stav", "ruda", suroviny["ruda"])
	cfg.set_value("stav", "ingot", suroviny["ingot"])
	cfg.set_value("stav", "zbran_poskozeni", zbran_poskozeni)
	cfg.set_value("stav", "zbran_trvanlivost", zbran_trvanlivost)
	cfg.save("user://sandbox.cfg")

func _load_state() -> void:
	var cfg := ConfigFile.new()
	var err := cfg.load("user://sandbox.cfg")
	if err != OK:
		return
	dovednosti["tezba"] = cfg.get_value("stav", "tezba", dovednosti["tezba"])
	dovednosti["kovarstvi"] = cfg.get_value("stav", "kovarstvi", dovednosti["kovarstvi"])
	suroviny["ruda"] = cfg.get_value("stav", "ruda", suroviny["ruda"])
	suroviny["ingot"] = cfg.get_value("stav", "ingot", suroviny["ingot"])
	zbran_poskozeni = cfg.get_value("stav", "zbran_poskozeni", zbran_poskozeni)
	zbran_trvanlivost = cfg.get_value("stav", "zbran_trvanlivost", zbran_trvanlivost)
	_update_hud()
