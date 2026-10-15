# FAKTA — naměřený faktový list hry `uo-shadows`

> **Co to je:** **faktový list** (snapshot měření), ze kterého se přepisují
> `docs/GDD.md`, `docs/TDD.md`, `docs/ADD.md` a `docs/BRANY-HRY.md`.
> **Není to design ani návrh** — je to seznam čísel s postupem, jak vznikla.
> Kde dokument tvrdí něco o kódu, je tady naměřená hodnota **a** případný rozpor
> (viz `## Rozpory`).
>
> **Datum měření:** 15. 10. 2026, 13:35–14:15 (+02:00).
>
> **HEAD při měření:** `6986b0d` (`6986b0d65cd9fc36d1b828a3b82522af1d6de5eb`,
> commit z 2026-10-12 14:45:06 +0200 „ZASTAVENO: ukoncovaci zaznam…“).
> `git rev-parse --short HEAD` dal `6986b0d` **na začátku i na konci měření**.
>
> ⚠ **Platí k tomuto commitu.** Projekt je zastavený, ale čísla se vážou na
> `6986b0d` — po jakémkoli dalším commitu je nutné je přeměřit, ne je opisovat.
>
> **Čím bylo měřeno:**
> - Godot `4.7.2.stable.official.ed1daf0bf` — `E:\Tools\godot\Godot_v4.7.2-stable_win64_console.exe`
> - Python 3.12.10 (`C:\Users\Ssevc\AppData\Local\Programs\Python\Python312\python.exe`), Pillow 12.3.0
> - git (stav stromu, HEAD, větve)
> - Skripty měření (vše v `_analyza/PRACE-2026-10-15/`, `.py` bez BOM):
>   `mereni-kod.py`, `mereni-assety.py`, `mereni-assety2.py`, `mereni-obsah.py`,
>   `mereni-dotazy.py`, `sonda-cena.gd`
> - Surové výstupy: `vysledek-kod.txt`, `vysledek-assety.txt`,
>   `vysledek-assety2.txt`, `vysledek-obsah.txt`, `vysledek-dotazy.txt`,
>   `raw-test-run.txt`, `raw-test-run2.txt`
>
> **Stav pracovního stromu při měření:** necommitnuté byly jen
> `_analyza/PRACE-2026-10-15/` (můj výstup) a `_analyza/_scratch-soulad.py`
> (**cizí soubor, nesahal jsem na něj**). Nic jiného v repu jsem neměnil,
> necommitoval ani nestageoval.
>
> **Autorita pro řádky:** `splitlines()` (ne `split("\n")`, ne
> `Measure-Object -Line`).

---

## Tabulka faktů

### A. Testy

| # | fakt | hodnota | jak bylo změřeno (přesný příkaz/postup) | zdroj (soubor) | stav |
|---|---|---|---|---|---|
| 1 | Výsledek testů | **113 kontrol, 0 selhání** | `& 'E:\Tools\godot\Godot_v4.7.2-stable_win64_console.exe' --headless --path . --script res://tests/run_tests.gd` (workdir `E:\Workspaces\uo-shadows`), čten **řádek** `[test] N kontrol, M selhání` | `tests/run_tests.gd` | OK |
| 2 | Exit kód testů | **0** | `$LASTEXITCODE` hned po běhu, bez roury (běh 2×, pokaždé 0) | — | OK |
| 3 | Úklidové chyby při běhu testů | `WARNING: 11 ObjectDB instances were leaked at exit`, `ERROR: 1 resources still in use at exit` | tytéž řádky ze surového výstupu `raw-test-run2.txt` | — | OK |
| 4 | Staticky: řádky s `has_method` | **28** | `len([l for l in text.splitlines() if 'has_method' in l])` nad `tests/run_tests.gd` | `tests/run_tests.gd` | OK |
| 5 | Staticky: výskytů `has_method` | **41** | `text.count('has_method')` | `tests/run_tests.gd` | OK |
| 6 | Staticky: výskytů řetězce `_check(` | **155** | `text.count('_check(')` | `tests/run_tests.gd` | OK |
| 7 | Staticky: **volání** `_check(` | **154** | 155 výskytů **− 1 definice** na řádku 46 (`func _check(ok: bool, label: String)`) | `tests/run_tests.gd:46` | OK |
| 8 | ⚠ Statické číslo ≠ počet kontrol z běhu | staticky **154** volání `_check(`, běh hlásí **113** kontrol | obojí výše; rozdíl je daný podmíněnými bloky `has_method` (28 řádků) a přeskočenými kontrolami | `tests/run_tests.gd` | OK |
| 9 | Řádky `tests/` | 5 souborů `.gd`, **1884** řádků celkem; `run_tests.gd` **1569** řádků | `splitlines()` nad každým `tests/*.gd` | `tests/` | OK |
| 10 | Přeskočená kontrola v běhu | `[test] skilly: get() nevrátil hodnoty pro 'tezba'/'kovarstvi' – kontrola začátků na 0 se přeskakuje` | surový výstup běhu | `tests/run_tests.gd` | OK |
| 11 | Testy se pokoušejí načíst neexistující skripty | `res://scripts/npc.gd` a `res://scripts/enemy.gd` → `File not found` (řádky 813 a 819 běhu) | surový výstup běhu | `tests/` | OK |

### B. Kód

