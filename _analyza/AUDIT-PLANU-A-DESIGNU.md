# Audit: vývojový plán a game design UO-Shadows proti praxi harnessu

> **Co tenhle dokument JE:** **analýza** (audit) — odpověď na otázku „je plán a design
> této hry dobře formulovaný a organizovaný pro slabší AI modely, a co z toho plyne".
> Není to zadání, není to stav projektu a není to záznam o provedení.
>
> **Zadavatel a datum:** uživatel, 7. 10. 2026.
> **Vzniklo:** 7. 10. 2026.
> **Kde brát současný stav:** `.forge/roadmap.json` (co se má dělat),
> `docs/ARCHITEKTURA.md` (co je závazné), `git HEAD` (co je hotové),
> `E:\Workspaces\forge-orchestra\HANDOFF.md` (stav orchestra).
>
> **Co z něj bylo provedeno:** k datu vzniku **nic** — všechna doporučení v §5 jsou
> návrh, ne záznam. Jakmile se podle některého z nich začne pracovat, patří do
> hlavičky **datum spotřeby** a co se provedlo.
>
> **Vzniklo ze TŘÍ nezávislých měření.** Vedle tohoto dokumentu existují dva
> paralelní audity, každý s vlastními skripty, a všechny tři se sešly na stejných
> číslech:
>
> - `E:\Workspaces\_audit-uos\AUDIT-PLANU-uo-shadows.md` (36 kB) — přinesl
>   **mutační sondu** a **sondu „smaž soubor"** (obojí jsem přeměřil sám),
>   plus dvě živé vady: `price()` = 0 a `repair()` 100 → 20;
> - `E:\Workspaces\_free-models-analyza\` — všech **323 job-logů** z GitHub API,
>   per-granule úspěšnost modelů a nález, že **`/roadmap` není prázdná, jen ji
>   nástroj neumí přečíst** (tím vyvrátil tvrzení mé první verze — viz §7.4).
>
> Ani jeden z nich nezapsal do herního repa nic.
>
> **Autor není reviewer.** Dokument vznikl v session, která sama nic v herním repu
> neopravovala (jediný zápis je tento soubor a snímek v `_analyza/`).

---

## 0. Odpověď v šesti větách

1. **Hypotéza uživatele platí a je měřitelná:** zadání „jak se hra hraje" v celém
   repu **neexistuje** — herní smyčka je tam **jednou větou v odrážce rozsahu**,
   ovládání, UI, prvních pět minut ani „jak hráč pozná úspěch" nikde.
2. **Nejlevnější vada je účetní, ne technická:** čtyři granule mají svou práci
   **sloučenou v `main` a `done` nemají** — dvě z nich drží `engine.shell`.
   A `world.map` (soubor 0 B) blokuje 5 granul, přičemž ji už nahradila
   `world.nodes`; **obě dnes vlastní tentýž soubor a obě jsou „připravené"**.
3. **Pro slabší modely organizovaný není — a je vidět proč.** Agent dostane
   `--map-tokens 0` (žádnou mapu repa), `CONVENTIONS.md`, své soubory a **ručně
   psanou prózu o mediánu 530 znaků**. Design k němu **nedorazí nikdy**.
   A empiricky: **dvě granule s nejkratším zadáním (211 a 278 znaků) selhaly
   58× ze 58**, zatímco delší a konkrétnější zadání procházela. **A dvě ze tří
   příčin těch porážek nejsou vina modelu** — brána parsování běží před importem
   (26 z 32 parse-selhání má falešnou chybu na prvním řádku) a rotace modelů je
   pro granule `any` od 2. 10. mrtvá (`entity.npc` dostala 18× tentýž model).
4. **Důsledek je naměřený:** 13 granul je `done`, ale běžící hra jich používá
   **tři** (a dvě z nich jsou týž soubor). Zbylých **10 hotových granulí hra nikdy
   nezavolá** — leží v repu jako knihovna bez konzumenta.
5. **Brány jsou zelené a je to zelená, která nic neznamená:** testy hlásí
   `91 kontrol, 0 selhání`, ale **41 ze 132 kontrol (31 %) se nikdy nespustí**,
   a **smažete-li soubor hotové granule, testy zůstanou zelené** (ověřeno:
   `attributes.gd` pryč → 89 kontrol, 0 selhání, `exit 0`) — což `AGENTS.md`
   výslovně zakazuje.
6. **Hra, kterou dnes hráč spustí, je sběračka dvou mincí** na izometrické mapě
   30×16 — se startovní chybou `tween_property` a nápovědou inzerující pět
   kláves, které kód neobsluhuje.

---

## 1. Co praxe harnessu říká, že má správný plán a design obsahovat

### 1.1 Metodika, kterou stanice má

Zlaté pravidlo (`~\.dsh\skills\game-developer\SKILL.md:16`):

```
Cíl → Požadavky → Architektura → Smlouvy → Granule → DAG → Brány → Ověření proti cíli
```

**Kde metodika sedí a kde má díru.** Pro **rozpad** a pro **zápis smluv** je
propracovaná a opřená o naměřené případy. Pro **herní design jako takový
neexistuje** — a to není dojem, to je měření:

> **Plošný sken (Python walk, ne `grep`) přes `C:\Users\Ssevc\Local-Deepseek`,
> `E:\Workspaces\forge-orchestra`, `E:\Workspaces\uo-shadows` a
> `C:\Users\Ssevc\.dsh\skills`, jen soubory `.md`:**
> zkratka `GDD` — **0 výskytů**; „game design document" — **0**;
> „jak se hraje" — **0**; „herní smyčka / core loop / play loop" — **0**;
> „prvních 5 minut" — **0**.

Co je místo toho, je **jediné normativní místo** — `JAK-PSAT-DESIGN-A-PLANOVAT-VYVOJ.md`
§2 (`:36–76`) — a je to **šest kontrolních otázek o smlouvách, ne o hře**:
tvar dat, přijímací kritérium, definice hotovo, explicitní non-goals, vlastnictví
souborů, „závislost = hotové a funkční". Plus šestibodový checklist před vydáním
granule.

**A ta jediná věta o hře, kterou KB má:** „*Cíl — jedna věta: co hráč dělá a jaký
je zážitek*" (`game-developer\SKILL.md:45`). Jedna věta. Zbytek metodiky je
architektura. Když se hledá „jak se hra hraje", najdou se v celé KB **tři místa
a dohromady jedna věta** (`SKILL.md:45`; `NAVRH-ORCHESTRA-NG.md:486–487`
s `goal.acceptance = ["hratelnost: hráč se pohne a nasbírá rudu"]`;
`:1009–1010`).

> **Žádný dokument neříká, jak herní smyčku popsat, jak ji rozepsat na okamžiky
> hraní, jak zapsat ovládání, obtížnost, tempo ani pocit ze hry.**

**A ten dokument, který měl tuhle mezeru zacelit, stojí.** `JAK-PSAT…` je
**„rostoucí dokument"** a jeho §7 (`:233–236`) nařizuje: „*každá session, která
při práci narazí na naměřenou vadu designu nebo plánování… Přidá oddíl do §4*".
Naměřeno 7. 10. 2026: **od 2. 10. do něj nepřibyl ani jeden případ** — poslední
commit, který se souboru dotkl, je přesun na `E:`, obsah je bajt na bajt shodný
se snapshotem z 2. 10. Hlavička pořád tvrdí „*Stav: 1. sezení, 6 naměřených
případů*". **Mechanismus, kterým se metodika měla učit z praxe, je přerušený.**

Poznámka k místu: `JAK-PSAT…` **není v knowledge base stanice** — leží
v `E:\Workspaces\forge-orchestra\` (a ve dvou identických snapshotted v jeho
`_analyza\`). Kdo ho hledá v `Local-Deepseek`, nenajde ho.

### 1.2 Co orchestra SKUTEČNĚ vynucuje — a co je jen text

Rozdíl mezi tím, co plán **deklaruje**, a tím, co orchestra **vymáhá**, je
v tomhle projektu hlavní zdroj iluze. Měřeno v `conductor/src/index.ts`,
šabloně `repo/` a v kopiích, které reálně běží v této hře:

| Pole granule | Čte ho conductor? | Co se stane, když chybí |
|---|---|---|
| `id`, `title`, `prompt` | ano | **shodí celý tik** — nevydá se NIC, pro žádnou hru, každou minutu |
| `owns` | ano (zámek souběhu) | bez něj agent nedostane soubor v chatu → model odmítne editovat |
| `depends_on` | ano | `[]` → granule se vydá okamžitě |
| `size_lines` | ano (jen limit auto-merge) | default 60 → větší změna je zamítnuta |
| `model` | ano | `any` → dostane ji první slabý free model |
| `done` | ano | přeskočí se a **počítá se jako hotová pro závislosti** |
| **`acceptance`** | **NE — 0 čtenářů** | nic. Granule projde i s `acceptance: ["nesmysl"]` |
| **`provides` / `consumes`** | **NE — 0 čtenářů** | nic |
| `done_note` | NE | nic |

**Tři pravidla, která platí jen jako text** (a proto se v praxi porušují):

1. **`size_lines > 60 ⟹ model: strong`** — kód obě pole čte nezávisle. Není to
   vynucené. V této roadmapě to porušuje **5 granul** včetně `world.level`
   s limitem **`<= 300` a bez `model`** → **slabý model dostane třísetřádkovou
   granuli**.
2. **`acceptance` je smlouva o ověření** — nemá ani čtenáře. Brány jsou natvrdo
   v `ci.yml` a `agent.yml`, bez ohledu na deklaraci.
3. **`owns` = soubory, které granule vlastní** — gate auto-merge povolí **jen
   `scripts/` a `assets/`**. Granule, jejíž `owns` je jinde, **se nemůže sloučit
   sama, nikdy**. V této roadmapě je taková právě jedna — `tests.harness`
   (vlastní `tests/run_tests.gd`), tedy granule, která vlastní testy.

### 1.3 Kde je v orchestra game design — **není**

Tohle je pro otázku uživatele klíčový nález, doložený na pěti místech:

1. **Žádné pole.** `RoadmapItem` ani registr her design neznají; `POST /game`
   bere jen `game_id`, `repo`, `roadmap_file`.
2. **Agent ho nečte.** `--read` obsahuje **jen** `CONVENTIONS.md` a soubory
   závislostí. Do `--read` se design nemá jak dostat — **žádná granule `docs/`
   nevlastní**.
3. **V šabloně herního repa design není.** `repo/` obsahuje `.gitattributes`,
   `CONVENTIONS.md`, `.forge/`, `.github/`. **Žádné `docs/`.** Nová hra si design
   ani nedoveze.
4. **Jediný kód, který `DESIGN.md` otevře**, je `release.yml`
   (`cat docs/DESIGN.md >> poznámky k vydání`) — **kosmetika pro člověka**.
5. **Konductor má design jen v komentáři** (`conductor/schema.sql:84`,
   `src/index.ts:1366`) — kód ho nečte.

**Co z toho plyne a je to nejdůležitější věta tohohle auditu:**

> **Designový dokument není pro orchestra dokument — je to zdroj, ze kterého se
> musí dát přepsat `prompt` granule. Co se do promptu nepřepíše, k modelu
> nedorazí. Design, který není zkompilovatelný do zadání, je dekorace.**

### 1.4 Co stanice sama navrhla a neprovedla

Není pravda, že by harness nevěděl, jak má správný plán vypadat. **Ví to a má to
sepsané** — jen to nezavedl:

- **`NAVRH-ORCHESTRA-NG.md` §8.4 `plan.json`** — plán jako **strom s povinnou
  stopovatelností**: `goal → requirements → capabilities → contracts (s tvarem
  dat) → grains`, kde granule má **povinné** `capability`, `size_lines`, `model`,
  **strukturované** `acceptance` (`{gate, call, expect}`, ne `["tests","wiring"]`)
  a `non_goals`. A tabulka vynucení: co se při porušení stane (`fail`, granule se
  nevydá).
- **`POUCENI-A-VZORY.md` §10.1 (O1–O12), §10.4 (pět vrstev), §11 (checklist pro
  nový projekt)** — dvanáct pravidel odvozených z naměřených omylů, včetně
  „žádný stav bez protějšku", „žádná tichá cesta", „rozhodnutí se měří, netvrdí".
- **§10.4 pět vrstev:** `1. KONTRAKT` (rozhoduje o ~0 nákladů) → `2. ZADÁNÍ`
  (rozhoduje o 55 % běhů) → `3. PROVEDENÍ` (který model — **až třetí páka**)
  → `4. OVĚŘENÍ` → `5. PRODUKT`.

**To je odpověď na „jak má vypadat správný plán": má vypadat jako §8.4. A plán
UO-Shadows nevypadá — je to předchozí generace.**

---

## 2. Verdikt: je plán UO-Shadows dobře formulovaný?

### 2.1 Měřený stav plánu

Vše níž je **naměřeno 7. 10. 2026** na `HEAD = 932dc6f`, ne převzato z dokumentace.

| Veličina | Naměřeno |
|---|---|
| granul celkem | **22** |
| `done: true` | **13** |
| nedokončených | **9** |
| granul bez `size_lines` | **8** |
| granul se `size_lines > 60` a **bez** `model` | **5** (`world.level` 300, `sim.combat` 130, `sim.mining` 80, `persist.save` 100, `ui.hud` 100) |
| granul s `provides`/`consumes` | **0 z 22** |
| granul s klíčem `capability` (vazba na cíl) | **0 z 22** |
| granul s `non_goals` | **0 z 22**; v `docs/ARCHITEKTURA.md` slovo `non_goals` **0×** |
| výskytů slova „hotovo" v `CONVENTIONS.md` | **0×** (definice hotovo v repu není) |
| granul s `acceptance` | 22 — ale **19× doslova `["tests","wiring"]`** |
| souborů vlastněných dvěma granulemi | **3** (`scripts/world.gd`, `scripts/player.gd`, `scripts/save.gd`) |
| závislostí mířících na nehotovou granuli | **10** |
| z toho z **hotové** granule na nehotovou | **2** (`sim.mining`→`world.map`, `persist.save`→`world.map`) |
| granul s `owns` mimo `scripts/`/`assets/` | **1** (`tests.harness` → nemůže se sloučit sama) |
| granul, jejichž **práce je v `main`, ale nejsou `done`** | **4** — `sim.crafting` (#34), `sim.offline` (#35), `persist.save.state` (#37), `tests.harness` (`279f584`); ověřeno `git merge-base --is-ancestor` = `True` |
| granul překračujících svůj deklarovaný `size_lines` | **5** (`entity.player` 191>120, `entity.player.api` 191>180, `persist.save` 150>100, `persist.save.state` 150>140, `tests.harness` 1406>1200) + `engine.shell` (377>120, ještě neproběhla) |
| kontrol v `tests/run_tests.gd`, které se **nikdy nespustí** | **41 ze 132 (31 %)**; hláškou je ohlášená **jedna** (kryje 3 kontroly) |
| granul, které má **D1 conductora** omylem `done` | **2** — `world.map` a `world.nodes`; `scripts/world.gd` má v `origin/main` **0 B** → conductor je už **nikdy nevydá** |
| běhů workflow `agent.yml` (celé dějiny / éra hry) | **323 / 114**; úspěšnost **10,5 % / 12,3 %** |
| součet délek zadání | **15 886 znaků**; medián **530**, min **211**, max **2 080** |
| zadání odkazujících na externí kontext (`CONVENTIONS.md §…`, „vzor je v…") | **8 z 22** |

**Linter plánu** (`forge-orchestra\tools\lint-roadmapa.py`, spuštěn na této roadmapě)
hlásí **3 blokující problémy** (tři kolize `owns`) a 13 poradních. **Skončí ale
`exit 0`** — je poradní, ne brána. A nehlásí ani rozpad konzistence `done`, ani
chybějící `model`, ani chybějící `provides`. **V CI hry se nespouští vůbec.**

### 2.2 Vady plánu seřazené podle dopadu

**V0 — Kritická cesta je zablokovaná účetnictvím, ne chybějící prací.**
**Nejlevnější a nejdopadovější nález celého auditu.** Čtyři granule mají svou
práci **sloučenou v `main`**, ale v roadmapě `done` nemají (ověřeno
`git merge-base --is-ancestor` = `True`):

| Granule | Commit v `main` | `done` |
|---|---|---|
| `sim.crafting` | `9876586` (PR #34) | **ne** |
| `sim.offline` | `ee7af53` (PR #35) | **ne** |
| `persist.save.state` | `7ad8d04` (PR #37) | **ne** |
| `tests.harness` | `279f584` | **ne** |

`engine.shell` přitom na `sim.crafting` a `sim.offline` **závisí**. Část kritické
cesty tedy není zatarasená chybějící prací, ale **zastaralým zápisem** — a
`sim.crafting` je navíc dnes v množině „připraveno", takže ji conductor
**vydá znovu** a vznikne zbytečný PR (a konflikt na `scripts/crafting.gd`).

**V1 — Kritická cesta vede přes mrtvou granuli.**
`engine.shell` je jediná granule, která měla přepsat monolit `game.gd` na kostru
s registrem komponent — tedy **jediné místo, kde by hotové komponenty dostaly
konzumenta**. Je blokovaná šesti granulemi, z toho **`world.map` je zombie**:
je `done: false`, její soubor `scripts/world.gd` má **0 bajtů**, její práce
skončila v `_retired/world.gd`, a **nahradila ji nová granule `world.nodes`** —
ale `world.map` z plánu nikdo neodstranil. Drží tedy `engine.shell`, blokuje
5 dalších granul a **vlastní tentýž soubor jako `world.nodes`**.
**A obě jsou dnes v množině „připraveno"** — conductor je smí vydat **paralelně
na tentýž soubor**, což je přesně to, čemu má `owns` zabránit.

**V2 — Tři soubory vlastní dvě granule.**
`world.gd`, `player.gd`, `save.gd`. Vždy je to stejný vzor: první granule byla
zapsaná jako `done`, práce v repu nebyla, tak se **dodatečně založila druhá
granule na tentýž soubor**. To je obcházení pravidla „1 granule = 1 soubor"
místo opravy plánu — a znamená to, že plán **nemá jak vyjádřit „tuhle granuli
ještě jednou, pořádně"**.

**V3 — `done` je pro ostatní granule důvěryhodné jen papírově.**
`done: true` se používá jako splněná závislost. Dvě hotové granule ale závisí na
nehotové (`world.map`). Historicky se `done` **už jednou muselo opravovat ručně**
(`entity.player`, `world.map`) a linter ho sám označuje za **„naměřeno jako
NESPOLEHLIVÉ"**. Přesto se na něm staví celý DAG.

**V4 — Plán nenese rozhraní.**
`provides`/`consumes` **0 z 22**. Rozhraní tedy existuje jen jako **prozaický text
uvnitř `prompt`**. Smlouvy v `docs/ARCHITEKTURA.md` §2 existují — ale agent ten
soubor nikdy nevidí. **Plán a smlouvy jsou ve dvou světech, které se nepotkají.**

**V5 — `acceptance` je pečeť, ne kritérium.**
19 z 22 granul má doslova `["tests","wiring"]`. Metodika přitom žádá **konkrétní
volání s očekávanou hodnotou** (`gather(uzel, 5) == 6`). Třiadvacetkrát opsaná
dvojice slov nenese žádnou informaci — a **stejně ji nikdo nečte**.

**V6 — Pravidlo velikosti se porušuje u 5 granul.**
`world.level` smí mít **300 řádků a nemá `model`** → orchestrace ji pošle slabému
modelu. To je přesně ta vada, kterou metodika označuje za nejdražší.

**V7 — Granule, která vlastní testy, se nemůže sloučit.**
`tests.harness` vlastní `tests/run_tests.gd`. Gate auto-merge povolí jen
`scripts/` a `assets/` → **PR z této granule zůstane otevřený vždy** a po pěti
pokusech úloha skončí `failed`. Není to náhoda v datech, je to **návrh plánu
proti gate**.

**V8 — Dokument a strojový plán se rozešly.**
`docs/ARCHITEKTURA.md` — který se sám hlásí jako **„jediný závazný"** — vyjmenovává
v §3 **18 granul**. Strojový plán jich má **22**. Čtyři (`world.nodes`,
`entity.player.api`, `persist.save.state`, `tests.harness`) v závazném dokumentu
**nejsou vůbec**, a `world.map` v něm naopak figuruje jako živá granule.
Dokument, který je autorita, **popisuje jiný plán, než jaký se vykonává**.

### 2.3 Je plán organizovaný pro slabší modely?

**Ne — a je to měřitelné, ne dojmové.** Tři měření:

**(a) Co model skutečně dostane.** Přesné složení kontextu
(`.github/workflows/agent.yml:224–236`):

```
aider --model openai/$FORGE_MODEL
      --read CONVENTIONS.md            # natvrdo, vždy
      --read <soubory závislostí>      # z owns granul v depends_on, jen existující
      --file <soubory granule>         # editovatelné, z owns
      --map-tokens 0                   # ŽÁDNÁ mapa repa
      --edit-format diff
      --message "$FORGE_PROMPT"        # ručně psaná próza z roadmapy
