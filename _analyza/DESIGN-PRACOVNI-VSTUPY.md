# Design — pracovní vstupy a kritická revize (sezení 1)

> **Co tenhle dokument JE:** **pracovní podklad pro GDD.** Zapisuje, co uživatel
> rozhodl (jeho slovy, jako **pocit a směr**, ne jako hotovou specifikaci),
> a přidává **kritiku, rozpory a návrhy** — o které uživatel výslovně požádal.
>
> **Není to:** GDD. GDD vznikne, až se tyhle vstupy vyladí.
>
> **Zadání:** uživatel, 8. 10. 2026: *„ber moje vstupy jako můj pocit… projdi se
> mnou celý plán, buď kritický, podávej zpětnou vazbu nebo náměty. Chci to
> projít detailně, vyladit co nejvíce hned a objasnit to, aby se systém a AI pak
> nemusely hádat."*
> **Vzniklo:** 8. 10. 2026. **Odkud brát stav:** tenhle dokument je stav svého
> tématu; technický stav projektu je v `_analyza/REKONSTRUKCE-ADD-TDD-GDD.md`.

---

## 1. Co uživatel rozhodl

### 1.1 Prototypy a grafika

> „*než bude vyvinutá grafika, budu rád za primitivní prototypy — cokoliv
> nejlevnějšího. Mám i přístup k webům s free assety s volnou licencí — jsou
> pěkné.*"

**Zapsáno jako:** grafika **není** blokátor. Do doby, než hra funguje, se kreslí
primitivech. Free assety jsou k dispozici.

### 1.2 Ovládání (odpověď na G-1)

> „*chci plynulý pohyb nezamčený v herní mřížce. Kolize objektů — nemohou se
> překrývat. Měl by být plynulý všesměrový a je potřeba vyladit rozběh
> a zastavení, aby dobře korespondovaly se vstupem od hráče. Primárně se bude
> používat vstup myši, pravděpodobně držení pravého tlačítka a proximita kurzoru
> k postavě (a nebo toggle a stamina) rozhodují o rychlosti pohybu — chůze, běh,
> pomalá chůze?*"

**Zapsáno jako:** pohyb plynulý, všesměrový, mimo mřížku; objekty se nesmí
překrývat; zrychlení a zpomalení musí ladit se vstupem; hlavní vstup = myš.

### 1.3 Pilíře a zážitek (odpověď na G-2)

> „*volně rostoucí skilly, které se vzájemně doplňují. Nejenže třeba zbraň,
> která seká i bodá, bude těžit pro plný potenciál z umění s bodnými a sečnými
> zbraněmi, ale také je současně trénuje. A kdo umí mlátit kladivem (kovář),
> získává lehkou zkušenost do boje s těžkopádnými zbraněmi. Porozumění kovům
> pomáhá kováři rychleji se učit tinkering, atd. Hra je sandbox, každý hráč si
> může zvolit směr a kombinovat libovolné dovednosti, ale s limitem. Kromě toho
> je potřeba dovednosti udržovat — používáním, jinak atrofují. Mistrovství ve
> skillu je hluboce rewarding, ale každá fáze skillu od 0 po max je důležitá.
> I málo schopný válečník si může zabojovat a řemeslník, co těží jen železo, si
> vydělá, protože železo je potřeba na výrobu spotřebního zboží, stavby, atd.
> Zážitek ze hry je účast na živém světě. Plnit roli a užívat si roli mistra
> řemeslníka, obchodníka, válečníka, dobrodruha, hraničáře. Mít požitek
> z vytrénované postavy a z vlastní dovednosti.*"

**Zapsáno jako:** čtyři nosné myšlenky — **skilly se doplňují a navzájem
trénují**, **skilly atrofují**, **každá úroveň skillu má cenu** (ne jen max),
**hráč je účastník živého světa a hraje roli**.

### 1.4 Hlavní smyčka (odpověď na G-3)

