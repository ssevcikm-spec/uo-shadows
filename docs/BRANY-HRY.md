# Brány hry `uo-shadows` — co měří a kde mají slepá místa

**Co tenhle dokument JE:** **projektová znalost HRY** o jejích branách
(`.forge/*`) — co která měří, kde má **naměřené** slepé místo a co se u ní
změřilo. Nejsou to pravidla orchestry (ta jsou v orchestra) ani stav hry.

**Odkud brát dnešní stav:** kód v `.forge/`, běhy `ci.yml`, roadmapa
`.forge/roadmap.json` a `AGENTS.md` hry (shrnutí + pravidla). Tenhle dokument
je **znalost a naměřené případy** — čísla jsou **stav v čase měření**.

> **⚠ ODKUD SE SEM PŘESUNUL (7. 10. 2026):** tenhle obsah byl do té doby
> v **skillu `orchestra`** (oddíl „Assety a „oči" orchestra", ~11,6 kB). Skill
> se ale načítá **v každé session, kde je potřeba orchestra** — tedy i v session
> o obrázcích nebo o jiné hře, kde je celý zbytečný. Znalost o **branách hry**
> patří projektu hry; ve skillu zůstal **odkaz**.
>
> **Doklad, že přesun nebyl zkrácení:** měřeno plošným skenem 6. 10. 2026 —
> z devíti vzorů o branách hry jich měl **skill 8** a `AGENTS.md` hry **2**.
> Kdyby se text jen „zkrátil" podle auditu, znalost by **zanikla** a hra by
> ji neměla čím nahradit. Proto se **přesouvá** a přesměrovala se i brána
> (`tools/over-dokumentaci.py` v orchestra), která ty texty vyžaduje.

---

## Assety a „oči" hry

Orchestra umí ověřit, že něco **funguje** (testy, wiring, běh). Neuměla ověřit,
že to **vypadá dobře** — a to je jiná vrstva. Dvě komponenty, které na to jsou:

