extends Node
# Boj — rozřešení zásahu a poškození.
#
# TVAR SMLOUVY (rozhodnuto 2. 10. 2026, dřív tu nebyl — a proto byla funkce
# rozbitá zároveň dvakrát):
#
#   resolve(attacker, defender) -> Dictionary
#     attacker : Node   uzel kostry s vybavenou zbraní (viz `vybrana_zbran`)
#     defender : Node   uzel kostry s vlastností `armor_rating`
#     vrací     {"hit": bool, "damage": int}
#
#   ODKUD SE BEROU ČÍSLA — z REGISTRU KOMPONENT, ne z uzlu samého:
#     * `Attributes` (scripts/attributes.gd) -> `hodnota("Str"/"Dex")`
#     * `Skills`     (scripts/skills.gd)     -> `hodnota("boj_na_blizko")`
#   Původní verze volala `attacker.hodnota(...)` pro atributy I pro skill na
#   TÉMŽ objektu. Naměřeno 2. 10. 2026 (Python walk nad oběma soubory): žádný
#   objekt v repu neposkytuje `hodnota("Dex")` i `hodnota("boj_na_blizko")`
#   zároveň — `attributes.gd` umí jen Str/Dex/Int, `skills.gd` jen dovednosti.
#   Ať byl `attacker` cokoli, jedna z těch dvojic neexistovala.
#
#   Zbraň: `attacker.vybrana_zbran` (nebo `attacker.zbran`), uzel/předmět
#   s vlastností `damage`. Když tam není, útočí se naprázdno (damage zbraně 0).
#
# DRUHÁ VADA TÉHOŽ SOUBORU (naměřeno 2. 10. 2026): řádky pro zbraň a zbroj
# používaly `has()` — to je **Godot 3 API** a v Godotu 4 neexistuje
# (`Object.has()` tam není). Bylo to ale schované UVNITŘ `if hit:` (řádek 14),
# takže to nespadlo při každém volání, jen při zásahu (hit_chance ≈ 0,5).
# Pravděpodobnostní vada je při testování horší než deterministická.
# V Godotu 4 se vlastnost ptá přes `"jmeno" in uzel` — vzor je v scripts/mining.gd.
#
# TŘETÍ VADA: `resolve()` nikdo nevolal. `combat.gd` je v D1 `done` (úloha #135),
# takže ji conductor znovu nevydá — a `entity.enemy` (#144) na ní závisí.
# Test se ptal jen `has_method("resolve")`, tedy na PŘÍTOMNOST, ne na chování.

const ZAKLADNI_SANCE := 0.5
const SANCE_ZA_BOD := 200.0


func resolve(attacker, defender) -> Dictionary:
	"""Rozhodne, jestli útok zasáhl, a kolik ubere.

	Vrací vždy `{"hit": bool, "damage": int}` — i když chybí komponenty.
	Nikdy nespadne na `has()` (Godot 3 API v Godotu 4 neexistuje).
	"""
	if attacker == null or not (attacker is Node):
		push_error("combat.gd: attacker musí být uzel kostry (dostal jsem %s)"
			% ("null" if attacker == null else type_string(typeof(attacker))))
		return {"hit": false, "damage": 0}

	var atributy = _komponenta("Attributes")
	var skilly = _komponenta("Skills")

	# ČÍSLA SE ČTOU DVĚMA ZPŮSOBY A JE TO ZÁMĚR (naměřeno 2. 10. 2026):
	#   * `attributes.gd` i `skills.gd` MAJÍ `hodnota(...)`, ale každý na něco
	#     jiného — atributy na Str/Dex/Int, skilly na dovednosti.
	#   * `run_tests.gd` má atrapu `TestAtributy`, která `hodnota()` NEMÁ
	#     a vystavuje rovnou `Str` a `Dex` (proto taky testy čtou atributy
	#     přes `Object.get("Str")`). Kdyby combat uměl jen `hodnota()`, spadl by
	#     na `Nonexistent function 'hodnota' in base 'Node (TestAtributy)'`.
	# Proto se zkouší metoda, a když není, čte se vlastnost.
	var dex: int = _cislo(atributy, "Dex")
	var boj: int = _cislo(skilly, "boj_na_blizko")

	var sance: float = ZAKLADNI_SANCE + (dex + boj) / SANCE_ZA_BOD
	var hit: bool = randf() < sance
	if not hit:
		return {"hit": false, "damage": 0}

	var sila: int = _cislo(atributy, "Str")
	var zaklad: int = 1 + sila / 10

	var zbran = _vybrana_zbran(attacker)
	var zbran_poskozeni: int = 0
	if zbran != null and "damage" in zbran:
		zbran_poskozeni = int(zbran.damage)

	var zbroj: int = 0
	if typeof(defender) == TYPE_OBJECT and "armor_rating" in defender:
		zbroj = int(defender.armor_rating)
	elif typeof(defender) == TYPE_DICTIONARY and defender.has("armor_rating"):
		zbroj = int(defender["armor_rating"])

	return {"hit": true, "damage": int(max(0, zaklad + zbran_poskozeni - zbroj))}


func _cislo(komponenta, klic: String) -> int:
	"""Číslo z komponenty: napřed zkus `hodnota(klic)`, pak vlastnost téhož jména.

	PROČ OBOJÍ (naměřeno 2. 10. 2026): `attributes.gd` má `hodnota("Str")`,
	ale testovací atrapa `TestAtributy` v `run_tests.gd` `hodnota()` NEMÁ
	a vystavuje `Str`/`Dex` rovnou (proto taky testy čtou atributy přes
	`Object.get("Str")`). Když combat uměl jen `hodnota()`, spadl na
	`Nonexistent function 'hodnota' in base 'Node (TestAtributy)'`.
	"""
	if komponenta == null:
		return 0
	if komponenta.has_method("hodnota"):
		return int(komponenta.hodnota(klic))
	if klic in komponenta:
		return int(komponenta.get(klic))
	return 0


func _vybrana_zbran(attacker):
	"""Zbraň v ruce útočníka, nebo null. Bere oba zavedené názvy vlastnosti."""
	var zbran = null
	if "vybrana_zbran" in attacker:
		zbran = attacker.vybrana_zbran
	elif "zbran" in attacker:
		zbran = attacker.zbran
	if zbran == null:
		return null
	if "damage" in zbran:
		return zbran
	return null


func _komponenta(id: String):
	"""Komponenta z registru kostry (rodič umí `component(id)`), jinak null.

	Vzor je v scripts/mining.gd:68 — služby se berou z registru RODIČE, nikdy
	z `/root/` (projekt nemá ani jeden autoload).
	"""
	var kostra := get_parent()
	if kostra != null and kostra.has_method("component"):
		return kostra.component(id)
	return null