> „*prožívat dobrodružství, získat odměnu pro sebe nebo příspěvek do světové
> ekonomiky (možnost prodávat, předávat získané materiály, zboží z výprav
> a z výroby). Vidět vliv na ekonomiku nebo na stav světa.*"

**Zapsáno jako:** smyčka je **výprava → odměna → uplatnění** (prodat, předat,
spotřebovat) **→ viditelná změna světa nebo ekonomiky**.

### 1.5 Co je na obrazovce (odpověď na G-4)

> „*Herní okno, rychlý náhled do paperdoll, rychlý přístup do inventáře, mapa.*"

### 1.6 Jak hráč pozná úspěch (odpověď na G-5)

> „*Hra nemá konec, bude to mmo. Úspěch je například v boji vyšší úspěšnost
> zásahu, vyšší zranění, delší přežití, vyšší potenciál. Ve výrobě menší
> ztrátovost, lepší kvalita, otevírají se možnosti modifikace finálního
> produktu, řemeslník má ve výrobě lepší konzistenci úspěchu, hraničář zase
> spolehlivěji střílí, jezdí, ochočí zvěř nebo podobné příšery, umí je trénovat
> a šlechtit — výsledek každé profese je nějaký přínos do ekonomiky nebo
> schopnost komunity odolávat, či zdolávat výzvy. Dungeony, infestace monster,
> získávání materiálů pro řemeslníky, výroba a údržba výzbroje a výstroje
> dobrodruhů.*"

**Zapsáno jako:** **hra nemá konec.** Úspěch je **měřitelný růst schopnosti**
(hit rate, damage, přežití, kvalita, konzistence) a **přínos pro komunitu**
(ekonomika, odolnost proti výzvám). Obsahové výzvy: dungeony, infestace,
zásobování řemeslníků, výzbroj dobrodruhů.

### 1.7 A-1 — odpověď, i když otázka nebyla pochopená

> „*Nerozumím zadání. Zdá se mi, že vrstvení má větší potenciál. Například
> postava hráče má zobrazovat co má nasazeno — meč? krumpáč? zbroj nebo
> oblečení? Má meč v ruce nebo u pasu?*"

**Zapsáno jako:** uživatel chce **vrstvení** — postava má zobrazovat, co má
nasazené. (Co otázka znamenala, vysvětluji v §2.6.)

---

## 2. Kritické připomínky

> **Ber to jako protinázor, ne jako odmítnutí.** U každého bodu je i to, co
> navrhuju místo toho.

### 2.1 ⚠ „Bude to MMO" je největší riziko celého projektu

**V čem je problém.** MMO není vlastnost hry, ale **provoz**: server,
autoritativní simulace, síť, persistence, odolnost proti podvádění — a hlavně
**živí hráči**. Vaše vlastní `ARCHITEKTURA.md:34` říká: „*simulace běží lokálně
(single-player); server/MMO vrstva až později*" a `DESIGN.md:20–21` dává MMO
mimo rozsah. Dnešní hra je Godot projekt na GitHub Pages, který si stáhne
jednotlivec.

**A druhý, ostřejší problém:** hlavní smyčka stojí na „*příspěvku do světové
ekonomiky*". **Ekonomika funguje jen s populací.** Při pár hráčích nevznikne
poptávka ani ceny — a smyčka se rozpadne. To není detail, to je nosný pilíř.

**Co navrhuju:**

| Místo | Navrhuju |
|---|---|
| „Bude to MMO" | **„Navrženo tak, aby MMO šlo přidat — ale MVP je single-player."** Architektura zůstane rozdělená na simulaci a zobrazení (to už `ARCHITEKTURA.md` má), takže se server dá připojit později bez přepisu jádra |
| „Příspěvek do světové ekonomiky" | **Simulovaná ekonomika**: svět má poptávku (kovárna chce rudu, vesnice chce zbraně), ceny reagují na to, co dodáš. **Funguje i v single-playeru** a je to zároveň přesně to „vidět vliv na svět", které chceš |
| „Živý svět" | **Stav světa, který se mění viditelně**: infestace roste, dokud ji nečistíš; vesnice je lépe vyzbrojená, když ji zásobuješ. Testovatelné a měřitelné |

