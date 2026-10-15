# GDD — `uo-shadows`: co hra je a jak se hraje

> **Co tenhle dokument JE:** **zdroj pravdy o designu hry** (game design
> document). Říká, co hra je, jak se hraje, jaké má mechaniky s čísly a co v ní
> **záměrně není**.
>
> **Platí z něj:** co je v tomhle dokumentu, **platí** — je to **zdroj pravdy
> o designu**; `TDD`, `ADD` i `BRANY-HRY` na něj **odkazují a neopisují ho**.
> Kde GDD tvrdí něco o **kódu** a měření ukáže opak, platí **měření** (kód je
> realita) — text se pak označí datem, nepřepíše se potichu.
>
> **Nahrazuje `docs/DESIGN.md`** jako zdroj pravdy. `DESIGN.md` zůstává v repu
> jako **historie** (sám se hlásí jako zrušený) a needituje se.
>
> **Odkud brát stav:** tenhle dokument je stav designu. **Zdroj rozhodnutí** je
> `_analyza/DESIGN-REVIZE-2.md` — uzavřená revize vize (5 kol dialogu
> s uživatelem, 8. 10. 2026). Každé rozhodnutí tady má odtud zdroj; odkazy
> `(§N)` míří do `DESIGN-REVIZE-2.md`. Technický stav je v `docs/TDD.md`
> a v `.forge/roadmap.json`, vzhled v `docs/ADD.md`.
>
> **Datum spotřeby:** design v GDD **nezaniká commitem**; čísla o **kódu** jsou
> měření k **15. 10. 2026** (`HEAD = 6986b0d`) a po dalším commitu se **přeměří,
> ne opíšou** (postupy a naměřené hodnoty: `_analyza/PRACE-2026-10-15/FAKTA.md`).
> Starší čísla nesou značku **„ve svém čase správná“**.
>
> **Vlastník a údržba:** o designu rozhoduje **uživatel**; text GDD udržuje
> **agent** — smí ho přepisovat, ale **jen podle rozhodnutí**, nikdy vlastním
> nápadem. Co rozhodnuté není, patří do §14.1 (otevřené body), ne do textu.
>
> **Vzniklo:** 8. 10. 2026 sepsáním z `_analyza/DESIGN-REVIZE-2.md` (zadání
> `ZADANI-GDD-ADD-TDD.md`). **Nic tady není domyšlené** — co rozhodnuté není,
> je v §14 jako otevřený bod.
>
> **Co tenhle dokument NENÍ:** není technický návrh (to je `docs/TDD.md`), není
> art bible (to je `docs/ADD.md`) a není plán práce (to je `.forge/roadmap.json`).
>
> **Jak se mění:** GDD je **stav** — přepisuje se celý, když se změní rozhodnutí.
> **Ceny rozhodnutí a historie dialogu se needitují** — ty zůstávají
> v `DESIGN-REVIZE-2.md`. Když se GDD a `DESIGN-REVIZE-2.md` rozejdou, **platí
> GDD** (je to dnešní stav) a `DESIGN-REVIZE-2.md` je záznam, jak k němu došlo.
>
> **Značky zdrojů v tomhle dokumentu:** `§N` = `_analyza/DESIGN-REVIZE-2.md`
> oddíl N · `VSTUPY §N` = `_analyza/DESIGN-PRACOVNI-VSTUPY.md` · `spec.json` =
> `assets/spec.json` · `kód` = měřeno v repu (u čísel je řečeno, čím).

---

## 0. Záměr jednou větou — a pro koho hra je

> **Živý izometrický sandbox, ve kterém si hráč vybere roli — řemeslník,
> obchodník, válečník, dobrodruh nebo hraničář — roste v ní tím, co dělá,
> a svět na jeho práci viditelně reaguje.** (§2)

**Pro koho:** pro hráče, který chce mít v herním světě **svou roli a svůj
přínos** — ne být vyvoleným hrdinou. (Odvozeno z uživatelova textu, `VSTUPY`
§1.3; potvrzeno `K2` „Sedí“.)

**Cena (co tím ztrácíme):** záměr je **filtr**. Co neposiluje „roli, která roste
a kterou svět potřebuje“, do hry nepatří — hra nebude o hrdinovi, který zachrání
svět, a nebude mít konec. (§2, `VSTUPY` §1.6)

---

## 1. Pilíře jako POCITY (rozhodovací pravidla, ne hesla)

Sedm „pilířů“ v `docs/ARCHITEKTURA.md:19–27` jsou **featury** („synergie skill +
atribut“) — nedají se použít jako rozhodovací pravidlo. Platí proto **pět
pocitů**, každý s tím, co znamená pro rozhodnutí a **co vylučuje**. (§3)

| # | Pilíř (pocit) | Co znamená pro rozhodnutí | Co vylučuje |
|---|---|---|---|
| **P1** | **„Mám svou roli a svět ji potřebuje.“** | Co posiluje, aby každá z pěti rolí měla co nabídnout, je v duchu hry | Příběh „vyvoleného“, kde je hráč střed světa a ostatní profese jsou kulisa |
| **P2** | **„Rostu tím, co dělám — a je to vidět.“** | Pokrok musí být vidět **v číslech** (úspěšnost, zranění, kvalita, konzistence), ne v odznaku | Dovednosti rostoucí za něco jiného než za své použití; „pocit pokroku“ bez měřitelné změny |
| **P3** | **„Dovednosti se potkávají, ne soupeří.“** | Vazby mezi dovednostmi jsou součástí designu (kladivo → tupé zbraně; znalost kovů → tinkering) | Pevné třídy a povolání, které kombinace zamknou; dovednosti, které spolu nesmí mluvit |
| **P4** | **„Každý stupeň umí něco — a mistr umí víc.“** | I začátečník musí mít co dělat a vydělat; zároveň musí být poznat rozdíl proti mistrovi | Obsah, který dá začátečníkovi nulu; a obsah, kde je mistr zbytečný |
| **P5** | **„Co udělám, je ve světě vidět.“** | Odměna se musí dát **uplatnit** a svět musí zareagovat (ceny, zásobenost, bezpečí) | Odměny bez odběratele a svět, který se nemění |

**Cena:** pilíře nejsou práce, jsou to **filtry** — každý navíc umí zablokovat
i dobrý nápad, proto jich je pět, ne deset. **Bez nich:** každá další session si
domyslí, „co je v duchu hry“, a dva návrhy se budou hádat bez rozhodčího. (§3)

### 1.1 Hlavní pilíř je `P2` — rozhodčí při sporu

Když si dva nápady odporují, **vyhrává ten, který víc zviditelní měřitelný
růst** (§3, rozhodnutí uživatele `K2`). Co z toho plyne konkrétně:

