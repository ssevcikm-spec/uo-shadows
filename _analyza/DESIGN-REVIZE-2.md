# Revize vize `uo-shadows` — kolo 1: Záměr a zážitek

> **Co tenhle dokument JE:** **pracovní stav revize vize** — zapisuje, co je
> v vizi **rozhodnuté**, co je **návrh k potvrzení** a co je **otevřené**,
> a u každého rozhodnutí **cenu**, kterou volba má.
>
> **Není to:** GDD ani zdroj pravdy o designu. Rozhodnuté smí být jen to, co
> uživatel **viděl a potvrdil** (skill `dialog-s-uzivatelem` §2: *co není
> převyprávěné a potvrzené, není rozhodnuté*).
>
> **Zadání:** `ZADANI-REVIZE-VIZE.md` — projít vizi po vrstvách v pěti kolech.
> **Vzniklo:** 8. 10. 2026, session 2 (ta, pro kterou bylo zadání napsané).
> **Doplněno:** 8. 10. 2026 — odpovědi uživatele na kolo 1 (viz §6 a §11)
> a otevřené **kolo 2** (viz §12).
> **Odkud brát stav:** tenhle dokument pro stav **vize**; technický stav projektu
> je v `_analyza/REKONSTRUKCE-ADD-TDD-GDD.md` a `_analyza/AUDIT-PLANU-A-DESIGNU.md`;
> otevřená témata napříč stanicí v `OTEVRENA-TEMATA.md` (workspace stanice).
> **Stav celé revize (8. 10. 2026): UZAVŘENO** — všech pět kol je
> zodpovězených (`K1`–`K5`, `R2-1`–`R2-5`, `M6`–`M8`, `R-1`/`N-2`/`N-9`/`R-3`,
> `P1`–`P4`), tři nepravdivá tvrzení v pravidlech jsou **opravená** (§15.5).
> **Zbývá jediné:** napsat **GDD → ADD → TDD** podle §8 — a teprve pak měnit
> roadmapu. **Jeden koncept zůstává otevřený** a je to pojmenované: čím platí
> řemeslník, když ne grindem (§13.8).
>
> **Stav kola 1 (8. 10. 2026):** **UZAVŘENO** — uživatel rozhodl `K1`–`K5`
> i odložení `A-1` (§6, §7, §11). **Odchylka od kritéria zadání, zapsaná
> a ne zamlčená:** smyčku **nepřevyprávěl** zpět svými slovy, ale odpověděl na
> **tři krajní případy** (§4) — což je podle skillu `dialog-s-uzivatelem` §2
> **stres test**, jiná (a tady **silnější**) metoda validace: odhalila
> **tři pravidla, která v návrhu smyčky nebyla** (těžba má hloubku; poptávka
> světa je tříděná a mění se; hnací silou je cíl s číslem).
> **Co se z tohohle dokumentu už provedlo:** rozhodnutí `K1`–`K5` zapsaná
> do §2–§7 a §11 (a tím i do zadání pro GDD), doplnění smyčky z §4, rozhodnutí
> o placeholder grafice (§7), architektonická podmínka pro cestu B (§11 → patří
> do `R-1`), a dva nálezy zanesené do ledgeru stanice.

---

## 1. Co jsem ověřil měřením (a co z toho nesedí)

Zadání §2 říká „neověřuj znovu, jen ověř, že sedí" — a zároveň žádá ověřit aspoň
tři klíčová tvrzení. **Ověřeno 8. 10. 2026** čtením souborů a počítáním
(`HEAD = bc51e46`; kdyby někdo tenhle dokument četl později, čísla jsou k tomu
commitu).

| # | Tvrzení zadání | Naměřeno 8. 10. 2026 | Sedí? |
|---|---|---|---|
| 1 | `project.godot` nemá ani jednu vstupní akci | sekce `[input]` obsahuje **jen** `input_devices=…`; výskytů `InputEvent` = **0** | ✅ |
| 2 | hra je sběračka dvou mincí, mapa 30×16, Label se skóre, chyba `tween_property`, nápověda inzeruje 5 kláves | mapa `main.json` = **16 řádků × 30 znaků**; markery: 1× spawn, **2× coin**, 1× exit; `help_label` (game.gd:221) inzeruje **6** kláves (`E, C, B, X, R, M`); `tween_property` na `modulate:a` je v `game.gd:140–141` | ✅ s upřesněním (5 → **6**) |
| 3 | 13 granul je `done`, hra používá 3 | roadmapa má **22 granul, z toho `done: true` = 13**; produkční kód ale instancuje **2** komponenty (`level.gd` a `player.gd` v `game.gd`) | ✅ / ⚠ hra používá **2**, ne 3 |
| 4 | dva výtvarné systémy: 256 vyrenderovaných PNG vs. 16 plochých | `tools/blender/sprites/**` = **258 PNG** (128 hráč + 128 NPC + `_compare.png` + `_player_vs_npc.png`), `assets/sprites/` = **16 PNG**; odkaz na vrstvené sprity v kódu mimo `tools/` = **0** | ✅ (256 snímků + 2 srovnávací) |
| 5 | `spec.json` je hotová ADD ve strojové podobě | 88 řádků: viewport, dlaždice, 8 rolí, 8 slotů vrstev, 6 bran s tolerancemi, směr stylu se zákazy, zrušená paleta s důvodem | ✅ |
| 6 | TDD má 18 smluv, tvar dat jen 3 | `ARCHITEKTURA.md` §2 má **18 řádků** (řádky 128–145), tvar dat ve třech pododdílech §2.1–2.3 | ✅ |
| 7 | obsah: 4 materiály, 4 skilly, 3 recepty, 1 nestvůra, 2 předměty | `materials.json` 4 (`iron_ore, wood, stone, iron_ingot`), `skills.json` 4, `recipes.json` 3, `monsters.json` 1 (`skeleton`), `items.json` 2 | ✅ |
| 8 | `engine.shell` blokuje mrtvá granule `world.map`, `world.gd` má 0 B | `scripts/world.gd` = **0 B**; `world.map` i `world.nodes` mají `done: false`; `engine.shell` na `world.map` závisí | ✅ |
| 9 | `docs/DESIGN.md` je zrušený, ale `AGENTS.md:91` na něj odkazuje jako na zdroj pravdy | `DESIGN.md:3` se sám hlásí „**Zrušeno jako zdroj pravdy**"; `AGENTS.md:91` o něm píše „*co hra je a jak se má chovat*" | ✅ |
| 10 | pravidla obsahují tři nepravdivá tvrzení | `CONVENTIONS.md:252` posílá na `_safe_spot(vp)` „(už v `game.gd` je)" — v `scripts/` je **0 výskytů**; `AGENTS.md:108–110` tvrdí, že rozhraní `add_rule` míchá jazyky (`"cíl mrtev"`), ale `assist.gd:15` má **`"target dead"`** → rozhraní je jazykově konzistentní; `CONVENTIONS.md:273` tvrdí „**26 kontrol**", zatímco měřený záznam v roadmapě (3. 10. 2026, spuštěním) uvádí **91 kontrol** | ✅ (třetí bod je zastaralý, ne přeměřený — viz §10) |

**Tři věci, které zadání neuvádí a měření je našlo:**

1. **`game.gd` v produkci instancuje 2 komponenty, ne 3.** Načítá `level.gd`
   (řádek 155) a `player.gd` (řádek 270); `hud.gd` **není** v produkční cestě
   vůbec — `hud` v `game.gd` je jen `Label`. To tvrdí i komentář v
   `tests/_snimek-hp.gd:12`. **Důsledek pro vizi:** hra dnes nepoužívá ani
   boj, ani výrobu, ani ekonomiku, ani ukládání — ne že je používá špatně.
2. **Nápověda inzeruje 6 kláves, ne 5** (`E, C, B, X, R, M`) — číslo v zadání
   je o jednu nižší. Na pointě to nic nemění (kód je neobsluhuje).
3. **Název hry uvnitř projektu je `uo-sandbox`, repo se jmenuje `uo-shadows`**
   (`project.godot` `config/name`, `assets/spec.json` `_popis`). Pravidlo
   stanice je „odkaz na projekt se odvozuje z názvu repa" — je to drobnost,
   ale patří na seznam k rozhodnutí (kolo 5).

---

## 2. ROZHODNUTO (8. 10. 2026) — záměr jednou větou (vrstva 0)

