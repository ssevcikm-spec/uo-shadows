# Rozpory a drift v dokumentech `uo-shadows` — měření a návrh řešení

> **Co tenhle dokument JE:** **analýza (snapshot) rozporů mezi dokumenty** —
> seznam míst, kde si dva dokumenty (nebo dokument a měření) odporují, s citací
> **obou** stran, s tím, **co je pravda podle měření**, a s návrhem řešení.
>
> **Co z něj platí:** platí **k datu měření** (15. 10. 2026, `HEAD = 6986b0d`,
> pracovní strom čistý, `origin/main = 01a9649`). **Nic jsem neopravil** — všechny
> návrhy jsou ke schválení; až se podle nich bude psát, patří do hlavičky
> přepsaného dokumentu „podle `_analyza/PRACE-2026-10-15/ROZPORY.md`“.
>
> **Vzniklo:** 15. 10. 2026 (session, která **nemění kód ani dokumenty**).
> Zadání vyšlo z `ZASTAVENO.md:68–70` („sedm rozporů v dokumentech“) — to je
> **začátek, ne úplný seznam**; naměřeno je **24 rozporů** (níž).
>
> **Rozlišení, které se v tomhle dokumentu drží (a proč):**
> **rozpor** = dvě tvrzení si odporují (někdo se musí rozhodnout) ·
> **drift** = dokument zaostal za kódem/spec/rozhodnutím (opravuje se text) ·
> **duplicita** = totéž je na dvou místech a kopie se rozejdou ·
> **neškodné, ale matoucí** = měření ukázalo, že to neškodí — a je to zapsané,
> aby to někdo neopravoval jako vadu.
>
> **Co tenhle dokument NENÍ:** není oprava (nic jsem nezměnil), není plán práce
> a **není náhrada `ZASTAVENO.md`** — ten zůstává záznamem o zastavení projektu.
>
> **Historická čísla se nepřepisují:** kde bylo číslo ve svém čase správné
> (např. `57 funkcí` v `BRANY-HRY:87`, `15 souborů` v `TDD:779`), je to
> v tabulkách níž označené jako **„ve svém čase správné“** — rozdíl je čas,
> ne nepravda.

---

## 1. Jak jsem to měřil (a co z toho vyšlo)

| Čím | Co to udělalo | Výsledek |
|---|---|---|
| `python .forge\check-wiring.py .` | kontrola zapojení funkcí | **97 funkcí v 16 souborech**, `exit 0`, 4 poznámky o nevolaných funkcích (`_save_state`, `_load_state`, `unequip`, `flash`) |
| `python _analyza\over-dokumenty.py` | kontrola čísel v `GDD`/`ADD`/`TDD` proti zdrojům | **97 OK / 0 FAIL / 0 NEMĚŘENO**, `exit 0` (okna: 160 znaků, oddíly 87) |
| čtení po řádcích | `docs/*.md` (**6 souborů**), `AGENTS.md`, `CONVENTIONS.md`, `assets/spec.json`, `.forge/roadmap.json`, `HANDOFF.md`, `ZASTAVENO.md` | citace v tabulkách jsou **řádek po řádku**, ne podle dojmu |
| Python `os.walk` / `json` / `splitlines()` | soubory, PNG, klíče JSON, počty řádků | např. `spec.json` 88 ř. / 5 496 B; `game.gd` 377 ř.; `registry.gd` 150 ř.; `tools/blender/sprites` 258 PNG; `baseline.json` 272 položek (16 + 256); `.forge` 13 souborů v rootu (22 rekurzivně) |
| `git log` / `git show --stat` | kdo co změnil a kdy (rozhoduje o autoritě) | `0a5ee2f` (9. 10.) změnil **jen `docs/GDD.md`**; `01a9649` změnil `export_presets.cfg`; `799481d` přidal `registry.gd`; `8fe57ce` přepsal čísla v `AGENTS.md`/`BRANY-HRY.md`/`GDD.md`/`TDD.md` |
| čtení mimo repo (jen ke čtení) | `forge-orchestra\tools\over-dokumentaci.py`, `over-skilly.py`, `.github\workflows\agent.yml` | brány orchestry **pinují** `docs/BRANY-HRY.md` (`over-dokumentaci.py:28`, `:197–211`, `:393–397`); agent orchestry dostane **jen `CONVENTIONS.md`** (`agent.yml:227`) |

**Nespouštěl jsem Godot** (hra je zastavená) — proto jsou čísla o testech brána
z **běhu zaznamenaného v `HANDOFF.md:168`** (`[test] 113 kontrol, 0 selhání`)
a z mého spuštění `check-wiring.py`; nikde netvrdím nic o dnešním běhu testů.

---

## 2. Souhrn

| Druh | Počet | Kde |
|---|---|---|
| **Rozporů** (dvě tvrzení si odporují) | **24** | §3 (tabulka) — z toho **23× `ROZHODNOUT`**, **1× `PONECHAT JAKO OTEVŘENÉ`** (`R20`) |
| **Duplicit** (totéž na dvou a více místech) | **8** | §4 + `REJSTRIK-NAVRH.md` §3 |
| **Driftů** (dokument zaostal za měřením) | **3** | §5 |
| **Neškodných, ale matoucích** | **5** | §6 |
| **Ověřeno a sedí** (nic se nemá měnit) | **10 skupin** | §7 |

**Tři nejdůležitější nálezy:**

1. **Plán je druhý (a rozporný) zdroj smluv** — `.forge/roadmap.json` je to jediné,
   co agent orchestry dostane jako text zadání (`agent.yml:227`), a jeho prompty
   u `world.nodes`, `ui.hud` a `sim.mining` **odporují `docs/TDD.md §3`** (`R10`–`R12`);
   `world.nodes` je přitom **granule, která se má vydat příští**.
2. **Dvě pravidla v `CONVENTIONS.md` – tedy v jediném souboru, který agent dostane –
   popírají dnešní stav**: §2 tvrdí „Godot sám nemáš“ (`R13`), §3 zakazuje
   přidávat soubory vedle `game.gd` (`R14`) — což je přesně to, co má `M0` rozebrat.