| # | fakt | hodnota | jak bylo změřeno (přesný příkaz/postup) | zdroj (soubor) | stav |
|---|---|---|---|---|---|
| 12 | Skripty hry celkem | **16** souborů `scripts/*.gd`, **1716** řádků | `splitlines()` nad každým `scripts/*.gd` (`mereni-kod.py`) | `scripts/` | OK |
| 13 | **Produkční cesta** (dosažitelná řetězem `load()`/`preload()` z `main.tscn`) | **3 soubory, 851 řádků** — `game.gd` 377, `level.gd` 283, `player.gd` 191 | graf: `main.tscn` → `game.gd` → {`level.gd`, `player.gd`}; `mereni-kod.py` §2 | `main.tscn`, `scripts/` | OK |
| 14 | **Mimo produkční cestu** (mrtvá knihovna) | **13 souborů, 865 řádků** | tytéž skripty, na které nevede žádné `load()`/`preload()` z `main.tscn` | `scripts/` | OK |
| 15 | Seznam mimo produkční cestu | `assist` 17, `attributes` 21, `combat` 127, `crafting` 78, `economy` 47, `hud` 92, `item` 39, `mining` 72, `offline` 57, `registry` 150, `save` 150, `skills` 15, `world` 0 (řádků) | `mereni-kod.py` §2 | `scripts/` | OK |
| 16 | Skript, který je dosažitelný **jen** z mrtvé větve | `item.gd` — referencují ho `crafting.gd` a `save.gd`, oba samy mimo produkční cestu; `game.gd`/`player.gd`/`level.gd` ho nepreloadují | graf `load()`/`preload()` | `scripts/item.gd` | OK |
| 17 | `scripts/world.gd` | **0 bajtů, 0 řádků**; nenačítá ho nikdo; v `run_tests.gd` je zmíněn **0×** | `splitlines()` + graf referencí + `text.count('world.gd')` v testech | `scripts/world.gd` | OK |
| 18 | Kolik z 16 skriptů načtou testy | **15** (všech kromě `world.gd`) | počet zmínek `scripts/<jmeno>` v `run_tests.gd`; `world.gd` = 0 | `tests/run_tests.gd` | OK |
| 19 | Hlavní scéna | `main.tscn` má **1** `ext_resource` — `res://scripts/game.gd`; celá scéna se staví programově | čtení `main.tscn` | `main.tscn` | OK |

**Co dělá který skript jednou větou** (řádky = `splitlines()`):

| soubor | řádků | co dělá | v produkční cestě |
|---|---|---|---|
| `game.gd` | 377 | Hlavní scéna: postaví pozadí, mapu, hráče, mince, NPC, HUD a FPS label; drží i druhé (nepoužité) ukládání `user://sandbox.cfg` | ano |
| `level.gd` | 283 | Mapa úrovně z `assets/levels/*.json` — izometrická projekce, dlaždice, markery, průchodnost | ano |
| `player.gd` | 191 | Hráč: stav (hp/mana/cíl), inventář, pohyb po ose dlaždic, smrt | ano |
| `registry.gd` | 150 | Registr komponent, pevný tik simulace 50 ms, fronty příkazů a událostí | ne |
| `save.gd` | 150 | Ukládání/načtení stavu přes `ConfigFile` do `user://save.cfg` z komponent registru | ne |
| `combat.gd` | 127 | Boj — rozřešení zásahu a poškození | ne |
| `hud.gd` | 92 | HUD: HP, atributy, dovednosti, zlato, vybavená zbraň | ne |
| `crafting.gd` | 78 | Výroba — tavení, kování, oprava | ne |
| `mining.gd` | 72 | Těžba a dřevorubectví — výtěžek podle skillu a obtížnosti suroviny | ne |
| `offline.gd` | 57 | Rozřešení offline činnosti s denním stropem | ne |
| `economy.gd` | 47 | Ekonomika — `gold()`, `price()`, `buy()`, `sell()`; `class_name Economy` | ne |
| `item.gd` | 39 | Předmět — `id`/`nazev`/`material`/`trvanlivost`/`damage`/`armor_rating`/`kvalita`, `use()`/`repair()`/`broken()`, `class_name GameItem` | ne |
| `attributes.gd` | 21 | Atributy Str/Dex/Int (start 10) a `derived()` (damage, hit_chance, attack_speed, mana, carry) | ne |
| `assist.gd` | 17 | Pravidla asistence — `add_rule(trigger, action)`, `evaluate(player)` | ne |
| `skills.gd` | 15 | Dovednosti (slovník 4 skillů, strop 100), `add()`, `hodnota()` | ne |
| `world.gd` | 0 | **Prázdný soubor** — granule `world.nodes` ho nikdy nenaplnila | ne |

### C. Brány

| # | fakt | hodnota | jak bylo změřeno (přesný příkaz/postup) | zdroj (soubor) | stav |
|---|---|---|---|---|---|
| 20 | `check-schema.py` | **exit 0**; výstup: `projekce=izometricka, dlaždice=[96, 48], viewport=[960, 540]`, `mapa main.json cell=96 viewport=[960, 540] mřížka=[30, 16]`, `tiles/manifest.json: tile_size=[96, 48]`, `sprity: zkontrolováno 8, nesedí 0` | `$env:PYTHONIOENCODING='utf-8'; python .forge\check-schema.py .` | `.forge/check-schema.py` | OK |
| 21 | `check-schema.py` — **slepé místo** | `scripts/world.gd existuje, ale jeho buňku se NEPODAŘILO přečíst – kontrola „dvě různé představy o mřížce“ NEPROBĚHLA` | tytéž řádky výstupu brány | `.forge/check-schema.py` | OK |
| 22 | `check-wiring.py` | **exit 0**; `zkontrolováno funkcí: 97 v 16 souborech` | `$env:PYTHONIOENCODING='utf-8'; python .forge\check-wiring.py .` | `.forge/check-wiring.py` | OK |
| 23 | `check-wiring.py` — hlášený mrtvý kód | 4 poznámky: `game.gd: _save_state()` a `_load_state()` nikde volané; `player.gd: unequip()` a `flash()` nikde volané | tytéž řádky výstupu brány | `.forge/check-wiring.py`, `scripts/game.gd:355,366`, `scripts/player.gd` | OK |
| 24 | `check-assets.py` | **exit 0**; `8` spritů OK, všechny `okraj 0 %`, `děry 0`; poznámky: „animace chůze v projektu není – přeskočeno“, „hudba ve hře není – měření hudby přeskočeno“ | `$env:PYTHONIOENCODING='utf-8'; python .forge\check-assets.py .` | `.forge/check-assets.py` | OK |
| 25 | `check-assets.py` — naměřené rozměry a barvy | player 38×95 / 1103 barev; npc 38×95 / 985; enemy 79×64 / 2899; ore 54×48 / 1614; chest 50×48 / 1911; weapon 42×48 / 125; potion 17×32 / 260; coin 26×24 / 471; poměry coin/player 0.25× | tytéž řádky výstupu brány | `.forge/check-assets.py` | OK |

### D. Assety

