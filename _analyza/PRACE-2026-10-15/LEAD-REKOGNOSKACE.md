# LEAD — rekognoskace a naměřené nálezy (pracovní záznam session)

> **Co tenhle soubor JE:** **pracovní záznam lead session** z 15. 10. 2026, která
> přepracovává design dokumenty `uo-shadows`. **Není to stav projektu** (ten je
> v `ZASTAVENO.md`) a **není to výstup pro uživatele** — výstupem je přepsaný
> `docs/` a záznam o provedení. Slouží k tomu, aby se měření nemuselo opakovat
> a aby šlo dohledat, odkud které číslo pochází.
>
> **Napsáno:** 15. 10. 2026, session `session-911df9a2-…`, model deepseek-flash.
> **Repo při měření:** `HEAD 6986b0d`, pracovní strom čistý (jen tato složka
> untracked), `origin/main` = `01a9649` → **3 commity nepushnuté**.

---

## 1. Stav, jak byl naměřen živě (ne opsán z dokumentů)

| Co | Hodnota | Postup |
|---|---|---|
| `HEAD` | `6986b0d` | `git rev-parse --short HEAD` |
| Necommitnuté změny | žádné (strom čistý) | `git status --short` |
| Nepushnuté commity | **3** (`6986b0d`, `e4dccdb`, `0a5ee2f`) | `git rev-list --count origin/main..HEAD` |
| `origin/main` | `01a9649` | `git rev-parse --short origin/main` |
| Repo na GitHubu | **veřejné** (`private: false`), Pages zapnuté, `pushed_at` 8. 10. 2026 | GitHub API `repos/ssevcikm-spec/uo-shadows` |
| Souběh session | v repu nikdo jiný nepíše | `kdo-pise.mjs .` → `exit 0` |
| Brána dokumentů | `OK: 97 FAIL: 0 NEMĚŘENO: 0`, `exit 0` | `python _analyza/over-dokumenty.py --root .` |

> **⚠ Rozpor se záznamem:** `ZASTAVENO.md` §7 tvrdí **2 nepushnuté commity**.
> Naměřeno 15. 10. 2026 jsou **3** (`0a5ee2f` přibyl po zastavení projektu).
> Číslo v `ZASTAVENO.md` bylo **ve svém čase správné** (12. 10.) — je to záznam,
> nepřepisuje se; jen se k němu doplňuje.

## 2. Slepé místo brány nad dokumentací — naměřeno sabotáží

**Postup:** do **kopie** repa (`_analyza/saboter-dok`, po měření smazána) jsem
vložil dvě vady a spustil bránu nad kopií:

| Vložená vada | Co brána udělala |
|---|---|
| do `docs/GDD.md` věta „Hra má 500 kontrol a všechny jsou zelené." | **zelená** — `FAIL: 0` (číslo nikdo neměří) |
| do `docs/TDD.md` oddíl „Assist je non-goal `N9` a hra nesmí asistovat hráči." | **zelená** — `FAIL: 0` (rozpor mezi dokumenty se neměří) |

**Závěr:** brána měří **odkazy a čísla proti zdrojům** (co má ve svém seznamu),
ale **neměří vnitřní soulad dokumentů** ani **tvrzení, která nezná**. Proto
mohla být zelená nad dokumenty, o kterých `ZASTAVENO.md` §6 píše, že obsahují
**sedm rozporů**.

> **Past, na kterou jsem u toho narazil (a je použitelná jinde):** kopie repa
> nestačí jen s `docs/` — brána sahá i na `assets/data/*.json`, `tests/run_tests.gd`
> a `project.godot`, a bez nich **spadne na `FileNotFoundError`** (vypadá to jako
> vada nástroje, je to neúplný vstup). A spuštěná bez `PYTHONIOENCODING=utf-8`
> **spadne na vlastním českém výstupu** (`UnicodeEncodeError`, cp1252).
> Navíc `Set-Content -Encoding utf8` v PowerShellu přidá **BOM** — brána to
> poznala jako vadu `jazyk … BOM` (což je správně, ale měřilo to moje pero,
> ne dokument).

## 3. Rozpory nalezené vlastním čtením (křížová kontrola k teammateům)

| # | Rozpor | Místo A | Místo B | Co je pravda |
|---|---|---|---|---|
| R1 | `assist` je zakázaný (non-goal `N9`) vs. povolený | `docs/TDD.md:481–482` „`assist` je **non-goal `N9`** pro MVP — smlouva zůstává, ale nic na ní v MVP nestaví" | `docs/GDD.md:432–446` — `N9` **přerámováno 9. 10. 2026**: „rozhoduje hráč, hra provádí"; `assist.gd` a `offline.gd` **nejsou v rozporu s designem** | **GDD je novější a je zdroj pravdy o designu** → `TDD.md:481` je drift z doby před 9. 10. |
| R2 | Počet funkcí téhož měření | `docs/BRANY-HRY.md:87` „naměřeno **57 funkcí v 7 souborech**" | `docs/TDD.md:742,780` + `HANDOFF.md:193` „**97 funkcí** v 16 souborech" | rozhoduje **běh brány** `check-wiring.py` (měřeno znovu v této session — viz `FAKTA.md`) |
| R3 | Osud grafiky z Blenderu | `ZASTAVENO.md` §3/§6 „**258 PNG**, které hra nepoužívá" | `docs/ADD.md` §3 + `HANDOFF.md:170–173` — část je **pixel-identická** složenině vrstev (`d0_f1`), hra tedy zobrazuje **1 frame ze 128, zploštěný** | rozhoduje **měření odkazů v kódu** (viz `FAKTA.md`), ne odhad |
| R4 | Počet kontrol testů | staticky **154** volání `_check(` (`TDD.md:742`) | běh hlásí **`[test] 113 kontrol`** tamtéž | **běh**; statické číslo není počet kontrol (různé čítače téhož jména) |

> **Poznámka k metodě:** R1 a R2 jsem našel **grepem a čtením**, tedy jinou
> cestou než teammate `navrh-vrstev` (ten prochází celé dokumenty). Shoda obou
> cest je pro mě částečné ověření; neshoda znamená, že jeden z nás něco minul.

## 4. Co z toho plyne pro přepis

1. **Zdroj pravdy o designu je `GDD.md`** — kde se `TDD`/`ADD`/`BRANY-HRY`
   rozcházejí s ním, opravuje se **ten druhý dokument**, ne GDD.
2. **Čísla o kódu patří do jednoho faktového listu** (`FAKTA.md`) a dokumenty
   je citují s postupem — jinak vznikne třetí verze téhož čísla.
3. **Brána se musí rozšířit** o vnitřní soulad — bez toho se stejná vada vrátí
   při dalším přepisu (viz §2).