3. **Tvrzení skillu `game-developer` o chybějících vrstvách 1/2/5 je vyvrácené**
   (jsou v `GDD`, s řádky — viz `REJSTRIK-NAVRH.md` §1) a **vzorový „rozpor 57 vs 97
   funkcí“ ze `ZASTAVENO:70` rozpor není** — jsou to dvě datovaná měření (`N1`).

---

## 3. Rozpory (tabulka)

**Legenda k „co je pravda“:** `[K]` = naměřeno v kódu, `[S]` = v `assets/spec.json`,
`[R]` = v `.forge/roadmap.json`, `[G]` = v gitu (kdo co změnil a kdy),
`[H]` = historické číslo, ve svém čase správné.

| # | Rozpor (co proti čemu) | Místo A (soubor:řádek + citace) | Místo B (soubor:řádek + citace) | Co je pravda (změřeno) | Návrh řešení | Doporučení |
|---|---|---|---|---|---|---|
| **R1** | **`assist` je/není non-goal `N9`** | `docs/TDD.md:481–482`: „`assist` je **non-goal `N9`** pro MVP — smlouva zůstává, ale nic na ní v MVP nestaví“ | `docs/GDD.md:432–446`: „⚠ `N9` PŘEFORMULOVÁNO 2026-10-09 … Nově je dovolené, aby hra **provedla, co hráč rozhodl** … `scripts/assist.gd` … **nejsou v rozporu s designem**“ | `[G]` `0a5ee2f` (9. 10. 2026) změnil **jen `GDD.md`** (+19 řádků), `TDD.md` ne — platí **GDD** (zdroj pravdy o designu, `AGENTS.md:101–102`) + rozhodnutí `game-clone\ROZHODNUTI-2026-10-09-SMER.md` §2 D3 (cituje `GDD:448–449`) | v `TDD §3.15` nahradit status (hotové znění v §8.1); `N9` v `TDD` neopakovat, jen odkázat | **ROZHODNOUT** |
| **R2** | **`world.map` je/není v plánu a co `world.gd` blokuje** | `docs/TDD.md:302–303`: „Vlastní ho **dvě** granule (`world.map`, `world.nodes`), obě nehotové“ (též `TDD:775`); `docs/GDD.md:489`: „`scripts/world.gd` = **0 B** — blokuje `world.map` i `engine.shell`“ | `docs/TDD.md:45–46`: „byla blokovaná mrtvou granulí `world.map` … **ta je z plánu vyřazená**“ + `.forge/roadmap.json` `_popis`: „VYŘAZENO 8. 10. 2026 (3 granule): `world.map` …“ | `[R]` v roadmapě **`world.map` není** (21 id); `world.gd` vlastní **`world.nodes`** (`done:false`); `engine.shell.depends_on = ["engine.registry"]` → `world.gd` **neblokuje `engine.shell`**; blokuje `sim.mining` a `persist.save.state` (jejich `depends_on` obsahuje `world.nodes`) | `TDD §3.5` a `§10 vada 4`: „vlastní ji granule **`world.nodes`**; `world.map` byla 8. 10. vyřazena“; `GDD:489`: „blokuje `world.nodes` (a přes ni `sim.mining` a `persist.save.state` z `M2`)“ | **ROZHODNOUT** |
| **R3** | **Kolik je v `scripts/` souborů** | `docs/TDD.md:779`: „`scripts/` má 15 souborů; žádný z nich se tak nejmenuje“ | `docs/TDD.md:522–524`: „**registr existuje** (`scripts/registry.gd`, 150 řádků, hotový ručně 8. 10. 2026…)“ | `[K]` **16 souborů `.gd`** (registry.gd 150 ř. — naměřeno), `ZASTAVENO.md:35` uvádí 16; 15 platilo **před** `799481d` → `[H]` | v `TDD:779` „15“ → „16 (před `M0` bylo 15 — ve svém čase správné)“ | **ROZHODNOUT** |
| **R4** | **Brána `check-licence.py` existuje/neexistuje** | `docs/BRANY-HRY.md:98–101`: „…nemají žádný offline test (na rozdíl od `check-schema.py`, `vision.mjs`, `baseline.py` a **`check-licence.py`**)“ | `docs/ADD.md:348`: „**Zmíněná brána `check-licence.py` neexistuje** | `docs/BRANY-HRY.md` ji zmiňuje; v `.forge/` **není**“ | `[K]` v `.forge/` **žádný `check-licence.py` není** (13 souborů v rootu, 22 rekurzivně) → platí `ADD` | v `BRANY-HRY:100` vypustit `check-licence.py` ze seznamu a nahradit větou „kontrola licence **neexistuje** (viz `ADD §11` řádek 6)“; naopak `ADD §11` řádek 6 je pak vyřešený | **ROZHODNOUT** |
| **R5** | **Barvy se mapují/neMapují na paletu** | `assets/spec.json:26`: „Barvy se mapuji na paletu hry (ne kvantizace na 16 nahodnych barev).“ | `assets/spec.json:79–82`: „`paleta` … **ZRUŠENO pro tuhle hru** … `zdroj: null`“; `assets/spec.json:76`: „plné barvy (stovky až tisíce), žádná kvantizace na paletu“ | `[S]` rozhodnutí je `zdroj: null` (8. 10. 2026) a `styl.barvy`; `_popis` je **starší popis plánu** (popisuje i „celočíselný dělitel 8“, viz `R6`); `ADD:44` a `ADD:47–50` berou zrušení palety za platné | v `spec.json` `_popis` přepsat větu na „Barvy zůstávají přirozené z renderu (paleta ZRUŠENA — viz `paleta`)“ — nebo klíč přejmenovat na `_popis_historie` | **ROZHODNOUT** |
| **R6** | **Zmenšování: celočíselný dělitel 8 vs. Lanczos** | `assets/spec.json:24–25`: „Sprity se generuji velke (768 px) a zmensuji **celociselnym delitelem 8** … zadne mixels, zadne zvetsovani.“ | `assets/spec.json:75`: „zmenšování: **Lanczos/bilineární (hladké)**, NE celočíselný nearest“; `docs/ADD.md:49–50` a `docs/ADD.md:216`: „zmenší **Lanczosem** na výšku přesně 96 px“ | `[K]` pipeline opravdu zmenšuje Lanczosem přes `union_bbox` ze 128 obrázků (`ADD:216`, `postprocess.py`); celočíselný dělitel 8 je **starý plán** | v `spec.json` `_popis` vypustit větu o děliteli 8 a odkázat na `styl.zmenšování` | **ROZHODNOUT** |
| **R7** | **Renderuje se v 5, nebo ve 4 směrech** | `assets/spec.json:74`: „…(Blender headless, zdarma) **v 5 směrech**“ | `assets/spec.json:31–33`: `role.*.smery = 4`; `assets/spec.json:4`: „izo kamera 45°, **4 směry**“; `ADD:343` (řádek 1 měřených rozporů) | `[S]`+`[K]` 4 směry (pipeline `range(4)`); `5 směrů` je zbytek staršího textu | v `spec.json:74` „v 5 směrech“ → „ve 4 směrech“; v `ADD §11` řádek 1 přepsat na „vyřešeno v `spec.json` (datum)“ — **řádek nemazat** (je to záznam) | **ROZHODNOUT** |
| **R8** | **`_stav` v `spec.json` odkazuje na soubory, které nejsou** | `assets/spec.json:16`: „Náhled herního okna: `tools/gamewindow_preview.py` → `_gamewindow_preview.png` (960×540)“; `assets/spec.json:11`: „zdroj `assets/sprites/items/sword.png`“ | `docs/ADD.md:346` (řádek 4 měřených rozporů): „**`spec.json` odkazuje na soubory, které neexistují** … `soubor není`“ | `[K]` `tools/gamewindow_preview.py` **je**, `tools/_gamewindow_preview.png` **není**; `assets/sprites/items/sword_final.png` **je**, `sword.png` **není** → platí `ADD` | `spec.json` `_stav` je **historie** → přejmenovat na `_stav_historie` (nebo do něj přidat „(stav k 8. 10. 2026, historie)“) | **ROZHODNOUT** |
| **R9** | **Kdo vlastní tik, registr a fronty** | `docs/TDD.md:646`: „tik, registr, fronty příkazů a událostí, seed \| **`game.gd`** (kostra) … \| **dnes neexistuje jako kostra**“ | `docs/TDD.md:522–527`: „**registr existuje** (`scripts/registry.gd`, 150 řádků … `component(id)`, `advance()`/`step()` s pevným tikem 50 ms, fronty příkazů a událostí)“ | `[K]` tik a fronty **skutečně vlastní `registry.gd`**: `:26 const TICK_MS := 50`, `:91 advance()`, `:129 push_command()`, `:141 push_event()`; `TDD §2` (`:154–163`) `registry.gd` **v žádné vrstvě nejmenuje** | v `TDD §5` (`:646`) změnit vlastníka na **`registry.gd`** (kostra scény = `game.gd`); do `TDD §2` doplnit `scripts/registry.gd` do vrstvy `engine`; do `§3` přidat smlouvu **`Registry`** | **ROZHODNOUT** |
| **R10** | **Rozhraní v zadání granule: `attributes.get`/`skills.get`** | `.forge/roadmap.json:202` (prompt `ui.hud`): „Čte jen veřejné gettery (**attributes.get, skills.get**, economy.gold, player).“ | `CONVENTIONS.md:111–125`: „**ŠPATNĚ** – Parse Error: The method „get()“ overrides a method from native class „Object“ … **Nikdy nepoužívej jako název funkce:** `get`“; `TDD:225–227`, `TDD:243–244`: `hodnota(attr)`/`hodnota(skill)` | `[K]` `scripts/hud.gd:64–68` volá `_skills.hodnota(...)`; `attributes.gd`/`skills.gd` mají `hodnota()`; **`get()` v GDScriptu 4 nejde** — a `roadmap.json:26` sám tvrdí „PROMPT SE GENERUJE ZE SMLOUVY v `docs/TDD.md §3`“ | přepsat prompt `ui.hud` na `Skills.hodnota("tezba")`, `Attributes.hodnota("Str")`, `Economy.gold(player)` (hotové znění §8.2) | **ROZHODNOUT** |
| **R11** | **Smlouva `World`: `bool`/`Array` (plán) vs. `Dictionary` (TDD)** | `.forge/roadmap.json:226` (prompt `world.nodes`): „(1) `gather(cell: Vector2i) -> bool` — … vrátí true … (5) `snapshot() -> Array` a `restore(stav: Array) -> void` … KAŽDÝ uzel … `resource_id: String, difficulty: int, cell: Vector2i`“ | `docs/TDD.md:280–294`: „`gather(cell) -> Dictionary` (co zdroj vydal)“; tvar: `{ok, common: {id, amount}, rare: {id, amount}\|null}` — **směs**; `snapshot()` = `Dictionary` (uzly **i** stav světa); uzly `{cell, kind, rich, respawn_at}` | `[K]` `save.gd:71–74` ukládá, co `snapshot()` vrátí, a `:133–137` to vrací do `restore()`; `GDD:107–108` (pravidlo `A`: směs) a `GDD:173` (`V4`) vyžadují **vzácnou složku**, `GDD:282–287` vyžaduje stav světa (infestace/zásobenost) → **`bool` ani `Array` to neunesou**, platí `TDD §3.5`; i `NAVRH-ROADMAPY-M0-M6.md:120` plánuje pro `M2` „směs …, `snapshot()`/`restore()`“ | přepsat prompt `world.nodes` **ze smlouvy `TDD §3.5`** (hotové znění §8.3) — je to **nejbližší granule k vydání** | **ROZHODNOUT** |
| **R12** | **`Mining.gather` vrací `int`, nebo `Dictionary`** | `docs/TDD.md:386–391`: „**poskytuje:** `gather(node) -> Dictionary` … tvar se shoduje s `World.gather()` … `{ok, common, rare, skill_gain}`“ | `.forge/roadmap.json:130` (prompt `sim.mining`): „vytvoř `gather(node) -> int` … **Vrať počet vytěžených kusů**“; `[K]` `scripts/mining.gd:17`: `func gather(node: Node) -> int:` | `[K]` kód i plán říkají `int`; `GDD:173` (`V4`: „dva různě dlouhé zásahy dají **jiný obsah**“) potřebuje směs → cíl je `TDD` | v `TDD §3.10` status upravit: „dnes vrací `int` (naměřeno `mining.gd:17`); cílový tvar je `Dictionary` podle `World`“ + prompt `sim.mining` přepsat při otevření `M2` | **ROZHODNOUT** |
| **R13** | **Agent „sám Godot nemá“ vs. jak si Godot spustit** | `CONVENTIONS.md:225–227`: „…**spustit si je musí CI** – **ty sám Godot nemáš**.“ | `AGENTS.md:40–49`: „## Jak spustit hru a testy … `$godot = 'E:\Tools\godot\Godot_v4.7.2-stable_win64_console.exe'`; `& $godot --headless --path . --script res://tests/run_tests.gd`“ | `[K]` Godot **existuje** (`Test-Path` = `True`); `AGENTS.md` je novější (vznikl 4. 10. 2026, `AGENTS.md:6`) → `CONVENTIONS §2` je zastaralé a **popírá vlastní nástroj** (to je dražší než chybějící informace) | `CONVENTIONS §2` přepsat: „Testy běží v CI; lokálně je spustíš, pokud máš Godot — cesta a příkaz jsou v `AGENTS.md` §Jak spustit hru a testy.“ | **ROZHODNOUT** |
| **R14** | **Nové soubory se nemají přidávat / mají (monolit vs. registr)** | `CONVENTIONS.md:229–237`: „## 3. Hra je postavená programově — Celá scéna se staví v `scripts/game.gd` … **nepřidávej nové soubory, když to jde udělat v `scripts/game.gd`**“ | `docs/GDD.md:460` (`M0`): „**přepis `game.gd` (monolit) na registr** (`engine.shell`), pevný tik“; `TDD:43–52`: „**Cena `R-1`** … znamená to **přepsat monolit** `scripts/game.gd`“ | `[K]`+`[G]` monolit se právě rozebírá: `799481d` přidal `registry.gd` (150 ř.), `8fe57ce` přepsal čísla; směr je **monolit → komponenty**, tedy opak `CONVENTIONS §3` | `CONVENTIONS §3` přepsat: „scéna se staví programově (beze změny); **nová komponenta = nový soubor v `scripts/`** registrovaný přes `component(id)` (`TDD §1.1`); do `game.gd` patří jen sestavení scény a tik.“ | **ROZHODNOUT** |
| **R15** | **Vlastnost `Level` se jmenuje `cell`, nebo `cell_w`/`cell_h`** | `CONVENTIONS.md:249`: „`spawn_cell -> Vector2i`, `width`, `height`, **`cell`** \| rozměry mřížky“ | `docs/TDD.md:265–266`: „vlastnosti `grid`, `width`, `height`, **`cell_w`, `cell_h`**, `offset` …“ | `[K]` `scripts/level.gd:44–45`: `var cell_w := CELL_W_DEFAULT`, `var cell_h := CELL_H_DEFAULT` — **`cell` na `Level` neexistuje** (je jen v `main.json` a ignoruje se, `TDD:588–592`) | v `CONVENTIONS §4` v tabulce `cell` → `cell_w`, `cell_h` | **ROZHODNOUT** |
| **R16** | **Čísla z běhu se do dokumentu neopisují / opisují** | `CONVENTIONS.md:278–281`: „**Počet kontrol se ČTE z výstupu běhu** … — **do dokumentu se neopisuje**, protože zestará: naměřeno 3. 10. 2026 jich bylo **91**“ | `AGENTS.md:85–86`: „staticky je tam **154** volání `_check(`, běh hlásí **113** kontrol“; `TDD:742` totéž; `BRANY-HRY.md:90–94` totéž | `[K]` obě čísla **sedí** (155 výskytů `_check(` = 154 volání + 1 definice; běh 113; `has_method` 28/41, bez komentářů 20/33) → pravidlo a praxe si odporují, ne čísla | v `CONVENTIONS §7` nahradit zákaz: „**opisovat jen s datem a se zdrojem** (odkud bylo číslo přečteno); bez toho zestará“ | **ROZHODNOUT** |
| **R17** | **Vydavatel a copyright ve exportu** | `docs/GDD.md:524` (`O-3`): „`company_name` v `export_presets.cfg` **zůstává `GameForge`**“; `docs/ADD.md:349`: „má `product_name` = `uo-shadows` a **`copyright` prázdné**; **`company_name` zůstává `GameForge`**“; `docs/ADD.md:357`: „`export_presets.cfg` má `copyright` **prázdné**“ | `export_presets.cfg:43`: `application/company_name="ssevcikm-spec"`; `:46`: `application/copyright="© 2026 ssevcikm-spec"` | `[K]`+`[G]` soubor je **novější** (commit `01a9649` „export: vydavatel a copyright hry (rozhodnuti uzivatele)“) než dokumenty z 8. 10. → platí soubor; tvrzení „copyright je prázdné“ je dnes **nepravdivé** | `GDD:524` a `ADD:349`, `ADD:357` uvést na pravou míru („změněno 8. 10. 2026 rozhodnutím uživatele: `company_name` = `ssevcikm-spec`, `copyright` = „© 2026 ssevcikm-spec““) a ponechat poznámku, co platilo dřív | **ROZHODNOUT** |
| **R18** | **„Plán vzniká z milníků `M0`–`M6`“ vs. roadmapa bez milníků** | `docs/GDD.md:502`: „**Plán granulí a pořadí práce** → `.forge/roadmap.json` (**vzniká z §12**)“; `.forge/roadmap.json` `_popis:1`: „plán podle milníků M0-M6 z `docs/GDD.md §12`“; `ZADANI-GDD-ADD-TDD.md:133–134`: „návrh nové `.forge/roadmap.json` (milníky `M0`–`M6`)“ | `[R]` **změřeno:** 21 granul, klíče granul jsou `acceptance, depends_on, done, done_note, id, kind, model, owns, prompt, size_lines, title` — **klíč `milestone` není ani u jedné**; a **žádná granule pro `M2`–`M6`** (chybí `orders.gd`, `standing.gd`, `layers.gd`, `anim.gd`, `npc.gd`, `enemy.gd`) | `[R]` plán dnes pokrývá **`M0`+`M1`** + staré granule; tabulky `M2`–`M6` jsou jen v `_analyza/NAVRH-ROADMAPY-M0-M6.md:115–160` (záznam) | buď doplnit `"milestone"` ke granulím (mechanické), nebo `GDD:502` a `_popis` upravit na „plán obsahuje otevřené milníky `M0`–`M1`; `M2`–`M6` se doplní při otevření milníku (`NAVRH-ROADMAPY §4`)“ — a **nezakládat `M2`–`M6` dopředu** | **ROZHODNOUT** |
| **R19** | **`ARCHITEKTURA.md` je „jediný závazný“ / „není zdroj pravdy“** | `docs/ARCHITEKTURA.md:11–13`: „**Autoritativní zdroj pravdy** pro rozpad na granule. … tenhle soubor je **jediný závazný**. … agenti čtou ji.“ (+ `:137–138` žádá `get(attr)`, `get(skill)`) | `docs/ARCHITEKTURA.md:3–9`: „⚠ **NAHRAZENO `docs/TDD.md`** … **není zdroj pravdy** o technice a needituje se“; `AGENTS.md:163`: „`docs/ARCHITEKTURA.md` \| **historie** … nahrazeno `docs/TDD.md`“ | `[G]` hlavička je novější (8. 10. 2026), tělo je původní — v jednom souboru jsou **dvě vzájemně se vylučující tvrzení o autoritě**; a `get(...)` je rozhraní, které Godot 4 **neumí** (`CONVENTIONS:111–125`) | **nic nepřepisovat** (je to záznam) — jen **doplnit** k řádkům 11–15 a 137–138 jednu označovací větu „(původní znění — od 8. 10. 2026 nahrazeno `docs/TDD.md`, neplatí)“ | **ROZHODNOUT** (doplněním, ne přepisem) |
| **R20** | **`DESIGN.md` posílá na `ARCHITEKTURA.md` jako na závaznou** | `docs/DESIGN.md:11–15`: „**Zrušeno jako zdroj pravdy.** Závazná architektura a rozpad na granule je v `docs/ARCHITEKTURA.md` …“ | `docs/DESIGN.md:7–9`: „Odkazy níž na `docs/ARCHITEKTURA.md` a `.forge/roadmap.json` **platily ve svém čase** — `ARCHITEKTURA.md` je taky nahrazený (`docs/TDD.md`)“; `AGENTS.md:161` | `[K]` obě věty jsou **v jednom viditelném bloku** (`:3–9` hned nad `:11–15`) → čtenář narazí na opravu dřív než na tvrzení; **naměřená škoda: žádná** | ponechat; případně při nejbližší editaci sjednotit slovem „historicky“ | **PONECHAT JAKO OTEVŘENÉ** (agent orchestry tenhle soubor nedostane — `agent.yml:227` — a hlavička ho usadí) |
| **R21** | **Nearest filtr: zakázaný vs. zapnutý** | `assets/spec.json:71–72`: „Zakázané: 16barevná paleta, dithering, **nearest-neighbour zmenšování** …“; `:75`: „NE celočíselný nearest“ | `project.godot:30`: `textures/canvas_textures/default_texture_filter=0` s komentářem „; 0 = Nearest – u pixel-artu žádoucí“; `docs/ADD.md:344` (řádek 2 měřených rozporů) to popisuje | `[K]` **dvě různé věci**: zvětšení viewportu 2× (`project.godot:23 window/stretch/mode="viewport"`) je celočíselné → Nearest je zamýšlený; dlaždice se ale škálují `cell_w / šířka_textury` (`level.gd`), což celočíselné není → **spec zakazuje právě ten druhý případ** | `ADD §11` řádek 2 přepsat na ROZHODNUTÍ: „Nearest je zamýšlený pro celočíselné 2× zvětšení viewportu; pro dlaždice platí zákaz — a **filtr se doplní do `spec.json` jako deklarace** (`filtr`), aby ho šlo měřit“ | **ROZHODNOUT** |
| **R22** | **„Sedm rozporů“ a vzorový „rozpor 57 vs 97 funkcí“** | `ZASTAVENO.md:68–70`: „**Sedm rozporů v dokumentech** (např. … **dvě různá čísla téže brány: 57 vs 97 funkcí**)“ | `[K]` **změřeno:** `check-wiring.py` dnes hlásí **97 funkcí v 16 souborech**; `57 v 7 souborech` je v `BRANY-HRY.md:87` (stav před `M0`) | `[K]`+`[H]` **rozpor to není** — jsou to **dvě datovaná měření téhož nástroje**; `BRANY-HRY.md:8–9` sám říká „čísla jsou **stav v čase měření**“. A „sedm“ je **číslo bez seznamu** (u zbytku není dohledatelné) | do `ZASTAVENO §6` **doplnit** (ne přepsat) větu: „Úplný seznam rozporů k 15. 10. 2026 je v `_analyza/PRACE-2026-10-15/ROZPORY.md` (24); ‚57 vs 97‘ jsou dvě datovaná měření, ne rozpor.“ | **ROZHODNOUT** |
| **R23** | **Pravidlo jazyka bez výjimky pro existující české klíče** | `AGENTS.md:123–127`: „identifikátory, klíče a literály rozhraní ASCII … platí i pro `assets/data/*.json`: `id` anglicky (`iron_sword`) …“ | `docs/GDD.md:517` (`O-5`): „stávající české klíče se **nepřejmenovávají mimochodem** (rozbité by byly testy, roadmapa i uložené pozice)“; `TDD:719–723`: totéž + „je to **samostatný úkol**“ | `[K]` v datech **jsou** české klíče (`skills.json`: `tezba`, `drevorubectvi`, `kovarstvi`, `boj_na_blizko`; `recipes.json`: `kovani_mece`, `kovani_zbroje`) | do `AGENTS.md` §Jazyk přidat jednu větu: „**Výjimka (O-5):** existující české klíče v `assets/data/*.json` se nepřejmenovávají mimochodem — přejmenování je samostatný úkol (`GDD §14.1 O-5`).“ | **ROZHODNOUT** |
| **R24** | **ADD „neopisuje čísla“ vs. ADD §1 je vypisuje** | `docs/ADD.md:384–385`: „**Konkrétní rozměry, role, vrstvy a tolerance** → `assets/spec.json` (**ADD je neopisuje jako druhý zdroj**; vysvětluje je)“; `docs/ADD.md:8–10`: „kde si odporují, platí `spec.json` pro čísla a ADD pro **důvod**“ | `docs/ADD.md:32–45`: tabulka s `960×540`, `96×48`, 8 rolemi (rozměry, směry, framy), 8 sloty a **6 tolerancemi bran**; `docs/ADD.md:318–324` je vypisuje znovu | `[S]` duplicita je reálná — a už jednou **vyrobila rozpor** (`R7`: ADD má 4 směry správně, `spec.json` `styl` říká 5) | do `ADD §1` přidat jednu větu nad tabulku: „**Opis deklarace k 8. 10. 2026** — závazná čísla jsou v `assets/spec.json`; když se rozejdou, platí `spec.json`.“ | **ROZHODNOUT** |

