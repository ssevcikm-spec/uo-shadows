# ZADÁNÍ: napsat GDD, ADD a TDD pro `uo-shadows`

> **Co tenhle dokument JE:** **zadání pro session, která přijde.** Není to stav
> a není to analýza — je to instrukce, co má nová session udělat a co k tomu má
> použít.
>
> **Kdo ho napsal:** session z 8. 10. 2026, která **uzavřela revizi vize**
> (vedla dialog s uživatelem v pěti kolech). Nová session ten dialog nemá —
> proto je tady všechno podstatné vypsané a odkázané.
>
> **Vzniklo:** 8. 10. 2026. **Stav repa při psaní:** `main` = `5fe6d8e`,
> pushnuto (`origin/main` = `HEAD`).
> **Odkud brát stav:** `_analyza/DESIGN-REVIZE-2.md` je **zdroj rozhodnutí**
> (všechna s cenou); tenhle dokument říká, **co z nich napsat kam**.
>
> **Hotovo, když:** existují `docs/GDD.md`, `docs/ADD.md`, `docs/TDD.md`,
> odkazy v `AGENTS.md` ukazují na nové dokumenty — a **žádné tvrzení v nich
> se nemusí dohadovat**, protože má zdroj v rozhodnutí.

---

## 1. Cíl

**Napsat tři dokumenty, ze kterých se dá vygenerovat plán granulí — a ve kterých
se nic nedohaduje.**

Uživatel to řekl 8. 10. 2026 takhle: *„aby se systém a AI pak nemusely hádat."*
Revize vize to zařídila pro **rozhodnutí**; tenhle krok z nich dělá **dokumenty**.

**Pořadí je závazné** (každý se odvozuje z předchozího):

| # | Dokument | Nahradí | Proč v tomhle pořadí |
|---|---|---|---|
| 1 | **`docs/GDD.md`** | `docs/DESIGN.md` jako **zdroj pravdy** | „jak se hra hraje" — bez toho nemá ADD ani TDD co popisovat |
| 2 | **`docs/ADD.md`** | nic (je to **lidská vrstva** k `assets/spec.json`) | vzhled se odvozuje ze hry, ne naopak |
| 3 | **`docs/TDD.md`** | `docs/ARCHITEKTURA.md` jako **zdroj pravdy** | technika se odvozuje z obsahu a vzhledu |
| 4 | úprava `AGENTS.md` | — | dnes ukazuje na `docs/DESIGN.md` jako na zdroj pravdy, **což je nepravda** (`DESIGN.md:3` se sám hlásí jako zrušený) |
| 5 | `.forge/roadmap.json` | — | **teprve po 1–4**; generuje se z milníků `M0`–`M6` |

---

## 2. Odkud co vzít (mapa rozhodnutí → dokument)

**Tohle je jádro zadání.** Všechno je v `_analyza/DESIGN-REVIZE-2.md`; čísla
v závorkách jsou jeho oddíly.

### Do GDD