```

**`--map-tokens 0` znamená, že model nevidí strukturu projektu.** Jeho svět je:
276 řádků `CONVENTIONS.md` + vlastní soubory + soubory přímých závislostí +
**jeden odstavec zadání**. Žádný design, žádná architektura, žádná mapa.

**(b) Zadání jsou krátká a nestejnoměrně kvalitní.** Medián 530 znaků (≈ 90 slov).
Nejslabší:

- `entity.npc` — **211 znaků**: „*Vytvoř obchodníka (Area2D): při dotyku hráče
  otevře obchod — buy/sell přes economy.gd. Vystav trade(player) -> void…*"
  **„Otevře obchod" není specifikace** — jaké UI? odkud ceny? co když hráč nemá
  zlato? Model si musí vymyslet tři věci, které pak nikdo netestuje.
- `sim.economy` — **258 znaků**: „*ceny předmětů (price(item) -> int odvozená
  z materiálu a kvality)*" — **vzorec není**, a `player` začíná s **0 zlatem**,
  takže `buy()` nemůže nikdy uspět. Zadání je nesplnitelné a nikde to není.

**(c) Zadání si navzájem odporují.** Naměřený případ, který je pro otázku
„zvládne to hloupější model" nejvýmluvnější — **granule `core.skills`**:

Zadání té granule (`roadmap.json`) obsahuje **obě** tyhle věty současně:

> „*vytvoř dovednosti jako VLASTNOST s konkrétním jménem: `var dovednosti:
> Dictionary = {"tezba": 0, …}`*"
>
> „*testy je čtou takto: `sk.get("tezba")` … Když skript vlastní `get()` nemá,
> `sk.get("tezba")` vrátí hodnotu vlastnosti.*"

**Obě nemůžou platit.** Když je celý stav v jednom slovníku `dovednosti`, pak
`Object.get("tezba")` **nemá co vrátit** — `tezba` není vlastnost. Naměřeno
spuštěním: `sk.get("tezba")` vrací `null`, test to zjistí, **vypíše hlášku
a tři kontroly přeskočí**. Běh přesto hlásí `91 kontrol, 0 selhání`, `exit 0`.

A aby to bylo horší: `core.skills` je `done`, **visí na ní 10 dalších granul**
a v `ARCHITEKTURA.md` §2 je její smlouva zapsaná jako **`get(skill)`** — což
`CONVENTIONS.md:127` **výslovně zakazuje** („*Nikdy nepoužívej jako název funkce:
`get`, …*"). Smlouva a konvence si v témž repu přímo odporují.

**Verdikt:** plán je pro slabší modely organizovaný **na úrovni infrastruktury**
(DAG, zámky `owns`, brány, rotace modelů — to je promyšlené a funguje), ale
**ne na úrovni zadání**. Zadání je ruční próza bez schématu, bez rozhraní
a v nejméně jednom případě **vnitřně rozporná**.

**(d) A je to vidět i v datech.** Empirický záznam všech 114 běhů éry hry
(§4.6) ukazuje korelaci, která se nedá přehlédnout:

| znaků zadání | granule | běhů | úspěch |
|---|---|---|---|
| **211** | `entity.npc` | 33 | **0 %** |
| **278** | `entity.enemy` | 25 | **0 %** |
| 407 | `sim.offline` | 2 | 50 % |
| 989 | `persist.save.state` | 5 | 20 % |
| 1 805 | `world.nodes` | 2 | 50 % |

**Dvě granule s nejkratším zadáním selhaly 58× ze 58.** A `entity.npc` navíc
**18 běhů v řadě dostala tentýž model** (mrtvá rotace, §4.5 g2) — takže jejích
33 pokusů je statisticky **jeden pokus zopakovaný 33×**.

**Co v zadání `entity.npc` chybí** (a model to 33× musel uhodnout): jaký `extends`,
že se v `Area2D` **nesmí deklarovat `position`** (8× `Member "position" redefined`
— a `CONVENTIONS.md:129` to zakazuje, přičemž soubor je v chatu přes `--read`),
výslovné typy místo `:=` u neotypovaných výrazů (19× `Cannot infer the type`),
že služby se berou z `get_parent().component(id)` — **o registru komponent
v zadání není ani slovo**, přitom celá architektura na registru stojí — a že
`Economy` je `class_name` v `economy.gd`, kdežto `Combat` žádný nemá.

**A kde je hranice:** `world.nodes` (1 805 znaků), `entity.player.api` (1 362)
a `persist.save.state` (989) — všechny přepsané 3. 10. — mají tyhle věty
větu po větě. **A prošly.**

---

## 3. Verdikt: game design

### 3.1 Původ: design nepsal designér, vygeneroval ho plánovač

`docs/DESIGN.md:3–7` to říká sám:

> „**Zrušeno jako zdroj pravdy.** … Tenhle dokument **vygeneroval plánovač
> (`forge plan`)** pro první nástřel a popisuje starý 6-úkolový plán — orchestr
> ho už nepoužívá."

A `docs/ARCHITEKTURA.md:6–7` dodává, že jeho **autorská kopie je mimo repo**
(`gameforge/projects/uo-sandbox/docs/ARCHITEKTURA.md`) — jenže **GameForge byl
30. 9. 2026 zrušen a smazán**. Autorská kopie závazného dokumentu tedy
**neexistuje**.

Co designér zadal, je dohledatelné v `DESIGN.md:27` jako **„Původní obsah
(zmrazený)"** — **jeden odstavec české prózy** začínající „*Nova hra podle
principu Ultima Online, ale v rozsahu, ktery zvladne maly tym…*". To je celé
zadání, ze kterého vznikla hra.

**Takže:** hra nevznikla z designu. Vznikla z **odstavce**, ze kterého plánovač
vygeneroval design, z designu architekturu a z architektury 22 granul.
To je přesně mechanismus, který vyrábí „popis vrstev místo smluv" — a metodika
to pojmenovává (`JAK-PSAT…:188–191`).

### 3.2 Zadání „jak se hra hraje" neexistuje — měření

Prohledány `docs/DESIGN.md`, `docs/ARCHITEKTURA.md`, `CONVENTIONS.md`,
`AGENTS.md`, `docs/BRANY-HRY.md`, `project.godot`. **(README v repu není.)**

| Otázka | Odpověď v repu |
|---|---|
| Jaké je ovládání (klávesy, myš)? | **NIKDE.** `project.godot` nemá definovanou ani jednu vstupní akci. Jediné místo v repu, kde je ovládání popsané, je běhová nápověda `game.gd:221` — **a ta je nepravdivá** (viz §4.1). |
| Co hráč dělá v prvních 5 minutách? | **NIKDE.** |
| Co je vidět na obrazovce, jak vypadá UI? | **NIKDE.** `ARCHITEKTURA.md:97` říká jen „prezentace \| HUD, kamera \| `scripts/hud.gd`". Skutečný obsah lišty je jen v kódu. |
| Jak hráč pozná úspěch? (vítězná podmínka, feedback) | **NIKDE** — nemá ji ani `DESIGN.md`. |
| Jak zní hra? | `DESIGN.md:52–53` zvuk popisuje; **`ARCHITEKTURA.md` o zvuku nemá ani slovo**; `assets/audio/` v repu **neexistuje**. |

**Jediné, co existuje, je jedna věta** (`ARCHITEKTURA.md:32`):

> „*smyčka: `těžit → tavit → kovat → používat → opravovat`*"

To je celý popis hraní v celém repu.

**A co je jako „zdroj pravdy o tom, jak se hra hraje", označeno dnes:**

- `docs/DESIGN.md` se **sám zrušil** (`:3`).
- `AGENTS.md:137` posílá na `.forge/roadmap.json` — což je DAG granulí
  (`owns`, `depends_on`), o hraní neříká nic.
- **`AGENTS.md:91` přitom STÁLE tvrdí**, že „`docs/DESIGN.md` — co hra je a jak se
  má chovat". To je **přímý rozpor uvnitř trvalých pravidel**: jeden řádek
  odkazuje na dokument, který se o dvě sekce výš hlásí jako zrušený.

### 3.3 Rozpory mezi dokumenty

**Nejostřejší rozpor je uvnitř `DESIGN.md` samotného** — denní cyklus je na
`:14–16` **out-of-scope**, na `:42` v seznamu mechanik a na `:57` v rozsahu
implementace. Tři místa, tři odpovědi.

Dále: **`DESIGN.md` a `ARCHITEKTURA.md` se neshodnou na osmi mechanikách.**
`DESIGN.md` má navíc alchymii, léčení, tatažství, **NPC reakce na činy** a zvuk;
`ARCHITEKTURA.md` má navíc offline režim, asistenci, smrt se ztrátou věcí,
zlato s obchodníkem, trvalý svět s respawnem a tvar světa (ostrov + důl + les).
Průnik „out-of-scope" jsou jen **MMO a magie**.

**Nejhorší důsledek:** `DESIGN.md` alchymii a denní cyklus **pojmenovává a ruší**
— je tedy dohledatelné, že byly vyřazeny. `ARCHITEKTURA.md` je **nemá vůbec**,
takže **není dohledatelné, že byly vyřazeny**. Co není vyřazené, se dá omylem
vrátit — a `game.gd` je dodnes pořád má (`:20` `alchymie`, `:25` `cas_dne`).

### 3.4 Kolik z „architektury" je vlastně design

`docs/ARCHITEKTURA.md` má **395 řádků**. Rozdělení podle oddílů:

| Druh obsahu | Řádků | Podíl |
|---|---|---|
| **game design** (§0 cíl, pilíře, rozsah, požadavky, schopnosti, obsah) | ~75 | **19 %** |
| architektura (vrstvy, smlouvy, tvary dat) | ~202 | 51 % |
| proces a plán orchestry (granule, DAG, vlny, tooling) | ~98 | 25 % |
| hlavička | 8 | 2 % |

I když k designu připočteme vzorce a tabulku stavů hráče z §2.1–2.3,
je to **~95 řádků (24 %)**. A ani to **není popis hraní** — je to soupis
schopností a datových tvarů.

**Závazný dokument hry je z čtyř pětin o něčem jiném než o hře.**

---

## 4. Aktuální stav hry a kvalita zpracovaných granulí

### 4.1 Co hra dnes skutečně dělá

Naměřeno spuštěním (`--headless`, HEAD `932dc6f`) a snímkem
(`_analyza/uo-shadows-stav-hry.png`):

```
[level] main: 30×16 políček, izometricka 96×48 px, dlaždic: 480, značek: 4
[game] připraveno: hráč + 2 mincí, zvuků načteno: 0, dlaždice: ano, úroveň: main 30×16
ERROR: Required object "rp_target" is null.   (game.gd:181, tween_property)
```

**Hra, kterou hráč spustí, je tohle:** izometrická mapa 30×16 (480 dlaždic),
hráč, **dva identické sprity** (hráč a NPC — nerozeznatelné), **dvě mince**,
Label „Skóre: 0 / 2 HODNOTA: 25", FPS a nápověda. Dá se **jen chodit**
(šipky/WASD) a sbírat mince.

**A tohle není zastaralý klon — je to i to, co je venku.** Ověřeno 7. 10. 2026:
`https://ssevcikm-spec.github.io/uo-shadows/index.png` odpovídá `200`,
`last-modified` **11:40:00 GMT**; `main` na GitHubu je **932dc6f** (11:38:58),
lokální `HEAD` je **932dc6f** a `origin/main..HEAD` = **0**. Nasazení je tedy
**aktuální** — sběračka mincí je skutečný, publikovaný stav hry.