---

## 4. Duplicity (totéž na dvou a více místech)

Podrobně (včetně ceny sjednocení) v **`REJSTRIK-NAVRH.md` §3** — tady jen seznam,
protože duplicita je **živný zdroj rozporů** (dvě z nich `R4` a `R16` už nastaly):

| # | Téma | Místa | Už se rozešlo? |
|---|---|---|---|
| D1 | Co která brána měří | `AGENTS.md:65–71`, `BRANY-HRY.md:30–37`+`:68–101`, `TDD:734–742`, `ADD:318–324` | **ano** (`R4`, `N1`, `DR1`) |
| D2 | Počty testů / `has_method` | `AGENTS.md:80–86`, `BRANY-HRY.md:88–97`, `TDD:742` | ne (všechna tři sedí s měřením) |
| D3 | Definice hotovo (4 podmínky) | `GDD:470–474`, `TDD:22–23`, `.forge/roadmap.json` `_popis` | ne (formulace shodná) |
| D4 | Milníky `M0`–`M6` | `GDD:453–468`, `ADD:114–116`, `NAVRH-ROADMAPY-M0-M6.md:100–160`, roadmapa `_popis` | **ano** (`R18`) |
| D5 | Čísla vzhledu | `assets/spec.json`, `ADD:32–45`, `ADD:318–324`, `BRANY-HRY:33` | **ano** (`R7`, `R21`, `R24`) |
| D6 | Pravidlo jazyka `R-3` | `AGENTS.md:121–127`, `TDD:697–723`, `CONVENTIONS.md:269–274`, `GDD:517` | **skoro** (`R23`) |
| D7 | 18 smluv | `TDD:183–537` vs `ARCHITEKTURA.md:134–153` (historie) | ne — historie je označená (`R19`) |
| D8 | „Co hra je“ jednou větou | `GDD:34–38`, `AGENTS.md:101–102`, `DESIGN.md:33–44` | ne — `DESIGN.md` je označená historie |