| Co | Odkud |
|---|---|
| záměr jednou větou, pro koho | §2 |
| **5 pilířů jako POCITY** + co který vylučuje | §3 |
| **hlavní pilíř `P2`** („rostu tím, co dělám — a je to vidět") | §3 |
| **hlavní smyčka na 8 vět** + 3 pravidla z krajních případů (těžba má hloubku; poptávka je tříděná a mění se; hnací silou je cíl s číslem) | §4 |
| jak hráč pozná úspěch (tři místa; „vyšší potenciál" = strop **i** možnosti) | §5 |
| ovládání (pravé tlačítko + vzdálenost kurzoru, stamina, mrtvá zóna, vyhlazení) | §6 `K5`, §14.1 |
| **míra úspěchu `V1`–`V8`** (každý bod s důkazem a s tím, kdy musí platit) | §12.2 |
| **non-goals** (11 zákazů s důvody) | §12.3 |
| **prvních 5 minut** (scénář) | §12.4 |
| **rozsah v číslech** (rozsah `M`) | §12.5 |
| mechaniky: atrofie (přepínač), synergie (20 %), stav světa (infestace + zásobenost, ceny z nich), léčení obvazy, zbraň jen v ruce | §13.1, §13.7 |
| obsah v číslech: 11 materiálů, 7 předmětů, 3 nestvůry, 8 receptů, 6 dovedností, mapa | §13.2 |
| vzorce a startovní čísla (růst, výnos, kvalita, ceny, infestace) | §13.3 |
| jak svět pozná mistra (trojice kritérií) | §13.4 |
| co je na obrazovce (herní okno, inventář, mapa; paperdoll až s vrstvenou grafikou) | §1.5 vstupů, §14.1 |

### Do ADD

| Co | Odkud |
|---|---|
| co je hotová strojová ADD | `assets/spec.json` (rozměry 960×540, dlaždice 96×48, 8 rolí, 8 slotů vrstev, 6 bran s tolerancemi, styl se zákazy, zrušená paleta s důvodem) |
| **odložené rozhodnutí `A-1`** (vrstvená grafika je cíl, rozhodne se po prototypech `M0`–`M5`) | §7 |
| **placeholdery**: generovaná primitiva jako základ; free assety na UI, ikony a zvuk — **s podmínkou deklarovaných rozměrů** | §7 |
| lidská vrstva (co v `spec.json` nemá smysl držet strojově) | `REKONSTRUKCE-ADD-TDD-GDD.md` §2.2 |
| katalog assetů „co má být vyrobeno" vs. „co existuje" | tamtéž §2.2 (`tools/*.txt` jsou rozhodovací materiál bez výsledku) |
| dokumentace pipeline (Blender / SDXL) | `tools/blender/*.py` — **ještě nenačtené**, patří přečíst |
| zvuk | `DESIGN.md:52–53` ho popisuje, `assets/audio/` **neexistuje** |

### Do TDD

| Co | Odkud |
|---|---|
| **architektura běhu** (`R-1`): pevný tik **50 ms**, jeden kořen s registrem komponent, simulace oddělená od zobrazení (zprávy a příkazy) | §14.1, §11 |
| **výkonnostní rozpočet** (`R-2`): 60 FPS při 960×540, simulace **< 2 ms/tik** | §14.2 |
| **jazyk** (`R-3`): klíče a identifikátory anglicky, texty pro člověka česky (i pro `assets/data/*.json`) | §14.1 |
| datové formáty: `assets/data/*.json` (obsah), `assets/levels/*.json` (mapa a markery), `ConfigFile` do `user://` | §14.2 |
| chybové chování: `push_error` + hra zůstane hratelná; **tichý `return` zakázán** | §14.2 |
| **15 smluv bez tvaru dat** (dnes tvar mají 3 z 18) | `ARCHITEKTURA.md` §2 + `REKONSTRUKCE…` §3.2 |
| podmínka pro cestu B (oddělená simulace) — **z rozhodnutí, ne z vkusu** | §11 |
| brány: co která měří a **kde má slepá místa** | `docs/BRANY-HRY.md` |

### Do plánu (až po dokumentech)

| Co | Odkud |
|---|---|
| **milníky `M0`–`M6`** jako hratelné stavy (kostra → pohyb → těžba s číslem → výroba → svět reaguje → uznání a smrt → grafika) | §15.1 |
| **definice hotovo** (soubor v `main` **A** brána funkci zavolala **A** kritérium s hodnotou **A** volá to produkční kód) | §15.2 |
| co u bran chybí (brána nad dokumentací; třetí stav „neměřeno" `exit 2`) | §15.2 |

---

## 3. Naměřená fakta (neověřuj znovu, jen ověř, že sedí)

| # | Fakt | Kde je doložený |
|---|---|---|
| 1 | **Hra je dnes sběračka dvou mincí** — mapa 16×30, 2 coin markery, Label se skóre, nápověda inzeruje **6** kláves, které kód neobsluhuje | `DESIGN-REVIZE-2.md` §1 |
| 2 | **13 granul je `done`, hra používá 2** (`level.gd`, `player.gd`); HUD, boj, výroba, ekonomika ani ukládání nejsou v produkční cestě | tamtéž |
| 3 | **`scripts/world.gd` = 0 B** — blokuje `world.map` i `engine.shell` | tamtéž |
| 4 | **Obsah: 4 materiály, 4 skilly, 3 recepty, 1 nestvůra, 2 předměty** | tamtéž |
| 5 | **Dva výtvarné systémy**: 258 PNG v `tools/blender/sprites/**` (hra je nepoužívá, 0 odkazů) vs. 16 plochých v `assets/sprites/` | tamtéž |
| 6 | **`ARCHITEKTURA.md` má 18 smluv, tvar dat 3** | tamtéž |
| 7 | **Tři nepravdivá tvrzení v pravidlech jsou OPRAVENA** 8. 10. 2026 (`AGENTS.md` §Jazyk, `CONVENTIONS.md` §4 a §7) | tamtéž §15.5 |
| 8 | **CI hry je zelené** (`ci.yml` #118 nad `932dc6f`), ale **`Forge agent` je červený** (20 selhání v řadě, naposledy 8. 10. 11:39) a **roadmapa conductora je prázdná** | měřeno 8. 10. 14:15 přes `/health` a `tools/status.mjs` |

> **⚠ `docs/DESIGN.md` a `docs/ARCHITEKTURA.md` se NEMAŽOU.** Nahrazují se jako
> **zdroj pravdy**, ale zůstávají jako historie (`DESIGN.md` se sám tak hlásí).
> Do jejich hlaviček patří věta „**nahrazeno `<nový soubor>` dne <datum>**",
> ne smazání — historická znalost se needituje.

---

## 4. Required výstup

1. **`docs/GDD.md`** — hlavička (co to je, odkud brát stav), záměr, pilíře,
   smyčka, míra úspěchu `V1`–`V8`, prvních 5 minut, ovládání, UI, rozsah
   v číslech, **non-goals**, mechaniky se vzorci, obsah.
2. **`docs/ADD.md`** — lidská vrstva vzhledu + katalog assetů + pipeline
   + rozhodnutí „ploché vs. vrstvené" jako **vědomě odložené**.
3. **`docs/TDD.md`** — architektura běhu, vrstvy, **18 smluv s tvarem dat**,
   datové formáty, vlastnictví stavu, výkon, ukládání, chybové chování, jazyk.
4. **`AGENTS.md`** — přepsané odkazy („co hra je" → `docs/GDD.md`, „architektura
   a smlouvy" → `docs/TDD.md`) + doplnit `docs/ADD.md` do „Kam pro co".
5. **Až po 1–4**: návrh nové `.forge/roadmap.json` (milníky `M0`–`M6`) —
   **návrh k odsouhlasení**, ne tichá změna (roadmapa je zdroj pravdy orchestry).

**U každého dokumentu platí:**
- **hlavička** říká, čím dokument je a odkud brát stav;
- **každé číslo má zdroj** (odkaz na `DESIGN-REVIZE-2.md` §N nebo na kód);
- **sekce „co v tom záměrně NENÍ"** (jinak si agent domyslí sousední vrstvu);
- **žádné placeholdery** (TODO/TBD) — co není rozhodnuté, patří do otevřených témat.

---

## 5. Otázky pro člověka (co ještě není rozhodnuté)

```
[ ] O-1  ČÍM PLATÍ ŘEMESLNÍK, když ne grindem        (DESIGN-REVIZE-2.md §13.8)
         Uživatel sám řekl „ještě nevím, nebo jestli vůbec".
         Menu nákladů: palivo, opotřebení nástroje, zmetkovost (doporučeno vzít
         ty tři), poplatek za stanici, riziko cesty (patří do L).
         → Dokud to není rozhodnuté, patří to do GDD jako OTEVŘENÝ BOD,
           ne jako tichá volba agenta.

[ ] O-2  NÁZEV HRY: sjednotit na `uo-shadows`        (§15.5 `P3`)
         Uživatel rozhodl „sjednotit" — ale mění to `project.godot` a
         `assets/spec.json`, což je kód. → zařadit jako samostatný úkol,
           ne ho provést mimochodem při psaní dokumentů.

[ ] O-3  `_acl-recovery/` v rootu repa — patří do repa, nebo pryč?
         Je to necommitnutý artefakt opravy ACL ze sandboxu.

[ ] O-4  BRÁNY NAD DOKUMENTACÍ: zavést `check-docs-refs` a `check-zadani`
         (vzor `game-clone`) a třetí stav „neměřeno" (`exit 2`)?
         Až budou dokumenty existovat — dnes by neměly co měřit.
```

---

## 6. Co NEDĚLAT

1. **Neměnit kód hry** — tenhle krok je psaní dokumentů. Když dokument odhalí
   vadu v kódu, **zapiš ji**, neopravuj ji mimochodem.
2. **Neměnit `.forge/roadmap.json` dřív**, než jsou dokumenty hotové
   a zkontrolované — jinak vznikne plán z rozpracovaných dokumentů.
3. **Nezakládat čtvrtý zdroj pravdy.** Tři dokumenty + `spec.json` stačí;
   `DESIGN.md` a `ARCHITEKTURA.md` se **nahrazují**, ne obcházejí.
4. **Nekopírovat `DESIGN-REVIZE-2.md` doslova.** Je to záznam dialogu;
   dokumenty se z něj **odvozují** a odkazují na něj.
5. **Nepřebírat čísla bez kontroly.** Kde dokument tvrdí něco o kódu
   (počty, rozměry, chování), **ověř to v kódu** — v téhle session se dvě čísla
   zadání nepotvrdila.
6. **Nespouštět Godot, dokud to není potřeba k ověření tvrzení.** Testy se čtou
   z výstupu běhu (`[test] N kontrol, M selhání`), ne z exit kódu.
7. **Nepsat `done: true`** ani jiná tvrzení o hotovosti — ta se **měří**
   (definice hotovo, §15.2).

---

## 7. Co je potřeba ověřit na začátku (5 minut)

```powershell
# 1. stav repa
git -C E:\Workspaces\uo-shadows log --oneline -3
git -C E:\Workspaces\uo-shadows status --short

# 2. že zdroj rozhodnutí existuje a je úplný
#    (má mít oddíly §1–§16 a v hlavičce „UZAVŘENO")
Select-String -Path E:\Workspaces\uo-shadows\_analyza\DESIGN-REVIZE-2.md -Pattern '^## '

# 3. že pravidla už nelžou (tři opravy z 8. 10.)
Select-String -Path E:\Workspaces\uo-shadows\CONVENTIONS.md -Pattern '_safe_spot'
Select-String -Path E:\Workspaces\uo-shadows\AGENTS.md -Pattern 'target dead'
```

**Očekávané výsledky:** `main` = `5fe6d8e` nebo novější; `DESIGN-REVIZE-2.md`
má oddíly `§1`–`§16`; oba grepy najdou **jen opravné poznámky** (ne tvrzení).
