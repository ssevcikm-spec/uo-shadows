# BRIEF — přepis design dokumentů `uo-shadows` (15. 10. 2026)

> **Co tenhle soubor JE:** **pracovní zadání pro autory přepisu** (teammates, které
> vede lead session). Není to dokument hry a **není to výstup pro uživatele**.
> Drží dohromady: co je zdroj pravdy, co je naměřeno, jak má vypadat hlavička
> a jak se výsledek ověřuje. **Kdo přepisuje dokument, čte tenhle soubor první.**

---

## 0. Zadání od uživatele (doslovně, 15. 10. 2026)

> „S aktuálními skilly a poznatky přepracuj veškeré design dokumenty"

**Co to znamená konkrétně:** design dokumenty hry `uo-shadows` přepsat tak, aby
odpovídaly **dnešní metodice** (skill `game-developer` — vrstvy přípravy;
skill `dokumentace` — druhy dokumentů a hlavičky; `KONCEPT-PRIPRAVY-HRY.md` —
jedenáct vrstev a kontrolní seznam), aby si **neodporovaly** a aby každé číslo
mělo **postup, kterým vzniklo**.

**Co to NEznamená:**
- **Neměnit kód hry** ani `.forge/roadmap.json` (projekt je **zastavený** —
  `ZASTAVENO.md`; kód se neopravuje, jen se o vadách píše).
- **Nepřepisovat historii:** `docs/DESIGN.md` a `docs/ARCHITEKTURA.md` zůstávají,
  jen s hlavičkou „čím je a čím bylo nahrazeno". Historická čísla se **nepřepisují**,
  označí se jako „ve svém čase správná".
- **Nezakládat čtvrtý zdroj pravdy.** Tři zdroje (`GDD`, `TDD`, `ADD`) + `spec.json`
  stačí; rozpor se řeší **v jednom z nich**, ne novým souborem.

## 1. Zdroj pravdy — kdo rozhoduje v čem

| Otázka | Rozhoduje | Ostatní dokumenty |
|---|---|---|
| Jak se hra hraje, pilíře, smyčka, non-goals, milníky | **`docs/GDD.md`** | odkazují, neopisují |
| Jak je hra postavená, smlouvy, formáty, stav | **`docs/TDD.md`** | odkazují |
| Jak hra vypadá, assety, pipeline | **`docs/ADD.md`** | odkazují; **čísla vzhledu** jsou v `assets/spec.json` |
| Co která brána měří a kde má slepá místa | **`docs/BRANY-HRY.md`** | `TDD` jen odkazuje (dnes to má na dvou místech) |
| Naměřená fakta o kódu | **`_analyza/PRACE-2026-10-15/FAKTA.md`** | každý dokument cituje fakt + postup |