---

## 5. Drift (dokument zaostal za měřením — není to rozpor dvou dokumentů)

| # | Kde | Co tvrdí | Naměřeno | Návrh |
|---|---|---|---|---|
| **DR1** | `docs/BRANY-HRY.md:139` | „`.forge\check-schema.py` … **461** řádků“ (naměřeno 1. 10. 2026) | **468 řádků**; obě kopie (hra i šablona) mají **shodný SHA256** `531AE8…` — tvrzení „shodný hash“ tedy platí | ponechat (je to datované měření); při nejbližší editaci číslo aktualizovat |
| **DR2** | `ZASTAVENO.md:38` | „Dokumenty: **16 `.md` / 58 081 slov**“ | **17 `.md`** (bez souborů této session) — číslo **nemá uvedený postup** (co se počítá), proto ho nelze reprodukovat | ponechat (záznam je datovaný „v den zastavení“); **nová čísla vždy s postupem** |
| **DR3** | `docs/ADD.md:348` | „v `.forge/` **není** (14 souborů, měřeno)“ | **13 souborů** v rootu `.forge/` (**22** rekurzivně) — platí pointa (žádný `check-licence.py`), číslo je bez rozsahu | ve `R4` opravit formulaci na „`.forge/` má 13 souborů v rootu (22 rekurzivně) a žádný `check-licence.py`“ |

