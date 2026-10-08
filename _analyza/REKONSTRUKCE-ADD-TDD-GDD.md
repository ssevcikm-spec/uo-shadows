# Rekonstrukce: ADD, TDD a GDD pro `uo-shadows`

> **Co tenhle dokument JE:** **rekonstrukce a zadání** — co z ADD, TDD a GDD
> v projektu existuje, co se dá obnovit bez rozhodnutí, co chybí, a **která
> rozhodnutí patří uživateli**.
>
> **Není to:** návrh dokumentů. Ty vzniknou **až po odpovědích** v §5.
>
> **Zadání:** uživatel, 8. 10. 2026 — „znovu-vybudování ADD, TDD a GDD",
> zvolen postup **rekonstrukce → otázky → dokumenty**, projekt `uo-shadows`.
> **Vzniklo:** 8. 10. 2026 měřením repa `E:\Workspaces\uo-shadows`,
> `HEAD = 932dc6f` + 3 commity auditu.
> **Odkud brát současný stav:** tenhle dokument je stav svého tématu.
>
> **Co z něj bylo provedeno:** nic — je to podklad pro rozhodnutí.

---

## 0. Souhrn: co rekonstrukce našla

| Dokument | Co existuje | Dá se obnovit? | Blokuje ho rozhodnutí? |
|---|---|---|---|
| **GDD** | `docs/DESIGN.md` (4 kB, sám se zrušil) + `ARCHITEKTURA.md` §0–0.4 (cíl, pilíře, rozsah, 13 REQ, schopnosti, obsah MVP) + skutečná data v `assets/data/` | **částečně** — „co ve hře je" ano, „jak se to hraje" **ne** | **ANO — 9 rozhodnutí** |
| **ADD** | **`assets/spec.json` je hotová ADD ve strojové podobě** (5,5 kB: rozměry, role, vrstvy, brány, styl i se zákazy, zrušená paleta s důvodem) + `.forge/vision-profile.json` + **vyrenderované sprity v `tools/blender/sprites/`** | **z 80 %** — chybí lidská vrstva a katalog | **ANO — 2 rozhodnutí** (jedno z nich blokující, §4.1) |
| **TDD** | `ARCHITEKTURA.md` §1–2 (8 vrstev, 18 smluv — **tvar dat má jen 3**) + `CONVENTIONS.md` + kód | **z 70 %** — odvoditelné z kódu | **ANO — 3 rozhodnutí** |

