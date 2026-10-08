# TDD — `uo-shadows`: jak je hra postavená a jaké má smlouvy

> **Co tenhle dokument JE:** **zdroj pravdy o technice hry** (technical design
> document) — architektura běhu, vrstvy, **smlouvy komponent s tvarem dat**,
> datové formáty, vlastnictví stavu, výkonnostní rozpočet, ukládání, chybové
> chování a jazyk rozhraní.
>
> **Nahrazuje `docs/ARCHITEKTURA.md`** jako zdroj pravdy. `ARCHITEKTURA.md`
> zůstává v repu jako **historie** (nese smlouvy `§2.1`–`2.3` a naměřené
> případy, které se needitují) — viz jeho hlavička.
>
> **Odkud brát stav:** tenhle dokument je stav techniky. **Zdroj rozhodnutí** je
> `_analyza/DESIGN-REVIZE-2.md` (uzavřená revize vize, 8. 10. 2026); odkazy
> `(§N)` míří tam. **Co má hra dělat**, říká `docs/GDD.md`; **jak vypadá**,
> `docs/ADD.md`; **co se staví**, `.forge/roadmap.json`.
>
> **Vzniklo:** 8. 10. 2026 sepsáním z `_analyza/DESIGN-REVIZE-2.md` §11 a §14,
> z `docs/ARCHITEKTURA.md` (18 smluv, 3 s tvarem dat) a **měřením kódu**
> (naměřeno 8. 10. 2026; u každého čísla je řečeno, čím).
>
> **Co tenhle dokument NENÍ:** není design (to je GDD), není plán granulí
> (roadmapa) a **není seznam hotových věcí** — kde je hotovo, se **měří**
> (definice hotovo, GDD §12).
>
> **Jak se mění:** TDD je **stav** — přepisuje se. Naměřené případy a vady
> (hlavně §10) se **needitují**, jen doplňují.

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
v plánu je, ale je blokovaná mrtvou granulí `world.map` (`scripts/world.gd` =
**0 B**). Dokud přepis neproběhne, je **10 hotových komponent mrtvá knihovna**:
`hud.gd`, `save.gd`, `combat.gd`, `mining.gd` a `offline.gd` hledají
`get_parent().component(id)` — a **v `scripts/` není ani jedna funkce
`component(`** (naměřeno: `grep` nad `scripts/`, 0 výskytů), takže v běžící hře
dostanou `null`. **Zároveň je to podmínka cesty B** (§11): kdyby se oddělení
simulace a zobrazení porušilo, byla by síť přepis jádra.

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
- **Tik řídí kořen**, ne jednotlivé komponenty. Komponenta **nesmí** mít vlastní
  `_process`/`_physics_process` s vlastním časem — jinak si každá vymyslí svůj
  čas a **budou se hádat o to, co se stalo dřív** (`VSTUPY` §6).
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
| **engine** | smyčka, tik, vstup, okno, registr | `main.tscn`, `scripts/game.gd` (kostra) |
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

## 3. Smlouvy komponent (18) — s tvarem dat

**Agent volá jen to, co komponenta poskytuje (`provides`), nikdy nečte cizí
vnitřek.** Smlouva bez tvaru dat je jen jméno — a podle jména si agent vymyslí
zbytek. Naměřeno: `ARCHITEKTURA.md` §2 má **18 smluv, tvar dat jen 3**
(`sim.combat`, `Hráč → move`, `Ukládání → pozice`); důsledek byl konkrétní —
`get(attr)` v dokumentu vs. `hodnota(attr)` v kódu, `trade(player, item)` vs.
`buy/sell/gold`, `component(name)`, který **v `scripts/` vůbec není**.

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
- **status:** **`neexistuje`** — `scripts/world.gd` je **0 B** (naměřeno).
  Vlastní ho **dvě** granule (`world.map`, `world.nodes`), obě nehotové;
  `save.gd:71–74` na něm **už** volá `snapshot()`/`restore()`.

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
  dlaždic v `level.gd`** — hráč proto chodí po stejných osách jako mapa
- **acceptance:** test **ZAVOLÁ `move()`**, změří **posun** a porovná jeho sklon
  se sklonem osy dlaždice, který si **PŘEČTE z `level.cell_center`** (ne
  z konstanty opsané do testu); dále ZAVOLÁ `die()` a ověří, že vznikl uzel ve
  skupině `corpse`, inventář se vyprázdnil a hráč stojí na `level.spawn_cell`
- **status:** `hotovo` (`scripts/player.gd`, 191 řádků; smlouva `move` je závazná od 3. 10. 2026)

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
- **status:** `částečně` (`scripts/mining.gd`, 72 řádků; bere komponenty z registru, který v běžící
  hře není → vrací prázdno, viz `TDD` §10 vada 3)

