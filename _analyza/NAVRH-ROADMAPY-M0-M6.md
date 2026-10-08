# NÁVRH: nová `.forge/roadmap.json` pro milníky `M0`–`M6`

> **⚠ APLIKOVÁNO 8. 10. 2026 (uživatel odsouhlasil „zapsat hned“).**
> `.forge/roadmap.json` **je nahrazená** — tenhle dokument je od teď **záznam
> o návrhu a jeho aplikaci**, ne plán.
> **S čím se to aplikovalo jinak, než návrh §4 říkal** (a proč):
> návrh chtěl do JSON dát **jen 5 granulí `M0`+`M1`**; aplikováno je **21 granulí**,
> protože `depends_on` odkazuje na **starší granule** (`world.level`, `entity.player`,
> `persist.save`) — kdyby v souboru nebyly, conductor by je nikdy nepovažoval
> za sloučené a nové granule by se nevydaly. Zůstaly tedy **zachované granule
> s prací v `main`** (a `done` se u tří srovnalo s gitem, viz §5 bod 1).
> **Navíc (nad rámec návrhu):** `entity.npc` a `entity.enemy` jsou **parkované**
> (v souboru nejsou, ale nejsou smazané — jsou v gitu a v §3 níž), protože byly
> **READY** a conductor by je vydal mimo pořadí milníků; vrátí se v `M4`/`M5`.
> **Stav po aplikaci (naměřeno):** 21 granulí, `done: true` 15, `done: false` 1
> (`world.nodes`), **vydatelná hned jediná: `engine.registry`** — přesně to je
> začátek `M0`. Pravidlo „dva grains, jeden soubor“ drží.
> **Strojová část `_analyza/roadmap-navrh.json` je tím historický artefakt**
> (obsahuje jen `M0`+`M1`); needituje se.
>
> **Co tenhle dokument JE:** **návrh k odsouhlasení** (a jeho záznam). Nahradil
> dnešní `.forge/roadmap.json` (22 granul z 29. 9. – 3. 10. 2026), který vznikl
> pro **jiný plán** — pro „první hratelný řez“ z `docs/ARCHITEKTURA.md` §0.1,
> tedy pro hru, která byla **sběračka dvou mincí**.
>
> **Zdroj rozhodnutí:** `docs/GDD.md` §12 (milníky `M0`–`M6`) a `docs/TDD.md`
> §3 (18 smluv s tvarem dat). **Odkud brát stav:** tenhle dokument je návrh;
> stav plánu je `.forge/roadmap.json`.
>
> **Vzniklo:** 8. 10. 2026. **Strojová část návrhu:**
> `_analyza/roadmap-navrh.json` (validní JSON, připravený k přesunu po
> odsouhlasení).
>
> **Co tenhle dokument NENÍ:** není plán práce pro člověka (to je GDD §12)
> a není rozhodnutí — **návrh se odsouhlasuje**.

---

## 1. Co je dnes naměřeno na staré roadmapě

Naměřeno 8. 10. 2026 čtením `.forge/roadmap.json` (26 706 B, klíče `_popis`
a `grains`):

| Co | Naměřeno | Co to znamená |
|---|---|---|
| Granulí | **22** | plán prvního řezu |
| `done: true` | **13** | ale hra používá **2 komponenty** (GDD §13) |
| `done` klíč chybí | **7** | `sim.crafting`, `entity.npc`, `entity.enemy`, `sim.offline`, `engine.shell`, `tests.harness`, `persist.save.state` |
| `done: false` | **2** | `world.map`, `world.nodes` |
| **Dva grains, jeden soubor** | **3×** | `world.map` + `world.nodes` → `scripts/world.gd` (oba **připravené** zároveň); `entity.player` + `entity.player.api` → `player.gd`; `persist.save` + `persist.save.state` → `save.gd` |
| `size_lines` jako **string** | 14 granul (`"<= 100"`) | limit pro auto-merge se z toho musí parsovat |
| `model: strong` | 9 granul | zbytek „any“ |
| `wave` | **0 granul** | plán je DAG přes `depends_on` (to je správně) |

**Tři vady, které z toho plynou a které musí návrh vyřešit:**

1. **`engine.shell` je blokovaná navždy.** Má **19 závislostí** — včetně
   `world.map` (mrtvá), `entity.npc` a `entity.enemy` (**nikdy neprošly**)
   a `entity.player.api` (hotová, ale jen duplikuje `entity.player`). Dokud se
   to nerozsekne, je **10 hotových komponent mrtvá knihovna** (GDD §13).