Tohle je podle mě **nejcennější úprava, kterou ti můžu nabídnout** — zachová
zážitek, ale udělá z něj něco, co jde postavit a ověřit.

### 2.2 Plynulý všesměrový pohyb mění víc, než se zdá

**Není to jen „přepnout pohyb".** Naměřeno v projektu:

| Co dnes je | Co plynulý pohyb znamená |
|---|---|
| `player.move(dir)` = **jeden krok po izometrických osách**, pevná vzdálenost `SPEED/60` | pozice je **spojitá** (float) ve světových souřadnicích |
| Test měří „sklon posunu proti sklonu osy dlaždice" | test musí měřit zrychlení, zpomalení, rychlost |
| `z_index` celá čísla (hráč 5, zeď 0) | **spojité řazení podle hloubky** — jinak bude postava „na střeše" |
| kolize = „uklouznutí po jedné ose" (`_step`) | **samostatný systém kolizí** (tělesa se nesmí překrývat) |
| **4 směry** spritů (`spec.json: role.player.smery = 4`) | pro plynulé otáčení je potřeba **8 směrů** → **dvojnásobek grafiky** |

**To poslední je konkrétní a drahé:** dnes je 4 vrstvy × 4 směry × 8 framů =
**128 obrázků** na postavu. Při 8 směrech je to **256 na postavu** — a pro každý
kus výbavy znovu.

**Co navrhuju:** plynulý pohyb **ano**, ale postavit ho na **pevném ticku**
(např. 50 ms) a s pozicí ve světových souřadnicích; mřížka zůstane jako
**kolizní a vykreslovací** vrstva. Osmi směry **odložit** — prototyp zvládne
4 směry a otočení „skokem"; vyhlazení se dodá, až bude pohyb fungovat.

### 2.3 Tři schémata ovládání nejdou „a nebo" — skládají se

Napsal jsi: „*držení pravého tlačítka a proximita kurzoru k postavě **a nebo**
toggle a stamina*". Podle mě to nejsou alternativy, ale **tři různé osy**:

| Prvek | Co vyjadřuje | Příklad |
|---|---|---|
| **Vzdálenost kurzoru** | **záměr** — jak rychle chci jít | kurzor blízko = pomalá chůze, dál = chůze, ještě dál = běh |
| **Stamina** | **rozpočet** — jak dlouho to vydržím | běh ubírá staminu, vyčerpaný zpomalíš |
| **Toggle** | **zámek** — držet tempo bez držení tlačítka | přepínač „jdi stále" pro dlouhé cesty |

**Praktické doporučení:** v MVP **držení pravého tlačítka + vzdálenost kurzoru**;
stamina jako jednoduchý ukazatel, který běh omezuje; toggle až později.

**A jedna věc, na kterou se zapomíná:** potřebuješ **mrtvou zónu** kolem
postavy (aby nekmitala, když kurzor stojí na ní) a **vyhlazení** (aby rychlost
neskákala). To je přesně to „vyladit rozběh a zastavení" — a je to
**testovatelné číslem** (doba do plné rychlosti ve ms, doba do zastavení).

### 2.4 Atrofie + synergie + strop = tři systémy najednou

Tvoje G-2 obsahuje **tři samostatné mechaniky**:

1. **Růst používáním** (skill roste, když ho použiješ)
2. **Synergie** (kladivo trénuje tupé zbraně; znalost kovů zrychluje tinkering)
3. **Atrofie** (nepoužívaný skill klesá)

Každá je sama o sobě jednoduchá; **dohromady tvoří systém, který se musí ladit**
— a ladění vyžaduje hraní, ne plánování.