**Nejdůležitější nález celé rekonstrukce** (víc v §4.1):
**Projekt má DVA paralelní výtvarné systémy.** V `tools/blender/sprites/` leží
**128 framů vrstvené postavy** (4 vrstvy × 4 směry × 8 framů) a druhá sada pro
NPC — přesně to, co `spec.json` deklaruje jako cíl („*oblékání jako v UO:
postava je SLOŽENÁ Z VRSTEV*"). **Hra ale kreslí ploché sprity** z
`assets/sprites/` (`player.png`, `npc.png`, …) a vrstvy nikdy nepoužije.
`check-assets.py` to poctivě hlásí jako poznámku: „*animace chůze v projektu
není – přeskočeno*" — protože v `assets/sprites/` žádné `walk_*` nejsou.

**Důsledek:** to, co je v projektu napsané jako cíl vzhledu, **není to, co hra
dělá**. ADD musí rozhodnout, který z těch dvou systémů je budoucnost — a to je
rozhodnutí uživatele, ne agenta.

---

## 1. GDD — co existuje a co chybí

### 1.1 Co je obnovitelné (existuje, jen je roztroušené)

| Co | Kde | Stav |
|---|---|---|
| **Cíl** (jedna věta) | `ARCHITEKTURA.md:9–17` | „*Moderní Ultima Online: izometrický sandbox…*" — existuje |
| **Pilíře (7)** | `ARCHITEKTURA.md:19–27` | existují, ale jsou to **featury**, ne pocity (viz §5 G-2) |
| **Herní smyčka (jedna věta)** | `ARCHITEKTURA.md:32` | „*těžit → tavit → kovat → používat → opravovat*" — **celý popis hraní** |
| **Rozsah řezu** | `ARCHITEKTURA.md:29–35` | ostrov + důl + les, 1 nepřítel — **ale bez čísel** |
| **Požadavky (13× REQ-)** | `ARCHITEKTURA.md:37–54` | existují — od skillek po smrt a respawn |
| **Schopnosti** | `ARCHITEKTURA.md:56–70` | 13 ověřitelných vět |
| **Obsah MVP** | `ARCHITEKTURA.md:72–87` | tabulka kategorií |
| **Skutečný obsah** | `assets/data/*.json` | **4 materiály, 4 skilly, 3 recepty, 1 nestvůra, 2 předměty** — tohle je reálný rozsah hry |
| **Out-of-scope** | `DESIGN.md:9–23` | denní cyklus, alchymie, MMO, magie |
| **Vzhled a zvuk** | `DESIGN.md:46–53` | popis, jak má vypadat a znít |
| **Starý plán 6 úloh** | `DESIGN.md:59–67` | historie, orchestr ho nepoužívá |

### 1.2 Co chybí — a **není to nikde**, ani náznakem

Ověřeno hledáním v celém repu (7 dokumentů, `AGENTS.md`, `CONVENTIONS.md`,
`BRANY-HRY.md`); README v repu **není**:

| Chybí | Proč to vadí |
|---|---|
| **Ovládání** — jaké klávesy, myš? | `project.godot` nemá **ani jednu** vstupní akci. Jediné místo, kde je ovládání popsané, je běhová nápověda `game.gd:221` — a **ta lže** (inzeruje E/C/B/X/R/M, která kód neobsluhuje) |
| **Co je na obrazovce** — jak vypadá UI | `ARCHITEKTURA.md:97` říká jen „HUD, kamera"; skutečný obsah lišty je jen v kódu `hud.gd` |
| **Prvních 5 minut** | hráč dnes začne na mapě 30×16 se dvěma mincemi a nemá co dělat |
| **Jak hráč pozná úspěch** | není vítězná podmínka, cíl hraní, ani „co je zábava" |
| **Rozsah v číslech** | „ostrov + důl + les" — kolik dlaždic, kolik předmětů, kolik hodin hraní? |
| **Non-goals** | `ARCHITEKTURA.md` má **0 výskytů** slova `non_goals` i „NEDĚLAT". `DESIGN.md` sice čtyři věci vyřazuje, ale **není zdroj pravdy** |
| **Délka sezení / meta smyčka** | hra nemá tempo: co se změní za jedno posezení, co za týden |
| **Ekonomika jako smyčka** | `REQ-econ` říká „výroba = střed, loot doplňuje" — ale hráč začíná s **0 zlatem**, takže `buy()` nemůže nikdy uspět |

---

## 2. ADD — co existuje a co chybí

### 2.1 `assets/spec.json` je překvapivě dobrý — a je to **strojová ADD**

Obsahuje **rozhodnutí s odůvodněním**, ne jen čísla:

| Co | Hodnota / rozhodnutí | Odůvodnění v souboru |
|---|---|---|
| Viewport | `960×540`, celočíselně 2× na 1080p | „*zadne rozmazani*" |
| Dlaždice | izometrický diamant `96×48`, poměr 2:1 | — |
| **Role (8)** | player/npc 96 px, enemy 64, ore/chest 48, weapon 48, potion 32, coin 24 — každá s `canvas`, `smery`, `framy`, `stin` | — |
| **Vrstvy oblékání** | 8 slotů (`body, legs, feet, torso, cloak, head, shield, weapon`), počáteční 4, tonování u 3 | „*jakákoli kombinace výbavy je zdarma, bez dalšího rendru*" |
| **Brány (6)** | tolerance výšky 10 %, 0 děr, okraj ≤5 %, IoU ≥0,80, posun ≤3 px, kontrast ≥150 | u kontrastu: „*u nepritele v plošinovce vyšlo 93 = splýval s podlahou*" |
| **Styl** | UO:T2A, realistický až mírně fantasy, **NE pixel art** | „*UO vypadalo realisticky proto, že jeho sprity byly PŘEDRENDROVANÉ 3D MODELY*" |
| **Zákazy stylu** | 16barevná paleta, dithering, nearest-neighbour, pixelové hrany, přehnané proporce | — |
| **Paleta** | **ZRUŠENA** | „*mapování na paletu dělalo sprity špinavé a tmavé (naměřeno)*" |
| **Stín** | elipsa v kódu, šířka 0,7, krytí 0,35 | „*stín se nekreslí modelem*" |
| **Historie** | `_stav` — co je schválené (postava 5/5, meč = provizorní kandidát) | — |

**Z toho plyne:** ADD **není potřeba vymýšlet** — je potřeba ho **vytáhnout
z `spec.json` do lidsky čitelné podoby** a doplnit to, co ve strojové podobě
nemá smysl držet.

### 2.2 Co v ADD chybí

| Chybí | Detail |
|---|---|
| **Lidská vrstva** | Nikde není souvislý popis „jak hra vypadá a proč" — jen JSON a `_popis` pole |
| **Katalog assetů** | Nikde není seznam „co má být ve hře vyrobeno" vs. „co existuje". Přitom `tools/` obsahuje **`sword_candidates.txt`, `items.txt`, `floor_textures.txt`, `ore_chest.txt`, `arming_sword_rest.txt`** — tedy rozhodovací materiál bez výsledku |
| **Dokumentace pipeline** | `tools/blender/build_character.py` (13 kB), `postprocess.py`, `make_iso_tiles.py` (13 kB), `items_postprocess.py` — **fungují, ale nejsou popsané jako postup** |
| **Dva paralelní systémy** | viz §4.1 — **rozpor, ne mezera** |
| **Co je „hotové" u assetu** | `spec.json` má brány pro měření, ale ne lidské „tohle je ono" |
| **Zvuk** | `DESIGN.md:52–53` zvuk popisuje; `ARCHITEKTURA.md` o něm **nemá ani slovo**; `assets/audio/` **neexistuje** |

### 2.3 Co je vyrenderované a **nepoužité**

Naměřeno v `tools/blender/sprites/`:

| Sada | Obsah |
|---|---|
| `sprites/` (hráč) | `body`, `legs`, `torso`, `weapon` × **4 směry** × **8 framů** = 128 PNG |
| `sprites/npc/` | táž struktura znovu = 128 PNG |
| Pomocné | `_compare.png`, `_player_vs_npc.png`, `preview.png`, `_smoke.png` |

**Hra z toho nepoužívá nic.** `assets/sprites/` má 16 souborů plochých spritů
a `check-schema.py` měří právě těch 8 z `assets/spec.json` `role`.

---

## 3. TDD — co existuje a co chybí

### 3.1 Co je obnovitelné

| Co | Kde | Stav |
|---|---|---|
| **Vrstvy (8) a směry závislostí** | `ARCHITEKTURA.md:89–104` | existuje, včetně pravidla „shora dolů, žádné kruhy" |
| **Externí závislosti** | `ARCHITEKTURA.md:106–118` | „obsah = data, ne kód" |
| **Smlouvy (18)** | `ARCHITEKTURA.md:120–145` | tabulka komponent — **jen jména API** |
| **Tvar dat (3 z 18)** | `ARCHITEKTURA.md:147–293` | `sim.combat` §2.1, `Hráč→move` §2.2, `Ukládání→pozice` §2.3 — **vzor, jak psát ostatní** |
| **Konvence Godotu 4** | `CONVENTIONS.md` (12,5 kB) | 8 sekcí pastí — `File`/`json` neexistují, `get`/`set`/`name` kolidují, `extends Node` |
| **Skutečná architektura kódu** | `scripts/*.gd` | registr komponent `get_parent().component(id)`, žádný autoload, `ConfigFile` do `user://` |
| **Brány** | `docs/BRANY-HRY.md` (13 kB) | co která měří a kde má slepá místa |
| **Běhové prostředí** | `main.tscn`, `project.godot` | scéna se staví programově v `game.gd` |

### 3.2 Co chybí

| Chybí | Detail |
|---|---|
| **15 smluv bez tvaru dat** | `ARCHITEKTURA.md` §2 má 18 řádků, tvar dat jen 3. Agent tak dostane jméno a vymyslí si zbytek — naměřeno: `get` vs `hodnota`, `trade` vs `buy/sell/gold` |
| **Architektura běhu** | Jak plyne čas? Kdo vlastní tick? Jak se staví scéna? Dnes je to „*monolit v `game.gd`*" a plán říká „*registr komponent*" — ale **mezi tím není nic** |
| **Datové formáty** | Co je v `assets/levels/*.json` (markery!), co v `assets/data/*.json`. `check-schema.py` o surovinách neví **nic** |
| **Vlastnictví stavu** | §2.3 to řeší pro pozici hráče; pro ostatní stav **ne** |
| **Výkonnostní rozpočet** | `spec.json` má viewport, ale nikde není „60 FPS / kolik ms na frame" |
| **Ukládání** | `save.gd` existuje, formát je v kódu, **ve smlouvě není** |
| **Chybové chování** | Co se stane, když chybí soubor/komponenta? Dnes to každý řeší jinak (`push_error`, `push_warning`, tichý `return`) |
| **Jazyk rozhraní** | `assets/data/*.json` má **české `name`** („Železný meč") a **anglické `id`** (`iron_sword`); `AGENTS.md` to nazývá vadou rozhraní. Není rozhodnuté, co platí |

---

## 4. Rozpory, které blokují

### 4.1 Dva výtvarné systémy — ploché sprity vs. vrstvená postava

| | Ploché sprity | Vrstvená postava |
|---|---|---|
| Kde | `assets/sprites/*.png` (16 souborů) | `tools/blender/sprites/**` (256 PNG) |
| Používá hra? | **ANO** | **NE** |
| Měří brány? | ano (`check-assets.py`, 8 spritů) | ne — „*animace chůze v projektu není – přeskočeno*" |
| Deklaruje `spec.json`? | role ano | **vrstvy ano** („*oblékání jako v UO*") |

**Rozhodnutí:** který systém je budoucnost? **Tohle je blokující** — dokud to
není jasné, ADD nemůže popsat, co má být vyrobeno, a brány nemůžou měřit to
správné.

### 4.2 `DESIGN.md` je zrušený, ale `AGENTS.md` na něj odkazuje jako na zdroj pravdy

`AGENTS.md:91` tvrdí „*`docs/DESIGN.md` — co hra je a jak se má chovat*";
`DESIGN.md:3` se sám hlásí jako **zrušený zdroj pravdy**. Kdo hledá design, čte
zrušený dokument.

### 4.3 Dokument, který je „jediný závazný", popisuje jiný plán

`ARCHITEKTURA.md` §3–4 tvrdí **18 granul v 6 vlnách**; `.forge/roadmap.json` má
**22 granul v 5 vlnách**. Čtyři granule (`world.nodes`, `entity.player.api`,
`persist.save.state`, `tests.harness`) v závazném dokumentu **nejsou vůbec**.

---

## 5. Rozhodnutí, která patří tobě

**Jak to číst:** u každého bodu je `[ ]`, otázka, co už existuje, a **můj návrh**
(kde se dá odvodit). Odpověz `A` = souhlasím s návrhem, nebo napiš vlastní.
Nemusíš odpovědět na všechno — ale **G-1 až G-5 a R-1 blokují GDD**.

### A. GDD — co potřebuju od tebe

```
[ ] G-1  JAK SE HRA HRÁČEM OVLÁDÁ?
         Existuje: nic (project.godot nemá ani jednu vstupní akci)
         Návrh:   klávesnice — šipky/WASD pohyb, E interakce, I inventář, C postava.
                  Myš jen na volbu cíle? (UO má klik-to-move — chceš ho?)
         Dopad:   bez toho nemá ADD ani TDD co popsat

[ ] G-2  JAKÝ POCIT MÁ HRA VYVOLAT? (pilíře, ne featury)
         Existuje: 7 „pilířů" v ARCHITEKTURA.md:19–27, ale jsou to featury
                  („synergie skill+atribut", „svět škálovaný dovedností")
         Návrh:   4 věty o pocitu, např. „cítím se jako řemeslník, který si
                  všechno vyrobí sám"; „svět mě neškáluje, já rostu"
         Dopad:   pilíř je jediné rozhodovací pravidlo, které přežije změny

[ ] G-3  CO HRÁČ DĚLÁ POŘÁD DOKOLA? (hlavní smyčka, věta po větě)
         Existuje: jedna věta „těžit → tavit → kovat → používat → opravovat"
         Návrh:   rozepsat na 6–8 vět jako scénář (jako game-clone §1.3),
                  každá musí fungovat celá, jinak hra není hotová
         Dopad:   tohle je definice „dojeté hry"

[ ] G-4  CO JE VIDĚT NA OBRAZOVCE?
         Existuje: `hud.gd` kreslí HP/atributy/skilly/zlato — jen v kódu
         Návrh:   seznam prvků: lišta s HP/manou, zlato, vybavená zbraň;
                  inventář na I; nic víc v MVP
         Dopad:   UI je vrstva 1 — bez ní hráč nepozná stav

[ ] G-5  JAK HRÁČ POZNÁ ÚSPĚCH?
         Existuje: nic
         Návrh:   žádná „výhra" — cíl je růst postavy; úspěch = dosáhl skillu X
                  a vyrobil si předmět Y. Nebo chceš konkrétní cíl?
         Dopad:   bez toho nelze říct „hra je hotová"

[ ] G-6  ROZSAH V ČÍSLECH
         Existuje: „ostrov + důl + les", 1 nepřítel, 4 materiály, 3 recepty
         Návrh:   zůstat u toho (MVP) a zapsat čísla: 1 mapa, 4 materiály,
                  3 recepty, 1 nestvůra, 1 obchodník, ~15–30 min na sezení
         Dopad:   na rozsahu padají projekty nejčastěji

[ ] G-7  NON-GOALS — co tam ZÁMĚRNĚ není
         Existuje: `DESIGN.md` vyřazuje denní cyklus, alchymii, MMO, magii
                  (ale DESIGN je zrušený)
         Návrh:   přenést těchhle 5 + přidat „žádná fyzika enginu",
                  „žádné UO-soubory" podle skutečného stavu
         Dopad:   bez seznamu zákazů si agent domyslí sousední vrstvu

[ ] G-8  KTERÉ Z 13 REQ-* PATŘÍ DO MVP?
         Existuje: 13 požadavků, ale část z nich je mimo řez (MMO, více postav,
                  asistence, offline)
         Návrh:   do MVP: skills, attrs, craft, econ, interact, world, respawn,
                  death, trade, persist. Mimo: offline, assist, chars, mmo
         Dopad:   určuje, co má TDD vůbec popsat

[ ] G-9  PRVNÍCH 5 MINUT
         Existuje: nic
         Návrh:   hráč se objeví ve městě s 0 zlatem, najde žílu rudy,
                  vytěží, u pece vytaví, u kovadliny uková meč, tím zabije
                  kostlivce
         Dopad:   onboarding je první, co hráč zažije
```

### B. ADD — dvě rozhodnutí

```
[ ] A-1  KTERÝ VÝTVARNÝ SYSTÉM JE BUDOUCNOST?   ← BLOKUJÍCÍ
         Existuje: ploché sprity (hra je používá) vs. vrstvená postava
                  (256 vyrenderovaných PNG, hra je nepoužívá)
         Návrh:   vrstvená postava — odpovídá `spec.json`, umožňuje oblékání
                  a je to věc, která odlišuje UO od jiných her
         Dopad:   určuje, co má být vyrobeno a co mají brány měřit

[ ] A-2  POKRAČOVAT V GENEROVÁNÍ ASSETŮ PŘES SDXL/BLENDER?
         Existuje: `spec.json` `_stav` říká, že meč je PROVIZORNÍ kandidát,
                  SDXL u dlouhých čepelí dělá vady
         Návrh:   ano, ale s výslovným pravidlem „co SDXL neumí, se dělá v Blenderu"
         Dopad:   ovlivní katalog assetů
```

### C. TDD — tři rozhodnutí

```
[ ] R-1  ARCHITEKTURA BĚHU                               ← BLOKUJÍCÍ pro GDD
         Existuje: `game.gd` je monolit (377 řádků); plán říká „registr
                  komponent", ale **mezi tím není nic** — a `engine.shell`
                  je blokovaná mrtvou granulí
         Návrh:   potvrdit cestu „komponenty + registr `component(id)`" a
                  doplnit, kdo vlastní tick a jak se staví scéna
         Dopad:   bez toho nelze napsat 15 chybějících smluv

[ ] R-2  VÝKONNOSTNÍ ROZPOČET
         Existuje: nikde
         Návrh:   60 FPS při 960×540, simulace pod 2 ms na snímek
         Dopad:   bez rozpočtu nemá výkonová brána co měřit

[ ] R-3  JAZYK OBSAHU A ROZHRANÍ
         Existuje: `id` anglicky (`iron_sword`), `name` česky („Železný meč"),
                  UI česky, `AGENTS.md` to nazývá vadou
         Návrh:   `id` a klíče anglicky (stroj), `name` a texty česky (člověk)
                  — a zapsat to jako pravidlo do smluv
         Dopad:   ovlivní datové formáty i všechny texty
```

**Co se stane po odpovědích:** napíšu tři dokumenty v tomhle pořadí —
**GDD** (co hra je a jak se hraje) → **ADD** (jak vypadá a co vyrobit) →
**TDD** (jak je postavená a jaké má smlouvy). Každý s hlavičkou, s odkazy na
zdroje a s tím, co v něm **záměrně není**.

---

## 6. Co tahle rekonstrukce neví

- **Neprošel jsem `tools/` soubor po souboru** — četl jsem jen názvy a velikosti
  a `spec.json`. Skripty `build_character.py`, `make_iso_tiles.py` a
  `items_postprocess.py` **jsou funkční, ale nevím přesně, co který umí** —
  to patří do ADD jako dokumentace pipeline a budu to muset přečíst.
- **Nevím, jestli je meč `sword.png` opravdu ten, který `spec.json` označuje za
  provizorní** — soubor existuje, ale kandidátů je víc (`sword_candidates.txt`,
  `arming_sword_candidates.txt`).
- **Nevím nic o zvuku** — `DESIGN.md` ho popisuje, ale `assets/audio/`
  neexistuje a v repu nejsou žádné zvukové soubory.
- **Nepočítal jsem, kolik z 256 vyrenderovaných PNG je použitelných** —
  naměřil jsem jen jejich existenci a strukturu.

## 7. Co čeká na tebe

**Odpovědět na `G-1` až `G-9`, `A-1`, `A-2` a `R-1` až `R-3`** (§5) — ideálně
zkráceně (`G-1 A, G-2 vlastní znění: …`). **Blokující jsou `G-1`–`G-5`, `A-1`
a `R-1`**; na ostatních se dá pracovat souběžně.

**A jedna věc, kterou bych chtěl výslovně:** tyhle tři dokumenty budou
**závazné** — znamená to, že `docs/DESIGN.md` a `docs/ARCHITEKTURA.md` se
**nahradí**, ne že k nim přibudou další. Jinak vznikne **čtvrtý zdroj pravdy**,
což je v tomhle projektu už jednou naměřená vada.
