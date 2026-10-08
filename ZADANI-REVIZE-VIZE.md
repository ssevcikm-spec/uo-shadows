# ZADÁNÍ: Revize vize `uo-shadows` (nová session)

> **Co tenhle dokument JE:** **zadání pro session, která přijde.** Není to stav
> a není to analýza — je to instrukce, co má nová session udělat.
>
> **Kdo ho napsal:** session z 8. 10. 2026, která **měla kontext** (stavěla
> rekonstrukci ADD/TDD/GDD a vedla první kolo design dialogu). Nová session ten
> kontext nemá — proto je tady všechno podstatné vypsané.
>
> **Zkontrolováno při:** `af6abd8` (`design: pracovni vstupy uzivatele +
> kriticka revize`) · **8. 10. 2026 12:37 UTC**
> **Stav repa při psaní:** `origin/main` = `932dc6f`, lokálně **5 commitů napřed**
> (`origin/main..HEAD = 5`) — **nepushnuto**, pravidla hry říkají nepushovat bez
> vyžádání.
> **Pushnuto:** ne.
>
> **⚠ Nová session POVINNĚ ověří, že `rev-parse HEAD` odpovídá** — a **i když
> ano, ověří aspoň tři klíčová tvrzení níž**, protože shodný commit neznamená, že
> tvrzení sedí (může být špatně **už při zápisu**).

---

## 0. Jak začít (v tomhle pořadí, ne jinak)

1. `AGENTS.md` hry (trvalá pravidla) — **a ověř, že se skutečně načetla**.
2. **`_analyza/DESIGN-PRACOVNI-VSTUPY.md`** — vstupy uživatele + kritika.
   **Tohle je jádro zadání.**
3. **`_analyza/REKONSTRUKCE-ADD-TDD-GDD.md`** — co z dokumentů existuje a co ne.
4. `assets/spec.json` — **strojová podoba ADD**, hodně rozhodnutí je v něm.
5. `C:\Users\Ssevc\Local-Deepseek\KONCEPT-PRIPRAVY-HRY.md` — metodika vrstev
   (§2 žebřík, §7 kontrolní seznam).
6. `C:\Users\Ssevc\.dsh\skills\dialog-s-uzivatelem\SKILL.md` — **jak se ptát**
   (forma otázek, opozice, cena rozhodnutí). **Použij ho.**

**Nespouštěj Godot ani brány** — tahle session nemá opravovat kód.

---

## 1. Cíl

**Projít s uživatelem celou vizi hry po vrstvách a vyladit ji tak, aby se podle
ní dal napsat GDD, ADD a TDD — bez dohadování.**

Uživatel to řekl takhle: *„ber moje vstupy jako můj pocit. Prosím projdi se mnou
celý plán, buď kritický, podávej zpětnou vazbu nebo náměty. Chci to projít
detailně, vyladit co nejvíce hned a objasnit to, aby se systém a AI pak nemusely
hádat."*

**Pořadí podle závislostí — neotevírej další vrstvu, dokud není předchozí
uzavřená:**

| Kolo | Vrstva | Hotovo, když… |
|---|---|---|
| 1 | Záměr + Zážitek | smyčku jde převyprávět bez zaváhání |
| 2 | Míra úspěchu + Non-goals | každé tvrzení je měřitelné nebo zakázané |
| 3 | Mechaniky + Obsah | každá mechanika má číslo nebo vzorec |
| 4 | Technika + Smlouvy | tick, pohyb, kolize, datové formáty |
| 5 | Plán + Brány + Pravidla | každý milník je vidět na obrazovce |

---

## 2. Naměřená fakta (neověřuj znovu, jen ověř, že sedí)