**Co navrhuju:** v MVP **růst + strop + tabulka synergií** (synergie jako
**data**, ne kód — `assets/data/synergies.json`). **Atrofii zapnout přepínačem**,
ať je hotová, ale nesvazuje první ladění. Důvod: atrofie je trestající
mechanika, která dává smysl, až když je svět živý a hráč má důvod se vracet.

**A ještě jedna ostrá poznámka:** „*každá fáze skillu od 0 po max je důležitá*"
je krásný cíl, ale **je to tvrzení o ladění, ne o kódu**. Nedá se naplánovat —
dá se jen měřit. Patří to jako **kritérium**, ne jako úkol.

### 2.5 Free assety: ano na zvuk a UI, opatrně na hlavní vzhled

Free assety jsou dobrý nápad, ale mají **dvě pasti**:

1. **Stylová nekonzistence.** Cíl je „*předrendrovaný 3D model do 2D spritu,
   realistické světlo*" (`spec.json`). Žádná free sada izometrických dlaždic
   tomu nebude odpovídat — a míchání vypadá hůř než jeden horší, ale jednotný styl.
2. **Rozměry.** Free izometrické sady mají vlastní mřížku (typicky 64×32 nebo
   128×64), ne tvoji **96×48**. Přepočet rozbije ostrost.

**Kde je free assety brát hned:** **zvuk a hudba** (`assets/audio/` je prázdný
a `DESIGN.md` zvuk slibuje), **ikony a font pro UI**, případně **textury terénu**
(ty se dají obarvit do stylu).

**Kde ne:** hlavní vzhled postav, budov a předmětů.

### 2.6 A-1 — co ta otázka znamenala, a proč je tvoje odpověď správná i drahá

**Otázka nebyla o vkusu.** V projektu jsou **dvě sady obrázků** a hra používá
jen jednu:

| | Ploché | Vrstvené |
|---|---|---|
| Soubor | `assets/sprites/player.png` — jedna kresba celé postavy | `tools/blender/sprites/body_d0_f0.png` + `legs…` + `torso…` + `weapon…` |
| Ve hře | **používá se** | **nepoužívá se** (0 odkazů v kódu) |
| Co umí | nic nemění | **oblékání** — vyměníš vrstvu a postava má jinou zbroj |