### 3.11 `Crafting` — `scripts/crafting.gd`

- **poskytuje:** `smelt() -> Dictionary`, `forge() -> Dictionary`,
  `repair(item) -> bool`
- **spotřebovává:** `Skills`, `Attributes`, `Item`, `Data`
- **tvar dat:** recept = `{id, name, inputs: [{id, amount}], outputs: [{id,
  amount}]}` (přesně to, co je dnes v `recipes.json`); výsledek výroby =
  `{ok: bool, id: String, kvalita: int, zmetek: bool}`
- **odkud čísla:** **kvalita = `dovednost/20` → 0–5 stupňů** (GDD §9.2);
  palivo/opotřebení/zmetkovost jsou **otevřený bod `O-1` GDD** — dokud není
  rozhodnutý, smí být ve vzorci **jen to, co je rozhodnuté**
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
- **status:** `částečně` (`scripts/assist.gd`, 17 řádků; `assist` je **non-goal `N9`** pro MVP —
  smlouva zůstává, ale nic na ní v MVP nestaví)

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
- **status:** **`neexistuje`** — `scripts/game.gd` je **monolit** (377 řádků)
  a **`func component(` v `scripts/` není ani jednou** (naměřeno)

### 3.19 Souhrn: co má tvar dat a co ne

| | Stav 8. 10. 2026 |
|---|---|
| Smluv celkem | **18** |
| S tvarem dat **před** TDD | **3** (`sim.combat`, `Hráč → move`, `Ukládání → pozice`) |
| S tvarem dat **po** TDD | **18** (tabulky výš) |
| Komponent, které v `scripts/` **neexistují** | **3** (`world.gd` = 0 B, `npc.gd`, `enemy.gd`) |
| Komponent, které fungují v běžící hře | **2** (`level.gd`, `player.gd` — naměřeno, `game.gd` instancuje jen ty) |

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
| tik, registr, fronty příkazů a událostí, seed | `game.gd` (kostra) | všichni přes registr | **dnes neexistuje jako kostra** |
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

## 9. Brány: co měří a kde mají slepá místa

**Tvrdá brána je jen jedna** — `check-schema.py` (rozpor v deklaraci je
objektivní fakt); ostatní jsou poradní nebo mají **naměřená** slepá místa.
Detail: **`docs/BRANY-HRY.md`** (sem se přesunul 7. 10. 2026 ze skillu
`orchestra`).

| Brána | Co měří | ⚠ Naměřené slepé místo |
|---|---|---|
| `.forge/check-schema.py` | deklarace (`spec.json`), mapy, vykreslování a dlaždice musí říkat totéž číslo | — (tvrdá) |
| `.forge/check-assets.py` | sprity proti specu (výška, okraj, díry v siluetě, barvy) | **animace se neměří** — chůze je rozložená po vrstvách v `tools/blender/sprites/`, v `assets/sprites` nejsou `walk_*`; limit IoU se **nikdy neuplatní** (brána to hlásí jako poznámku) |
| `.forge/check-wiring.py` | každá funkce je odněkud volaná | **na jiném enginu hlásí zelenou nad NULOU souborů** (`:73` čte jen `scripts/*.gd`); **čte i `tests/`**, takže funkce zmíněná jen v testu se počítá jako použitá |
| `.forge/verify-level-render.py` | že snímek hry odpovídá mapě | — (nemá offline test) |
| `.forge/vision.mjs` | **vidí** (režimy `presence`/`diff`) | **neblokuje** — `exit 1` běh nezhodí (v CI `\|\| echo`); názor modelu má chybovost |
| `.forge/baseline.py` | co je vizuálně schválené (LGTM) a co se změnilo | **LGTM cache je lokální optimalizace — v CI neplatí nikdy** (`baseline.py:252` chce obrázek uvnitř repa, CI píše do `/tmp/frames`) |
| `tests/run_tests.gd` | herní kontroly | **podmíněný test je tiše zelený**: v souboru o **1406 řádcích** má `has_method` **26 řádků** a **39 výskytů** (hrubě; po odstranění komentářů **20 / 33**) — funkce, která není, se **přeskočí** |

**Pořadí kroků v CI je dané a testuje se** (naměřeno z `.github/workflows/ci.yml`,
181 řádků, job `test-and-build`): checkout → cache Godotu → instalace Godotu →
**import assetů** → **kontrola schématu** → **testy** → kontrola assetů →
kontrola zapojení → smoke (hra se spustí bez `SCRIPT ERROR`) → snímek hry →
`verify-level-render` → **vision** (neblokuje) → export buildů.

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
co dokument odhalí, **zapíše**, neopraví mimochodem. Všechny vady níž jsou
**naměřené 8. 10. 2026** (u každé je čím).