- hra musí **brzy ukazovat čísla** — dnešní HUD umí jen `Skóre: 2 / 2`, takže
  „růst je vidět“ dnes **nemá kde být vidět** (§1, `kód`: `scripts/game.gd`;
  naměřeno 15. 10. 2026 čtením `game.gd`: na obrazovce je `Label` s textem
  `Skóre: %d / %d` — na mapě jsou **2** coin markery, takže ukazuje `2 / 2`);
- „pocit pokroku“ bez čísla je **proti hlavnímu pilíři**, i kdyby se líbil;
- platí to i na `P5`: vliv na svět se musí projevit **jako číslo nebo stav**
  („vesnice je zásobenější“ musí být vidět), ne jako dojem.

**Cena:** `P2` tlačí na **měřitelnost už v prvním hratelném stavu** (HUD, čísla
dovedností, viditelný stav světa) a omezuje „náladové“ prvky, které se číslem
doložit nedají. (§3)

---

## 2. Hlavní smyčka — osm vět

`[U]` = uživatelova slova, `[D]` = dotvořený krok (potvrzený). (§4)

1. **[U]** Vyberu si, co mě baví — roli a směr; a vidím, **co svět potřebuje**
   (kovárna chce rudu, vesnice chce zbraně).
2. **[U]** Vypravím se za tím: těžím, kácím, lovím, prozkoumávám, čistím.
3. **[U]** Přinesu, co jsem získal — suroviny, kořist, zboží z výprav.
4. **[U]** Zpracuji to: tavení, kování, výroba, oprava — a použiji na sobě
   (výzbroj, výstroj).
5. **[U]** Uplatním výsledek: **prodám, předám, spotřebuji**.
6. **[U]** Svět na to zareaguje **viditelně** — ekonomika se pohne, stav světa
   se změní (zásobenost, infestace, odolnost komunity).
7. **[D]** Za svou práci dostanu odměnu **a roste mi dovednost** — měřitelně.
8. **[D]** Příští výprava je proto o něco lepší a svět má zase novou poptávku;
   smyčka se opakuje.

**Tři pravidla, která do návrhu smyčky přidaly krajní případy** (stres test,
8. 10. 2026 — uživatel místo převyprávění odpověděl na tři krajní situace; §4):

| # | Pravidlo | Co to znamená |
|---|---|---|
| **A** | **Těžba má hloubku** | Zdroj má **obsah** (běžná + vzácná složka) a **trvání**; delší těžba se vyplácí. A i bez uplatnění roste dovednost → **smyčka není blokovaná obchodem**; kdo jen těží, není v slepé uličce. |
| **B** | **Poptávka světa je tříděná a mění se** | Předpoklad „svět má vždycky poptávku“ **neplatí**. Věci jsou **odpad** (nikdo ho nechce), **recyklovatelné** (dá se vrátit do výroby) a **situační** (chce se to jen za nějaké situace, např. když roste infestace). Poptávka se navíc **mění v čase**. |
| **C** | **Hnací silou je cíl s číslem** | Ne jen „svět má novou poptávku“, ale **cíl s číslem** („100 dávek lektvaru“). **Kdo cíl zadává — rozhodnuto:** **oba** — svět zadává **zakázky** a hráč si může dát **vlastní cíl** (počítadlo); jdou vedle sebe, ne proti sobě. (§12.1) |

**Příklady obsahu smyčky jsou jen příklady.** Uživatelův vlastní příklad cíle
(„100 dávek lektvaru“) **není v MVP splnitelný**, protože lektvary jsou mimo MVP
(`R2-3`, §12.3 `N11`) — nahrazuje se něčím, co v MVP je (např. „100 ingotů“,
§12.2 `V7`).

### 2.1 Delší smyčky: sezení a meta

- **Sezení (30–60 min, rozsah `M`, §12.5):** hráč stihne jednu až dvě výpravy,
  zpracování a dodávku; na konci sezení musí být vidět **aspoň jedno číslo,
  které se pohnulo** (dovednost, zásobenost, infestace, stav účtu — `P2`).
- **Meta (bez konce):** hra **nemá konec** (`VSTUPY` §1.6). Dlouhodobý cíl je
  **růst dovedností** (0→100), **uznání od světa** (GDD §8.2) a **vlastní cíle
  hráče**. Mistrovství je „běh na dlouho“ — na 90→100 se podle návrhu tempa
  spotřebuje 10 h+ herního času (`§13.6` `M6`, předsada `normalni`).

**Cena smyčky:** 8 vět = **8 systémů, které se musí potkat**. Dokud jedna věta
nefunguje celá, hra není hotová — i kdyby všechno ostatní klapalo. Kratší smyčka
by byla rychlejší, ale hůř by udržela pocit živého světa. (§4)

---

## 3. Jak hráč pozná úspěch

Úspěch nemá jedno číslo. Pozná se na **třech místech** (§5, rozhodnutí `K4`
„Od každého kousek — strop i možnosti“):

1. **V číslech** — úspěšnost zásahu, zranění, doba přežití, kvalita, ztrátovost,
   konzistence.
2. **V nových možnostech** — co mistr umí a začátečník **vůbec ne** (modifikace
   produktu, ochočení zvířete).
3. **Ve světě** — co je díky mně lepší (zásobenost, bezpečí, ceny).

**„Vyšší potenciál“ = vyšší STROP i ODEMČENÉ MOŽNOSTI** (varianty (a) + (c)):

- **strop:** s rostoucí dovedností a lepším vybavením roste **horní mez**
  (max. zranění, max. kvalita, max. konzistence) — mistr není jen rychlejší,
  ale **dosáhne výš**;
- **možnosti:** na určitých stupních se **odemykají akce, které začátečník nemá
  vůbec** (modifikace produktu, ochočení a šlechtění zvěře).

**A třetí složka (rozhodnutí `R2-5` „I uznání od světa“):** mistrovství se pozná
také podle toho, že **svět na mistra reaguje** — lepší zakázky, jiné ceny, titul
na obrazovce (GDD §8.2, zdroj rozhodnutí `§13.4`).

**Cena:** jsou to **dva mechanismy místo jednoho** — strop se ladí čísly,
odemykání je **obsah k postavení** (každá odemčená možnost musí existovat
i pro toho, kdo ji nemá: musí být vidět, že na ni nemá). Varianta „jen strop“
by byla levnější, ale zmizel by kvalitativní skok, který dělá mistrovství
„rewarding“. (§5)

---

## 4. Míra úspěchu `V1`–`V8` — čím se pozná, že hra funguje

**Jak to číst:** každý bod je tvrzení, které se dá **ověřit** — na obrazovce
nebo měřením. Co ověřit nejde, není míra úspěchu, ale přání. (§12.2)

