# ZÁZNAM: přepracování design dokumentů `uo-shadows` (15. 10. 2026)

> **Co tenhle dokument JE:** **záznam o provedení** — co se 15. 10. 2026 udělalo
> s design dokumenty hry, čím je to doložené a co zůstalo otevřené.
> **Není to stav projektu** (ten je v `ZASTAVENO.md` — projekt je zastavený)
> **a není to zadání.**
>
> **Proč vznikl:** zadání znělo „s aktuálními skilly a poznatky přepracuj veškeré
> design dokumenty". Aby se příště nehádalo, co se vlastně změnilo a proč, je
> tady **postup, čísla a důkazy** — ne dojem z práce.
>
> **Vlastník:** session, která dokumenty mění. **Jak se mění:** **jen doplňuje**
> (je to záznam); co už neplatí, se označí, nemaže.

---

## 1. Co bylo zadáno a co z toho vzniklo

| # | Výstup | Stav |
|---|---|---|
| 1 | `docs/GDD.md` — zdroj pravdy o designu, přepsán podle dnešní metodiky | hotovo |
| 2 | `docs/TDD.md` — zdroj pravdy o technice (19 smluv, vlastník tiku, verze enginu) | hotovo |
| 3 | `docs/ADD.md` — vzhled a assety (copyright, opis deklarace, brány odkazem) | hotovo |
| 4 | `docs/BRANY-HRY.md` — jediný zdroj detailu o branách (+ nová slepá místa) | hotovo |
| 5 | `docs/README.md` — **rejstřík dokumentů** (vrstvy 0–10 → soubor) | hotovo |
| 6 | `ZASTAVENO.md` — doplněn odkaz na úplný seznam rozporů | hotovo (doplněno, ne přepsáno) |
| 7 | `_analyza/over-dokumenty.py` — brána rozšířena o vnitřní soulad | hotovo |
| 8 | `_analyza/PRACE-2026-10-15/` — měření, návrhy, tento záznam | hotovo |
| 9 | `CONVENTIONS.md` + `AGENTS.md` — opravy pravidel | **NEAPLIKOVÁNO** → `NAVRH-PRAVIDLA.md` |

## 2. Proč se do toho vůbec šlo — naměřený důvod

**Brána nad dokumentací byla zelená nad dokumenty, které si odporují.**
Naměřeno sabotáží (15. 10. 2026, na **kopii** repa, ne v repu):

| Vložená vada | Co stará brána udělala |
|---|---|
| do `docs/GDD.md` věta „Hra má 500 kontrol a všechny jsou zelené." | **zelená** (`FAIL: 0`) — vymyšlené číslo nikdo neměřil |
| do `docs/TDD.md` oddíl „Assist je non-goal `N9`…" (rozpor s `GDD.md:432`) | **zelená** (`FAIL: 0`) — rozpor mezi dokumenty se neměřil |

Stav před prací: **`OK: 97 / FAIL: 0`**, `exit 0`. Stav po práci:
**`OK: 127 / FAIL: 0`**, `exit 0`, sabotér **17 mutací** (z toho jeden negativní
test: citace zákazu se hlásit **nesmí**).

## 3. Co se našlo (a co se s tím udělalo)

| Co | Počet | Kde je doloženo |
|---|---|---|
| **Rozpory** mezi dokumenty | **24** (23× `ROZHODNOUT`, 1× ponechat otevřené) | `_analyza/PRACE-2026-10-15/ROZPORY.md` |
| **Duplicity** (totéž na dvou a více místech) | **8** | tamtéž §4 |
| **Drift** (dokument zaostal za kódem) | **3** | tamtéž §5 |
| **„Neškodné, ale matoucí"** | **5** | tamtéž §6 |
| **Naměřená fakta** o kódu pro přepis | **109** | `_analyza/PRACE-2026-10-15/FAKTA.md` |
| **Neměřeno** (s pojmenovaným důvodem) | **13** | tamtéž |

**Tři nálezy, které mají cenu i mimo tenhle projekt:**

1. **Plán je druhý a rozporný zdroj smluv.** `.forge/roadmap.json` je to jediné,
   co agent orchestry dostane jako zadání (`agent.yml:227`) — a prompty granul
   `world.nodes`, `ui.hud` a `sim.mining` odporují smlouvám v `docs/TDD.md` §3.
   U `world.nodes` (granule připravená k vydání) prompt žádá `gather() -> bool`
   a `snapshot() -> Array`, což neunese ani směs podle `GDD` `V4`, ani stav světa.
2. **Dvě pravidla v `CONVENTIONS.md` popírala dnešní stav** (agent „sám Godot
   nemá" — má; „nepřidávej nové soubory" — cíl `M0` je přesně opačný).
   `CONVENTIONS.md` je přitom **jediný dokument, který agent skutečně dostane**.