2. **Sémantický cyklus:** `engine.shell` vytváří registr komponent, ale
   `sim.combat`/`entity.enemy` registr **potřebují** — a jsou v `depends_on`
   před ním. To je kruh, který žádné pořadí nerozváže; musí se **rozseknout
   řezem** (registr jako samostatná, závislostí prázdná granule).
3. **Past „dva grains, jeden soubor“** je reálná: `world.map` a `world.nodes`
   jsou **obě připravené** a vlastní tentýž `scripts/world.gd`. Kdyby je
   conductor vydal současně, přepíšou se.

---

## 2. Pravidla, podle kterých je návrh postavený

1. **Jeden milník = hratelný stav, který je vidět na obrazovce** (`GDD` §12,
   rozhodnutí `P1`). Granule se zařazují podle **milníku**, ne podle vrstvy.
2. **Jeden grains = jeden soubor** (`owns`). **Dva grains smí vlastnit tentýž
   soubor, jen když je druhý `depends_on` první** — jinak je to past
   `world.map`/`world.nodes`. *(Nové pravidlo, vyplývá z měření.)*
3. **Registr komponent je první a bez závislostí.** Rozsekne cyklus z §1.2.
4. **Chybějící komponenta se přeskočí a ohlásí** — `engine.shell` se staví
   **aditivně** (`TDD` §7, `ARCHITEKTURA.md` §3). Hra zůstane hratelná po celou
   migraci.
5. **`prompt` se generuje ze smlouvy v `docs/TDD.md` §3**, ne ručně prózou.
   Naměřeno: `entity.npc` a `entity.enemy` mají **nejkratší zadání ze všech**
   (211 a 278 znaků) a jsou to **jediné dvě granule, které nikdy neprošly**
   (58 běhů, 0 úspěchů) — a v zadání `entity.npc` **není ani slovo o registru**,
   přitom celá architektura na registru stojí. *(Nález auditu; čísla jsou jeho.)*
6. **`tests/` se neplánuje jako granule.** `CONVENTIONS.md` §5 zakazuje
   agentovi měnit testy — a granule, která vlastní `tests/run_tests.gd`, se
   **nemůže sloučit sama**. Testy jsou **pravidlo**, ne práce agenta.
7. **`acceptance` zůstává `tests`/`wiring`/`render`** (schema se nemění), ale
   `docs/TDD.md` §3 u každé smlouvy říká, **co musí test ZAVOLAT**.

---

## 3. Milníky → granule (celý DAG)

**Legenda:** 🆕 nová · ✏️ přepis existující · ♻️ existuje, jen se zapojí ·
🗑️ návrh na vyřazení · `?` = ještě nerozhodnuté, patří do milníku

### M0 — Kostra (vidět: hra se spustí a nezhroutí se)

| id | owns | závisí na | proč |
|---|---|---|---|
| 🆕 `engine.registry` | `scripts/registry.gd` | **—** | `component(id)`, **pevný tik 50 ms**, fronty příkazů a událostí (`TDD` §1.1–1.3). **Bez závislostí schválně** — rozsekne cyklus |
| ✏️ `engine.shell` | `scripts/game.gd` | `engine.registry` | přepíše monolit (377 řádků) na scénu z komponent; **co v repu není, přeskočí a ohlásí** |

### M1 — Hýbu se (vidět: plynulý pohyb myší, objekty se nepřekrývají)

| id | owns | závisí na | proč |
|---|---|---|---|
| 🆕 `engine.input` | `scripts/input.gd` | `engine.registry` | **vstup → záměr pohybu**: pravé tlačítko, vzdálenost kurzoru (mrtvá zóna), WASD/šipky jako záložní cesta. **Frontu příkazů neplní sám** — jen vzorkuje vstup, aby frontu neměl dva pisatele (`TDD` §1.2 krok 1) |
| ✏️ `entity.move.smooth` | `scripts/player.gd` | `engine.registry`, `world.level`, `engine.input` | plynulý pohyb, stamina, vyhlazení rozběhu a zastavení (`GDD` §6) |
| 🆕 `world.bodies` | `scripts/bodies.gd` | `engine.registry`, `world.level` | kolize těles (nesmí se překrývat) a **spojité řazení hloubky** |

### M2 — Těžím a vidím číslo (vidět: ruda v inventáři, číslo dovednosti se pohnulo)

