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

> **⚠ Podmíněný test je tiše zelený.** `tests/run_tests.gd` má **26 řádků
> s `has_method`** (**39 výskytů** — naměřeno 7. 10. 2026; dřívější číslo „27
> podmíněných kontrol" bylo nepravdivé) — funkce, která **není**, se **přeskočí**
> a test projde. Test musí kód **ZAVOLAT** a ověřit výsledek.

> **➡ Detail bran (co měří, kde mají slepá místa, past „TIŠE PŘESTALA MĚŘIT"):**
> **`docs/BRANY-HRY.md`**. Sem se přesunul 7. 10. 2026 ze skillu `orchestra`
> (ten se načítá i v session, kde je zbytečný) — `AGENTS.md` drží jen souhrn.

## Design a smlouvy

- **`docs/DESIGN.md`** — co hra je a jak se má chovat.
- **`docs/ARCHITEKTURA.md`** — architektura a **smlouvy** (kdo vlastní jaký
  stav). **Kdo mění vlastnictví stavu, mění smlouvu** — ne kód potichu.
  Naměřeno 3. 10. 2026: `save.gd` ukládá pozici hráče podmíněně a `load()` jí
  přepíše spawn; kdo vlastní pozici, **není ve smlouvě** a nikdo to nenaplánoval.
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
program anglicky.** Naměřený případ tady: `scripts/assist.gd:11–15` — veřejné
rozhraní `add_rule(trigger, action)` **míchá jazyky** (`"hp < X"` a
`"mana < X"` anglicky, ale `"cíl mrtev"` česky s diakritikou). Volající musí
uhodnout jazyk — to je vada rozhraní, ne kosmetika.

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
| `docs/DESIGN.md` | design hry |
| `docs/BRANY-HRY.md` | **brány hry do detailu** — co která měří, naměřená slepá místa, past „TIŠE PŘESTALA MĚŘIT", šablona vs. hra |
| `docs/ARCHITEKTURA.md` | architektura a **smlouvy** (vlastnictví stavu) |
| `CONVENTIONS.md` | konvence pro psaní granulí (agent je dostává přes `--read`) |
| `.forge/roadmap.json` | plán granulí (DAG) — **zdroj pravdy o tom, co se má dělat** |
| `.forge/vision-profile.json` | chování vizuální kontroly pro **tuhle** hru (záměrně v něm **není** schéma dlaždic — to je ve `spec.json`) |
| `assets/spec.json` | vizuální schéma hry (deklarace, proti které měří `check-schema.py`) |
| `tests/run_tests.gd` | testy hry — **čti „`[test] N kontrol, M selhání`"**, ne jen exit kód |
| `E:\Workspaces\forge-orchestra` | **orchestra** — kdo tuhle hru vyvíjí (jiné repo!) |
| `~\.dsh\skills\game-developer` | metodika rozpadu hry na granule (DAG) — jak se tu pracuje |
| `DSH_HOME\AGENTS.md` | **obecná pravidla stanice** — platí i tady, nejsou součástí hry |