---

## 6. Neškodné, ale matoucí (nezamlčet, ale neopravovat jako vadu)

| # | Co vypadá jako vada | Co naměřeno | Doporučení |
|---|---|---|---|
| **N1** | `ZASTAVENO:70` „dvě různá čísla téže brány: 57 vs 97 funkcí“ | `BRANY-HRY:87` (57/7 souborů, před `M0`) vs. **naměřeno 97/16** — **dvě datovaná měření**, ne rozpor; `BRANY-HRY:8–9` to sám přiznává | **PONECHAT** (případně u `57` doplnit datum „1. 10. 2026“) — je to učebnicový příklad „různé čítače nesou stejné jméno“ |
| **N2** | `ADD:274–275`: slovo „Zvuk“ je „**jediný výskyt v celém `docs/`**“ | naměřeno **3×**: `DESIGN.md:60`, `ADD.md:266` (vlastní nadpis oddílu) a `ADD.md:275` (sám výrok) — počítadlo **počítá i sebe** | **PONECHAT**; věcně platí, že jediné místo, které o zvuku něco **rozhoduje**, je `DESIGN.md:52–53` |
| **N3** | `sprites.json` v rootu: `colors: 16/12`, `size: 64` — druhý zdroj o rozměrech a paletě | `[K]` 17 řádků, 5 spritů; **žádný skript ho nečte** (výskyt jen v `docs/ADD.md`) | **PONECHAT** (dokud ho `ADD §11` řádek 3 vede jako legacy manifest) — agent orchestry ho nedostane |
| **N4** | `BRANY-HRY:36` a `ADD:324`: „co je vizuálně **SCHVÁLENÉ (LGTM)**“ | `[K]` `.forge/vision/baseline.json`: `_ceka_na_lgtm: true`, `_stav` = „PŘEVZATO **AGENTEM** 30. 9. 2026 – **čeká na lidskou kontrolu**“; 272 položek = 16 (`assets/sprites`) + 256 (`tools/blender/sprites`) | **PONECHAT** + při editaci jedno slovo: „schválené **agentem** (čeká na lidské LGTM)“ — dnes to zní, jako by schválil člověk |
| **N5** | `.forge/roadmap.json`: `acceptance` má jen **3 kombinace** (`["tests","wiring"]`, `["tests","render"]`, `["tests","wiring","render"]`) a `provides`/`consumes` **0 z 21** | `[R]` naměřeno; `NAVRH-ROADMAPY-M0-M6.md:212–213` to vede jako nedodělek | **PONECHAT jako otevřené** (`NAVRH-ROADMAPY §5.3`) — není to rozpor, dokud smlouvu nese `TDD §3` |