| # | Fakt | Kde je doložený |
|---|---|---|
| 1 | **„Jak se hra hraje" v repu NEEXISTUJE.** Ovládání, UI, prvních 5 minut, míra úspěchu, rozsah v číslech i non-goals chybí. `project.godot` nemá **ani jednu** vstupní akci | `REKONSTRUKCE…` §1.2 |
| 2 | **Hra je dnes sběračka dvou mincí** — mapa 30×16, hráč, 2 mince, Label se skóre, běhová chyba `tween_property` při startu, nápověda inzeruje 5 kláves, které kód neobsluhuje | `AUDIT-PLANU-A-DESIGNU.md` §4.1 |
| 3 | **13 granul je `done`, ale hra používá 3.** 10 hotových komponent hra **nikdy nezavolá** | `AUDIT…` §4.2 |
| 4 | **Dva paralelní výtvarné systémy** — 256 vyrenderovaných PNG vrstvené postavy v `tools/blender/sprites/**` (hra je **nepoužívá**, 0 odkazů v kódu) vs. 16 plochých spritů v `assets/sprites/` (hra je používá) | `REKONSTRUKCE…` §2.3, §4.1 |
| 5 | **`assets/spec.json` je hotová ADD ve strojové podobě** — rozměry, 8 rolí, vrstvy oblékání, 6 bran s tolerancemi, směr stylu **i se zákazy**, zrušená paleta s důvodem | `REKONSTRUKCE…` §2.1 |
| 6 | **TDD má 18 smluv, tvar dat jen 3 z 18** (`ARCHITEKTURA.md` §2.1–2.3) | `REKONSTRUKCE…` §3.2 |
| 7 | **Skutečný obsah hry je malý:** 4 materiály, 4 skilly, 3 recepty, 1 nestvůra, 2 předměty (`assets/data/*.json`) | `REKONSTRUKCE…` §1.1 |
| 8 | **`engine.shell` (jediná granule, která měla hru složit) je blokovaná mrtvou granulí `world.map`** — soubor `scripts/world.gd` má **0 bajtů** | `AUDIT…` §2.2 V1 |
| 9 | **`docs/DESIGN.md` je zrušený, ale `AGENTS.md:91` na něj odkazuje jako na zdroj pravdy** | `REKONSTRUKCE…` §4.2 |
| 10 | **Pravidla hry obsahují tři nepravdivá tvrzení** — `AGENTS.md:108–110` („cíl mrtev" vs. `"target dead"`), `CONVENTIONS.md:273` (26 vs. 91 kontrol), `CONVENTIONS.md:252` (`_safe_spot` neexistuje) | `AUDIT…` §4.5(c) |

---

## 3. Co už je ROZHODNUTÉ (neptej se znovu)

Ze sezení 8. 10. 2026 — uživatel to řekl, je to zapsané
v `DESIGN-PRACOVNI-VSTUPY.md` §1:

1. **Prototypy první.** *„než bude vyvinutá grafika, budu rád za primitivní
   prototypy — cokoliv nejlevnějšího."* → **Dokud nefunguje smyčka, nevzniká
   žádná grafika, jen barevné obdélníky.**
2. **Pohyb:** plynulý, **nezamčený v mřížce**, všesměrový, s vyladěným
   rozběhem a zastavením; objekty se **nesmí překrývat**.
3. **Vstup:** primárně **myš** — držení pravého tlačítka + vzdálenost kurzoru
   od postavy určuje rychlost (pomalá chůze / chůze / běh).
4. **Skilly:** volně rostoucí, **vzájemně se doplňují a navzájem trénují**
   (kladivo → tupé zbraně; znalost kovů → rychlejší tinkering), **atrofují**
   při nepoužívání, mají **strop**, každá fáze 0→max má cenu.
5. **Smyčka:** prožít dobrodružství → získat odměnu → **uplatnit ji** (prodat,
   předat, spotřebovat) → **vidět vliv na ekonomiku nebo stav světa**.
6. **UI:** herní okno, rychlý náhled do **paperdoll**, rychlý přístup do
   **inventáře**, **mapa**.
7. **Hra nemá konec.** Úspěch = měřitelný růst schopnosti (hit rate, damage,
   přežití, kvalita, konzistence) a **přínos pro komunitu**.
8. **Vrstvení postavy ano** — postava má zobrazovat, co má nasazené.

---

## 4. Co je OTEVŘENÉ (tohle potřebuje uživatele)

### 4.1 Blokující — bez nich se nedá psát GDD

```
[ ] N-1  MMO: „bude to mmo" je v rozporu s ARCHITEKTURA.md:34 („simulace běží
         lokálně, single-player"). A hlavně: příspěvek do světové ekonomiky
         NEFUNGUJE bez populace. → Navrženo: „navrženo pro MMO, MVP
         single-player" + SIMULOVANÁ ekonomika + viditelný stav světa.
[ ] G-1  (částečně zodpovězeno bodem 3 v §3 — chybí mřížka vs. volný pohyb
         v souvislosti s dlaždicovou grafikou; potvrdit)
[ ] G-2  Pilíře jako POCITY, ne featury (dnešních 7 „pilířů" v ARCHITEKTURA.md
         jsou featury). Uživatelův text §1.3 je surovina — zformulovat.
[ ] G-3  Hlavní smyčka rozepsaná na 6–8 vět, kde každá musí fungovat celá.
[ ] G-5  „Jak hráč pozná úspěch" — uživatelův text §1.6 je surovina;
         „vyšší potenciál" je potřeba rozpadnout na měřitelné.
```

### 4.2 Nezablokuje první krok

```
[ ] A-1  Který výtvarný systém (ploché vs. vrstvené) — uživatel řekl „vrstvení",
         ale odpověď „nemusí se rozhodnout teď" je platná (prototypy první).
[ ] R-1  Architektura běhu: tick, kořen, jak spolu komponenty mluví.
         → Vysvětlit lidsky (uživatel řekl „R1 vysvětlit prosím"), pak navrhnout.
[ ] N-2  Osmi směry pro plynulé otáčení — teď, nebo po prototypech?
         (2× grafika na každý kus výbavy)
[ ] N-3  Potvrdit ovládání: držení pravého tlačítka + vzdálenost kurzoru = MVP,
         stamina jako omezení běhu, toggle později. (Tři věci se SKLÁDAJÍ:
         záměr / rozpočet / zámek.)
[ ] N-4  Atrofie: hned, nebo jako přepínač až po prvním ladění?
[ ] N-5  Synergie jako data (`assets/data/synergies.json`) — souhlas?
[ ] N-6  Zbraň „v ruce" vs. „u pasu" — MVP jen v ruce? (2× obrázků)
[ ] N-7  Free assety: zvuk + UI + textury ano, hlavní vzhled ne — souhlas?
[ ] N-8  Co je „stav světa", který má hráč vidět? Aspoň dvě měřitelné věci.
[ ] N-9  Paperdoll v MVP, nebo až s vrstvenou grafikou?
[ ] N-10 „Vysoce rewarding mistrovství" — jak se to pozná?
```

---

## 5. Required výstup

**Tři věci, všechny zapsané:**

1. **Aktualizovaný `_analyza/DESIGN-PRACOVNI-VSTUPY.md`** — nebo nový
   `DESIGN-REVIZE-2.md` — s **rozhodnutými** odpověďmi na §4 a s **cenou**
   u každého rozhodnutí (skill `dialog-s-uzivatelem` §4).
2. **Návrh obsahu GDD, ADD a TDD** — osnova + co je rozhodnuté + co chybí.
   **Ještě ne plné dokumenty** (ty vzniknou až po uzavření vize).
3. **Aktualizovaný `OTEVRENA-TEMATA.md`** — co zůstalo otevřené.

**A na konci:** *„co se udělá dál"* — konkrétní krok, ne „budeme pokračovat".

---

## 6. Co NEDĚLAT

1. **Nezačni psát GDD.** Nejdřív revize vize s uživatelem. GDD je výstup, ne cíl
   téhle session.
2. **Neměň kód ani nespouštěj Godot.** Je to design session.
3. **Nevymýšlej design za uživatele.** Když něco nejde odvodit, je to otázka.
   *(Naměřeno: chybějící odpověď na „co hráč dělá" se nedá dohnat prací.)*
4. **Nezakládej nové dokumenty vedle existujících.** `docs/DESIGN.md`
   a `docs/ARCHITEKTURA.md` se mají **nahradit**, ne obcházet — jinak vznikne
   **čtvrtý zdroj pravdy**, což je v tomhle projektu už jednou naměřená vada.
5. **Nepiš do `docs/` ani do `.forge/roadmap.json`** — plán se mění až po
   uzavření vize, a roadmapa je zdroj pravdy orchestry.
6. **Nepushovat** bez vyžádání.
7. **Neptej se na to, co je v §3** — uživatel to odpověděl. Zopakovaná otázka
   je známka, že session nečetla zadání.
8. **Nepoužívej žargon v otázkách.** Naměřeno dvakrát dne 8. 10.:
   „který výtvarný systém?" → *„Nerozumím zadání"*;
   „architektura běhu?" → *„vysvětlit prosím"*. Viz skill §1.1.

---

## 7. Hotovo znamená

```
[ ] Uživatel odpověděl na všechny blokující otázky (§4.1)
[ ] Každá odpověď má u sebe CENU (co to znamená, co se tím ztratí)
[ ] Hlavní smyčka je rozepsaná na věty a uživatel ji převyprávěl zpět
[ ] Pilíře jsou POCITY, ne featury
[ ] Non-goals existují jako výslovný seznam
[ ] Je jasné, který z těch dvou výtvarných systémů je budoucnost (nebo je
    výslovně odloženo na prototypech)
[ ] Je zapsané, kdo vlastní rozhodnutí a kde jsou dokumenty
[ ] `OTEVRENA-TEMATA.md` je aktualizovaný
[ ] Zaznělo „co se udělá dál"
```

---

## 8. Poznámky pro novou session (co si ta stará myslela a neřekla)

- **Největší riziko je MMO** (`N-1`). Když uživatel trvá na skutečném MMO,
  **mění se celý plán** — a je lepší to vědět v prvním kole než po třech.
- **Druhé největší riziko je rozsah.** Hra má dnes 4 materiály a 1 nestvůru;
  uživatel mluví o dungeonech, infestacích a šlechtění zvěře. Rozdíl mezi tím
  je **řádově** — a patří to na stůl hned.
- **Nejužitečnější, co můžeš udělat, je oponovat prostředku, ne záměru**
  (skill §3.1). Uživatel o opozici **výslovně žádal**.
- **Uživatel nečte kód.** Vysvětluj koncepty, ne implementaci.