| id | owns | závisí na | proč |
|---|---|---|---|
| 🆕 `data.content.m` | `assets/data/*.json` (+ `synergies.json`) | — | obsah rozsahu `M` (`GDD` §10); **nový obsah = nový záznam** |
| ✏️ `world.nodes` | `scripts/world.gd` (+ markery v `assets/levels/main.json`) | `world.level`, `data.content.m` | uzly surovin, **směs** (běžná + vzácná), respawn, `snapshot()`/`restore()` |
| ✏️ `sim.mining` | `scripts/mining.gd` | `core.skills`, `world.nodes` | výnos podle dovednosti, růst dovednosti, vzácná složka podle délky těžby |
| ✏️ `core.skills.growth` | `scripts/skills.gd` | `data.content.m` | vzorec růstu, 6 dovedností, synergie 20 %, **atrofie za přepínačem** |
| ✏️ `ui.hud.numbers` | `scripts/hud.gd` | `core.skills.growth`, `core.attributes`, `entity.player`, `sim.economy` | čísla na obrazovce (`P2`) |

### M3 — Vyrábím (vidět: u pece ingot, u kovadliny meč, kvalita, opotřebení)

| id | owns | závisí na | proč |
|---|---|---|---|
| ✏️ `entity.item.quality` | `scripts/item.gd` | `data.content.m` | kvalita 0–5, trvanlivost, `repair()` **nesmí předmět zničit** (`TDD` §10 vada 2) |
| ✏️ `sim.crafting` | `scripts/crafting.gd` | `core.skills.growth`, `entity.item.quality` | tavení, kování, kvalita; **jen náklady, které jsou rozhodnuté** (`O-1` je otevřený) |
| 🆕 `data.content.recipes` | `assets/data/recipes.json` | `data.content.m` | 8 receptů (`GDD` §10) |

### M4 — Prodávám a svět reaguje (vidět: stav světa se po dodávce změní)

| id | owns | závisí na | proč |
|---|---|---|---|
| ✏️ `world.state` | `scripts/world.gd` | `world.nodes` | infestace a zásobenost 0–100, tik světa (`GDD` §8.1). **Sekvenčně po `world.nodes` — tentýž soubor, proto závislost** |
| ✏️ `sim.economy.prices` | `scripts/economy.gd` | `world.state`, `entity.item.quality` | cena z stavu světa; **`price()` dnes vrací 0** (`TDD` §10 vada 1) |
| 🆕 `sim.orders` | `scripts/orders.gd` | `sim.economy.prices` | zakázky světa (cíl s číslem, `V7`) |
| ✏️ `entity.npc` | `scripts/npc.gd` | `sim.orders`, `entity.item.quality` | **přepsat zadání** (registr, `extends`, žádné `position` v `Area2D`) |
| ✏️ `ui.hud.state` | `scripts/hud.gd` | `ui.hud.numbers`, `world.state`, `sim.orders` | stav světa a postup zakázky na obrazovce (`V5`, `V7`) |

### M5 — Žiju ve světě (vidět: svět se hýbe beze mě, smrt a respawn)

| id | owns | závisí na | proč |
|---|---|---|---|
| ✏️ `entity.player.death` | `scripts/player.gd` | `entity.move.smooth`, `world.level`, `world.bodies` | smrt, mrtvola, respawn (`REQ-death`) |
| ✏️ `entity.item.use` | `scripts/item.gd` | `entity.item.quality` | **obvaz kliknutím v inventáři** (`TDD` §3.6, `GDD` §9.4) |
| ✏️ `entity.enemy` | `scripts/enemy.gd` | `sim.combat`, `entity.item.quality` | **přepsat zadání** (soubor v repu **není**; 5 pokusů spadlo) |
| 🆕 `sim.standing` | `scripts/standing.gd` | `sim.orders`, `world.state` | **uznání světa** z trojice kritérií (`GDD` §8.2) |
| ✏️ `sim.offline` | `scripts/offline.gd` | `world.state`, `sim.mining`, `sim.crafting` | „svět žije i bez tebe“ + denní strop |
| ✏️ `persist.save.state` | `scripts/save.gd` | `world.nodes`, `entity.player.death` | inventář a stav světa; **`false`, když není co uložit** |

### M6 — Grafika (vidět: postava ukazuje, co má nasazené)

| id | owns | závisí na | proč |
|---|---|---|---|
| 🆕 `render.layers` | `scripts/layers.gd` | `engine.registry`, `entity.move.smooth` | skládání vrstev podle `spec.json` (`vrstvy.slot_poradi`), tonování |
| 🆕 `render.walk` | `scripts/anim.gd` | `render.layers` | přehrávání chůze (8 framů, 4 směry) |
| 🆕 `render.paperdoll` | *(rozhodne `A-1`)* | `render.layers` | náhled postavy — **jen když vrstvená grafika projde** |

### Vyřazené (návrh)