3. **Tvrzení skillu `game-developer` o chybějících vrstvách 1, 2 a 5 bylo
   pro dnešek vyvrácené** — všechny tři v `GDD` jsou (smyčka 8 vět, `V1`–`V8`,
   `N1`–`N11`). **Ve svém čase to správné bylo** (stav před 8. 10. 2026), takže
   se to označuje datem, **nepřepisuje**.

## 4. Jak se to ověřovalo

```powershell
$env:PYTHONIOENCODING='utf-8'; cd E:\Workspaces\uo-shadows
python _analyza\over-dokumenty.py --root .              # dokumenty proti zdrojům i sobě
python _analyza\over-dokumenty.py --root . --selftest   # umí brána vůbec selhat?
python E:\Workspaces\forge-orchestra\tools\over-dokumentaci.py   # pinované texty (jiné repo)
python .forge\check-schema.py .
python .forge\check-wiring.py .
& 'E:\Tools\godot\Godot_v4.7.2-stable_win64_console.exe' --headless --path . --script res://tests/run_tests.gd
```

**Výsledky (naměřeno 15. 10. 2026, `HEAD 6986b0d`; dokumenty byly před během
i po běhu **hashované stejně** — čísla jsou tedy pinovaná k verzi, ne „nějaká
z běhu“):**

| Co | Výsledek |
|---|---|
| `over-dokumenty.py --root .` (5 dokumentů) | **`OK: 152 / FAIL: 0 / NEMĚŘENO: 0`**, `exit 0` (před prací **97 / 0 / 0**) |
| `over-dokumenty.py --selftest` | **17/17 mutací chyceno**, `exit 0`; ⚠ **i negativní test**: citace zákazu a povolená výjimka **nesmí** vyrobit poplach |
| `_analyza/test-over-dokumenty.py` | **10/10**, `exit 0` (offline test výjimek nových kontrol; **umí spadnout** — doloženo 4 sabotážemi mechanismu) |
| `over-dokumentaci.py` (orchestra, jiné repo) | **`Kontrol: 64, chyb: 0`**, `exit 0` — všech 13 pinovaných textů na místě |
| `check-schema.py` | `exit 0` (a sám hlásí, že kontrola `world.gd` **NEPROBĚHLA**) |
| `check-wiring.py` | `exit 0`, **97 funkcí v 16 souborech** |
| `check-assets.py` | `exit 0` |
| Godot testy (běh) | **`[test] 113 kontrol, 0 selhání`** |
| Změněné soubory (`git diff --stat`) | |

**Hashy dokumentů při ověření (pin):** `GDD.md` `C361AEA7` · `TDD.md` `EEA35C1E`
· `ADD.md` `3EC36211` · `BRANY-HRY.md` `E93DC294` · `README.md` `74509B2B`
· `over-dokumenty.py` `AC71884F` — **před i po** všech bězích shodné.

## 5. Co se ZÁMĚRNĚ neudělalo

1. **Kód hry se neopravoval** — vady se **zapisují**. Nově naměřené:
   `game.gd:181` tweenuje `hud` dřív, než ho `_add_ui()` vytvoří (ERROR při
   každém načtení scény; CI to nechytí, hledá jen `SCRIPT ERROR`), a
   `economy.price()` vrací **0** pro oba předměty (`economy.gd:21`).
2. **`.forge/roadmap.json` se neměnil** — je to vstup orchestry (jiné repo)
   a jeho výměna je **operace**, ne editace souboru; navíc je projekt zastavený.
3. **Historie se nepřepisovala** — `docs/DESIGN.md` a `docs/ARCHITEKTURA.md`
   zůstávají; u `ARCHITEKTURA.md` je uvnitř **dvě vzájemně se vylučující tvrzení
   o autoritě** (`R19`) a správná oprava je **doplnit označení**, ne přepsat.
4. **Dokumenty se nepřejmenovaly** na číslované — naměřeno: rozbilo by **57 odkazů
   v záznamech** (které se nesmí přepisovat), **30 v plánu**, 1 bránu v repu
   a 2 v orchestraci.
5. **Trvalá pravidla (`CONVENTIONS.md`, `AGENTS.md`) se neaplikovala** — návrh
   s přesným zněním je v `_analyza/PRACE-2026-10-15/NAVRH-PRAVIDLA.md`.
   Důvod: podle pravidla stanice mění trvalá pravidla uživatel.
6. **Nepushovalo se** — v repu jsou **3 commity z předchozích session**
   (nevytvořila je tahle session; `ZASTAVENO.md` §7 to řeší).

## 6. Co zůstalo otevřené

**Nic se nemazalo** — co bylo otevřené před přepisem, je otevřené dál (v GDD
`O-1`…`O-5`, odložené `N-2`, `A-1`; v TDD `§10` známé vady). Tohle je výčet
**nový**, který přepis odhalil nebo který vznikl jeho prací:

| # | Co je otevřené | Kde je to doložené | Co to vrátí |
|---|---|---|---|
| 1 | **`assets/spec.json` si odporuje sám se sebou** — `_popis` tvrdí „celočíselný dělitel 8“ a „barvy se mapují na paletu“, ale `styl.zmenšování` a `paleta.zdroj = null` říkají opak; `styl.technika` „v 5 směrech“ vs. `smery = 4` a `postprocess.py` `DIRS = 4`; `_stav` odkazuje na neexistující soubory | `ROZPORY.md` `R5`–`R8`; `ADD §11` | rozhodnutí uživatele (spec.json se v této session **needituje** — je to deklarace, ne dokument) |
| 2 | **`.forge/roadmap.json` je druhý, rozporný zdroj smluv.** Prompty granul `world.nodes`, `ui.hud`, `sim.mining` odporují `TDD §3` (např. `gather() -> bool`, `snapshot() -> Array`, `attributes.get`) | `ROZPORY.md` `R10`–`R12`, §8.2 a §8.3 (hotové znění) | přepsat prompty **ze smluv** — a je to **operace** (plán čte orchestra přes API), ne editace souboru |
| 3 | **`provides`/`consumes` = 0 z 21 granul** — agent orchestry dostane smlouvu jen prózou promptu | `FAKTA.md`, `REJSTRIK-NAVRH.md` §2 (vrstva 7) | doplnit při příští editaci plánu |
| 4 | **Agent orchestry design a smlouvy NEDOSTANE** — `.github/workflows/agent.yml` předává jen `CONVENTIONS.md` + soubory granule | `REJSTRIK-NAVRH.md` §2.1 | **změna orchestrace v jiném repu** (`forge-orchestra`) |
| 5 | **Chybí rejstřík pastí** (vrstva 10) — pastí je šest na pěti místech a nikde není jejich seznam | `REJSTRIK-NAVRH.md` §2 | doplnit do `CONVENTIONS.md` (návrh je v `NAVRH-PRAVIDLA.md`) |
| 6 | **Tři náklady řemesla (palivo, opotřebení, zmetkovost) jsou rozhodnuté, ale bez čísel** — hodnoty se ladí hraním (`M3`) | `GDD §9.2` | sehrát `M3` (projekt je zastavený) |
| 7 | **Dvě nové vady běhu jsou zapsané, ne opravené:** `game.gd:181` tweenuje `hud` před `_add_ui()` (`ERROR: Required object "rp_target" is null`); `economy.price()` vrací **0** pro oba předměty (`economy.gd:21`) | `TDD §10` vada 11; `BRANY-HRY.md` | **rozhodnutí uživatele** — projekt je zastavený, kód se neopravuje |
| 8 | **`CONVENTIONS.md` + `AGENTS.md` zůstaly neaplikované** (jsou to trvalá pravidla) | `NAVRH-PRAVIDLA.md` | **rozhodnutí uživatele**: aplikovat návrh, nebo ho zamítnout |
| 9 | **`spec.json` nemá deklaraci filtru** — `project.godot` má Nearest (pro celočíselné 2× zvětšení), dlaždice se ale škálují neceločíselně | `ROZPORY.md` `R21` | doplnit `filtr` do `spec.json`, aby to bylo měřitelné |
| 10 | **Měření testů je citlivé na prostředí:** čistý export bez `.godot/` dá **111 kontrol / 3 selhání** místo 113/0 (falešná regrese) | `BRANY-HRY.md` | vědět to předtím, než někdo „opraví“ zdravý strom |
| 11 | **V repu jsou 3 commity z předchozích session, nepushednuté** — nevznikly v této session | `git rev-list --count origin/main..HEAD` = 3 | **rozhodne session, která je vytvořila** (`ZASTAVENO.md` §7) |
| 12 | **`ZASTAVENO.md §7` uvádí 2 nepushnuté commity, naměřeno jsou 3** | `ZASTAVENO.md:74–76` | číslo bylo **ve svém čase správné** (12. 10.); jen se k němu doplňuje |
| 13 | **Mimo repo zůstala evidence** `E:\Workspaces\_mereni-uo-shadows-6986b0d\` (698 souborů, 12,5 MB) | — | smazat, až nebude potřeba (je to surový záznam měření) |

## 7. Jak si to ověřit (5 minut)

```powershell
$env:PYTHONIOENCODING='utf-8'; cd E:\Workspaces\uo-shadows
python _analyza\over-dokumenty.py --root .              # OK: 152 / FAIL: 0 / NEMĚŘENO: 0, exit 0
python _analyza\over-dokumenty.py --root . --selftest   # 17/17 mutací, REPO NEDOTČEN
python _analyza\test-over-dokumenty.py                  # 10/10, exit 0
python E:\Workspaces\forge-orchestra\tools\over-dokumentaci.py   # Kontrol: 64, chyb: 0
& 'E:\Tools\godot\Godot_v4.7.2-stable_win64_console.exe' --headless --path . `
  --script res://tests/run_tests.gd                     # [test] 113 kontrol, 0 selhání
git show --stat HEAD                                    # co je v commitu (po commitu)
```