**Vady viditelné okamžitě:**

- **Nápověda lže.** `game.gd:221` inzeruje „*E těžba rudy, C tavení, B kování,
  X použít zbraň, R oprava, M hudba*". V `game.gd` je **0 výskytů `Input`/`KEY_`**
  (naměřeno; jediné čtyři nálezy v celém `scripts/` jsou v `player.gd:74–81`).
  **Pět z šesti inzerovaných kláves nedělá nic.**
- **Ukládání neexistuje.** `game.gd:355–377` `_save_state()`/`_load_state()` jsou
  definované a **nikdy se nevolají** — `check-wiring.py` to hlásí jako poznámku.
- **NPC nikdy nic neudělá.** `game.gd:348` testuje `suroviny["ruda"] < 3`, ale
  `suroviny` se nikde nezvyšuje.
- **Chyba při startu** (`tween_property` na `null`).
- `assets/audio/` a `assets/ui/` **neexistují** → „zvuků načteno: 0".

### 4.2 Klíčová otázka: dostane se hotová práce k hráči?

**Ne.** Měřeno:

| Skript | Načten běžícím kódem? |
|---|---|
| `scripts/game.gd` | ano (`main.tscn`) |
| `scripts/level.gd` | **ano** (`game.gd:155`) |
| `scripts/player.gd` | **ano** (`game.gd:270`) |
| `assist.gd`, `attributes.gd`, `combat.gd`, `crafting.gd`, `economy.gd`, `hud.gd`, `item.gd`, `mining.gd`, `offline.gd`, `save.gd`, `skills.gd` | **NE — jen z `tests/`** |
| `npc.gd`, `enemy.gd` | **v repu vůbec nejsou** |
| `world.gd` | **0 bajtů** |