| # | Vada | Důkaz | Dopad |
|---|---|---|---|
| 1 | **`Economy.price()` vrací 0 pro každý skutečný předmět** | `economy.gd:14–30` čte `item.material` (očekává `"wood"/"stone"/"metal"`) a `item.quality` (očekává `"common"…`), ale `item.gd:6–10` má `material` z `items.json` (kde klíč **není** → `""`) a `kvalita: int` | obchod je **zdarma**; `price()` je zároveň druhý zdroj pravdy o kvalitě |
| 2 | **`Item.repair()` předmět ZNIČÍ** | `item.gd:36` nastaví `trvanlivost = 20` natvrdo; `items.json` deklaruje `durability` 100 (meč) a 150 (zbroj) | „oprava“ sníží trvanlivost ze 100 na 20 |
| 3 | **Registr komponent v kódu NENÍ** | `grep` na `func component(` v `scripts/` = **0 výskytů**; `hud.gd:90`, `save.gd:148`, `combat.gd:125`, `mining.gd:70`, `offline.gd:55` ho volají | v běžící hře dostanou `null` → HUD ukazuje nuly, `save()` neuloží nic |
| 4 | **`scripts/world.gd` = 0 B** | naměřeno: 0 bajtů, 0 řádků; vlastní ho **dvě** granule (`world.map`, `world.nodes`), obě nehotové | blokuje `engine.shell`; `save.gd` na něm už volá `snapshot()` |
| 5 | **`save.gd:14` má zastaralý komentář** | tvrdí, že `player.gd` inventář „nemá“; naměřeno `player.gd:52` (`inventory`), `:130` (`add_item`), `:136` (`remove_item`) | komentář popírá kód — kdo mu věří, „opraví“ fungující věc |
| 6 | **`assets/spec.json` nemá klíč `projekce`** | `level.gd:74` → `{}`, `:83` odvodí izometrii z `96 ≠ 48` | izometrie je **odvozená**, ne deklarovaná → druhé místo pravdy o projekci |
| 7 | **Název hry se rozejšel ve třech zdrojích** | `project.godot:9` = `uo-sandbox`; `forge.json` a `.forge/vision-profile.json` = `uo-shadows`; repo = `uo-shadows` | hledání pod jedním jménem selže (řeší GDD `O-3`) |
| 8 | **`npc.gd` a `enemy.gd` v repu NEJSOU** | `scripts/` má 15 souborů; žádný z nich se tak nejmenuje | dvě smlouvy (`Npc`, `Enemy`) nemají implementaci, přestože na ně plán navazuje |
| 9 | **`done` není měření: v `.forge/roadmap.json` je 21 granul a `done: true` = 15, ale hra používá 2** | `roadmap.json`: 21 granul, `done: true` = 15 (stav po přepsání roadmapy 8. 10. 2026; **před ním 22 / 13** — ve svém čase správná čísla); produkční cesta instancuje `level.gd` a `player.gd` | „hotovo“ dnes není měření (definice hotovo to mění) |
| 10 | **`assets/data/*.json` nemá klíč `material`** | `items.json`: `id`, `name`, `durability`, `damage`, `armor_rating`; `item.gd:25` ho čte jako nepovinný | viz vada 1 |

**Co z toho plyne pro plán:** vady 1–4 jsou na kritické cestě milníků `M0`
(kostra a registr) a `M3` (výroba a ekonomika). **Nejsou to úkoly TDD** — TDD
je jen **pojmenovává**, aby se na ně nezapomnělo a aby je plán mohl zařadit.

---

## 11. Co v tomhle dokumentu ZÁMĚRNĚ NENÍ

- **Design a obsah** (co je zábava, V1–V8, non-goals, čísla obsahu) →
  `docs/GDD.md`. TDD říká **jak**, ne **co** a **proč**.
- **Vzhled, rozměry spritů, pipeline a katalog assetů** → `docs/ADD.md`
  a strojově `assets/spec.json`.
- **Plán granulí, pořadí a vlny** → `.forge/roadmap.json` (vzniká z milníků
  `M0`–`M6` v GDD §12). **TDD neurčuje, co se kdy staví.**
- **Samotná síťová vrstva (cesta `B`)** — TDD drží jen podmínku, aby se dala
  přidat (`TDD` §1.4). Kdy a jestli se staví, je rozhodnutí mimo TDD.
- **Konkrétní ladicí hodnoty** (mrtvá zóna, doba náběhu, obtížnost uzlů) —
  patří do ladění a do otevřených bodů GDD (GDD §14 tam).
- **Historie rozhodnutí a jejich ceny** → `_analyza/DESIGN-REVIZE-2.md`
  (needituje se).
