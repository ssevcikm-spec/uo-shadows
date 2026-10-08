# Session Handoff — revize vize `uo-shadows` (5 kol dialogu s uživatelem) uzavřena

> **⚠ SPOTŘEBOVÁNO 8. 10. 2026 druhou session.** Zadání, které tenhle handoff
> předával (`napiš GDD, ADD a TDD`), je **splněné**: vznikly `docs/GDD.md`,
> `docs/ADD.md`, `docs/TDD.md`, `AGENTS.md` má přepsané odkazy a je hotový
> **návrh** roadmapy (`_analyza/NAVRH-ROADMAPY-M0-M6.md` +
> `_analyza/roadmap-navrh.json`) — **k odsouhlasení, ne aplikovaný**.
> **Dnešní stav není tenhle soubor** — je v `docs/GDD.md` (design),
> `docs/TDD.md` (technika), `docs/ADD.md` (vzhled) a v „Co zbývá“ níž.
> Tenhle soubor zůstává jako **záznam předání** (needituje se zpětně).
>
> **Co tenhle soubor JE:** **předávací artefakt** pro session, která začne
> v čistém kontextu. Není to stav projektu (ten je
> v `_analyza/DESIGN-REVIZE-2.md`) — je to „kde jsem přestal a co dělat dál".
>
> **Napsáno:** 8. 10. 2026 session `session-70e0de90-c89c-404e-aa73-5cfe4aed0f7e`
> (kontext 355 k/1 M, 0 kompakcí, cache-hit 99,23 % — session byla zdravá,
> větvila se kvůli **změně tématu**, ne kvůli tokenům).

## Where it started

Uživatel zadal `ZADANI-REVIZE-VIZE.md`: projít s ním celou vizi hry po vrstvách
(pět kol) a vyladit ji tak, aby se podle ní dal napsat GDD, ADD a TDD **bez
dohadování**. Projekt: `E:\Workspaces\uo-shadows` (Godot 4.7 hra, kterou vyvíjí
cloudová orchestra `forge-orchestra`). Uživatel nečte kód — rozumí konceptu
v lidském jazyce, takže otázky musely být v jazyce zážitku, ne implementace.

## Decisions locked + what shipped

**Všech pět kol je rozhodnutých** (u každého rozhodnutí je v dokumentu **cena**):

- **Záměr**: živý izometrický sandbox, hráč si vybere roli (řemeslník,
  obchodník, válečník, dobrodruh, hraničář), roste v ní a svět na to reaguje.
