# PLÁN VÝVOJE — `uo-shadows` (reset k 15. 10. 2026)

> **Co tenhle dokument JE:** **plán** — jak se hra staví po milnících a co je
> k vydání orchestře. **Není to zdroj pravdy o designu** (to je `docs/GDD.md`)
> **ani o technice** (`docs/TDD.md`); strojový plán je `.forge/roadmap.json`.
> **Odkud brát stav:** `.forge/roadmap.json` (co je hotové a co k vydání),
> `ZASTAVENO.md` (proč se nevyvíjelo) a orchestra (`/health`, `/roadmap`).
> **Vzniklo:** 15. 10. 2026 · **Vlastník:** session, která mění plán.
> **Jak se mění:** přepisuje se celý (je to stav); historie plánu se archivuje,
> nemaže (`_analyza/PRACE-2026-10-15/ROADMAPA-STARA-2026-10-15.json`).

---

## 1. Co reset znamená a co ne

**Zadání (uživatel, 15. 10. 2026):** „Podle tvé změny resetuj kompletní vývoj
hry a granule. Připrav plán podle designu a pustíme na to orchestru."

| Co se resetovalo | Co se NEresetovalo |
|---|---|
| **`done` u granulí** — 16 příznaků `true` nahradilo **měření** (soubor v `main` **A** volá ho produkční cesta) | **Kód v `main`** — 1 716 řádků zůstává; nic se nemazalo |
| **Složení plánu** — 21 granulí → **10** (5 hotových, 5 k vydání) | **Historie** — stará roadmapa je archivovaná jako soubor |
| **Zadání granulí** — znovu podle smluv v `docs/TDD.md` §3 a s rozpočtem | **Dokumenty** — `GDD`/`TDD`/`ADD`/`BRANY-HRY` zůstávají, jak byly přepsané |
| **Pořadí podle milníků** — každá granule má nově `milestone` | **`assets/data/*.json`** — obsah hry se nemazal |

**Naměřený důvod resetu** (`_analyza/PRACE-2026-10-15/zmer-produkci.py`, `HEAD 7434cd4`):

```
běžící hra instancuje JEN:  scripts/game.gd (kostra) → scripts/level.gd, scripts/player.gd
mimo produkční cestu:       13 souborů
```

Dřívější podoba plánu ale hlásila hotovost u **16** položek (stav 8. 10. 2026 — **ve
svém čase správné číslo**; dnes je hotových **5** z deseti, protože se `done`
měří). To není kosmetika: `done` je to,
podle čeho conductor granuli **přeskočí** — a podle čeho si člověk myslí, že je
hotovo. Tři z těch granulí (`sim.mining`, `sim.crafting`, `sim.combat`) navíc
visely na jedné granulované funkci.

## 2. Milníky a co je v nich (stav 15. 10. 2026)

Milníky jsou z `docs/GDD.md` §12 a každý je **hratelný stav, ne vrstva kódu**.
`milestone` v granulích je od 15. 10. 2026 — bez něj se „plán podle milníků"
nedal měřit.

| Milník | Co je na konci vidět | Stav plánu |
|---|---|---|
| **M0** — Kostra | hra se spustí a nezhroutí se; komponenty existují přes registr | **5 granulí**: `engine.registry` ✅ (postaven ručně), `engine.shell` ✅ (zapojení registru), `persist.save` ✅ (knihovna), **k vydání:** `shell.coins`, `sim.wire` |
| **M1** — Hýbu se | postava jde plynule za kurzorem, objekty se nepřekrývají | **5 granulí**: `world.level` ✅, `entity.player` ✅, **k vydání:** `engine.input`, `entity.move.smooth`, `world.bodies` |
| **M2** — Těžím a vidím číslo | ruda v inventáři, číslo dovednosti se pohnulo | **zásoba** (viz §4) |
| **M3** — Vyrábím | u pece ingot, u kovadliny meč, kvalita, opotřebení | **zásoba** |
| **M4** — Prodávám a svět reaguje | stav světa se po dodávce změní | **zásoba** |
| **M5** — Žiju ve světě | svět se hýbe beze mě, smrt a respawn | **zásoba** |
| **M6** — Grafika | postava ukazuje, co má nasazené | **zásoba** |

**K vydání hned (5):** `shell.coins`, `sim.wire`, `engine.input`, `entity.move.smooth`,
`world.bodies`. Dvě z nich (`sim.wire`, `entity.move.smooth`) **čekají na předka**
— conductor je vydá sám, až předchůdce dobehne; to **není vada plánu**.

## 3. Proč je hotové právě tohle (měřená definice)

