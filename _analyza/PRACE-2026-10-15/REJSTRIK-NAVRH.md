# Rejstřík vrstev pro `uo-shadows` — NÁVRH

> **Co tenhle dokument JE:** **návrh rejstříku** (rozcestník „která vrstva přípravy
> → kde je dnes → kam patří v nové verzi“). Není to stav projektu a **není to
> plán práce** — je to podklad k rozhodnutí, co s dokumenty udělat.
>
> **Co z něj platí:** platí **mapa a nálezy k datu měření** (viz níže). Neplatí
> jako závazek — strukturu mění až rozhodnutí uživatele/lead session. Až podle něj
> někdo dokumenty přepíše, patří do hlavičky tenhle soubor jako **zdroj zadání**
> (a řádek „podle čeho se přepisovalo“).
>
> **Vzniklo:** 15. 10. 2026 (session, která **nemění kód ani dokumenty**).
> **Metodika:** `C:\Users\Ssevc\Local-Deepseek\KONCEPT-PRIPRAVY-HRY.md` — jedenáct
> vrstev `0`–`10` (§2) + kontrolní seznam „je příprava dost?“ (§7) + třináct zásad
> pro AI (§5) + **příloha B** (jak má vypadat který dokument).
> **Vzory hotového stavu (jiné projekty, jen ke čtení):**
> `E:\Workspaces\game-clone\docs\` (11 souborů) a `E:\Workspaces\The-Hero-Arc\docs\`
> (`01-cil-a-scope` … `09-pravidla`).
>
> **Naměřeno k:** `HEAD = 6986b0d` (12. 10. 2026 14:45, `origin/main = 01a9649`,
> pracovní strom čistý). **Kód ani dokumenty jsem neměnil** — jediné, co jsem
> zapsal, jsou dva soubory v `_analyza/PRACE-2026-10-15/` (tento a `ROZPORY.md`).
>
> **Čím se měřilo:** čtení `docs/*.md`, `AGENTS.md`, `CONVENTIONS.md`,
> `assets/spec.json` a `.forge/roadmap.json` po řádcích; `python .forge\check-wiring.py .`
> (97 funkcí / 16 souborů, `exit 0`); `python _analyza\over-dokumenty.py`
> (97 OK / 0 FAIL / 0 NEMĚŘENO, `exit 0`); měření souborů a JSON klíčů Pythonem
> (`os.walk`, `json`, `splitlines()`); `git log`/`git show --stat`.

---

## 0. Souhrn pro rozhodnutí (jedním odstavcem)

**Všech jedenáct vrstev dnes v repu je.** Tvrzení skillu `game-developer`, že
chybí vrstvy 1 (zážitek), 2 (míra úspěchu) a 5 (non-goals), **pro dnešek
neplatí** — všechny tři jsou v `docs/GDD.md` s konkrétními čísly řádků (§2).
Co ale **neplatí dobře, je „jedno místo“**: vrstva **9 (brány)** je na čtyřech
místech, vrstva **10 (pravidla a pasti)** nemá jedno místo vůbec, vrstva
**8 (plán)** má domov jen pro milníky `M0`–`M1` a **žádná vrstva není dostupná
agentovi orchestry** (tomu se předává jen `CONVENTIONS.md` a soubory granule —
naměřeno v `.github/workflows/agent.yml:227`). Doporučuji **variantu A**
(zachovat názvy `GDD`/`TDD`/`ADD`, přidat mapu vrstev a povinnou hlavičku) —
přejmenování na číslované soubory by rozbilo **57 odkazů v souborech, které se
podle pravidla stanice **nesmí přepisovat** (záznamy)**, **30 odkazů v plánu**
`.forge/roadmap.json` a **tři brány** (jedna v repu, dvě v orchestraci).

---

## 1. Kontrola tvrzení skillu `game-developer` (vrstvy 1, 2, 5)

**Co skill tvrdí** (`C:\Users\Ssevc\.dsh\skills\game-developer\SKILL.md:742–744`):
> „**Druhá práce (neuděláno):** přepsat design `uo-shadows` podle konceptu —
> chybí vrstvy 1 (zážitek), 2 (míra úspěchu) a 5 (non-goals) — **v session,
> která zároveň neopravuje kód**.“

**Co je naměřeno dnes** (čtením `docs/GDD.md`, 524 řádků, sepsán 8. 10. 2026):

| Vrstva | Kde je | Co v ní je (doklad) | Verdikt |
|---|---|---|---|
| **1 Zážitek** | `docs/GDD.md:50–81` (pilíře), `:85–128` (hlavní smyčka **8 vět** + pravidla A/B/C), `:116–124` (delší smyčky: sezení 30–60 min, meta bez konce), `:185–203` (**prvních 5 minut**, scénář), `:207–231` (ovládání: pravé tlačítko, vzdálenost kurzoru, stamina, mrtvá zóna, vyhlazení), `:235–255` (co je na obrazovce, UI) | smyčka je **seznam vět** (`GDD:87–100`), každá věta má zdroj `[U]`/`[D]`; „jak hráč pozná úspěch“ je `GDD:132–159` | **je tam** |
| **2 Míra úspěchu** | `docs/GDD.md:163–181` — `V1`–`V8`, každý bod s **důkazem** a s tím, **kdy musí platit**; `:179–181` „kdo celek vyhodnotí“ (uživatel hraním, agent měřením) | 8 měřitelných bodů (`V1` růst jako číslo … `V8` hru nejde zablokovat obchodem) | **je tam** |
| **5 Non-goals** | `docs/GDD.md:407–449` — `N1`–`N11`, každý s důvodem; navíc „co v dokumentu záměrně není“ v `GDD:496–509`, `TDD:789–802`, `ADD:376–392` | 11 výslovných zákazů (`N9` přeformulováno 9. 10. 2026, `GDD:432–446`) | **je tam** |

**Závěr:** tvrzení skillu je **vyvrácené pro dnešek** — a **ve svém čase správné**:
skill ho psal podle stavu před 8. 10. 2026 (kdy existoval jen `DESIGN.md`
a `ARCHITEKTURA.md`; `KONCEPT-PRIPRAVY-HRY.md:561` to formuluje jako úkol
„dopsat vrstvy 1, 2 a 5“). Dnešní text skillu je tedy **zastaralý záznam
v metodice**, ne popis hry. **Historické číslo se nepřepisuje** — správná oprava
je označit ho datem („stav před 8. 10. 2026“) a odkázat na `docs/GDD.md`.

> **Druhá, stejně zastaralá věta téhož skillu** (`SKILL.md:251`): „`uo-shadows`
> `tests/run_tests.gd` je **27 podmíněných kontrol**“. `AGENTS.md:80–83` a
> `docs/BRANY-HRY.md:90–93` přitom už 8. 10. 2026 zapsaly, že „27 podmíněných
> kontrol“ bylo **nepravdivé číslo** a správně je **28 řádků s `has_method`
> (41 výskytů)** — naměřeno mnou znovu: 28 / 41, v kódu bez komentářů 20 / 33.

---

## 2. Rejstřík vrstev `0`–`10`

**Jak číst:** „kde je dnes“ = soubor **a řádky**, kde vrstva skutečně bydlí
(u souborů v `docs/` čísluji řádky toho souboru). „Pokrytí“ hodnotím podle
KONCEPT §2 (co v ní musí být) a §7 (kontrolní seznam), ne dojmem.

| # | Vrstva | Kde je dnes (soubor:řádky) | Pokrytí | Co chybí | Kam to v nové verzi patří |
|---|---|---|---|---|---|
| **0** | Záměr | `docs/GDD.md:34–46` (cíl jednou větou + pro koho + cena) | **plné** | — | `GDD §0` beze změny |
| **1** | Zážitek | `GDD:50–81` (pilíře-pocity `P1`–`P5`), `GDD:85–128` (smyčka 8 vět + `A`/`B`/`C`), `GDD:116–124` (sezení/meta), `GDD:185–203` (prvních 5 minut), `GDD:207–231` (ovládání), `GDD:235–255` (UI) | **plné** | hodnoty mrtvé zóny a vyhlazení jsou vědomě otevřené (`GDD:223–226`, `O-4` na `GDD:516`); 8 směrů odloženo (`N-2`, `GDD:221`, `GDD:515`); rozložení lišty a panelů až k `M2`/`M4` (`ADD:309–310`) — to jsou **otevřené body, ne chybějící vrstva** | `GDD §1–§7` beze změny |
| **2** | Míra úspěchu | `GDD:163–181` (`V1`–`V8` + kdo vyhodnotí) | **plné** | — | `GDD §4` beze změny |
| **3** | Mechaniky | `GDD:315–375` (§9.1 růst/atrofie/synergie, §9.2 těžba/výroba/kvalita, §9.3 ceny/infestace/zásobenost, §9.4 boj/výbava/léčení) | **částečné** | **tři ROZHODNUTÉ náklady řemesla nemají vzorec ani číslo**: palivo, opotřebení nástroje, zmetkovost (`GDD:339–341` a `GDD:343–346`), přitom `TDD:410–412` výslovně říká „patří do vzorce a **musí mít svá čísla na jednom místě**“ — dnes nejsou nikde | `GDD §9.2` doplnit o vzorec/tabulku (a určit JEDNO místo pro ladicí hodnoty) — nebo je vědomě nechat na `M3` s poznámkou „hodnoty až při ladění“ (dnes chybí i ta poznámka u čísel) |
| **4** | Obsah | `GDD:379–403` (§10 obsah v číslech: 11 materiálů, 7 předmětů, 3 nestvůry, 8 receptů, 6 dovedností, mapa, délka sezení) + `TDD:547–571` (§4.1 datové soubory) | **plné** jako seznam; **data** chybí (to je práce, ne dokument) | `assets/data/synergies.json` **neexistuje** (`TDD:564`); data rozsahu `M` v `assets/data/*.json` nejsou (naměřeno: 5 souborů, 4/4/3/1/2 záznamů) | `GDD §10` = seznam a počty; **hodnoty jednotlivých záznamů** patří do `assets/data/*.json` (`GDD:505–507`) |
| **5** | Rozsah a non-goals | `GDD:407–449` (`N1`–`N11`) + `GDD:496–509`, `TDD:789–802`, `ADD:376–392` („co tam záměrně není“) | **plné** | „rozsah v číslech“ je v `GDD:379–403` (počty) ✔; **rozpočet na velikost světa chybí** a `TDD:665–667` to přiznává („číslo by bylo dohad“) | `GDD §11` + `GDD §10` beze změny; rozpočet světa až z měření `M2`/`M4` (`TDD:665–667`) |
| **6** | Technika | `TDD:30–52` (§0 rozhodnutí `R-1`,`R-2`,`R-3`), `TDD:56–149` (§1 tik/kořen/fronty), `TDD:152–179` (§2 vrstvy), `TDD:651–667` (§6 výkon), `TDD:671–693` (§7 chyby), `TDD:697–723` (§8 jazyk) | **plné** | **verze enginu a platforma nejsou v žádném dokumentu**: `project.godot:10` má `config/features=PackedStringArray("4.7")`, cesta k `4.7.2` je jen v `AGENTS.md:31` (nástroj stanice) a `export_presets.cfg` má **tři presety** (Windows `:18`, Web `:63`, Linux `:99`) — TDD je nejmenuje ani jedním slovem | `TDD §0` (nebo §6) doplnit **jednu větu**: „Godot 4.7.2-stable; export Windows/Web/Linux (`export_presets.cfg`); výstup `build/`“ — je to vrstva 6 podle KONCEPT přílohy B.1 |
| **7** | Smlouvy | `TDD:183–537` (§3, **18 smluv** s tvarem dat), `TDD:631–647` (§5 vlastnictví stavu), `TDD:620–628` (§4.4 kde je co) | **plné** | (a) **vlastník tiku/registru je v `TDD:646` `game.gd`**, ale měřeno ho vlastní `scripts/registry.gd` (`registry.gd:26 TICK_MS`, `:129 push_command`, `:141 push_event`) — viz `ROZPORY.md` `R9`; (b) **`registry.gd` není v žádné vrstvě** `TDD:154–163` ani jako smlouva; (c) `provides`/`consumes` v plánu = **0 z 21 granul** (naměřeno) → agent dostane smlouvu jen prózou promptu; (d) uzly/datové typy, které se nesmí měnit tiše: `TDD:541–628` je má, ale **plán je neopisuje** | `TDD §3` doplnit smlouvu **`Registry`** (`registry.gd`) a v `TDD:646` opravit vlastníka; `provides`/`consumes` do granul doplnit při příští editaci roadmapy (`NAVRH-ROADMAPY-M0-M6.md:212–213`) |
| **8** | Plán | `GDD:453–474` (§12 milníky `M0`–`M6` jako hratelné stavy + definice hotovo) + `.forge/roadmap.json` (21 granul) | **částečné** | roadmapa **nemá klíč `milestone`** (klíče granul: `acceptance`, `depends_on`, `done`, `done_note`, `id`, `kind`, `model`, `owns`, `prompt`, `size_lines`, `title`) a **neobsahuje žádnou granuli pro `M2`–`M6`** (měřeno: chybí `orders.gd`, `standing.gd`, `layers.gd`, `anim.gd`, `npc.gd`, `enemy.gd`, `skills.growth`, `content.m`); tabulky granul pro `M2`–`M6` existují **jen v `_analyza/NAVRH-ROADMAPY-M0-M6.md:115–160`** (což je záznam, ne plán) | `GDD §12` = milníky (beze změny); `.forge/roadmap.json` = granule **+ `milestone` u každé**; doplňování `M2`–`M6` má postup v `NAVRH-ROADMAPY-M0-M6.md:190–197` („plán se doplňuje z uzavřeného milníku“) |
| **9** | Brány | `docs/BRANY-HRY.md` (192 ř., detail) + `AGENTS.md:60–90` (souhrn) + `TDD:727–760` (§9) + `ADD:314–332` (§10) | **plné, ale na čtyřech místech** | tři chybějící brány jsou pojmenované v `TDD:750–760` (brána nad dokumentací; třetí stav `exit 2` = NEMĚŘENO; brána nad obsahem `assets/data/*.json`); kandidát na první dvě je `_analyza/over-dokumenty.py` (mimo `.forge/`, měřeno) | **`docs/BRANY-HRY.md` = jediné místo detailu**; `AGENTS.md` už dnes drží jen souhrn a odkaz (`AGENTS.md:88–90`) — tak to má zůstat; `TDD §9` a `ADD §10` mají být **odkazy + to, co se týká jich**, ne druhá tabulka |
| **10** | Pravidla a pasti | `CONVENTIONS.md` (284 ř., poučky pro agenta), `AGENTS.md` (171 ř., trvalá pravidla hry), `ZASTAVENO.md:63–70` (6 pastí), `TDD:764–785` (§10 známé vady), `BRANY-HRY.md:68–144` (slepá místa + „TIŠE PŘESTALA MĚŘIT“), `GDD:470–474` (**definice hotovo**) | **částečné — a bez jednoho místa** | (a) **definice hotovo bydlí v GDD §12** (design), ne v pravidlech; (b) pasti jsou na **pěti místech** a nikde není jejich rejstřík; (c) **typované lekce neexistují** (KONCEPT §6 a Z10 — `game-clone` jich má 162); (d) **„co tahle část NEudělala“ není nikde** (KONCEPT Z13 — u `uo-shadows` to je jeden z drahých nálezů); (e) **vlastník a režim údržby u dokumentů chybí** (KONCEPT §7 bod 21: „Je u každého dokumentu, KDO ho udržuje a kdy?“) | **bez nového souboru:** do `CONVENTIONS.md` přidat oddíl „Rejstřík pastí“ (8–10 řádků: odkazy na `ZASTAVENO §6`, `TDD §10`, `BRANY-HRY`, `CONVENTIONS §1`, `AGENTS §Co nikdy`) + do hlaviček dokumentů doplnit **vlastníka a režim údržby** (§7 níže); definice hotovo zůstává v `GDD §12` a `CONVENTIONS.md` na ni odkazuje |

### 2.1 Které vrstvy tedy „nemají domov“

Tvrzení v zadání znělo, že chybí vrstvy 1, 2 a 5. **Měření říká jiné tři věci** —
a je fér je oddělit:

| Kategorie | Vrstvy | Doklad |
|---|---|---|
| **Úplně chybí** (nikde ani zmínka) | **žádná z `0`–`10`** | všech jedenáct má v repu text; u `1`, `2`, `5` viz §1 |
| **Nemá JEDNO místo** (obsah je, ale je na 4–5 místech a kopie driftují) | **9 (brány)** a **10 (pravidla a pasti)** | brány: 4 tabulky (`AGENTS:65–71`, `BRANY-HRY:30–37`+`68–101`, `TDD:734–742`, `ADD:318–324`) — a **už se rozešly**: `BRANY-HRY:100` jmenuje `check-licence.py`, `ADD:348` píše, že neexistuje (`ROZPORY.md` `R4`); pasti: 5 míst, rejstřík chybí |
| **Má domov, ale naplněný jen zčásti** | **8 (plán)** — domov je `.forge/roadmap.json`, ale chybí `milestone` a celé `M2`–`M6`; **3 (mechaniky)** — tři rozhodnuté náklady bez čísel; **6 (technika)** — chybí verze enginu a platforma; **7 (smlouvy)** — chybí smlouva `Registry` a vlastník tiku | viz tabulka §2 |
| **Má domov, ale agent orchestry ho NEDOSTANE** | **všechny** | `.github/workflows/agent.yml:227` předává aideru jen `--read CONVENTIONS.md` + soubory granule (`--file`) + soubory závislostí (`--read`, `files-to-edit.mjs:69–83`); `--map-tokens 0` (`agent.yml:230`). **Naměřeno dřív (`KONCEPT:54–58`): „design hry (`docs/ARCHITEKTURA.md`, 25 kB) nedostal nikdy — žádná granule `docs/` nevlastní“** — a to platí i dnes: v `.forge/roadmap.json` **nemá `owns` ani jednu cestu do `docs/`** |

---

## 3. Duplicitní zdroj pravdy — kandidáti na sjednocení

**Kritérium:** totéž téma je na dvou a více místech **a kopie se už rozešly nebo
můžou** (u každého uvádím naměřený důsledek, ne dojem).

| # | Téma | Místo A | Místo B (+ C, D) | Naměřený důsledek duplicity | Návrh |
|---|---|---|---|---|---|
| **D1** | **Co která brána měří a kde má slepá místa** | `AGENTS.md:65–71` | `docs/BRANY-HRY.md:30–37`, `:68–101`; `TDD:734–742`; `ADD:318–324` | **rozešlo se:** `check-licence.py` (`BRANY-HRY:100`) vs „neexistuje“ (`ADD:348`); počty funkcí `57` (`BRANY-HRY:87`) vs `97` (`HANDOFF:196`); řádků `461` (`BRANY-HRY:139`) vs **468** (naměřeno) | **jeden zdroj detailu = `BRANY-HRY.md`**; ostatní jen odkaz + věta, co se týká jich (`AGENTS` to už tak má) |
| **D2** | **Počty testů a `has_method`** | `AGENTS.md:80–86` (28/41, 154/113) | `BRANY-HRY.md:88–97`; `TDD:742` | tři kopie téhož čísla; **dnes správně** (naměřeno: `has_method` 28 řádků / 41 výskytů, bez komentářů 20/33; `_check(` 155 výskytů = 154 volání + 1 definice; běh hlásí 113 kontrol), ale `CONVENTIONS.md:278–281` **zakazuje** čísla opisovat | **jedno místo s datem a zdrojem** (`BRANY-HRY.md`), ostatní odkaz — a změnit pravidlo v `CONVENTIONS §7` (viz `ROZPORY.md` `R16`) |
| **D3** | **Definice hotovo (4 podmínky)** | `GDD:470–474` | `TDD:22–23`; `.forge/roadmap.json` `_popis` (odstavec „POZOR: ‚sloučené' NENÍ totéž co ‚hotové'…“) | tři kopie; **zatím se nerozešly** (formulace je shodná) | ponechat jednu **závaznou** (`GDD §12`) a v ostatních jen odkaz — u `roadmap.json` stačí „viz `docs/GDD.md §12`“ |
| **D4** | **Milníky `M0`–`M6`** | `GDD:453–468` | `ADD:114–116`; `_analyza/NAVRH-ROADMAPY-M0-M6.md:100–160`; `.forge/roadmap.json` `_popis` | plán je **neodkazuje** (chybí `milestone`), takže „plán podle milníků“ je tvrzení bez měřitelné vazby (`ROZPORY.md` `R18`) | `GDD §12` = jediná definice milníku; plán dostane `milestone`; `ADD` jen odkaz (už dnes odkazuje `ADD:114`) |
| **D5** | **Čísla vzhledu** | `assets/spec.json` (strojová deklarace: `viewport`, `tile`, `role`, `vrstvy`, `gates`) | `ADD:32–45` (§1 tabulka) + `ADD:318–324` (tolerance bran znovu) + `BRANY-HRY:33` | `ADD:384–385` tvrdí, že ADD čísla **neopisuje** — a přitom je v §1 vypisuje; `spec.json _popis:26` navíc odporuje `spec.json paleta` (`ROZPORY.md` `R5`) | ponechat `spec.json` jako **jediný zdroj čísel**; v `ADD §1` přidat jednu větu „opis deklarace k 8. 10. 2026 — platí `spec.json`“ (nebo tabulku zkrátit na odkazy) |
| **D6** | **Pravidlo jazyka (`R-3`)** | `AGENTS.md:121–127` | `TDD:697–723`; `CONVENTIONS.md:269–274` (§6 „komentáře a texty v UI česky“); `GDD:517` (`O-5`) | čtyři místa; **všechna se shodují**, jen `AGENTS.md` **nemá výjimku** `O-5` (české klíče `tezba`, `kovani_mece` se nepřejmenovávají) → hrozí „oprava“ fungujících dat (`ROZPORY.md` `R23`) | výjimku doplnit do `AGENTS.md` jednou větou s odkazem na `GDD §14.1 O-5` |
| **D7** | **Seznam smluv (18)** | `TDD:183–537` (§3, dnešní stav) | `ARCHITEKTURA.md:134–153` (§2, historie, **tvar dat nemá**) | pojmenované jako historie (`ARCHITEKTURA:3–9`, `AGENTS:163`) — **drift neškodí**, ale `ARCHITEKTURA:137–138` žádá `get(attr)`/`get(skill)`, což Godot 4 **neumí** (`CONVENTIONS:111–125`) | ponechat jako historii; **nedávat do ní nic nového** (viz `ROZPORY.md` `R19`) |
| **D8** | **„Co hra je“ v jedné větě** | `GDD:34–38` | `AGENTS.md:101–102`; `docs/DESIGN.md:33–44` (zmrazené, jiná vize) | tři různé věty o téže hře — `DESIGN.md` je ale **označená historie** (`DESIGN.md:3–9`) | ponechat: souhrn v `AGENTS.md` je navigace, ne zdroj (a je označený jako „zdroj pravdy o designu = GDD“) |

---

## 4. Co je pokryté dobře a nemá se měnit

Aby se při přepisu nezničilo to, co funguje (a co jinde chybí):

1. **Vrstva 0 (záměr) a 1 (zážitek) — smyčka jako SEZNAM VĚT.** `GDD:85–100`:
   8 vět, každá označená `[U]` (uživatelova slova) nebo `[D]` (dotvořený krok),
   plus tři pravidla z krajních případů (`GDD:105–109`). Přesně tohle
   `game-clone` **sám vykazuje jako svou slabinu** (`KONCEPT:534–538`).
2. **Vrstva 2 — `V1`–`V8` s důkazem a s „kdy to musí platit“** (`GDD:168–177`).
   Je to jediná míra úspěchu, kterou projekt má; `KONCEPT:553–554` ji označuje
   za práci, kterou u původní hry **nikdo nemá hotovou**.
3. **Vrstva 5 — non-goals s DŮVODEM** (`GDD:411–423`), včetně `N9`
   přeformulovaného **doplňujícím zápisem, ne přepsáním** (`GDD:432–449`) —
   to je přesně vzor „co je záznam, se jen doplňuje“.
4. **Vrstva 7 — smlouvy s TVAREM DAT** (`TDD:192–200` vzor zápisu + 18 oddílů
   `§3.1`–`§3.18`). `ARCHITEKTURA.md` měl tvar dat u 3 z 18 (`TDD:186–190`),
   TDD ho má u 18 — **a každá smlouva má `acceptance`, které říká, co test
   ZAVOLÁ** (`TDD:199`). To je nejcennější část repa.
5. **Hlavičky `GDD`/`TDD`/`ADD`** (`GDD:3–30`, `TDD:3–26`, `ADD:3–26`):
   druh dokumentu + odkud brát stav + co v něm záměrně není + jak se mění.
   Tuhle osnovu **rozšířit na všechny dokumenty** (§6), ne ji měnit.
6. **Třetí stav brány `exit 2` = NEMĚŘENO** (`_analyza/over-dokumenty.py:44`,
   naměřeno: 97 OK / 0 FAIL / **0 NEMĚŘENO**) a sabotér (9/9 mutací,
   `HANDOFF:167`). Je to nejlepší brána nad dokumentací, kterou stanice má.

---

## 5. Návrh minimální změny struktury: varianta A vs. varianta B

**Zadání:** ne devět nových souborů, ale **každá vrstva jedno jasné místo**
a aby to agent našel.

### Varianta A — zachovat `GDD.md` / `TDD.md` / `ADD.md` + přidat mapu vrstev

**Co se udělá (4 kroky, žádný nový dokument):**
1. `AGENTS.md` §„Kam pro co“ (`AGENTS.md:154–171`) se rozšíří o **sloupec vrstvy**
   (a doplní chybějící řádky: `ZASTAVENO.md`, `HANDOFF.md`,
   `_analyza/DESIGN-REVIZE-2.md`, `assets/data/*.json`).
2. `CONVENTIONS.md` dostane **krátkou mapu vrstev** (10–15 řádků: vrstva → soubor §)
   — protože **jen tento soubor agent orchestry skutečně dostane**
   (`agent.yml:227`). Mapa je navigace; nese **jen cesty a §**, ne obsah
   (aby nevznikl druhý zdroj pravdy).
3. Všechny dokumenty dostanou **povinnou hlavičku** (§6) — tím je vrstva
   dohledatelná i bez mapy.
4. Doplní se tři dílčí místa bez domova: verze enginu + platforma do `TDD §0`,
   čísla tří nákladů do `GDD §9.2`, rejstřík pastí do `CONVENTIONS.md` (§2, řádek 10).

**Cena (naměřená):** **téměř nulová** — nic se nepřejmenovává, takže **žádný
odkaz nespadne**.
**Riziko:** mapa v `CONVENTIONS.md` a tabulka v `AGENTS.md` jsou dvě kopie →
můžou se rozejít. **Mitigace:** mapa v `CONVENTIONS.md` nese jen `vrstva → soubor`,
žádná čísla ani tvrzení; a `_analyza/over-dokumenty.py` (nebo jeho budoucí
nástupce v `.forge/`) dostane kontrolu „**každý soubor jmenovaný v rejstříku
existuje**“ (KONCEPT příloha B.4; vzor: `idle-realm` odkazoval na
`ROADMAP_OBSAHU.md`, který neexistuje).

### Varianta B — přejmenovat na číslované soubory (`01-cil.md` … `09-pravidla.md`)

**Co to rozbije (naměřeno, ne odhad):**

| Co | Kolik odkazů | Důsledek přejmenování |
|---|---|---|
| `.forge/roadmap.json` (prompty granul) | **10×** `docs/GDD.md`, **13×** `docs/TDD.md`, **1×** `docs/ADD.md`, 6× `CONVENTIONS.md` | prompty (text, který dostane agent) by odkazovaly na **neexistující soubory**; plán čte conductor přes GitHub API |
| `AGENTS.md` | 4× `docs/GDD.md`, 4× `docs/TDD.md`, 2× `docs/ADD.md` (+ tabulka „Kam pro co“) | trvalá pravidla hry by ukazovala na mrtvé cesty — a to je soubor, který dostane **každá DSH session** |
| `_analyza/over-dokumenty.py` | `DEFAULT_DOCS` na `:54` a `REVIZE` na `:55` | brána nad dokumentací by přestala měřit (nebo hlásila `NEMĚŘENO`) — dnes 97 OK / 0 FAIL |
| `docs/*.md` (křížové odkazy) | `GDD.md` 10 zmínek, `TDD.md` 8, `ADD.md` 13, `DESIGN.md` 8 (obě formy — `docs/X.md` i `X.md`) | včetně hlaviček „nahrazeno `docs/TDD.md`“ — ty **se nesmí přepsat** (jsou to záznamy) |
| **Záznamy, které se needitují** | `HANDOFF.md` **23** zmínek, `ZADANI-GDD-ADD-TDD.md` **16**, `ZASTAVENO.md` **10**, `_analyza/NAVRH-ROADMAPY-M0-M6.md` **8** (dohromady **57**) | 57 odkazů v souborech, kde pravidlo stanice říká **„co je záznam, se jen doplňuje, nepřepisuje“** → po přejmenování by záznamy navždy odkazovaly na soubory, které nejsou |
| **Jiný repozitář (orchestra)** | `tools/over-dokumentaci.py:28` (`BRANY_HRY = HRA / "docs" / "BRANY-HRY.md"`), `tools/over-skilly.py:90` | dvě brány orchestry by spadly na „soubor neexistuje“ — mimo tenhle repozitář |
| `docs/BRANY-HRY.md` (obsah je pinovaný) | `over-dokumentaci.py:197–211` a `:393–397` vyžaduje 13 konkrétních textů | přejmenování souboru bránu shodí ještě dřív, než se řeší obsah |

**Přínos B:** jméno souboru řekne vrstvu a pořadí (to je reálná výhoda pro
člověka i pro agenta). **Cena B:** **57** odkazů v záznamech (nepřepisovatelných),
**30** odkazů v plánu, 1 brána v repu, 2 brány v orchestraci.

### Doporučení: **varianta A**

**Proč:** B kupuje čitelnost jména za cenu, která padá **na záznamy a na plán** —
tedy na věci, které se podle pravidel stanice nesmí přepisovat, a na brány
v cizím repu. A navíc **B neřeší hlavní problém**: že agent orchestry dokumenty
**vůbec nedostane** (`agent.yml:227`) — po přejmenování by je nedostal pořád.

**Co k tomu patří (a je to mimo dokumenty):** aby mapa vrstev měla smysl,
musí se změnit **předání**, ne struktura: buď `agent.yml` předá `--read`
`docs/TDD.md` (nebo jeho oddíl), nebo se smlouva vloží **do promptu granule**
(plán to deklaruje — `roadmap.json` `_popis`: „PROMPT SE GENERUJE ZE SMLOUVY
v `docs/TDD.md` §3“ — ale u `ui.hud`, `world.nodes` a `sim.mining` to **není
pravda**, naměřeno v `ROZPORY.md` `R10`–`R12`). To je změna orchestrace
(`E:\Workspaces\forge-orchestra`), tedy **jiné repo** — tady ji jen pojmenovávám.

---

## 6. Povinná hlavička každého dokumentu (návrh)

**Proč:** dnes má plnou hlavičku jen `GDD`/`TDD`/`ADD`; `CONVENTIONS.md` **nemá
hlavičku vůbec** (začíná větou „Tenhle soubor je **jen ke čtení**…“) a
`BRANY-HRY.md` nemá datum ani režim údržby. Důsledek je naměřený: ve workspace se
sejde víc dokumentů a každý tvrdí jiný „dnešní stav“ (skill `dokumentace` §1).

**Povinné položky (v tomto pořadí):**

```
> **Co tenhle dokument JE:** <druh> — <jedna věta, co v něm je>.
> **Čím je:** zadání / snapshot / záznam o provedení / stav / plán / kronika / rejstřík.
> **Odkud brát současný stav:** <soubor, který je dnešní stav — NE tenhle dokument>.
> **Platí z něj:** <co z něj platí dnes>; **datum spotřeby:** <kdy/čím se spotřeboval>.
> **Vzniklo:** <datum> <kdo>. **Vlastník a údržba:** <kdo ho udržuje a kdy>.
> **Jak se mění:** stav = přepisuje se celý · záznam = jen se doplňuje · kronika = nikdy.
```

**Tabulka stavu (naměřeno):**

| Dokument | Druh | Hlavička dnes | Co chybí |
|---|---|---|---|
| `docs/GDD.md` | stav (zdroj pravdy o designu) | `GDD:3–30` — je, odkud brát stav, „jak se mění“ | **vlastník a režim údržby** |
| `docs/TDD.md` | stav (technika) | `TDD:3–26` — plná | datum spotřeby u naměřených čísel (má je u čísel, ne v hlavičce) |
| `docs/ADD.md` | stav (vzhled) | `ADD:3–26` — plná | vlastník |
| `docs/BRANY-HRY.md` | **znalost a naměřené případy** | `BRANY-HRY:3–9` — „co je“ + „odkud brát stav“ | **datum vzniku, datum měření, vlastník, režim údržby** |
| `docs/DESIGN.md`, `docs/ARCHITEKTURA.md` | **historie (needituje se)** | `DESIGN:1–15`, `ARCHITEKTURA:1–13` | obojí má „nahrazeno“, ale **tělo si dál hraje na autoritu** (`ROZPORY.md` `R19`, `R20`) |
| `AGENTS.md` | trvalá pravidla hry | `AGENTS.md:3–21` | datum poslední změny + vlastník (dnes jen „vznikl 4. 10. 2026“) |
| `CONVENTIONS.md` | poučky pro agenta (dodávané přes `--read`) | **žádná hlavička** | **všechno**: čím je, odkud brát stav, datum, vlastník, jak se mění |
| `ZASTAVENO.md` | záznam o zastavení | `ZASTAVENO.md:3–8` — plná | vlastník (kdo doplňuje) |
| `HANDOFF.md` | záznam předání | `HANDOFF.md:3–18` — plná | — |
| `.forge/roadmap.json` | **plán (strojový)** | `_popis` (25 řádků) — čím je + změny | chybí **datum poslední změny a `milestone` u granul** |

**Navíc (KONCEPT §7, body 21–25):** u každého dokumentu musí být **vlastník**
(bod 21), u odloženého tématu **proč a co ho vrátí** (bod 23), zápis stavu
**vynucený krokem** (bod 24) a u hotové části **„co tahle část NEudělala“**
(bod 25). Dnes je z toho splněné jen „proč a co ho vrátí“ (`GDD §14.1`,
`ZASTAVENO §4`, `HANDOFF` „Deferred“).

---

## 7. Co jsem nepřeměřil (meze tohohle návrhu)

- **Nespouštěl jsem Godot** (hra je zastavená, zadání to nevyžadovalo) — čísla
  o testech jsou z **běhu zaznamenaného v `HANDOFF.md:168`** (`[test] 113 kontrol,
  0 selhání`) a z **výstupu `check-wiring.py`, který jsem spustil** (97/16, `exit 0`).
- **Nečetl jsem orchestraci do hloubky** — jen dvě místa, kde sahá na dokumenty
  hry (`over-dokumentaci.py:28,197–211,393–397`, `over-skilly.py:90`).
- **Neposuzuji, které z otevřených bodů (`O-2`, `O-4`, `O-5`) se mají dořešit** —
  to je rozhodnutí uživatele, ne agenta (`KONCEPT §10.1`).
- **Číslo „16 `.md` / 58 081 slov“ (`ZASTAVENO:38`) jsem nepřeměřoval na shodu** —
  bez uvedeného postupu (co se počítá) se reprodukovat nedá; dnes je `.md` **17**
  (bez souborů této session) a to je jiná otázka než „kolik jich bylo 12. 10.“.
