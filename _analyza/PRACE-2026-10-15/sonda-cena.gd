extends SceneTree
# Sonda: co REALNE vrati economy.price() pro predmet z assets/data/items.json?
# Kontext: roadmap done_note u sim.economy tvrdi "price() vraci 0 pro kazdy
# skutecny predmet". Tohle to meri, misto aby se to opakovalo z dokumentu.
# Spusteni:
#   & 'E:\Tools\godot\Godot_v4.7.2-stable_win64_console.exe' --headless --path . `
#     --script res://_analyza/PRACE-2026-10-15/sonda-cena.gd

func _init() -> void:
	var data = JSON.parse_string(FileAccess.get_file_as_string("res://assets/data/items.json"))
	print("[sonda] items.json: ", JSON.stringify(data))
	var ItemScript = load("res://scripts/item.gd")
	var EconomyScript = load("res://scripts/economy.gd")
	for row in data:
		var it = ItemScript.new()
		it.id = row.id
		# POZOR: `get_root().add_child(it)` v SceneTree._init() _ready() NESPUSTI
		# (overeno: nazev zustal prazdny). Proto se _ready() vola PRIMO --
		# sonda tak meri mapovani poli z items.json, ne zivotni cyklus uzlu.
		it._ready()
		var ec = EconomyScript.new()
		var cena = ec.price(it)
		print("[sonda] id=%s  nazev=%s  material=%s  kvalita=%s  trvanlivost=%s  damage=%s  ->  price()=%s" % [
			it.id, it.nazev, it.material, it.kvalita, it.trvanlivost, it.damage, cena])
	print("[sonda] hotovo")
	quit()
