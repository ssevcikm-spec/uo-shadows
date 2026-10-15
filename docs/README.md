# Rejstřík dokumentů hry `uo-shadows`

> **Co tenhle dokument JE:** **rejstřík (rozcestník)** — druh: rozcestník, ne
> zdroj pravdy o hře. Odpovídá na otázku „**kde je která vrstva přípravy hry**"
> a „**co je zdroj pravdy v čem**". **Není to zdroj pravdy o ničem** — jen
> ukazuje, kam se chodit ptát. (Kdyby tu stálo totéž co v odkazovaných
> dokumentech, byl by to **čtvrtý zdroj pravdy** — přesně ta vada, kterou
> tenhle rejstřík pomáhá odstraňovat.)
>
> **Vzniklo:** 15. 10. 2026 (session, která přepracovala design dokumenty).
> **Vlastník a údržba:** session, která mění dokumenty hry (řádek navíc při
> každé změně struktury). **Jak se mění:** přepisuje se celý (je to stav);
> **řádek se nikdy nemaže** — když soubor zmizí, řádek se označí a zůstane jako
> stopa. **Odkud brát stav:** `docs/GDD.md` (design), `docs/TDD.md`
> (technika), `docs/ADD.md` (vzhled), `.forge/roadmap.json` (plán),
> `ZASTAVENO.md` (proč se nevyvíjí) — **ne tenhle rejstřík**.

---

## 1. Zdroj pravdy v jedné tabulce

| Otázka | Dokument | Poznámka |
|---|---|---|
| Jak se hra hraje, pilíře, smyčka, non-goals, milníky | **`docs/GDD.md`** | zdroj pravdy o **designu** |
| Jak je hra postavená, smlouvy, formáty, vlastnictví stavu | **`docs/TDD.md`** | zdroj pravdy o **technice** |
| Jak hra vypadá, assety, pipeline, licence | **`docs/ADD.md`** | lidská vrstva; **čísla vzhledu** jsou v `assets/spec.json` |
| Co která brána měří a **kde má slepá místa** | **`docs/BRANY-HRY.md`** | jediné místo detailu o branách |
| Co se má dělat (granule a závislosti) | **`.forge/roadmap.json`** | strojový plán; čte ho orchestra |
| Jak se hra staví po milnících a co je k vydání | **`docs/PLAN-VYVOJE.md`** | lidská vrstva plánu (lidská vrstva k `.forge/roadmap.json`) |
| Proč se nevyvíjí a co by ho vrátilo | **`ZASTAVENO.md`** | záznam o zastavení (12. 10. 2026) |
| Čím se psát kód (poučky pro agenta) | **`CONVENTIONS.md`** | jediný dokument, který agent orchestry dostane |
| Trvalá pravidla hry | **`AGENTS.md`** | dostane je každá session |
| Jak se staví a co se už pokazilo | `_analyza/DESIGN-REVIZE-2.md`, `_analyza/PRACE-2026-10-15/` | zdroj rozhodnutí + měření |

## 2. Vrstvy přípravy → kde jsou

**Model vrstev** je z `KONCEPT-PRIPRAVY-HRY.md` (jedenáct vrstev `0`–`10`, každá
se odvozuje z té nad sebou). **Tabulka je navigace, ne náhrada** — čti soubor.