---

## 7. Co jsem ověřil a sedí (neměnit, jen vědět)

Aby se při přepisu „neopravovalo“ to, co je správně:

1. **Brány:** tvrdá je jen `check-schema.py`; `check-wiring` dnes **97 funkcí / 16 souborů**, `exit 0`; `over-dokumenty.py` **97 OK / 0 FAIL / 0 NEMĚŘENO**, `exit 0`.
2. **Čísla `TDD`:** `game.gd` **377** ř., `registry.gd` **150** ř., `run_tests.gd` **1569** ř., `_check(` **155 výskytů = 154 volání + 1 definice**, `has_method` **28 řádků / 41 výskytů** (bez komentářů **20/33**), `ci.yml` **181** ř. a jeho pořadí kroků — **vše sedí**.
3. **Čísla `ADD`:** `spec.json` **88 ř. / 5 496 B**; `assets/` **57 souborů / 24 PNG**; `tools/blender/sprites` **258 PNG** (130 + 128 v `npc/`); `tools/*.txt` **6** promptů a **žádný skript je nečte**; `baseline.json` **272** položek; `assets/audio/` a `assets/ui/` **neexistují**; font v repu **0**.
4. **Dvě kopie brány:** `.forge/check-schema.py` hra vs. šablona — **shodný SHA256**; `vision.test.mjs` hra **13 318 B** vs. šablona **17 576 B** → tvrzení `BRANY-HRY:37` (36/36 vs 28/28) **platí**.
5. **Tvrzení `GDD` o dnešním stavu:** na obrazovce je `Label` se skóre a nápověda **6 kláves** (`game.gd:54`, `:221`), `KEY_`/`Input.` je jen v `player.gd:74–80` (WASD/šipky) → **inzerovaných 6 kláves kód neobsluhuje** ✔; `project.godot` **nemá `[input]` akce** ✔; `scripts/world.gd` **0 B** ✔; `hud.gd` se v produkční cestě **neinstancuje** ✔.
6. **Milníky `M0`–`M6`** v `GDD:458–466` jsou **shodné** s rozhodnutím `DESIGN-REVIZE-2.md:947–955` (a `GDD:455` cituje `P1` „Sedí M0–M6“).
7. **Non-goals `N1`–`N11`** (`GDD:411–423`) odpovídají `DESIGN-REVIZE-2.md` §12.3 + §12.7 (`N11` doplněno `R2-3`).
8. **`V1`–`V8`** (`GDD:168–177`) mají důkaz i „kdy to musí platit“ — a `GDD:179–181` říká, kdo je vyhodnotí.
9. **České klíče v datech** (`tezba`, `kovani_mece`) jsou **skutečně v datech** a `TDD §8` i `GDD O-5` je **správně** označují za samostatný úkol.
10. **Dokumenty neobsahují placeholdery** `TODO/TBD/XXX/FIXME` (prohledáno `*.md`; slovo „placeholder“ je jen ve významu grafických primitiv) — `ZADANI-GDD-ADD-TDD.md:140` to nařizuje a **je to splněné**.