`docs/GDD.md` §12 definuje hotovo **čtyřmi** podmínkami:

```
hotovo JE:  soubor je v main
            A brána jeho funkci SKUTEČNĚ zavolala
            A přijímací kritérium proběhlo s KONKRÉTNÍ hodnotou
            A funkci volá PRODUKČNÍ kód (ne jen test)
```

**Naměřeno 15. 10. 2026** (`zmer-produkci.py`, `HEAD 7434cd4`):

| Skupina | Co do ní patří | Důkaz |
|---|---|---|
| **V produkční cestě** (3) | `game.gd` (kostra), `level.gd`, `player.gd` | `game.gd:155` a `:270` je instancují přes `load()` |
| **Knihovna, kterou produkce nevolá** (13) | `registry.gd`, `save.gd`, `hud.gd`, `economy.gd`, `skills.gd`, `item.gd`, `attributes.gd`, `world.gd`, `mining.gd`, `crafting.gd`, `combat.gd`, `offline.gd`, `assist.gd` | nikdo je z produkce neinstancuje |

Proto je `engine.shell` hotový **jen jako zapojení registru do dnešní scény** —
a teprve `shell.coins` a `sim.wire` přesouvají logiku z monolitu do komponent.
Kdo si přečte jen `done: true`, tomu to unikne; proto je to i v `done_note`.

## 4. Zásoba: co se doplní, až se milník otevře

**Procedura (závazná):** milník se otevírá, když je **předchozí milník vidět na
obrazovce**. Tehdy se z jeho granulí vygenerují **prompty ze smluv**
(`docs/TDD.md` §3) a doplní se do `.forge/roadmap.json`.

| Milník | Připravené granule (id → soubor) | Zdroj smluv |
|---|---|---|
| **M2** | `data.content.m` → `assets/data/*.json` · `world.nodes` → `scripts/world.gd` · `sim.mining` → `scripts/mining.gd` · `core.skills.growth` → `scripts/skills.gd` · `ui.hud.numbers` → `scripts/hud.gd` | `TDD` §3.5, §3.10, §3.2, §3.17 |
| **M3** | `entity.item.quality` · `sim.crafting` · `data.content.recipes` | `TDD` §3.6, §3.11 |
| **M4** | `world.state` · `sim.economy.prices` · `sim.orders` · `entity.npc` · `ui.hud.state` | `TDD` §3.5, §3.9, §3.8 |
| **M5** | `entity.player.death` · `entity.item.use` · `entity.enemy` · `sim.standing` · `sim.offline` | `TDD` §3.4, §3.6, §3.9, §3.14 |
| **M6** | `render.layers` · `render.walk` · `render.paperdoll` (rozhodne `A-1`) | `TDD` §4, `ADD` §4 |

**Proč ne dopředu:** u `entity.npc` a `entity.enemy` měly prompty nejkratší
zadání ze všech a **58 běhů, 0 úspěchů** — protože nebyly ze smlouvy. Dopsat
dnes 26 próz by vyrobilo víc slepých zadání, ne víc práce.

**Vyřazené (zůstávají vyřazené):** `world.map` (mrtvá, duplikovala soubor),
`entity.player.api` (duplikát `entity.player`), `tests.harness` (granule nad
`tests/` se nemůže sloučit sama a `CONVENTIONS.md` §5 zakazuje agentovi měnit testy).

## 5. Ověření před vydáním (a co je naměřeno)

```powershell
$env:PYTHONIOENCODING='utf-8'; cd E:\Workspaces\uo-shadows
python .forge\zkontroluj-plan.py            # plán: JSON, závislosti, owns, rozpočet zadání
python _analyza\over-dokumenty.py --root .  # dokumenty proti zdrojům i sobě
python .forge\check-schema.py .             # tvrdá brána
```

**Naměřeno 15. 10. 2026:** `zkontroluj-plan.py` → `VÝSLEDEK: 0`, 10 granulí,
**5 připravených**; zadání mají **220–353 tokenů** (strop 400) — proti návrhu
z 8. 10. (434–556 t), který se do stropu nevešel.

⚠ **Zadání nemá obsahovat cestu k souboru.** Nástroj si podle cesty přitáhne celý
dokument (naměřeno +8 000 tokenů na request); smlouva patří **do zadání**, ne
odkazem. Validátor to hlásí jako poznámku u každé granule.

## 6. Spuštění orchestry — co proběhlo 15. 10. 2026

