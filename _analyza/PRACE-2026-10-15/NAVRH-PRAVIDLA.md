# NÁVRH: opravy `CONVENTIONS.md` a `AGENTS.md` (k rozhodnutí uživatele)

> **Co tenhle soubor JE:** **návrh k aplikaci** — přesné znění oprav dvou souborů,
> které jsou **trvalá pravidla** (`CONVENTIONS.md` dostává agent orchestry přes
> `--read`, `AGENTS.md` dostává každá DSH session). Podle pravidla stanice
> („měnit trvalá pravidla patří uživateli") je **lead session sám neaplikoval**.
>
> **Vzniklo:** 15. 10. 2026 (session, která přepracovává design dokumenty).
> **Stav:** **neaplikováno** — čeká na rozhodnutí. Aplikace = zkopírovat znění níž.
> **Proč to není jen formalita:** obě opravy se týkají **nepravdivých tvrzení
> o dnešním stavu**, a `CONVENTIONS.md` je **jediný dokument, který agent orchestry
> skutečně dostane** (`.github/workflows/agent.yml:227`). Nepravdivé pravidlo
> v něm tedy **aktivně brání správnému postupu** — což je dražší než chybějící
> informace (naměřeno: `AGENTS.md` sám to tak formuluje).

---

## 1. `CONVENTIONS.md` §2 — „ty sám Godot nemáš" (nepravda)

**Dnes** (`CONVENTIONS.md:223–227`):

> ## 2. Když se skript hry nenačte, poznáš to hned
>
> Testy to řeknou („skript hry jde načíst"), ale **spustit si je musí CI** – ty
> sám Godot nemáš. Proto: změnu dělej malou, v jednom souboru, a nikdy
> nepřepisuj celý soubor, když měníš pár řádků.

**Naměřeno 15. 10. 2026:** `E:\Tools\godot\Godot_v4.7.2-stable_win64_console.exe`
**existuje** (`Test-Path` = `True`) a `AGENTS.md:40–49` dává přesný příkaz, jak
testy spustit lokálně. Pravidlo tedy **popírá vlastní nástroj stanice**.
(„Ve svém čase správné" být mohlo — ale dnes je nepravdivé.)

**Navržené znění (náhrada celého odstavce):**

```markdown
Testy to řeknou („skript hry jde načíst"). Spustíš je **lokálně** — Godot na
stanici je (`E:\Tools\godot\Godot_v4.7.2-stable_win64_console.exe`) a přesný
příkaz je v `AGENTS.md` §„Jak spustit hru a testy"; v CI běží na každý PR.
Výsledek se čte z řádku `[test] N kontrol, M selhání`, **ne z exit kódu**.
Proto: změnu dělej malou, v jednom souboru, a nikdy nepřepisuj celý soubor,
když měníš pár řádků.
```

## 2. `CONVENTIONS.md` §3 — „nepřidávej nové soubory" (jde proti `M0`)

**Dnes** (`CONVENTIONS.md:229–237`, poslední odrážka):

> ## 3. Hra je postavená programově
>
> Celá scéna se staví v `scripts/game.gd` (uzly se vytvářejí v kódu, žádné
> ukládané `.tscn` kromě `main.tscn`). Když přidáváš uzel:
>
> - dej mu `name` (testy a hledání podle skupin se o to opírají),
> - přidej ho do skupiny (`coin`, `enemy`, `chest`, `player`), když se s ním má
>   něco dít,
> - **nepřidávej nové soubory, když to jde udělat v `scripts/game.gd`.**

**Naměřeno:** cíl `M0` je přesně opačný — `GDD.md:460` „**přepis `game.gd`
(monolit) na registr** (`engine.shell`)". Už se to děje: `799481d` přidal
`scripts/registry.gd` (150 řádků, `TICK_MS`, fronty příkazů a událostí).
Pravidlo „nepřidávej soubory" by agenta poslalo **proti jeho vlastnímu zadání**.

**Navržené znění (náhrada poslední odrážky):**

```markdown
- **nová komponenta = nový soubor** v `scripts/` (např. `scripts/registry.gd`),
  zaregistrovaný přes `component(id)` — viz `docs/TDD.md` §1.1 a §3.19;
  do `scripts/game.gd` patří **jen sestavení scény a tik** (monolit se rozebírá,
  cíl `M0`). Když přidáváš uzel, drž se dvou odrážek výš.
```

## 3. `CONVENTIONS.md` §4 — vlastnost `cell` na `Level` neexistuje

**Dnes** (`CONVENTIONS.md:249`): `| spawn_cell -> Vector2i, width, height, cell | rozměry mřížky |`

**Naměřeno:** `scripts/level.gd:44–45` má `cell_w` a `cell_h`; vlastnost `cell`
na `Level` **není** (je jen v `main.json` a ignoruje se — `TDD.md:588–592`).

**Navržené znění řádku:**

```markdown
| `spawn_cell -> Vector2i`, `width`, `height`, `cell_w`, `cell_h` | rozměry mřížky |
```

## 4. `CONVENTIONS.md` §7 — zákaz opisovat čísla vs. praxe

**Dnes** (`CONVENTIONS.md:278–281`): „…**do dokumentu se neopisuje**, protože zestará…"

**Naměřeno:** `AGENTS.md:85–86`, `docs/TDD.md:742` i `docs/BRANY-HRY.md` čísla
**opisují** — a **správně** (běh hlásí 113 kontrol, staticky 154 volání `_check(`;
obojí sedí). Pravidlo a praxe si tedy odporují; chyba je v pravidle.

**Navržené znění (náhrada věty):**

```markdown
**Počet kontrol se ČTE z výstupu běhu** (`[test] N kontrol, M selhání`) a do
dokumentu se smí opsat **jen s datem a se zdrojem** (odkud bylo číslo přečteno) —
bez toho zestará a nikdo nepozná, co platí. Naměřeno 15. 10. 2026: běh hlásí
**113 kontrol** (staticky je v souboru 154 volání `_check(` — to není totéž).
```

## 5. `CONVENTIONS.md` — chybí hlavička (a je to soubor, který agent dostane)

**Dnes:** soubor začíná větou „Tenhle soubor je **jen ke čtení**…" — nemá druh
dokumentu, datum, vlastníka ani „odkud brát stav".

**Navržené znění (vložit na začátek):**

```markdown
> **Co tenhle dokument JE:** **poučky pro agenta**, který píše granule hry
> `uo-shadows` — jak psát GDScript pro Godot 4, co nesmí měnit a jak ověřit
> výsledek. **Není to zdroj pravdy o designu** (to je `docs/GDD.md`) **ani
> o technice** (`docs/TDD.md`).
> **Odkud brát současný stav:** `docs/GDD.md`, `docs/TDD.md`, `docs/BRANY-HRY.md`
> a `.forge/roadmap.json`; tenhle soubor drží jen to, co musí agent vědět **před**
> psaním kódu.
> **Vzniklo:** 30. 9. 2026 (aktualizováno 8. 10. 2026). **Vlastník:** session,
> která mění pravidla hry. **Jak se mění:** přepisuje se celý (je to stav),
> ale historické poznámky „OPRAVENO &lt;datum&gt;" se **doplňují, nemažou**.
```

---

## 6. `AGENTS.md` — tři cílené doplňky (nic se neruší)

**(a) Chybí výjimka k pravidlu jazyka (`R23`).** `AGENTS.md:121–127` zakazuje
ne-ASCII klíče, ale v `assets/data/*.json` **české klíče jsou** (`tezba`,
`kovani_mece`) a `GDD §14.1` (`O-5`) říká, že se **nepřejmenovávají mimochodem**.
Bez věty o výjimce hrozí, že agent „opraví" fungující data.

```markdown
> **Výjimka (`O-5`):** existující české klíče v `assets/data/*.json`
> (`tezba`, `kovani_mece`) se **nepřejmenovávají mimochodem** — přejmenování je
> samostatný úkol (`docs/GDD.md` §14.1 `O-5`).
```

**(b) „Kam pro co" nemá sloupec vrstvy** a chybí v něm čtyři soubory, které
session potřebuje najít: `ZASTAVENO.md` (proč se nevyvíjí), `HANDOFF.md`
(záznam předání), `_analyza/DESIGN-REVIZE-2.md` (zdroj rozhodnutí o designu),
`assets/data/*.json` (obsah hry) a `docs/README.md` (rejstřík dokumentů —
vzniká 15. 10. 2026).

**(c) Doplnit pravidlo o bráně nad dokumentací** — dnes existuje
`_analyza/over-dokumenty.py` (97 kontrol, tři stavy `exit 0/1/2`) a od 15. 10. 2026
**měří i vnitřní soulad dokumentů**:

```markdown
- **Dokumenty se měří jako kód.** `python _analyza\over-dokumenty.py --root .`
  (`exit 0` = vše změřeno · `1` = rozpor se zdrojem nebo mezi dokumenty ·
  `2` = něco zůstalo NEMĚŘENO) a `--selftest` (sabotér: umí brána vůbec selhat?).
  **Nepřepisuj dokument, dokud brána není zelená** — a když hlásí `NEMĚŘENO`,
  není to zelená.
```

---

## 7. Co jsem NEnavrhl (a proč)

- **Přejmenovat dokumenty na číslované** (`01-cil.md`…) — naměřeno: rozbilo by
  **57 odkazů v záznamech** (které se nesmí přepisovat), **30 v plánu**, 1 bránu
  v repu a 2 v orchestraci. Varianta A (zachovat názvy + rejstřík) je levnější
  a nic nerozbije.
- **Přepsat `docs/DESIGN.md` a `docs/ARCHITEKTURA.md`** — jsou to **záznamy
  (historie)**; `ARCHITEKTURA.md` má uvnitř dvě vzájemně se vylučující tvrzení
  o autoritě (`R19`) a správná oprava je **doplnit označení, ne přepsat**.
- **Změnit `.forge/roadmap.json`** — plán je vstup orchestry (jiné repo) a jeho
  změna je **operace**, ne editace souboru; navíc projekt je zastavený.
- **Cokoli v kódu hry** — vady se **zapisují**, neopravují.

## 8. Co by aplikace rozbila (kontrola)

| Riziko | Jak je ošetřeno |
|---|---|
| `over-dokumentaci.py` v orchestraci pinuje texty v `BRANY-HRY.md` | opravy `CONVENTIONS`/`AGENTS` se ho netýkají |
| `AGENTS.md` čte každá session → změna je „publikovaná" | doplňky jsou **aditivní**, nic se neruší; po aplikaci projít `git diff` |
| Rozpor s `docs/GDD.md` (zdroj pravdy o designu) | doplňky se na GDD **odvolávají**, neopisují jeho obsah |