`game.gd` volá `load()` na skripty **dvakrát** — a to je celý seznam.
**Z 13 hotových granulí jsou pro hru dosažitelné tři** (`world.level`,
`entity.player`, `entity.player.api` — poslední dvě jsou týž soubor).
**Deset hotových granulí hra nikdy nezavolá.**

A protože **`game.gd` nemá funkci `component(name)`**, kterou komponenty
vyžadují (berou z ní služby), komponenty by ani nefungovaly: testovací běh
to říká nahlas — `ERROR: mining.gd: komponenta Skills není v registru`,
`ERROR: save.gd: nad sebou nemám kostru s component(id)`.

**Komponenty byly vyvíjeny a testovány proti atrapě**, která v běžící hře
neexistuje (`run_tests.gd` `TestKostra`). Komentář to přiznává: „*totéž rozhraní,
jaké **bude mít** `game.gd`*".

### 4.3 Kvalita granulí po jedné

| # | Granule | `done` | Soubor (řádků v HEAD) | Je vidět ve hře? | Kvalita |
|---|---|---|---|---|---|
| 1 | `data.content` | ✅ | 5× JSON (11–33) | ne (nikdo je nečte) | obsah je, konzument chybí |
| 2 | `core.attributes` | ✅ | `attributes.gd` (21) | ne | **dobrá** — test volá `hodnota()`, ověřeno |
| 3 | `core.skills` | ✅ | `skills.gd` (15) | ne | **API dobré, zadání rozporné**; 3 kontroly se přeskočí |
| 4 | `world.level` | ✅ | `level.gd` (283) | **ano** | **nejlepší granule** — izometrie ověřená měřením sklonu |
| 5 | `world.map` | ❌ | `world.gd` (**0 B**) | ne | **mrtvá granule**, blokuje 5 dalších |
| 6 | `entity.item` | ✅ | `item.gd` (39) | ne | funguje; `material`/`quality` v datech **nejsou**; **`repair()` sníží trvanlivost ze 100 na 20** |
| 7 | `entity.player` | ✅ | `player.gd` (191) | **ano** | dobrá; historicky `done` bez práce; **`die()` nemá jediné volání**; limit 120 **překročen** |
| 8 | `sim.combat` | ✅ | `combat.gd` (127) | ne | **vzorová smlouva** (§2.1); funkčně testovaná |
| 9 | `sim.mining` | ✅ | `mining.gd` (72) | ne | funkčně testovaná; **závisí na mrtvém `world.map`** |
| 10 | `sim.crafting` | — | `crafting.gd` (78) | ne | **práce je v `main` (`9876586`), ale `done` chybí** → dnes „připraveno" a vydá se znovu; dělá si vlastní instanci `skills.gd` |
| 11 | `sim.economy` | ✅ | `economy.gd` (47) | ne | **jen `has_method`**; **`price()` = 0 pro každý předmět** (`SCRIPT ERROR`) → obchod zdarma |
| 12 | `entity.npc` | — | **chybí** | — | zadání 211 znaků, nedodáno |
| 13 | `entity.enemy` | — | **chybí** | — | **5 neúspěšných běhů** |
| 14 | `sim.offline` | — | `offline.gd` (57) | ne | **práce je v `main` (`ee7af53`), ale `done` chybí**; jen `has_method` |
| 15 | `sim.assist` | ✅ | `assist.gd` (17) | ne | funkčně testovaná; **slovník triggerů nikde** |
| 16 | `persist.save` | ✅ | `save.gd` (150) | ne | funkčně testovaná; **závisí na mrtvém `world.map`** |
| 17 | `ui.hud` | ✅ | `hud.gd` (92) | ne | funkčně testovaná; `<= 100` **bez `model`** |
| 18 | `engine.shell` | — | `game.gd` (377) | — | **NIKDY NEPROBĚHLA** — hra je pořád monolit |
| 19 | `world.nodes` | ❌ | `world.gd` (0 B) | ne | PR #32 sloučen, doručil **prázdný soubor** |
| 20 | `entity.player.api` | ✅ | `player.gd` (191) | **ano** | oprava předchozí vady, ne nová práce |
| 21 | `tests.harness` | — | `run_tests.gd` (1 406) | — | **owns mimo `scripts/`** → nemůže se sloučit; **práce je v `main` (`279f584`)**, `done` chybí; limit 1200 překročen; **hodnotí sám sebe** (`acceptance: [tests]`) |
| 22 | `persist.save.state` | — | `save.gd` (150) | ne | oprava předchozí vady; **práce je v `main` (`7ad8d04`)**, `done` chybí |