---

## 8. Hotové znění pro nejdůležitější opravy

*(Aby se dalo rovnou psát. Nic z toho jsem neprovedl.)*

### 8.1 `R1` — `docs/TDD.md:481–482`, status smlouvy `Assist`

**Vypustit:** „`assist` je **non-goal `N9`** pro MVP — smlouva zůstává, ale nic na ní v MVP nestaví“
**Nahradit:** „`assist` je v MVP **přípustný** ve smyslu `N9` po přeformulování z 9. 10. 2026 (`docs/GDD.md:432–449`): **rozhoduje hráč, hra provádí** (i offline doběh a i podle pravidel s podmínkami). Zakázané zůstává, aby hra rozhodovala za hráče. Smlouva platí; kdo `assist` zapojí, musí v kódu napsat, které rozhodnutí je hráčovo.“

### 8.2 `R10` — `.forge/roadmap.json:202`, prompt granule `ui.hud`

**Nahradit větu** „Čte jen veřejné gettery (attributes.get, skills.get, economy.gold, player)“ **za:**
„Čte jen to, co komponenty **skutečně poskytují**: `Skills.hodnota("tezba")`, `Attributes.hodnota("Str")`, `Economy.gold(player)` a stav hráče (`hp`, `inventory`, `equipped`) — `get()` v GDScriptu **nesmíš použít** (koliduje s `Object.get()`, `CONVENTIONS.md §1f`).“

### 8.3 `R11` — `.forge/roadmap.json:226`, prompt granule `world.nodes` (nejbližší k vydání)

**Nahradit smlouvu** v promptu **smlouvou z `docs/TDD.md §3.5`:**
```
SMLOUVA (docs/TDD.md §3.5) — přesně tohle volají jiné komponenty:
(1) nodes -> Array[Dictionary]; každý uzel {cell: Vector2i, kind: "ore"|"tree"|"rock"|"field",
    rich: float, respawn_at: float}
(2) gather(cell: Vector2i) -> Dictionary  {ok: bool,
    common: {id: String, amount: int},
    rare: {id: String, amount: int} | null}     ← SMĚS (GDD §2 pravidlo A); delší těžba = víc vzácného
(3) is_walkable(pos: Vector2) -> bool
(4) infestation: float, supply: float (0–100)   ← stav světa (GDD §8.1), ceny z nich počítá Economy
(5) snapshot() -> Dictionary  a  restore(data: Dictionary) -> void
    ← MUSÍ unést uzly I stav světa (save.gd:71–74 to ukládá a :133–137 vrací)
```
**A doplnit acceptance:** „dva různě dlouhé zásahy do téhož uzlu dají jiný obsah (`V4`); `snapshot()` → `restore()` vrátí totéž `infestation`/`supply`“.

### 8.4 `R13` — `CONVENTIONS.md:223–227`, §2