> **Pravidlo proti tichému rozporu:** kde dokument potřebuje cizí číslo, **cituje
> ho s postupem** („naměřeno: …") — nevymýšlí druhé. Kde potřebuje cizí tvrzení,
> **odkazuje na oddíl** (`GDD` §11) a **neopakuje ho vlastními slovy**.

## 2. Naměřená fakta (z `FAKTA.md`, HEAD `6986b0d`)

**Používej tato čísla a nic si nedomýšlej. Kde chceš jiné, změř ho a napiš postup.**

| Co | Hodnota | Poznámka |
|---|---|---|
| Testy (běh) | **`[test] 113 kontrol, 0 selhání`**, exit 0 | 2 běhy; úklid hlásí `11 ObjectDB leaked` — to **není** selhání testů |
| Testy (staticky) | `has_method` 28 řádků / 41 výskytů; `_check(` **154 volání** | **statické číslo není počet kontrol** — různé čítače téhož jména |
| Kód | 16 skriptů / **1 716 řádků**; produkční cesta **3 soubory / 851**; mrtvá knihovna **13 / 865** | `scripts/world.gd` = **0 B** |
| Brány | `check-schema` exit 0 · `check-wiring` exit 0 = **97 funkcí v 16 souborech** · `check-assets` exit 0 | u `check-schema` **kontrola `world.gd` NEPROBĚHLA** (slepé místo) |
| Sprity | `assets/sprites` 16 PNG → hra odkazuje **2**; dlaždice 7 → použité **4**; `tools/blender/sprites` **258 → 0 odkazů** | `player.png`/`npc.png` jsou **pixel-identické** složenině `d0_f1` (shodné sha256) |
| Obsah | materials 4, items 2, recipes 3, skills 4, monsters 1 | `creatures.json` **neexistuje** |
| Mapa | **30×16 = 480** dlaždic, průchodných 109, markery **4** (spawn 1 / coin 2 / exit 1), spawn (17,7) | |
| Plán | 21 granulí, **16 `done: true`**, 4 READY, 1 blokovaná; **`provides`/`consumes` = 0/0** | 0/0 je nález: smlouvy nejsou ve strojové roadmapě |
| Konfigurace | **0 autoloadů**, **0 `input/*` akcí**, 960×540, `product_name = uo-shadows`, 3 export presety | vstup jde přes `Input.is_key_pressed` |
| Ukládání | `user://save.cfg`, 9 klíčů | druhá cesta `user://sandbox.cfg` v `game.gd` je **nepoužitá** |
| CI | 13 kroků: schema → testy → assety → wiring → smoke → render → vision (neblokuje) → export | |

**Dvě nové vady (zapsat, neopravovat):** `game.gd:181` tweenuje `hud` dřív, než ho
`_add_ui()` vytvoří (ERROR při každém načtení scény; CI hledá jen `SCRIPT ERROR`,
takže to nechytí) · `economy.price()` vrací **0** pro oba předměty a hlásí chybu
na `economy.gd:21`.

## 3. Rozpory — jak se řeší

1. **`TDD.md:481`** říká, že `assist` je non-goal `N9`, ale **`GDD.md:432–446`** ho
   od 9. 10. 2026 **povoluje** („rozhoduje hráč, hra provádí"). → **GDD je novější
   a je zdroj pravdy o designu**: `TDD` se opraví na „mimo MVP, ale dovolený v mezích
   `N9`" a **odkáže na GDD**.
2. **Počet funkcí:** `BRANY-HRY.md:87` „57 v 7 souborech" vs naměřených **97 v 16**.
   → opravit na naměřené číslo **s postupem** (výstup `check-wiring.py`).
3. **„258 PNG hra nepoužívá"** je nepřesné: část je pixel-identická složenině
   vrstev. → napsat přesně: **0 odkazů z kódu**, ale `player.png`/`npc.png` **jsou**
   složenina jednoho framu (`d0_f1`), doloženo sha256.
4. **Další rozpory** najdeš v `ROZPORY.md` (teammate `navrh-vrstev`) a `FAKTA.md` §rozpory.

## 4. Jak má vypadat hlavička (povinná, skill `dokumentace`)

Každý dokument začíná hlavičkou, která odpoví **čtyřmi** větami:
1. **Co tenhle soubor JE** (druh: zdroj pravdy o designu / o technice / o vzhledu /
   katalog bran / historie) — a čím **není**.
2. **Odkud brát současný stav**, když jím sám není.
3. **Datum poslední revize** a **co se v ní změnilo** (jedna věta).
4. U historie navíc: **čím bylo nahrazeno a kdy**.

## 5. Pravidla psaní (bez nich je přepis k ničemu)

1. **Každé číslo má postup.** „97 funkcí" bez „výstup `check-wiring.py`, exit 0" je
   neověřitelné — čtenář ho buď uvěří, nebo „opraví" špatně.
2. **Stav se ověřuje živě.** Netvrď „není pushnuto", „běží", „fronta je prázdná",
   když to nemáš z měření v této session.
3. **Nula ≠ neměřeno.** Co se nezměřilo, se **pojmenuje** (`NEMĚŘENO` + důvod).
4. **Historická čísla se nepřepisují** — označí se „ve svém čase správná".
5. **Nic nesmí zmizet.** Otevřené body z původní verze se buď přenesou, nebo
   se přesunou do oddílu „už není otevřené" — **nemažou se**.
6. **Každý dokument má oddíl „co v něm ZÁMĚRNĚ NENÍ"** — jinak si agent domyslí
   sousední vrstvu.
7. **Doslovné ukázky rozbité diakritiky se popisují slovem**, ne znakem.
8. **Jazyk:** identifikátory, klíče a literály rozhraní **anglicky**; dokumentace
   a texty pro člověka **česky**.

## 6. Jak se výsledek ověřuje (povinné pro každého autora)

```powershell
$env:PYTHONIOENCODING='utf-8'
cd E:\Workspaces\uo-shadows
python _analyza\over-dokumenty.py --root .        # dokumenty proti zdrojům
python _analyza\over-dokumenty.py --root . --selftest   # sabotér: umí brána selhat?
python .forge\check-schema.py .                   # tvrdá brána
python .forge\check-wiring.py .
& 'E:\Tools\godot\Godot_v4.7.2-stable_win64_console.exe' --headless --path . --script res://tests/run_tests.gd
```

**Autor hlásí:** co přepsal, která čísla vzal odkud, co si **nevymyslel**, co
zůstalo otevřené a co **nešlo ověřit**. Bez toho se přepis neuzavírá.
