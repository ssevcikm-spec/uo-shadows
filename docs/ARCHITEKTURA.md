# Architektura — UO Shadows (uo-shadows)

> Autoritativní zdroj pravdy pro rozpad na granule. Vzniklo z vize uživatele
> metodou skillu `game-developer` (rozpad shora dolů). Nahrazuje plán v
> `DESIGN.md` (plánovač) — tenhle soubor je jediný závazný.
> Toto je závazná kopie v repu — agenti čtou ji. Autorská kopie pro `forge plan`
> je mimo repo (`gameforge/projects/uo-sandbox/docs/ARCHITEKTURA.md`).

## 0. Cíl

Moderní Ultima Online: izometrický sandbox, kde hráč hledí do „zmenšeného
skutečného světa" — realistická, praktická výbava (zbraně, zbroj, nástroje)
s navazujícími fantasy prvky (příšery, magie, materiály, magické vlastnosti).
Dovednosti rostou používáním a v synergii s atributy dělají postavu silnou.
Svět je škálovaný dovedností (ne levelem), vše je interaktivní, činy mají
důsledek. Ekonomika stojí na výrobě, loot ji doplňuje. MMO s offline režimem
pro lidi s prací a rodinou.

### Pilíře (nevyjednatelné)

1. **Synergie skill + atribut** — Dex → rychlost útoku, Int → síla kouzel, skill → lepší materiály.
2. **Svět škálovaný dovedností, ne levelem** — žádný level scaling (antiteze WoW).
3. **Vše interaktivní** — těžit každý kámen i strom, otevřít každé dveře, používat nástroje tovaryšů.
4. **Výroba = střed ekonomiky; loot doplňuje** (vzácné/mocné z lootu, část jen z lootu).
5. **Offline režim je legitimní, ale ohraničený; aktivní hra je vždy lepší.**
6. **Asistence při hraní = reaktivní pravidla, ne bot.**
7. **Obsah je DATA, ne kód** — materiály, recepty, skilly, příšery, kouzla v datech; nový obsah = nový záznam, ne nová granule.

## 0.1 Rozsah — první hratelný řez (MVP)

- jeden ostrov / město + 1 důl (železo, kámen) + 1 les (dřevo)
- smyčka: `těžit → tavit → kovat → používat → opravovat`
- 1 druh nepřítele (drak až později)
- simulace běží lokálně (single-player); server/MMO vrstva až později
- MMO, plná interaktivita a draci = vize, ne obsah MVP

## 0.2 Požadavky (mechaniky)

| id | Požadavek |
|---|---|
| REQ-skills | dovednosti 0–100, rostou používáním; **bez celkového stropu** (strop = budoucí přepínatelný parametr) |
| REQ-attrs | atributy Str/Dex/Int + armor rating; resistence později |
| REQ-craft | těžba → tavení → kování → použití → oprava (trvanlivost) |
| REQ-econ | výroba = střed, loot doplňuje; propad (sink) skrze trvanlivost/spotřebu |
| REQ-interact | vše interaktivní (kámen, strom, dveře, nástroje) |
| REQ-world | svět škálovaný dovedností, ne levelem |
| REQ-offline | offline = jedno „rozřešení" (boj/výroba/těžba dle skillu × obtížnosti), denní strop |
| REQ-chars | N postav na hráče, právě 1 „běžící" (aktivní nebo offline úkol); ostatní spí |
| REQ-assist | asistence = reaktivní pravidla (spoušť → akce) přes server, spotřebovává skutečné zdroje |
| REQ-mmo | server-autoritativní simulace; MMO jako vrstva nad simulací |
| REQ-persist | trvalý svět (činy mají důsledek); suroviny se obnovují — viz REQ-respawn |
| REQ-death | smrt = ztráta všeho na těle (mrtvola); insurance/blessing = budoucí granule |
| REQ-trade | zlato + 1 NPC obchodník (prodej/nákup) |
| REQ-respawn | suroviny se obnovují (MVP: statické uzly + časovač; budoucnost: objevitelné žíly podle skillu) |

## 0.3 Schopnosti (capabilities — ověřitelné věty)

