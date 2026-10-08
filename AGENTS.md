# Pravidla pro agenty v tomto workspace (hra UO-Shadows)

> **Co tenhle soubor JE:** **trvalá pravidla HRY** — design, smlouvy a brány
> konkrétně pro `uo-shadows`. Platí napříč session.
>
> **⚠ VZNIKL 4. 10. 2026 při přesunu na `E:`.** Do té doby hra **žádná**
> `AGENTS.md` neměla: projektový root se hledá podle `.git`, takže session
> otevřená v herním repu dostala jen **obecná pravidla stanice**
> (`DSH_HOME\AGENTS.md`) a **žádná projektová** (naměřeno před přesunem:
> `.git` **True**, `AGENTS.md` **False**).
>
> **⚠ PRAVIDLA ORCHESTRY TU NEJSOU.** Orchestra je **jiný repozitář a jiný
> workspace**: `E:\Workspaces\forge-orchestra` (sourozenec tohoto repa).
> Její pravidla platí **pro ni**, ne pro hru. Kdo je hledá tady, nenajde je.
>
> **Obecná pravidla stanice** (prostředí, ověřování, dokumentace, jazyk) jsou
> v `DSH_HOME\AGENTS.md` a načtou se samy. **Pasti prostředí** jsou ve skillu
> `dsh-prostredi`, metody ověřování ve `overovani`.

**Ověřeno měřením.** Každé pravidlo níž vzniklo z konkrétní chyby, která něco
stála. Když si nejsi jistý, jdi po důkazu — ne po znění.

---

## Kde co je

| Co | Kde |
|---|---|
| **tento repozitář** (hra) | `E:\Workspaces\uo-shadows` |
| **orchestra** (vyvíjí tuhle hru) | `E:\Workspaces\forge-orchestra` — **sourozenec**, ne nadřazená složka |
| **Godot** | `E:\Tools\godot\Godot_v4.7.2-stable_win64_console.exe` — obecný nástroj stanice, **ne** součást žádného repa |
| **koren stanice** | `C:\Users\Ssevc\Local-Deepseek` — dokumenty, které zůstaly stanici |

**⚠ Vazba hra → orchestra je jen jedna a je nepovinná:** `hra.cmd` umí vzít
Godot z `FORGE_GODOT`; když proměnná není nastavená, sáhne na
`E:\Tools\godot\...` (funkční fallback). **Hra NEMÁ `.forge\node\.env`**
(gitignorované) a `hra.cmd` ho **nečte** — kdyby fallback neexistoval,
v čerstvém klonu by launcher skončil „Godot nenalezen". Naměřeno 4. 10. 2026.

## Jak spustit hru a testy

```powershell
# hra (okno)
.\hra.cmd

# headless testy (Godot; výsledek se čte z „[test] N kontrol, M selhání")
$godot = 'E:\Tools\godot\Godot_v4.7.2-stable_win64_console.exe'
& $godot --headless --path . --script res://tests/run_tests.gd
```

> **⚠ `--user-data-dir` tenhle build IGNORUJE** — `user://` míří do
> `%APPDATA%\Godot\...`. V sandboxu to znamená zápis mimo workspace, a nástroj
> **nespadne** (jen tiše neuloží). Když něco „se neuložilo", první otázka je
> **kam** se to mělo uložit. Detail: skill `dsh-prostredi`.

> **⚠ Godot testy mohou vypsat `[test] N kontrol, 0 selhání` a PŘESTO skončit
> nenulově** (úklidové volání s GDScript backtrace). **Čti výsledek testů**, ne
> jen exit kód — a naopak: samotný výstup testů bez exit kódu taky nestačí.

## Brány hry (a co u nich neplatí)

Brány žijí v `.forge/` a pouští je `ci.yml`. **Tvrdá brána** je jen
`check-schema.py` — ostatní jsou poradní nebo mají známá slepá místa:

| Brána | Co dělá | ⚠ Slepé místo (naměřené) |
|---|---|---|
| `.forge/check-schema.py` | **tvrdá** — deklarace (`assets/spec.json`), mapy, vykreslování a dlaždice musí říkat totéž číslo | — |
| `.forge/check-assets.py` | měří sprity proti specu (výška, okraj, díry v siluetě, barvy) | **animace se neměří** — chůze je rozložená po vrstvách v `tools/blender/sprites/`, v `assets/sprites` nejsou `walk_*`; kontrola to poctivě ohlásí jako poznámku, ale limit IoU se **nikdy neuplatní** |
| `.forge/check-wiring.py` | hledá, že každá funkce je odněkud volaná | **na jiném enginu hlásí zelenou nad NULOU souborů**; navíc čte i `tests/`, takže funkce zmíněná jen v testu se počítá jako použitá |
| `.forge/vision.mjs` | **vidí** (režimy `presence`/`diff`), klíč z GitHub Secrets | **neblokuje** — `exit 1` běh nezhodí (v CI `\|\| echo`). Názor modelu má chybovost; falešný poplach je dražší než přehlédnutí |
| `.forge/baseline.py` | co je vizuálně schválené (LGTM) a co se změnilo | **LGTM cache je lokální optimalizace — v CI neplatí nikdy** (`baseline.py:252` chce obrázek uvnitř repa, CI píše do `/tmp/frames`) |