| # | Vrstva | Kde je | Pokrytí k 15. 10. 2026 |
|---|---|---|---|
| **0** | Záměr | `GDD §0` | plné |
| **1** | Zážitek (pilíře, smyčka, ovládání, UI) | `GDD §1`–`§7` | plné |
| **2** | Míra úspěchu | `GDD §3` + `GDD §4` (`V1`–`V8`) | plné |
| **3** | Mechaniky a čísla | `GDD §9` | **částečné** — tři náklady řemesla jsou rozhodnuté, ale **bez čísel** (ladí se hraním, `M3`) |
| **4** | Obsah | `GDD §10` + `TDD §4` + `assets/data/*.json` | plné jako seznam; data rozsahu `M` chybí (práce, ne dokument) |
| **5** | Rozsah a non-goals | `GDD §10` + `GDD §11` (`N1`–`N11`) | plné |
| **6** | Technika | `TDD §0` (engine a platformy), `§1`, `§6`, `§7`, `§8` | plné |
| **7** | Smlouvy | `TDD §3` (**19 smluv** s tvarem dat), `§4`, `§5` | plné v dokumentu; **v plánu nejsou strojově** (`provides`/`consumes` se v granulích nevedou — smlouva je vložená v zadání, ne odkazem) |
| **8** | Plán | `docs/PLAN-VYVOJE.md` + `GDD §12` (milníky) + `.forge/roadmap.json` (dnes **11 granulí**, z toho 5 k vydání) | **částečné** — k vydání `M0`+`M1`; `M2`–`M6` jsou zásoba, doplní se při otevření milníku |
| **9** | Brány | **`docs/BRANY-HRY.md`** (+ `TDD §9` = jen pořadí v CI) | plné |
| **10** | Pravidla a pasti | `CONVENTIONS.md`, `AGENTS.md`, `TDD §10` (známé vady), `BRANY-HRY.md` (slepá místa), `ZASTAVENO.md §6` | částečné — **rejstřík pastí chybí** (pastí je šest na pěti místech) |

> **Kdo vrstvy nedostane:** agent orchestry dostane jen `CONVENTIONS.md` a soubory
> své granule (`.github/workflows/agent.yml`) — **design ani smlouvy ne**. To je
> otevřený bod orchestrace (jiné repo), ne vada dokumentů; je zapsaný níž.

## 3. Historie — dokumenty, které se needitují

| Soubor | Čím byl | Nahrazen |
|---|---|---|
| `docs/DESIGN.md` | design od plánovače | `docs/GDD.md` (8. 10. 2026) |
| `docs/ARCHITEKTURA.md` | architektura a smlouvy (tvar dat u 3 z 18) | `docs/TDD.md` (8. 10. 2026) |

**Pravidlo:** do historie se **nepřidává nová znalost** a **nepřepisuje se** —
jen se doplňuje označení, co už neplatí. Naměřeno 15. 10. 2026:
`ARCHITEKTURA.md` má uvnitř **dvě vzájemně se vylučující tvrzení o autoritě**
(hlavička „není zdroj pravdy" vs. tělo „jediný závazný") — čte se to jako
neškodné, protože hlavička je výš, ale **matoucí to je** (zapsáno v `ROZPORY.md`
`R19`).

## 4. Povinná hlavička každého dokumentu

Každý dokument v tomhle rejstříku začíná šesti položkami:

```
> **Co tenhle dokument JE:** <druh> — <jedna věta>.
> **Čím je:** zdroj pravdy / zadání / snapshot / záznam / stav / plán / kronika / rejstřík.
> **Čím NENÍ:** <co si v něm čtenář nesmí hledat>.
> **Odkud brát stav:** <soubor, který je dnešní stav — ne tenhle dokument>.
> **Platí z něj:** <co platí dnes>; **datum spotřeby:** <kdy/čím se spotřebovalo>.
> **Vzniklo:** <datum> · **Vlastník a údržba:** <kdo a kdy> · **Jak se mění:** stav = přepisuje se · záznam = doplňuje se · kronika = nikdy.
```

**Proč to je povinné (naměřeno):** ve workspace se sejde víc dokumentů a každý
tvrdí jiný „dnešní stav"; kdo pak hledá pravdu, čte ten **nejnovější podle data
souboru** — a to je jiná otázka, než „který je zdroj pravdy".

## 5. Rozhodnutí o rozporech (k 15. 10. 2026)

