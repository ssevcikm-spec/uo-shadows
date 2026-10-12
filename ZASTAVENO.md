# ZASTAVENO — uo-shadows

> **Co tenhle soubor JE:** **záznam o zastavení projektu** (rozhodnutí uživatele
> 12. 10. 2026). Není to stav projektu ani kronika. **Doplňuje se, nepřepisuje.**
> **Proč tu je:** naměřeno na `idle-realm` — když u projektu není napsáno, že
> stojí a **proč**, další session začne dělat **hotovou práci znovu** (u
> `idle-realm` o tom nebyla zmínka ve 23 dokumentech ani v session logách).
> **Odkud brát stav kódu:** `git log`, `docs/TDD.md`, `HANDOFF.md` (z 9. 10. 2026).

---

## 1. Co to znamená

* **Projekt se dál nevyvíjí.** Kód, dokumenty, historie i necommitnuté větve
  zůstávají — **nic se nemaže a nic se nepřepisuje**.
* **Není zastavený proto, že by byl rozbitý.** Naposledy měřený stav: brány
  zelené, testy běží.
* **Není to hotová hra.** Je to nedokončený projekt — a to je jiná věc.

## 2. Proč stojí

Uživatel 12. 10. 2026 rozhodl (**O1–O3**), že se vývoj přesouvá do **nového
projektu** (`E:\Workspaces\The-Hero-Arc`) — nová hra, vlastní malý svět, vědomé
dědictví místo pokračování. Zdůvodnění a ceny: `The-Hero-Arc\ROZHODNUTI-2026-10-12.md`.

Důvod, který platí i bez toho: **každý živý projekt spotřebovává session.**
Tři projekty = pozornost rozdělená na třetiny, a to je při agentním vývoji to
nejdražší, co se dá ztratit.

## 3. Naměřený stav v den zastavení (12. 10. 2026)

| Co | Hodnota |
|---|---|
| Git | `HEAD e4dccdb`, **9. 10. 2026 11:56**, 99 commitů, strom **čistý**, **2 commity nepushnuté** (`origin/main` = `01a9649`) |
| Kód | `scripts/*.gd` 16 souborů / **1 716 řádků**, z toho **produkční cesta 851**; **865 řádků ve 13 souborech je mrtvá knihovna** |
| Plán | `roadmap.json` = 21 granul, **`done: true` u 16** — při **dvou funkčních komponentách** |
| Grafika | **258 PNG** z Blender pipeline, které hra nepoužívá (vznikly **před** smyčkou) |
| Dokumenty | 16 `.md` / 58 081 slov; `GDD.md`+`ADD.md`+`TDD.md` (1 779 řádků) z revize vize 8.–9. 10. |
| Navíc na disku | `_analyza/idle-realm/` = **133,5 MB** cizích session logů (gitignorováno) |
| Orchestra | nevydala nic od **3. 10. 2026** (`origin/forge/*`) |

## 4. Co by ho vrátilo

**Projekt se neoživuje proto, že by na něm zbyla práce.** Vrací se jen tehdy,
když **uživatel výslovně rozhodne**, že se k němu vrací — a **řekne čím**.

Znalost, kterou nese, se dá vzít **bez oživení** (viz §5). Dokud takové
rozhodnutí nepadne, platí: **je to zdroj, ne projekt.**

## 5. Co si z něj nová hra bere (a co ne)

**Bere (řemeslo a měření — není o UO):**
`CONVENTIONS.md` (naměřené pasti Godotu 4) · `docs/BRANY-HRY.md` (katalog bran
včetně případu „brána tiše přestala měřit“) · `_analyza/over-dokumenty.py`
(kontrola tvrzení v dokumentech proti zdrojům, sabotér 9/9 mutací, `exit 2`
= NEMĚŘENO) · `tools/blender/` (3D→2D pipeline) · pořadí kroků v CI ·
**tvar** `GDD.md`/`TDD.md` (pilíře jako pocity, `V1–V8` s důkazem, non-goals
s důvodem, smlouvy s tvarem dat).

**Nebéře:** obsah a vizi „Moderní Ultima Online“ (`docs/ARCHITEKTURA.md`),
258 nepoužitých spritů, mrtvou knihovnu 865 řádků, UO klon jako cíl.

## 6. Na co pozor (aby se to nezopakovalo)

1. **Grafika vznikla dřív než smyčka** → 258 PNG, které hra nikdy nepoužila.
2. **`done: true` u 16 granul při dvou funkčních komponentách** → hotovost se
   musí **měřit** (git + test + volání z produkčního kódu), ne hlásit.
3. **Sedm rozporů v dokumentech** (např. `TDD.md:481–482` tvrdí, že `assist` je
   non-goal `N9`, zatímco `GDD.md:432–446` ho po 9. 10. povoluje; dvě různá
   čísla téže brány: 57 vs 97 funkcí). → Brány nad dokumentací, ne dobrá vůle.

## 7. Co není dořešené (a co to vrátí)

* **2 nepushnuté commity** (`e4dccdb`, a předchozí) — **rozhodne session, která
  je vytvořila.** Push by je publikoval, a to není práce téhle session.
* **Necommitnuté větve orchestra:** `oprava-139`, `oprava-140`,
  `oprava/mining-registr` — opravy směrem k registru komponent, které se
  **nikdy nesloučily**. Leží v gitu, nic je nemaže.
* **`Forge agent` na GitHubu je červený** a **příčina není změřená** (doloženo
  8. 10. 2026). S zastavením projektu to **není vyřešené** — je to jen odložené.