- hráč vytěží rudu (výtěžek dle skillu těžby × obtížnosti suroviny)
- hráč vytaví ingot
- hráč uková zbraň (kvalita dle skillu kovářství)
- hráč použije zbraň (sníží trvanlivost; poškození dle Str, rychlost dle Dex)
- hráč opraví zbraň (za ingot)
- hráč bojuje (hit chance dle Dex, damage dle Str, armor rating snižuje zranění)
- hráč sesílá kouzlo (úspěšnost a mana dle Int) — *později, magie není v MVP*
- hráč nastaví asistenci (spoušť → akce)
- offline: postava vyřeší boj/těžbu/výrobu za dobu nečinnosti, s denním stropem
- hráč přepíná mezi postavami (jen jedna běží)
- hráč zemře a ztratí vše na těle (mrtvola s výbavou k vyzvednutí)
- hráč prodá/nakoupí u obchodníka za zlato
- vytěžená surovina se po čase obnoví (respawn)

## 0.4 Obsah MVP (data prvního řezu)

Konkrétní minimální obsah, na kterém se postaví datová vrstva (§1.1).

| Kategorie | Obsah |
|---|---|
| Suroviny | železná ruda, dřevo, kámen |
| Meziprodukt | železný ingot (tavení) |
| Výrobky | železný meč (ingot + dřevo), železná zbroj (ingoty) |
| Uzly (s respawnem) | žíla železa, strom, skála |
| Příšera | 1 (kostlivec/slime) — drop: zlato + občas ruda |
| NPC | 1 obchodník (prodej/nákup) |
| Skilly (4) | těžba, dřevorubectví, kovářství, boj na blízko |
| Atributy | Str, Dex, Int |
| Měna | zlato |
| Kouzla | 0 v MVP (magie = pozdější granule; Int už je v modelu) |

## 1. Architektura (vrstvy + směry závislostí)

| Vrstva | Odpovědnost | Soubory |
|---|---|---|
| engine | smyčka, vstup, okno | `main.tscn`, `scripts/game.gd` (jen kostra) |
| svět | mapa, dlaždice, izo projekce, průchodnost | `scripts/world.gd`, `scripts/level.gd` |
| entity | hráč, NPC, nepřítel, předmět | `scripts/player.gd`, `npc.gd`, `enemy.gd`, `item.gd` |
| simulace | skilly, atributy, řemesla, boj, ekonomika, offline, asistence | `scripts/skills.gd`, `attributes.gd`, `crafting.gd`, `mining.gd`, `combat.gd`, `economy.gd`, `offline.gd`, `assist.gd` |
| prezentace | HUD, kamera | `scripts/hud.gd` |
| persistence | ukládání/načítání | `scripts/save.gd` |
| síť | MMO vrstva (později) | `scripts/net.gd` |
| nástroje | brány ověřující vzhled a zapojení | `.forge/check-*.py` |

**Pravidlo závislosti:** shora dolů (prezentace → simulace → svět → engine). Žádné kruhy.
**Simulace nezávisí na síti** — MMO je vrstva nad server-autoritativní simulací (tik),
takže první řez běží lokálně a MMO se přidá, aniž by se měnilo jádro.

## 1.1 Extenzibilita (jak se hra rozšiřuje)

Dvě cesty rozšíření, zásadně rozdílné náročnosti:

| Druh | Příklady | Jak se přidává |
|---|---|---|
| **Obsah (data)** | materiálová žíla, nový skill, recept, příšera, kouzlo | nový záznam v datech (JSON/Resource) — **bez kódu** |
| **Systém** | taming/followers, pet system, levelovací výbava | nová granule (komponenta + rozhraní), napojená na existující vrstvy |

Proto **MVP musí postavit datovou vrstvu správně hned** (tabulky surovin, receptů,
skillů, příšer), i když zatím obsahuje jen pár položek. Pak „přidat žílu na zlato"
= jeden řádek, ne přepis `mining.gd`. Nové systémy (taming, pet) se přidávají jako
nové granule do DAG, aniž by se měnilo jádro.

## 2. Smlouvy (kontrakty — provides/consumes)

Rozhraní komponent. Agent volá jen `provides`, nikdy nečte cizí vnitřek.
Tohle je vrstva, která umožňuje paralelní granule (každý staví proti smlouvě,
ne proti nedokončenému sousedovi).

