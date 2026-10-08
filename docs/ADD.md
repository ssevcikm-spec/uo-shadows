# ADD — `uo-shadows`: jak hra vypadá, proč to tak je a co má být vyrobeno

> **Co tenhle dokument JE:** **art design document** — **lidská vrstva** ke
> strojovému schématu `assets/spec.json`. Říká, jak hra vypadá a **proč**,
> jaký je katalog assetů („co má být vyrobeno“ vs. „co existuje“), jak funguje
> pipeline (Blender / SDXL) a co je u vzhledu **vědomě odložené**.
>
> **Nenahrazuje `assets/spec.json`** — ten zůstává **strojová pravda** (rozměry,
> role, vrstvy, brány). ADD je k němu **člověčí protějšek**; kde si odporují,
> platí `spec.json` pro čísla a ADD pro **důvod**.
>
> **Odkud brát stav:** tenhle dokument je stav vzhledu. **Zdroj rozhodnutí** je
> `_analyza/DESIGN-REVIZE-2.md` (`§N` = jeho oddíl); co má hra dělat, říká
> `docs/GDD.md`; jak je postavená, `docs/TDD.md`.
>
> **Vzniklo:** 8. 10. 2026 sepsáním z `assets/spec.json`,
> `_analyza/DESIGN-REVIZE-2.md` §7 a §14.1, `_analyza/REKONSTRUKCE-ADD-TDD-GDD.md`
> §2 a **měřením** assetů a pipeline (naměřeno 8. 10. 2026 — u čísel je řečeno,
> čím; Godot ani Blender se **nespouštěl**, četl se kód a měřily se soubory).
>
> **Co tenhle dokument NENÍ:** není katalog „co je hotové“ (hotovost se měří
> branami, ne slibem), není rozpis výroby (to je plán) a **není návrh nového
> vzhledu** — popisuje rozhodnutý směr a placeholdery.
>
> **Jak se mění:** ADD je **stav** — přepisuje se, dokud je odložené rozhodnutí
> `A-1`; naměřené rozpory (ADD §11) se **doplňují**, ne mažou.

---

## 1. Čím je vzhled deklarovaný (strojová část)

**Strojová ADD je `assets/spec.json`** (88 řádků, 5 496 B — naměřeno). Není to
sbírka čísel, jsou to **rozhodnutí s odůvodněním**. Co v ní je:

| Co | Hodnota | Zdroj / důvod v souboru |
|---|---|---|
| **Viewport** | `960×540` | „*na 1080p zvětšuje PRESNE 2x (celociselne, zadne rozmazani)*“ |
| **Dlaždice** | izometrický diamant **96×48**, poměr **2:1** | — |
| **Role (8)** | `player` 96/128 (4 směry, 8 framů), `npc` 96/128 (4/8), `enemy` 64/96 (4/**4**), `ore` 48/64 (1/1), `chest` 48/64 (1/1), `weapon` 48/64 (1/1), `potion` 32/48 (1/1), `coin` 24/32 (1/1) | formát `visual_height` / `canvas` / `smery` / `framy` / `stin` |
| **Vrstvy oblékání** | **8 slotů**: `body, legs, feet, torso, cloak, head, shield, weapon`; **startovní sada 4**: `body, torso, legs, weapon`; tonování u `cloak, torso, legs` | „*jakákoli kombinace výbavy je zdarma, bez dalšího rendru*“ |
| **Brány (6)** | výška ±10 %, 0 děr, okraj ≤5 %, IoU ≥0,80, posun těžiště ≤3 px, kontrast ≥150 | u kontrastu: „*u nepritele v plošinovce vyšlo 93 = splýval s podlahou*“ |
| **Styl** | UO: The Second Age — realistický až mírně fantasy, **NE pixel art** | „*UO vypadalo realisticky proto, že jeho sprity byly PŘEDRENDROVANÉ 3D MODELY*“ |
| **Zákazy stylu** | 16barevná paleta, dithering, nearest-neighbour zmenšování, výrazné pixelové hrany, přehnané fantasy proporce (nepraktický meč) | tamtéž |
| **Paleta** | **ZRUŠENA** (`zdroj: null`) | „*mapování na paletu prostředí dělalo sprity špinavé a tmavé (naměřeno u prvního testu)*“ |
| **Stín** | **nekreslí se modelem** — elipsa v kódu, šířka 0,7 šířky postavy, krytí 0,35 | „*stin se nekresli modelem, ale v kode*“ |

**Co z toho plyne pro každé rozhodnutí o vzhledu:** barvy **nejsou** omezené
paletou (stovky až tisíce barev), rozměry **jsou** závazné (96×48 dlaždice,
96 px postava, 128 px canvas) a **hladkost je závazná** (zmenšovat Lanczosem,
ne nearest).

### 1.1 Dlaždice a terén (co existuje)

`assets/tiles/`: `grass`, `dirt`, `sand`, `stone`, `water`, `brick` — **každá
96×48** — a `tileset.png` (576×48) + `manifest.json` (naměřeno 8. 10. 2026).
Mapa `main.json` používá tři z nich: `0`→`brick` (zeď), `1`→`stone` (podlaha),
`2`→`dirt` (chodba); `grass` používá scéna jako pozadí.

---

## 2. Jak má hra vypadat — a proč (lidská vrstva)

- **Izometrická 2.5D jako Ultima Online** — dlaždicový svět viděný shora,
  dlaždice i postavy v projekci **2:1**. Cíl je dojem „**reálný svět viděný
  shora**“, ne retro. (`DESIGN.md:48–51`, `spec.json` `_popis`)
- **Předrenderované 3D do 2D.** Postava **není kreslená** — je to 3D model
  renderovaný do sprity. Proto vypadají sprity realisticky: skutečné světlo,
  skutečné materiály, přirozené barvy, jen malý výsledný rozměr. (`spec.json`
  `styl._popis`)
- **Žádný pixel art.** Zakázaná je 16barevná paleta, dithering, nearest-neighbour
  zmenšování i výrazné pixelové hrany. (`spec.json` `styl`)
- **Proporce lidské a praktické** — „zbraň musí vypadat použitelně, ne jako
  dekorace“ (`spec.json` `styl.proporce`).
- **Stín je kód, ne grafika** — elipsa pod postavou (šířka 0,7 šířky postavy,
  krytí 0,35). Model se nestíní. (`spec.json` `stin`)

---

## 3. Dva výtvarné systémy — a co je o nich dnes PRAVDA

`_analyza/REKONSTRUKCE-ADD-TDD-GDD.md` §4.1 to nazvalo **blokujícím rozporem**:
v repu jsou **dvě sady obrázků** a hra používá jen jednu.

| | Ploché sprity | Vrstvená postava |
|---|---|---|
| Kde | `assets/sprites/**` — **16 PNG** | `tools/blender/sprites/**` — **258 PNG** |
| Kolik | 8 přímo + 8 v `items/` | 128 hráč + 128 NPC + 2 pomocné (`_compare.png`, `_player_vs_npc.png`) |
| Rozměry | canvas podle role (`player.png` 128×128, `coin.png` 32×32) | canvas **128×128**, postava **96 px** vysoká |
| Struktura | jedna kresba celé postavy | **4 vrstvy** (`body`, `torso`, `legs`, `weapon`) × **4 směry** × **8 framů chůze** |
| Odkazy z herního kódu | **ano** (`game.gd` je kreslí) | **0** — v `scripts/`, `main.tscn`, `project.godot` ani `.tres` **není ani jeden odkaz** (naměřeno plošným skenem 414 textových souborů) |
| Měří je brány | ano (`check-assets.py`, 8 spritů) | ne — chůze se **neměří** (v `assets/sprites` nejsou `walk_*`) |

> **⚠ Měřená korekce tvrzení „hra je nepoužívá“ (naměřeno 8. 10. 2026):**
> obsah se **používá, ale zploštěný**. `assets/sprites/player.png` je
> **pixel-identický** se složením `body_d0_f1 + legs_d0_f1 + torso_d0_f1 +
> weapon_d0_f1` z `tools/blender/sprites/` (měřeno `ImageChops.difference(…)
> .getbbox() is None`; z 32 kombinací směr × frame odpovídá **právě směr 0,
> frame 1**). Totéž platí pro `npc.png` proti `tools/blender/sprites/npc/`.
> **Důsledek pro ADD:** hra dnes zobrazuje **1 frame ze 128** jako jeden plochý
> obrázek — animace chůze se **nepoužívá vůbec** a vrstvení také ne. Není to
> „druhý, cizí systém“: je to **tatáž grafika zploštěná**.

---

## 4. Rozhodnutí `A-1`: vrstvená grafika je CÍL — a je VĚDOMĚ ODLOŽENÁ

**Uživatel:** *„Nerozumím zadání. Zdá se mi, že vrstvení má větší potenciál.
Například postava hráče má zobrazovat co má nasazené — meč? krumpáč? zbroj nebo
oblečení? Má meč v ruce nebo u pasu?“* (`VSTUPY` §1.7). A k odložení: *„sice
souhlasím, ale zdráhavě“* (`K5`/`A-1`, §6).

**Co je rozhodnuté:**

1. **Vrstvení je směr, ne volba k diskusi** — `docs/GDD.md` §12 má milník
   **`M6 — Grafika`** („postava ukazuje, co má nasazené“) a uživatel potvrdil
   `M0`–`M6` (`P1` „Sedí M0–M6“). **Grafika jde až nakonec** — po `M5`.
2. **Rozhodnutí o finálním vzhledu se vědomě odkládá** na dobu **po prototypech
   `M0`–`M5`** (§7: „Finální vzhled zůstává nerozhodnutý a vrací se v kole 4
   s číslem, kolik obrázků vrstvená postava znamená“ — to číslo je níž).
3. **Dokud smyčka nefunguje, nevzniká žádná nová grafika** — jen primitivní
   tvary (`VSTUPY` §2.7). „*Dokud nefunguje smyčka, nevzniká žádná grafika —
   jen primitivní tvary.*“

**Cena vrstvení (naměřená čísla, ať se rozhoduje s otevřenýma očima):**

| Co | Kolik | Odkud |
|---|---|---|
| Jeden kus výbavy dnes | **4 směry × 8 framů = 32 obrázků** | `spec.json` `role.player`: `smery` 4, `framy` 8 |
| Kdyby se rozhodlo pro **8 směrů** (`N-2`) | **64 obrázků na kus** | §14.1 `N-2` |
| Zbraň „v ruce“ **a** „u pasu“ | **2× obrázků pro zbraně** | §13.1 (rozhodnuto: **MVP jen v ruce**) |
| Dnešní stav | **4 vrstvy × 4 směry × 8 framů = 128 PNG** na postavu (hráč i NPC zvlášť) | naměřeno: `tools/blender/sprites/` = 128 + `npc/` = 128 |

**Rozhodnutí, která k tomu patří:** **osm směrů až po prototypech** (`N-2`),
**zbraň jen v ruce** (§13.1), **paperdoll až s vrstvenou grafikou** (`N-9`).

**Co v `M6` chybí a musí se dorozhodnout:** kolik z **8 slotů** `spec.json`
(`body, legs, feet, torso, cloak, head, shield, weapon`) se skutečně vyrobí.
Startovní sada jsou **4**; zbytek je deklarace, ne slib.

---

## 5. Placeholdery: primitiva jako základ, free assety jen na to, co nemá mřížku

**Rozhodnuto** (§7) — uživatel chtěl místo holých obdélníků „předgenerovanou
primitivní vektorovou grafiku nebo free assety“; odpověď je **obojí, ale
rozdělené podle jedné podmínky — ROZMĚRU**:

| Cesta | Co to je | Cena | Riziko |
|---|---|---|---|
| **Generovaná primitiva** (kód nakreslí kosočtverec dlaždice, postavu ze dvou–tří tvarů, rudu jako hromádku) | **základ** — zdarma, konzistentní, barva = druh suroviny | jeden malý úkol | **žádné** — vzor už v kódu je (`game.gd` kreslí barevný obdélník, když sprite chybí) |
| **Free assety** | **jen na to, co nemá mřížku**: ikony, UI, **zvuk** (a textury terénu) | stahování + kontrola licence + převzorkování | **jiná mřížka** (free izo sady bývají 64×32 nebo 128×64) → rozbité rozměry |

**Podmínka, která není styl, ale rozměr:** dlaždice **96×48**, postava
**96 px**, okno **960×540**. Když placeholder tenhle rozměr nedodrží,
**rozpadne se rozvržení mapy** a při přechodu na finální grafiku se předělává
**scéna, ne obrázky** (§7).

**Cena placeholderů:** prototyp bude čitelnější a líp se ladí (což je pro ladění
smyčky důležité), **ale není to investice do finálního vzhledu** — až se vrstvená
grafika rozhodne, placeholdery se zahodí. **Kdo si je splete s cílem, udělá
z prototypu slepou uličku.** (§7)

---

## 6. Katalog assetů: „co má být vyrobeno“ vs. „co existuje“

**Naměřeno 8. 10. 2026** (`os.walk` přes celý strom; rozměry z hlavičky PNG).

### 6.1 Co existuje

| Sada | Souborů | Co to je |
|---|---|---|
| `assets/sprites/**` | **16 PNG** | 8 rolí podle `spec.json` (`player.png` 128², `npc.png` 128², `enemy.png` 96², `ore/chest/weapon.png` 64², `potion.png` 48², `coin.png` 32²) + 8 v `items/` (`*_final.png`, `slime_final.png`) |
| `assets/sprites/items/` (textury) | 2 PNG | `dirt_tex.png`, `grass_tex.png` — **1024×1024**, dohromady ~4,2 MB |
| `assets/tiles/` | 7 PNG | 6 dlaždic **96×48** + `tileset.png` (576×48) |
| `assets/levels/` | 1 PNG | `main.preview.png` (480×256) — náhled mapy |
| `tools/blender/sprites/**` | **258 PNG** | vrstvená postava (hráč i NPC), 128×128 canvas, **nepoužitá po vrstvách** |
| `tools/blender/` (pomocné) | 2 PNG | `preview.png` (512²), `_smoke.png` (256²) |

**Celkem `assets/` = 57 souborů, 24 PNG.**

### 6.2 Co má být vyrobeno (a co z toho není)

| Co GDD žádá (rozsah `M`, GDD §10) | Existuje dnes | Chybí vyrobit |
|---|---|---|
| **11 materiálů** (běžné + vzácné složky + 3 meziprodukty) | 4 (`iron_ore`, `wood`, `stone`, `iron_ingot`) | ikony/objekty pro `coal`, `flax`, `silver_ore`, `hardwood`, `fine_flax`, `cloth`, `steel_ingot` |
| **7 předmětů** | 2 spritey role (`weapon.png`, `potion.png`) + `sword_final.png` | `iron_sword`, `iron_armor`, `steel_sword`, `pickaxe`, `hammer`, `bandage`, `silver_ring` (7 ikon / modelů) |
| **3 nestvůry** | 1 (`enemy.png` / `slime_final.png`); `spec.json` `role.enemy` = 96 px, **4 framy** | `wolf`, `bandit` (+ animace: dnes **žádná** nestvůra animaci nemá) |
| **8 receptů** | 3 | 5 receptů — **data, ne grafika** (ale každý nový výstup = předmět) |
| **6 dovedností** | 4 | 2 — **data**, grafiku nepotřebují |
| **mapa: vesnice + důl + les + pole** | 1 mapa 30×16 (`main.json`), dlaždice 6 druhů | dlaždice pro důl/les/pole, **markery zdrojů** (dnes 4 markery: spawn, 2× coin, exit) |
| **UI**: inventář, mapa, stav světa, zakázka s postupem | **nic** | UI prvky (rámeček, ikony, panel) — sem patří **free assety** (ADD §5) |
| **zvuk**: ambientní hudba + efekty | **nic** (`assets/audio/` **neexistuje**) | hudba a zvuky — **free assety** (§5, §8) |
| **vrstvená postava**: 8 slotů | **4 vrstvy** vyrenderované (`body`, `torso`, `legs`, `weapon`), jen pro hráče a NPC | `feet`, `cloak`, `head`, `shield` — **až `M6`** (ADD §4) |
| **animace** | **jen chůze** (8 framů, 4 směry); žádné idle/attack/death | idle, útok, smrt — **až když je smyčka** (ADD §4) |

> **⚠ Co v katalogu chybí a je to vidět:** `tools/*.txt` obsahují **6 seznamů
> promptů** (rozhodovací materiál pro SDXL) — a **žádný skript v repu je nečte**
> (naměřeno: 0 odkazů). Kandidáti na sword z nich **na disku neexistují**
> (`sword1..6.png`, `asword1..6.png` → `False`); `tools/sword_contact.py`, který
> z nich staví kontaktní list, tedy **také nemá co zobrazit**.

---

## 7. Pipeline: jak se assety vyrábějí

**Princip:** 3D model → render do 2D spritu, **zdarma a lokálně** (Blender
headless). Cesta „AI obrázky“ (SDXL) je pro **předměty a textury**, ne pro
postavu. (`spec.json` `styl.technika`, `_stav`)

### 7.1 Cesta A — postava z Blenderu (hotová, používaná)

| Krok | Nástroj | Co dělá | Výstup |
|---|---|---|---|
| 1 | `tools/blender/build_character.py` (338 řádků) | postaví postavu z primitiv, **rig 14 kostí**, chůzi přes **2-kostní IK**, izo kameru (ORTHO, `ortho_scale 2.4`) a vyrenderuje **vrstvy zvlášť** | `tools/blender/raw/{layer}_d{d}_f{f}.png`, **1024×1024** |
| 2 | `tools/blender/postprocess.py` (132 řádků) | vezme **jeden `union_bbox` přes všech 128 obrázků** (aby framy seděly na sebe), zmenší **Lanczosem** na výšku přesně **96 px**, složí na canvas **128 px** (chodidla na `FEET_Y = 112`) | `tools/blender/sprites/{layer}_d{d}_f{f}.png` |

**Jak se to spouští** (z docstringu skriptu, doslovně):
`blender -b -P build_character.py -- --preview` (jeden náhledový snímek),
`blender -b -P build_character.py` (plný render), a pak
`python tools/blender/postprocess.py` (vyžaduje Pillow).

**Parametry, které se musí dodržet (naměřeno v kódu):** `FRAMES = 8`,
`LAYERS = ["body", "torso", "legs", "weapon"]`, **4 směry**
(`aim_cam(d * π/2)` pro `d` v `range(4)`), chůze `STRIDE 0.45`, `LIFT 0.09`,
`bob 0.02`, paže `0.50`, náklon `−0.05`, `CANVAS = 128`, `VISUAL_H = 96`,
`FEET_Y = 112`. **Pořadí skládání vrstev** je `body → legs → torso → weapon`.

**Závislost na Blenderu:** Blender **není v PATH** (naměřeno
`shutil.which("blender")` → `None`); reálná cesta je
`C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`, verze
**5.2.1 LTS**. **Skripty verzi nekontrolují ani nepinují** — spoléhají na
`blender` v PATH. `render.engine = 'BLENDER_EEVEE'` je na 5.2.1 platný.

> **⚠ Kde se to smí renderovat:** **Blender v orchestra není a být nemůže** —
> `ubuntu-latest` ho nemá a instalace je drahá. Render tedy běží **na domácím
> uzlu** nebo se sprity **commitují hotové**. (`docs/BRANY-HRY.md`)

### 7.2 Cesta B — předměty a textury přes SDXL (částečně hotová)

- **Prompty jsou v repu** jako `.txt` (jeden řádek = jeden prompt ve formátu
  `prompt | out=<soubor> | seed=<n> | size=WxH`), **6 souborů**:
  `items.txt` (meč, lektvar, mince), `ore_chest.txt` (žíla rudy, truhla),
  `floor_textures.txt` (tráva, hlína), `sword_candidates.txt` (6 kandidátů),
  `arming_sword_candidates.txt` (6 kandidátů historického meče),
  `arming_sword_rest.txt` (duplikát zbytku dávky).
- **Postprocessing:** `tools/items_postprocess.py` — zmenšení a **odstranění
  pozadí PODLE BARVY POZADÍ, ne podle jasu** (`spec.json` `_stav`).
- **Známé meze SDXL (naměřeno a zapsáno ve `spec.json` `_stav`):**
  **dlouhé čepele dělá vadně** a žádný kandidát nebyl plně historický → meč je
  **PROZATÍMNÍ**; u `ore`/`rock` dával SDXL **tmavé pozadí** (řeší se promptem
  „product photo“); lektvar a mince jsou **čisté**.

**Pravidlo, které z toho plyne (`A-2`):** **co SDXL neumí, se dělá v Blenderu.**
Není to zákaz SDXL — je to rozdělení podle toho, co které cestě jde.

### 7.3 Co pipeline NEDĚLÁ

- **Nevyrábí animace** kromě chůze (jediná funkce v `build_character.py`).
- **Nevyrábí UI, ikony ani zvuk** — na to jsou free assety (ADD §5).
- **Nedrží licenci ani původ** (viz §12).
- **Neběží v CI** — sprity se do repa commitují hotové.

---

## 8. Zvuk

**Stav: neexistuje.** `assets/audio/` **není** (naměřeno `isdir` → `False`),
stejně jako `assets/audio/sfx/` a `assets/audio/music/`. V repu **není ani jeden
zvukový soubor**.

**Co je o zvuku rozhodnuté:** jen to, co o něm říká **historický** `DESIGN.md:52–53`
(doslovně): *„**Zvuk:** ambientní fantasy hudba s jemnými zvuky přírody,
poškození předmětů, alchymie a NPC reakcemi“* — a to je **jediný výskyt slova
„Zvuk“ v celém `docs/`**. Pozor: **alchymie je mimo MVP** (`N11`), takže ten
popis **není závazný seznam**; je to směr.

**Co kód na zvuk chce (a nemá):** `scripts/game.gd:11` má
`SFX_DIR := "res://assets/audio/sfx/"`, `:113` skládá
`res://assets/audio/music/%s.wav` a hraje hudbu; `tests/run_tests.gd:107–109`
iteruje `assets/audio/sfx`, `assets/audio/music` a `assets/ui` — a **žádný z těch tří adresářů v repu není** (naměřeno). **Kód tedy na zvuk i UI sahá a tiše nenajde nic.**

**Kde je volné místo pro free assety:** **zvuk a hudba** jsou podle §7 a
`VSTUPY` §2.5 **první místo, kde se free assety mají vzít** — nemají mřížku,
takže nehrozí rozbité rozměry (na rozdíl od izo dlaždic).

**Co se musí dorozhodnout (patří do plánu, ne do ADD):** odkud zvuk vzít, pod
jakou licencí a **jak se to ověří** — `check-assets.py` umí měřit hudbu
**z manifestu**, který v repu není (`assets/audio/music/manifest.json`:
kroky, skoky, motiv, smyčka), takže „hudba se neměří“ (`BRANY-HRY.md`).

---

## 9. UI a font

- **Font: v repu není žádný** (naměřeno `os.walk` na `.ttf/.otf/.woff/.fnt/
  .font` → **0 nálezů**). Hra používá **vestavěný font Godotu**;
  `project.godot` **nemá sekci `[gui]`** ani vlastní Theme a v repu **není ani
  jeden `.tres`**. Jediné nastavení v kódu je velikost:
  `add_theme_font_size_override("font_size", 8)` (`game.gd:60` a `:222`).
- **UI prvky: neexistují** — `assets/ui/` **není**, přestože kód i testy na
  `res://assets/ui/panel.png` sahají (`game.gd` načítá `NinePatchRect`, když
  soubor existuje — a on neexistuje).
- **Rozhodnutí, co je na obrazovce**, je v `docs/GDD.md` §7 (herní okno,
  ukazatel stavu s čísly, stav světa, zakázka, inventář, mapa; **paperdoll až
  s vrstvenou grafikou**).
- **Kde vzít UI a font:** **free assety** (§7, `VSTUPY` §2.5) — UI a ikony
  mřížku nemají, takže je to bezpečné místo pro cizí obsah.
- **Co ADD neurčuje:** konkrétní rozložení lišty a vzhled panelů — to je
  **práce k milníku `M2`/`M4`** (až je co zobrazovat), ne rozhodnutí k dnešku.

---

## 10. Brány, které na vzhled dohlížejí (a kde mají slepá místa)

Detail: `docs/BRANY-HRY.md`. Tady jen to, co se týká **vzhledu**:

| Brána | Co měří | ⚠ Slepé místo (naměřené) |
|---|---|---|
| `check-schema.py` (**tvrdá**) | že deklarace (`spec.json`), mapy, vykreslování a dlaždice říkají totéž číslo | — |
| `check-assets.py` | sprity proti `spec.json`: výška vs. spec, neprůhledný okraj, díry v siluetě, počet barev, poměry mezi rolemi, shoda siluet mezi framy chůze; hudbu z manifestu | **animace se NEMĚŘÍ** — hledá `assets/sprites/walk_*.png`, jenže chůze je rozložená po vrstvách v `tools/blender/sprites/`; limit `min_silhouette_iou: 0.80` se tak **nikdy neuplatní**, i když spec deklaruje `framy: 8` |
| `verify-level-render.py` | že snímek hry odpovídá mapě | nemá offline test |
| `vision.mjs` | **vidí** — pošle obrázek modelu a vrátí text/JSON (režimy `presence`/`diff`) | **neblokuje** (`exit 1` běh nezhodí); názor modelu má chybovost a falešný poplach je dražší než přehlédnutí |
| `baseline.py` | co je vizuálně **schválené (LGTM)** a co se změnilo | **LGTM cache je lokální optimalizace — v CI neplatí nikdy** (`baseline.py:252` chce obrázek uvnitř repa, CI píše do `/tmp/frames`) |

**Naměřená čísla k baseline:** `.forge/vision/baseline.json` má **272 záznamů**
= 16 z `assets/sprites` + 256 z `tools/blender/sprites` (pomocné soubory
s podtržítkem se přeskakují). **Schválené jsou tedy sprity, ne snímky hry.**

> **Pravidlo pro „hotový asset“:** brány umí změřit, že sprite **odpovídá
> specu** — **neumí** říct, že je to **on**. „Tohle je ono“ je lidské rozhodnutí
> (a proto existuje `baseline.py` se `schval`/`zamitni`).

---

## 11. Naměřené rozpory ve vzhledu (zapsané, ne opravené)

**Zadání je psaní dokumentů, ne oprava kódu** (`ZADANI-GDD-ADD-TDD.md` §6.1):
co dokument odhalí, **zapíše**. Všechno níž je naměřeno 8. 10. 2026.

| # | Rozpor | Důkaz | Proč to vadí |
|---|---|---|---|
| 1 | **„v 5 směrech“ vs. 4 směry** | `spec.json` `styl.technika` říká „v 5 směrech“; `role.*.smery` = **4** u všech rolí a pipeline renderuje 4 (`build_character.py`, `range(4)`) | kdo se řídí textem, vyrenderuje 5. směr, který nikdo nepoužije |
| 2 | **Filtr textur vs. zákaz nearest** | `project.godot` `default_texture_filter = 0` = **Nearest** (s komentářem „u pixel-artu žádoucí“); `spec.json` přitom zakazuje **nearest-neighbour** a pixel art | u **celočíselného zvětšení 2×** je Nearest zamýšlený (ostrý obraz); u dlaždic, které `level.gd` škáluje poměrem `cell_w / šířka_textury`, vznikne **neceločíselné** zvětšení — a to je přesně to, co spec zakazuje |
| 3 | **`sprites.json` v kořeni repa** | 17 řádků, deklaruje `colors: 16/12` a `size: 64` pro hráče — legacy manifest šablony; **žádný skript ho nečte** (0 výskytů jinde v repu) | druhý zdroj pravdy o rozměrech a paletě, který `spec.json` popírá |
| 4 | **`spec.json` odkazuje na soubory, které neexistují** | `_stav` uvádí `tools/gamewindow_preview.py` → `_gamewindow_preview.png` (960×540) — **soubor není**; `:11` uvádí zdroj meče `assets/sprites/items/sword.png` — **soubor není** (je tam `sword_final.png`) | historie v `_stav` se čte jako stav |
| 5 | **Docstringy pipeline lžou o počtu framů** | `build_character.py` docstring říká „4 framy“, kód má `FRAMES = 8`; `postprocess.py` popisky říkají „4 framy“, kód skládá **8** | kdo čte popis, vyrobí 4 framy a rozbije vazbu na `spec.json` (`framy: 8`) |
| 6 | **Zmíněná brána `check-licence.py` neexistuje** | `docs/BRANY-HRY.md` ji zmiňuje; v `.forge/` **není** (14 souborů, měřeno) | kdo se na ni spolehne, nemá kontrolu licence — a licence chybí úplně (ADD §12) |
| 7 | **Název projektu ve exportu — OPRAVENO 8. 10. 2026** | `export_presets.cfg` má `product_name` = `uo-shadows` a `copyright` prázdné; **`company_name` zůstává `GameForge`** (je to vydavatel, ne název hry — k rozhodnutí zvlášť) | jméno hry je sjednocené s repem; zbývá jen vydavatel a copyright |

---

## 12. Licence a původ assetů

**Stav: v repu není žádný záznam.** Naměřeno: `LICENSE`/`LICENCE`/`CREDITS`/
`COPYING`/`NOTICE` **neexistuje** (kontrolováno `os.walk` i `git ls-files`);
`assets/**/*.txt` **není**; `export_presets.cfg` má `copyright` **prázdné**.

**Co se dá doložit nepřímo (a v repu to nikde není napsané):**

- **postava a dlaždice jsou vlastní procedurální obsah** — vyrábí je vlastní kód
  (`tools/blender/build_character.py`, `tools/make_iso_tiles.py`), žádný cizí
  model ani textura;
- **předměty a textury vznikly z vlastních promptů** v `tools/*.txt`
  (seedy jsou v nich zapsané, takže je výroba reprodukovatelná);
- **v repu nejsou žádné stažené cizí assety** — pokud se použijí free assety
  (§5, zvuk a UI), **tehdy** vzniká povinnost licenci doložit.

**Co to znamená pro plán (ne pro ADD):** než se stáhne první free asset
(nejpravděpodobněji zvuk nebo UI), musí vzniknout **místo, kam se licence
zapisuje** — dnes by se původ ztratil. Není to vada vzhledu, je to **chybějící
záznam**, a patří na seznam úkolů před prvním stažením.

---

## 13. Co v tomhle dokumentu ZÁMĚRNĚ NENÍ

- **Design a mechaniky** (co je zábava, čísla obsahu, `V1`–`V8`) →
  `docs/GDD.md`. ADD neříká, **co** hra dělá, jen **jak vypadá**.
- **Technika a smlouvy** (tik, registry, datové formáty, výkon) →
  `docs/TDD.md`.
- **Rozpis výroby assetů po granulích a pořadí** → `.forge/roadmap.json`
  (vzniká z milníků v GDD §12).
- **Konkrétní rozměry, role, vrstvy a tolerance** → `assets/spec.json`
  (ADD je neopisuje jako druhý zdroj; vysvětluje je).
- **Finální vzhled a rozhodnutí „ploché vs. vrstvené“** → **vědomě odloženo**
  na `M6` po prototypech `M0`–`M5` (ADD §4). ADD **neslibuje**, jak to dopadne.
- **Rozhodnutí o zvuku** (odkud, jaká licence, jaký manifest) → plán;
  ADD jen zaznamenává, že **zvuk dnes není** a že je to první místo pro free
  assety.
- **Historie rozhodnutí a jejich ceny** → `_analyza/DESIGN-REVIZE-2.md`
  (needituje se).