| Komponenta | Kde | Co dělá |
|---|---|---|
| `.forge/check-schema.py` | repo hry | **kontroluje, že si hra neodporuje ve vizuálním schématu** — deklarace (`spec.json`), mapy (`levels/*.json`), vykreslování (`level.gd`), dlaždice (`tiles/`) a druhá logika (`world.gd`) musí říkat totéž číslo. **Tvrdá brána v CI, běží PŘED vision** |
| `.forge/check-assets.py` | repo hry | **měří** sprity proti `assets/spec.json`: výška vs. spec, neprůhledný okraj, díry v siluetě, počet barev, poměry mezi rolemi (mince/chest/player), shoda siluet mezi framy chůze; hudbu z manifestu (kroky/skoky/motiv/smyčka) |
| `.forge/vision.mjs` | repo hry | **vidí** — pošle obrázek modelu s viděním a vrátí text/JSON. Režimy `presence` (obsah proti očekávání z mapy) a `diff` (dva obrázky). Klíč z GitHub Secrets, **`exit 1` běh nezhodí** (v CI se používá s `\|\| echo`) |
| `.forge/vision-profile.json` | repo hry | **chování kontroly pro danou hru** — očekávaný obsah, zákazy v promptu, řetěz poskytovatelů, stropy. **Záměrně v něm NENÍ schéma** (dlaždice, projekce) — to je per-game ve `spec.json` |
| `.forge/baseline.py` | repo hry | **co je vizuálně SCHVÁLENÉ (LGTM) a co se změnilo** — `stav` / `init` / `schval` / `zamitni` / `kontrola`. Drží `.forge/vision/baseline.json`, `verdicts.jsonl` a `rejected.jsonl`. **Cache pro vision: schválený a nezměněný obrázek se modelu vůbec neposílá** (doloženo testem: 0 volání) |
| `.forge/node/vision.test.mjs` | repo hry | **offline testy vision** proti mock API — bez sítě a bez klíčů. Ověřuje i to, že se schéma čte ze `spec.json` a že cache opravdu brání volání modelu. **POZOR: existují DVĚ různé verze téhož jména** (naměřeno spuštěním 1. 10. 2026): v **šabloně** `repo\.forge\node\` → **36/36** (17 576 B), ve **hře** → **28/28** (13 318 B). Hra je **starší**, chybí jí 8 testů (mj. na `popis_stylu`). **Kód `vision.mjs` je přitom v obou kopiích shodný** (shodný SHA256) — rozešly se jen TESTY, a `kontrola-driftu.mjs` ten soubor nehlídá. Třetí, rozbitá kopie je v rootu workspace (`5 OK / 23 chyb`, kandidát na smazání) |

> **Dvě mezery `phash`, které se našly měřením** (a obě jsou zavřené, viz
> `baseline.py`) — bez nich by **změněný asset prošel jako nezměněný**:
>
> | Mezera | Naměřeno | Řešení |
> |---|---|---|
> | phash je **slepý na barvu** (DCT přes odstupy) | červená i modrá se stejnými bloky → stejný hash `f8f8f8f0f0070707` | ukládá se i **barevný podpis**; cache chce shodu obojího |
> | phash **degeneruje u jednolitého** obrázku | plná červená i plná modrá → `8000000000000000` | `phash()` vrátí `None` → porovnává se **přesný `sha256`** |
>
> Poučení: **hash není důkaz, že se nic nezměnilo** — je to jen nástroj, jehož
> meze se musí změřit. Tichá chyba „nezměněno" u změněného assetu je horší než
> žádná cache.

> **Tvrdá brána vs. poradní kontrola — důležité rozdělení:**
> `check-schema.py` **blokuje** (rozpor v zadání je objektivní fakt),
> `vision.mjs` **neblokuje** (názor modelu má chybovost a falešný poplach je
> dražší než přehlédnutí). Když vision spadne na kvótu, běh musí pokračovat.

**Pořadí v CI je dané a testuje se** (`tools\test-ci-workflow.mjs` v orchestra):
import assetů → **kontrola schématu** → testy → assety → wiring → smoke →
snímek hry → **vision**. Vision čte snímek, takže musí být po jeho vyrobení;
a kontrola schématu musí být před vision, protože vision potřebuje vědět,
**proti čemu měří**.

**Proč jsou potřeba obě:** brána naměřila „mince 30 px vs truhla 45 px"
a „v truhle prosvítá pozadí dírou uvnitř siluety" — ale **nepozná**, jestli je na
spritu to, co má být. Naměřeno 30. 9. 2026 na `uo-shadows`: `check-assets.py`
hlásí „Vše v pořádku: assety odpovídají specu" (player 38×95 px, 1103 barev,
0 děr), a přesto o obsahu neříká nic.

## Kde jsou slepá místa brány (změřeno, ne odhad)

- **Animace se neměří.** `check-assets.py` hledá `assets/sprites/walk_*.png`,
  jenže chůze je rozložená po vrstvách v `tools/blender/sprites/body_d0_f*.png`
  → v `assets/sprites` je **0** souborů `walk_*`. Brána to poctivě ohlásí jako
  poznámku („animace chůze v projektu není – přeskočeno"), takže nic
  nepředstírá, ale kontrola `min_silhouette_iou: 0.80` ze specu se **nikdy
  neuplatní**, i když spec deklaruje `framy: 8`. Ruční měření: IoU 0.834–0.908,
  posun těžiště 0.46–0.99 px (limit 3.0) → animace je v pořádku, jde o slepé
  místo, ne o vadu.
- **Hudba se neměří**, dokud není `assets/audio/music/manifest.json` (u
  `uo-shadows` není).
- **`kind` nic neřídí.** `inputs.kind` je v `agent.yml` jen v šabloně PR
  komentáře; všechny granule roadmapy mají `"kind": "code"`.
- **`check-wiring.py` na jiném enginu hlásí zelenou nad NULOU souborů.**
  `check-wiring.py:73` čte jen `scripts/*.gd`; když tam žádné `.gd` nejsou,
  vrátí prázdné `vady` a `main` vytiskne *„Vše v pořádku: každá funkce je
  odněkud volaná."* s **exit 0** (`:169`). Je to nejnebezpečnější brána
  orchestra, protože **nespadne a neohlásí se** — jen přestane měřit.
  (Pro Godot je v pořádku: naměřeno 57 funkcí v 7 souborech.)
- **Kontrola zapojení čte i testy.** `check-wiring.py:83-89` hledá použití
  funkce v **celém repu** včetně `tests/`, a `tests/run_tests.gd`
  má **26 řádků s `has_method`** (**39 výskytů** — naměřeno 7. 10. 2026
  hledáním v souboru; dřív tu stálo „27 podmíněných kontrol", což bylo
  **nepravdivé číslo na dvou místech** — tady a v `AGENTS.md` hry).
  Funkce zmíněná jen v testu se tedy počítá jako „použitá", i když ji hra
  nikdy nezavolá. **To je přesně past z `game-developer` skillu** („podmíněný
  test je tiše zelený").
- **`check-assets.py`, `check-wiring.py` a `verify-level-render.py` nemají
  žádný offline test** (na rozdíl od `check-schema.py`, `vision.mjs`,
  `baseline.py` a `check-licence.py`). Brána bez testu se nedá poznat jako
  nefunkční — proto zůstává nefunkční (tři slepá místa výš jsou toho důkaz).

**Pravidlo:** „brána nic nehlásí" může znamenat „brána se na to nedívá".
Než se spolehneš na zelenou, ověř, že kontrola **skutečně proběhla**.

## Naměřeno 1. 10. 2026: tvrdá brána schématu TIŠE PŘESTALA MĚŘIT

Šlo o kontrolu výchozí buňky v `scripts/level.gd`:

| | |
|---|---|
| Co kontrola hledala | `var cell := 16` (tvar před migrací na izometrii) |
| Co je v kódu po migraci | `const CELL_W_DEFAULT := 96` + `CELL_H_DEFAULT := 48` |
| Co to udělalo | regexy nenašly nic → cyklus proběhl nad **prázdným seznamem** → **zelená** |
| Jak to bylo vidět | jen v řádku `level.gd: výchozí cell=[], fallback=[]` — `[]` vypadá jako naměřená nula |

**Oprava:** kontrola měří oba tvary, hlásí **vadu**, když výchozí buňku
přečíst nelze („kontrola NEPROBĚHLA" není totéž jako „je to v pořádku"),
a rozlišuje šířku od výšky (u izometrie 96×48 se liší). Navíc pojmenovává
**mrtvé větve**: `world.gd` se při migraci smazal, takže kontroly, které na
něj sahají, se už nikdy nespustí — to se musí hlásit, ne mlčet.

**Pojistka proti regresi:** `tools\test-check-schema.py` v orchestra
(17 offline testů se známým správným i chybným repem, spouští ho
`validate-all.mjs`). Při psaní **odhalil čtyři chyby ve vlastním regexu**
(case sensitivity, záměna os, první vs. poslední deklarace, `\b` po
podtržítku) a jednu skutečnou: **šablona `repo/` a herní repo se rozešly**.
Proto test hlídá i to, že obě kopie mají shodný hash.

**Zapsáno v:** `.forge/check-schema.py` (šablona i hra) — **staví na tom,
že se to musí commitnout do hry**; dokud je oprava jen v pracovním stromu,
CI ji nevidí.

> **POZOR: v orchestra byly DVĚ kopie téhle brány a NEJSOU stejné**
> (naměřeno 1. 10. 2026). Nenech se zmást jménem:
>
> | soubor | řádků | co to je |
> |---|---|---|
> | `.forge\check-schema.py` v repu orchestry (`repo/.forge/`, **šablona**) **i** tady (`.forge/`) | **461** | **opravená verze** — měří oba tvary deklarace, hlásí „kontrola NEPROBĚHLA", pojmenovává mrtvé větve. **Tuhle pouští CI** |
> | ~~`tools\kontrola-schematu.py`~~ (v orchestra) | 305 | **stará, slepá verze** — ⚠ **6. 10. 2026 už NEEXISTUJE** (`Test-Path` = False v orchestra i ve hře), takže slepá větev je pryč. Kdo ji hledá podle starého textu, nenajde ji |
>
> Obě `.forge/` kopie mají shodný hash se svým protějškem, takže „drift" nic
> neodhalí — jsou to **dvě různé cesty k témuž nástroji**.
> Když budeš bránu ověřovat, **použij tu v `.forge/`**.

## Kde je slepé místo mezi „vidím sám" a „vidí model"

Agent v GitHub Actions **nemá nativní vision** — proto existuje
`.forge/vision.mjs`. Naopak `read_image` (kterým se agent v DSH podívá sám,
zdarma) **v CI runneru k dispozici není**. Nepleť si ty dvě věci: lokálně vidím
sám, v cloudu vidí jen Gemini.

**LGTM cache (`baseline.py`) je LOKÁLNÍ optimalizace — v CI neplatí nikdy.**
Naměřeno 1. 10. 2026: `baseline.py:252` vyžaduje, aby byl obrázek **uvnitř
repu hry**, ale CI píše snímek do `/tmp/frames` (`ci.yml:109`). Ověřeno:
snímek mimo repo → `{"v_cache": false, "duvod": "mimo repo hry"}`; schválený
asset v repu → `{"v_cache": true}`. **Důsledek:** v CI se vision ptá modelu
**vždy** (a to je správně); nenech se uklidnit tím, že je něco „v baseline".
Schválených 272 položek v `uo-shadows` jsou **sprity** (16 z `assets/sprites`
+ 256 z `tools/blender/sprites`), ne snímky hry.

## 3D → 2D sprity (a kde se to smí renderovat)

**Blender v orchestra není a být nemůže** — `ubuntu-latest` ho nemá a instalace
je drahá. 3D → 2D render tedy musí běžet **na domácím uzlu** (`pc-domaci`,
`FORGE_KINDS=assets,test,build`) nebo se sprity commitovat hotové. Hotová
pipeline k tomu leží **tady v repu hry**: `tools\blender\`
(`build_character.py` + `postprocess.py`, 258 spritů).

⚠ **A pozor na orchestra stranu téhož:** `worker.mjs` zná kroky jen `shell`,
`godot-import`, `godot-test`, `godot-export`, `python`, `make-dir` —
**`blender:` mezi nimi není**, skládá se přes `shell:` (a ten se vždy ptá y/N).
Podrobně (i s mrtvým defaultem `FORGE_CMD` a absencí testu logiky uzlu) je to
v **`E:\Workspaces\forge-orchestra\PROVOZ-ORCHESTRA.md`** — tam to patří,
protože to je znalost orchestry, ne hry.

## Dvě kopie souborů: šablona vs. hra

`check-schema.py`, `check-wiring.py` a `vision.mjs` existují **ve DVOU
kopiích** — v **šabloně** (`E:\Workspaces\forge-orchestra\repo\.forge\`) a
**tady**. Drift hlídá `node E:\Workspaces\forge-orchestra\tools\kontrola-driftu.mjs`.
**Nikdy neměň jen jednu kopii** — a pozor: **`vision.test.mjs` se mezi kopiemi
ROZEŠEL** (šablona 36/36, hra 28/28) a drift test ten soubor **nehlídá**.

## Kam pro co

| Co | Kde |
|---|---|
| shrnutí bran a pravidla hry | `AGENTS.md` (tady) |
| **tento dokument** | `docs/BRANY-HRY.md` |
| orchestra (kdo hru vyvíjí) | `E:\Workspaces\forge-orchestra`, provoz a invarianty v `PROVOZ-ORCHESTRA.md` |
| metodika granulí (DAG) | skill `game-developer` |