| Komponenta | Soubor | Poskytuje (provides) | Spotřebovává (consumes) |
|---|---|---|---|
| Data | `assets/data/*.json` | materiály, skilly, recepty, příšery, předměty | — |
| Atributy | `scripts/attributes.gd` | `get(attr)`, `derived()` (damage, hit chance, attack speed, mana, carry) | — |
| Skilly | `scripts/skills.gd` | `add(skill, n)`, `get(skill)` | — |
| Úroveň | `scripts/level.gd` | `load_file()`, `is_walkable_cell()`, `cell_center()` (nese izo projekci hry), `cell_at()`, `spawn_cell` | data levelů |
| Svět | `scripts/world.gd` | uzly surovin: `gather(cell)`, `is_walkable(pos)`, respawn (**PRÁCE V `main` NENÍ** — viz §2.2) | Úroveň |
| Předmět | `scripts/item.gd` | def, trvanlivost, materiál, kvalita | Data |
| Hráč | `scripts/player.gd` | `move(dir)`, stav `hp`/`max_hp`/`mana`/`max_mana`/`target`, `inventory` + `add_item()`/`remove_item()`, `equipped`, `die()` — **tvar dat viz §2.2** | Úroveň (kolize), Předmět, Atributy, Skilly |
| NPC | `scripts/npc.gd` | `trade(player)` (koupit/prodat) | Předmět, Ekonomika |
| Nepřítel | `scripts/enemy.gd` | `attack()`, `drop_loot()` | Předmět, Boj |
| Těžba | `scripts/mining.gd` | `gather(node)` (výtěžek dle skillu × obtížnosti) | Skilly, Svět, Data |
| Výroba | `scripts/crafting.gd` | `smelt()`, `forge()`, `repair()` | Skilly, Atributy, Předmět, Data |
| Boj | `scripts/combat.gd` | `resolve(attacker: Node, defender: Node)` → `{hit, damage}` — **tvar dat viz §2.1** | Atributy, Skilly, Předmět |
| Ekonomika | `scripts/economy.gd` | `price(item)`, `trade(player, item)` | Předmět, Data |
| Offline | `scripts/offline.gd` | `resolve(char, úkol, doba)` (ohraničené) | Skilly, Těžba, Výroba, Boj |
| Asistence | `scripts/assist.gd` | `add_rule(spoušť, akce)`, `evaluate(char)` | Hráč, Předmět |
| Ukládání | `scripts/save.gd` | `save()`, `load()` | celý stav |
| HUD | `scripts/hud.gd` | `update(...)` | Hráč, Skilly, Atributy, Ekonomika |
| Kostra | `scripts/game.gd` | `component(name) -> Node` (registr), sestavení scény | všechny komponenty (přes registr) |

### 2.1 Tvar dat a přijímací kritérium u smluv (doplněno 2. 10. 2026)