| # | Co to znamená | Jak se to pozná (důkaz) | Kdy to musí platit |
|---|---|---|---|
| **V1** | **Růst je vidět jako číslo** — dovednost má hodnotu viditelnou ve hře | hráč ukáže dvě čísla z různých časů a jsou jiná | MVP |
| **V2** | **Růst mění výsledek**, ne jen číslo | stejná akce se dvěma hodnotami dovednosti dá **prokazatelně jiný výsledek** (výnos, kvalita, úspěšnost) | MVP |
| **V3** | **Mistrovství odemyká nové možnosti** | ve hře je akce, kterou začátečník **nemá** — a je vidět, že na ni nemá | po MVP |
| **V4** | **Těžba má hloubku** (směs) | dva různě dlouhé zásahy do téhož zdroje dají **jiný obsah** | MVP |
| **V5** | **Uplatnění je vidět na světě** | stav světa je na obrazovce a po dodávce se **změní číslo** | MVP |
| **V6** | **Poptávka je tříděná a mění se** | táž věc má v různých situacích jinou cenu/poptávku (odpad / recyklovatelné / situační) | po MVP |
| **V7** | **Cíl s číslem existuje** | zakázku světa jde splnit a je vidět postup | zakázka v MVP, vlastní cíl později |
| **V8** | **Hru nejde zablokovat obchodem** | kdo jen těží a vyrábí, roste dál a není v slepé uličce | MVP |

**Kdo celek vyhodnotí:** uživatel hraním (`V1`, `V4`, `V5`, `V7`, `V8`) a agent
měřením (`V2` je test: dvě hodnoty dovednosti → jiný výsledek). Body, které nejde
vyhodnotit, se do seznamu nepíšou. (§12.2)

---

## 5. Prvních 5 minut (scénář prvního hratelného stavu)

Scénář je závazný jako **definice „hra funguje“ pro první hratelný stav**;
potvrzeno uživatelem (`R2-4` „Sedí“). (§12.4)

1. Hráč se objeví ve **vesnici** (dlaždice + postava + ukazatel stavu, na kterém
   je i **číslo dovednosti** — protože hlavní pilíř je `P2`).
2. Najde **zdroj rudy** (viditelný objekt), drží u něj pravé tlačítko a těží.
   Za pár vteřin má rudu a **číslo dovednosti těžby se pohnulo** (`V1`).
3. U pece **vytaví ingot**, u kovadliny **uková meč** — a vidí, že kovářství roste.
4. Svět mezitím ukazuje, **co potřebuje** (zakázka: „kovárna chce 3 ingoty“) —
   hráč dodá a **stav světa se viditelně změní** (`V5`).
5. **Cíl prvních 5 minut:** hráč projde celý cyklus *získat → zpracovat →
   uplatnit → vidět změnu* a uvidí **aspoň dvě čísla, která se pohnula**.

**Cena:** dnešní mapa má **2 mince a žádný zdroj rudy** — „prvních 5 minut“ tedy
znamená postavit vesnici, zdroje, pec, kovadlinu, HUD s čísly a stav světa.
(naměřeno 15. 10. 2026 v `assets/levels/main.json`: markery jsou **4** —
`spawn` 1, `coin` **2**, `exit` 1; zdroj surovin tam není. Uzly surovin má nést
granule `world.nodes`, ale její `scripts/world.gd` je **0 B**.)
Je to **největší jednotlivý kus práce z celé revize** — a zároveň **první věc,
která má být vidět na obrazovce**. (§12.4, §12.7 `R2-4`)

---

## 6. Ovládání

**Rozhodnuto** (`K5` „Souhlas“, §6 `K5`; odvozeno z `VSTUPY` §1.2 a §2.3):

| Prvek | Jak to je |
|---|---|
| **Pohyb** | **Držení PRAVÉHO TLAČÍTKA myši = jdu.** Vzdálenost kurzoru od postavy určuje **jak rychle**: těsně u postavy = stojím, dál = pomalá chůze / chůze / běh. |
| **Stamina** | Omezuje **běh** —běh ubírá staminu, vyčerpaný hráč zpomalí. |
| **Toggle** („jdi stále“) | **Až později** — v MVP není. |
| **Záložní cesta** | **WASD/šipky** zůstávají (pro testování, nestojí nic). |
| **Mrtvá zóna** | Kolem postavy je **mrtvá zóna**, aby postava nekmitala, když kurzor stojí na ní. |
| **Vyhlazení** | Rychlost **neskáče** — rozběh a zastavení musí ladit se vstupem. Měří se **číslem**: doba do plné rychlosti a doba do zastavení (v ms). |
| **Mřížka** | Svět zůstává **dlaždicový** — dlaždice určují, kudy se dá jít, a kreslí se po nich. **Plynulá je POSTAVA po nich, ne mřížka** (pozice je spojitá, ve světových souřadnicích). |
| **Kolize** | Objekty se **nesmí překrývat**; hloubkové řazení je spojité (ne celá čísla), jinak bude postava „na střeše“. |
| **Směry** | Prototyp zůstává u **4 směrů**; **osm směrů se rozhodne, až bude vidět pohyb** (`N-2` „Až po prototypech“). Kdyby se pro 8 směrů rozhodlo později, je to **2× obrázků na každý kus výbavy** (dnes 32 → 64 na kus; naměřeno 15. 10. 2026 v `assets/spec.json`: role `player` má **4 směry × 8 framů = 32** obrázků na vrstvu). |

**Co v této sekci NENÍ rozhodnuté:** konkrétní hodnoty mrtvé zóny a vyhlazení
(poloměr v px, doba náběhu v ms). Rozhodnutý je **požadavek, že jsou měřitelné
číslem**; hodnoty patří k ladění (`VSTUPY` §2.3). Neladí se ale „podle dojmu“ —
`P2` platí i tady.

**Proč na tom záleží pro plán:** plynulý pohyb znamená předělat pohyb, kolize
i řazení hloubky (dnes se postava hýbe po krocích po dlaždicích a řadí se celými
čísly). V prototypu z primitiv je to levné — drahé by bylo dělat to až
s hotovou grafikou. (§6 `K5`)

---

## 7. Co je na obrazovce (UI)

**Rozhodnuto** — uživatelova odpověď na „co je na obrazovce“ (`VSTUPY` §1.5):
*„Herní okno, rychlý náhled do paperdoll, rychlý přístup do inventáře, mapa.“*
S rozpadem na MVP (§14.1):

| Prvek | V MVP? | Poznámka |
|---|---|---|
| **Herní okno** (izometrická scéna, 960×540) | **ano** | rozměr je deklarovaný v `spec.json` (`viewport`) |
| **Ukazatel stavu s čísly** | **ano** | `P2`: dovednosti, HP, zlato — bez čísel není „růst je vidět“ kde vidět |
| **Stav světa** (infestace, zásobenost 0–100) | **ano** | `V5` — po dodávce se musí změnit **číslo na obrazovce** |
| **Zakázky světa** (cíl s číslem + postup) | **ano** | `V7` |
| **Inventář** | **ano** | „rychlý přístup“; **obvaz se použije kliknutím v inventáři** (§14.2) |
| **Mapa** | **ano** | uživatelův požadavek (`VSTUPY` §1.5) |
| **Paperdoll** (náhled postavy) | **NE — až s vrstvenou grafikou** | rozhodnutí `N-9` „Až s vrstvenou grafikou“; do té doby hráč vidí výbavu jen v inventáři a na postavě ve hře |