**Řádky jsou z blobu (`git show HEAD:…`), protože `Get-Content | Measure-Object -Line`
naměřilo u téhož souboru o 4–45 řádků méně** — autorita je blob, ne přepočet.

### 4.4 Co se daří

Poctivě: **víc než by verdikt „hra je sběračka mincí" naznačoval.**

1. **Komponentní vrstva je skutečně kvalitní.** `attributes`, `skills`,
   `combat`, `mining` mají smluvní API a **testy je volají**. Smlouva `combat.resolve()`
   v `ARCHITEKTURA.md` §2.1 je **učebnicový příklad toho, co metodika žádá** —
   tvar dat, odkud jsou čísla, přijímací kritérium. Test navíc obsahuje
   **atrapu v rozporu se sebou** (`hodnota` 100 vs vlastnost 10), aby se větvení
   nedalo obejít.
2. **Infrastruktura orchestra funguje.** DAG, zámky `owns`, rotace modelů,
   auto-merge s gate, `--check-only`, `--import` — to je promyšlené a v praxi
   to drží.
3. **Dokumentace omylů je výjimečná.** `JAK-PSAT…`, `POUCENI-A-VZORY.md` (64 kB),
   `KRONIKA-PROJEKTU.md`, `docs/BRANY-HRY.md` — každá poučka má **soubor, číslo
   a datum**. Tohle je nejcennější aktivum celého harnessu a je nadstandardní.
4. **Některé lekce se aplikovaly.** Poté, co tři PR prošla zeleným CI a nemohla
   fungovat, se `combat` a `mining` přepsaly na **funkční** kontroly (ne
   `has_method`) — a je to v kódu vidět i s odůvodněním.

### 4.5 Kde to selhává

**(a) Zelená, která nic neznamená.** Běh testů: `[test] 91 kontrol, 0 selhání`,
`exit 0`. Naměřeno třemi nezávislými sondami:

**(a1) 41 ze 132 kontrol se nikdy nespustí.** Ze 132 volání `_check(` je jen
**17 mimo každý `if`/`for`** — ostatních **107 je podmíněných** a **94 z nich je
přítomnostních** (`has_method`, `!= null`, `has(`, `.size()`). Empiricky se
spustí **91** kontrol, **41 se nikdy nespustí (31 %)**. A **ohlášena je jediná
výjimka** — hláška u skillů, která kryje 3 kontroly. **Zbylých 38 se přeskočí
bez slova.**

**(a2) Smaž soubor hotové granule — testy zůstanou zelené.** Ověřeno mnou
v kopii repa 7. 10. 2026:

| Běh | Výsledek |
|---|---|
| baseline | `91 kontrol, 0 selhání`, `exit 0` |
| **smazáno `scripts/attributes.gd`** (`done: true`) | **`89 kontrol, 0 selhání`, `exit 0`** |
| **smazáno i `scripts/economy.gd`** (`done: true`) | **`88 kontrol, 0 selhání`, `exit 0`** |

`AGENTS.md` to zakazuje výslovně: „*Soubor, který součástí hry být MÁ, musí při
nenačtení **SELHAT***." V souhrnné sondě přes 20 souborů prošlo smazání
**9× tiše** (kromě uvedených i `crafting.gd`, `offline.gd`, `world.gd`
a 4 z 5 datových souborů `data.content`).

**(a3) Mutace v hotové komponentě zůstane zelená.** Sonda (20 mutací, v kopii,
s ověřením provedení mutace): **12 odhaleno, 7 neodhaleno**. Neodhalené:
`player.die()` nezahodí inventář · `attributes.hodnota()` vrací vždy 0 ·
`attributes.derived()` damage ×100 · strop skillu 1000 · `economy.gold()`
vrací 999 · `offline` strop 10× · `crafting` kvalita vždy 0.
**Proč:** blok „funkčních kontrol" ukládání a HUDu běží proti **atrapám**
(`TestAtributy`, `TestSkilly`, `TestEkonomika`, `TestHrac`), ne proti skutečným
komponentám. `run_tests.gd` má **16 tříd-atrap na 315 řádcích (22 %)**.

**(a4) Dokument slibuje `get()`, kód má `hodnota()`.** `docs/ARCHITEKTURA.md:129–130`
deklaruje `get(attr)` a `get(skill)`; `CONVENTIONS.md:127` `get` **zakazuje**;
kód má `hodnota()`. `run_tests.gd` je napsaný **podle dokumentu**, takže
`sk.get("tezba")` se trefí do enginového `Object.get()` → `null` → **tři
kontroly stropu skillu se přeskakují od napsání souboru** (§2.3c).

Dále:

- **`sim.economy` a `sim.assist` (obě `done`) mají jen `has_method`**
  (`run_tests.gd:809`, `:835`) — a to i přesto, že soubor o dvě stě řádků výš
  (`:620`, `:754`) nese komentář „*FUNKČNÍ kontrola, ne jen `has_method`*".
  **Lekce se aplikovala na dvě granule a na dvě ne.**
- **Kontroly migrace monolitu se nikdy nespustí** (`run_tests.gd:952`
  `if main.has_method("component")` — `game.gd` `component()` nemá). Tedy
  „kostra instancuje komponenty" i „monolit je pryč" se **nikdy neměří**.
- **`combat.gd` to má ve vlastním komentáři**: „`resolve()` nikdo nevolal.
  `combat.gd` je v D1 `done`, takže ji conductor znovu nevydá."

**(b) Brány jsou zelené a samy přiznávají, že neměřily.** Spuštěno 7. 10. 2026:

| Brána | Výsledek | Co nepřiznala jako vadu, ale jako poznámku |
|---|---|---|
| `check-schema.py` | `exit 0` „Schéma je v souladu" | „*level.gd nemá fallback buňky — kontrola fallbacku tedy nemá co měřit*"; „*scripts/world.gd existuje, ale jeho buňku se NEPODAŘILO přečíst — kontrola „dvě různé představy o mřížce" **NEPROBĚHLA***" |
| `check-wiring.py` | `exit 0` „Vše v pořádku" | 4 poznámky o mrtvých funkcích; **korpus staví z `rglob("*.gd")` — včetně `tests/`**, takže funkce zmíněná jen v testu se počítá za použitou |
| `check-assets.py` | `exit 0` „assety odpovídají specu" | „*animace chůze v projektu není – přeskočeno*"; „*hudba ve hře není – měření hudby přeskočeno*" |