| # | fakt | hodnota | jak bylo změřeno (přesný příkaz/postup) | zdroj (soubor) | stav |
|---|---|---|---|---|---|
| 26 | PNG v `assets/sprites/` (rekurzivně) | **16** — 8 přímo v `assets/sprites/`, 8 v `assets/sprites/items/` | `sorted(Path('assets/sprites').rglob('*.png'))` | `assets/sprites/` | OK |
| 27 | PNG v `assets/tiles/` | **7** (`brick, dirt, grass, sand, stone, tileset, water`) | `glob` | `assets/tiles/` | OK |
| 28 | PNG v `tools/blender/sprites/` (rekurzivně) | **258** — 130 v kořeni, 128 v `npc/` | `rglob` | `tools/blender/sprites/` | OK |
| 29 | **Kolik PNG z `assets/sprites/` hra skutečně odkazuje** | **2 z 16** — `player.png` a `coin.png` | statická extrakce jmen z kódu, který je načítá: `_visual("…")` v `game.gd` dává jen `player` (řádky 283 a 327) a `coin` (řádek 312); `_texture()` bere `sprites/<jmeno>` | `scripts/game.gd:228,283,312,327` | OK |
| 30 | Proč zrovna tato dvě — doložení | `game.gd:10` `SPRITE_DIR := "res://assets/sprites/"`, `game.gd:230` `_texture("sprites/%s" % asset_name)`; jediná volání `_visual` mají literály `"player"`, `"coin"`, `"player"` | čtení `game.gd` | `scripts/game.gd` | OK |
| 31 | Které PNG v `assets/sprites/` hra **NEODEbÍRÁ** | **14 z 16**: `chest, enemy, npc, ore, potion, weapon` a všech 8 v `items/` | doplněk k #29 | `assets/sprites/` | OK |
| 32 | `assets/sprites/npc.png` se ve hře nepoužije | NPC v `game.gd:327` volá `_visual("player", …)` — tedy sprite **hráče**, ne `npc.png` | čtení `game.gd:318–331` | `scripts/game.gd:327` | OK |
| 33 | Dlaždice, které hra načte | **4 ze 7**: `brick`, `stone`, `dirt` (z `main.json` → `tiles`), `grass` (pozadí, `game.gd:84`) | `main.json` `tiles={"0":"brick","1":"stone","2":"dirt"}`, `grid` obsahuje jen znaky `0,1,2`; `level.gd` `TILE_DIR + tile_name + ".png"`; `game.gd` `_texture("tiles/grass")` | `assets/levels/main.json`, `scripts/level.gd:223`, `scripts/game.gd:84` | OK |
| 34 | Nepoužité dlaždice | **3 ze 7**: `sand`, `water`, `tileset` | doplněk k #33 (měřeno, ne odhad) | `assets/tiles/` | OK |
| 35 | Kolik PNG z `tools/blender/sprites/` hra odkazuje | **0 z 258** | prohledal jsem `scripts/`, `assets/`, `main.tscn`, `project.godot`, `export_presets.cfg`: **žádný** z nich neodkazuje na konkrétní PNG z `tools/blender/sprites/` ani ho nenačítá. Jediná zmínka v produkčních datech je **popisná poznámka** v `assets/spec.json` (`_stav`), která vypisuje, co pipeline vyrobila — nic se podle ní nenačítá | `assets/spec.json` (`_stav`) | OK |
| 36 | `tools/blender/sprites/` = meziprodukt, ne herní obsah | 128 = 4 vrstvy × 4 směry × 8 framů; producent je `tools/blender/postprocess.py` (`OUT = tools/blender/sprites`) | čtení `postprocess.py:8`, počty souborů | `tools/blender/postprocess.py` | OK |
| 37 | **HANDOFF.md:170 ověřeno — `assets/sprites/player.png` je pixel-identický složenině vrstev `d0_f1`** | **ANO, True** — `sha256(RGBA bytes)` cíle i složeniny `38743559754d93e5b19cfaee6d132eac5651f1a36441cce0dfd24ca2f6d2bdb0` | složení `body_d0_f1 + legs_d0_f1 + torso_d0_f1 + weapon_d0_f1` přes `alpha_composite` v pořadí z `postprocess.py:53`; obojí 128×128; porovnání `tobytes()` | `assets/sprites/player.png`, `tools/blender/sprites/*_d0_f1.png`, `tools/blender/postprocess.py:50–55` | OK |
| 38 | Totéž pro `npc.png` | **ANO, True** — `sha256` obou `2122afa7ea3dfc66ac9f7cb43839724911408366e133ce37d1e044813292806a` | vrstvy z `tools/blender/sprites/npc/*_d0_f1.png` | `assets/sprites/npc.png` | OK |
| 39 | Duplicity v `assets/sprites/` (shodný hash, jiné jméno) | **6 dvojic**: `coin`=`items/coin_final`, `chest`=`items/chest_final`, `enemy`=`items/slime_final`, `ore`=`items/ore_final`, `potion`=`items/potion_final`, `weapon`=`items/sword_final` | `sha256` všech 16 PNG, seskupení podle hashe | `assets/sprites/` | OK |
| 40 | Duplicity kořen vs. `npc/` v `tools/blender/sprites/` | **64 byte-identických** dvojic, **64 se liší** (liší se `legs_*` a další), navíc v kořeni `_compare.png` a `_player_vs_npc.png` | `sha256` 130 + 128 PNG | `tools/blender/sprites/` | OK |
| 41 | Skutečné rozměry PNG v `assets/sprites/` | player 128×128, npc 128×128, enemy 96×96, ore 64×64, chest 64×64, weapon 64×64, potion 48×48, coin 32×32 — **všechny sedí na `canvas` v `spec.json`** | `PIL.Image.open(f).size` + srovnání s `spec.json` `role[*].canvas` | `assets/sprites/`, `assets/spec.json` | OK |
| 42 | `assets/levels/main.preview.png` | 1435 B, odkazuje ho `assets/levels/manifest.json` (`preview`) | čtení manifestu | `assets/levels/manifest.json` | OK |

### E. Obsah (data, mapy)