**Vypustit:** „…ale **spustit si je musí CI** – **ty sám Godot nemáš**.“
**Nahradit:** „…ale spustit si je musí CI. **Lokálně je spustit můžeš**, pokud máš Godot — přesná cesta a příkaz jsou v `AGENTS.md` §Jak spustit hru a testy. Výsledek se čte z výstupu („`[test] N kontrol, M selhání`“), ne z exit kódu.“

### 8.5 `R14` — `CONVENTIONS.md:236–237`, §3 (poslední odrážka)

**Vypustit:** „**nepřidávej nové soubory, když to jde udělat v `scripts/game.gd`**“
**Nahradit:** „**nová komponenta = nový soubor v `scripts/`**, zaregistrovaný přes `component(id)` (`docs/TDD.md §1.1`); do `scripts/game.gd` patří jen sestavení scény a tik. `game.gd` je dnes **monolit**, který `M0` rozebírá (`docs/GDD.md:460`) — neposiluj ho.“

### 8.6 `R15` — `CONVENTIONS.md:249`, §4

`cell` → **`cell_w`, `cell_h`** (a případně doplnit „projekci nese `level.gd`, `world.gd` ji nesmí opisovat“).

### 8.7 `R9` — `docs/TDD.md:646` (§5) a `docs/TDD.md:154–163` (§2)

- `:646` — vlastník „tik, registr, fronty příkazů a událostí, seed“: **`registry.gd`** (kostra scény = `game.gd`); poznámka „dnes neexistuje jako kostra“ se mění na „**registr hotový 8. 10. 2026** (`scripts/registry.gd`, 150 ř.); `game.gd` ho zatím nevolá“.
- `:156` — do vrstvy `engine` doplnit `scripts/registry.gd` a do `§3` **novou smlouvu `Registry`** (`component(id)`, `register(id, node)`, `components()`, `advance(delta)`, `step(dt)`, `push_command(cmd)`, `commands()`, `push_event(ev)`, `events()`, `TICK_MS = 50`).

### 8.8 `R17` — `docs/GDD.md:524` (konec `O-3`) a `docs/ADD.md:349`, `:357`

**Doplnit za stávající text:** „**Změněno 8. 10. 2026 rozhodnutím uživatele** (`01a9649`): `company_name = "ssevcikm-spec"`, `copyright = "© 2026 ssevcikm-spec"`. Text výš je **stav před touto změnou** (ve svém čase správný).“

### 8.9 `R2` — `docs/TDD.md:302–303`, `:775`, `docs/GDD.md:489`

- `TDD:302–303` → „Vlastní ho **granule `world.nodes`** (`.forge/roadmap.json`); `world.map` byla **8. 10. 2026 vyřazena z plánu**.“
- `TDD:775` → totéž.
- `GDD:489` → „Mrtvá granule \| `scripts/world.gd` = **0 B** — blokuje `world.nodes` a přes ni `sim.mining` a `persist.save.state` (milník `M2`)“.

### 8.10 `R18` — `docs/GDD.md:502` a `.forge/roadmap.json` `_popis:1`

Buď do každé granule doplnit `"milestone": "M0"|"M1"|…`, nebo text upravit na:
„Plán granulí a pořadí práce → `.forge/roadmap.json`. Dnes obsahuje **otevřené granule `M0`–`M1`** (+ granule s prací v `main`); granule pro `M2`–`M6` se doplňují **při otevření milníku** (`_analyza/NAVRH-ROADMAPY-M0-M6.md` §4) — ne dopředu naslepo.“

---

## 9. Co by z toho měla chytit brána nad dokumentací

*(Podklad pro `_analyza/over-dokumenty.py`, který dnes měří 97 čísel v `GDD`/`ADD`/`TDD`
a **žádný z 24 rozporů výš nechytí** — protože všechny jsou **mezi dokumenty**,
ne uvnitř jednoho.)*

1. **Cizí jméno API v plánu:** každý výskyt `X.get(`/`.get(` v `prompt`u granule
   musí být v `CONVENTIONS.md` zakázaný tvar → `FAIL` (`R10`).
2. **Smlouva v promptu vs. smlouva v `TDD §3`:** u granule, která má v `TDD`
   oddíl, musí `prompt` obsahovat **tytéž názvy metod a typy návratů** (`R11`, `R12`).
3. **Mrtvé odkazy:** každé jméno souboru zmíněné v dokumentu musí existovat
   (dnes: `world.map`, `check-licence.py`, `sword.png`, `_gamewindow_preview.png`) — `R2`, `R4`, `R8`.
4. **Zakázaný text v `prompt`u** proti `CONVENTIONS.md` (např. `get(`, `position =`, `class_name Item`) — `R10`.
5. **Tvary, které se nesmí rozejít:** `M0`–`M6` v `GDD §12` vs. `milestone` v plánu (`R18`);
   čísla v `ADD §1` vs. `spec.json` (`R7`, `R24`).
6. **Externí pin:** `docs/BRANY-HRY.md` je pinovaný 13 texty v orchestraci
   (`over-dokumentaci.py:197–211`, `:393–397`) — brána hry by měla vědět, že tenhle
   soubor **nejde přejmenovat ani vyprázdnit**.
7. **Třetí stav `exit 2` = NEMĚŘENO** pro nové kontroly (aby „nenašel jsem“ nebylo zelené).

---

## 10. Meze tohohle měření (co jsem nedělal)

- **Nespouštěl jsem Godot** ani `ci.yml` — proto neposuzuji běhové vady (`TDD §10` je
  bere jako známé a pojmenované; nic z nich jsem nepřeměřoval).
- **Nečetl jsem `_analyza/` do hloubky** (`AUDIT-PLANU-A-DESIGNU.md` 1 033 řádků,
  `DESIGN-REVIZE-2.md` 1 122 řádků) — četl jsem oddíly, které rozhodují o autoritě
  (§1, §8, §9, §12.2–12.7, §15.1–15.5, §16, §17).
- **Neposuzuji, které rozhodnutí je „správné“** tam, kde jde o vkus — u každého
  rozporu jen říkám, **který zdroj je autorita a proč** (kód, spec, `roadmap.json`,
  datované rozhodnutí).
- **Neopravil jsem ani jedno místo** — a to ani tam, kde by to bylo na jeden řádek
  (např. `TDD:779` „15“ → „16“). Zadání to zakazuje a oprava by znehodnotila
  tenhle záznam jako důkaz.