**Brána, která napíše „NEPROBĚHLA" a přesto vytiskne „v souladu", je přesně ta
past, kterou metodika popisuje** („Nula a nezměřeno nejsou úspěch").

**(c) Trvalá pravidla obsahují tvrzení, která už neplatí.** Tři naměřené:

| Kde | Co tvrdí | Naměřeno 7. 10. 2026 |
|---|---|---|
| `AGENTS.md:108–110` | rozhraní `add_rule` „**míchá jazyky**" a kód má `"cíl mrtev"` česky | `assist.gd:15` má **`"target dead"`** — anglicky. `git show 2858c7e` dokládá, že se to přejmenovalo **2. 10.**; `AGENTS.md` vznikl **4. 10.**, ale popisuje stav před přejmenováním. **Dnešní kód je jazykově konzistentní** — kdo se řídí pravidlem, „opraví" správný kód. |
| `CONVENTIONS.md:273` | „testy: **26 kontrol**, počet roste" | běh hlásí **91 kontrol** |
| `CONVENTIONS.md:252` | „Použij `_safe_spot(vp)` **(už v `game.gd` je)**" | `_safe_spot` v `scripts/` — **0 nálezů**. Návod na neexistující funkci. |
| `AGENTS.md:91` | „`docs/DESIGN.md` — **co hra je a jak se má chovat**" | `DESIGN.md:3` se hlásí jako **zrušený zdroj pravdy** |

Tohle je obzvlášť zákeřné **pro slabý model**: dostane `CONVENTIONS.md` do
kontextu jako `--read` při **každém** běhu. Tři z těch tvrzení jsou nepravdivá
nebo rozporná — a jsou to právě ta, kterými se má řídit.

**(d) `CONVENTIONS.md` radí opak architektury.** `:237`:

> „*nepřidávej nové soubory, když to jde udělat v `scripts/game.gd`*"

To je instrukce **k opaku celého plánu** — plán je postavený na tom, že se
`game.gd` **rozloží** na komponenty (`engine.shell`). Model, který se řídí
konvencemi, bude monolit **posilovat**.

**(e) Slovníky rozhraní nikde.** Agent si musel vymyslet:

- **ID komponent** — `ARCHITEKTURA.md:145` uvádí jen `component(name) -> Node`,
  žádný seznam. Každá komponenta si je vymyslela sama (`hud.gd` volá
  `component(id)`, dokumentace píše `component(name)`).
- **Kvalitu předmětu dvakrát jinak** — `item.gd:10` má `kvalita: int`,
  `economy.gd:21–30` čte `item.quality` jako **řetězec**
  (`"common"…"legendary"`). Vlastnost `quality` **neexistuje** → `price()` na
  skutečném předmětu selže. A `items.json` **nemá ani `material`** → `item.gd:25`
  nastaví `""`.
- **Tvar uzlu suroviny** — `mining.gd` čte `resource_id`, `difficulty`, `cell`;
  ve smlouvě to není a mapa má **0 markerů surovin**.
- **Zbraň hráče** — smlouva i `combat.gd` berou `vybrana_zbran`/`zbran`,
  `player.gd` má **`equipped`** → `resolve()` na skutečném hráči **nenajde zbraň
  a tiše dá damage 0**.

**(f) Fronta stojí — ale ne z toho důvodu, jaký hlásí nástroj.**
*(Oprava dřívějšího tvrzení tohoto auditu.)* Napsal jsem, že `/roadmap` je
**prázdná**. **Není.** Ověřeno přímým dotazem 7. 10. 2026:

```
GET /roadmap → HTTP 200, klíč odpovědi: roadmap, řádků: 21
statusy: {"done": 19, "failed": 1, "queued": 1}
```

`tools/status.mjs:81` čte `rm.json.items || rm.json.grains` — conductor vrací
`{roadmap: […]}` → nástroj dostane `undefined` a vypíše **„(prazdna)"**.
**Roadmapa je plná; čte ji špatně nástroj.** Přesně past, kterou metodika
popisuje: *když výsledek vypadá jako „nic tam není", první otázka je
„proběhlo to měření?"* — a já jsem se jí nechal chytit.

Skutečný stav: `entity.npc` (`#236`, `ready`, `attempts=3`) čeká na **cooldown
`RETRY_HOURS=3`** (`roadmap.updated_at` = 12:16:29) → uvolní se ~15:16.
`entity.enemy` (`#235`, `failed` 5/5) dostane po cooldownu **novou úlohu `#237`
s `attempts=0`** a smyčka se opakuje každé 3 h.

**A jeden rozchod, který vadou JE:** D1 tvrdí `done` u **`world.map`**
i **`world.nodes`**, ale `.forge/roadmap.json` má u obou `done: false`
a `scripts/world.gd` má v `origin/main` **0 bajtů**. Conductor `done` věří →
**`world.nodes` už nikdy nevydá.** Granule, jejíž práce v repu není, je
v řidici vrstvě navěky uzavřená.

**(g) Dvě chyby harnessu, které znehodnocují měření modelů.**

**(g1) Brána parsování běží PŘED importem assetů.** `agent.yml:264`
(`Kontrola parsování (rychlá brána)`) je **před** `:371` (`Import assetů`).
`.godot/` je v `.gitignore`, takže v čerstvém checkoutu **není cache globálních
`class_name`** — a každý odkaz na typ z jiného skriptu spadne.
Naměřeno na skutečném výstupu modelu (běh #280): **týž soubor, týž příkaz** →
bez `.godot` **exit 1, 9 parse chyb**; po `godot --import` **exit 0, 0 chyb**.
Ze 32 klasifikovatelných parse-selhání má **26 falešnou chybu na prvním řádku**
hlášení — a model se opravuje podle první hlášky.

**(g2) Rotace modelů pro granule `any` je od 2. 10. mrtvá.** Commit `194735d`
(„*oprava N3: FORGE_ATTEMPT patri na krok spoustajici agenta*") přesunul
`FORGE_ATTEMPT` z kroku *Vyber poskytovatele* do kroku *Spusť agenta* — a tím ho
prvnímu (rozhodujícímu) volání `pick-provider.mjs` sebral.
Naměřeno napříč 316 logy: **krok výběru poskytovatele vidí `FORGE_ATTEMPT`
v 0 případech ze 316**; řádek „pokus č. N – pořadí posunuto" se naposledy
objevil v běhu #262, tedy **před** tím commitem.

Důsledek: **`entity.npc` dostala 18 běhů v řadě (#274…#322) VŠECHNY stejný
model** (mistral/codestral-latest). **Jejích 33 pokusů je statisticky JEDEN
pokus zopakovaný 33×** — a proto z nich nelze vyvozovat, že selhal model,
protože mechanismus, který měl přinést druhý názor, byl 18× vypnutý.
(Pro granule `strong` rotace žije — proto `entity.enemy` modely střídá.)

**(g) Ví se to — a přesto to platí.** Tohle je asi nejužitečnější zjištění
celého auditu. `docs/BRANY-HRY.md` (aktualizovaný **7. 10. 2026**) **sám
popisuje** skoro každou vadu, kterou jsem naměřil:

- `:116` — „*přečíst nelze („kontrola NEPROBĚHLA" není totéž jako „je to
  v pořádku")*"
- `:118` — „*mrtvé větve: `world.gd` se při migraci smazal, takže kontroly,
  které na něj sahají, se už nikdy nespustí*"
- `:90` — „*26 řádků s `has_method` (39 výskytů — naměřeno 7. 10. 2026)*"
- `:73` — „*animace chůze v projektu není – přeskočeno*"

**Diagnóza je tedy vynikající. Chybí vynucení.** Stejný vzor se opakuje na všech
úrovních:

| Kde je znalost | Kde chybí vynucení |
|---|---|
| `docs/BRANY-HRY.md` popisuje slepá místa | brány jsou zelené dál |
| `JAK-PSAT…` §2 žádá tvar dat a přijímací kritérium | smlouvy mají tvar dat **3 z 18** |
| `ARCHITEKTURA.md` žádá `model: strong` nad 60 řádků | kód to **nespojuje** — 5 granul to porušuje |
| roadmapa má `acceptance` u všech 22 granul | **0 čtenářů v kódu** |
| `NAVRH-ORCHESTRA-NG.md` §8.4 navrhuje vynucení | je to **návrh, ne stav** |
| `lint-roadmapa.py` vady najde | skončí **`exit 0`** a v CI hry se nespouští |

> **Harness není neinformovaný. Harness je neozbrojený.** Ví, co je špatně,
> napsal to a **nemá nic, co by to vymohlo** — protože všechna vynucení, která
> má, jsou v **cizím repu** (orchestra), ne v tom, kde se pracuje.

### 4.6 Empirický závěr o slabých modelech

Naměřeno ze **všech 323 job-logů** workflow `agent.yml` (GitHub API, 29. 9. – 7. 10. 2026):

| | běhů | `success` | úspěšnost |
|---|---|---|---|
| celé dějiny | 323 | 34 | 10,5 % |
| **éra roadmapy hry** (běhy s `FORGE_GRAIN`) | **114** | **14** | **12,3 %** |

**Per granule — a tohle je jádro odpovědi:**

| granule | znaků zadání | běhů | úspěch |
|---|---|---|---|
| **`entity.npc`** | **211** | **33** | **0 %** |
| **`entity.enemy`** | **278** | **25** | **0 %** |
| `sim.offline` | 407 | 2 | 50 % |
| `sim.crafting` | 530 | 12 | 8 % |
| `persist.save.state` | 989 | 5 | 20 % |
| `entity.player.api` | 1 362 | 3 | 33 % |
| `world.nodes` | 1 805 | 2 | 50 % |

**Dvě granule s nejkratším zadáním jsou přesně ty dvě, které nikdy neprošly.** Dohromady 58 běhů, 0 úspěchů. Delší a konkrétnější zadání procházela.
**15 z 17 granul, které měly úlohu, je dnes hotových.**

**Modely (éra hry):** cerebras/gpt-oss-120b **~25 %** · mistral/codestral **~8 %** ·
groq **~5 %**. Z 14 úspěchů jich 8 udělal cerebras. *(Pozor na interpretaci:
cerebras dostával granule později v DAG, část rozdílu je výběr.)*

**Příčiny 100 selhání éry hry:** parse-error **68** (mistral 47×, cerebras 15×,
groq 6×) · testy **16** · agent nezměnil nic **14** · auto-merge gate 1 ·
**krok PR 1 (infrastruktura, ne model)**.

**Ale dvě z těch porážek nejsou porážky modelu** — viz §4.5 (g1) a (g2):
**26 z 32 parse-selhání má falešnou chybu na prvním řádku** (brána běží před
importem) a **`entity.npc` dostala 18× po sobě tentýž model** (mrtvá rotace).
Jak to shrnuje `POUCENI-A-VZORY.md:759–762`:

> „*Naměřeno: hlavní ztráty nejsou v tom, že model **neumí**, ale v tom, že
> **nedostal** (tvar dat, verzi enginu, soubor v chatu, vejitý prompt) — to jsou
> vady **zadání**, ne modelu.*"

**A odpověď na otázku „zvládnou to hloupější modely" v jedné větě:**
na orchestraci to stačí (15 z 17 granul hotových), ale **tam, kde je zadání
jednou větou a kde navíc selhal mechanismus rotace modelů, je 33 pokusů
statisticky JEDEN pokus** — a to není vlastnost modelu, to je vlastnost zadání
a harnessu.

---

## 5. Doporučení

### P0 — bez tohohle se hra nikdy nespustí jako hra

0. **Srovnat `done` se skutečností v gitu — je to nejlevnější krok s největším
   dopadem.** Čtyři granule mají práci v `main` a `done` nemají (§2.2 V0);
   dvě z nich drží `engine.shell`. Postup: u každé granule, která má `done`
   chybějící, ověřit `git merge-base --is-ancestor <commit PR> HEAD`, a když
   je `True`, zapsat `done: true` + `done_note` s PR a datem.
   **Zároveň to znamená, že `sim.crafting` se nesmí vydat** — je dnes
   v „připraveno" a spálila by běh na práci, která je hotová.
1. **Zrušit `world.map`.** Je mrtvá, vlastní tentýž soubor jako `world.nodes`
   a blokuje kritickou cestu. Buď ji odstranit z roadmapy, nebo ji přepsat na
   `done: true` s odkazem na `world.nodes` — a **v `docs/ARCHITEKTURA.md` §3
   doplnit 4 chybějící granule**, aby dokument a plán říkaly totéž.
   **Nutně před dalším tikem conductora** — obě granule jsou dnes připravené
   a vlastní tentýž soubor.
2. **Dát `engine.shell` průchod.** Dokud neproběhne, je 10 hotových granulí
   mrtvá knihovna. Pozor: **`entity.enemy` je před `engine.shell` nesplnitelná**
   — `combat.resolve()` potřebuje registr, který vzniká až v `engine.shell`.
   To je **sémantický cyklus v DAG** a je potřeba ho rozseknout (např. dodat
   minimální registr jako součást `engine.shell` a `entity.enemy` vydat až po něm).
3. **Rozhodnout, co je `tests.harness`.** Granule, která vlastní `tests/`, se
   **nemůže sloučit sama** — patří buď do ruční fronty (a být to napsané), nebo
   se má vzdát vlastnictví testů ve prospěch člověka.
4. **Opravit dvě živé vady v kódu, které dnes dělají hru nehratelnou i kdyby se
   komponenty zapojily:**
   - **`economy.price()` vrací `0` pro každý skutečný předmět** — čte
     `item.material` a `item.quality`, ale `item.gd` má `kvalita` a `items.json`
     nemá ani `material`, ani `quality`. Na skutečném předmětu to skončí
     `SCRIPT ERROR` a `0 * 0 = 0` → **obchod je zdarma**.
   - **`item.repair()` sníží trvanlivost ze 100 na 20** — `items.json`
     deklaruje `durability` 100 (meč) a 150 (zbroj), `item.gd:36` nastaví
     natvrdo **20**. „Oprava" tedy předmět **zničí**.
5. **Opravit bránu parsování — běží PŘED importem assetů.** `agent.yml:264`
   (`Kontrola parsování`) je před `:371` (`Import assetů`) a `.godot/` je
   v `.gitignore`, takže v čerstvém checkoutu není cache globálních `class_name`.
   Naměřeno na skutečném výstupu modelu: **týž soubor, týž příkaz** → bez
   `.godot` `exit 1` a 9 parse chyb; po `--import` `exit 0` a 0 chyb.
   **26 z 32 parse-selhání má falešnou chybu na prvním řádku** — a model se
   opravuje podle první hlášky. Oprava: `Import assetů` **před** bránu.
   **Tohle je nejdřív** — bez toho je každé další měření modelů znehodnocené.
6. **Vrátit `FORGE_ATTEMPT` do kroku „Vyber bezplatného poskytovatele LLM".**
   Commit `194735d` (2. 10.) ho přesunul do kroku spouštějícího agenta, čímž ho
   rozhodujícímu volání `pick-provider.mjs` sebral. Naměřeno napříč 316 logy:
   **krok výběru poskytovatele vidí `FORGE_ATTEMPT` v 0 případech ze 316.**
   Důsledek: **`entity.npc` dostala 18 běhů v řadě tentýž model** — jejích
   33 pokusů je statisticky **jeden pokus zopakovaný 33×**, takže z nich
   **nelze vyvodit, že selhal model**.
7. **Nechat `entity.enemy` proběhnout znovu po opravě infrastruktury.**
   Její **5. pokus spadl na `fatal: could not read Username for
   'https://github.com'` v kroku PR — a testy přitom byly zelené (`92/0`)**.
   To není chyba modelu, to je přihlášení (PAT). Stejná třída jako H1/H2:
   spálený pokus, který nic neříká o zadání.
8. **Přepsat zadání `entity.npc` a `entity.enemy` podle vzoru `world.nodes`.**
   Jsou to **jediné dvě granule, které nikdy neprošly** (58 běhů, 0 úspěchů) —
   a mají **nejkratší zadání ze všech** (211 a 278 znaků). Doplnit přesně to,
   na čem modely padaly: jaký `extends`, **zákaz deklarovat `position`
   v `Area2D`** (8× `Member "position" redefined`), výslovné typy místo `:=`
   u neotypovaných výrazů (19× `Cannot infer the type`), že služby se berou
   z `get_parent().component(id)` (**v zadání `entity.npc` o registru není ani
   slovo**, přitom celá architektura na registru stojí), že `Economy` je
   `class_name` a `Combat` není, a že `Input.get_string()` v headless hře
   neexistuje.

### P1 — aby plán unesl smlouvy

9. **Zavést `provides`/`consumes` a strukturované `acceptance`** do roadmapy
   (přesně jak navrhuje `NAVRH-ORCHESTRA-NG.md` §8.4). Bez toho se smlouvy
   nemají kam psát a agent je nikdy nedostane.
10. **Přepsat `docs/ARCHITEKTURA.md` podle `JAK-PSAT…` §5.1.** Dnes je hotová
   **3 z 18 smluv** (§2.1–2.3). Chybí datové formáty, definice hotovo
   (v `CONVENTIONS.md` je slovo „hotovo" **0×**) a **non-goals** (v `ARCHITEKTURA.md`
   **0×**) — a non-goals jsou přesně to, co má zabránit druhému číslu mřížky.
   **Tuhle práci nedělat v session, která opravuje kód** (`AGENTS.md`).
   Zároveň **srovnat smluvní jména s kódem**: dokument slibuje `get(attr)`,
   `get(skill)`, `trade(player, item)` a `component(name)` — kód má `hodnota()`,
   `buy/sell/gold` a `game.gd` registr **vůbec nemá**.
11. **Přidat `model: strong` pěti granulím**, které mají `size_lines > 60`
   (`world.level` 300, `sim.combat` 130, `sim.mining` 80, `persist.save` 100,
   `ui.hud` 100) — nebo jim limit snížit.
12. **Srovnat `size_lines` s realitou.** Pět granul s prací v `main` už svůj
   deklarovaný limit překračuje (`entity.player` 191>120, `entity.player.api`
   191>180, `persist.save` 150>100, `persist.save.state` 150>140,
   `tests.harness` 1406>1200). Deklarace je vstup pro gate auto-merge — když
   neodpovídá, je každý další odhad velikosti špatný.

### P2 — aby zadání zvládl slabý model

13. **Dát agentovi design.** Nejbližší cestou je **přidat `docs/ARCHITEKTURA.md`
   do `--read`** v `agent.yml` — nebo ještě lépe **generovat `prompt` ze schématu**
   (což metodika žádá a praxe nedělá: 22 ručních próz).
14. **Zavést „feasibility před dispatchem"** — priorita 1 podle
   `POUCENI-A-VZORY.md` §10.2. Konkrétně: **kontrola, že každá smlouva, kterou
   granule spotřebovává, existuje v `main` a jde zavolat.** `entity.enemy`
   by se pak nevydala pětkrát.
15. **Opravit tři nepravdivá tvrzení v trvalých pravidlech** — ne přepsáním
    (historie se needitue), ale **označením „ve svém čase správná"** a doplněním
    dnešního stavu: `AGENTS.md:108–110` (`"cíl mrtev"` → dnes `"target dead"`),
    `CONVENTIONS.md:273` (26 → 91 kontrol), `CONVENTIONS.md:252` (`_safe_spot`
    neexistuje) a `AGENTS.md:91` (DESIGN.md už není zdroj pravdy).
    **Navíc:** `docs/ARCHITEKTURA.md` je „jediný závazný" a chybí v něm
    **4 granule z 22**; tvrdí „18 granulí v 6 vlnách" (je **22 v 5 vlnách**),
    „13 granulí na `<= 60`" (je **8**) a „16 závislostí `engine.shell`" (je **19**).
16. **Odstranit z `CONVENTIONS.md` §3 radu „nepřidávej nové soubory"** — je
    v přímém rozporu s architekturou, kterou má agent stavět.

### P3 — aby zelená něco znamenala

17. **Zrušit tiché přeskakování v testech.** **41 ze 132 kontrol (31 %) se dnes
    nikdy nespustí** a jen 3 to ohlásí. Soubor, který součástí hry být MÁ, musí
    při nenačtení **SELHAT** — dnes smazání `attributes.gd` i `economy.gd`
    (obě `done`) projde se zeleným CI.
18. **Doplnit funkční kontroly `sim.economy` a `sim.assist`** — obě jsou `done`
    a obě mají jen `has_method`, přestože stejný soubor o 200 řádků výš má
    komentář, že to nestačí. A **nahradit atrapy skutečnými komponentami**
    v bloku ukládání/HUDu (`run_tests.gd:854–931`) — kvůli nim zůstane zelená
    i mutace `economy.gold()` vracející 999.
19. **`check-wiring.py` nesmí počítat `tests/`** jako důkaz použití produkčním
    kódem — jinak zůstane slepý přesně na „funguje to, ale nic to nedělá",
    což je vada, kterou má hledat. Naměřeno: přesun `tests/` mimo cíl zvedne
    počet hlášených mrtvých funkcí z **4 na 13**.

### P4 — aby se metodika přestala učit jen z minulosti

20. **Oživit `JAK-PSAT-DESIGN-A-PLANOVAT-VYVOJ.md`.** Je to jediná metodika
    designu a plánování, kterou harness má, je označená jako **rostoucí** a její
    §7 nařizuje každé session doplnit naměřený případ. **Od 2. 10. 2026 nemá ani
    jeden nový případ.** Tenhle audit je sám o sobě **~12 nových naměřených
    případů** (viz §2.2 V1–V8, §3.2, §4.5) — patří do jeho §4.
    **Zároveň je to otevřený bod celé stanice**:
    `OTEVRENA-TEMATA.md:106` — „*DOKONČIT REVIZI SKILLU `game-developer` +
    PŘEPSAT DESIGN UO-SHADOWS*" — je **nezaškrtnutý** a má stále stav
    „6 případů, 1. sezení".

---

## 6. Co čeká na tebe (rozhodnutí, která nejsou na agentovi)

| # | Rozhodnutí | Proč to není na agentovi | Cena | Doporučení | Cesta zpět |
|---|---|---|---|---|---|
| 1 | **Zrušit `world.map` z roadmapy** | mění rozsah plánu (co se má dělat) | 0 (granule je mrtvá) | zrušit | `git revert` commitu roadmapy |
| 2 | **Přepsat `docs/ARCHITEKTURA.md` na smlouvy s tvarem dat** | mění závazný dokument hry; je to práce na samostatnou session | jeden večer | ano, podle §5.1 | soubor je v gitu |
| 3 | **Dopsat game design: jak se hra hraje** | **to je ta chybějící část zadání** — ovládání, prvních 5 minut, UI, úspěch | 1–2 h lidsky | ano — bez toho nemá smysl psát další granule | nový `docs/HRANI.md` |
| 4 | **Zavést `provides`/`consumes` do orchestra** | mění orchestra (jiný repozitář, jiný projekt) | dny | nejdřív návrh NG | orchestra má vlastní git |
| 5 | **Doplnit `JAK-PSAT…` o naměřené případy z tohoto auditu** | dokument leží v **jiném repu** (`forge-orchestra`) — zápis do cizího projektu | hodina | ano, jeho §7 to nařizuje | `git revert` v orchestra |

**To třetí je jádro.** Ostatní vady se dají opravit v plánu. Chybějící odpověď
na „co má hráč dělat a jak pozná, že si vede dobře" se opravit nedá — a je to
**jediná věc, kterou plán nemůže vymyslet za tebe**.

---

## 7. Metody, meze a nezávislé ověření

### 7.1 Čím byla která čísla naměřena

| Číslo | Postup |
|---|---|
| 22 granul, 13 `done`, visící závislosti, kolize `owns`, délky zadání | Python nad `.forge/roadmap.json` |
| řádky souborů | `git show HEAD:<soubor>` + `splitlines()` — **autorita je blob** |
| „práce je v `main`, ale není `done`" | `git merge-base --is-ancestor <commit> HEAD` |
| `provides`/`consumes`/`acceptance` = 0 čtenářů | Python walk nad `conductor/`, `repo/`, `tools/` s vyloučením dokumentace |
| 91 kontrol / 0 selhání | `Godot --headless --script res://tests/run_tests.gd` |
| smazání souboru hotové granule | kopie repa → `Remove-Item` → testy (baseline 91/0, po smazání 89/0 a 88/0, `exit 0`) |
| mutace v hotové komponentě | kopie repa, 20 mutací, před každou revert z originálu + ověření, že mutace proběhla |
| 41 ze 132 kontrol se nikdy nespustí | statická analýza `_check(` proti obalujícím `if`/`for` + empirický počet spuštěných |
| co hra dělá | `Godot --headless --quit-after`, snímek přes `--write-movie` |
| nasazení | Node `fetch` HEAD na `index.png` + GitHub API na `commits/main` |
| 323 běhů, per-granule úspěšnost, kdo selhal a čím | GitHub API `actions/workflows/370048079/runs` (4 strany) + všech 323 job-logů, klasifikace podle spadlého **kroku** |
| `/roadmap` = 21 řádků | přímý dotaz na endpoint (`GET /roadmap`) s hlavičkou `x-forge-secret`, ne přes `status.mjs` |
| pořadí kroků v CI | `agent.yml`: `Kontrola parsování` ř. 264, `Import assetů` ř. 371 |

### 7.2 Co naměřeno NEBYLO (a je to vidět)

- **Běhy orchestra jsem nepřeměřoval.** Úspěšnost modelů (11,3 %, 240 běhů) je
  **citace** z analýz orchestra s datem, ne moje měření.
- **Nepouštěl jsem `vision.mjs`** (potřebuje klíč z GitHub Secrets; v CI
  neblokuje) ani `baseline.py`.
- **Linter plánu je poradní** — spustil jsem ho, jeho `exit 0` nic neznamená.
- **Jedna mutace z 20 se neprovedla** (vzor nenalezen) — je vedená jako
  **nezměřená**, ne jako „prošlo".
- **`verify-level-render.py`** dal `207/208 = 99,5 %` (1 chyba `(21,14) brick
  vs dirt`) — to je převzato z paralelního auditu, sám jsem ho nespouštěl.

### 7.3 Nezávislé ověření

Tenhle audit vznikl **třikrát, nezávisle**. Tři měření (toto, `_audit-uos`
a `_free-models-analyza`) dospěla ke **shodným číslům** u DAG, běhů bran, řádků
i délek promptů. Dvě z nich přinesla to, co jsem sám neměl:

- **mutační sondu** (7 z 20 mutací zůstane zelených) a **sondu „smaž soubor"**
  (9 z 20 smazání projde tiše) — **přeměřil jsem je sám** v kopii repa;
- **empirický záznam 323 běhů** s rozlišením „kde selhal model" vs. „kde selhal
  harness" — a **vyvrácení mého vlastního tvrzení** o prázdné roadmapě.

Podle `AGENTS.md` („autor není nezávislý reviewer") je tohle přesně ten postup,
který má být: **tři měření, jeden závěr — a oprava toho, co se nepotvrdilo**.

### 7.4 Oprava vlastního tvrzení (záznam, ne přepis)

**Tenhle audit v první verzi tvrdil, že `/roadmap` conductora je „prázdná", a
stavěl na tom, že orchestra nevidí žádnou práci.** To bylo **nepravdivé** a
stálo to za to zapsat, protože je to přesně past, kterou metodika popisuje.

- **Co jsem udělal:** přečetl jsem výstup `node tools\status.mjs`, který vypsal
  `ROADMAP /roadmap` → „(prazdna)".
- **Co jsem měl udělat:** zeptat se **endpointu**, ne nástroje.
- **Naměřeno 7. 10. 2026:** `GET /roadmap` → HTTP 200, klíč `roadmap`,
  **21 řádků** (`done: 19, failed: 1, queued: 1`).
- **Příčina:** `tools/status.mjs:81` čte `rm.json.items || rm.json.grains`;
  conductor vrací `{roadmap: […]}`. **Nástroj tiše vrátí `[]` a vypíše
  „(prazdna)"** — chyba nástroje, ne stavu.
- **Kde je oprava:** §4.5 (f) a (g). Původní text je **nahrazen** tam, kde
  tvrdil nepravdu, a toto je záznam o tom, co se změnilo a proč.

**Poučení, které platí i na tenhle dokument:** *když výsledek vypadá jako
„nic tam není", první otázka je „proběhlo to měření?"* — a druhá je
**„ptám se správného místa?"**. Nástroj je měřidlo; měřidlo se ověřuje.
