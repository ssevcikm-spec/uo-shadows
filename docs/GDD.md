# GDD — `uo-shadows`: co hra je a jak se hraje

> **Co tenhle dokument JE:** **zdroj pravdy o designu hry** (game design
> document). Říká, co hra je, jak se hraje, jaké má mechaniky s čísly a co v ní
> **záměrně není**.
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
  „růst je vidět“ dnes **nemá kde být vidět** (§1, `kód`: `scripts/game.gd`);
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
| **Směry** | Prototyp zůstává u **4 směrů**; **osm směrů se rozhodne, až bude vidět pohyb** (`N-2` „Až po prototypech“). Kdyby se pro 8 směrů rozhodlo později, je to **2× obrázků na každý kus výbavy** (dnes 32 → 64 na kus). |

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
| **Výnos těžby** | `1 + (dovednost − obtížnost)/10` | už v kódu (`mining.gd`), §13.3 |
| **Směs u všech zdrojů** | Každý zdroj má **běžnou i vzácnou složku**; **delší těžba vydá víc vzácného**. | §12.1 |
| **Vzácná složka — šance** | start **2 %**, **+1 % za každých 10 s** nepřetržité těžby, **strop 30 %** | §13.3 |
| **Kvalita výrobku** | `dovednost/20` → **0–5 stupňů** (cena + trvanlivost) | už v roadmapě (`sim.crafting`), §13.3 |
| **Zmetkovost** | část výroby se nepovede (uživatelovo „menší ztrátovost“) | **rozhodnuto 8. 10. 2026** (§13.8) |
| **Palivo** | tavení spotřebuje **uhlí** — uhlí se musí těžit | **rozhodnuto 8. 10. 2026** (§13.8) |
| **Opotřebení nástroje** | krumpáč a kladivo se **ničí** (trvanlivost už v kódu je) → nutí opravovat = další odběratel materiálu | **rozhodnuto 8. 10. 2026** (§13.8) |

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

**Co to znamená proti dnešnímu stavu:** naměřeno 8. 10. 2026 je obsah hry
**4 materiály, 4 dovednosti, 3 recepty, 1 nestvůra a 2 předměty** (§1) — rozdíl
je **řádový**, a to je cena rozsahu `M`.

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

## 13. Odkud hra startuje (naměřeno 8. 10. 2026)

Tahle sekce **není design** — je to **srovnávací základ**: co z GDD dnes
existuje. Detail technického stavu je v `docs/TDD.md` a v `.forge/roadmap.json`.
(Zdroj: `§1` — měřeno čtením souborů k `HEAD = bc51e46`.)

| Co | Naměřeno |
|---|---|
| Hra dnes | **sběračka dvou mincí** — mapa 30×16, 2 coin markery, `Label` se skóre; nápověda inzeruje **6** kláves, které kód neobsluhuje |
| Obsah | 4 materiály, 4 dovednosti, 3 recepty, 1 nestvůra, 2 předměty |
| Plán vs. realita | **`done` se nerovná „hra to používá“: v roadmapě je `done: true` u 16 granul** (stav 8. 10. 2026 po postavení `engine.registry`; předtím 15 a ještě předtím 13), **ale hra používá 2** (`level.gd`, `player.gd`); HUD, boj, výroba, ekonomika ani ukládání nejsou v produkční cestě |
| Mrtvá granule | `scripts/world.gd` = **0 B** — blokuje `world.map` i `engine.shell` |
| Vstupní akce | `project.godot` nemá **ani jednu** (`[input]` obsahuje jen `input_devices`) |
| Dva výtvarné systémy | 258 PNG v `tools/blender/sprites/**` (kód na ně **neodkazuje ani jednou**) vs. 16 plochých v `assets/sprites/**`. **Naměřeno 8. 10. 2026:** `assets/sprites/player.png` je **pixel-identický** se složením 4 vrstev `d0_f1` z Blenderu — hra tedy zobrazuje **1 frame ze 128**, zploštěný. Není to cizí systém, je to **tatáž grafika zploštěná** (detail: `docs/ADD.md` §3) |
| Smlouvy | `ARCHITEKTURA.md` má 18 smluv, **tvar dat 3** |

---