**Tvoje odpověď („ať je vidět, co má nasazené") = vrstvení.** A je to správná
odpověď — je to věc, kterou UO odlišuje.

**Ale řeknu ti cenu, kterou to má, ať se rozhoduješ s otevřenýma očima:**

- Každý **kus výbavy** se musí vyrenderovat **ve všech směrech a všech framech
  animace**. Dnes: 4 směry × 8 framů = **32 obrázků na jeden kus**.
- **Tvoje otázka „meč v ruce, nebo u pasu?" je přesně ten násobič.** „V ruce"
  a „u pasu" jsou **dvě různé polohy téhož předmětu** — tedy 2× tolik obrázků
  pro zbraně. Není to nemožné, ale je to rozhodnutí, které má cenu udělat
  vědomě: **navrhuju MVP = zbraň jen v ruce**, „u pasu" přidat později.
- A pozor: dokud se nerozhodne o osmi směrech (§2.2), počet obrázků na kus
  není 32, ale **možná 64**.

**A co je důležitější:** **tuhle otázku nemusíš rozhodnout teď.** Tvoje vlastní
věta „*než bude vyvinutá grafika, budu rád za primitivní prototypy*" ji
**odkládá správně** — prototyp nakreslí postavu jako obdélník a vrstvení se
rozhodne, až bude stát hratelná smyčka. Přesně to dělá i `game-clone`: vrstvy
řeší, až když je vidět, že hra stojí.

### 2.7 Prototypy první — tohle je nejlepší věta celého vstupu

Projekt má **256 vyrenderovaných PNG** vrstvené postavy a hra je **sběračka
dvou mincí**. To je přesně ta nerovnováha, kterou tvoje věta opravuje.

**Navrhuju to zapsat jako pravidlo:** *„Dokud nefunguje smyčka, nevzniká žádná
grafika — jen primitivní tvary."* A k tomu konkrétně: prototyp = **barevné
obdélníky a kolečka** s popiskem, žádné sprity. Ušetří to týdny a udrží
pozornost na tom, co je drahé (mechaniky), ne na tom, co je vidět.

---

## 3. Co z toho plyne pro projekt

| # | Dnešní stav | Po tvých vstupech |
|---|---|---|
| 1 | Pohyb po krocích, zamčený na mřížku | **plynulý všesměrový**, mřížka jen kolizní a vykreslovací |
| 2 | Kolize „uklouznutí po ose" | **samostatný systém** — tělesa se nesmí překrývat |
| 3 | 4 skilly (`tezba, drevorubectvi, kovarstvi, boj_na_blizko`) | **synergie mezi skilly** jako data + strop + (přepínačem) atrofie |
| 4 | Ekonomika: `buy()`/`sell()` se 0 zlatem | **simulovaná poptávka světa** — hráč vidí vliv |
| 5 | Žádný stav světa | **viditelný stav**: infestace, zásobenost, kvalita |
| 6 | UI: jeden Label se skóre | **paperdoll, inventář, mapa** + stavové ukazatele |
| 7 | „MMO" mimo rozsah bez vysvětlení | **„navrženo pro MMO, MVP single-player"** + simulovaná ekonomika |
| 8 | Grafika se vyvíjela před hratelností | **prototyp z primitiv, grafika až po smyčce** |

---

## 4. Nové otázky, které tvá rozhodnutí otevírají

```
[ ] N-1  MMO: souhlasíš s „navrženo pro MMO, MVP single-player" a se
         simulovanou ekonomikou místo skutečné?            (§2.1)
[ ] N-2  Osmi směry pro plynulé otáčení: teď, nebo až po prototypech?
         (dvojnásobek grafiky na každý kus výbavy)          (§2.2)
[ ] N-3  Ovládání: beru „držení pravého tlačítka + vzdálenost kurzoru"
         jako MVP, stamina jako omezení běhu, toggle později?  (§2.3)
[ ] N-4  Atrofie: zapnout hned, nebo jako přepínač až po prvním ladění? (§2.4)
[ ] N-5  Synergie: jako data (`assets/data/synergies.json`) — souhlas?
[ ] N-6  Zbraň „v ruce" vs. „u pasu": MVP jen v ruce?        (§2.6)
[ ] N-7  Free assety: zvuk + UI + textury ano, hlavní vzhled ne — souhlas? (§2.5)
[ ] N-8  Co je „stav světa", který má hráč vidět? (infestace? zásobení?
         ceny? opotřebení cest?) — potřebuju aspoň dvě věci, které se dají měřit
[ ] N-9  Paperdoll v MVP: ano, nebo až s vrstvenou grafikou? (Je svázaný s A-1)
[ ] N-10 „Vysoce rewarding mistrovství": jak se to pozná? (Vizuálně? Novou
         akcí? Rychlostí?) — bez toho se to nedá postavit
```

---

## 5. Jak budeme pokračovat

Navrhuju **jít po vrstvách** a u každé říct: co je rozhodnuté, co je otevřené,
a co z toho plyne pro dokumenty. Pořadí odpovídá závislostem.

| Kolo | Vrstva | Co se u ní rozhodne | Hotovo, když… |
|---|---|---|---|
| **1** | 0 Záměr + 1 Zážitek | pilíře jako **pocity**, hlavní smyčka **větu po větě**, role | smyčka jde převyprávět bez zaváhání |
| **2** | 2 Míra úspěchu + 5 Non-goals | čím se pozná „to je ono", co tam **není** | každé tvrzení je měřitelné nebo zakázané |
| **3** | 3 Mechaniky + 4 Obsah | skilly, synergie, ekonomika, stav světa, obsah v číslech | každá mechanika má číslo nebo vzorec |
| **4** | 6 Technika + 7 Smlouvy | **R1** (architektura běhu), tick, pohyb, kolize, datové formáty | 15 chybějících smluv má tvar dat |
| **5** | 8 Plán + 9 Brány + 10 Pravidla | milníky jako **hratelné stavy**, brány, definice hotovo | každý milník je vidět na obrazovce |

**Termínem „kolo" nemyslím session** — může to být půl hodiny povídání. Jde
o to, **neotevírat vrstvu 3, dokud není uzavřená vrstva 1** — jinak se začne
ladit obsah proti smyčce, která se ještě změní.

---

## 6. R1 — co ta otázka znamenala (vysvětlení)

**Otázka zněla: „jaká je architektura běhu?"** Vysvětluju, protože to nebylo
srozumitelné.

**Dnešní stav:** celá hra je **jeden soubor** — `scripts/game.gd` (377 řádků).
Ten postaví mapu, vytvoří hráče, nakreslí dlaždice, spočítá mince, ukáže HUD,
umí hudbu a má v sobě i ukládání. Když se do něj sáhne, rozbije se všechno.

**Plán říká:** rozdělit ho na **komponenty** — každá dělá jednu věc
(`combat.gd`, `mining.gd`, `economy.gd`…). Ty komponenty **už existují**, ale
**nikdo je nezavolá** (naměřeno: hra jich používá 3 z 13).

**„Architektura běhu" = odpovědi na tři otázky, které mezi tím chybí:**

1. **Co se děje každý snímek a v jakém pořadí?** Nejdřív vstup, pak pohyb, pak
   souboj, pak překreslení? Kdo to řídí?
2. **Kdo je „kořen"?** Který uzel drží všechny komponenty a jak je najdou
   (dnes: `get_parent().component("Skills")`)?
3. **Jak spolu mluví?** Volá si souboj přímo ekonomiku, nebo si posílají
   **zprávy** („hráč zabil kostlivce" → loot → zápis do žurnálu)?

**Proč na tom záleží konkrétně:** bez odpovědi si každá komponenta vymyslí
vlastní — jedna bude počítat čas v `_process`, druhá v `_physics_process`,
třetí si udělá vlastní časovač. **A budou se hádat o to, co se stalo dřív.**
Přesně tomu se dá předejít tím, že se to napíše.

**Moje doporučení (k odsouhlasení, ne hotová věc):**

- **Pevný tik 50 ms** (20× za sekundu) pro simulaci; vykreslování zvlášť, jak
  nejrychleji to jde. Důvod: simulace je **opakovatelná** a **testovatelná** —
  stejný vstup dá stejný výsledek. `game-clone` to tak má a je to jeho
  nejsilnější technické rozhodnutí.
- **Kořen = jeden uzel** (`game.gd`), který vytvoří komponenty a předá jim
  registr.
- **Zprávy místo přímého volání** mezi vrstvami: simulace **nikdy** nesahá na
  obrazovku, jen plní frontu událostí; UI **nikdy** nemění stav přímo, jen
  posílá příkazy. *(To už `ARCHITEKTURA.md:102–104` říká — jen to není
  vynucené.)*

---

## 7. Co tenhle dokument neví

- **Nevím, jestli je MMO skutečně cíl, nebo „pocit světa".** Z tvého textu to
  čtu jako **pocit** — a proto navrhuju simulovanou ekonomiku. Když je to
  skutečně MMO, mění se celý plán a je potřeba to vědět **hned**.
- **Nevím, kolik lidí má hrát.** Od toho se odvíjí, jestli ekonomika potřebuje
  simulaci, nebo stačí hráči.
- **Nevím, co přesně znamená „vyšší potenciál"** v boji (G-5) — je to
  abstraktní a potřebuju to rozpadnout.
- **Neověřoval jsem, jak drahá je výroba 8směrné vrstvené grafiky** — číslo
  „2× proti dnešku" je odvozené z počtu souborů, ne měřené časem.