> **Potvrzeno uživatelem** (`K2`: „*Sedí*").

> **Živý izometrický sandbox, ve kterém si hráč vybere roli — řemeslník,
> obchodník, válečník, dobrodruh nebo hraničář — roste v ní tím, co dělá,
> a svět na jeho práci viditelně reaguje.**

**Pro koho:** pro hráče, který chce mít v herním světě **svou roli a svůj přínos**
— ne být vyvoleným hrdinou (odvozeno z uživatelova textu §1.3: *„Plnit roli
a užívat si roli mistra řemeslníka, obchodníka, válečníka, dobrodruha,
hraničáře"*).

**Odkud je znění:** `ARCHITEKTURA.md:9–17` („Moderní Ultima Online: izometrický
sandbox…") + uživatelův text v `DESIGN-PRACOVNI-VSTUPY.md` §1.3. Nové je jen to,
že role a reakce světa jsou v té větě **vyjmenované** — dřív byly schované
v seznamu featur.

**Cena rozhodnutí:** záměr je teď filtr — co neposiluje „roli, která roste
a kterou svět potřebuje", do hry nepatří. Ztrácí se tím volnost „přidat cokoli
zábavného": hra nebude o hrdinovi, který zachrání svět.

---

## 3. ROZHODNUTO (8. 10. 2026) — pilíře jako POCITY (vrstva 0)

> **Potvrzeno uživatelem** (`K2`: „*Sedí*"). **Otevřené zůstává jediné:**
> který pilíř je pro uživatele **hlavní rozhodčí** (viz `K2` v §6).

Současných 7 „pilířů" v `ARCHITEKTURA.md:19–27` jsou **featury** („synergie
skill + atribut", „svět škálovaný dovedností") — nedají se použít jako
rozhodovací pravidlo. Níž je pět **pocitů** odvozených z uživatelových slov,
každý s tím, co znamená pro rozhodování a **co vylučuje** (bez toho by pilíř
nebyl filtr, ale heslo).

| # | Pilíř (pocit) | Co znamená pro rozhodnutí | Co vylučuje |
|---|---|---|---|
| **P1** | **„Mám svou roli a svět ji potřebuje."** | Co posiluje, aby každá z pěti rolí měla co nabídnout, je v duchu hry | Příběh „vyvoleného", kde je hráč střed světa a ostatní profese jsou kulisa |
| **P2** | **„Rostu tím, co dělám — a je to vidět."** | Pokrok musí být vidět **v číslech** (úspěšnost, zranění, kvalita, konzistence), ne v odznaku | Dovednosti rostoucí za něco jiného než za své použití; „pocit pokroku" bez měřitelné změny |
| **P3** | **„Dovednosti se potkávají, ne soupeří."** | Vazby mezi dovednostmi jsou součástí designu (kladivo → tupé zbraně; znalost kovů → tinkering) | Pevné třídy a povolání, které kombinace zamknou; dovednosti, které spolu nesmí mluvit |
| **P4** | **„Každý stupeň umí něco — a mistr umí víc."** | I začátečník musí mít co dělat a vydělat; zároveň musí být poznat rozdíl proti mistrovi | Obsah, který dá začátečníkovi nulu; a obsah, kde je mistr zbytečný |
| **P5** | **„Co udělám, je ve světě vidět."** | Odměna se musí dát **uplatnit** a svět musí zareagovat (ceny, zásobenost, bezpečí) | Odměny bez odběratele a svět, který se nemění |

**Cena rozhodnutí:** pilíře nejsou práce, jsou to **filtry**. Každý navíc umí
zablokovat i dobrý nápad — proto jich je pět, ne deset. **Co by se ztratilo
bez nich:** každý další agent (a každá další session) si domyslí, „co je v duchu
hry", a za měsíc se dva návrhy budou hádat bez rozhodčího. To je přesně stav,
který má tahle revize odstranit.

### HLAVNÍ PILÍŘ — ROZHODNUTO (8. 10. 2026): `P2` — „Rostu tím, co dělám — a je to vidět."

Uživatel vybral tenhle jako **rozhodčího**: když si dva nápady odporují, vyhrává
ten, který **víc zviditelní měřitelný růst**. Co z toho plyne konkrétně:

- hra musí **brzy ukazovat čísla** — dnešní HUD umí jen „Skóre: 2 / 2", takže
  „růst je vidět" dnes nemá kde být vidět;
- „pocit pokroku" bez čísla je **proti hlavnímu pilíři**, i kdyby se líbil;
- platí to i na pilíř `P5` (vliv na svět): i ten se musí projevit **jako číslo
  nebo stav**, ne jako dojem („vesnice je zásobenější" musí být vidět).

**Cena:** `P2` tlačí na **měřitelnost už v prvním hratelném stavu** — což je
práce navíc (HUD, čísla dovedností, viditelný stav světa) a omezuje to
„náladové" prvky, které se nedají číslem doložit.

---

## 4. ROZHODNUTO (8. 10. 2026) — hlavní smyčka po větách (vrstva 1)

> **Potvrzeno uživatelem** (`K3`: „*Sedí*"), **ale ještě ne převyprávěno** —
> a podle skillu `dialog-s-uzivatelem` §2 platí: *co není převyprávěné
> a potvrzené, není rozhodnuté*. Převyprávění je proto jediná zbývající
> podmínka u tohohle bodu.

Značky: **[U]** = uživatelova slova, **[D]** = dotvořený krok (potvrzený).

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

**Smyčka zůstává 8 vět — ale tři z nich se zpřesňují** odpověďmi na krajní
případy níž: věta 1 (co svět potřebuje, se **mění**), věta 2 (těžba **má
hloubku**) a věta 8 (co hráče žene dál, je **cíl s číslem**).

### Doplnění z krajních případů (8. 10. 2026) — a co to mění

Uživatel místo převyprávění odpověděl na **tři krajní případy** — což je podle
skillu `dialog-s-uzivatelem` §2 **stres test**, jiná metoda validace, a v tomhle
případě **silnější**: odhalila tři pravidla, která v návrhu smyčky nebyla.

**(a) „Hráč deset minut jen těží a nic neuplatní — co se stane?"**

> *„A — dostává materiály, hlubší těžbou získává obtížněji získatelné (pokud může
> zdroj obsahovat směsku, pak delší těžba zvyšuje zisk vzácnějších materiálů),
> roste mu dovednost."*

**Co to mění:** těžba **není plochá** („klik → jeden kus rudy"). Zdroj má
**obsah** (běžná + vzácná složka) a **trvání**; delší těžba se vyplácí.
A i bez uplatnění roste dovednost — takže **smyčka není blokovaná obchodem**;
kdo jen těží, není v slepé uličce. *(Do kola 3 patří: výnosový vzorec a jestli
mají být i zdroje jednodruhové.)*

**(b) „Hráč nemá co prodat, protože svět nic nechce — je to vada, nebo plán?"**

> *„B — svět to nemusí chtít, ale to se může změnit. Něco je odpad, něco se dá
> recyklovat, něco je situační."*

**Co to mění:** předpoklad „svět má vždycky poptávku" **neplatí**. Věci se dělí
aspoň na **tři třídy**: **odpad** (nikdo ho nechce), **recyklovatelné** (dá se
vrátit do výroby) a **situační** (chce se to jen za nějaké situace — např. když
roste infestace). Poptávka se navíc **mění v čase**. *(Do kola 3 patří: které
předměty do které třídy a co poptávku mění.)*

**(c) „Hráč dělá totéž po sté — co ho přiměje jít dál?"**

> *„C — Pokrok nebo dosažení cíle — chtěl 100 dávek lektvaru?"*

**Co to mění:** hnací silou není jen „svět má novou poptávku", ale **cíl
s číslem** („100 dávek lektvaru"). Zůstává otevřené, **kdo ten cíl zadává** —
svět (zakázka), nebo hráč sám (vlastní cíl) — a to je otázka kola 2, protože
od ní se odvíjí, jestli je potřeba systém zakázek, nebo jen viditelné počítadlo
cílů.

**Cena rozhodnutí:** 8 vět = **8 systémů, které se musí potkat**. Dokud jedna
věta nefunguje celá, hra není hotová — i kdyby všechno ostatní klapalo. Kratší
smyčka by byla rychlejší, ale hůř by udržela pocit živého světa.

> **⚠ Rozsahový rozdíl, který je fér vidět hned:** smyčka výš mluví o výpravách,
> dungeonech, infestacích a šlechtění zvěře — **skutečný obsah hry je dnes
> 4 materiály, 4 dovednosti, 3 recepty, 1 nestvůra a 2 předměty** (§1, řádek 7).
> Rozdíl je **řádový**. Čísla se rozhodnou ve **kole 3** (rozsah v číslech),
> ale nemá smysl potvrzovat smyčku, aniž by bylo řečeno, že je to takhle velký
> skok. *Poznámka: „dungeon" a „šlechtění" jsou dnes **slova**, ne systémy —
> v GDD budou muset být buď v rozsahu, nebo v non-goals.*

---

## 5. ROZHODNUTO (8. 10. 2026) — jak hráč pozná úspěch (vrstva 1/2)

> **Potvrzeno uživatelem** (`K4`: „*Od každého kousek — strop i možnosti*").

Úspěch nemá jedno číslo. Pozná se na **třech místech**:

1. **V číslech** — úspěšnost zásahu, zranění, doba přežití, kvalita, ztrátovost,
   konzistence. (To dnešní hra neumí zobrazit: má jen „Skóre: 2 / 2".)
2. **V nových možnostech** — co mistr umí a začátečník **vůbec ne** (modifikace
   produktu, ochočení zvířete).
3. **Ve světě** — co je díky mně lepší (zásobenost, bezpečí, ceny).

**„Vyšší potenciál" = ROZHODNUTO jako „vyšší strop I odemčené možnosti"**
(varianty (a) + (c) z původní nabídky). Znamená to konkrétně:

- **strop**: s rostoucí dovedností a lepším vybavením roste **horní mez**
  (max. zranění, max. kvalita, max. konzistence) — mistr tedy není jen rychlejší,
  ale **dosáhne výš**;
- **možnosti**: na určitých stupních se **odemykají akce, které začátečník
  nemá vůbec** (modifikace produktu, ochočení a šlechtění zvěře).

**Cena rozhodnutí:** jsou to **dva mechanismy místo jednoho** — strop se ladí
čísly, odemykání je **obsah k postavení** (každá odemčená možnost musí existovat
i pro toho, kdo ji nemá: musí být vidět, že na ni nemá). Varianta „jen strop"
by byla levnější, ale zmizel by kvalitativní skok, který dělá mistrovství
„rewarding".

**Co tím zůstává otevřené do kola 2:** kolik stupňů dovednosti je a co se na
kterém odemyká (to je míra úspěchu a mechaniky, ne záměr).

---

## 6. Otázky kola 1 — a jak dopadly (8. 10. 2026)

### Výsledek

| Otázka | Odpověď uživatele | Rozhodnutí a jeho cena |
|---|---|---|
| `K1` | nejdřív vlastní otázky („*MMO je nereálné… lze kombinovat třeba solo hru, do které se někdo přidá?*"), pak: „**Pokud je ekonomické a nedestruktivní, že se vytvoří i síťová vrstva, tak jsem pro ni, jinak volím doporučené A + architektura připravená**" | **ROZHODNUTO: A + architektura připravená na B** (§11). Podmínka „nedestruktivní" **platí** (oddělená simulace = síť je vyměnitelná doprava, ne přepis jádra); podmínka „ekonomické" **neplatí** (síť je samostatný milník **a trvalá služba**). **Cena:** síť se teď neřeší, ale architektura se kvůli ní nesmí zanedbat |
| `K2` | „**Sedí**"; hlavní pilíř: „**P2 — Rostu tím, co dělám — a je to vidět**" | záměr i pět pocitů potvrzeno (§2, §3), **hlavní rozhodčí = `P2`** (§3). **Cena:** každý pilíř je filtr, který umí zablokovat i dobrý nápad; a `P2` znamená, že se **čísla musí ukazovat brzy** |
| `K3` | „**Sedí**" | smyčka na 8 vět platí jako definice „dojeté hry" (§4). **Cena:** 8 systémů, které se musí potkat. **Otevřené:** převyprávění uživatelem |
| `K4` | „**Od každého kousek — strop i možnosti**" | „vyšší potenciál" = strop **i** odemčené možnosti (§5). **Cena:** dva mechanismy místo jednoho |
| `K5` | „**Souhlas**" | ovládání pro MVP potvrzeno (§6 `K5` níž). **Cena:** plynulý pohyb znamená předělat pohyb, kolize i řazení hloubky — v prototypech z primitiv levné |
| `A-1` | „**Sice souhlasím, ale zdráhavě**" + chce místo obdélníků primitivní vektorovou grafiku nebo free assety | odložení potvrzeno **s úpravou o placeholdery** — viz §7 |

### Znění otázek (původní, bez úprav — je to záznam, co se ptalo)

**Jak odpovídat:** zkráceně (`K1 A, K2 sedí, K3 vlastní: …`).

#### K1 — Svět: opravdoví hráči, nebo svět, který se chová, jako by žil?

```
Co už víme:  „Hra nemá konec, bude to mmo" (tvoje slova, §1.6).
             Projekt dnes říká: „simulace běží lokálně (single-player);
             server/MMO vrstva až později" (ARCHITEKTURA.md:34).
             A smyčka stojí na „příspěvku do světové ekonomiky".
Návrh:       Navrženo tak, aby MMO šlo přidat, ale MVP je JEDEN hráč —
             a svět místo živých lidí SIMULUJE: má poptávku (kovárna chce
             rudu, vesnice chce zbraně), ceny reagují na to, co dodáš,
             a jeho stav je vidět (infestace roste, dokud ji nečistíš;
             vesnice je lépe vyzbrojená, když ji zásobuješ).
Cena návrhu: Ekonomika je „divadlo" — čísla řídí model, ne lidé. Nikdy
             nepocítíš, že ti cenu přebil jiný hráč. Ale funguje i o samotě.
Cena druhé cesty (skutečné MMO hned): server, přihlašování, autoritativní
             simulace, ochrana proti podvodům, provoz — a hlavně ŽIVÍ HRÁČI:
             bez populace poptávka nevznikne a smyčka se rozpadne. Odhadem
             jiný projekt, ne „přidat na konec"; a bez lidí nefunguje ani tak.
Dopad:       Rozhoduje o CELÉM plánu: hra pro jednoho se simulovaným světem,
             nebo služba pro mnohé.
```

#### K2 — Záměr a pilíře: je to takhle?

```
Co už víme:  Dnešních 7 „pilířů" (ARCHITEKTURA.md:19–27) jsou FEATURY
             („synergie skill + atribut"), ne pocity. Tvoje věty o pocitu
             jsou v DESIGN-PRACOVNI-VSTUPY.md §1.3.
Návrh:       Jedna věta o hře (§2) + pět pocitů (§3) — každý s tím,
             co vylučuje. A odpověz i na: KTERÝ pilíř je pro tebe hlavní
             (podle kterého se rozhodne, když si dva návrhy odporují)?
Dopad:       Pilíř je jediné rozhodovací pravidlo, které přežije změny
             plánu. Co v pilířích není, se v hře neuhlídá.
Cena:        Každý pilíř navíc je další filtr, který umí zablokovat dobrý
             nápad — proto jich je pět, ne deset.
```

#### K3 — Hlavní smyčka: sedí těch 8 vět?

```
Co už víme:  Dnes existuje JEDNA věta: „těžit → tavit → kovat → používat
             → opravovat" (ARCHITEKTURA.md:32). Z tvého textu je smyčka
             „výprava → odměna → uplatnění → vliv na svět i ekonomiku".
Návrh:       8 vět v §4; každá je kus hry, který musí fungovat CELÝ.
Dopad:       Tohle je definice „dojeté hry". Dokud jedna věta nefunguje
             celá, hra není hotová — i kdyby všechno ostatní klapalo.
Cena:        8 vět = 8 systémů, které se musí potkat. Kratší smyčka
             (4 věty) je rychlejší, ale hůř udrží pocit živého světa.
A navíc:     Napiš mi ji zpátky SVÝMI SLOVY (dvě až tři věty).
```

#### K4 — Jak hráč pozná, že si vede dobře? A co je „vyšší potenciál"?

```
Co už víme:  Tvoje čísla: úspěšnost zásahu, zranění, přežití, kvalita,
             ztrátovost, konzistence, spolehlivost hraničáře. A slovo
             „vyšší potenciál", které se měřit nedá.
Návrh:       Úspěch se pozná na třech místech: v číslech, v nových
             MOŽNOSTECH (co mistr umí a začátečník ne) a ve světě.
             A „vyšší potenciál" = (a) vyšší strop, (b) rychlejší růst,
             (c) víc možností.
Dopad:       Podle toho se ve kole 3 počítají vzorce dovedností.
Cena:        (a) mistr narazí na strop; (b) hloubka se nezvýší, jen se
             zrychlí cesta; (c) každá odemčená možnost je nový obsah.
```

#### K5 — Ovládání pro první hratelnou verzi: takhle?

```
Co už víme:  Tvoje slova (§1.2): plynulý pohyb mimo mřížku, všesměrový,
             vyladěný rozběh a zastavení, primárně myš — „držení pravého
             tlačítka a proximita kurzoru k postavě (a nebo toggle
             a stamina) rozhodují o rychlosti".
Návrh:       Držení PRAVÉHO TLAČÍTKA = jdu. VZDÁLENOST KURZORU od postavy
             = jak rychle (těsně u postavy = stojím, pak pomalá chůze /
             chůze / běh). STAMINA = jak dlouho běžím. TOGGLE („jdi stále")
             až později. Klávesy WASD/šipky zůstanou jako záložní cesta
             (pro testování, nestojí to nic).
             A k tomu: svět zůstane DLAŽDICOVÝ (dlaždice určují, kudy se dá
             jít, a kreslí se po nich) — plynulá je POSTAVA po nich, ne
             mřížka. V prototypu bude postava obdélník, takže „4 nebo
             8 směrů" se rozhodne, až bude grafika (8 směrů = 2× obrázků
             na každý kus výbavy, tj. dnes 32 → 64 na kus).
Dopad:       Bez toho nemá ADD ani TDD co popsat — tohle je „jak se hra
             hraje" pro první minutu.
Cena:        Plynulý pohyb znamená předělat pohyb, kolize i řazení hloubky
             (dnes se postava hýbe po krocích po dlaždicích a řadí se
             celými čísly). V prototypu z primitiv je to ale levné —
             drahé by bylo dělat to až s hotovou grafikou.
```

---

## 7. ROZHODNUTO — odložená témata a placeholdery

| Kolo | Vrstva | Co se v něm rozhodne | Otevřené body, které tam patří |
|---|---|---|---|
| **2** | Míra úspěchu + Non-goals | čím se pozná „to je ono", co tam **není** | `N-10` („vysoce rewarding mistrovství" — jak se to pozná), **prvních 5 minut** (`G-9`), rozsah v číslech (`G-6`), non-goals (`G-7`), které z 13 `REQ-*` patří do MVP (`G-8`), potvrzení obsahu obrazovky (`G-4`), počet stupňů dovednosti a co se na kterém odemyká (§5) |
| **3** | Mechaniky + Obsah | každá mechanika má číslo nebo vzorec | `N-4` (atrofie hned / přepínačem), `N-5` (synergie jako data), `N-8` (co je „stav světa" — aspoň dvě měřitelné věci), `N-6` (zbraň v ruce vs. u pasu), `A-2` (SDXL/Blender), obsah v číslech |
| **4** | Technika + Smlouvy | tick, pohyb, kolize, datové formáty | `R-1` (architektura běhu — nejdřív vysvětlit lidsky), `N-2` (osm směrů), `N-9` (paperdoll v MVP), `R-2` (výkonnostní rozpočet), `R-3` (jazyk obsahu), 15 chybějících tvarů dat |
| **5** | Plán + Brány + Pravidla | každý milník je vidět na obrazovce | milníky jako hratelné stavy, brány, definice hotovo, **kdo vlastní který dokument**, název hry (`uo-sandbox` vs `uo-shadows`), oprava tří nepravdivých tvrzení v pravidlech (§1, řádek 10) |

### `A-1` (který výtvarný systém je budoucnost) — VĚDOMĚ ODLOŽENO, ale prototyp nebude „ošklivý"

Uživatel odložení **potvrdil** („*sice souhlasím, ale zdráhavě*") a řekl, co mu
na holých obdélnících vadí:

> *„Jestli to jde, preferoval bych předgenerování primitivní vektorové grafiky —
> předpokládám, že to je velmi levné — nebo předstažení assetů, které jsou
> zdarma — na internetu jsou celé tuny."*

**To je proveditelné a levné — s jednou podmínkou.** Podmínka není styl, ale
**rozměr**: dlaždice 96×48, postava 96 px, okno 960×540 (`assets/spec.json`).
Když placeholder tenhle rozměr nedodrží, **rozpadne se rozvržení mapy** a při
přechodu na finální grafiku se předělává scéna, ne obrázky.

| Cesta k placeholderům | Cena | Riziko |
|---|---|---|
| **Generovaná primitiva** (kód nakreslí kosočtverec dlaždice, postavu ze dvou–tří tvarů, rudu jako hromádku) | jeden malý úkol, **zdarma**, barva = druh suroviny | žádné — vzor už v kódu je (`game.gd:_visual` kreslí barevný obdélník, když sprite chybí) |
| **Free assety jako placeholdery** | stahování + kontrola licence + převzorkování na 96×48 | **jiná mřížka** (free izo sady bývají 64×32 nebo 128×64) → rozbité rozměry; styl nevadí, ten je dočasný |

**Rozhodnutí:** primitiva **jako základ** (zdarma a konzistentní), free assety
**na to, co mřížku nemá** — ikony, UI, zvuk (což je i doporučení
`DESIGN-PRACOVNI-VSTUPY.md` §2.5). **Finální vzhled zůstává nerozhodnutý**
a vrací se ve **kole 4** s číslem, kolik obrázků vrstvená postava znamená.

**Cena:** prototyp bude čitelnější a bude se líp hrát (což je pro ladění smyčky
důležité), ale **není to investice do finálního vzhledu** — až se vrstvená
grafika rozhodne, placeholdery se zahodí. Kdo si je splete s cílem, udělá
z prototypu slepou uličku.

---

## 8. PŘEDBĚŽNÁ OSNOVA GDD, ADD a TDD (co v nich bude a co chybí)

**Tohle ještě nejsou dokumenty** — je to osnova, podle které se napíšou, až se
vize uzavře. Pravidlo ze zadání §6.4 platí: **nové dokumenty se nezakládají
vedle starých** — `docs/DESIGN.md` a `docs/ARCHITEKTURA.md` se **nahradí**.

| Dokument | Nahradí | Co v něm musí být | Co už existuje | Co chybí |
|---|---|---|---|---|
| **GDD** | `docs/DESIGN.md` (dnes sám „zrušený") | cíl větou, pilíře-pocity, hlavní smyčka po větách, delší smyčky (sezení / meta), ovládání, co je na obrazovce, prvních 5 minut, jak hráč pozná úspěch, rozsah v číslech, **non-goals** | `ARCHITEKTURA.md` §0 (cíl, 7 featur-pilířů, 13 `REQ-`, obsah MVP), `DESIGN.md` (out-of-scope), `assets/data/*.json` | **kola 1–2** — tedy skoro všechno, co dělá hru hrou; z kola 1 už je hotové: záměr, pilíře, smyčka, úspěch, ovládání |
| **ADD** | nic — `assets/spec.json` zůstává strojová část | jak hra vypadá a **proč**; katalog assetů („co má být vyrobeno" vs. „co existuje"); dokumentace pipeline (Blender / SDXL); rozhodnutí ploché vs. vrstvené; zvuk | `spec.json` (rozměry, role, vrstvy, 6 bran, styl se zákazy, zrušená paleta), `tools/blender/*`, 16 plochých spritů | lidská vrstva, katalog, pipeline, `A-1`, zvuk (`assets/audio/` neexistuje) |
| **TDD** | `docs/ARCHITEKTURA.md` | architektura běhu (tick, kořen, jak spolu mluví), 8 vrstev, 18 smluv **s tvarem dat**, datové formáty, vlastnictví stavu, výkonnostní rozpočet, ukládání, chybové chování, jazyk rozhraní | `ARCHITEKTURA.md` §1–2 (18 smluv, 3 s tvarem dat), `CONVENTIONS.md`, kód | `R-1`, `R-2`, `R-3`, **15 tvarů dat**, formáty `assets/levels/*.json` vs `assets/data/*.json` |

**Pořadí psaní:** GDD → ADD → TDD (každý se odvozuje z předchozího).
**Až po nich** se smí sáhnout na `.forge/roadmap.json` — ta je zdroj pravdy
orchestry a mění se až podle uzavřené vize (zadání §6.5).

---

## 9. Kdo co vlastní a kde to je

| Rozhodnutí | Vlastník | Kde je zapsané |
|---|---|---|
| vize, pilíře, smyčka, rozsah, non-goals, co se má zlikvidovat | **uživatel** | `_analyza/DESIGN-PRACOVNI-VSTUPY.md` (vstupy) → **tento dokument** (rozhodnutí s cenou) |
| měření, návrhy, zápisy, dokumenty, brány | agent | `_analyza/*`, `docs/*` po přepisu |
| trvalá pravidla hry a stanice | **uživatel** | `AGENTS.md`, `CONVENTIONS.md`, `DSH_HOME\AGENTS.md` |
| plán granulí | orchestra (nástroj), **mění se až po uzavření vize** | `.forge/roadmap.json` |
| strojová podoba vzhledu | projekt | `assets/spec.json`, `.forge/vision-profile.json` |
| otevřená témata napříč stanicí | kdokoli, kdo téma otevře | `OTEVRENA-TEMATA.md` (workspace stanice) |

---

## 10. Co tenhle dokument neví (a co záměrně nezměřil)

- **Nespouštěl Godot ani brány** — zadání §0 to zakazuje. Proto:
  běhová chyba `tween_property` **není přeměřená** (v kódu je podezřelé místo
  `game.gd:141`: `hud` se používá bez kontroly na `null`, zatímco `level` na
  řádku 137 kontrolu má — to je **hypotéza, ne měření**), a počet kontrol
  v testech **není přeměřený** (proto §1 řádek 10 říká „zastaralé", ne „špatné").
- **Nevím, kolik hráčů je potřeba, aby ekonomika „žila"** — v §11 je to
  označené jako **odhad**, ne měření.
- **Nevím, kolik z 258 vyrenderovaných PNG je použitelných** — naměřena je jen
  jejich existence a struktura.
- **Nečetl jsem `tools/blender/*.py` do hloubky** — patří do ADD jako
  dokumentace pipeline.
- **Nevím, jak vypadá UI** — `hud.gd` existuje, ale hra ho neinstancuje (§1),
  takže „co je na obrazovce" je dnes jen `Label` se skóre a nápověda 6 kláves.
- **Uživatel ještě nezodpověděl:** který pilíř je hlavní rozhodčí; a nepřevyprávěl
  smyčku zpátky (obojí je v §6 a obojí je levné doplnit).

---

## 11. `K1` — svět a ostatní hráči: uživatel se ptá zpět (a odpovědi)

**Uživatel 8. 10. 2026 (doslovně):**

> *„Upřímně se mi nedaří vyhmátnout přesně co bych chtěl. MMO je nereálné.
> Nebudu vést server, udržovat hru, neseženu hráče. Kolik hráčů je potřeba aby
> hra byla živá a persistentní? Fungoval by multiplayer? Co když přestanou hrát,
> svět umře? A co MMO, které relativně žije a umí rychle a účinně zakomponovat
> nové hráče, takže nevadí, že odejdou, ale jejich příchod a akce pozitivně
> ovlivní živost světa? Jak náročná by byla primitivní simulace světa, aby si to
> hráč mohl užít solo? Lze kombinovat třeba solo hru, do které se někdo přidá?"*

**To je nejlepší možná odpověď na tuhle otázku** — nehledá „MMO ano/ne", ale
**„jak mít živý svět, který nemusím provozovat"**. Odpovídám po bodech; kde
nemám měření, je to označené jako **odhad**.

### 1) Kolik hráčů je potřeba, aby byl svět živý? *(odhad, ne měření)*

Jsou to dvě různé otázky:

- **Aby se svět hýbal** — **nula hráčů.** Hýbe ho simulace.
- **Aby ekonomika byla ze hráčů** (někdo kupuje, někdo prodává) — **desítky
  hráčů současně a denně.** Pod tím je obchod prázdný, každý si všechno vyrobí
  sám a „světová ekonomika" je jeden člověk, který prodává sobě. Naměřeno to
  nemám; je to odhad podle toho, jak vypadají malé hobby shardy.

**Důsledek:** ekonomika **ze hráčů** není cesta pro tuhle hru. Simulovaná
poptávka není náhrada za lidi — je to **jiný a dostupný způsob**, jak mít
ekonomiku vůbec.

### 2) Fungoval by multiplayer? Ano — ale není to „přidat na konec"

- **Dva až čtyři hráči, jeden z nich hostitel** (jeho počítač počítá svět,
  ostatní se připojí): technicky zvládnutelné a svět žije, dokud hostitel hraje.
- **Ale pozor na prohlížeč:** hra se publikuje na GitHub Pages (statické
  stránky) a **prohlížeč neumí naslouchat na síti** — takže i tahle varianta
  potřebuje **alespoň jednu malou trvale běžící službu** (spojovací/relay).
  To je přesně ten „provoz", který nechceš. Není velký, ale je to služba,
  kterou musíš držet při životě.

### 3) Co když přestanou hrát — umře svět? Ne, a je to levné

Dva modely, **oba bez serveru**:

- **Zastavený čas:** svět se mění, jen když někdo hraje. Nikdo nehraje → nic se
  nemění, stav zůstává. (Nejlevnější.)
- **Dopočet:** když se vrátíš, svět se **doměří podle pravidel** („zatímco jsi
  byl pryč, infestace vzrostla o X, vesnice spotřebovala Y").
  **A to už v plánu je:** roadmapa má granuli `sim.offline`
  (`resolve(char, job, hours)` s denním stropem) — „svět žije i bez tebe" je
  tedy **jeden systém**, ne nový projekt.

### 4) „MMO, které rychle zakomponuje nové hráče a jejich příchod ovlivní živost světa"

To je **persistentní sdílený svět**: příspěvky se sčítají do jednoho stavu.
Rozdíl proti solo je **jediná věc — kde ten stav leží**:

- **solo:** stav je u hráče → každý má **svůj** svět;
- **sdílený:** stav leží na serveru → příspěvky se sčítají.

A to je ta část, která potřebuje **trvalý server, databázi a identitu hráče** —
tedy to, co jsi označil za nereálné. *Poznámka: „rychlé zakomponování nového
hráče" je z 90 % design (nový hráč musí mít co dělat hned), ne technologie.*

### 5) „Jak náročná by byla primitivní simulace světa, aby si to hráč užil solo?" *(odhad)*

**Kód je levný, ladění je drahé.**

- Simulace je pravidla + čísla + tik, **žádná grafika**: jeden až dva systémy
  (řádově 200 řádků + datový soubor + jedna obrazovka, která stav světa ukáže).
  Pro srovnání: komponenty v tomhle projektu mají 15–283 řádků a roadmapa je
  plánuje po 80–140 řádcích.
- Drahé je **najít čísla, při kterých to působí živě** — a to se nedá naplánovat,
  jen odehrát. Proto je simulace dobrý první krok: **je vidět na obrazovce
  a dá se ladit hraním.**

### 6) „Lze kombinovat solo hru, do které se někdo přidá?"

Ano — a je to **nejschůdnější multiplayer**, protože nepotřebuje trvalý server
(jen tu malou spojovací službu z bodu 2). Má to ale jednu podmínku, která se
rozhoduje **skoro zdarma a právě teď**: simulace musí být **oddělená od
zobrazení** a počítat **stejně na všech strojích** (pevný tik, žádné náhody
závislé na snímcích). To je přesně to, co `ARCHITEKTURA.md:102–104` už říká
a co patří do TDD — takže „připravit se na to" dnes nestojí skoro nic, kdežto
„dodělat to později" by znamenalo přepsat jádro.

### Tři cesty (a co která stojí)

| Cesta | Co to je | Co stojí | Co se ztratí |
|---|---|---|---|
| **A — Solo + simulovaný svět** | svět se hýbe sám podle pravidel, hraješ sám | **žádný server**; 1–2 systémy + obrazovka stavu světa | nikdy nepocítíš cizího hráče |
| **B — Solo, ke kterému se přidá 2–4 hráči** | svět běží u hostitele; svět žije, dokud hostitel hraje | **všechno z A** + architektura připravená od začátku (**skoro zdarma**) + jeden milník na síť + **malá trvalá služba** (prohlížeč neumí naslouchat) | musíš držet službu; a je to práce navíc před prvním hraním |
| **C — Persistentní svět pro víc hráčů** | sdílený stav, příspěvky se sčítají, nový hráč rychle zapadne | **všechno z A+B** + trvalý server, databáze, identita, řešení konfliktů | to je MMO, které jsi označil za nereálné — odhadem měsíce a trvalý náklad |

**Co z toho plyne:** **A je předpokladem B i C** — rozhodnout A tedy nic nezavírá
a je to první krok, ať se rozhodneš jakkoli. Zbývá jediná otázka, která se má
rozhodnout **teď**: *má se architektura od začátku dělat tak, aby šla B přidat?*
Je to skoro zdarma a kdyby se to zanedbalo, B by znamenalo přepis jádra.
**C navrhuju vědomě odložit**, dokud A nefunguje: rozhodovat o serveru a databázi
dřív, než je co sdílet, je práce do prázdna.

### ROZHODNUTÍ (8. 10. 2026): cesta **A + architektura připravená na B**

Uživatel odpověděl podmíněně:

> *„Pokud je ekonomické a nedestruktivní, že se vytvoří i síťová vrstva, tak jsem
> pro ni, jinak volím doporučené A + architektura připravená."*

**Obě podmínky se rozpadly na dvě a mají různý výsledek** — proto rozhoduje
ta druhá:

| Podmínka | Platí? | Proč |
|---|---|---|
| **nedestruktivní** | **ANO** | Když se simulace udělá oddělená od zobrazení (pevný tik, stav jako data, příkazy místo přímého sahání na obrazovku), je síť **vyměnitelná doprava**, ne přepis jádra. Přesně to `ARCHITEKTURA.md:102–104` už předepisuje — a je to **právě teď skoro zdarma** |
| **ekonomické** | **NE** | Síťová vrstva je **samostatný milník** (synchronizace stavu, kdo je autorita, připojení a odpojení, konflikty při ukládání) **a k tomu trvalá služba**, protože prohlížeč neumí naslouchat na síti. Bezplatné tarify existují *(neověřováno)*, ale i bezplatná služba je **služba, kterou musíš držet** — a když padne, hra se nespustí |

**A ještě jeden důvod, proč síť ne teď (a je to ten nejtvrdší):** uživatel sám
řekl, že **nesežene hráče** — a co-op se **nedá ověřit bez druhého hráče**.
Postavit vrstvu, kterou nemá kdo vyzkoušet, znamená stavět naslepo: dvě okna
na jednom počítači ověří, že se něco přenáší, ale ne že to spolu dva lidé vydrží
hrát hodinu.

**Co je tím rozhodnuté:**

- **Teď:** cesta **A** (solo + simulovaný svět) — a architektura se udělá tak,
  aby B byla **doplňková vrstva**: oddělená simulace, pevný tik, stav jako data,
  příkazy a události místo přímých volání. **Tohle je ta část, která se rozhoduje
  dnes** (a v kole 4 se promítne do `R-1`).
- **Později:** **B zůstává otevřená jako samostatný milník** s vlastním
  rozhodnutím — v momentě, kdy bude co sdílet a bude s kým to vyzkoušet.
  Není to zamítnuté, je to **zařazené**.
- **C** (persistentní sdílený svět) — **odloženo**, dokud A nefunguje.

**Cena rozhodnutí:** architektura musí od začátku dodržet oddělení simulace
a zobrazení (což je disciplína navíc při každé nové komponentě), a výměnou
se nezavírá cesta k multiplayeru. Kdyby se oddělení porušilo, B by znamenala
přepis jádra — a to je přesně to, co si uživatel nepřeje.

---

## 12. KOLO 2 — Míra úspěchu, non-goals, prvních 5 minut, rozsah

> **Stav:** **UZAVŘENO** (8. 10. 2026) — všech pět otázek `R2-1`–`R2-5` (§12.6)
> je zodpovězených; **výsledky a ceny jsou v §12.7**.

### 12.1 Dvě rozhodnutí, která vyplynula z kola 1

| Otázka | Odpověď uživatele (8. 10. 2026) | Rozhodnutí a jeho cena |
|---|---|---|
| **Kdo zadává cíl s číslem?** | „**Obojí — svět zadává, hráč si může dát vlastní**" | Ve hře bude **systém zakázek** (svět objednává: „100 dávek lektvaru") **i vlastní cíl hráče** (počítadlo). **Cena:** dva systémy místo jednoho; musí se rozhodnout, co se stane, když si odporují (návrh: neodporují si — zakázka je cíl „od světa", vlastní cíl je „můj", a jdou vedle sebe) |
| **Složení zdroje** | „**Směs u všech zdrojů**" | Každý zdroj má **běžnou i vzácnou složku**; delší těžba vydá víc vzácného. **Cena:** výnos se hůř plánuje — musí se **měřit**, ne odhadovat |

### 12.2 NÁVRH — míra úspěchu (`V1`–`V8`)

**Jak to číst:** každý bod je tvrzení, které se dá **ověřit** — na obrazovce
nebo měřením. Co ověřit nejde, není míra úspěchu, ale přání.

| # | Co to znamená | Jak se to pozná (důkaz) | Kdy to musí platit |
|---|---|---|---|
| **V1** | **Růst je vidět jako číslo** — dovednost má hodnotu viditelnou ve hře | hráč ukáže dvě čísla z různých časů a jsou jiná | MVP |
| **V2** | **Růst mění výsledek**, ne jen číslo | stejná akce se dvěma hodnotami dovednosti dá **prokazatelně jiný výsledek** (výnos, kvalita, úspěšnost) | MVP |
| **V3** | **Mistrovství odemyká nové možnosti** (rozhodnutí `K4`) | ve hře je akce, kterou začátečník **nemá** — a je vidět, že na ni nemá | po MVP |
| **V4** | **Těžba má hloubku** (směs) | dva různě dlouhé zásahy do téhož zdroje dají **jiný obsah** | MVP |
| **V5** | **Uplatnění je vidět na světě** | stav světa je na obrazovce a po dodávce se **změní číslo** | MVP |
| **V6** | **Poptávka je tříděná a mění se** | táž věc má v různých situacích jinou cenu/poptávku (odpad / recyklovatelné / situační) | po MVP |
| **V7** | **Cíl s číslem existuje** | zakázku světa jde splnit a je vidět postup *(příklad „100 dávek lektvaru" se mění — lektvary v MVP nejsou, viz `R2-3`; místo nich např. „100 ingotů")* | zakázka v MVP, vlastní cíl později |
| **V8** | **Hru nejde zablokovat obchodem** | kdo jen těží a vyrábí, roste dál a není v slepé uličce | MVP |

**Kdo celek vyhodnotí:** uživatel hraním (V1, V4, V5, V7, V8) a agent měřením
(V2 je test: dvě hodnoty dovednosti → jiný výsledek). Body, které nejde
vyhodnotit, se do seznamu nepíšou.

### 12.3 NÁVRH — non-goals (co tam ZÁMĚRNĚ není)

| # | Co tam není | Proč |
|---|---|---|
| N1 | **Skutečné MMO a server** v MVP | rozhodnuto v §11 — provoz a populace; architektura se na cestu B jen připraví |
| N2 | **Pevné třídy a povolání** | pilíř `P3` — kombinace dovedností jsou volné |
| N3 | **Příběh „vyvoleného"** | pilíř `P1` — hráč je účastník světa, ne jeho střed |
| N4 | **Pixel art, 16barevná paleta, dithering** | zakázáno `assets/spec.json` (styl UO:T2A = předrenderované 3D) |
| N5 | **UO datové soubory a klient** | hra je vlastní, není to klient Ultimy |
| N6 | **Fyzika enginu** (převrhnutelné předměty, síly) | pohyb i kolize jsou vlastní systémy; fyzika by přidala ladění, které vize nechce |
| N7 | **Denní cyklus a roční období** | `DESIGN.md` je vyřadil a nic v jejich prospěch nezaznělo *(k potvrzení)* |
| N8 | **Dungeony, infestace a šlechtění zvěře v MVP** | jsou to **slova, ne systémy**; obsah hry je dnes 4 materiály a 1 nestvůra → patří do rozsahu (`R2-1`, `R2-2`) |
| N9 | **Automatická asistence** (pravidla hrají za hráče) | **rozpor s hlavním pilířem `P2`**: „požitek z vlastní dovednosti" a automat, který hraje za tebe, nejdou dohromady *(k potvrzení)* |
| N10 | **Více postav na jednom účtu** v MVP | `G-8` z rekonstrukce — rozsah |
| N11 | **Lektvary a alchymie** v MVP | rozhodnuto `R2-3` (8. 10. 2026) — srovnalo tři rozporné dokumenty; role lektvaru v `spec.json` zůstává nevyužitá |

**✅ Rozpor s lektvary — VYŘEŠEN (`R2-3`, 8. 10. 2026).** Uživatel rozhodl
**„lektvary později"**. Tím se srovnaly tři dokumenty, které si odporovaly:
`DESIGN.md` alchymii vyřadil, v `assets/data/items.json` lektvar není
a `assets/spec.json` pro něj má vyhrazenou roli (32 px). **Role v `spec.json`
zůstává nevyužitá, dokud se lektvary nepřidají** — a to je v pořádku, je to
deklarace vzhledu, ne slib obsahu.

**Co tím vzniklo:** uživatelův vlastní příklad cíle („100 dávek lektvaru") **není
v MVP splnitelný** — příklad se nahrazuje něčím, co v MVP je (např. „100 ingotů",
viz `V7`). A otevírá se otázka, kterou rozhodne kolo 3: **čím se hráč léčí, když
lektvary nejsou?** (jídlo, odpočinek, obvazy — nebo jen časem).

### 12.4 NÁVRH — prvních 5 minut

1. Hráč se objeví ve **vesnici** (dlaždice + postava + ukazatel stavu, na kterém
   je i **číslo dovednosti** — protože hlavní pilíř je `P2`).
2. Najde **zdroj rudy** (viditelný objekt), drží u něj pravé tlačítko a těží.
   Za pár vteřin má rudu a **číslo dovednosti těžby se pohnulo** (`V1`).
3. U pece **vytaví ingot**, u kovadliny **uková meč** — a vidí, že kovářství roste.
4. Svět mezitím ukazuje, **co potřebuje** (zakázka: „kovárna chce 3 ingoty") —
   hráč dodá a **stav světa se viditelně změní** (`V5`).
5. **Cíl prvních 5 minut:** hráč projde celý cyklus *získat → zpracovat →
   uplatnit → vidět změnu* a uvidí **aspoň dvě čísla, která se pohnula**.

**Cena:** dnešní mapa má **2 mince a žádný zdroj rudy** — „prvních 5 minut" tedy
znamená postavit vesnici, zdroje, pec, kovadlinu, HUD s čísly a stav světa.
Je to **největší jednotlivý kus práce z celé téhle revize** — a zároveň **první
věc, která má být vidět na obrazovce**.

### 12.5 NÁVRH — rozsah v číslech

Tohle je **druhé největší riziko** hry (vedle MMO) a rozhoduje se tady:

| | **S — dnešní + smyčka** | **M — doporučuji** | **L — vize naplno** |
|---|---|---|---|
| materiály | 4 | 8–10 (se směsmi) | 20+ |
| recepty | 3 | 6–8 | 20+ |
| nestvůry | 1 | 2–3 | 10+ |
| předměty | 2 | 5–8 | 30+ |
| mapa | 30×16 dlaždic | vesnice + důl + les | víc oblastí |
| zakázky a stav světa | ne | ano | ano |
| dungeony / infestace / šlechtění | ne | infestace jen jako **stav světa** | ano, i jako aktivity |
| délka sezení | 15–30 min | 30–60 min | hodiny |
| **práce (odhad)** | **+5–8 granulí** | **+20–30 granulí** | **+60–100 granulí** |

*(„Granule" jsou jednotky, ve kterých projekt už pracuje — roadmapa jich má 22
a jeden granule = jeden soubor s testem. Čísla jsou **odhad**, ne měření.)*

**Proč doporučuji M:** `S` nechá smyčku tenkou (málo věcí k výrobě → „uplatnění"
je prázdné, `V5` nemá co ukázat) a `L` řádově přeroste to, co dnes existuje —
a hlavně: **`L` se nedá ladit**, protože ladění vyžaduje hraní a na 10 nestvůr
a 30 předmětů není kdy. `M` je nejmenší rozsah, ve kterém smyčka funguje **celá**.

### 12.6 Otázky kola 2 (`R2-1`–`R2-5`)

```
[ ] R2-1  ROZSAH: S, M, nebo L?                                    (§12.5)
          Co už víme: dnes 4 materiály, 3 recepty, 1 nestvůra, 2 předměty.
          Návrh:     M — 8–10 materiálů, 6–8 receptů, 2–3 nestvůry,
                     5–8 předmětů, vesnice + důl + les, zakázky, stav světa.
          Cena:      S nechá smyčku tenkou („uplatnění" je prázdné);
                     L je řádově větší a nedá se ladit hraním.
          Dopad:     určuje, co má GDD popsat a co se kdy staví.

[ ] R2-2  DUNGEONY, INFESTACE A ŠLECHTĚNÍ ZVĚŘE: teď, později, nebo nikdy?
          Co už víme: jsou v tvém textu (§1.6) jako obsah; v repu nejsou vůbec.
          Návrh:     infestace = jen STAV SVĚTA (číslo, které roste a klesá),
                     ne bojová aktivita; dungeony a šlechtění = později.
          Cena:      každé „ano teď" je nový systém + grafika + ladění.
          Dopad:     bez výslovného seznamu si agent domyslí sousední vrstvu.

[ ] R2-3  LEKTVARY A ALCHYMIE — rozpor tří dokumentů.              (§12.3)
          Co už víme: tvůj příklad cíle je „100 dávek lektvaru"; `DESIGN.md`
                     alchymii vyřadil; v `items.json` lektvar není; `spec.json`
                     pro něj má vyhrazenou roli (32 px).
          Návrh:     lektvary ANO v MVP (jinak nemá tvůj vlastní příklad cíle
                     co plnit), alchymie jako systém až později.
          Cena:      lektvar = předmět + recept + grafika + účinek.
          Dopad:     bez rozhodnutí si to každý domyslí jinak — a už se to stalo.

[ ] R2-4  PRVNÍCH 5 MINUT (§12.4) a MÍRA ÚSPĚCHU `V1`–`V8` (§12.2): sedí?
          Co už víme: dnes hráč začne na mapě se 2 mincemi a nemá co dělat.
          Návrh:     scénář §12.4 a osm měřitelných bodů §12.2.
          Cena:      „prvních 5 minut" je největší jednotlivý kus práce.
          Dopad:     tohle je definice „hra funguje" pro první hratelný stav.

[ ] R2-5  „VYSOCE REWARDING MISTROVSTVÍ" — jak se to pozná?          (`N-10`)
          Co už víme: mistrovství = vyšší STROP i nové MOŽNOSTI (rozhodnuto).
          Návrh:     (a) číslo je vidět (úspěšnost 40 % → 85 %); (b) nová akce,
                     kterou začátečník nemá; (c) svět to pozná (zakázky, ceny).
          Cena:      (c) je nejdražší — svět musí mít na hráče „názor";
                     (a) a (b) jsou už rozhodnuté, tedy zdarma.
          Dopad:     bez toho se „rewarding" nedá postavit ani ověřit.
```

### 12.7 Výsledek kola 2 (8. 10. 2026)

| Otázka | Odpověď uživatele | Rozhodnutí a jeho cena |
|---|---|---|
| `R2-1` rozsah | „**M — doporučuji**" | **rozsah `M`** (§12.5): 8–10 materiálů, 6–8 receptů, 2–3 nestvůry, 5–8 předmětů, vesnice + důl + les, zakázky, stav světa — **odhad +20–30 granulí**. **Cena:** `L` (dungeony, 10+ nestvůr, 30+ předmětů) zůstává za dveřmi a `S` byl zamítnut jako příliš tenká smyčka |
| `R2-2` obsahové výzvy | „**Infestace jako stav světa, zbytek později**" | **infestace = číslo stavu světa**, ne bojová aktivita; **dungeony a šlechtění zvěře později**. **Cena:** nepřítel bude jen číslo — hráč ho neutlačí bojem, ale ekonomikou (dodávkami) |
| `R2-3` lektvary | „**Lektvary později**" | **lektvary a alchymie mimo MVP** (§12.3). **Cena:** příklad cíle se nahrazuje (např. „100 ingotů") a **otevírá se otázka léčení** (kolo 3) |
| `R2-4` míra úspěchu + prvních 5 minut | „**Sedí**" | `V1`–`V8` (§12.2) i scénář prvních 5 minut (§12.4) **platí jako definice „hra funguje"**. **Cena:** potvrzuje se **největší jednotlivý kus práce** — vesnice, zdroje, pec, kovadlina, čísla dovedností, stav světa |
| `R2-5` mistrovství | „**I uznání od světa**" | mistrovství se pozná **čísly, odemčenými možnostmi a tím, že svět na mistra reaguje** (lepší zakázky, jiné ceny, titul). **Cena:** přibývá systém — **svět musí mít na hráče „názor"**; kolo 3 musí rozhodnout, podle čeho se počítá, a je to další věc k ladění |

**Co je tím splněné z kritérií zadání §7:** non-goals existují jako výslovný
seznam (§12.3), míra úspěchu je měřitelná (`V1`–`V8`), rozsah je v číslech
(§12.5), prvních 5 minut je scénář (§12.4). **Co zůstává:** kola 3–5.

---

## 13. KOLO 3 — Mechaniky a obsah

> **Stav:** **UZAVŘENO s jedním otevřeným konceptem** (8. 10. 2026) — osm
> rozhodnutí (§13.1 a §13.7), obsah a startovní čísla potvrzené (§13.2–§13.4),
> a **otevřený koncept „čím platí řemeslník"** (§13.8), který uživatel sám
> označil jako nerozhodnutý.

### 13.1 Rozhodnuto (8. 10. 2026)

| Otázka | Odpověď uživatele | Rozhodnutí a jeho cena |
|---|---|---|
| **Atrofie** | „**Přepínač — zapnout po prvním ladění**" | Mechanika bude hotová, ale **vypnutá**. **Cena:** musí se udělat přepínač a **ověřit, že po zapnutí opravdu klesá** — vypnutá mechanika, která nikdy neběžela, je slepé místo |
| **Synergie** | „**Jemné — vedlejší růst cca 20 %**" | Vedlejší dovednost roste **~20 % tempa** té hlavní. **Cena:** synergie je znát, ale **není povinná** — hráč nemusí kombinovat, jen může (což je v duchu `P3`) |
| **Stav světa** | „**Sedí — infestace + zásobenost, ceny z nich**" | Dvě čísla 0–100: **infestace** roste časem a klesá zásobeností; **zásobenost** roste dodávkami a klesá spotřebou; **ceny jsou důsledek** (ne třetí stav) |
| **Zbraň** | „**MVP jen v ruce**" | Poloha „u pasu" se odkládá — 2× obrázků na každou zbraň |
| **Léčení** | „**Obvazy jako předmět**" | Léčba je **řemeslo**, ne regenerace. **Cena:** nový materiál a recept — `flax` (len) → `cloth` (látka) → `bandage` (obvaz) |

### 13.2 NÁVRH — obsah v číslech (rozsah `M`)

| Kategorie | Návrh | Poznámka |
|---|---|---|
| **Materiály (11, z toho 3 meziprodukty)** | běžné: `iron_ore`, `coal`, `stone`, `wood`, `flax` · **vzácné složky směsi**: `silver_ore` (doly), `hardwood` (les), `fine_flax` (pole) · meziprodukty: `cloth` (len), `iron_ingot` (ruda + uhlí), `steel_ingot` (ingot + uhlí) | **každý zdroj má běžnou i vzácnou složku** — tím je splněno rozhodnutí z §12.1 |
| **Předměty (7)** | `iron_sword`, `iron_armor` (existují), `steel_sword`, `pickaxe` (krumpáč), `hammer` (kovářské kladivo — **zároveň zbraň**, demonstruje `P3`), `bandage` (obvaz), `silver_ring` (stříbro jako prodejní zboží) | stříbro dostává smysl: je to **vzácná složka, která se vyplatí prodat** |
| **Nestvůry (3)** | `skeleton` (existuje), `wolf` (vlk — les), `bandit` (loupežník — cesty) | živí boj a dávají kůži/zlato |
| **Recepty (8)** | tavení (ruda + uhlí → ingot), ocel (ingot + uhlí → ocel), kování meče, kování zbroje, ocelový meč, tkaní (len → látka), obvazy (látka → obvaz), krumpáč/kladivo | **uhlí je palivo** — tavení tím dostává cenu (návrh k potvrzení) |
| **Dovednosti (6)** | `tezba`, `drevorubectvi`, `kovarstvi`, `tkani`, `boj_na_blizko`, `obchod` | `obchod` ovlivňuje ceny — drží roli „obchodník" ze záměru |
| **Mapa** | vesnice + důl + les + pole (len) | dnes: 30×16 dlaždic a 4 markery |

### 13.3 NÁVRH — vzorce a startovní čísla (k ladění, ne k víře)

| Co | Startovní hodnota | Odkud |
|---|---|---|
| Atributy | Str/Dex/Int 0–100, výchozí 10 | **už v kódu** (`attributes.gd`) |
| Boj — zásah | 0,5 + Dex/200 + dovednost/200 | **už v roadmapě** (`sim.combat`) |
| Boj — zranění | 1 + Str/10 + zbraň − zbroj | tamtéž |
| Výnos těžby | 1 + (dovednost − obtížnost)/10 | **už v kódu** (`mining.gd`) |
| Kvalita výrobku | dovednost/20 → 0–5 stupňů (cena + trvanlivost) | **už v roadmapě** (`sim.crafting`) |
| Růst dovednosti | +1 bod se **pravděpodobností (100 − dovednost)/100** (na 0 skoro vždy, na 90 v 10 % případů) | návrh |
| Synergie | vedlejší dovednost dostane **20 %** toho, co hlavní | rozhodnutí `M2` |
| **Vzácná složka** | šance roste s **dobou nepřetržité těžby**: start 2 %, +1 % za každých 10 s, strop 30 % | návrh — naplňuje „delší těžba = vzácnější" |
| Cena | základ × (1 + (100 − zásobenost)/100) × (1 + infestace/200) | návrh |
| Infestace | +1 za hodinu hry, −2 × (zásobenost/100) za hodinu | návrh |
| Zásobenost | −1 za hodinu, +5 za dodanou dávku (ingot, zbraň) | návrh |

> **Proč jsou to „startovní" čísla:** čísla se **ladí hraním**, ne plánováním.
> Jejich hodnota není v tom, že jsou správná, ale že **existují a dají se měnit
> na jednom místě** — bez nich si každá komponenta vymyslí vlastní.

### 13.4 NÁVRH — jak svět pozná mistra (k rozhodnutí `R2-5`)

Svět má mít na hráče „názor". Návrh: počítá se z **trojice** — (a) nejvyšší
dovednost hráče, (b) počet splněných zakázek, (c) **průměrná kvalita** dodávek.
Efekt: větší zakázky, lepší ceny a **titul na obrazovce**.

### 13.5 Co zůstává otevřené v kole 3

- **Hraničář a luk:** uživatelova vize zmiňuje hraničáře („spolehlivěji střílí,
  jezdí, ochočí zvěř"). **Luk je ale nový druh souboje** (projektily, dostřel) —
  v rozsahu `M` navrhuju hraničáře zastoupit **lovem zvěře na blízko a kůží**;
  luk a zvěř jako systém později.
- **Uhlí jako palivo:** přidává do tavení krok a cenu („mít čím topit").
- **Jak se obvaz používá:** klávesa, klik v inventáři, nebo automaticky při
  zranění? (Do kola 4 k UI a smlouvám.)
- **Mění krumpáč a kladivo mechaniku** (zrychlí těžbu / umožní tvrdší zdroje),
  nebo jsou jen předměty s číslem?

### 13.6 Otázky kola 3 (`M6`–`M8`)

```
[ ] M6  TEMPO RŮSTU: jak dlouho má trvat cesta k mistrovi?
        Co už víme: růst = +1 bod s pravděpodobností (100 − dovednost)/100.
        Návrh:     rychlé pro ladění — 0→50 ≈ 2–3 h, 50→90 ≈ 10–15 h,
                   90→100 dalších 10 h+ (tj. mistrovství je běh na dlouho).
        Cena:      rychlejší = dřív se pozná, co je špatně, ale hra „uteče“;
                   pomalejší = delší motivace, ale ladění trvá měsíce.
        Dopad:     určuje, jak dlouhé má být sezení a kolik obsahu stačí.

[ ] M7  OBSAH V ČÍSLECH (§13.2): sedí seznam?
        Co už víme: dnes 4 materiály, 3 recepty, 1 nestvůra, 2 předměty.
        Návrh:     11 materiálů (3 meziprodukty), 7 předmětů, 3 nestvůry,
                   8 receptů, 6 dovedností, vesnice + důl + les + pole.
        Cena:      každá položka = data + recept + (u předmětu) obrázek.
        Dopad:     tohle je „kolik toho hra obsahuje“ — a co GDD vypíše.

[ ] M8  UZNÁNÍ OD SVĚTA: podle čeho svět pozná mistra?      (§13.4, `R2-5`)
        Co už víme: mistrovství = čísla + odemčené možnosti + uznání světa.
        Návrh:     trojice — nejvyšší dovednost, počet splněných zakázek,
                   průměrná kvalita dodávek.
        Cena:      čím víc kritérií, tím hůř se to vysvětluje hráči
                   (musí být vidět, proč mě svět bere vážně).
        Dopad:     systém zakázek a cen se podle toho počítá.
```

---

### 13.7 Výsledek druhé poloviny kola 3 (8. 10. 2026)

| Otázka | Odpověď uživatele | Rozhodnutí a jeho cena |
|---|---|---|
| `M6` tempo růstu | „**Pro ladění zatím ještě rychlejší, případně s přepínatelným postupem/stavem**" | **Rychlost růstu je parametr s předsadami:** `ladici` (mistrovství v minutách — aby se dalo ladit hned), `normalni`, případně `pomala`. **Cena:** parametr musí být v konfiguraci a **hlídat se, aby se ladicí předsada nedostala do hry** (přesně past „ladicí hodnota v produkci"); a „přepínatelný stav" znamená rozhodnout, **co se stane s už rozdanými body při přepnutí** (návrh: nic — přepínač mění jen tempo dalšího růstu) |
| `M7` obsah | „**Sedí**" | obsah v číslech §13.2 platí: 11 materiálů, 7 předmětů, 3 nestvůry, 8 receptů, 6 dovedností, vesnice + důl + les + pole |
| `M8` uznání světa | „**Trojice kritérií**" | svět pozná mistra podle **nejvyšší dovednosti + počtu splněných zakázek + průměrné kvality dodávek** (§13.4) |

### 13.8 OTEVŘENÝ KONCEPT — cena řemesla, a čím ji platit, když ne grindem

**Uživatel 8. 10. 2026 (doslovně):**

> *„Řemeslnictví často reprezentuje svou cenu hlavně časem stráveným získáváním
> materiálů a výrobou, ale zboží je pak čistý zisk. Chci zvážit jiný koncept —
> kdo ví, kde získat kvalitní materiál a to rychle a snadno, ten neztratí čas
> a nechci aby to byl odporný grind, ALE podobně jako v reálném světě by mohlo
> cenu ovlivňovat i něco jiného, jiné náklady, které musí řemeslník vydat.
> Ještě nevím co a nebo jestli vůbec se vydávat tímto směrem."*

**Proč na tom záleží (obava je správná):** když je zboží **čistý zisk**,
ekonomika nemá tlak — vyplatí se vyrobit všechno, takže **žádná volba není
rozhodnutím**. Cena v řemesle má jediný účel: **nutit volit**.

**Co v návrhu už je — a je to jiná cena než čas:**

1. **Svět sám je cenotvorný** — ceny rostou s infestací a klesají se zásobeností
   (§13.3). Když trh zaplavíš, **marže spadne** a musíš hledat jiné zboží nebo
   lepší zdroj. To je náklad, který **není čas** — je to **příležitost**.
2. **Vzácná složka** (§13.2) — kvalitní věc nejde vyrobit z běžné rudy; nákladem
   je **najít**, ne „naklikat".
3. **Znalost zkracuje čas** (uživatelova vlastní věta) — kdo ví, kde je kvalitní
   materiál, neztrácí čas. To je **hmatatelná odměna za poznání světa** a sedí
   to na roli hraničáře.

**Co se dá přidat jako „jiný náklad" (menu, každé s cenou):**

| Náklad | Jak vypadá | Cena |
|---|---|---|
| **Palivo** | tavení spotřebuje uhlí | jedno číslo a jeden krok navíc; uhlí se musí těžit |
| **Opotřebení nástroje** | krumpáč a kladivo se **ničí** (trvanlivost už v kódu je) | nutí opravovat = další odběratel materiálu |
| **Zmetkovost** | část výroby se nepovede (uživatelovo „menší ztrátovost" z §1.6) | jedno číslo k ladění; zvyšuje cenu neúspěchu |
| **Poplatek za stanici** | pec a kovadlina patří vesnici → za použití se platí | peníze se vrací světu (zásobenost), ne mizí |
| **Riziko cesty** | vzácné zdroje jsou dál a v nebezpečnějších místech | těží z toho svět (cesty, loupežníci) — ale je to obsah navíc |

**Doporučení:** vzít **první tři** (palivo, opotřebení, zmetkovost) — jsou to
čísla a data, ne nové systémy, a dohromady dělají z výroby **rozhodnutí místo
rutiny**. Poplatek za stanici a riziko cesty jsou obsah navíc (patří do `L`).

**A jedna věc, kterou je fér říct:** „nechci odporný grind" a „zboží je čistý
zisk" **nejdou vyřešit zároveň bez nějakého nákladu** — když není čas ani jiný
náklad, je výroba zdarma a cena ztratí smysl. Rozdíl je jen v tom, **čím se
platí**: časem (grind), nebo rozhodnutím (co, kdy a z čeho vyrobit).

**Tohle zůstává OTEVŘENÉ** — uživatel to sám označil jako „ještě nevím, nebo
jestli vůbec". Rozhodne se na konci kola 3 nebo v plánu (kolo 5).

---

## 14. KOLO 4 — Technika a smlouvy

> **Stav:** **UZAVŘENO** (8. 10. 2026) — čtyři rozhodnutí uživatele (§14.1)
> a tři rozhodnutí agenta (§14.2). Co zůstává, je **psaní TDD** (§14.3),
> ne rozhodování.

### 14.1 Rozhodnuto uživatelem (8. 10. 2026)

| Otázka | Odpověď uživatele | Rozhodnutí a jeho cena |
|---|---|---|
| **`R-1` architektura běhu** | „**Sedí**" | **Pevný tik 50 ms** pro simulaci (vykreslování zvlášť), **jeden kořen** s registrem komponent, **simulace oddělená od zobrazení** (zprávy a příkazy místo přímého volání). **Cena:** znamená to **přepsat monolit** `game.gd` (377 řádků) — granule `engine.shell` v plánu je, ale je blokovaná mrtvou granulí `world.map` (`scripts/world.gd` = 0 B). Zároveň je to **podmínka cesty B** z §11 |
| **`N-2` osm směrů** | „**Až po prototypech**" | Prototyp zůstane u **4 směrů**; rozhodne se, až bude vidět pohyb. **Cena:** neřeší se teď nic; kdyby se pro 8 směrů rozhodlo později, je to **2× obrázků na každý kus výbavy** (dnes 32 → 64 na kus) |
| **`N-9` paperdoll** | „**Až s vrstvenou grafikou**" | Náhled postavy se ne staví do MVP. **Cena:** do té doby hráč vidí výbavu jen v inventáři a na postavě ve hře |
| **`R-3` jazyk** | „**Klíče anglicky, texty česky**" | **Klíče, identifikátory a literály rozhraní anglicky; texty pro člověka česky.** Platí i pro `assets/data/*.json` (dnešní stav je takový: `id` = `iron_sword`, `name` = „Železný meč") — jen se to **zapíše jako pravidlo**, aby to příště nikdo nehádal. **Cena:** texty pro hráče se musí udržovat zvlášť od klíčů (dvě pole), což je ale standard |

### 14.2 Rozhodnuto agentem (uživatel to nemusí rozhodovat)

| Co | Rozhodnutí | Proč to není na uživateli |
|---|---|---|
| **`R-2` výkonnostní rozpočet** | **60 FPS** při 960×540; **simulace pod 2 ms na snímek** (tik 50 ms = 20 tiků/s má na tik 50 ms, takže rezerva je 25×) | technické číslo; uživatel ho nemá s čím srovnat |
| **Použití obvazu** | **kliknutím v inventáři** (myš je primární vstup), s odečtením jednoho kusu | vyplývá z rozhodnutí `K5` (ovládání myší) |
| **Datové formáty** | `assets/data/*.json` = obsah (data, ne kód); `assets/levels/*.json` = mapa a markery; ukládání = `ConfigFile` do `user://` (jak to dělá `save.gd`) | odvozeno z existujícího kódu, ne z vkusu |
| **Chybové chování** | chybějící komponenta = `push_error` a **hra zůstane hratelná** (jak to dělá `engine.shell` v plánu); tichý `return` je zakázaný (naměřená past z 2. 10. 2026) | technické pravidlo s naměřeným důvodem |

### 14.3 Co zůstává na TDD (ne rozhodnutí, ale práce)

**15 smluv bez tvaru dat** (`ARCHITEKTURA.md` §2 má 18 smluv, tvar dat jen 3),
formáty `assets/levels/*.json` vs `assets/data/*.json`, vlastnictví stavu pro
všechno kromě pozice hráče, a ukládání inventáře a stavu světa. **To se píše**,
až bude uzavřená vize (kolo 5) — podle §8.

---

## 15. KOLO 5 — Plán, brány a pravidla

> **Stav:** **UZAVŘENO** (8. 10. 2026) — všechny čtyři otázky `P1`–`P4` jsou
> zodpovězené; výsledky v §15.5. **Tím je uzavřená celá revize vize.**

### 15.1 NÁVRH — milníky jako HRATELNÉ stavy

Pravidlo: **každý milník je vidět na obrazovce** (ne „vrstva kódu“).

| Milník | Co je na konci vidět | Co to obnáší |
|---|---|---|
| **M0 — Kostra** | hra se spustí a nezhroutí se; komponenty existují přes registr | přepis `game.gd` na registr (`engine.shell`), pevný tik |
| **M1 — Hýbu se** | postava se **plynule** pohybuje myší po dlaždicové mapě, objekty se nepřekrývají, rozběh a zastavení sedí | pohyb, kolize, řazení hloubky |
| **M2 — Těžím a vidím číslo** | v inventáři je ruda, **číslo dovednosti se pohnulo**, delší těžba dala vzácnější kus | zdroje, směs, výnos, HUD s čísly |
| **M3 — Vyrábím** | u pece ingot, u kovadliny meč; kvalita je vidět, nástroj se opotřebovává | recepty, kvalita, opotřebení, zmetkovost |
| **M4 — Prodávám a svět reaguje** | **stav světa na obrazovce** (infestace, zásobenost) se po dodávce změní | zakázky, ceny, simulace světa |
| **M5 — Žiju ve světě** | svět se hýbe **i beze mě**; zakázky odpovídají tomu, jak si mě váží; smrt a respawn | uznání světa, léčení, smrt |
| **M6 — Grafika** | postava ukazuje, co má nasazené (vrstvená grafika, `A-1`) | až po M5 — rozhodnutí z §7 |

### 15.2 NÁVRH — brány (a co u nich chybí)

| Brána | Stav | Co chybí |
|---|---|---|
| `check-schema.py` (tvrdá), `check-assets.py`, `check-wiring.py`, `tests/run_tests.gd` | existují | u každé je naměřené slepé místo (viz `docs/BRANY-HRY.md`) |
| `vision.mjs` | existuje, **neblokuje** | — |
| **brána nad dokumentací** | **chybí** | `check-docs-refs` (každý odkaz `§N.N` musí existovat) a `check-zadani` (placeholdery, vadné literály, **konzistence čísel**) — vzor má `game-clone` |
| **třetí stav „neměřeno"** | **chybí** | dnes jsou dva stavy (prošlo/selhalo); `game-clone` má `exit 2` = něco zůstalo neměřeno a **to není zelená** |

**Definice hotovo (návrh, převzato z konceptu `KONCEPT-PRIPRAVY-HRY.md`):**
hotovo JE, když **soubor je v `main`** A **brána jeho funkci skutečně zavolala**
A **přijímací kritérium proběhlo s konkrétní hodnotou** A **funkci volá produkční
kód** (ne jen test). Hotovo NENÍ „PR je sloučené", „testy jsou zelené",
„funkce existuje" ani `done: true`.

### 15.3 Co je potřeba rozhodnout (a je to na uživateli)

- **Tři nepravdivá tvrzení v pravidlech hry** (§1, řádek 10): `AGENTS.md:108–110`
  popisuje vadu rozhraní, která dnes neexistuje; `CONVENTIONS.md:252` posílá na
  funkci `_safe_spot`, která nikde není; `CONVENTIONS.md:273` tvrdí 26 kontrol
  místo měřených 91. **Mění to trvalá pravidla projektu, proto to patří
  uživateli** — návrh opravy je v ledgeru stanice.
- **Název hry:** `project.godot` a `spec.json` říkají `uo-sandbox`, repo je
  `uo-shadows`. Sjednotit?
- **Roadmapa se mění až po uzavření vize** (zadání §6.5) — po kole 5.

### 15.4 Otázky kola 5 (`P1`–`P4`)

```
[ ] P1  MILNÍKY (§15.1): sedí M0–M6 jako hratelné stavy?
        Co už víme: dnes je hra „sběračka dvou mincí“ a 10 z 13 hotových
                   komponent nikdo nezavolá.
        Návrh:     M0 kostra → M1 pohyb → M2 těžba a číslo → M3 výroba →
                   M4 svět reaguje → M5 uznání a smrt → M6 grafika.
        Cena:      M6 (vrstvená grafika) je až za M5 — tedy grafika později,
                   než by se komukoli líbilo.
        Dopad:     určuje pořadí práce na měsíce dopředu.

[ ] P2  TŘI NEPRAVDIVÁ TVRZENÍ V PRAVIDLECH: opravit?
        Co už víme: ověřeno měřením 8. 10. 2026 (§1, řádek 10).
        Návrh:     ano — tři jednořádkové opravy (a číslo testů vzít
                   z VÝSTUPU BĚHU, ne ze vzoru v souboru).
        Cena:      mění trvalá pravidla projektu; kdo je neopraví, „opraví“
                   podle nich správný kód.
        Dopad:     pravidla se stanou použitelná jako zdroj pravdy.

[ ] P3  NÁZEV HRY: sjednotit na `uo-shadows`?
        Co už víme: `project.godot` `config/name = "uo-sandbox"`,
                   `assets/spec.json` píše „projekt uo-sandbox“, repo je
                   `uo-shadows`.
        Návrh:     ano, sjednotit na název repa (pravidlo stanice).
        Cena:      změna projektového souboru — v téhle session se nedělá,
                   jen se to zařadí.
        Dopad:     kdo hledá hru, najde ji pod jedním jménem.

[ ] P4  DEFINICE HOTOVO (§15.2): platí čtyři podmínky?
        Co už víme: dnes se „hotovo“ počítá z příznaku `done` v roadmapě
                   (13 granul, z toho 10 nikdo nezavolá).
        Návrh:     soubor v main A brána zavolala funkci A kritérium proběhlo
                   s hodnotou A volá to produkční kód.
        Cena:      každá granule bude „hotová“ později než dnes.
        Dopad:     „hotovo“ přestane být tvrzení a stane se měřením.
```

---

### 15.5 Výsledek kola 5 (8. 10. 2026) — a tím uzavřená revize vize

| Otázka | Odpověď uživatele | Rozhodnutí a jeho cena |
|---|---|---|
| `P1` milníky | „**Sedí M0–M6**" | práce jde v pořadí kostra → pohyb → těžba s číslem → výroba → svět reaguje → uznání a smrt → **grafika až nakonec**. **Cena:** vzhled je poslední, i když by se líbil dřív |
| `P2` tři nepravdivá tvrzení | „**Opravit**" | **PROVEDENO 8. 10. 2026** (tabulka níž). Uživatel tím výslovně povolil změnu **trvalých pravidel projektu** — jinak by to agent dělat nesměl |
| `P3` název hry | „**Sjednotit na `uo-shadows`**" | **zařazeno, ne provedeno**: mění `project.godot` a `assets/spec.json`, a tahle session kód needituje (zadání §6.2) |
| `P4` definice hotovo | „**Platí ty čtyři podmínky**" | hotovo = soubor v `main` **A** brána jeho funkci zavolala **A** kritérium proběhlo s konkrétní hodnotou **A** funkci volá produkční kód. **Cena:** granule budou „hotové" později než dnes — a poprvé to bude něco znamenat |

**Co se podle `P2` provedlo (8. 10. 2026):**

| Soubor | Bylo tam | Je tam |
|---|---|---|
| `AGENTS.md` §Jazyk | tvrzení, že rozhraní `add_rule` „**míchá jazyky**" (`"cíl mrtev"`) | **opraveno**: `scripts/assist.gd:15` má `"target dead"`; doplněno potvrzení jazykového pravidla (`R-3`) |
| `CONVENTIONS.md:252` | „Použij `_safe_spot(vp)` (už v `game.gd` je)" | **opraveno** na `marker_positions(...)` + `is_walkable_at()`; `_safe_spot` je v `scripts/` **0×** |
| `CONVENTIONS.md:273` | „**26 kontrol**" | **opraveno**: počet se čte z výstupu běhu (`[test] N kontrol`); naměřeno 3. 10. 2026 = **91**; staré číslo označeno jako *„ve svém čase správné, dnes zastaralé"* |

**Co zůstává po revizi otevřené (a je to pojmenované, ne zapomenuté):**

1. **Čím platí řemeslník, když ne grindem** (§13.8) — uživatel sám řekl „ještě
   nevím"; rozhodne se v plánu (kolo 5 byla poslední kola revize, tohle téma
   patří do plánovací session).
2. **Název hry** `uo-sandbox` → `uo-shadows` (zařazeno, §15.5 `P3`).
3. **Luk a zvěř (hraničář)** — v rozsahu `M` zastoupeno lovem na blízko
   (§13.5); luk je nový druh souboje, patří do `L`.
4. **Obvaz: jak přesně se použije** — rozhodnuto „kliknutím v inventáři"
   (§14.2), ale patří to do smluv (TDD).

---

## 16. Co se udělá dál (konkrétní krok)

1. **Revize vize je UZAVŘENÁ** (8. 10. 2026) — kola 1–5 zodpovězená, tři
   pravidla opravená (§15.5). **Tenhle dokument je teď zadání pro psaní
   dokumentů** — nic dalšího se v něm nerozhoduje.
2. **Další session píše GDD** podle osnovy v §8 — a bere k tomu:
   §2 (záměr), §3 (pilíře), §4 (smyčka + tři pravidla z krajních případů),
   §5 (úspěch), §12.2 (`V1`–`V8`), §12.3 (non-goals), §12.4 (prvních 5 minut),
   §12.5 (rozsah `M`), §13 (mechaniky, obsah, vzorce), §15.1 (milníky).
   **Nic z toho se nemusí dohadovat** — to byl účel celé revize.
3. **Pak ADD** (lidská vrstva k `assets/spec.json` + katalog assetů + pipeline)
   **a TDD** (15 tvarů dat, architektura běhu z `R-1`, výkonnostní rozpočet
   z §14.2, jazyk z `R-3`). TDD nahradí `docs/ARCHITEKTURA.md`, GDD nahradí
   `docs/DESIGN.md`, a odkazy v `AGENTS.md` se přepíšou — **nezakládat čtvrtý
   zdroj pravdy** (zadání §6.4).
4. **Teprve pak** se smí změnit `.forge/roadmap.json` (zadání §6.5) — a vznikne
   z něj plán granulí pro milníky `M0`–`M6`.
5. **Zařazené drobnosti:** sjednotit název hry na `uo-shadows` (`P3`), dořešit
   koncept „čím platí řemeslník" (§13.8) a rozhodnout, co s necommitnutou
   složkou `_acl-recovery/` v rootu repa.
