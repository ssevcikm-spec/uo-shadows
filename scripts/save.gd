extends Node
# Ukládání a načtení stavu přes ConfigFile do user://save.cfg.
#
# ODKUD BERE KOMPONENTY (rozhodnuto 2. 10. 2026): z registru kostry —
# `game.gd` vystavuje `component(id) -> Node` (docs/ARCHITEKTURA.md:145).
# Původní verze je hledala ve skupinách "attributes"/"skills"/"economy"/"world",
# které v projektu NIKDO nezakládá. Následek (naměřeno 2. 10. 2026): `save()`
# zapsalo 35 B — jen pozici hráče — a přesto vrátilo `true`. Tichý úspěch nad
# neuloženým stavem je horší než chyba, protože se na něj někdo spolehne:
# když není co uložit, `save()` teď vrátí `false` a ohlásí to.
#
# CO SE UKLÁDÁ: atributy, dovednosti, zlato a pozice hráče — tedy to, co
# komponenty v `main` SKUTEČNĚ poskytují. Inventář a stav uzlů světa uložit
# nelze: `scripts/player.gd` inventář nemá (granule `entity.player` ho nedodala)
# a `scripts/world.gd` v repu není (smazán při izometrické migraci, commit
# c651368). Až je komponenty dostanou, patří sem — a musí se to ohlásit,
# ne tiše vynechat.

const SOUBOR := "user://save.cfg"
const POTREBNE := ["Attributes", "Skills", "Economy", "Player"]


func save() -> bool:
	var cfg := ConfigFile.new()
	var komponenty := {}
	var chybejici: Array = []
	for id in POTREBNE:
		komponenty[id] = _komponenta(id)
		if komponenty[id] == null:
			chybejici.append(id)
	if chybejici.size() == POTREBNE.size():
		push_error("save.gd: nad sebou nemám kostru s component(id) – neuložil jsem nic")
		return false
	if not chybejici.is_empty():
		push_warning("save.gd: chybí komponenty %s – ukládám jen to, co je" % str(chybejici))

	var atributy = komponenty["Attributes"]
	if atributy != null:
		cfg.set_value("attributes", "Str", atributy.Str)
		cfg.set_value("attributes", "Dex", atributy.Dex)
		cfg.set_value("attributes", "Int", atributy.Int)

	var skilly = komponenty["Skills"]
	if skilly != null:
		cfg.set_value("skills", "dovednosti", skilly.dovednosti)

	var ekonomika = komponenty["Economy"]
	var hrac = komponenty["Player"]
	if ekonomika != null and hrac != null:
		cfg.set_value("economy", "gold", ekonomika.gold(hrac))

	if hrac != null and "position" in hrac:
		cfg.set_value("player", "position", hrac.position)
	elif hrac != null:
		# ⚠ Podmíněný zápis musí být VIDĚT (docs/ARCHITEKTURA.md §2.3): kdyby
		# hráč pozici neměl, `load()` by tiše nechal spawn a vypadalo by to
		# jako uložený stav. Atrapa bez pozice je proto OHLÁŠENÁ mez.
		push_warning("save.gd: hráč nemá 'position' – pozici NEUKLÁDÁM")

	# --- Inventory saving ---
	if hrac != null and "inventory" in hrac:
		var inv_data = []
		for item in hrac.inventory:
			if item != null:
				inv_data.append({"id": item.id, "trvanlivost": item.trvanlivost, "kvalita": item.kvalita})
		cfg.set_value("inventory", "items", inv_data)
		if hrac.equipped != null:
			cfg.set_value("inventory", "equipped_id", hrac.equipped.id)

	# --- World state saving ---
	var world = _komponenta("World")
	if world != null and world.has_method("snapshot"):
		var world_data = world.snapshot()
		cfg.set_value("world", "data", world_data)

	return cfg.save(SOUBOR) == OK


func load() -> bool:
	var cfg := ConfigFile.new()
	if cfg.load(SOUBOR) != OK:
		return false

	var pouzito := 0
	var atributy = _komponenta("Attributes")
	if atributy != null and cfg.has_section("attributes"):
		atributy.Str = cfg.get_value("attributes", "Str", atributy.Str)
		atributy.Dex = cfg.get_value("attributes", "Dex", atributy.Dex)
		atributy.Int = cfg.get_value("attributes", "Int", atributy.Int)
		pouzito += 1

	var skilly = _komponenta("Skills")
	if skilly != null and cfg.has_section_key("skills", "dovednosti"):
		skilly.dovednosti = cfg.get_value("skills", "dovednosti", skilly.dovednosti)
		pouzito += 1

	var ekonomika = _komponenta("Economy")
	if ekonomika != null and cfg.has_section_key("economy", "gold"):
		# economy.gd veřejný setter nemá (vlastní ho granule sim.economy),
		# proto se sahá na její stav přímo. Až přibude `set_gold()`, patří sem.
		ekonomika.set("_gold", int(cfg.get_value("economy", "gold", 0)))
		pouzito += 1

	var hrac = _komponenta("Player")
	if hrac != null and cfg.has_section_key("player", "position") and "position" in hrac:
		hrac.position = cfg.get_value("player", "position", hrac.position)
		pouzito += 1
	elif hrac != null and cfg.has_section_key("player", "position"):
		# Týž důvod jako v `save()`: uložená pozice, kterou není komu vrátit,
		# se nesmí zamlčet — jinak `load()` vypadá jako úspěch.
		push_warning("save.gd: uložená pozice je, ale hráč 'position' nemá – nevracím ji")

	# --- Inventory loading ---
	var inv_items = cfg.get_value("inventory", "items", [])
	if inv_items is Array:
		var player = _komponenta("Player")
		if player != null:
			var item_script = preload("res://scripts/item.gd")
			for dict_item in inv_items:
				var itm = item_script.new()
				itm.id = dict_item.get("id", "")
				itm.trvanlivost = dict_item.get("trvanlivost", 20)
				itm.kvalita = dict_item.get("kvalita", 0)
				player.add_item(itm)
			var equipped_id = cfg.get_value("inventory", "equipped_id", "")
			if equipped_id != "":
				for itm in player.inventory:
					if itm.id == equipped_id:
						player.equip(itm)
						break

	# --- World state loading ---
	var world_data = cfg.get_value("world", "data", null)
	if world_data != null:
		var world = _komponenta("World")
		if world != null and world.has_method("restore"):
			world.restore(world_data)

	if pouzito == 0:
		push_error("save.gd: soubor uložený je, ale není kam stav vrátit (chybí komponenty)")
		return false
	return true


func _komponenta(id: String):
	"""Komponenta z registru kostry (rodič umí `component(id)`), jinak null."""
	var kostra := get_parent()
	if kostra != null and kostra.has_method("component"):
		return kostra.component(id)
	return null