Úplný seznam (24 rozporů, 8 duplicit, 3 drifty, 5 „neškodné, ale matoucí")
s citacemi obou stran je v `_analyza/PRACE-2026-10-15/ROZPORY.md`.
Tady je jen **co se rozhodlo**, aby se to nemuselo hledat:

| # | Rozpor | Rozhodnutí | Kde se to projevilo |
|---|---|---|---|
| `R1` | `assist` je/není non-goal `N9` | **`GDD §11` platí** (`N9` přeformulováno 9. 10. 2026: „rozhoduje hráč, hra provádí"); `TDD` byl drift | `TDD §3.15` |
| `R2` | `world.gd` blokuje `world.map`, nebo `engine.shell` | blokuje **`world.nodes`**; `world.map` vyřazena 8. 10. 2026; `engine.shell` **blokovaná není** | `TDD §3.5`, `§10`; `GDD §13` |
| `R9` | Tik a fronty vlastní `game.gd`, nebo `registry.gd` | **`scripts/registry.gd`** (naměřeno); `game.gd` = kostra scény | `TDD §1.2`, `§2`, `§3.19`, `§5` |
| `R12` | `Mining.gather` vrací `int`, nebo `Dictionary` | dnes **`int`** (naměřeno); cílový tvar `Dictionary` podle `World.gather` | `TDD §3.10` |
| `R17` | Vydavatel a copyright v exportu | **`ssevcikm-spec`** a „© 2026 ssevcikm-spec" (rozhodnutí uživatele); dokumenty tvrdily opak | `GDD §14.2`, `ADD §12` |
| `R4` | Brána `check-licence.py` existuje/neexistuje | **neexistuje** (naměřeno v `.forge/`) | `BRANY-HRY.md`, `ADD §11` |
| `R22` | „Sedm rozporů" a „57 vs 97 funkcí" | **není to rozpor**: jsou to **dvě datovaná měření téhož nástroje**; „sedm" bylo číslo bez seznamu | `ZASTAVENO.md §6`, `BRANY-HRY.md` |

## 6. Brána nad dokumenty

Dokumenty se **měří jako kód**:

```powershell
$env:PYTHONIOENCODING='utf-8'; cd E:\Workspaces\uo-shadows
python _analyza\over-dokumenty.py --root .              # dokumenty proti zdrojům i sobě
python _analyza\over-dokumenty.py --root . --selftest   # sabotér: umí brána vůbec selhat?
```

**Tři stavy:** `exit 0` = vše změřeno a v pořádku · `1` = rozpor (se zdrojem
nebo **mezi dokumenty**) · `2` = něco zůstalo **NEMĚŘENO** — a to **není zelená**.
`--selftest` vkládá do **kopií** dokumentů vady (včetně rozporu mezi dokumenty
a vymyšleného čísla) a ověřuje, že je brána chytí; repo přitom zůstává nedotčené.

**Naměřeno 15. 10. 2026:** před rozšířením `OK 97 / FAIL 0` — a **přitom nechala
projít** jak vymyšlené číslo, tak rozpor `assist`/`N9`. Po rozšíření
`OK 127 / FAIL 0`, sabotér **17 mutací**.

> **Dokument, který brána nezměří, není hotový.** A když brána hlásí `NEMĚŘENO`,
> **není to zelená** — je to přiznání, že se něco nezkontrolovalo.

## 7. Co v tomhle rejstříku ZÁMĚRNĚ NENÍ

- **Žádná vlastní tvrzení o hře** — jen cesty a rozdělení odpovědností. Co je
  v GDD, se tu neopakuje (druhý zdroj pravdy by vznikl okamžitě).
- **Žádný seznam granulí** — ten je v `.forge/roadmap.json` a rejstřík by ho
  jen zdvojil.
- **Žádná čísla o kódu** — ta mají domov v `docs/TDD.md`, `docs/BRANY-HRY.md`
  a v měření (`_analyza/PRACE-2026-10-15/FAKTA.md`).
- **Rejstřík pastí** (vrstva 10) tu ještě není — pastí je dnes šest na pěti
  místech a jejich sjednocení je otevřený bod (viz `_analyza/PRACE-2026-10-15/NAVRH-PRAVIDLA.md`).