> **⚠ `.gitattributes` a dva soubory téhož jména:** `check-schema.py`,
> `check-wiring.py` a `vision.mjs` existují **ve DVOU kopiích** — v **šabloně**
> (`forge-orchestra/repo/.forge/`) a **tady**. Drift hlídá
> `node <orchestra>\tools\kontrola-driftu.mjs`. **Nikdy neměň jen jednu kopii** —
> a pozor: **`vision.test.mjs` se mezi kopiemi ROZEŠEL** (šablona 36/36,
> hra 28/28) a drift test ten soubor **nehlídá**.

> **⚠ Podmíněný test je tiše zelený.** `tests/run_tests.gd` má **28 řádků
> s `has_method`** (**41 výskytů** — **přeměřeno 8. 10. 2026**; „26 / 39"
> naměřené 7. 10. 2026 bylo ve svém čase správné, „27 podmíněných kontrol"
> před tím bylo nepravdivé) — funkce, která **není**, se **přeskočí**
> a test projde. Test musí kód **ZAVOLAT** a ověřit výsledek.
> **Počet kontrol se čte z BĚHU** (`[test] N kontrol`), ne ze vzorů v souboru:
> staticky je tam 154 volání `_check(`, běh hlásí 113 kontrol.

> **➡ Detail bran (co měří, kde mají slepá místa, past „TIŠE PŘESTALA MĚŘIT"):**
> **`docs/BRANY-HRY.md`**. Sem se přesunul 7. 10. 2026 ze skillu `orchestra`
> (ten se načítá i v session, kde je zbytečný) — `AGENTS.md` drží jen souhrn.

## Design a smlouvy

> **⚠ PŘEPSÁNO 8. 10. 2026:** do té doby tu stálo, že `docs/DESIGN.md` je
> „co hra je a jak se má chovat“ a `docs/ARCHITEKTURA.md` je architektura
> a smlouvy. **Obě tvrzení byla nepravdivá**: `DESIGN.md:3` se sám hlásí jako
> **zrušený zdroj pravdy** a `ARCHITEKTURA.md` má tvar dat jen u **3 z 18**
> smluv. Nahradily je `docs/GDD.md` a `docs/TDD.md`; oba staré soubory
> **zůstávají jako historie** (nesmazány, v hlavičce mají, čím byly nahrazeny).

- **`docs/GDD.md`** — **co hra je a jak se hraje** (záměr, pilíře, smyčka,
  `V1`–`V8`, non-goals, obsah, milníky `M0`–`M6`). **Zdroj pravdy o designu.**
- **`docs/TDD.md`** — architektura běhu, vrstvy, **18 smluv s tvarem dat**,
  datové formáty, vlastnictví stavu, výkon, ukládání, chybové chování, jazyk.
  **Zdroj pravdy o technice.** **Kdo mění vlastnictví stavu, mění smlouvu** —
  ne kód potichu. Naměřeno 3. 10. 2026: `save.gd` ukládá pozici hráče
  podmíněně a `load()` jí přepíše spawn; kdo vlastní pozici, **není ve smlouvě**
  a nikdo to nenaplánoval.
- **`docs/ADD.md`** — jak hra vypadá a **proč**, katalog assetů („co má být
  vyrobeno“ vs. „co existuje“), pipeline (Blender / SDXL), placeholdery.
  **Strojová část vzhledu zůstává `assets/spec.json`** — ADD je k ní lidská
  vrstva, ne druhý zdroj čísel.
- **`CONVENTIONS.md`** — poučky, které agent dostává přes `--read`.
  **§1g je klíčový:** soubor granule musí začít `extends Node`, `class_name`
  nesmí být i jménem vnořené class, `_init()` bez povinného argumentu.
- **`.forge/roadmap.json`** — plán granulí (klíč **`grains`**, ne `tasks`;
  volitelně `owns`/`depends_on`/`acceptance`/`done`/`size_lines`/`model`).
  **Po každé editaci validuj JSON** — orchestra si ho čte přes GitHub API
  a rozbitá roadmapa znamená, že na hře **nikdo nepracuje**.

## Jazyk

Pravidlo je v `DSH_HOME\AGENTS.md`: **identifikátory, klíče a literály rozhraní
ASCII; dokumentace a komentáře česky; výstup pro člověka česky, hodnota pro
program anglicky.** **Potvrzeno uživatelem 8. 10. 2026** (rozhodnutí `R-3`,
`_analyza/DESIGN-REVIZE-2.md` §14.1) — platí i pro `assets/data/*.json`:
`id` anglicky (`iron_sword`), `name` česky („Železný meč").

> **⚠ OPRAVENO 8. 10. 2026 — text, který tu do té doby stál, byl nepravdivý.**
> Tvrdil, že veřejné rozhraní `add_rule(trigger, action)` v
> `scripts/assist.gd:11–15` **míchá jazyky** (`"hp < X"` a `"mana < X"`
> anglicky, ale `"cíl mrtev"` česky s diakritikou). **Naměřeno 8. 10. 2026:
> `scripts/assist.gd:15` má `"target dead"`** — rozhraní je **jazykově
> konzistentní** (anglicky) a je to správně. Kdo se řídil původním zněním,
> „opravoval" kód, který byl v pořádku. *(Naměřený případ:
> `_analyza/AUDIT-PLANU-A-DESIGNU.md` §4.5.)*

## Co nikdy

- **Nepřesouvat hru zpátky ani nedělat junctionu na staré místo.** Kdyby cesty
  vedly přes junctionu na `C:\...\Local-Deepseek\games\uo-shadows`, každá
  nepřepsaná cesta by **tiše fungovala dál** — a to je přesně to, čemu se
  přesun vyhýbal. Cesty mají **spadnout nahlas**.
- **Nepushovat bez vyžádání.** Předem ukázat `git status` a `git diff --stat`.
- **Nezaměňovat tuhle hru s jinou.** Vlastník `ssevcikm-spec` má **pět**
  repozitářů a `forge-quest` je **samostatná živá hra** (má vlastní Pages).
  **Odkaz na hru se odvozuje z NÁZVU REPA**, nikdy neopisuje z historie —
  v `release.yml` už jednou zůstal odkaz na `forge-quest` a kdo ho otevřel,
  hrál jinou hru.
- **Nepřebírat tvrzení o schopnostech** z dokumentace bez ověření.
- **Nemazat `_retired/`** — jsou to soubory, jejichž práce v `main` nebyla,
  a jsou **dokladem** toho, proč granule nesmí být `done` bez práce v repu.

## Kam pro co

| Soubor | Co v něm je |
|---|---|
| `docs/GDD.md` | **design hry** — záměr, pilíře, smyčka, `V1`–`V8`, ovládání, UI, svět, mechaniky se vzorci, obsah, non-goals, milníky `M0`–`M6` — **zdroj pravdy o designu** |
| `docs/TDD.md` | **technika hry** — architektura běhu, vrstvy, **18 smluv s tvarem dat**, datové formáty, vlastnictví stavu, výkon, ukládání, chyby, jazyk — **zdroj pravdy o technice** |
| `docs/ADD.md` | **vzhled** — lidská vrstva k `assets/spec.json`, katalog assetů, pipeline (Blender / SDXL), placeholdery, `A-1` odloženo |
| `docs/DESIGN.md` | **historie** — design od plánovače; **nahrazeno `docs/GDD.md`** 8. 10. 2026 (sám se hlásí jako zrušený) |
| `docs/BRANY-HRY.md` | **brány hry do detailu** — co která měří, naměřená slepá místa, past „TIŠE PŘESTALA MĚŘIT", šablona vs. hra |
| `docs/ARCHITEKTURA.md` | **historie** — původní architektura a smlouvy (`§2.1`–`2.3` a naměřené případy); **nahrazeno `docs/TDD.md`** 8. 10. 2026 |
| `CONVENTIONS.md` | konvence pro psaní granulí (agent je dostává přes `--read`) |
| `.forge/roadmap.json` | plán granulí (DAG) — **zdroj pravdy o tom, co se má dělat** |
| `.forge/vision-profile.json` | chování vizuální kontroly pro **tuhle** hru (záměrně v něm **není** schéma dlaždic — to je ve `spec.json`) |
| `assets/spec.json` | vizuální schéma hry (deklarace, proti které měří `check-schema.py`) |
| `tests/run_tests.gd` | testy hry — **čti „`[test] N kontrol, M selhání`"**, ne jen exit kód |
| `E:\Workspaces\forge-orchestra` | **orchestra** — kdo tuhle hru vyvíjí (jiné repo!) |
| `~\.dsh\skills\game-developer` | metodika rozpadu hry na granule (DAG) — jak se tu pracuje |
| `DSH_HOME\AGENTS.md` | **obecná pravidla stanice** — platí i tady, nejsou součástí hry |