**Dnešní stav (naměřeno 8. 10. 2026, §1):** na obrazovce je **`Label` se skóre
`Skóre: 2 / 2`** a nápověda, která **inzeruje 6 kláves** (`E, C, B, X, R, M`),
**které kód neobsluhuje**. `hud.gd` existuje, ale **hra ho neinstancuje** —
v produkční cestě nejsou HUD, boj, výroba, ekonomika ani ukládání. Rozdíl proti
téhle sekci je tedy **celý**.

**Přeměřeno 15. 10. 2026 — sedí beze změny** (postup: čtení `scripts/game.gd`,
`scripts/player.gd` a `project.godot`): nápověda je v `game.gd` text
`E těžba rudy, C tavení, B kování, X použít zbraň, R oprava, M hudba` (tedy
**6** kláves) a `Input.` se v celém `scripts/` vyskytuje **jen** v `player.gd` —
naměřeno extrakcí volání `Input.` ze `scripts/`: **8 volání** (`KEY_W/A/S/D`
a `KEY_UP/DOWN/LEFT/RIGHT`); `project.godot` nemá ani
jednu `input/*` akci (sekce `[input]` obsahuje jen `input_devices`), `[autoload]`
tam **není**. Do produkční cesty (`main.tscn` → `game.gd` → `load()`) vedou
**jen** `scripts/level.gd` a `scripts/player.gd` — `hud.gd` se nenačítá
(v `game.gd` je `hud` jen `Label`). (`FAKTA.md` #13, #29, #66–#68.)

---

## 8. Svět a ostatní hráči

**Rozhodnuto (cesta `A` + architektura připravená na `B`, §11):**

| Cesta | Co to je | Stav |
|---|---|---|
| **A — solo + simulovaný svět** | svět se hýbe sám podle pravidel, hraješ sám | **TOTO JE MVP.** Žádný server. |
| **B — solo, ke kterému se přidá 2–4 hráči** | svět běží u hostitele; svět žije, dokud hostitel hraje | **otevřená jako samostatný milník**, ne zamítnutá; potřebuje architekturu připravenou od začátku + malou trvalou službu (prohlížeč neumí naslouchat na síti) |
| **C — persistentní sdílený svět (MMO)** | sdílený stav, příspěvky se sčítají | **odloženo**, dokud `A` nefunguje |

**Proč ne rovnou síť (dva důvody, oba z rozhodnutí):** (1) **ekonomické to
není** — síťová vrstva je samostatný milník **a k tomu trvalá služba**;
(2) **co-op se nedá ověřit bez druhého hráče** — a uživatel sám řekl, že hráče
nesežene. Postavit vrstvu, kterou nemá kdo vyzkoušet, znamená stavět naslepo.
(§11)

**Co je tím závazné pro architekturu (a patří do `docs/TDD.md`):** simulace
**oddělená od zobrazení** (pevný tik, stav jako data, příkazy a události místo
přímých volání). Kdyby se oddělení porušilo, `B` by znamenalo **přepis jádra**.
(§11, §14.1 `R-1`)

### 8.1 Stav světa (co hráč vidí, že se mění)

**Dvě čísla 0–100** (rozhodnutí: „Sedí — infestace + zásobenost, ceny z nich“,
§13.1):

- **infestace** — roste časem a klesá zásobeností;
- **zásobenost** — roste dodávkami a klesá spotřebou;
- **ceny jsou důsledek** těchto dvou čísel, **ne třetí stav**.

**Infestace je jen STAV SVĚTA, ne bojová aktivita** (rozhodnutí `R2-2`):
hráč ji neutlačuje bojem, ale **ekonomikou** (dodávkami). Dungeony a šlechtění
zvěře jsou **později**. (§12.7 `R2-2`)

### 8.2 Uznání od světa (jak svět pozná mistra)

Svět má mít na hráče **„názor“**. Počítá se z **trojice kritérií** (rozhodnutí
`M8` „Trojice kritérií“, §13.4):

1. **nejvyšší dovednost hráče**,
2. **počet splněných zakázek**,
3. **průměrná kvalita dodávek**.

**Efekt:** větší zakázky, lepší ceny a **titul na obrazovce**. **Cena:** čím víc
kritérií, tím hůř se to vysvětluje hráči — musí být vidět, **proč** mě svět bere
vážně. (§13.4, §13.6 `M8`)

---

## 9. Mechaniky a startovní čísla

**Všechna čísla v téhle sekci jsou „startovní“ — k ladění, ne k víře.** Jejich
hodnota není v tom, že jsou správná, ale že **existují a dají se měnit na jednom
místě**; bez nich si každá komponenta vymyslí vlastní. Co je už v kódu nebo
v roadmapě, se **nepřepisuje**, jen se přebírá. (§13.3)

### 9.1 Růst dovedností, atrofie, synergie

| Mechanika | Rozhodnutí / vzorec | Zdroj |
|---|---|---|
| **Růst** | `+1` bod se **pravděpodobností `(100 − dovednost)/100`** (na 0 skoro vždy, na 90 v 10 % případů). Do 100, **bez celkového stropu**. | §13.3, `roadmap.json` (`REQ-skills`) |
| **Tempo růstu** | **Parametr s předsadami:** `ladici` (mistrovství v minutách — aby se dalo ladit hned), `normalni`, případně `pomala`. Přepínač mění **jen tempo dalšího růstu**; už rozdané body se nemění. | §13.7 `M6` |
| **Atrofie** | Mechanika **bude hotová, ale vypnutá** („přepínač — zapnout po prvním ladění“). | §13.1 |
| **Synergie** | Vedlejší dovednost roste **~20 % tempa** té hlavní. Je znát, ale **není povinná** — hráč nemusí kombinovat, jen může (duch `P3`). | §13.1 |

**Dvě pasti, které jsou součástí rozhodnutí (a musí se hlídat):**

- **ladicí předsada se nesmí dostat do hry** — přesně past „ladicí hodnota
  v produkci“ (§13.7 `M6`);
- **vypnutá mechanika, která nikdy neběžela, je slepé místo** — u atrofie se musí
  ověřit, že **po zapnutí opravdu klesá** (§13.1).

### 9.2 Těžba, výroba, kvalita

| Co | Vzorec / hodnota | Zdroj |
|---|---|---|
| **Výnos těžby** | `1 + (dovednost − obtížnost)/10` | už v kódu, §13.3 — naměřeno 15. 10. 2026: `scripts/mining.gd:56` počítá `int(max(0, 1 + (hodnota - difficulty) / 10))` |
| **Směs u všech zdrojů** | Každý zdroj má **běžnou i vzácnou složku**; **delší těžba vydá víc vzácného**. | §12.1 |
| **Vzácná složka — šance** | start **2 %**, **+1 % za každých 10 s** nepřetržité těžby, **strop 30 %** | §13.3 |
| **Kvalita výrobku** | `dovednost/20` → **0–5 stupňů** (cena + trvanlivost) | už v kódu i v roadmapě (`sim.crafting`), §13.3 — naměřeno 15. 10. 2026: `scripts/crafting.gd:42` počítá `int(floor(dovednost / 20.0))` |
| **Zmetkovost** | část výroby se nepovede (uživatelovo „menší ztrátovost“); **ztrátovost je jedno z čísel, kterými je vidět růst** (GDD §3, pilíř `P2`) | **ROZHODNUTO 8. 10. 2026** — `_analyza/DESIGN-REVIZE-2.md` `§13.8` (menu nákladů) a **§17** (rozhodnutí) |
| **Palivo** | tavení spotřebuje **uhlí** — uhlí se musí těžit | **ROZHODNUTO 8. 10. 2026** — `§13.8` (menu) a **§17** (rozhodnutí) |
| **Opotřebení nástroje** | krumpáč a kladivo se **ničí** (trvanlivost už v kódu je) → nutí opravovat = další odběratel materiálu | **ROZHODNUTO 8. 10. 2026** — `§13.8` (menu) a **§17** (rozhodnutí) |

#### Tři náklady řemesla: kde vstupují, jaký mají vzorec — a co na nich (ne)je rozhodnuté

**Odkud rozhodnutí je:** `_analyza/DESIGN-REVIZE-2.md` **§17** (dodatek z 8. 10. 2026,
session 3) — uživatel doslovně: „*Zatím palivo, opotřebení, zmetkovost a můžeme
rozvíjet časem.*“ Vzaty jsou **první tři** náklady z menu v §13.8; **poplatek za
stanici a riziko cesty zůstávají pro rozsah `L`**. Technický dopad (tvar dat
a smlouva) patří do `TDD` — `TDD` §3.11 (smlouva `Crafting`); tady je jen to,
co je design.

| Náklad | Kde vstupuje | Vzorec (tvar, ne hodnota) | Číslo |
|---|---|---|---|
| **Palivo** | tavení a výroba oceli (recepty `smelting`, ocel) | uhlí je **vstup receptu** (`inputs`), takže se při výrobě odečte: `vstupy = recept.inputs` | **NEMĚŘENO** — „kolik uhlí na dávku“ **není rozhodnuté**; hodnoty až při ladění (milník `M3`) |
| **Opotřebení nástroje** | těžba krumpáčem, kování kladivem | `trvanlivost −= opotřebení_za_použití`; v nule je nástroj `broken()` a musí se opravit (`repair()`) | **NEMĚŘENO** — kolik opotřebení na použití, **není rozhodnuté**; v kódu je dnes jen `trvanlivost`, `repair()` a `broken()` (`scripts/item.gd` — naměřeno 15. 10. 2026) |
| **Zmetkovost** | každá výroba | výsledek výroby je `{ok, id, kvalita, zmetek: bool}`; `zmetek: true` = vstupy odešly a výstup není | **NEMĚŘENO** — pravděpodobnost **není rozhodnutá**; rozhodnutý je jen **směr** (ztrátovost má s dovedností klesat — GDD §3) |

**Proč u těch čísel stojí `NEMĚŘENO`, a ne nula:** nula by tvrdila, že náklad nic
nestojí — a to rozhodnuté není. Čísla se **ladí hraním, ne plánováním** (§13.8)
a projekt je zastavený, takže hodnoty patří k milníku `M3`. Vymyšlené číslo by se
četlo jako rozhodnuté a nikdo by ho nepřeměřil.

> **✅ ROZHODNUTO 8. 10. 2026 (uživatel):** berou se **první tři náklady —
> palivo, opotřebení nástroje a zmetkovost**; doslova „*zatím palivo,
> opotřebení, zmetkovost a můžeme rozvíjet časem*“. Zbývající dvě položky menu
> (poplatek za stanici, riziko cesty) zůstávají **pro rozsah `L`**.
> **Cena rozhodnutí:** výroba přestává být rutina — přibývají **tři čísla
> k ladění** (spotřeba uhlí, trvanlivost nástroje, zmetkovost) a musí se hlídat,
> aby se z nich nestal grind. Rozdíl proti grinduje ale pořád v tom, **čím se
> platí**: ne časem, ale **rozhodnutím** (co, kdy a z čeho vyrobit) — přesně to
> byla uživatelova obava v §13.8.

### 9.3 Svět: ceny, infestace, zásobenost

| Co | Vzorec | Zdroj |
|---|---|---|
| **Cena** | `základ × (1 + (100 − zásobenost)/100) × (1 + infestace/200)` | §13.3 |
| **Infestace** | `+1` za hodinu hry, `−2 × (zásobenost/100)` za hodinu | §13.3 |
| **Zásobenost** | `−1` za hodinu, `+5` za dodanou dávku (ingot, zbraň) | §13.3 |

**Proč je to takhle (a ne „třetí stav“):** ceny jsou **důsledek** dvou čísel,
takže hráč vidí **příčinu** (dodávky) i **následek** (cena) na jednom místě.
Když trh zaplavíš, **marže spadne** a musíš hledat jiné zboží nebo lepší zdroj —
to je náklad, který **není čas**, je to **příležitost**. (§13.1, §13.8)

### 9.4 Boj, výbava, léčení

| Co | Rozhodnutí / vzorec | Zdroj |
|---|---|---|
| **Boj — zásah** | `0,5 + Dex/200 + dovednost/200` | už v roadmapě (`sim.combat`), §13.3 |
| **Boj — zranění** | `1 + Str/10 + zbraň − zbroj` | tamtéž |
| **Atributy** | Str/Dex/Int **0–100, výchozí 10** | už v kódu (`attributes.gd`) |
| **Zbraň** | **MVP jen v ruce**; poloha „u pasu“ se odkládá (2× obrázků na každou zbraň) | §13.1 |
| **Léčení** | **Obvazy jako předmět** — léčba je **řemeslo, ne regenerace**. Řetěz: `flax` (len) → `cloth` (látka) → `bandage` (obvaz). | §13.1 |
| **Použití obvazu** | **kliknutím v inventáři**, s odečtením jednoho kusu (myš je primární vstup) | §14.2 |

---

## 10. Obsah v číslech (rozsah `M`)

**Rozhodnuto** (`R2-1` „M — doporučuji“, obsah potvrzen `M7` „Sedí“). (§13.2,
§12.5, §13.7)

| Kategorie | Obsah |
|---|---|
| **Materiály (11, z toho 3 meziprodukty)** | běžné: `iron_ore`, `coal`, `stone`, `wood`, `flax` · **vzácné složky směsi**: `silver_ore` (doly), `hardwood` (les), `fine_flax` (pole) · meziprodukty: `cloth` (len), `iron_ingot` (ruda + uhlí), `steel_ingot` (ingot + uhlí) |
| **Předměty (7)** | `iron_sword`, `iron_armor` (existují), `steel_sword`, `pickaxe` (krumpáč), `hammer` (kovářské kladivo — **zároveň zbraň**, demonstruje `P3`), `bandage` (obvaz), `silver_ring` (stříbro jako prodejní zboží) |
| **Nestvůry (3)** | `skeleton` (existuje), `wolf` (vlk — les), `bandit` (loupežník — cesty) |
| **Recepty (8)** | tavení (ruda + uhlí → ingot), ocel (ingot + uhlí → ocel), kování meče, kování zbroje, ocelový meč, tkaní (len → látka), obvazy (látka → obvaz), krumpáč/kladivo |
| **Dovednosti (6)** | `tezba`, `drevorubectvi`, `kovarstvi`, `tkani`, `boj_na_blizko`, `obchod` (`obchod` ovlivňuje ceny — drží roli „obchodník“ ze záměru) |
| **Mapa** | **vesnice + důl + les + pole** (len); dnes: 30×16 dlaždic a 4 markery |
| **Délka sezení** | 30–60 min |
| **Práce (odhad)** | **+20–30 granulí** |

**Co to znamená proti dnešnímu stavu:** naměřeno 8. 10. 2026 **čtením
`assets/data/*.json`** je obsah hry
**4 materiály, 4 dovednosti, 3 recepty, 1 nestvůra a 2 předměty** (§1) — rozdíl
je **řádový**, a to je cena rozsahu `M`. **Přeměřeno 15. 10. 2026 — sedí beze
změny** (`json.loads` nad `assets/data/*.json`; `creatures.json` v repu **není**,
přítel je `monsters.json`).

**Proč `M` a ne `S`/`L`:** `S` nechá smyčku tenkou (málo věcí k výrobě →
„uplatnění“ je prázdné, `V5` nemá co ukázat) a `L` řádově přeroste to, co dnes
existuje — a hlavně **`L` se nedá ladit**, protože ladění vyžaduje hraní a na
10 nestvůr a 30 předmětů není kdy. `M` je nejmenší rozsah, ve kterém smyčka
funguje **celá**. (§12.5)

---

## 11. Non-goals — co v MVP ZÁMĚRNĚ není

(§12.3; `N11` doplněno rozhodnutím `R2-3`.)

| # | Co tam není | Proč |
|---|---|---|
| N1 | **Skutečné MMO a server** v MVP | rozhodnuto v §11 — provoz a populace; architektura se na cestu `B` jen připraví |
| N2 | **Pevné třídy a povolání** | pilíř `P3` — kombinace dovedností jsou volné |
| N3 | **Příběh „vyvoleného“** | pilíř `P1` — hráč je účastník světa, ne jeho střed |
| N4 | **Pixel art, 16barevná paleta, dithering** | zakázáno `assets/spec.json` (styl UO:T2A = předrenderované 3D) |
| N5 | **UO datové soubory a klient** | hra je vlastní, není to klient Ultimy |
| N6 | **Fyzika enginu** (převrhnutelné předměty, síly) | pohyb i kolize jsou vlastní systémy; fyzika by přidala ladění, které vize nechce |
| N7 | **Denní cyklus a roční období** | `DESIGN.md` je vyřadil a nic v jejich prospěch nezaznělo |
| N8 | **Dungeony, infestace a šlechtění zvěře jako aktivity** v MVP | jsou to **slova, ne systémy**; infestace je jen **stav světa** (`R2-2`) |
| N9 | **Automatická asistence** (pravidla hrají za hráče) | **rozpor s hlavním pilířem `P2`** — „požitek z vlastní dovednosti“ a automat, který hraje za tebe, nejdou dohromady |
| N10 | **Více postav na jednom účtu** v MVP | rozsah (`G-8`) |
| N11 | **Lektvary a alchymie** v MVP | rozhodnuto `R2-3` („lektvary později“); srovnalo tři rozporné dokumenty. **Role lektvaru v `spec.json` zůstává nevyužitá** — je to deklarace vzhledu, ne slib obsahu |

**Co tím vzniklo:** uživatelův příklad cíle „100 dávek lektvaru“ **není v MVP
splnitelný** → nahrazuje se (např. „100 ingotů“).

**Zvlášť k `N11`:** lektvary jsou mimo MVP, ale **otázka „čím se hráč léčí?“**
rozhodnutá je — **obvazy** (§13.1). Kdo hledá v `items.json` lektvar, nenajde ho
a **není to vada**.

> **⚠ `N9` PŘEFORMULOVÁNO 2026-10-09 (rozhodnutí uživatele; záznam se
> nepřepisuje, jen doplňuje).** Původní znění `N9` („automatická asistence =
> rozpor s `P2`") **platí dál pro to, co zakazovalo**: hra nesmí **rozhodnout
> za hráče**. Nově je dovolené, aby hra **provedla, co hráč rozhodl** — i když
> u hry není (offline doběh), a to i podle pravidel s podmínkami („udělej toto;
> když nastane tamto, udělej tamto"). Dovednost hráče se tím přesouvá
> z klikací zručnosti na **plánování a rozhodnutí** — to je jiná obrana pilíře
> `P2`, ne jeho opuštění.
>
> **Co z toho plyne pro tenhle projekt:** `scripts/assist.gd` (17 řádků, pravidla
> „hp < X" a „target dead") a `scripts/offline.gd` (57 řádků, denní strop
> `DAILY_CAP = 100`, efektivita 0,3) **nejsou v rozporu s designem**, pokud
> platí hranice výš: **rozhoduje hráč, hra provádí**. Kdo je zapojí do monolitu,
> ať napíše, které rozhodnutí je hráčovo a které dělá kód — jinak se
> z asistence stane automat, který hraje místo hráče.
>
> **Zdroj rozhodnutí a plná hranice (i cena a cesta zpět):**
> `E:\Workspaces\game-clone\ROZHODNUTI-2026-10-09-SMER.md` §2 D3.

---

## 12. Milníky `M0`–`M6` — každý je vidět na obrazovce

**Rozhodnuto** (`P1` „Sedí M0–M6“, §15.5). Pravidlo: **každý milník je hratelný
stav, ne „vrstva kódu“** — pozná se to tak, že je **vidět na obrazovce**. (§15.1)

| Milník | Co je na konci vidět | Co to obnáší |
|---|---|---|
| **M0 — Kostra** | hra se spustí a nezhroutí se; komponenty existují přes registr | přepis `game.gd` (monolit) na registr (`engine.shell`), pevný tik |
| **M1 — Hýbu se** | postava se **plynule** pohybuje myší po dlaždicové mapě, objekty se nepřekrývají, rozběh a zastavení sedí | pohyb, kolize, řazení hloubky |
| **M2 — Těžím a vidím číslo** | v inventáři je ruda, **číslo dovednosti se pohnulo**, delší těžba dala vzácnější kus | zdroje, směs, výnos, HUD s čísly |
| **M3 — Vyrábím** | u pece ingot, u kovadliny meč; kvalita je vidět, nástroj se opotřebovává | recepty, kvalita, opotřebení, zmetkovost |
| **M4 — Prodávám a svět reaguje** | **stav světa na obrazovce** (infestace, zásobenost) se po dodávce změní | zakázky, ceny, simulace světa |
| **M5 — Žiju ve světě** | svět se hýbe **i beze mě**; zakázky odpovídají tomu, jak si mě váží; smrt a respawn | uznání světa, léčení, smrt |
| **M6 — Grafika** | postava ukazuje, co má nasazené (vrstvená grafika) | až po M5 — rozhodnutí z §7 (`A-1` odloženo) |

**Cena:** vzhled je **poslední**, i když by se líbil dřív. (§15.5 `P1`)

**Definice hotovo** (rozhodnuto `P4`, §15.2) — hotovo JE, když platí **všechny
čtyři**: **soubor je v `main`** A **brána jeho funkci skutečně zavolala**
A **přijímací kritérium proběhlo s konkrétní hodnotou** A **funkci volá
produkční kód**. Hotovo **NENÍ** „PR je sloučené“, „testy jsou zelené“,
„funkce existuje“ ani `done: true`.

---

## 13. Odkud hra startuje (naměřeno 8. 10. 2026; přeměřeno 15. 10. 2026)

Tahle sekce **není design** — je to **srovnávací základ**: co z GDD dnes
existuje. Detail technického stavu je v `docs/TDD.md` a v `.forge/roadmap.json`;
naměřená čísla **s postupem** jsou v `_analyza/PRACE-2026-10-15/FAKTA.md`.
Prostřední sloupec je **stav k 8. 10. 2026** (zdroj: `§1` — měřeno čtením
souborů k `HEAD = bc51e46`) a **nepřepisuje se** (historické číslo je „ve svém
čase správné“); pravý sloupec je **přeměření 15. 10. 2026** (`HEAD = 6986b0d`)
s postupem, odkud bylo čteno.

| Co | Naměřeno 8. 10. 2026 | Přeměřeno 15. 10. 2026 (postup) |
|---|---|---|
| Hra dnes | **sběračka dvou mincí** — mapa 30×16, 2 coin markery, `Label` se skóre; nápověda inzeruje **6** kláves, které kód neobsluhuje | **sedí**: `assets/levels/main.json` je 30×16 = **480** dlaždic, markerů **4** (`coin` 2, `spawn` 1, `exit` 1), spawn (17, 7) — čteno `json.loads` a ověřeno během testů; 6 kláves je text v `game.gd` a `Input.` je v celém `scripts/` jen v `player.gd` (`FAKTA.md` #48–#51, #67, #68) |
| Obsah | 4 materiály, 4 dovednosti, 3 recepty, 1 nestvůra, 2 předměty | **sedí** (`json.loads` nad `assets/data/*.json`): 4 / 4 / 3 / 1 / 2; `creatures.json` v repu **není** — přítel je `monsters.json` (`FAKTA.md` #43–#47) |
| Plán vs. realita | **`done` se nerovná „hra to používá“.** Naměřeno 15. 10. 2026: `.forge/roadmap.json` má **10 granulí** a `done: true` u **5**; hra používá 2 komponenty (`level.gd`, `player.gd`). Historicky (8. 10. 2026) byla hotovost hlášená u **16** položek — **ve svém čase správné číslo** (archiv plánu: `_analyza/PRACE-2026-10-15/ROADMAPA-STARA-2026-10-15.json`) | **sedí**: `done` je nově **měřené** (soubor v `main` A volá ho produkční cesta — nástroj `_analyza/PRACE-2026-10-15/zmer-produkci.py`). Do produkční cesty vedou z granul s prací v `main` jen `world.level` (`level.gd`) a `entity.player` (`player.gd`); `game.gd` vlastní granule `engine.shell`, `shell.coins` a `sim.wire` |
| Mrtvá granule | `scripts/world.gd` = **0 B** — blokuje `world.nodes` a přes ni `sim.mining` a `persist.save.state` (milník `M2`) | **potvrzeno**: `scripts/world.gd` = **0 B**, 0 řádků, nikdo ho nenačítá a v testech je zmíněn 0×; vlastní ho granule `world.nodes` (`done: false`). Původní znění „blokuje `world.map` i `engine.shell`“ bylo **nepravdivé**: `world.map` byla **8. 10. 2026 vyřazena z plánu** (v roadmapě není) a `engine.shell` závisí jen na `engine.registry` (`FAKTA.md` #17, `.forge/roadmap.json`) |
| Vstupní akce | `project.godot` nemá **ani jednu** (`[input]` obsahuje jen `input_devices`) | **sedí**: sekce `[input]` má jen `input_devices=PackedStringArray("keyboard", "mouse")` a `[autoload]` v souboru **není** (`FAKTA.md` #66, #67) |
| Dva výtvarné systémy | 258 PNG v `tools/blender/sprites/**` (kód na ně **neodkazuje ani jednou**) vs. 16 plochých v `assets/sprites/**`. **Naměřeno 8. 10. 2026:** `assets/sprites/player.png` je **pixel-identický** se složením 4 vrstev `d0_f1` z Blenderu — hra tedy zobrazuje **1 frame ze 128**, zploštěný. Není to cizí systém, je to **tatáž grafika zploštěná** (detail: `docs/ADD.md` §3) | **sedí**: `rglob` nad `tools/blender/sprites/` dal **258** PNG (130 v kořeni + 128 v `npc/`) a **0** odkazů na ně z `scripts/`, `assets/`, `main.tscn`, `project.godot`, `export_presets.cfg`; `assets/sprites/` má **16** PNG a hra odkazuje **2** (`player.png`, `coin.png`); `player.png` i `npc.png` mají **shodný `sha256`** se složeninou vrstev `d0_f1` (`FAKTA.md` #26, #28, #29, #35, #37, #38) |
| Smlouvy | `ARCHITEKTURA.md` má 18 smluv, **tvar dat 3** | **dnes platí `TDD` §3** — smlouvy **s tvarem dat** jsou tam (počet je v nadpisu oddílu; `Registry` přibyla 15. 10. 2026); `ARCHITEKTURA.md` je od 8. 10. 2026 **historie** (`_analyza/PRACE-2026-10-15/ROZPORY.md` R19). Naměřeno 15. 10. 2026 čtením: tabulka smluv v `ARCHITEKTURA.md` §2 má **18** komponent a tvar dat popisuje u **3** z nich |
| Známé vady běhu (ne design) | — | `game.gd:181` tweenuje `hud` dřív, než ho `_add_ui()` vytvoří (chyba při každém načtení scény; CI hledá jen `SCRIPT ERROR`, takže ji nechytí) a `economy.price()` vrací **0** pro oba předměty, přitom hlásí chybu na `economy.gd:21`. **Nezapisuje se sem podrobně** — seznam a postup je v `TDD` §10 a v `FAKTA.md` #92–#99 (naměřeno 15. 10. 2026) |

---

## 14. Co v tomhle dokumentu ZÁMĚRNĚ NENÍ

- **Technický návrh** (tik, vrstvy, smlouvy s tvarem dat, výkon, ukládání,
  chybové chování) → `docs/TDD.md`. GDD říká **co** a **proč**, ne **jak**.
- **Vzhled a assety** (rozměry, role, vrstvy, pipeline, katalog) → `docs/ADD.md`
  a strojově `assets/spec.json`.
- **Plán granulí a pořadí práce** → `.forge/roadmap.json`. Dřívější znění
  „**vzniká z §12**“ platilo **ve svém čase** (plán se navrhoval z milníků);
  dnes plán obsahuje **otevřené granule `M0`–`M1`** (+ granule s prací
  v `main`); granule pro `M2`–`M6` se doplňují **při otevření milníku**
  (`_analyza/NAVRH-ROADMAPY-M0-M6.md` §4) — **ne dopředu naslepo**. Naměřeno
  15. 10. 2026 (`json.loads` nad plánem): 21 granul a klíč `milestone` **není
  ani u jedné**, takže vazba na `M0`–`M6` je dnes jen v zadání granul, ne
  ve strojovém klíči; vyřazené granule (8. 10. 2026, mimo jiné `world.map`) jsou
  zapsané v `_popis` plánu.
- **Ceny rozhodnutí a historie dialogu** → `_analyza/DESIGN-REVIZE-2.md`
  (needituje se; je to záznam, ne stav).
- **Konkrétní čísla obsahu** (kolik má který předmět damage, kolik HP má vlk) —
  patří do `assets/data/*.json`; GDD určuje **rozsah a vzorce**, ne hodnoty
  jednotlivých záznamů.
- **Ceny a ladicí hodnoty nákladů řemesla** → **rozhodnuto je jen to, KTERÉ tři
  náklady to jsou** (GDD §9.2: palivo, opotřebení nástroje, zmetkovost);
  **konkrétní čísla rozhodnutá nejsou** — GDD §9.2 je vede jako `NEMĚŘENO`
  a patří k ladění (milník `M3`).

### 14.1 Otevřené body (pojmenované, ne zapomenuté)

| # | Co je otevřené | Kde se to rozhodne |
|---|---|---|
| **O-2** | **Luk a zvěř (hraničář).** Vize zmiňuje hraničáře („spolehlivěji střílí, jezdí, ochočí zvěř“); luk je ale **nový druh souboje** (projektily, dostřel). V rozsahu `M` je hraničář zastoupen **lovem zvěře na blízko a kůží**; luk a zvěř jako systém **později** (`L`). | §13.5 — vědomě odloženo do `L`. |
| **O-4** | **Hodnoty mrtvé zóny a vyhlazení** pohybu (GDD §6). Rozhodnutý je jen požadavek, že jsou měřitelné číslem. | Ladění při milníku `M1`. |
| **O-5** | **Klíče dovedností a části receptů jsou v datech česky** (`tezba`, `drevorubectvi`, `kovarstvi`, `boj_na_blizko`; recepty `kovani_mece`, `kovani_zbroje`), zatímco pravidlo jazyka (`R-3`) žádá **klíče anglicky** (a `items.json`/`materials.json` už anglicky jsou: `iron_sword`, `iron_ore`; recept `smelting` taky). | **Naměřeno 8. 10. 2026** čtením `assets/data/*.json` (**přeměřeno 15. 10. 2026 — sedí**: české klíče jsou v datech dál). Sjednocení **mění kód i data** → samostatný úkol; do té doby platí pravidlo `R-3` pro **nové** klíče a stávající české klíče se **nepřejmenovávají mimochodem** (rozbité by byly testy, roadmapa i uložené pozice). |

**Odložené (ne otevřené — zůstávají pojmenované):** `N-2` **osm směrů** („až po
prototypech“, GDD §6 — rozhodne se, až bude vidět pohyb) a `A-1` **paperdoll
a vrstvená grafika** („až s vrstvenou grafikou“, GDD §7 a milník `M6` v §12).
Oba jsou rozhodnuté jako **odložené**, proto nejsou v tabulce výš.

**Kam se podívat za všechny:** `O-1`…`O-5` jsou tady a v §14.2, `N-2` a `A-1`
ve větě výš — **nic se nemazalo**, jen se přesunulo (`O-1`, `O-3` jsou
rozhodnuté, proto jsou v §14.2).

### 14.2 Už není otevřené (rozhodnuto 8. 10. 2026 — záznam se nemaže)

| # | Co bylo otevřené | Jak je rozhodnuto |
|---|---|---|
| **O-1** | **Čím platí řemeslník, když ne grindem** (§13.8) — menu nákladů: palivo, opotřebení nástroje, zmetkovost, poplatek za stanici, riziko cesty. | **VZATO: palivo, opotřebení nástroje a zmetkovost** (uživatel: „*zatím palivo, opotřebení, zmetkovost a můžeme rozvíjet časem*“). Poplatek za stanici a riziko cesty zůstávají pro `L`. Zapsáno v GDD §9.2. |
| **O-3** | **Sjednocení názvu hry** `uo-sandbox` → `uo-shadows`. | **PROVEDENO 8. 10. 2026** (uživatel: „*přejmenuj hru na uo-shadows*“): `project.godot` `config/name` = `uo-shadows`, `assets/spec.json` `_popis` = „projekt uo-shadows“, `export_presets.cfg` `product_name` = `uo-shadows`. **Důsledek, který se musí vědět:** `user://` se přesunul z `%APPDATA%\Godot\app_userdata\uo-sandbox\` na `…\uo-shadows\` — ve starém adresáři ale **žádný `save.cfg` nebyl** (naměřeno: jen cache a logy), takže se nic neztratilo. `company_name` v `export_presets.cfg` zůstává `GameForge` (je to vydavatel, ne název hry). **Změněno 8. 10. 2026 rozhodnutím uživatele** (`01a9649`): `company_name = "ssevcikm-spec"`, `copyright = "© 2026 ssevcikm-spec"`. Text výš je **stav před touto změnou** (ve svém čase správný). **Naměřeno 15. 10. 2026 čtením `export_presets.cfg`:** řádek 43 `application/company_name="ssevcikm-spec"`, řádek 44 `application/product_name="uo-shadows"`, řádek 46 `application/copyright="© 2026 ssevcikm-spec"` — tvrzení „`copyright` je prázdné“ a „`company_name` zůstává `GameForge`“ jsou tedy **nepravdivá**; platí soubor. |