| # | Krok | Stav |
|---|---|---|
| 1 | Nový plán: **10 granulí** v `.forge/roadmap.json` (5 hotových, 5 k vydání) + validátor | ✅ hotovo |
| 2 | Archiv starého plánu — celý předešlý plán je v `_analyza/PRACE-2026-10-15/ROADMAPA-STARA-2026-10-15.json` (oddíl „2. Milníky a co je v nich" výš uvádí, kolik položek měl) | ✅ hotovo |
| 3 | **Push do `origin/main`** — orchestra čte roadmapu z GitHubu, ne z disku | ✅ `ca7fa4a`, k odeslání 0 |
| 4 | **Reset cache** — jinak se conductor drží starých id | ✅ `POST /roadmap/reset` cache vyčistil a fronta se postavila znovu (5 hotových, 5 `queued`) |
| 5 | **Aktivace hry** — `node tools\aktivuj-hru.mjs --hra uo-shadows` | ✅ `active=1` |
| 6 | Vypnutí `coin-picker` — dvě aktivní hry = rozdělená pozornost a kvóta | ✅ `active=0` (granule zůstávají v cache pro návrat) |

### 6.1 První vlna (naměřeno, ne odhad)

Conductor vydal **3 granule paralelně** (`shell.coins` #519, `engine.input` #520,
`world.bodies` #521) a **všechny tři selhaly**. Důvody jsou různé a oba jsou
opravitelné — a oba se opravily **hned**:

| Běh | Granule | Model | Co se stalo | Oprava |
|---|---|---|---|---|
| #519 | `shell.coins` | cerebras → mistral | **agent nic nezměnil** (`# cerebras … běh skončil jako „agent nic nezměnil"`) | fallback na dalšího poskytovatele je součást řetězce; zadání zůstává |
| #520 | `engine.input` | mistral | `Parse Error: Cannot infer the type …` | do zadání i do `CONVENTIONS.md` §1 doplněna pravidla (viz níž) |
| #521 | `world.bodies` | mistral | `Parse Error: Cannot infer the type of "bunka"…` a `Could not find type "Level"` | totéž |

**Co se z toho zjistilo (a je to poučení, ne stížnost):** zadání sice mělo smlouvu
a rozpočet, ale **nemělo dvě pasti parsování**, na které v GDScriptu narazí každý
model: (1) `:=` u hodnoty bez typu (např. `Vector2.ZERO`, klíč z `Dictionary`)
a (2) **typ z cizího skriptu v anotaci** — `Level`, `Player`, `Registry` jsou jen
**jména uzlů**, soubory nemají `class_name`, takže `var lvl: Level` neparsuje.
Dopsáno do `CONVENTIONS.md` §1 (doplněk „DOPLNĚNO 15. 10. 2026") a do zadání
`world.bodies` a `engine.input`. **Kdo píše další zadání, ať ty dvě věty kopíruje.**

**Proč druhá vlna neběží hned:** `RETRY_HOURS` = **3 h** — selhaná granule se vrací
do fronty až po cooldownu (guard se ptá na **čas**, ne na stav, takže fronta může
hlásit `queued` a dispatch přesto čeká). Je to **záměr orchestry**: free modely
mají denní limity a okamžitý retry jen pálí pokusy. Další pokus tedy přijde sám
kolem **16:13**; `sim.wire` navíc čeká na `shell.coins`.

**Stav orchestry po prvním kole:** `/health` → `main_ci = success` (na commitu
`ca7fa4a`), `ready` 0–3, `/failed` prázdné, PR zatím žádné.

## 7. Co musí proběhnout před DALŠÍ vlnou

**Poznámka k pořadí:** úklid cache je v orchestraci **operace**, ne editace
souboru — conductor si drží vlastní tabulku a stará id v ní zůstávají, dokud se
neresetují (naměřeno 9. 10.: v souboru 21 granulí, v cache 25 řádků → 5 osiřelých,
mezi nimi úloha ve stavu `ready`). A **`uo-shadows` je dnes `active: 0`** —
registr her ji vede, ale práce se jí nevydává.

## 8. Co v tomhle plánu ZÁMĚRNĚ NENÍ

- **Termíny ani odhady hodin** — „hotovo" se u téhle hry měří, ne plánuje.
- **Granule pro `M2`–`M6`** — jsou v §4 jako zásoba; doplní se při otevření
  milníku (jinak vzniknou slepá zadání).
- **Rozhodnutí o `spec.json`** — jeho vnitřní rozpory jsou zapsané
  (`docs/ADD.md` §11), ale `spec.json` je deklarace, ne dokument; mění ho
  rozhodnutí uživatele.
- **Oprava vad běhu** — `game.gd:181` a `economy.price()` jsou zapsané
  (`docs/TDD.md` §10), neopravují se mimochodem.