## 14. Co v tomhle dokumentu ZÁMĚRNĚ NENÍ

- **Technický návrh** (tik, vrstvy, smlouvy s tvarem dat, výkon, ukládání,
  chybové chování) → `docs/TDD.md`. GDD říká **co** a **proč**, ne **jak**.
- **Vzhled a assety** (rozměry, role, vrstvy, pipeline, katalog) → `docs/ADD.md`
  a strojově `assets/spec.json`.
- **Plán granulí a pořadí práce** → `.forge/roadmap.json` (vzniká z §12).
- **Ceny rozhodnutí a historie dialogu** → `_analyza/DESIGN-REVIZE-2.md`
  (needituje se; je to záznam, ne stav).
- **Konkrétní čísla obsahu** (kolik má který předmět damage, kolik HP má vlk) —
  patří do `assets/data/*.json`; GDD určuje **rozsah a vzorce**, ne hodnoty
  jednotlivých záznamů.
- **Ceny a ladicí hodnoty nákladů řemesla** → **rozhodnuto** (GDD §9.2:
  palivo, opotřebení nástroje, zmetkovost); konkrétní čísla patří k ladění.

### 14.1 Otevřené body (pojmenované, ne zapomenuté)

| # | Co je otevřené | Kde se to rozhodne |
|---|---|---|
| **O-2** | **Luk a zvěř (hraničář).** Vize zmiňuje hraničáře („spolehlivěji střílí, jezdí, ochočí zvěř“); luk je ale **nový druh souboje** (projektily, dostřel). V rozsahu `M` je hraničář zastoupen **lovem zvěře na blízko a kůží**; luk a zvěř jako systém **později** (`L`). | §13.5 — vědomě odloženo do `L`. |
| **O-4** | **Hodnoty mrtvé zóny a vyhlazení** pohybu (GDD §6). Rozhodnutý je jen požadavek, že jsou měřitelné číslem. | Ladění při milníku `M1`. |
| **O-5** | **Klíče dovedností a části receptů jsou v datech česky** (`tezba`, `drevorubectvi`, `kovarstvi`, `boj_na_blizko`; recepty `kovani_mece`, `kovani_zbroje`), zatímco pravidlo jazyka (`R-3`) žádá **klíče anglicky** (a `items.json`/`materials.json` už anglicky jsou: `iron_sword`, `iron_ore`; recept `smelting` taky). | **Naměřeno 8. 10. 2026** čtením `assets/data/*.json`. Sjednocení **mění kód i data** → samostatný úkol; do té doby platí pravidlo `R-3` pro **nové** klíče a stávající české klíče se **nepřejmenovávají mimochodem** (rozbité by byly testy, roadmapa i uložené pozice). |

### 14.2 Už není otevřené (rozhodnuto 8. 10. 2026 — záznam se nemaže)

| # | Co bylo otevřené | Jak je rozhodnuto |
|---|---|---|
| **O-1** | **Čím platí řemeslník, když ne grindem** (§13.8) — menu nákladů: palivo, opotřebení nástroje, zmetkovost, poplatek za stanici, riziko cesty. | **VZATO: palivo, opotřebení nástroje a zmetkovost** (uživatel: „*zatím palivo, opotřebení, zmetkovost a můžeme rozvíjet časem*“). Poplatek za stanici a riziko cesty zůstávají pro `L`. Zapsáno v GDD §9.2. |
| **O-3** | **Sjednocení názvu hry** `uo-sandbox` → `uo-shadows`. | **PROVEDENO 8. 10. 2026** (uživatel: „*přejmenuj hru na uo-shadows*“): `project.godot` `config/name` = `uo-shadows`, `assets/spec.json` `_popis` = „projekt uo-shadows“, `export_presets.cfg` `product_name` = `uo-shadows`. **Důsledek, který se musí vědět:** `user://` se přesunul z `%APPDATA%\Godot\app_userdata\uo-sandbox\` na `…\uo-shadows\` — ve starém adresáři ale **žádný `save.cfg` nebyl** (naměřeno: jen cache a logy), takže se nic neztratilo. `company_name` v `export_presets.cfg` zůstává `GameForge` (je to vydavatel, ne název hry). |
