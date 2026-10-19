# TDD — `uo-shadows`: jak je hra postavená a jaké má smlouvy

> **Co tenhle dokument JE:** **zdroj pravdy o technice hry** (technical design
> document) — architektura běhu, vrstvy, **smlouvy komponent s tvarem dat**,
> datové formáty, vlastnictví stavu, výkonnostní rozpočet, ukládání, chybové
> chování a jazyk rozhraní.
>
> **Čím NENÍ:** není design (`docs/GDD.md`), není vzhled (`docs/ADD.md`), není
> plán granulí (`.forge/roadmap.json`) a **není katalog bran** — co která brána
> měří a kde má slepá místa, je jediný zdroj `docs/BRANY-HRY.md`.
>
> **Odkud brát stav:** tenhle dokument je stav techniky. **Zdroj rozhodnutí** je
> `_analyza/DESIGN-REVIZE-2.md` (uzavřená revize vize, 8. 10. 2026); odkazy
> `(§N)` míří tam. **Co má hra dělat**, říká `docs/GDD.md`; **jak vypadá**,
> `docs/ADD.md`; **co se staví**, `.forge/roadmap.json`; **co která brána měří**,
> `docs/BRANY-HRY.md`.
>
> **Platí z něj:** smlouvy komponent (`TDD` §3), vrstvy (`TDD` §2) a vlastnictví
> stavu (`TDD` §5) jsou **závazné** — kdo mění vlastnictví stavu, mění smlouvu,
> ne kód potichu. Známé vady (`TDD` §10) jsou **záznam**, ne závazek k opravě.
>
> **Datum spotřeby:** **čísla o kódu platí k `HEAD = 6986b0d`** (naměřeno
> 15. 10. 2026, postup u každého čísla a v `_analyza/PRACE-2026-10-15/FAKTA.md`) —
> po každém dalším commitu se **přeměřují, ne opisují**. Smlouvy a vrstvy platí
> dál: zestarají rozhodnutím, ne commitem.
>
> **Vzniklo:** 8. 10. 2026 sepsáním z `_analyza/DESIGN-REVIZE-2.md` §11 a §14,
> z `docs/ARCHITEKTURA.md` (18 smluv, 3 s tvarem dat) a **měřením kódu**
> (naměřeno 8. 10. 2026; u každého čísla je řečeno, čím). **Přepsáno
> 15. 10. 2026** podle `_analyza/PRACE-2026-10-15/ROZPORY.md` (`R1`, `R2`,
> `R3`, `R9`, `R12`): status `Assist`, vlastník tiku (nová smlouva `Registry`),
> vlastník `world.gd`, počet skriptů, `Mining.gather` a oddíl bran (`TDD` §9).
>
> **Vlastník a údržba:** dokument patří **hře** (`docs/TDD.md`) — **údržbu má
> ten, kdo mění architekturu běhu nebo smlouvu**, a mění ji **tady**, ne
> v kódu potichu. Historie rozhodnutí (`_analyza/DESIGN-REVIZE-2.md`) se
> needituje.
>
> **Nahrazuje `docs/ARCHITEKTURA.md`** jako zdroj pravdy. `ARCHITEKTURA.md`
> zůstává v repu jako **historie** (nese smlouvy `§2.1`–`2.3` a naměřené
> případy, které se needitují) — viz jeho hlavička.
>
> **Co tenhle dokument NENÍ:** není seznam hotových věcí — kde je hotovo, se
> **měří** (definice hotovo, `GDD` §12).
>
> **Jak se mění:** TDD je **stav** — přepisuje se. Naměřené případy a vady
> (hlavně `TDD` §10) se **needitují**, jen doplňují; co přestalo platit, se
> označí jako **„ve svém čase správné“**, ne maže.

---

## 0. Rozhodnutí, ze kterých TDD vychází

| # | Rozhodnutí | Zdroj |
|---|---|---|
| **`R-1`** | **Architektura běhu:** pevný tik **50 ms** pro simulaci (vykreslování zvlášť), **jeden kořen** s registrem komponent, **simulace oddělená od zobrazení** (zprávy a příkazy místo přímého volání) | §14.1 (uživatel: „Sedí“), §11 |
| **`R-2`** | **Výkonnostní rozpočet:** **60 FPS** při 960×540; **simulace < 2 ms na tik** | §14.2 (rozhodl agent) |
| **`R-3`** | **Jazyk:** klíče, identifikátory a literály rozhraní **anglicky**; texty pro člověka **česky** (i v `assets/data/*.json`) | §14.1 (uživatel: „Klíče anglicky, texty česky“) |
| **`N-2`** | **Osm směrů** až po prototypech — prototyp zůstává u **4 směrů** | §14.1 |
| **`N-9`** | **Paperdoll** až s vrstvenou grafikou | §14.1 |
| **Formáty** | `assets/data/*.json` = obsah; `assets/levels/*.json` = mapa a markery; ukládání = `ConfigFile` do `user://` | §14.2 |
| **Chyby** | chybějící komponenta = `push_error` a **hra zůstane hratelná**; **tichý `return` je zakázaný** | §14.2 |
| **Podmínka cesty B** | simulace **oddělená od zobrazení** a **počítá stejně na všech strojích** (pevný tik, žádné náhody závislé na snímcích) | §11 |

**Cena `R-1` (a proč to není kosmetika):** znamená to **přepsat monolit**
`scripts/game.gd` (**377 řádků**, naměřeno 8. 10. 2026). Granule `engine.shell`
v plánu je; byla blokovaná mrtvou granulí `world.map` (`scripts/world.gd` =
**0 B**), **která je od 8. 10. 2026 z plánu vyřazená** — dnes je `engine.shell`
**READY** (`depends_on` = `engine.registry`, naměřeno 15. 10. 2026
v `.forge/roadmap.json`). Dokud přepis neproběhne, je **10 hotových
komponent mrtvá knihovna**: `hud.gd`, `save.gd`, `combat.gd`, `mining.gd`
a `offline.gd` hledají `get_parent().component(id)`. **Registr už v kódu JE**
(`scripts/registry.gd`, hotový ručně 8. 10. 2026 — viz §3.19), ale **monolit ho
nevolá**, takže v běžící hře dostanou `null` dál. **Zároveň je to podmínka cesty
B** (§11): kdyby se oddělení simulace a zobrazení porušilo, byla by síť přepis
jádra.