| # | fakt | hodnota | jak bylo změřeno (přesný příkaz/postup) | zdroj (soubor) | stav |
|---|---|---|---|---|---|
| 43 | `assets/data/materials.json` | **4** záznamy (`iron_ore`, `wood`, `stone`, `iron_ingot`), klíče `id, name, difficulty` | `json.loads` + `len()` | `assets/data/materials.json` | OK |
| 44 | `assets/data/items.json` | **2** záznamy (`iron_sword`, `iron_armor`), klíče `id, name, durability, damage` (zbroj navíc `armor_rating`) | totéž | `assets/data/items.json` | OK |
| 45 | `assets/data/recipes.json` | **3** záznamy (`smelting`, `kovani_mece`, `kovani_zbroje`), klíče `id, name, inputs, outputs` | totéž | `assets/data/recipes.json` | OK |
| 46 | `assets/data/skills.json` | **4** záznamy (`tezba`, `drevorubectvi`, `kovarstvi`, `boj_na_blizko`), klíče `id, name` | totéž | `assets/data/skills.json` | OK |
| 47 | `assets/data/monsters.json` | **1** záznam (`skeleton`, „Kostlivec"), klíče `id, name, hp, drops` | totéž. **Soubor `creatures.json` v repu NENÍ** — přítel je `monsters.json` | `assets/data/monsters.json` | OK |
| 48 | Rozměry mapy | **30 × 16 = 480 políček**, `cell = 96`, `seed = 648754554` | `main.json` klíče `width`, `height`, `cell`, `seed`; ověřeno i délkou všech 16 řádků `grid` = **30 znaků** | `assets/levels/main.json` | OK |
| 49 | Průchodnost mapy | **109 z 480** políček průchodných, `connectivity = 1.0`, `reachable = 109`, `floor_ratio = 0.2271` | `main.json` → `stats`; nezávisle potvrzeno testem „z každého políčka se dá dojít na spawn (109 z 109)“ | `assets/levels/main.json`, běh testů | OK |
| 50 | Markery mapy | **4** — `spawn` 1, `coin` 2, `exit` 1 | `len(main.json.markers)` + `Counter(type)` | `assets/levels/main.json` | OK |
| 51 | Spawn | políčko **(17, 7)**, na průchozím políčku | test běhu „spawn je na průchozím políčku (17, 7)“ | `assets/levels/main.json`, běh testů | OK |
| 52 | Mapa v souřadnicích světa | 480 dlaždic, izometrie 96×48 px, krok (1,0) = (48, 24) px | běh testů: `[level] main: 30×16 políček, izometricka 96×48 px, dlaždic: 480, značek: 4` | běh testů | OK |
| 53 | `assets/levels/manifest.json` | 1 úroveň (`main.json`, `size [30,16]`, `markers 4`, `connectivity 1.0`) | `json.loads` | `assets/levels/manifest.json` | OK |
| 54 | `assets/tiles/manifest.json` | **6** dlaždic, `tile_size [96, 48]`, `projekce "izometricka"`, `seed 20260930` | `json.loads` | `assets/tiles/manifest.json` | OK |

### F. Plán

| # | fakt | hodnota | jak bylo změřeno (přesný příkaz/postup) | zdroj (soubor) | stav |
|---|---|---|---|---|---|
| 55 | `.forge/roadmap.json` — validita | **JSON validní** (34 977 B, 288 řádků), kořen `{_popis, grains}` | `json.loads` + `json.dumps` nad přečteným obsahem | `.forge/roadmap.json` | OK |
| 56 | Počet granulí | **21**, unikátních id 21, **0 duplicit** | `len(rm["grains"])` | `.forge/roadmap.json` | OK |
| 57 | `done: true` | **16** (z toho `done: false` u 1 granule, `done` chybí u 4) | `[g for g in grains if g["done"] is True]` | `.forge/roadmap.json` | OK |
| 58 | **READY** (nedokončené a všechny `depends_on` jsou `done`) | **4**: `engine.shell`, `world.nodes`, `engine.input`, `world.bodies` | for-cyklus: `unmet = [d for d in deps if d not in doneset]`, ready = `not unmet` | `.forge/roadmap.json` | OK |
| 59 | BLOKOVANÉ | **1**: `entity.move.smooth`, chybí `engine.input` | totéž | `.forge/roadmap.json` | OK |
| 60 | Visící závislosti (odkaz na neexistující id) | **žádné** | množina všech `depends_on` mínus množina všech `id` | `.forge/roadmap.json` | OK |
| 61 | `provides` / `consumes` | **0 granulí má `provides`, 0 má `consumes`** (0 položek) | klíče granul: `acceptance, depends_on, done, done_note, id, kind, model, owns, prompt, size_lines, title` | `.forge/roadmap.json` | OK |
| 62 | `acceptance` | **21 granulí, 43 položek** | `len([g for g in grains if g.get("acceptance")])`, součet délek | `.forge/roadmap.json` | OK |
| 63 | `owns` | **21** granulí (každá granule = jeden soubor) | totéž | `.forge/roadmap.json` | OK |
| 64 | `size_lines` / `model` | `size_lines` u **15**, `model` u **10** granulí | totéž | `.forge/roadmap.json` | OK |

### G. Konfigurace

| # | fakt | hodnota | jak bylo změřeno (přesný příkaz/postup) | zdroj (soubor) | stav |
|---|---|---|---|---|---|
| 65 | Název projektu a hlavní scéna | `config/name="uo-shadows"`, `run/main_scene="res://main.tscn"`, `config/features=PackedStringArray("4.7")` | čtení `project.godot` | `project.godot` | OK |
| 66 | **Autoloady** | **0** — sekce `[autoload]` v `project.godot` **není** | `'[autoload]' in text` → `False` | `project.godot` | OK |
| 67 | **`input/*` akce** | **0** — žádná akce není definovaná; sekce `[input]` obsahuje jen `input_devices` | regex `^input/` nad `project.godot` | `project.godot` | OK |
| 68 | Jak hra čte vstup, když akce nejsou | přímo klávesami: `player.gd` volá `Input.is_key_pressed(KEY_W/A/S/D)` a `KEY_UP/DOWN/LEFT/RIGHT` (8 volání) | extrakce `Input\.[A-Za-z_]+\([^)]*\)` ze `scripts/*.gd` | `scripts/player.gd` | OK |
| 69 | Okno a vykreslování | viewport 960×540, `stretch/mode="viewport"`, `aspect="keep"`, `rendering_method="mobile"`, `default_texture_filter=0` (Nearest), `physics_ticks_per_second=60` | čtení `project.godot` | `project.godot` | OK |
| 70 | `export_presets.cfg` — presety | **3**: `name="Windows Desktop"`, `name="Web"`, `name="Linux"`; cíle `build/windows/game.exe`, `build/web/index.html`, `build/linux/game.x86_64`; `export_filter="all_resources"` u všech | regex `^name=` / `^export_path=` | `export_presets.cfg` | OK |
| 71 | `export_presets.cfg` — název hry | `application/product_name="uo-shadows"` (řádek 44), `application/company_name="ssevcikm-spec"` (řádek 43); klíč `application/config/name` tam **není** | grep `name=` | `export_presets.cfg:43–44` | OK |
| 72 | `assets/spec.json` — rozměry | `viewport [960, 540]`, `tile {sirka 96, vyska 48, pomer "2:1"}` | `json.loads` | `assets/spec.json` | OK |
| 73 | `assets/spec.json` — role | **8 rolí**: player (96/128, 4 směry, 8 framů, stín), npc (96/128, 4, 8, stín), enemy (64/96, 4, 4, stín), ore (48/64, 1, 1, stín), chest (48/64, 1, 1, stín), weapon (48/64, 1, 1, bez stínu), potion (32/48, 1, 1, bez), coin (24/32, 1, 1, bez) | `json.loads`; formát `visual_height/canvas, směry, framy, stín` | `assets/spec.json` | OK |
| 74 | `assets/spec.json` — vrstvy | `slot_poradi` **8** slotů (`body, legs, feet, torso, cloak, head, shield, weapon`), `pocatecni_sada` **4** (`body, torso, legs, weapon`), `render_na_vrstvu true`, `tonovani [cloak, torso, legs]` | `json.loads` | `assets/spec.json` | OK |
| 75 | `assets/spec.json` — brány (6 číselných) | `height_tolerance 0.10`, `max_holes 0`, `max_border_opaque 0.05`, `min_silhouette_iou 0.80`, `max_centroid_shift 3.0`, `min_contrast_vs_floor 150` | `json.loads`, klíče bez `_popis` | `assets/spec.json` | OK |
| 76 | `assets/spec.json` — paleta a stín | `paleta.zdroj = null` (mapování na paletu **ZRUŠENO**), `stin {sirka_pomer 0.7, kryti 0.35}`, `styl.technika = 3D model → render do 2D spritu (Blender headless) v 5 směrech` | `json.loads` | `assets/spec.json` | OK |
| 77 | ⚠ Nesoulad „5 směrů“ vs. realita | `spec.json` deklaruje v `styl.technika` **5 směrů**, ale `postprocess.py:12` má `DIRS = 4` a vrstev je 4×4×8 = 128 | čtení obou souborů | `assets/spec.json`, `tools/blender/postprocess.py:12` | OK |

### H. Ukládání

| # | fakt | hodnota | jak bylo změřeno (přesný příkaz/postup) | zdroj (soubor) | stav |
|---|---|---|---|---|---|
| 78 | Cesta ukládání | `user://save.cfg` (`save.gd:19 const SOUBOR`) | čtení `save.gd` | `scripts/save.gd:19` | OK |
| 79 | Potřebné komponenty | `["Attributes", "Skills", "Economy", "Player"]` (`save.gd:20`) | čtení `save.gd` | `scripts/save.gd:20` | OK |
| 80 | Klíče, které `save()` zapisuje | `[attributes] Str, Dex, Int`; `[skills] dovednosti`; `[economy] gold`; `[player] position`; `[inventory] items, equipped_id`; `[world] data` | extrakce všech `cfg.set_value("…", "…")` ze `save.gd` | `scripts/save.gd` | OK |
| 81 | `save()` vrátí `false`, když není co uložit | když jsou **všechny 4** komponenty `null`, zapíše `push_error` a vrátí `false` | čtení `save.gd:31–33`; test „save() bez registru komponent vrátí false“ | `scripts/save.gd` | OK |
| 82 | `load()` vrátí `false`, když není kam stav vrátit | `pouzito == 0` → `push_error` + `return false` | čtení `save.gd:139–141` | `scripts/save.gd` | OK |
| 83 | **Druhá, nepoužitá cesta ukládání** | `game.gd` má vlastní `_save_state()`/`_load_state()` do **`user://sandbox.cfg`**, sekce `[stav]`, klíče `tezba, kovarstvi, ruda, ingot, zbran_poskozeni, zbran_trvanlivost` | extrakce `cfg.set_value` z `game.gd:355–377`; **obě funkce nikdo nevolá** (potvrzeno `check-wiring.py`, poznámka #23) | `scripts/game.gd:355–377` | OK |
| 84 | Kam `user://` skutečně míří | `C:\Users\Ssevc\AppData\Roaming\Godot\app_userdata\uo-shadows\` — obsahuje **jen `logs/`**, **žádný `save.cfg` ani `sandbox.cfg`** | výpis `%APPDATA%\Godot\app_userdata\uo-shadows\` | — | OK |

### I. CI

| # | fakt | hodnota | jak bylo změřeno (přesný příkaz/postup) | zdroj (soubor) | stav |
|---|---|---|---|---|---|
| 85 | `ci.yml` — pořadí kroků (13) | 1 checkout → 2 cache Godotu → 3 `install-godot.sh` → 4 `--import` → 5 **`check-schema.py`** (tvrdá brána, s `pip install pillow`) → 6 **testy** (`run_tests.gd`, `timeout 150`) → 7 **`check-assets.py`** → 8 **`check-wiring.py`** → 9 **smoke** (`--quit-after 120`, `grep "SCRIPT ERROR"`) → 10 **`verify-level-render.py`** (xvfb + opengl3, 20 snímků) → 11 **`vision.mjs --mode presence`** (`continue-on-error: true` — neblokuje) → 12 export Linux + Web → 13 upload artifact | čtení `ci.yml`, kroky v pořadí | `.github/workflows/ci.yml` | OK |
| 86 | `ci.yml` — spouštěče | `push` na `main`, každý `pull_request`, `workflow_dispatch`; `permissions: contents: read`; `timeout-minutes: 30` | čtení `ci.yml:7–20` | `.github/workflows/ci.yml` | OK |
| 87 | `ci.yml` — runner | `ubuntu-latest` (Linux) | čtení `ci.yml:19` | `.github/workflows/ci.yml` | OK |
| 88 | `release.yml` | 152 řádků; export **Windows Desktop + Linux + Web**, zip, Release, nasazení na GitHub Pages (`https://ssevcikm-spec.github.io/uo-shadows/`); bez bran | čtení `release.yml` | `.github/workflows/release.yml` | OK |
| 89 | `agent.yml` | 698 řádků / 35 084 B; 23 kroků (pick-provider → agent → testy → patch → PR → auto-merge) | čtení `agent.yml` | `.github/workflows/agent.yml` | OK |
| 90 | `model-check.yml` | 52 řádků; `providers-check.mjs --no-ping` + `gh issue create` | čtení | `.github/workflows/model-check.yml` | OK |
| 91 | `agent.yml` používá `git add -A` | krok 11: `git add -A` + `git diff --cached --binary > agent.patch` | čtení `agent.yml` | `.github/workflows/agent.yml` | OK |

### J. Chyby a vady naměřené za běhu

| # | fakt | hodnota | jak bylo změřeno (přesný příkaz/postup) | zdroj (soubor) | stav |
|---|---|---|---|---|---|
| 92 | **Chyba při každém načtení scény** | `ERROR: Required object "rp_target" is null.` + backtrace `_add_level (res://scripts/game.gd:181)` ← `_ready (res://scripts/game.gd:33)` | surový výstup běhu testů (`raw-test-run2.txt`) | `scripts/game.gd:33,181` | OK |
| 93 | Proč to vzniká | `_ready()` volá `_add_level()` na řádku **33**, ale `_add_ui()` (které vytvoří `hud`) až na řádku **45**; `_add_level()` na řádku 181 tweenuje `hud`, který je v tu chvíli `null` | čtení `game.gd:28–49` | `scripts/game.gd:33,45,181` | OK |
| 94 | CI tuhle chybu **nezachytí** | krok 9 hledá jen řetězec `SCRIPT ERROR`; naměřená chyba začíná `ERROR:` | srovnání `ci.yml:105` a surového výstupu | `.github/workflows/ci.yml:105` | OK |
| 95 | **`economy.price()` vrací 0 pro oba předměty** | `iron_sword → price()=0`, `iron_armor → price()=0` | sonda `sonda-cena.gd` spuštěná `godot --headless --path . --script res://_analyza/PRACE-2026-10-15/sonda-cena.gd` (volá `item._ready()` přímo, protože `add_child` v `SceneTree._init()` `_ready()` nespustí) | `scripts/economy.gd`, `scripts/item.gd` | OK |
| 96 | Při tom vzniká `SCRIPT ERROR` | `Invalid access to property or key 'quality' on a base object of type 'Node (GameItem)'` na `economy.gd:21` | tytéž běh sondy | `scripts/economy.gd:21` | OK |
| 97 | Nesoulad polí `items.json` vs. co čte kód | `items.json` má `id, name, durability, damage` (+`armor_rating`); `item.gd` čte `material`, `quality`, `armor_rating`; `economy.gd` čte `item.material` a `item.quality` | `json.loads` + čtení `item.gd:22–30`, `economy.gd:14–30` | `assets/data/items.json`, `scripts/item.gd`, `scripts/economy.gd` | OK |
| 98 | Naměřené hodnoty předmětů | `iron_sword`: `nazev="Železný meč"`, `trvanlivost=100`, `damage=15`, `material=""`, `kvalita=0`; `iron_armor`: `nazev="Železná zbroj"`, `trvanlivost=150`, `damage=0`, `material=""`, `kvalita=0` | běh sondy | `scripts/item.gd`, `assets/data/items.json` | OK |
| 99 | `repair()` nastaví trvanlivost natvrdo na 20 | `item.gd:36` `trvanlivost = 20`, ale `items.json` deklaruje `durability` 100 a 150 | čtení `item.gd:35–36` + `items.json` | `scripts/item.gd:36` | OK |
| 100 | Chybějící komponenta `World` za běhu | `ERROR: Couldn't find the given section "world" and key "data"` + `ERROR: save.gd: nad sebou nemám kostru s component(id) – neuložil jsem nic` | surový výstup běhu testů; obojí je **očekávané** chování testů nad prázdným `world.gd` | `scripts/save.gd`, `scripts/world.gd` | OK |
| 101 | Zvuky a hudba | načteno **0** zvuků; `assets/audio/` v repu **neexistuje**; `_add_music()` i `_load_sfx()` tedy nic nenajdou | běh testů (`zvuků načteno: 0`) + výpis `assets/` | `scripts/game.gd:109–132,244–253` | OK |
| 102 | Animace chůze ve hře | `assets/walk.tres` **neexistuje**, `game.gd:290` tedy vrátí `null` → hráč dostane statický `_visual("player")` | test existence cesty + čtení `game.gd:287–300` | `scripts/game.gd:287–300` | OK |
| 103 | Pevný tik registru | `TICK_MS = 50`; 49 + 2 ms dá právě 1 tik; 150 ms dá 3 tiky; `dt = 0,05 s` | běh testů (řádky `[test] OK`) | `scripts/registry.gd`, `tests/run_tests.gd` | OK |

### K. Stav gitu (živě měřeno, ne z dokumentu)

| # | fakt | hodnota | jak bylo změřeno (přesný příkaz/postup) | zdroj (soubor) | stav |
|---|---|---|---|---|---|
| 104 | HEAD a čistota stromu | `6986b0d`; necommitnuté jen `_analyza/PRACE-2026-10-15/` (můj výstup) a `_analyza/_scratch-soulad.py` (**cizí**) | `git rev-parse --short HEAD`, `git status --porcelain` (před i po měření) | — | OK |
| 105 | Větev a upstream | lokální větev `main` **nemá nastavený upstream** (`git status -sb` hlásí jen `## main`) | `git status -sb` | — | OK |
| 106 | Vzdálenost od lokálního `origin/main` | **3 commity** (`git rev-list --count origin/main..HEAD` = 3); lokální ref `origin/main` = `01a9649`, naposledy aktualizovaný pushem **2026-10-08 21:09:09** | `git rev-list --count origin/main..HEAD`, `git reflog show origin/main` | — | OK |
| 107 | Skutečný stav na GitHubu | **NEMĚŘENO** — nebyl spuštěn `git fetch` ani dotaz na GitHub API, takže `origin/main` je jen lokálně známá hodnota | — | — | NEMĚŘENO (bez fetch/API) |

### L. Doplňky po dodatečné kontrole

| # | fakt | hodnota | jak bylo změřeno (přesný příkaz/postup) | zdroj (soubor) | stav |
|---|---|---|---|---|---|
| 108 | ⚠ `SPRITE_DIR` je **mrtvá konstanta** | `game.gd:10 const SPRITE_DIR := "res://assets/sprites/"` má v celém souboru **1 výskyt = jen sám sebe**; sprity se ve skutečnosti načítají přes `_texture("sprites/%s")` → `"res://assets/%s.png"` (`game.gd:76,230`) | `count(c) pro c in [SPRITE_DIR, SFX_DIR, LEVEL_DIR, LEVEL_NAME, COIN_COUNT]` nad `game.gd` | `scripts/game.gd:10,76,230` | OK |
| 109 | Počet mincí neřídí konstanta | `COIN_COUNT := 5` je jen **fallback**; skutečný počet mincí je **2** — bere se z markerů mapy (`_coin_spots()` → `level.marker_positions("coin")`, `main.json` má 2 markery typu `coin`) | běh testů „počet mincí odpovídá očekávání (2, nalezeno 2)“ + `game.gd:184–193` | `scripts/game.gd:9,184–193`, `assets/levels/main.json` | OK |

---

## Rozpory (obě hodnoty + která je autorita)

| # | kde | co tvrdí | co je naměřeno | autorita a proč |
|---|---|---|---|---|
| R1 | `docs/BRANY-HRY.md:87` vs `HANDOFF.md:196` | BRANY: „Pro Godot je v pořádku: naměřeno **57 funkcí v 7 souborech**.“ | **97 funkcí v 16 souborech**, exit 0 | **97/16** — výstup brány samotné (`python .forge/check-wiring.py .`) a `scripts/*.gd` na disku (16 souborů). `HANDOFF.md:196` uvádí totéž (97/16). Číslo 57/7 je ve svém čase mohlo být správné, ale dnes neplatí ani jeden z obou údajů. |
| R2 | `AGENTS.md` hry (souhrn bran) | „staticky je tam **154** volání `_check(`“ | **154 volání** (155 výskytů řetězce − 1 definice na řádku 46) | **154 je SPRÁVNĚ**, potvrzeno. Pozor na past: `text.count('_check(')` dá 155 a vypadá to jako rozpor, ale řádek 46 je definice funkce. |
| R3 | `AGENTS.md` hry | „**28** řádků s `has_method` (**41** výskytů)“ | 28 řádků, 41 výskytů | **potvrzeno beze změny** |
| R4 | `scripts/save.gd:15` (komentář) | „`scripts/world.gd` v repu **není** (smazán při izometrické migraci, commit c651368)“ | `scripts/world.gd` **existuje**, má **0 bajtů** | **Soubor na disku** — soubor existuje, jen je prázdný. Komentář je nepravdivý a je to přesně past „mrtvá větev“: brány na prázdný soubor sahají, ale nic nenaměří (viz #21). |
| R5 | `scripts/save.gd:12–17` (komentář) vs. `save.gd:61–68, 113–130` (kód) | Komentář: „Inventář a stav uzlů světa **uložit nelze**: `scripts/player.gd` inventář nemá“ | Kód inventář **ukládá i načítá** (`[inventory] items`, `equipped_id`), a `player.gd` stav `inventory` **má** (test „player.gd má stav 'inventory'“ prošel) | **Kód** — hlava `save.gd` je neaktuální zbytek z 2. 10. 2026; platí to, co soubor dělá. |
| R6 | `HANDOFF.md:170` | „`assets/sprites/player.png` a `npc.png` jsou **pixel-identické** se složením vrstev `d0_f1`“ | **Potvrzeno** — shodné `sha256` RGBA bajtů u obou (#37, #38) | **Potvrzeno beze změny** |
| R7 | `HANDOFF.md:179` | „vydatelné hned jsou `engine.shell`, `engine.input` a `world.bodies`“ (**3**) | **4** READY: navíc **`world.nodes`** (`done: false`, obě závislosti `world.level` a `data.content` jsou `done`) | **`.forge/roadmap.json`** — READY je vlastnost DAGu, ne výčet v dokumentu. `world.nodes` je zrádná: je READY, ale její soubor `scripts/world.gd` je prázdný (0 B). |
| R8 | `sprites.json` (kořen) vs `assets/spec.json` | `sprites.json` žádá pixel-art: `player size 64, colors 16`, `enemy … size/colors`, popis „méně = víc pixel-art“ | `spec.json`: `paleta.zdroj = null` (mapování na paletu **ZRUŠENO**), `styl` zakazuje „16barevnou paletu, dithering, …“ a role `player` má `visual_height 96` | **`assets/spec.json`** — je to deklarace, proti které měří tvrdá brána `check-schema.py`; `sprites.json` je pozůstatek `forge sprites` a zmiňuje ho **jen `docs/ADD.md`** (žádný kód). |
| R9 | `HANDOFF.md:183` | „`project.godot`, `assets/spec.json`, `export_presets.cfg` = `uo-shadows`“ | Všechny tři obsahují `uo-shadows` a **žádný** `uo-sandbox` (#65, #71). V `export_presets.cfg` je to ale `application/product_name`, klíč `application/config/name` tam **není** | **Potvrzeno** (s upřesněním, že jde o `product_name`) |
| R10 | `HANDOFF.md:161,163` | „**GDD** (495 řádků)“, „**TDD** (796 řádků)“ | `docs/GDD.md` = **524** řádků, `docs/TDD.md` = **802** řádků (`ADD.md` = 392 — to sedí) | **Soubory na disku** (`splitlines()`). `ADD.md` 392 řádků je potvrzeno beze změny. |
| R11 | `assets/spec.json` `styl.technika` vs `tools/blender/postprocess.py:12` | spec: „3D model → render do 2D spritu v **5 směrech**“ | `postprocess.py` má `DIRS = 4`; na disku je 4 vrstvy × 4 směry × 8 framů = 128 souborů | **`postprocess.py`** pro to, co je vyrobené (4 směry); `spec.json` je deklarace záměru. Rozpor je pojmenovaný, ne tichý (#77). |
| R12 | `.forge/roadmap.json` (popis) vs `HANDOFF.md:179` | HANDOFF: „21 granulí (**16 `done`**, `world.nodes` false)“ | 21 granulí, **16 `done: true`** (#56, #57) | **Potvrzeno beze změny** — rozpor je jen ve výčtu READY (viz R7). |
| R13 | `scripts/game.gd:10` (deklarace) vs `game.gd:76,230` (skutečná cesta) | Konstanta `SPRITE_DIR := "res://assets/sprites/"` vypadá jako místo, odkud se sprity berou | Konstanta je **mrtvá** (1 výskyt = deklarace); sprity jdou přes `_texture("sprites/%s")` → `"res://assets/%s.png"` | **Kód, který se skutečně vykoná** (`_texture`). Kdo by při přepisu TDD/ADD citoval `SPRITE_DIR`, popíše cestu, která se nikdy nepoužije. |
| R14 | `docs/BRANY-HRY.md:70–77` | „`check-assets.py` hledá `assets/sprites/walk_*.png`, chůze je po vrstvách v `tools/blender/sprites/`, v `assets/sprites` je 0 souborů `walk_*`“ | **Potvrzeno**: brána sama hlásí „animace chůze v projektu není – přeskočeno“ (#24) a `assets/sprites/` skutečně **0** souborů `walk_*` obsahuje (16 PNG, jiná jména) | **Potvrzeno beze změny** |

---

## Co zůstalo neměřeno

Nula a „neměřeno“ nejsou totéž — tam, kde se nic nezměřilo, stojí `NEMĚŘENO`
s pojmenovaným důvodem. **Nikde v tomhle listu není 0 místo neměřené hodnoty.**

1. **Stav na GitHubu (push, běhy CI, `forge.ok`)** — NEMĚŘENO.
   Důvod: nebyl spuštěn `git fetch` ani dotaz na GitHub API. Naměřeno je jen to,
   co je v lokálním repu (#106: 3 commity před **lokálním** `origin/main`,
   který se naposledy aktualizoval 8. 10. 2026). Čísla o bězích CI nebo o tom,
   zda orchestra vydává, v tomhle listu **nejsou** a nesmí se z něj opisovat.

2. **Vizuální kontrola `vision.mjs`** — NEMĚŘENO.
   Důvod: potřebuje API klíč (`GEMINI_API_KEY`/`DEEPSEEK_API_KEY`) a snímek hry;
   v CI je krok `continue-on-error: true`, takže ani tam nic neblokuje.

3. **`.forge/verify-level-render.py`** (shoda snímku s mapou) — NEMĚŘENO.
   Důvod: potřebuje vyrenderovaný snímek z `xvfb` + softwarového OpenGL; tady se
  .render neprováděl (headless běh snímky nevyrábí).

4. **`.forge/baseline.py`** (LGTM cache, co je vizuálně schválené) — NEMĚŘENO.
   Důvod: není součástí dvou bran, které zadání určilo ke spuštění, a bez snímků
   nemá co porovnávat.

5. **`.forge/node/vision.test.mjs`** (tvrzení „šablona 36/36, hra 28/28“) —
   NEMĚŘENO. Důvod: test se v zadání nepožadoval; tvrzení o jeho výsledku
   pochází z dokumentace a **nebylo ověřeno**.

6. **IoU a posun těžiště animace po framech** — NEMĚŘENO.
   Důvod: `check-assets.py` animaci neměří (poznámka „animace chůze v projektu
   není – přeskočeno“) a ruční měření IoU 0.834–0.908 uvedené v
   `docs/BRANY-HRY.md` **jsem nepřeměřoval** — je to tvrzení dokumentu, ne moje
   číslo. Naměřeno je jen to, že limit `min_silhouette_iou 0.80` se na animaci
   **nikdy neuplatní** (#24).

7. **Chování hry v okně a výkon (FPS)** — NEMĚŘENO.
   Důvod: všechny běhy byly `--headless`; `hra.cmd` jsem nespouštěl.

8. **Zvuk a hudba** — NEMĚŘENO jako vlastnost.
   Důvod: není co měřit — `assets/audio/` v repu neexistuje, takže hudba ani
   zvuky ve hře nejsou (naměřeno je jen to, že soubory chybí, #101).

9. **`assets/spec.json` `_stav` (textové tvrzení o schváleném milníku 1)** —
   NEMĚŘENO. Důvod: je to záznam o schválení uživatelem, ne měřitelná vlastnost
   souboru; naměřeno je jen to, že v souboru ten text je.

10. **`tools/make_iso_tiles.py`, `tools/items_postprocess.py`,
    `tools/blender/build_character.py`** (jsou-li spustitelné a reprodukovatelné)
    — NEMĚŘENO. Důvod: mimo zadání; navíc `postprocess.py` čte
    `tools/blender/raw/`, což v repu **není**, takže pipeline nelze z repa
    zopakovat (naměřeno z kódu, ale běh neověřen).

11. **`.forge/vision-profile.json`, `.forge/providers.json`,
    `.forge/vision/baseline.json`** (obsah) — NEMĚŘENO. Důvod: mimo zadání;
    v seznamu faktů proto o nich není žádné číslo.

12. **`_retired/` (2 soubory) a `_analyza/` (65 souborů)** — NEMĚŘENO.
    Důvod: mimo zadání (faktový list je o hře, ne o archivech); naměřeno je jen
    to, že složky existují a kolik mají souborů.

13. **Cizí soubor `_analyza/_scratch-soulad.py`** — NEMĚŘENO, jen zaznamenáno.
    Důvod: není můj, nečetl jsem ho a neměnil ho (pravidlo: cizí necommitnutou
    práci v pracovním stromě nemažu, nestageuji, neopravuji — jen o ní píšu).

---

## Jak tenhle list použít

- **Číslo bez postupu je tvrzení.** Každý řádek tabulky má v sloupci
  „jak bylo změřeno“ příkaz nebo postup — při přepisu dokumentů **přenášej
  i postup**, ne jen hodnotu.
- **Kde se dokument rozchází s kódem, platí kód** (a je to vypsané v `## Rozpory`
  včetně toho, který soubor je autorita a proč).
- **Statické číslo není výsledek běhu** (#8): počet kontrol se čte z řádku
  `[test] N kontrol, M selhání`, ne z počtu `_check(` v souboru.
- **Po každém dalším commitu tenhle list zastará** — je vázaný na `6986b0d`.
  Přeměřit, ne opisovat.