**Proč to tu je:** do 2. 10. 2026 nesla tabulka výš jen JMÉNA API. Agent dostal
`resolve(att, def)` bez typu, bez původu čísel a bez kritéria — a výsledek byl
takový, jaký byl: `sim.combat` se zapsal jako `done` (úloha #135) s funkcí,
která **nemohla fungovat** (volala `attacker.hodnota("Dex")`
i `attacker.hodnota("boj_na_blizko")` na TÉMŽ objektu, ačkoli to jsou dvě různé
komponenty), **nikdo ji nezavolal** a test se ptal jen `has_method("resolve")`.
Naměřeno téhož dne: `combat.gd` volal `has()` — **Godot 3 API**, které
v Godotu 4 neexistuje — a protože to bylo uvnitř `if hit:`, spadlo to jen
při zásahu (≈ 50 %).

**Vzor zápisu smlouvy (platí pro každou další):**

```
resolve(attacker: Node, defender: Node) -> Dictionary
  attacker : Node  uzel kostry; čísla se berou z REGISTRU na rodiči
  defender : Node  uzel kostry s vlastností armor_rating
  vrací     {hit: bool, damage: int}   – VŽDY, i když komponenty chybí
  odkud:     get_parent().component("Attributes").hodnota("Dex"/"Str")
             get_parent().component("Skills").hodnota("boj_na_blizko")
             attacker.vybrana_zbran (nebo .zbran) -> uzel s vlastností damage
             defender.armor_rating
  vzorec:    hit  = randf() < 0.5 + (Dex + boj_na_blizko) / 200
             damage = max(0, 1 + Str/10 + zbraň.damage − obránce.armor_rating)
  acceptance: test resolve() ZAVOLÁ a ověří {hit, damage} (zásah i minutí);
             `has_method("resolve")` NESTAČÍ
```

**Tři pravidla, která z toho plynou:**

1. **Kdo je kdo** — smlouva pojmenuje typ a roli obou stran, ne jen `(att, def)`.
2. **Odkud jsou čísla** — u každé hodnoty se řekne, která komponenta ji drží.
   Když jeden objekt poskytuje dvě různé věty, je to **dvě komponenty**.
3. **Přijímací kritérium** — co musí test ZAVOLAT a co musí naměřit.
   Slovem `acceptance` v roadmape se rozumí přesně tohle.

### 2.2 Smlouva `Hráč → move(dir)` — ROZHODNUTO 3. 10. 2026

**Proč to tu je:** granule `entity.player` byla zapsaná jako `done`, ale
`scripts/player.gd` v `main` **neměl `move()`, inventář ani `die()`** — a přitom
je volaly jiné komponenty (`economy.gd:39,47` volá `add_item`/`remove_item`,
`assist.gd:11–15` čte `hp`, `max_hp`, `mana`, `max_mana`, `target`). Vznikla
z toho **dvojí vada**: `assist.evaluate()` vypsal `SCRIPT ERROR` a **vrátil
`[]`** (asistence tiše nic nedělala) a `hud.gd` chybějící `hp` **obcházel**
přes `has_method("get_hp")` → ukazoval **HP: 0**, což vypadá jako naměřená nula.
Do 3. 10. 2026 nebylo nikde napsané, co je smlouva — a testy se ptaly jen
`has_method("evaluate")`.

```
move(dir: Vector2, delta: float = -1.0) -> void
  dir    : Vector2  směr VE HŘE (ne v pixelech): „vpravo“ (1,0), „dolů“ (0,1)
  delta  : float    čas kroku;  delta < 0  znamená „posun o JEDEN krok
                    SPEED/60“ — používají testy, které nesmějí čekat na snímek
  posun  : hráč se posune O JEDNU Z IZOMETRICKÝCH OS dlaždic, ne po obrazovce
  odkud:   izo poměr je (dx−dy)·0,5 a (dx+dy)·0,25 — TÝŽ poměr, jaký má
           kreslení dlaždic v `scripts/level.gd` → `cell_center()` a jaký
           deklaruje `assets/spec.json` (izometrie 2:1). Kolize se ptá
           `level.is_walkable_at(pos)`; poslední krok dělá `_step(target)`
           (klouzání po jedné ose) a `move()` drží hráče v obrazovce
  volá ho: `_physics_process()` (čtení kláves) — JEDINÁ cesta, kterou se mění
           pozice; testy a budoucí `engine.shell` taky
  acceptance: test `move()` ZAVOLÁ, změří POSUN a porovná jeho sklon se sklonem
           osy dlaždice, který si PŘEČTE z `level.cell_center` (ne z konstanty
           opsané do testu). `has_method("move")` NESTAČÍ.
```

**Stav hráče a inventář (co už volají jiné komponenty):**

| Prvek | Typ | Výchozí | Kdo to volá / čte |
|---|---|---|---|
| `hp`, `max_hp` | `int` | 100 | `assist.gd:11`, `hud.gd:47` |
| `mana`, `max_mana` | `int` | 50 | `assist.gd:13` |
| `target` | `Node` nebo `null` | `null` | `assist.gd:15` (`target.hp <= 0`) |
| `inventory` | `Array` | `[]` | `save.gd` (granule `persist.save.state`) |
| `add_item(item)`, `remove_item(item)` | `void` | — | `economy.gd:39,47` |
| `equipped` | `Node` nebo `null` | `null` | `hud.gd:44` |
| `die()` | `void` | — | smlouva (`REQ-death`); staví mrtvolu `Area2D` ve skupině `corpse` a vrací hráče na `level.spawn_cell` |

**Tři pravidla, která z toho plynou (obecně, ne jen pro hráče):**

1. **Rozhraní je jedna cesta.** Kdyby pohyb počítalo i `_physics_process`
   zvlášť, existují dvě implementace téhož a měří se ta nepoužívaná.
2. **Mrtvá větev se nepozná podle testu, který ji „kryje".** `player.gd` měl
   `if level.has_method("iso_position")` — metodu, kterou `level.gd` NIKDY
   neměl (má ji jen `_retired/world.gd`), takže se vždy použila větev `else`
   a hráč chodil **1:1 podle obrazovky** místo 2:1 po dlaždicích. Test to
   „kryl" tak, že v souboru hledal řetězec `level.iso_position` — tedy měřil
   PŘÍTOMNOST TEXTU a navíc zakazoval legitimní kód.
3. **Kdo nese projekci, musí být napsané.** Projekci nese `level.gd`
   (`cell_center`/`cell_at`); `world.gd` ji **nesmí opisovat** — přesně kvůli
   druhému číslu mřížky byl starý `world.gd` přesunut do `_retired/`.

**Naměřený rozdíl (sonda `tests/_sonda-pohyb.gd`):**

| směr | PŘED (1:1) | PO (izo osy) |
|---|---|---|
| vpravo | (2,167; 0) sklon 0 | (1,938; 0,969) sklon 0,5 |
| vpravo+dolů | (1,532; 1,532) 45° | (0; 2,167) svisle |

Osa dlaždice je `(48, 24)` → sklon **0,5**. Hráč teď jde po stejných osách
jako mapa. **Je to viditelná změna ovládání** — rozhodl o ní uživatel
3. 10. 2026.

## 3. Granule (atomické jednotky)

Každá granule = jeden soubor, vlastní `owns`, deklaruje `depends_on` a je
samostatně ověřitelná testem (test se píše před implementací).

### Velikost granule se řídí modelem (ne naopak)

60 řádků je **výchozí míra pro slabý model**, ne dogma. Když je soudržná
jednotka větší a rozsekání by vytvořilo **umělý šev** (stav entity + pravidla
smrti + inventář patří k sobě; rozseknutí by donutilo agenta lepit polovičaté
API, které stejně vyjde dráž), smí být granule větší — ale jen s deklarací
v `roadmap.json` (`size_lines` + `model: strong`) a jen pro **dostatečně silný
model**. Bez deklarace platí `<= 60` a `any`.

Důsledky pro orchestr (pravidla, ne přání):

- conductor vydá granuli `model: strong` jen silnému modelu; slabému ji
  nevydá, i kdyby fronta stála,
- brána auto-merge posuzuje limit podle deklarace granule, ne podle globálních
  60 řádků — jinak by PR z velké granule systematicky visel v ruční frontě,
- když orchestr silný model nemá (jen free rotace), granule `model: strong`
  zůstávají ve frontě a plán se buď doplní o silný model, nebo se přerozloží.

| Granule | size_lines | model | Proč ne 60 |
|---|---|---|---|
| `entity.player` | `<= 120` | strong | pohyb + inventář + vybavení + smrt/mrtvola = jeden celek |
| `sim.crafting` | `<= 100` | strong | tavení + kování + oprava + kvalita nad jedním receptovým modelem |
| `sim.offline` | `<= 100` | strong | tři druhy rozřešení + denní strop = jeden algoritmus |
| `entity.enemy` | `<= 90` | strong | hp + útok + loot + respawn = jeden životní cyklus |
| `engine.shell` | `<= 120` | strong | rozřezání monolitu: registr + přepojení scény + sjednocení skillů = jeden řez |

Ostatních 13 granulí zůstává na `<= 60` — zvládne je slabý model.

1. `data.content` — `assets/data/*.json` — depends: — → schémata obsahu
2. `core.attributes` — `scripts/attributes.gd` — depends: — → Atributy
3. `core.skills` — `scripts/skills.gd` — depends: — → Skilly
4. `world.level` — `scripts/level.gd` — depends: — → Úroveň
5. `world.map` — `scripts/world.gd` — depends: `world.level` → Svět (izo, uzly, respawn)
6. `entity.item` — `scripts/item.gd` — depends: `data.content` → Předmět
7. `entity.player` — `scripts/player.gd` — depends: `core.attributes, core.skills, world.map, entity.item` → Hráč (**size `<= 120`, model `strong`**)
8. `entity.npc` — `scripts/npc.gd` — depends: `entity.item, sim.economy` → NPC obchodník
9. `entity.enemy` — `scripts/enemy.gd` — depends: `entity.item, sim.combat` → Nepřítel (**size `<= 90`, model `strong`**)
10. `sim.mining` — `scripts/mining.gd` — depends: `core.skills, world.map, data.content` → Těžba
11. `sim.crafting` — `scripts/crafting.gd` — depends: `core.skills, core.attributes, entity.item, data.content` → Výroba (**size `<= 100`, model `strong`**)
12. `sim.combat` — `scripts/combat.gd` — depends: `core.attributes, core.skills, entity.item` → Boj
13. `sim.economy` — `scripts/economy.gd` — depends: `entity.item, data.content` → Ekonomika
14. `sim.offline` — `scripts/offline.gd` — depends: `core.skills, sim.mining, sim.crafting, sim.combat` → Offline (**size `<= 100`, model `strong`**)
15. `sim.assist` — `scripts/assist.gd` — depends: `entity.player, entity.item` → Asistence
16. `persist.save` — `scripts/save.gd` — depends: `core.skills, core.attributes, entity.player, world.map, sim.economy` → Ukládání
17. `ui.hud` — `scripts/hud.gd` — depends: `core.skills, core.attributes, entity.player, sim.economy` → HUD
18. `engine.shell` — `scripts/game.gd` — depends: všech 16 výše → Kostra + registr komponent (**size `<= 120`, model `strong`**)

### Migrace monolitu (`engine.shell`)

Dnešní `game.gd` je starý monolit (vlastní dovednosti `tezba/kovarstvi/alchymie`,
suroviny, save/load, NPC = tavení, denní cyklus). Granule `engine.shell` ho
přepíše na kostru:

- komponenty se instancují **z pevného registru** (jméno uzlu = název komponenty),
  chybějící soubor se přeskočí → hra zůstane hratelná po celou migraci,
- scéna (úroveň, hráč, HUD, NPC) se sestaví z veřejných `provides` komponent,
  ne z vnitřků,
- z monolitu se **smaže** vše, co převzaly komponenty (dovednosti, suroviny,
  ukládání, tavení u NPC) — brána wiring hlásí nepoužité funkce jen jako poznámku,
- **sjednocení dovedností** na 4 skilly z dat: `tezba, drevorubectvi, kovarstvi,
  boj_na_blizko` (alchymie a denní cyklus jsou out-of-scope — viz DESIGN.md),
- **změna je aditivní:** `_step`/`_physics_process` u hráče a uzel `Hud`
  (Label se skóre) zůstávají, dokud je nevymění komponenty — stojí na nich
  testy i hratelnost mezi vlnami.

Granule běží **poslední** (6. vlna), až jsou všechny komponenty sloučené —
jinak by se nemělo kam registrovat. Rozsekání tohohle řezu na menší granule by
vytvořilo umělý šev: půlka hry na starých polích a půlka na komponentách se
nedá nechat uležet mezi dvěma PR.

## 4. DAG a vlny (paralelizace)

Závislosti tvoří orientovaný acyklický graf. Granule ve stejné vlně mají
**disjunktní `owns`** → můžou běžet současně.

- **Vlna 0** (bez závislostí): `data.content`, `core.attributes`, `core.skills`, `world.level`
- **Vlna 1**: `world.map`, `entity.item`
- **Vlna 2**: `entity.player`, `sim.mining`, `sim.crafting`, `sim.combat`, `sim.economy`
- **Vlna 3**: `entity.npc`, `entity.enemy`, `sim.offline`, `sim.assist`
- **Vlna 4**: `persist.save`, `ui.hud`
- **Vlna 5** (migrace monolitu): `engine.shell`

Tohle je 18 granulí v 6 vlnách — první řez, ke kterému se MVP (§0.4) přesně mapuje.

## Co je dál (tooling)

1. ~~zapsat granule do `roadmap.json` jako DAG (migrace z lineárního seznamu)~~ ✅
2. ~~conductor: číst `depends_on`, povolit N souběžných větví, hlídat `owns`~~ ✅
3. každá granule dostane test (failing-first) + brany z §6 skillu `game-developer`
4. ~~conductor: číst `size_lines`/`model` — `model: strong` řadit do fronty silného
   modelu (slabým nevydávat) a `size_lines` předat jako limit bráně auto-merge
   (vstup `max_lines` workflowu agenta; bez něj platí 60)~~ ✅ (30. 9.: conductor +
   `strongModels` v providers.json + FORGE_MIN_STRONG v pick-provider)
5. conductor: selhanou granuli znovu do fronty po cooldownu (RETRY_HOURS) — ✅
   (30. 9.: retry + done-detekce přes sloučené PR, konec smyčky „world.level
   se vydává znovu")