**Technika, kterou hra dnes běží** (naměřeno 15. 10. 2026, `HEAD = 6986b0d`;
postup v `_analyza/PRACE-2026-10-15/FAKTA.md` #65–#71) — **nikde jinde to
zapsané není**: **Godot 4.7.2-stable** (`project.godot` → `config/features =
"4.7"`), export **Windows + Web + Linux** (`export_presets.cfg`, tři presety:
`Windows Desktop`, `Web`, `Linux`), `product_name` = `uo-shadows`, okno
**960×540**, **0 autoloadů** a **0 `input/*` akcí** — vstup jde přes
`Input.is_key_pressed` (`scripts/player.gd`, 8×). Tik i vrstvy z toho
vycházejí; kdo hru přenese na jiný engine, mění tenhle odstavec, ne kód.

---

## 1. Architektura běhu

### 1.1 Jeden kořen a registr komponent

- **Kořen = uzel `Main`** (`main.tscn`, dnes jediný uzel typu `Node2D` se
  skriptem `scripts/game.gd`; naměřeno 8. 10. 2026: `main.tscn` má **6 řádků**
  a jediný uzel).
- Kořen **vytvoří komponenty** a **vystaví registr**:
  `component(id: String) -> Node` (vrací `null`, když komponenta není).
- **Id v registru jsou jména komponent** a jsou **anglicky** (`R-3`):
  `Attributes`, `Skills`, `Economy`, `Player`, `World`, `Level`, `Item`, `Npc`,
  `Enemy`, `Mining`, `Crafting`, `Combat`, `Offline`, `Assist`, `Save`, `Hud`.
  **Zdroj:** `save.gd:20` (`POTREBNE = ["Attributes","Skills","Economy","Player"]`)
  a `hud.gd:33–36` tytéž názvy už používají — jsou to **naměřená** id, ne návrh.
- **Komponenta se hledá vždy čerstvá** (`hud.gd:30–32`: „komponenty se hledají
  při KAŽDÉM `update()`, ne jednou v `_ready()`“) — pořadí registrace nesmí
  rozhodovat o tom, jestli lišta ukazuje nuly.
- **Chybějící komponenta se přeskočí a OHLÁSÍ** (`push_error`/`push_warning`) —
  hra zůstane hratelná (§14.2). **Tichý `return` je zakázaný.**

### 1.2 Pevný tik 50 ms a pořadí v rámci tiku

- **Simulace běží v pevném tiku 50 ms (20 Hz)**; vykreslování jde **zvlášť**,
  jak nejrychleji to jde (`R-1`). Pozor: `project.godot` má dnes
  `physics/common/physics_ticks_per_second=60` (naměřeno) — to je **fyzikální
  tik enginu**, ne tik simulace hry; simulace si drží **vlastní akumulátor**
  50 ms, aby byly výsledky **opakovatelné a testovatelné** (stejný vstup → stejný
  výsledek).
- **Tik vlastní registr, ne jednotlivé komponenty.** Čas drží
  **`scripts/registry.gd`** (`TICK_MS` = 50 na `:26`, `advance()` na `:91`,
  `step()` na `:108` — naměřeno 15. 10. 2026); kořen (kostra) ho jen **vytvoří
  a volá** — dnes ho `scripts/game.gd` nevolá (viz §3.19). Komponenta **nesmí**
  mít vlastní `_process`/`_physics_process` s vlastním časem — jinak si každá
  vymyslí svůj čas a **budou se hádat o to, co se stalo dřív** (`VSTUPY` §6).
- **Pořadí v rámci jednoho tiku je závazné:**

  | # | Krok | Kdo to dělá |
  |---|---|---|
  | 1 | **Vstup → příkazy** (myš, klávesy) | kořen (vstupní vrstva) |
  | 2 | **Příkazy se aplikují** (pohyb, těžba, výroba, obchod, použití předmětu) | dotčené komponenty |
  | 3 | **Simulace světa** (infestace, zásobenost, respawn, offline dopočet) | `World` |
  | 4 | **Důsledky** (ceny, zakázky, uznání světa) | `Economy` |
  | 5 | **Události se publikují** (co se stalo, čísla) | kdokoli → fronta |
  | 6 | **Zobrazení se překreslí** (HUD, mapa, stav světa) | `Hud` (+ scéna) |

  **Proč je pořadí závazné:** `V1`–`V5` (GDD §4) se poznají **na obrazovce** —
  kdyby se zobrazení překreslilo dřív než simulace, hráč by viděl **číslo
  o tik staré** a „viditelný růst“ by se rozpadl na náhodu.

### 1.3 Jak spolu mluví: příkazy a události

**Simulace NIKDY nesahá na obrazovku; zobrazení NIKDY nemění stav přímo.**
Komunikace jde přes dvě fronty (`R-1`, `VSTUPY` §6):

```
Příkaz (UI / vstup → simulace)
  { "type": String, … }        – typicky 1–3 další klíče podle typu
  "move"    { "dir": [x, y] }              směr ve hře (ne v pixelech)
  "gather"  { "cell": [cx, cy] }           těžba uzlu na políčku
  "craft"   { "recipe": "smelting" }       výroba podle id receptu
  "trade"   { "order": 3 }                 dodávka zakázce / prodej
  "use_item"{ "id": "bandage" }            použití předmětu (obvaz)
  "equip"   { "id": "iron_sword" }         nasazení / sundání
  "accept_order" { "order": 3 }            přijetí zakázky světa

Událost (simulace → zobrazení)
  { "type": String, … }
  "skill_grew"  { "skill": "tezba", "value": 12 }        číslo pro HUD (V1)
  "item_gained" { "id": "iron_ore", "amount": 1 }
  "world_state" { "infestation": 42, "supply": 58 }      stav světa (V5)
  "order_done"  { "order": 3, "reward": 25 }
  "standing"    { "title": "kovář", "score": 61 }        uznání světa
  "died"        { "corpse": [x, y] }
```

**Pravidla, která z toho plynou:**

1. **Kdo chce změnit stav, pošle příkaz** — i HUD, i test, i budoucí síťová
   vrstva. Tím je síť **vyměnitelná doprava**, ne přepis jádra (§11).
2. **Kdo se ptá na stav, čte komponentu z registru** (ne cizí vnitřek).
3. **Událost není stav.** Kdo přijde pozdě, musí umět stav přečíst
   (`world_state` je i vlastnost `World`, ne jen zpráva) — jinak by se stav
   ztratil s první zmeškanou zprávou.

### 1.4 Determinismus a podmínka cesty B

- **Žádné náhody závislé na snímcích.** Náhodu potřebuje boj (`randf()`),
  vzácná složka těžby a drop — všechny se berou z **jednoho zdroje náhody**,
  který vlastní kořen a je **seedovaný** (dnes: `assets/levels/main.json` má
  `seed`; naměřeno 8. 10. 2026).
- **Pevný tik + stav jako data + příkazy** = simulace počítá **stejně na všech
  strojích**; to je přesně podmínka, kterou §11 určuje jako „skoro zdarma teď,
  přepis jádra později“.
- **Co tím zůstává otevřené:** samotná síťová vrstva (cesta `B`) je **samostatný
  milník** s vlastním rozhodnutím (§11). TDD jen drží to, co by se později
  přepisovalo.

---

## 2. Vrstvy a směry závislostí

| Vrstva | Odpovědnost | Soubory |
|---|---|---|
| **engine** | smyčka, tik, vstup, okno, registr | `main.tscn`, `scripts/game.gd` (kostra), `scripts/registry.gd` (tik a fronty — naměřeno 15. 10. 2026: `TICK_MS`, `advance()`, `push_command()`, `push_event()`; smlouva `Registry` je §3.19) |
| **svět** | mapa, dlaždice, izo projekce, průchodnost, uzly surovin, respawn, stav světa | `scripts/level.gd`, `scripts/world.gd` |
| **entity** | hráč, NPC, nepřítel, předmět | `scripts/player.gd`, `npc.gd`, `enemy.gd`, `item.gd` |
| **simulace** | dovednosti, atributy, řemesla, boj, ekonomika, offline, asistence | `scripts/skills.gd`, `attributes.gd`, `crafting.gd`, `mining.gd`, `combat.gd`, `economy.gd`, `offline.gd`, `assist.gd` |
| **prezentace** | HUD, stav světa na obrazovce | `scripts/hud.gd` |
| **persistence** | ukládání/načítání | `scripts/save.gd` |
| **síť** | vrstva pro cestu `B` (**později**) | `scripts/net.gd` (**soubor v repu není** — vznikne, až se cesta `B` rozhodne) |
| **nástroje** | brány ověřující schéma, assety, zapojení a vzhled | `.forge/*` |

**Pravidlo závislostí:** **shora dolů** (prezentace → simulace → svět → engine),
**žádné kruhy**. **Simulace nezávisí na síti** a **nesahá na obrazovku**.

**Kdo nese izometrickou projekci — a proč jen jeden:** projekci nese
**`level.gd`** (`cell_center()`, `cell_at()`, `je_izometricka()`), protože ji
potřebuje kreslení i kolize. **`world.gd` ji NESMÍ opisovat** — přesně kvůli
druhému číslu mřížky byl starý `world.gd` přesunut do `_retired/` (a jeho
smazaná verze tam dodnes je: `_retired/world.gd`, 47 řádků — naměřeno).

> **⚠ Naměřená past (8. 10. 2026), která se musí hlídat:** `assets/spec.json`
> **nemá klíč `projekce`** — `level.gd:74` udělá `data.get("projekce", {})`, pak
> `:83` usoudí z nerovnosti `cell_w != cell_h` (96 ≠ 48), že jde o izometrii.
> Izometrie je tedy **odvozená, ne deklarovaná**. Není to zatím vada (výsledek
> je správný), ale je to **druhé místo, kde vzniká pravda o projekci** — a přesně
> na tohle má bránu `check-schema.py`.

---

## 3. Smlouvy komponent (19) — s tvarem dat

**Agent volá jen to, co komponenta poskytuje (`provides`), nikdy nečte cizí
vnitřek.** Smlouva bez tvaru dat je jen jméno — a podle jména si agent vymyslí
zbytek. Naměřeno: `ARCHITEKTURA.md` §2 má **18 smluv, tvar dat jen 3**
(`sim.combat`, `Hráč → move`, `Ukládání → pozice`); důsledek byl konkrétní —
`get(attr)` v dokumentu vs. `hodnota(attr)` v kódu, `trade(player, item)` vs.
`buy/sell/gold`, `component(name)`, který **v `scripts/` vůbec není**.

**Dnes (15. 10. 2026) je smluv 19** — přibyla **`Registry`** (`TDD` §3.19): tik,
registr a fronty příkazů a událostí byly do té doby jen v próze §1 a v §5 je
vlastnil **nesprávný soubor** (`game.gd` místo `scripts/registry.gd`).

### 3.0 Vzor zápisu smlouvy (platí pro každou níž)

```
název(argument: Typ) -> NávratovýTyp
  kdo je kdo : co je který argument (role, ne jen jméno)
  odkud čísla: která komponenta drží kterou hodnotu
  vzorec     : výpočet (odkaz na GDD §9)
  acceptance : co test ZAVOLÁ a co musí naměřit – `has_method(…)` NESTAČÍ
```

**Status u každé smlouvy:** `hotovo` = existuje soubor i chování (a je ověřené),
`částečně` = soubor existuje, ale nesplňuje tvar/zdroj dat,
`neexistuje` = soubor v `scripts/` není (naměřeno 8. 10. 2026).

---

### 3.1 `Data` — `assets/data/*.json`

- **poskytuje:** materiály, dovednosti, recepty, nestvůry, předměty
  (+ navrhované `synergies.json`)
- **spotřebovává:** —
- **tvar dat:** soubory jsou **JSON array objektů**; společný klíč je `id`
  (anglicky) a `name` (česky, pro člověka — `R-3`). Konkrétní klíče jsou v §4.1.
- **odkud čísla:** soubor sám; **kód je neopisuje** (nový obsah = nový záznam,
  ne nová granule)
- **acceptance:** každý soubor jde načíst (`FileAccess.get_file_as_string` +
  `JSON.parse_string`) a **každý záznam má `id` a `name`**; test **ZAVOLÁ**
  načtení a ověří počet záznamů, ne jen existenci souboru
- **status:** `hotovo` (5 souborů; naměřeno: obsah v GDD §10 proti dnešním
  4 materiálům / 4 dovednostem / 3 receptům / 1 nestvůře / 2 předmětům)

### 3.2 `Attributes` — `scripts/attributes.gd`

- **poskytuje:** `hodnota(attr: String) -> int`, `derived() -> Dictionary`;
  veřejné vlastnosti `Str`, `Dex`, `Int`
- **spotřebovává:** —
- **tvar dat:**

  | Prvek | Typ | Výchozí | Kdo to čte |
  |---|---|---|---|
  | `Str`, `Dex`, `Int` | `int` | **10** | `hud.gd:56–58`, `save.gd:39–41`, boj, výroba |
  | `hodnota("Str"\|"Dex"\|"Int")` | `int` | — | neznámý klíč vrací **0** (a to je vidět, ne tiché) |
  | `derived()` | `Dictionary` | — | `damage`, `hit_chance`, `attack_speed`, `mana`, `carry` |

- **odkud čísla:** komponenta sama; rozsah **0–100** (GDD §9.4)
- **acceptance:** test **ZAVOLÁ** `hodnota("Dex")` a `derived()`, změní `Str`
  a ověří, že se `derived().damage` **změnil**; `has_method("derived")` NESTAČÍ
- **status:** `hotovo` (`scripts/attributes.gd`, 21 řádků; `derived()` naměřeno)

### 3.3 `Skills` — `scripts/skills.gd`

- **poskytuje:** `add(skill: String, n: int) -> void`, `hodnota(skill: String) -> int`,
  vlastnost `dovednosti: Dictionary`
- **spotřebovává:** —
- **tvar dat:** `Dictionary` klíč = **id dovednosti**, hodnota = `int` 0–100.
  GDD §10 určuje **6 dovedností**; dnes (naměřeno 8. 10. 2026) jsou v kódu
  i v datech **4** a klíče jsou **česky**: `tezba`, `drevorubectvi`, `kovarstvi`,
  `boj_na_blizko`. Chybí `tkani` a `obchod`.
- **odkud čísla:** vzorec růstu a synergie drží **tahle komponenta** (GDD §9.1);
  **jeden zdroj pravdy** — nikdo jiný nesmí `dovednosti` měnit napřímo
  (`save.gd:94` je výjimka, kterou je vidět v §5)
- **acceptance:** test ZAVOLÁ `add("tezba", 5)` a ověří `hodnota("tezba") == 5`;
  pak ZAVOLÁ `add("tezba", 500)` a ověří **strop 100**; a ZAVOLÁ `add("nesmysl", 5)`
  a ověří, že to **nezačne tiše vytvářet novou dovednost**
- **status:** `částečně` (`scripts/skills.gd`, 15 řádků; chybí 2 dovednosti,
  synergie, atrofie)

### 3.4 `Level` — `scripts/level.gd`

- **poskytuje:** `load_file(path) -> bool`, `is_walkable_cell(cx, cy) -> bool`,
  `is_walkable_at(pos) -> bool`, `cell_center(cx, cy) -> Vector2`,
  `cell_at(pos) -> Vector2i`, `marker_positions(type) -> Array`, `markers_of(type)`,
  `walkable_count()`, `reachable_count(from_cell)`, `build() -> void`;
  vlastnosti `grid`, `width`, `height`, `cell_w`, `cell_h`, `offset`,
  `spawn_cell`, `markers`, `stats`
- **spotřebovává:** data levelu (`TDD` §4.2) a schéma z `assets/spec.json`
- **tvar dat:** `grid` = `PackedStringArray` (řádek na řádek, **znak na buňku**:
  `0` = zeď, `1` = podlaha, `2` = chodba); `spawn_cell` = `Vector2i`
- **odkud čísla:** **velikost buňky a projekce se berou ze `spec.json`**, ne
  z mapy — mapa smí deklarovat jen to, co není schema hry
- **acceptance:** test ZAVOLÁ `load_file("res://assets/levels/main.json")`,
  ověří `width`/`height` proti hlavičce a **ZAVOLÁ `cell_center` + `cell_at`
  a ověří, že projekce je vzájemně inverzní**; `has_method("load_file")` NESTAČÍ
- **status:** `hotovo` (`scripts/level.gd`, 283 řádků; mřížka se validuje proti hlavičce — naměřeno
  `level.gd:126–133`)

### 3.5 `World` — `scripts/world.gd`

- **poskytuje:** uzly surovin (`nodes`), `gather(cell) -> Dictionary` (co zdroj
  vydal), `is_walkable(pos) -> bool`, respawn, **stav světa** (`infestation`,
  `supply` — obě 0–100) a `snapshot() -> Dictionary` / `restore(data) -> void`
  pro ukládání
- **spotřebovává:** `Level` (průchodnost), `Data` (co zdroj obsahuje), `Skills`
  (růst dovednosti těžby — přes příkaz/událost, ne přímým sáhnutím do cizího
  stavu)
- **tvar dat:**

  | Prvek | Typ | Význam |
  |---|---|---|
  | `nodes` | `Array[Dictionary]` | `{cell: Vector2i, kind: "ore"\|"tree"\|"rock"\|"field", rich: float, respawn_at: float}` |
  | `gather(cell)` | `Dictionary` | `{ok: bool, common: {id, amount}, rare: {id, amount}\|null}` — **směs** (GDD §2 pravidlo A) |
  | `infestation`, `supply` | `float` 0–100 | stav světa (GDD §8.1); ceny jsou **důsledek** |
  | `snapshot()` | `Dictionary` | serializovatelný stav uzlů + stavu světa (pro `save.gd`) |

- **odkud čísla:** vzorce infestace/zásobenosti drží **tahle komponenta**
  (GDD §9.3); **ceny z nich počítá `Economy`** — `World` ceny nezná
- **acceptance:** test ZAVOLÁ `gather(cell)` na známém uzlu a ověří, že vrací
  **běžnou složku vždy** a že **dva různě dlouhé zásahy dají jiný obsah**
  (`V4`); a že `snapshot()` → `restore()` vrátí **totéž** `infestation`/`supply`
- **status:** **`neexistuje`** — `scripts/world.gd` je **0 B** (naměřeno
  15. 10. 2026: `os.path.getsize()` = 0, `splitlines()` = 0 řádků).
  Vlastní ho **granule `world.nodes`** (`.forge/roadmap.json`); **`world.map`
  byla 8. 10. 2026 z plánu vyřazena** (naměřeno 15. 10. 2026: plán má **11 granulí**
  a `world.map` mezi nimi **není**) — je to tedy **mrtvé jméno**, ne druhá
  granule. `save.gd:71–74` na `world.gd` **už** volá `snapshot()`/`restore()`.

### 3.6 `Item` — `scripts/item.gd`

- **poskytuje:** `use() -> void`, `repair() -> void`, `broken() -> bool`;
  vlastnosti `id`, `nazev`, `material`, `trvanlivost`, `damage`, `armor_rating`,
  `kvalita`
- **spotřebovává:** `Data` (`items.json` + `materials.json`)
- **tvar dat:** hodnoty se plní v `_ready()` z `items.json` podle `id`
  (naměřeno `item.gd:12–30`)

  | Prvek | Typ | Výchozí | Poznámka |
  |---|---|---|---|
  | `id` | `String` | `""` | klíč do `items.json`, **anglicky** |
  | `nazev` | `String` | `""` | text pro člověka, česky |
  | `trvanlivost` | `int` | z data (`durability`), jinak 20 | | 
  | `kvalita` | `int` | z data (`quality`), jinak 0 | **0–5 stupňů** (GDD §9.2) |
  | `material` | `String` | z data (`material`), jinak `""` | | 
  | `damage`, `armor_rating` | `int` | z data, jinak 0 | |

- **acceptance:** test ZAVOLÁ `use()` a ověří **pokles trvanlivosti o 1**;
  ZAVOLÁ `repair()` a ověří, že trvanlivost **stoupla, ale ne nad maximum**
  předmětu (dnes to neplatí — viz `TDD` §10 vada 2); `broken()` po `use()` na nule
- **status:** `částečně` (`scripts/item.gd`, 39 řádků — soubor existuje, ale
  **`repair()` je vada**, viz `TDD` §10)

### 3.7 `Player` — `scripts/player.gd`

- **poskytuje:** `move(dir: Vector2, delta: float = -1.0) -> void`,
  `add_item(item) -> void`, `remove_item(item) -> void`, `equip(item) -> void`,
  `unequip() -> Node`, `die() -> void`, `flash() -> void`; signály
  `collected(what)`, `died()`; stav níž
- **spotřebovává:** `Level` (kolize), `Item`, `Attributes`, `Skills`
- **tvar dat** (stav hráče — **vlastní ho `player.gd`**):

  | Prvek | Typ | Výchozí | Kdo to čte |
  |---|---|---|---|
  | `hp`, `max_hp` | `int` | 100 | `hud.gd:48`, `assist.gd:11` |
  | `mana`, `max_mana` | `int` | 50 | `assist.gd:13` |
  | `target` | `Node` nebo `null` | `null` | `assist.gd:15` |
  | `inventory` | `Array` | `[]` | `save.gd:63`, `economy.gd` |
  | `equipped` | `Node` nebo `null` | `null` | `hud.gd:49`, `save.gd:67` |
  | `velocity` | `Vector2` | `ZERO` | pohyb (řazení, animace) |

- **odkud čísla:** `SPEED = 130.0` (konstanta hráče, naměřeno `player.gd:39`);
  izo poměr `(dx−dy)·0,5`, `(dx+dy)·0,25` je **týž poměr, jaký má kreslení
  dlaždic v `level.gd`** — hráč proto chodí po stejných osách jako mapa;
  `ACCEL 650`, `DECEL 900`, `DEAD_ZONE 12 px`, `RUN_DISTANCE 160 px`,
  `stamina 100` (`STAMINA_RUN_PER_S 20`, regen 12/s) — **dokončeno 19. 10. 2026**
  (M1 `entity.move.smooth`; hodnoty jsou laditelné, smlouva je měřitelnost)
- **dvě cesty `move()` (smlouva):** `delta < 0` = **jeden plný krok**
  `SPEED/60` po izo ose (testovací cesta; na ní stojí acceptance níž);
  `delta >= 0` = skutečný tik s **vyhlazením** (rychlost se rozjíždí/brzdí
  přes `velocity.move_toward`), mrtvou zónou (jen ze vstupní komponenty nebo
  záložní myši), staminou (běh ubírá, chůze regeneruje, při 0 je rychlost
  poloviční) a `_step()` (hráč nikdy neskončí ve zdi)
- **acceptance:** test **ZAVOLÁ `move()`**, změří **posun** a porovná jeho sklon
  se sklonem osy dlaždice, který si **PŘEČTE z `level.cell_center`** (ne
  z konstanty opsané do testu); dále ověří, že `move(Vector2.ZERO)` neposune,
  že po 10 ticích je posun **menší** než 10×`SPEED` (vyhlazení), že běh ubírá
  staminu a vyčerpaná stamina rychlost **sníží**, a že po 90 ticích je hráč
  pořád na průchodném políčku; nakonec ZAVOLÁ `die()` a ověří, že vznikl uzel
  ve skupině `corpse`, inventář se vyprázdnil a hráč stojí na `level.spawn_cell`
- **status:** `hotovo` (`scripts/player.gd`, ~270 řádků; smlouva `move` je
  závazná od 3. 10. 2026, rozšířená o vyhlazení 19. 10. 2026)

### 3.8 `Npc` — `scripts/npc.gd` (**soubor v repu není**)

- **poskytuje:** `trade(player) -> bool`, `orders() -> Array` (co vesnice chce)
- **spotřebovává:** `Item`, `Economy`
- **tvar dat:** objednávka = `{id: String, want: {id, amount}, reward: int,
  delivered: int}`; `trade()` vrací `true` jen když **skutečně obchod proběhl**
- **odkud čísla:** ceny a odměny drží `Economy`; `Npc` je **rozhraní
  k hráči**, ne druhý ceník
- **acceptance:** test ZAVOLÁ `trade()` s nedostatkem zboží a ověří **`false`
  a nezměněný stav**; pak s dostatkem a ověří **`true`, odečtené zboží
  a připsanou odměnu**
- **status:** **`neexistuje`** — `scripts/npc.gd` v repu **není** (naměřeno;
  granule `entity.npc` ho vlastní a je jediná, která nikdy neprošla)

### 3.9 `Enemy` — `scripts/enemy.gd` (**soubor v repu není**)

- **poskytuje:** `attack() -> void`, `drop_loot() -> Array`, stav `hp`,
  `max_hp`
- **spotřebovává:** `Item`, `Combat`
- **tvar dat:** kořist = pole `{id: String, amount: int}`; rozhoduje `Data`
  (`monsters.json` — dnes `skeleton`: `hp` 10 a 2 dropy, naměřeno)
- **odkud čísla:** šance a množství z `monsters.json`; **žádná náhoda mimo
  seedovaný zdroj** (`TDD` §1.4)
- **acceptance:** test ZAVOLÁ `attack()` a ověří **ubrání `hp`**; ZAVOLÁ
  `drop_loot()` a ověří, že každý drop má `id` **existující v `items.json`
  nebo `materials.json`** (ne vymyšlený klíč)
- **status:** **`neexistuje`** (soubor v `scripts/` není)

### 3.10 `Mining` — `scripts/mining.gd`

- **poskytuje:** `gather(node) -> Dictionary` (výtěžek dle dovednosti ×
  obtížnosti)
- **spotřebovává:** `Skills`, `World`, `Data`
- **tvar dat:** vrací `{ok: bool, common: {id, amount}, rare: {id, amount}|null,
  skill_gain: int}` — **tvar se shoduje s `World.gather()`**, protože `World`
  drží, co v uzlu je, a `Mining` počítá, **kolik toho hráč vydoluje**
- **odkud čísla:** `výnos = 1 + (dovednost − obtížnost)/10` (GDD §9.2);
  obtížnost je v `materials.json` (dnes `iron_ore` 1, `wood` 1, `stone` 2,
  `iron_ingot` 3 — naměřeno)
- **acceptance:** test ZAVOLÁ `gather()` se **dvěma různými hodnotami
  dovednosti** a ověří **prokazatelně jiný výnos** (`V2`) — ne jen že funkce
  existuje
- **status:** `částečně` — **dnešní stav a cíl se liší v návratovém typu**
  (naměřeno 15. 10. 2026: `scripts/mining.gd`, 72 řádků):
  - **dnes** je na `mining.gd:17` `func gather(node: Node) -> int:`
    (vrací **počet kusů**); komponenty bere z registru, který v běžící hře není
    → vrací prázdno (viz §10 vada 3).
  - **cíl** je `Dictionary` **shodný s `World.gather()`** (tabulka výš) —
    **směs** (dva různě dlouhé zásahy dají jiný obsah) je požadavek designu
    (`V4`, `GDD` §2 pravidlo A) a `int` ji neunese.
  - **plán:** prompt granule `sim.mining` v `.forge/roadmap.json` dnes žádá
    `gather(node) -> int` (naměřeno 15. 10. 2026) — **přepíše se při otevření
    milníku `M2`** ze smlouvy výš; projekt je zastavený, takže se plán
    neopravuje dopředu.

### 3.11 `Crafting` — `scripts/crafting.gd`

- **poskytuje:** `smelt() -> Dictionary`, `forge() -> Dictionary`,
  `repair(item) -> bool`
- **spotřebovává:** `Skills`, `Attributes`, `Item`, `Data`
- **tvar dat:** recept = `{id, name, inputs: [{id, amount}], outputs: [{id,
  amount}]}` (přesně to, co je dnes v `recipes.json`); výsledek výroby =
  `{ok: bool, id: String, kvalita: int, zmetek: bool}`
- **odkud čísla:** **kvalita = `dovednost/20` → 0–5 stupňů** (GDD §9.2);
  **palivo, opotřebení nástroje a zmetkovost jsou ROZHODNUTÉ** (uživatel
  8. 10. 2026: „zatím palivo, opotřebení, zmetkovost a můžeme rozvíjet časem“,
  GDD §9.2) — patří do vzorce a musí mít svá čísla na jednom místě
- **acceptance:** test ZAVOLÁ `smelt()` s dostatkem vstupů a ověří **odečtené
  vstupy a připsaný výstup**; se dvěma hodnotami dovednosti ověří **jinou
  kvalitu** (`V2`); ZAVOLÁ `repair(item)` a ověří, že trvanlivost **stoupla
  a nepřelezla maximum**
- **status:** `částečně` (`scripts/crafting.gd`, 78 řádků; v běžící hře nedostane registr)

### 3.12 `Combat` — `scripts/combat.gd`

- **poskytuje:** `resolve(attacker: Node, defender: Node) -> Dictionary`
- **spotřebovává:** `Attributes`, `Skills`, `Item`
- **tvar dat:** vrací **VŽDY** `{hit: bool, damage: int}` — i když komponenty
  chybí
- **odkud čísla:** `hit = randf() < 0,5 + (Dex + boj_na_blizko)/200`;
  `damage = max(0, 1 + Str/10 + zbraň.damage − obránce.armor_rating)`
  (GDD §9.4). **Čísla se berou z REGISTRU na rodiči**, ne z jednoho objektu:
  `get_parent().component("Attributes")` a `component("Skills")` jsou **dvě
  různé komponenty** — naměřená vada byla, že je funkce hledala na témž uzlu
- **acceptance:** test `resolve()` **ZAVOLÁ** a ověří `{hit, damage}` pro
  **zásah i minutí** (`has_method("resolve")` NESTAČÍ)
- **status:** `částečně` (`scripts/combat.gd`, 127 řádků; smlouva platí, registr v běžící hře chybí)

### 3.13 `Economy` — `scripts/economy.gd`

- **poskytuje:** `price(item: Node) -> int`, `buy(player, item) -> void`,
  `sell(player, item) -> void`, `gold(player: Node) -> int`
- **spotřebovává:** `Item`, `Data`, **stav světa** (`World`)
- **tvar dat:** cena = `int`; **vstupy ceny jsou `id` předmětu, jeho kvalita
  (0–5) a stav světa**:

  | Prvek | Typ | Význam |
  |---|---|---|
  | `price(item)` | `int` | `základ × (1 + (100 − supply)/100) × (1 + infestation/200)` (GDD §9.3) |
  | `gold(player)` | `int` | zlato **hráče**; `Economy` nesmí mít vlastní stav, který hráči nepatří |

- **odkud čísla:** `base` z `Data`; `supply`/`infestation` z `World` —
  **`Economy` je nepočítá**, jen z nich dělá cenu
- **acceptance:** test ZAVOLÁ `price(iron_sword)` a ověří **nenulovou cenu**,
  která se **změní**, když se změní `supply`; ZAVOLÁ `sell()` a ověří pohyb
  zlata **a** předmětu
- **status:** `částečně` — a **`price()` dnes vrací 0 pro každý skutečný
  předmět** (`TDD` §10 vada 1)

### 3.14 `Offline` — `scripts/offline.gd`

- **poskytuje:** `resolve(char, job, hours) -> Dictionary` s **denním stropem**
- **spotřebovává:** `Skills`, `Mining`, `Crafting`, `Combat`
- **tvar dat:** `{ok: bool, gained: Dictionary, hours_used: float,
  capped: bool}`; `gained` má **stejné klíče jako `World.gather()`** (`id`,
  `amount`) — „svět žije i bez tebe“ je **jeden systém**, ne nový projekt (§11)
- **odkud čísla:** tempo růstu se řídí předsadou `ladici`/`normalni`/`pomala`
  (GDD §9.1); **ladicí předsada se nesmí dostat do hry**
- **acceptance:** test ZAVOLÁ `resolve()` s překročeným denním stropem a ověří
  `capped == true` **a že se stav nezměnil víc, než strop dovoluje**
- **status:** `částečně` (`scripts/offline.gd`, 57 řádků)

### 3.15 `Assist` — `scripts/assist.gd`

- **poskytuje:** `add_rule(trigger: String, action: String) -> void`,
  `evaluate(char) -> Array`
- **spotřebovává:** `Player`, `Item`
- **tvar dat:** pravidlo = `{trigger: String, action: String}`; **literály
  rozhraní jsou anglicky** (`"hp < 30"`, `"target dead"` — naměřeno
  `assist.gd:15`), text pro hráče se překládá až v UI
- **odkud čísla:** prahy si určuje pravidlo; `evaluate()` **nic nemění**,
  jen vrací, co by se mělo stát (simulace rozhoduje)
- **acceptance:** test ZAVOLÁ `evaluate()` na hráče se **známým** `hp` a ověří
  **ne-prázdný výsledek**; a ZAVOLÁ ho na hráče **bez `hp`** a ověří, že to
  **ohlásí** (dřív vracel prázdné pole a vypadal jako „nic k práci“)
- **status:** `částečně` (`scripts/assist.gd`, 17 řádků). **`assist` je v MVP
  přípustný** ve smyslu `N9` po přeformulování z 9. 10. 2026 (`GDD` §11,
  `docs/GDD.md:432–449`): **rozhoduje hráč, hra provádí** (i offline doběh a i
  podle pravidel s podmínkami). Zakázané zůstává, aby hra rozhodovala za
  hráče. Smlouva platí; kdo `assist` zapojí, musí v kódu napsat, které
  rozhodnutí je hráčovo. *Původní znění TDD („`assist` je non-goal `N9` pro
  MVP“) odpovídalo `GDD` **před** 9. 10. 2026 — ve svém čase správné; platí
  `GDD`, protože je zdroj pravdy o designu a je novější (`R1`).*

### 3.16 `Save` — `scripts/save.gd`

- **poskytuje:** `save() -> bool`, `load() -> bool`
- **spotřebovává:** `Attributes`, `Skills`, `Economy`, `Player`, `World`
- **tvar dat:** `ConfigFile` → `user://save.cfg` (`TDD` §4.3)
- **odkud čísla:** nic nepočítá — **je to sklad**, stav vlastní komponenty
- **acceptance:** test ZAVOLÁ `save()` s hráčem na **známé pozici**, pozici
  **ZMĚNÍ**, ZAVOLÁ `load()` a ověří, že se pozice vrátila; a ZAVOLÁ `save()`
  **bez kostry** a ověří, že vrací **`false`** (ne tichý úspěch)
- **status:** `částečně` (`scripts/save.gd`, 150 řádků; rozšířeno o inventář a stav světa, ale
  `World` neexistuje → ukládá se jen to, co je, a **warningem se to ohlásí**)

### 3.17 `Hud` — `scripts/hud.gd`

- **poskytuje:** `update() -> void`
- **spotřebovává:** `Player`, `Skills`, `Attributes`, `Economy`, `World`
- **tvar dat:** **jen čte**; zobrazuje HP, atributy, dovednosti, zlato,
  vybavený předmět (naměřeno `hud.gd:74–81`) a podle GDD §7 navíc **stav světa**
  a **zakázku s postupem**
- **odkud čísla:** z komponent přes registr; **HUD nesmí nic dopočítávat**
  (jinak vznikne druhé číslo téhož)
- **acceptance:** test **ZAVOLÁ `update()`** nad **skutečnými** komponentami
  (ne atrapami) a ověří, že text obsahuje **konkrétní hodnotu** (např. `hp` 73),
  ne nulu; a že **po změně stavu** se text změní
- **status:** `částečně` (`scripts/hud.gd`, 92 řádků; **hra ho neinstancuje** — naměřeno: v běžící
  hře je jen `Label` z `game.gd`, `hud.gd` se instancuje pouze v testech)

### 3.18 `Shell` (kostra) — `scripts/game.gd`

- **poskytuje:** `component(id: String) -> Node`, sestavení scény, **tik**,
  **fronty příkazů a událostí** (`TDD` §1.2, `TDD` §1.3)
- **spotřebovává:** všechny komponenty **přes registr**
- **tvar dat:** registr = `Dictionary` id → `Node`; `component(id)` vrací
  `null` pro neznámé id (a **ohlásí to**, když jde o komponentu, která má být)
- **odkud čísla:** `TICK_MS = 50` (konstanta kostry); seed náhody
- **acceptance:** test ZAVOLÁ `component("Skills")` a ověří, že **vrací uzel,
  který umí `hodnota()`**; ZAVOLÁ `component("Neexistuje")` a ověří `null`
  **bez chyby**; a ZAVOLÁ `move` příkaz a ověří, že se hráč posunul
- **status:** **`částečně`** — **registr existuje** (`scripts/registry.gd`,
  150 řádků, hotový ručně 8. 10. 2026: `component(id)`, `advance()`/`step()`
  s pevným tikem 50 ms, fronty příkazů a událostí; měřeno testy — jeho vlastní
  smlouva je **§3.19**), ale
  **`scripts/game.gd` je pořád monolit** (377 řádků) a registr **nevolá** —
  kostru scény dodá `engine.shell`. `component()` tedy v repu je, ale v běžící
  hře ho zatím nikdo nezavolá

### 3.19 `Registry` — `scripts/registry.gd`

- **poskytuje:** `register(id: String, node: Node) -> void`,
  `component(id: String) -> Node`, `components() -> Dictionary`,
  `registered_order() -> Array[String]`, `advance(delta: float) -> int`,
  `step(dt: float = TICK_MS / 1000.0) -> void`, `ticks() -> int`,
  `push_command(cmd: Dictionary) -> void`, `commands() -> Array`,
  `push_event(ev: Dictionary) -> void`, `events() -> Array`; signál
  `ticked(dt: float)` a konstanty `TICK_MS` = 50, `MAX_TICKS_PER_FRAME` = 3
- **spotřebovává:** komponenty **jako své děti** — volá na nich `sim_tick(dt)`,
  když ho mají (`registry.gd:112`); nic jiného nečte a nic nepočítá
- **tvar dat:**

  | Prvek | Typ | Význam |
  |---|---|---|
  | registr | `Dictionary` `id -> Node` (+ `Array[String]` pořadí registrace) | **v tom pořadí** dostávají komponenty `sim_tick` — pořadí je součást smlouvy |
  | příkaz | `Dictionary` `{type: String, …}` | vstup → simulace (`TDD` §1.3) |
  | událost | `Dictionary` `{type: String, …}` | simulace → zobrazení (`TDD` §1.3) |
  | `commands()`, `events()` | `Array` | frontu **vrátí a VYPRÁZDNÍ** — druhý odběratel dostane prázdno, ne tatáž data dvakrát |
  | `advance(delta)` | `int` | počet provedených tiků; čas se akumuluje v **milisekundách** (`49 + 1 = 50` přesně, ne plovoucí `0,049 + 0,001`) |

- **odkud čísla:** `TICK_MS` = 50 (`registry.gd:26`) a `MAX_TICKS_PER_FRAME` = 3
  (`:29`) — vlastní je jen tenhle soubor; `step()` posílá `dt` = 0,05 s.
  **Ochrana proti spirále smrti:** po pauze (okno na pozadí) se dorovnají
  nejvýš 3 tiky na snímek (`:123–125`), ne stovky — simulace se tím nezrychluje,
  jen nezasekne
- **acceptance:** test **ZAVOLÁ** `register("Skills", uzel)` a ověří, že
  `component("Skills")` vrátí **týž uzel**, a že `component("Neexistuje")` vrátí
  `null` **bez chyby**; ZAVOLÁ `advance(0.049)` a ověří **0 tiků**, pak
  `advance(0.002)` a ověří **právě 1 tik** (49 + 2 ms) a `advance(0.15)` →
  **3 tiky**; ZAVOLÁ `push_command()` dvakrát a ověří, že `commands()` vrátí
  **oba příkazy v pořadí** a že **druhé čtení je prázdné**; totéž pro
  `push_event()` / `events()`; a ZAVOLÁ `step()` nad dvěma komponentami a ověří,
  že `sim_tick` přišel **v pořadí registrace** (to měří i `registered_order()`).
  `has_method("advance")` NESTAČÍ.
- **status:** `hotovo` (`scripts/registry.gd`, 150 řádků, hotový ručně
  8. 10. 2026; **tyhle acceptance už běží** — naměřeno 15. 10. 2026 během testů,
  `[test] 113 kontrol, 0 selhání`). **Co chybí:** kostra `scripts/game.gd` ho
  **nevytváří ani nevolá**, takže v běžící hře dostanou komponenty `null`
  (§10 vada 3) — to není vada registru, ale chybějící `engine.shell`.

### 3.20 Souhrn: co má tvar dat a co ne

| | Stav 15. 10. 2026 |
|---|---|
| Smluv celkem | **19** (18 do 8. 10. 2026 + `Registry`) |
| S tvarem dat **před** TDD | **3** (`sim.combat`, `Hráč → move`, `Ukládání → pozice`) — měřeno 8. 10. 2026 v `ARCHITEKTURA.md` |
| S tvarem dat **po** TDD | **19** (tabulky výš) |
| Komponent, které v `scripts/` **neexistují** | **3** (`world.gd` = 0 B, `npc.gd`, `enemy.gd` — naměřeno 15. 10. 2026) |
| Komponent, které fungují v běžící hře | **2** (`level.gd`, `player.gd`; naměřeno 15. 10. 2026: produkční cesta z `main.tscn` je `game.gd` 377 + `level.gd` 283 + `player.gd` 191 řádků) |

---

## 4. Datové formáty

**Pravidlo (`R-3`):** **klíče a identifikátory anglicky, texty pro člověka
česky** — a platí to i pro data. Dnešní stav to **z větší části** splňuje
(`id` = `iron_sword`, `name` = „Železný meč“), **až na dvě místa** — viz §8.

### 4.1 `assets/data/*.json` — obsah (data, ne kód)

- **Tvar:** **JSON array objektů.** Společné klíče: `id` (anglicky, klíč
  rozhraní) a `name` (česky, text pro člověka).
- **Dnešní soubory (naměřeno 8. 10. 2026):**

  | Soubor | Záznamů | Klíče záznamu | `id` |
  |---|---|---|---|
  | `materials.json` | 4 | `id`, `name`, `difficulty` | `iron_ore`, `wood`, `stone`, `iron_ingot` |
  | `skills.json` | 4 | `id`, `name` | `tezba`, `drevorubectvi`, `kovarstvi`, `boj_na_blizko` |
  | `recipes.json` | 3 | `id`, `name`, `inputs[]`, `outputs[]` | `smelting`, `kovani_mece`, `kovani_zbroje` |
  | `monsters.json` | 1 | `id`, `name`, `hp`, `drops[]` | `skeleton` |
  | `items.json` | 2 | `id`, `name`, `durability`, `damage`, `armor_rating` | `iron_sword`, `iron_armor` |

- **Co GDD žádá navíc** (rozsah `M`, GDD §10): 11 materiálů, 7 předmětů,
  3 nestvůry, 8 receptů, 6 dovedností. **Nový obsah = nový záznam, ne nová
  granule** — proto je datová vrstva smlouva, ne implementační detail.
- **Nový soubor (dnes neexistuje): `assets/data/synergies.json`** — synergie
  jako **data**, ne kód (`VSTUPY` §2.4, návrh `N-5`; míra **20 %** je
  rozhodnutá, §13.1). Tvar: `[{"from": "kovarstvi", "to": "boj_na_blizko",
  "rate": 0.2}]`.
- **Co se ověří:** každý soubor je validní JSON, každý záznam má `id` a `name`,
  každý `id` v `inputs`/`outputs`/`drops` **existuje** v materiálech nebo
  předmětech. (Dnes to **nikdo neměří** — `check-schema.py` o surovinách
  neví nic.)

### 4.2 `assets/levels/*.json` — mapa a markery

- **Dnešní stav (naměřeno):** `main.json` (87 řádků, 14 klíčů) a `manifest.json`
  (19 řádků).
- **Klíče `main.json`:** `name`, `seed`, `cell`, `width`, `height`, `viewport`,
  `offset`, `legend`, **`tiles`** (mapování znak → název dlaždice), **`grid`**
  (mřížka), **`markers`**, `stats`, `generated`, `_projekce`.
- **Mřížka:** `grid` = pole řádků, **znak na buňku**: `0` = zeď, `1` = podlaha
  místnosti, `2` = chodba (`legend` to pojmenovává). Dnes 16 řádků × 30 znaků,
  `walkable` 109, `connectivity` 1.0.
- **Markery:** `markers` = pole `{type, cell: [cx, cy]}`; dnes **4**
  (`spawn` [17,7], 2× `coin`, `exit`). `Level.marker_positions(type)` z nich
  dělá světové souřadnice — **nový předmět se nikdy neumisťuje na náhodnou
  pozici**.
- **Co je vlastnost HRY a co LEVELU:** velikost buňky a projekce jsou
  **vlastnost hry** (`assets/spec.json`) — `level.gd:105–108` proto `cell`
  z mapy **ignoruje**. Mapa deklaruje jen mřížku, markery a dlaždice.
- **Poznámka k `cell`:** `main.json` má `cell: 96`, což je **jen šířka** —
  výška 48 je ze specu. Formát proto **nenese úplné schema** a nesmí se z něj
  odvozovat.

### 4.3 Ukládání — `ConfigFile` do `user://save.cfg`

- **Formát:** `ConfigFile` (ne JSON) — **odvozeno z existujícího kódu**
  (`save.gd:19`), ne z vkusu.
- **Sekce a klíče (naměřeno ze `save.gd`):**

  | Sekce | Klíče | Význam |
  |---|---|---|
  | `attributes` | `Str`, `Dex`, `Int` | atributy |
  | `skills` | `dovednosti` (`Dictionary`) | dovednosti |
  | `economy` | `gold` | zlato hráče |
  | `player` | `position` (`Vector2`) | pozice hráče |
  | `inventory` | `items` (pole `{id, trvanlivost, kvalita}`), `equipped_id` | inventář a vybavení |
  | `world` | `data` (z `World.snapshot()`) | stav světa a uzlů |

- **Dvě cesty, které se nesmí slít:** po **`load()`** stojí hráč tam, kde hrál
  (uložený stav); po **`die()`** se vrací na **`level.spawn_cell`**. Kdyby obojí
  dělal `save.gd`, smrt by „vracela do rozehrané hry“.
- **Pravidlo proti tichému úspěchu:** `save()` vrací **`false`**, když není co
  uložit, a chybějící komponentu **ohlásí** (`push_warning`) — ne tiše vynechá.
  Naměřeno: dřív `save()` zapsal 35 B (jen pozici) a **vrátil `true`**.
- **Kam se ukládá:** `user://` (Godot: `%APPDATA%\Godot\...`). **Pozor
  v sandboxu:** `--user-data-dir` tenhle build ignoruje, takže `user://` může
  mířit mimo workspace — a nástroj **nespadne**, jen tiše neuloží (skill
  `dsh-prostredi`).

### 4.4 Kde je co (rychlý přehled)

| Data | Soubor | Kdo je čte | Kdo je vlastní |
|---|---|---|---|
| obsah hry | `assets/data/*.json` | všechny sim komponenty | `Data` (data) |
| mapa a markery | `assets/levels/main.json` | `Level` | level (data) |
| vizuální schema | `assets/spec.json` | `Level`, brány, ADD | projekt (data) |
| uložená hra | `user://save.cfg` | `Save` | komponenty (stav) |

---

## 5. Vlastnictví stavu (kdo co vlastní)

**Pravidlo: každý kus stavu má PRÁVĚ JEDNOHO vlastníka.** Kdo ho mění podruhé,
vytváří druhé číslo téhož — a to je naměřená vada z 3. 10. 2026 (pozice hráče
se ukládala podmíněně a `load()` ji přepisoval spawnem).

| Stav | Vlastník | Kdo ho smí ČÍST | Poznámka |
|---|---|---|---|
| pozice a stav hráče (`hp`, `mana`, `inventory`, `equipped`, `target`) | `player.gd` | `hud.gd`, `save.gd`, `assist.gd`, `economy.gd` | `save.gd` je **sklad**, nikdy ji nepočítá ani nezná spawn |
| atributy | `attributes.gd` | boj, výroba, HUD, save | |
| dovednosti | `skills.gd` | výroba, těžba, boj, HUD, save | jediná cesta změny je `add()` |
| zlato, ceny, zakázky, uznání světa | `economy.gd` | HUD, `npc.gd`, save | ceny jsou **důsledek** stavu světa, ne třetí stav |
| uzly surovin, respawn, infestace, zásobenost | `world.gd` | těžba, ekonomika, HUD, save | **dnes soubor neexistuje (0 B)** |
| mřížka, projekce, spawn | `level.gd` | hráč (kolize), svět, HUD (mapa) | `world.gd` projekci **nesmí opisovat** |
| trvanlivost a kvalita předmětu | `item.gd` | boj, výroba, ekonomika, save | |
| tik, registr, fronty příkazů a událostí | `scripts/registry.gd` | všichni přes registr | hotový ručně 8. 10. 2026 (`TICK_MS` na `:26`, `advance()` na `:91`, `push_command()` na `:129`, `push_event()` na `:141` — naměřeno 15. 10. 2026); **kostra scény (`scripts/game.gd`) ho zatím nevolá** (viz §3.19) |
| seed náhody | kostra (`scripts/game.gd`) | kdo potřebuje náhodu (`TDD` §1.4) | hodnotu dnes nese `assets/levels/main.json`; **sám registr seed nevede** (naměřeno 15. 10. 2026) |
| uložený stav | `user://save.cfg` | `save.gd` | formát je `ConfigFile` |

---

## 6. Výkonnostní rozpočet (`R-2`)

| Metrika | Rozpočet | Odkud |
|---|---|---|
| Snímková frekvence | **60 FPS** při **960×540** | §14.2 |
| Simulace | **< 2 ms na tik** (tik 50 ms → rezerva 25×) | §14.2 |
| Rozlišení | vnitřní 960×540, celočíselně 2× na 1080p | `spec.json` (`viewport`); `project.godot` `viewport_width/height` = 960×540 |

**Jak se to měří (co musí test ZAVOLAT):** změřit dobu **jednoho tiku
simulace** (`Time.get_ticks_usec()` před a po) v **nejhorším známém stavu**
(tik, ve kterém se těží, vyrábí a překresluje stav světa) a porovnat s 2 ms.
**Průměr z prázdného tiku nic neříká** — to je tatáž past jako „zelená nad
nulou souborů“.

**Co v rozpočtu NENÍ:** rozpočet na velikost světa (kolik uzlů a entit mapa
unese). Dnes to nikdo neměří a číslo by bylo dohad — patří do prvního měření
při milníku `M2`/`M4`, ne do TDD jako slib.

---

## 7. Chybové chování

**Rozhodnuto (§14.2), s naměřeným důvodem:**

1. **Chybějící komponenta** = `push_error` (nebo `push_warning`, je-li stav
   částečně použitelný) a **hra zůstane hratelná**. Komponenta se **přeskočí**,
   ne aby shodila scénu.
2. **Tichý `return` je zakázaný.** Když se něco neudělá, musí to být **vidět**:
   - `save()` nad neuloženým stavem **vrátí `false`** a ohlásí to (dřív vracel
     `true` nad 35 B);
   - chybějící pozice hráče se **ohlásí** (`push_warning`), ne tiše vynechá;
   - `load()` se souborem, který nemá kam vrátit, **ohlásí chybu a vrátí
     `false`**.
3. **Chybějící datový soubor** = `push_error` + návrat na **výchozí hodnoty**
   tam, kde to jde bez lhaní (např. `level.gd` použije výchozí schema a **řekne
   to**); nikdy ne „prázdno, které vypadá jako naměřená nula“.
4. **Poškozená data** (JSON, který není objekt/pole; mřížka, která nesedí
   s hlavičkou) = **`false`/`push_error`**, ne tichý částečný stav. Naměřeno
   v `level.gd:126–133`.
5. **Godot 3 vs. Godot 4:** konstanty a API Godotu 3 (`ALIGN_LEFT`,
   `File`, `json`, `has()`) **v Godotu 4 neexistují** a shodí parsování celého
   skriptu. Pravidlo: **nepoužívej konstantu, kterou jsi neviděl v tomhle repu**
   (`CONVENTIONS.md` §1c, §1h).

---

## 8. Jazyk rozhraní (`R-3`)

**Pravidlo:** **klíče, identifikátory a literály rozhraní = anglicky** (nikdy
český název funkce, nikdy český literál, který musí volající uhodnout);
**dokumentace, komentáře a texty pro člověka = česky**; **výstup nástroje pro
člověka česky, hodnota, kterou čte jiný program, anglicky.**

**Kde to dnes platí:** `items.json` (`id` = `iron_sword`, `name` = „Železný
meč“), `materials.json`, `monsters.json`, recept `smelting`, id registru
(`Attributes`, `Skills`, …), literály asistence (`"target dead"` — naměřeno
`assist.gd:15`).

**Kde to dnes NEplatí (naměřeno 8. 10. 2026 čtením `assets/data/*.json` a
`scripts/*.gd`):**

| Co | Dnešní stav | Pravidlo `R-3` |
|---|---|---|
| `skills.json` — `id` | `tezba`, `drevorubectvi`, `kovarstvi`, `boj_na_blizko` (**česky**) | anglicky (`mining`, `woodcutting`, …) |
| `recipes.json` — 2 ze 3 `id` | `kovani_mece`, `kovani_zbroje` (**česky**); `smelting` anglicky | anglicky |
| klíče v `skills.gd:3` | tytéž české klíče | anglicky |
| stavové veličiny v kódu | `hodnota()`, `trvanlivost`, `kvalita`, `nazev`, `dovednosti` (česky) | **pozor: tady jde o KOMPATIBILITU, ne o porušení** — `CONVENTIONS.md` §1f české názvy přímo doporučuje, protože `get`/`name`/`size` kolidují s enginem |

**Co z toho plyne (a co se NEMÁ udělat mimochodem):** sjednocení klíčů je
**změna kódu i dat** — přejmenování `tezba` → `mining` rozbije testy, roadmapu
i uložené pozice. Je to **samostatný úkol**, zapsaný v GDD §14 jako otevřený bod
`O-5`. **Do té doby platí `R-3` pro všechny NOVÉ klíče** a stávající české klíče
se **nepřejmenovávají potichu**.

---

## 9. Brány: co pouští CI a v jakém pořadí

**Detail bran je jinde a neopisuje se:** **co která brána měří, kde má naměřené
slepé místo a jaká je past „TIŠE PŘESTALA MĚŘIT", je jediný zdroj
`docs/BRANY-HRY.md`** (přesunul se tam 7. 10. 2026 ze skillu `orchestra`). TDD
drží **jen to, co potřebuje sám**: které brány pouští CI a v jakém pořadí.
**Tvrdá brána je jen jedna** — `check-schema.py` (rozpor v deklaraci je
objektivní fakt); ostatní jsou poradní nebo mají slepá místa (ta vypisuje
`docs/BRANY-HRY.md`, ne TDD).

> **TDD tabulku bran záměrně NEMÁ** — byla tady do 15. 10. 2026 a s `BRANY-HRY.md`
> se **rozešla** (duplicita `D1` v `_analyza/PRACE-2026-10-15/ROZPORY.md`); kdo
> hledá slepá místa, čte `BRANY-HRY`. Sem se nová tabulka **nevrací**.

**Pořadí kroků v CI je dané a testuje se** (naměřeno 15. 10. 2026 z
`.github/workflows/ci.yml`, 181 řádků, job `test-and-build`): checkout → cache
Godotu → instalace Godotu → **import assetů** → **kontrola schématu** → **testy**
→ kontrola assetů → kontrola zapojení → smoke (hra se spustí bez `SCRIPT ERROR`)
→ snímek hry → `verify-level-render` → **vision** (neblokuje) → export buildů.

**Co z toho platí pro TDD:** brány, které kód **volají** (`tests/run_tests.gd`),
měří **chování**, ne přítomnost metody — proto každá smlouva v §3 říká, **co test
ZAVOLÁ a co ověří**, a `has_method()` jako acceptance **nestačí**. Naměřený důvod
(8. 10. 2026, `splitlines()` a `count()` nad `tests/run_tests.gd`): soubor má
**1569 řádků** a `has_method` **28 řádků** / **41 výskytů** (bez komentářů
20 / 33) — funkce, která v kódu není, se **přeskočí** a test zůstane tiše zelený.
⚠ **Různé čítače téhož jména:** staticky je v souboru **154** volání `_check(`
(155 výskytů řetězce − 1 definice), ale běh hlásí **`[test] 113 kontrol`** —
**počet kontrol se čte z BĚHU**, ne ze vzorů v souboru. Která brána co měří a kde
má slepé místo, drží `docs/BRANY-HRY.md`.

**Co u bran chybí** (§15.2, pojmenované, ne zapomenuté):

1. **Brána nad dokumentací** — `check-docs-refs` (každý odkaz `§N.N` musí
   existovat) a `check-zadani` (placeholdery, vadné literály, **konzistence
   čísel**). Vzor má `game-clone`.
2. **Třetí stav „neměřeno" (`exit 2`)** — dnes jsou dva stavy (prošlo/selhalo);
   „neměřeno“ **není zelená**. Tohle je přesně případ `check-wiring.py` nad
   repem bez `scripts/*.gd`.
3. **Žádná brána neměří obsah dat** (`assets/data/*.json`): neověřuje se, že
   `id` v receptech a dropech existují, že každá dovednost má záznam, ani že
   čísla odpovídají GDD. Dnes to hlídá jen člověk.

---

## 10. Známé vady, které tenhle dokument NEMĚNÍ (naměřeno)

**Zadání je psaní dokumentů, ne oprava kódu** (`ZADANI-GDD-ADD-TDD.md` §6.1):
co dokument odhalí, **zapíše**, neopraví mimochodem. Vady 1–10 jsou **naměřené
8. 10. 2026**, vada 11 **15. 10. 2026** (u každé je čím).

| # | Vada | Důkaz | Dopad |
|---|---|---|---|
| 1 | **`Economy.price()` vrací 0 pro každý skutečný předmět** | `economy.gd:14–30` čte `item.material` (očekává `"wood"/"stone"/"metal"`) a `item.quality` (očekává `"common"…`), ale `item.gd:6–10` má `material` z `items.json` (kde klíč **není** → `""`) a `kvalita: int`; **přeměřeno 15. 10. 2026** sondou `_analyza/PRACE-2026-10-15/sonda-cena.gd`: `price()` = 0 u obou předmětů a `SCRIPT ERROR` „Invalid access to property or key 'quality'“ na `economy.gd:21` | obchod je **zdarma**; `price()` je zároveň druhý zdroj pravdy o kvalitě |
| 2 | **`Item.repair()` předmět ZNIČÍ** | `item.gd:36` nastaví `trvanlivost = 20` natvrdo; `items.json` deklaruje `durability` 100 (meč) a 150 (zbroj) | „oprava“ sníží trvanlivost ze 100 na 20 |
| 3 | **Registr komponent NEBYL volán z produkčního kódu** | `scripts/registry.gd` **existuje** (hotový ručně 8. 10. 2026, měřený testy), ale `hud.gd:90`, `save.gd:148`, `combat.gd:125`, `mining.gd:70` a `offline.gd:55` ho hledají přes `get_parent().component(id)` — a **`scripts/game.gd` (monolit) registr vůbec nevytváří**, takže v běžící hře dostanou `null` | HUD ukazuje nuly, `save()` neuloží nic. **Opravuje `engine.shell`** (další granule `M0`) — registr sám to nespraví |
| 4 | **`scripts/world.gd` = 0 B** | naměřeno 15. 10. 2026: 0 bajtů, 0 řádků (`os.path.getsize()`, `splitlines()`); vlastní ho **granule `world.nodes`**; **`world.map` byla 8. 10. 2026 z plánu vyřazena** (v plánu je 21 granulí a `world.map` mezi nimi není) | **neblokuje `engine.shell`** (její `depends_on` = `engine.registry`) — `world.nodes` má v `depends_on` **`sim.mining`** a **`persist.save.state`** (naměřeno 15. 10. 2026 v `.forge/roadmap.json`; obě jsou v plánu `done: true`, i když je `world.gd` prázdný — to je vada 9); `save.gd` na něm už volá `snapshot()` |
| 5 | **`save.gd:14` má zastaralý komentář** | tvrdí, že `player.gd` inventář „nemá“; naměřeno `player.gd:52` (`inventory`), `:130` (`add_item`), `:136` (`remove_item`) | komentář popírá kód — kdo mu věří, „opraví“ fungující věc |
| 6 | **`assets/spec.json` nemá klíč `projekce`** | `level.gd:74` → `{}`, `:83` odvodí izometrii z `96 ≠ 48` | izometrie je **odvozená**, ne deklarovaná → druhé místo pravdy o projekci |
| 7 | **Název hry se rozejšel ve třech zdrojích — OPRAVENO 8. 10. 2026** | `project.godot` = `uo-shadows`, `forge.json` a `.forge/vision-profile.json` = `uo-shadows`, repo = `uo-shadows`; **před opravou** říkaly `project.godot` a `assets/spec.json` `uo-sandbox` a `export_presets.cfg` `GameForge` | hledání pod jedním jménem teď funguje; **cena opravy:** `user://` se přesunul na `…\app_userdata\uo-shadows\` (ve starém adresáři žádný `save.cfg` nebyl — naměřeno) |
| 8 | **`npc.gd` a `enemy.gd` v repu NEJSOU** | `scripts/` má **16** souborů `.gd` (naměřeno 15. 10. 2026: `glob('scripts/*.gd')`); žádný z nich se tak nejmenuje. **Patnáct platilo před `M0`** (přibyl `registry.gd`) — ve svém čase správné číslo | dvě smlouvy (`Npc`, `Enemy`) nemají implementaci, přestože na ně plán navazuje |
| 9 | **`done` není měření: dřívější podoba plánu hlásila hotovost u 16 položek, ale hra používá 2** | **PŘEPOČÍTÁNO 15. 10. 2026:** dnešní `.forge/roadmap.json` má **11 granulí** a `done: true` u **6** — `done` je nově **měřené** (soubor v `main` A volá ho produkční cesta, nástroj `_analyza/PRACE-2026-10-15/zmer-produkci.py`). Historická čísla (16, předtím 15 a 13) byla **ve svém čase správná** a jsou v archivu plánu | „hotovo“ dnes není měření (definice hotovo to mění) |
| 10 | **`assets/data/*.json` nemá klíč `material`** | `items.json`: `id`, `name`, `durability`, `damage`, `armor_rating`; `item.gd:25` ho čte jako nepovinný | viz vada 1 |
| 11 | **`game.gd:181` tweenuje `hud` dřív, než ho `_add_ui()` vytvoří** | naměřeno 15. 10. 2026 během testů: `ERROR: Required object "rp_target" is null.` s backtrace `_add_level (res://scripts/game.gd:181)` ← `_ready (res://scripts/game.gd:33)`; `_ready()` volá `_add_level()` na `:33`, ale `_add_ui()` (které `hud` teprve vytvoří) až na `:45` → `hud` je v tu chvíli `null` | **`ERROR` při každém načtení scény**; CI to **nechytí** — krok smoke hledá jen řetězec `SCRIPT ERROR`, ale naměřená chyba začíná `ERROR:` (`ci.yml:105`) |

> **⚠ DOPLNĚNÍ 19. 10. 2026 (append-only; tabulka výš je záznam, nepřepisuje se):**
> **vada 11 je OPRAVENA** — tween na `hud` má v `game.gd` guard
> (`if hud != null`) v `_clear_entities()` i `_add_level()`, takže chyba při
> načtení scény zmizela (ověřeno testy hry). **Vady 1–10 zůstávají** (mimo
> rozsah M0/M1). Zároveň dokončeny granule `shell.nocoins` (bez mincí/skóre;
> testy **123/0**) a `entity.move.smooth` (smlouva `move` rozšířená o
> vyhlazení — viz §3.7).
>
> **⚠ DOPLNĚNÍ 20. 10. 2026:** **vada 3 je OPRAVENA** — `sim.wire` (PR #39
> orchestry, merge `d4d55e7`) přidal do `game.gd` registr a komponenty
> `Economy`/`Skills`/`Attributes`; při ověření se ale ukázalo, že PR
> **nezavolal `registry.register()`** a registr byl holý `Node` bez skriptu
> (vada **H240** v orchestra kronice). Doplněno: registr má skript
> `registry.gd`, komponenty jsou zaregistrované pod smluvními id a **test to
> nově měří** (`[test] 130 kontrol, 0 selhání`). `hud.gd`/`save.gd` tak už
> dostanou komponentu, ne `null`.

**Co z toho plyne pro plán:** vady 1–4 jsou na kritické cestě milníků `M0`
(kostra a registr) a `M3` (výroba a ekonomika). **Nejsou to úkoly TDD** — TDD
je jen **pojmenovává**, aby se na ně nezapomnělo a aby je plán mohl zařadit.

**Už není otevřené** (nezmizelo — přesunulo se sem, protože to **přestalo
platit**; co platí dál, zůstává v tabulce výš):

- **„Registr komponent neexistuje“** — neplatí od 8. 10. 2026: `scripts/registry.gd`
  je hotový a **měřený testy** (`component()`, `advance()`, fronty — naměřeno
  15. 10. 2026; smlouva `Registry` je §3.19). Otevřené zůstává jen to, že ho
  **kostra `scripts/game.gd` nevytváří ani nevolá** (vada 3).
- **„`world.map` blokuje `engine.shell`“** — neplatí: `world.map` byla
  8. 10. 2026 **vyřazena z plánu** a `engine.shell` má `depends_on` =
  `engine.registry` (naměřeno 15. 10. 2026 v `.forge/roadmap.json`). `world.nodes`
  má v `depends_on` `sim.mining` a `persist.save.state` (vada 4).
- **„`scripts/` má 15 souborů“** — ve svém čase správné (stav před `M0`); dnes
  **16** (vada 8).

---

## 11. Co v tomhle dokumentu ZÁMĚRNĚ NENÍ

- **Design a obsah** (co je zábava, V1–V8, non-goals, čísla obsahu) →
  `docs/GDD.md`. TDD říká **jak**, ne **co** a **proč**.
- **Vzhled, rozměry spritů, pipeline a katalog assetů** → `docs/ADD.md`
  a strojově `assets/spec.json`.
- **Plán granulí, pořadí a vlny** → `.forge/roadmap.json` (vzniká z milníků
  `M0`–`M6` v GDD §12). **TDD neurčuje, co se kdy staví.**
- **Detail bran hry** (co která měří, naměřená slepá místa, past „tiše přestala
  měřit") → `docs/BRANY-HRY.md`; TDD drží jen **pořadí kroků CI** (`TDD` §9).
- **Samotná síťová vrstva (cesta `B`)** — TDD drží jen podmínku, aby se dala
  přidat (`TDD` §1.4). Kdy a jestli se staví, je rozhodnutí mimo TDD.
- **Konkrétní ladicí hodnoty** (mrtvá zóna, doba náběhu, obtížnost uzlů) —
  patří do ladění a do otevřených bodů GDD (GDD §14 tam).
- **Historie rozhodnutí a jejich ceny** → `_analyza/DESIGN-REVIZE-2.md`
  (needituje se).