| id | proč |
|---|---|
| 🗑️ `world.map` | **mrtvá** — vlastní tentýž `scripts/world.gd` jako `world.nodes`, práce v `main` není |
| 🗑️ `entity.player.api` | **duplikát** `entity.player` (tentýž soubor, hotová) |
| 🗑️ `tests.harness` | granule nad `tests/` se **nemůže sloučit sama** a `CONVENTIONS.md` §5 zakazuje agentovi testy měnit |

**Počet granulí (naměřeno z tabulek výš):** dnešní roadmapa má **22 id**;
návrh má **38 id** = **19 zachovaných** (z toho 12 přepsaných řezů, které si
drží své id) + **19 nových** (řezů téhož souboru v dalším milníku nebo nových
souborů) − **3 vyřazené**.
**Není to odhad rozsahu `M`** (`GDD` §12.5 říká „+20–30 granulí“) — ten se
naplní, až se milníky `M2`–`M5` doplní o obsah (materiály, recepty, nestvůry,
zakázky), kde počet granulí ještě poroste.

**Co zůstává bez práce (a je to správně):** `core.attributes`, `world.level`,
`sim.combat`, `sim.assist` a `data.content` jsou hotové a v MVP se jich
**nikdo nedotkne** — nové řezy (`core.skills.growth`, `sim.economy.prices`, …)
je jen **používají**. `sim.assist` je navíc **non-goal `N9`** pro MVP.

---

## 4. Co je v návrhu strojově (a co ne)

**`_analyza/roadmap-navrh.json` obsahuje jen to, co je po odsouhlasení hned
k vydání: `M0` a `M1`** (5 granulí) — **s hotovými `prompt`y**.

**Proč ne všechny:** `prompt` se má **generovat ze smlouvy** (`docs/TDD.md` §3)
v momentě, kdy se milník otevírá. Ručně psaných 22 próz je přesně to, co dnes
u `npc`/`enemy` selhalo napořád (nízká kvalita zadání = 58 běhů, 0 úspěchů).
Napsat dnes 26 promptů by znamenalo **vyrobit víc slepých zadání**, ne víc práce.

**Co to znamená pro orchestraci:** po výměně roadmapy má conductor **5 granulí
k vydání** a po každém dokončeném milníku se doplní další. To je záměr:
**plán se doplňuje z uzavřeného milníku, ne dopředu naslepo.**

---

## 5. Co musí proběhnout PŘED výměnou roadmapy (návrh, ne hotová věc)

Tohle nejsou granule — je to **úklid, který by jinak plán zdědil**:

1. **Srovnat `done` se skutečností v gitu.** Audit naměřil, že **4 granule mají
   práci v `main` a `done` nemají** (mj. `persist.save.state`, jehož práce
   v `save.gd` **skutečně je** — inventář i stav světa tam jsou). Postup:
   u každé ověřit `git merge-base --is-ancestor <commit PR> HEAD` a zapsat
   `done: true` + `done_note`. *(Nález auditu; **v tomhle návrhu neověřeno** —
   ověření je první krok po odsouhlasení.)*
2. **Vyřadit tři granule** z §3 („Vyřazené“) — jinak zůstanou v DAG jako zombie.
3. **Doplnit `provides`/`consumes`** z `docs/TDD.md` §3 do každé granule, aby
   agent dostal smlouvu, ne jen jméno souboru.
4. **`size_lines` jako číslo**, ne string (`"<= 100"` → `100`) — konzument
   (brána auto-merge) z toho jinak musí parsovat text.

---

## 6. Co čeká na tebe (rozhodnutí, ne práce)

| # | Otázka | Doporučení |
|---|---|---|
| **R-1** | **Odsouhlasit návrh jako celek?** (26 granulí, 3 vyřazené, `M0`+`M1` k vydání) | ano — jinak orchestra nemá co vydávat a `engine.shell` zůstane blokovaná |
| **R-2** | **Vyřadit `tests.harness`?** (testy by pak měnil jen člověk) | ano — agent, který vlastní testy, ztrácí páku, která hlídá jeho práci |
| **R-3** | **Smí `engine.shell` přeskočit komponenty, které v repu nejsou?** (aditivní migrace) | ano — jinak čeká na `npc`/`enemy`, které nikdy neprošly |
| **R-4** | **Doplnit `M2`–`M6` prompty až při otevření milníku?** (ne dopředu) | ano — viz §4 |
| **R-5** | **Vyměnit roadmapu teď, nebo až po zeleném `Forge agent`?** | viz `HANDOFF.md`: `Forge agent` je **červený** (20 selhání v řadě) a **roadmapa conductora je prázdná** — výměna má smysl, až orchestra umí vydat granuli |