- **Pět pilířů jako POCITY**, hlavní rozhodčí je **`P2`** („rostu tím, co dělám
  — a je to vidět") → čísla se musí ve hře ukazovat brzy.
- **Hlavní smyčka na 8 vět** + tři pravidla, která vypadla ze stres testu:
  těžba má hloubku (směs, delší těžba = vzácnější), poptávka světa je tříděná
  (odpad / recyklovatelné / situační) a mění se, hnací silou je cíl s číslem.
- **Svět**: **žádné MMO** — solo se **simulovaným světem** (infestace +
  zásobenost 0–100, ceny z nich), ale architektura se udělá tak, aby se
  **2–4 hráči dali přidat později** (oddělená simulace, pevný tik, stav jako
  data). Persistentní sdílený svět odložen.
- **Rozsah `M`**: 11 materiálů (se vzácnými složkami), 7 předmětů, 3 nestvůry,
  8 receptů, 6 dovedností, vesnice + důl + les + pole. Odhad +20–30 granulí.
- **Non-goals**: 11 výslovných zákazů (mj. lektvary a alchymie mimo MVP —
  tím se srovnaly tři rozporné dokumenty).
- **Míra úspěchu `V1`–`V8`** (každá s důkazem), **prvních 5 minut** jako scénář.
- **Technika**: pevný tik 50 ms, kořen s registrem komponent, simulace oddělená
  od zobrazení; 60 FPS a simulace < 2 ms/tik; klíče anglicky, texty česky.
- **Plán**: milníky `M0`–`M6` jako hratelné stavy (grafika **až nakonec**);
  definice hotovo ve **čtyřech** podmínkách.
- **Opravena tři nepravdivá tvrzení v pravidlech hry** (uživatel to výslovně
  povolil): `AGENTS.md` §Jazyk, `CONVENTIONS.md` §4 a §7.

**Co se neprovedlo a je to zapsané jako odchylka:** uživatel **nepřevyprávěl**
hlavní smyčku zpět svými slovy (kritérium zadání §7) — místo toho odpověděl na
tři krajní případy, což je jiná a tady **silnější** metoda validace.

## Key files for next session

- `E:\Workspaces\uo-shadows\ZADANI-GDD-ADD-TDD.md` — **začni tady.** Zadání pro
  psaní GDD/ADD/TDD + mapa „které rozhodnutí jde do kterého dokumentu".
- `E:\Workspaces\uo-shadows\_analyza\DESIGN-REVIZE-2.md` — **zdroj rozhodnutí**
  (§1 ověřená fakta, §2–§5 záměr a zážitek, §11 svět a hráči, §12 míra úspěchu
  a non-goals, §13 mechaniky a obsah, §14 technika, §15 plán a brány, §16 co dál).
- `E:\Workspaces\uo-shadows\_analyza\REKONSTRUKCE-ADD-TDD-GDD.md` — co z ADD,
  TDD a GDD existuje a co ne (stav k `3b34b0e`).
- `E:\Workspaces\uo-shadows\_analyza\AUDIT-PLANU-A-DESIGNU.md` — naměřené vady
  plánu a designu (1033 řádků; čti oddíly, ne celé).
- `E:\Workspaces\uo-shadows\docs\BRANY-HRY.md` — co která brána měří a **kde má
  slepá místa** (povinné pro TDD).
- `E:\Workspaces\uo-shadows\assets\spec.json` — strojová podoba ADD (rozměry,
  role, vrstvy, 6 bran, styl se zákazy).
- `C:\Users\Ssevc\Local-Deepseek\OTEVRENA-TEMATA.md` — ledger stanice; téma
  „REVIZE VIZE `uo-shadows`" má stav po každém kole.
- Handoff artifact: `E:\Workspaces\uo-shadows\HANDOFF.md` (tento soubor).

## Environment

- Working directory: `E:\Workspaces\uo-shadows`
- Orchestra (jiné repo, sourozenec): `E:\Workspaces\forge-orchestra`
- Godot: `E:\Tools\godot\Godot_v4.7.2-stable_win64_console.exe` (nespouštěl se)
- Model / provider: deepseek-flash (DSH), souborová politika `danger-full-access`

## Objective to re-arm

- Objective: **none** — v téhle session nebyl vytvořen žádný `goal`.
  Práce byla vedena zadáním `ZADANI-REVIZE-VIZE.md`, které je splněné.

## Background processes

- none (žádný job jsem nezakládal; nic neběží)

## Subagents

- none (celou práci dělala tahle session; žádný subagent ani teammate)

## Running state

- Dev servery / porty: none (spuštěné žádné)
- Worktrees / větve: none — jedna pracovní kopie, větev `main`
- **Git (ověřeno živě 8. 10. 2026, druhá session):** `HEAD` = `945cba8`,
  `origin/main` = `945cba8`, **0 nepushnutých commitů**. **Nové dokumenty jsou
  zatím NECOMMITNUTÉ** (`docs/GDD.md`, `docs/ADD.md`, `docs/TDD.md`,
  `_analyza/NAVRH-ROADMAPY-M0-M6.md`, `_analyza/roadmap-navrh.json`,
  `_analyza/over-dokumenty.py`) + upravené `AGENTS.md`, `docs/DESIGN.md`,
  `docs/ARCHITEKTURA.md`, `HANDOFF.md`. Beze změny zůstala `_acl-recovery/`
  (není moje; otevřené téma `O-3`).

## Verification — how to confirm things still work

```powershell
# stav repa (main = 5fe6d8e nebo novější, jen _acl-recovery/ untracked)
git -C E:\Workspaces\uo-shadows log --oneline -3
git -C E:\Workspaces\uo-shadows status --short

# zdroj rozhodnutí je úplný (má vyjít §1 … §16)
Select-String -Path E:\Workspaces\uo-shadows\_analyza\DESIGN-REVIZE-2.md -Pattern '^## '

# tři opravy pravidel: grepy najdou JEN opravné poznámky, ne tvrzení
Select-String -Path E:\Workspaces\uo-shadows\CONVENTIONS.md -Pattern '_safe_spot'
Select-String -Path E:\Workspaces\uo-shadows\AGENTS.md -Pattern 'target dead'

# stav orchestry (cíle, ne řídicího systému)
node -e "(async()=>{const r=await fetch('https://forge-conductor.ssevcikm.workers.dev/health');console.log(JSON.stringify(await r.json(),null,1));})()"
# → main_ci = success, ale forge.ok = false (20 selhání v řadě) a /roadmap prázdná
```

## Deferred + open questions

- **Deferred:** čím platí řemeslník, když ne grindem (`DESIGN-REVIZE-2.md` §13.8)
  — uživatel sám řekl „ještě nevím"; patří do GDD jako otevřený bod, ne jako
  tichá volba agenta.
- **Deferred:** sjednotit název hry `uo-sandbox` → `uo-shadows` (rozhodnuto,
  ale mění `project.godot` — samostatný úkol, ne mimochodem).
- **Deferred:** brány nad dokumentací (`check-docs-refs`, `check-zadani`) a třetí
  stav „neměřeno" (`exit 2`) — až budou dokumenty, dnes by neměly co měřit.
- **Open:** `_acl-recovery/` v rootu herního repa — do repa, nebo pryč?
- **Open:** **`Forge agent` je červený** (20 selhání v řadě, naposledy 8. 10.
  11:39; conductor byl nasazen 13:07, takže se neví, jestli to opravil)
  a **roadmapa conductora je prázdná** — orchestra tedy nemá co vydávat.
  Příčina **není změřená**. Nezávislé na psaní dokumentů, ale blokuje to stavbu
  podle nového plánu — patří do **vlastní session**.
- **Open:** uživatel pracuje na červeném `Forge agent` v jiné session (zapsáno
  v ledgeru stanice) — nezačínat to dvakrát.

## Pick up here

> **✅ SPLNĚNO 8. 10. 2026 (druhá session).** Text níž je **záznam, co se
> zadalO** — ne dnešní stav. Dnešní stav je v tabulkách pod ním.

Přečti `E:\Workspaces\uo-shadows\ZADANI-GDD-ADD-TDD.md` a **napiš
`docs/GDD.md`** podle mapy v jeho §2 — bere se to z `DESIGN-REVIZE-2.md` §2–§5,
§12 a §13, nic se nedohaduje. ADD a TDD až po něm; `.forge/roadmap.json` teprve
po všech třech.

### Co je hotové (druhá session, 8. 10. 2026)

| # | Výstup | Kde | Jak je ověřený |
|---|---|---|---|
| 1 | **GDD** (495 řádků) — záměr, pilíře, smyčka, `V1`–`V8`, prvních 5 minut, ovládání, UI, svět, mechaniky se vzorci, obsah, non-goals, milníky | `docs/GDD.md` | `_analyza/over-dokumenty.py`: 92 tvrzení proti zdrojům, 0 FAIL |
| 2 | **ADD** (392 řádků) — lidská vrstva k `spec.json`, katalog assetů, pipeline Blender/SDXL, `A-1` odloženo, zvuk, licence | `docs/ADD.md` | tamtéž + naměřeno, že `assets/sprites/player.png` je **pixel-identický** složenině 4 vrstev `d0_f1` |
| 3 | **TDD** (796 řádků) — architektura běhu, vrstvy, **18 smluv s tvarem dat**, formáty, vlastnictví stavu, výkon, ukládání, chyby, jazyk, známé vady | `docs/TDD.md` | tamtéž; navíc `check-schema.py` a `check-wiring.py` zelené |
| 4 | **`AGENTS.md`** — přepsané odkazy („co hra je“ → GDD, „architektura a smlouvy“ → TDD, nově ADD); stará nepravdivá věta označena | `AGENTS.md` | `git diff` |
| 5 | **Hlavičky historie** — `DESIGN.md` a `ARCHITEKTURA.md` říkají, čím byly nahrazeny | `docs/DESIGN.md`, `docs/ARCHITEKTURA.md` | `git diff` |
| 6 | **Návrh roadmapy** `M0`–`M6` — **aplikovaný** (21 granulí; 3 vyřazené, 2 parkované, `done` u 3 srovnáno s gitem) | `.forge/roadmap.json`, `_analyza/NAVRH-ROADMAPY-M0-M6.md` | JSON validní, žádné visící závislosti, pravidlo „dva grains, jeden soubor“ drží; `_analyza/roadmap-navrh.json` je historický artefakt |
| 7 | **Ověřovací nástroj** dokumentů (kandidát na `check-docs-refs`) včetně sabotéra | `_analyza/over-dokumenty.py` | `--selftest`: **8/8 mutací chyceno** |

**Zásadní nález druhé session (zpřesňuje tvrzení revize):** „hra 258 spritů
nepoužívá“ **není přesné** — `assets/sprites/player.png` a `npc.png` jsou
**pixel-identické** se složením vrstev `d0_f1` z Blenderu, takže hra zobrazuje
**1 frame ze 128, zploštěný**, ne cizí grafiku. Zapsáno v `docs/ADD.md` §3.

### Co zbývá (a co z toho neudělá agent sám)

| # | Co | Stav / kdo |
|---|---|---|
| **A** | **Návrh roadmapy** — **ODSOUHLASENO A APLIKOVÁNO 8. 10. 2026**: `.forge/roadmap.json` má 21 granulí (15 `done`, `world.nodes` false), **vydatelná hned je `engine.registry`**; 3 zombie granule vyřazeny, `entity.npc`/`entity.enemy` parkovány do `M4`/`M5` | ✅ hotovo (`_analyza/NAVRH-ROADMAPY-M0-M6.md` je záznam) |
| **B** | **`Forge agent` je červený** (20 selhání v řadě) a roadmapa conductora je prázdná — bez toho orchestra nic nevydá | **vlastní session**, příčina neměřená |
| **C** | **`O-1` — čím platí řemeslník** (palivo / opotřebení / zmetkovost?) | ✅ **ROZHODNUTO 8. 10. 2026** („zatím palivo, opotřebení, zmetkovost a můžeme rozvíjet časem“) — zapsáno v `docs/GDD.md` §9.2, `docs/TDD.md` §3.11 a `DESIGN-REVIZE-2.md` §17 |
| **D** | **`O-5` — české klíče** `tezba`/`kovani_mece` vs. pravidlo `R-3` | samostatný úkol (mění kód i data) |
| **E** | **`O-2` — název hry** `uo-sandbox` → `uo-shadows` | ✅ **PROVEDENO 8. 10. 2026**: `project.godot`, `assets/spec.json`, `export_presets.cfg` = `uo-shadows`. ⚠ `user://` se přesunul na `…\app_userdata\uo-shadows\` — ve starém adresáři **žádný `save.cfg` nebyl** (naměřeno), takže nic nezmizelo |
| **F** | **`O-3` — `_acl-recovery/`** v rootu repa | rozhoduje uživatel |
| **G** | **`O-4` — brány nad dokumentací** (`check-docs-refs`, třetí stav `exit 2`) | základ existuje: `_analyza/over-dokumenty.py`; do `.forge/` patří až po rozhodnutí |
| **H** | **Úklid před výměnou roadmapy** — srovnat `done` se skutečností v gitu, vyřadit 3 zombie granule, doplnit `provides`/`consumes` | návrh §5 tamtéž |
| **I** | **Ledger stanice** `C:\Users\Ssevc\Local-Deepseek\OTEVRENA-TEMATA.md` — téma „REVIZE VIZE“ má stav po kolech, ne po dokumentech | mimo workspace (zápis potřebuje oprávnění) |

### Jak si stav ověřit (5 minut)

```powershell
cd E:\Workspaces\uo-shadows
python _analyza\over-dokumenty.py             # 94 kontrol, 0 FAIL, exit 0
python _analyza\over-dokumenty.py --selftest  # sabotér: 9/9 chyceno
python .forge\check-schema.py .               # tvrdá brána: exit 0
python .forge\check-wiring.py .               # 85 funkcí v 15 souborech, exit 0
git status --short ; git diff --stat
```
