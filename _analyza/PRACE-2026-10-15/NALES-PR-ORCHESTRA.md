# NÁLEZ: proč orchestra nevydává PR (a co s tím) — 15.–16. 10. 2026

> **Co tenhle dokument JE:** **naměřený nález** k orchestraci hry `uo-shadows`.
> Vznikl 16. 10. 2026 z živé diagnostiky (devět běhů, logy z GitHub API).
> **Není to stav projektu** — stav je v `docs/PLAN-VYVOJE.md`.
> **Odkud brát dnešní stav:** `node _analyza/PRACE-2026-10-15/hlidej-orchestru.mjs`.

---

## 1. Příznak

Agent orchestry **vyrobí kód, který projde testy**, ale do repa se nikdy nedostane:
krok „Otevři pull request" padá na

```
fatal: could not read Username for 'https://github.com': No such device or address
##[error]The process '/usr/bin/git' failed with exit code 128
```

Naměřeno: `coin-picker` má od 13. 10. 2026 **14 PR**, `uo-shadows` **0** —
přitom obě hry používají stejný workflow. Rozdíl je tedy v **secretu**, ne v kódu.

## 2. Příčina (změřená, ne odhadnutá)

Workflow bere token ze `secrets.FORGE_PAT` (`agent.yml:540`) a pushuje s ním
(`GH_TOKEN`, `:602`). Secret v repu hry **existoval**, ale jeho **hodnota
nefungovala**: GitHub ji odmítal, takže `git` se ptal na jméno a heslo — a v CI
se není koho zeptat.

**Jak se to pozná (test, který to rozliší):** zkus přes API vytvořit větev —
`POST /repos/{repo}/git/refs`. Kdo to umí, umí i push z CI.

| Token v `.secrets/` | Vytvoří větev? | Poznámka |
|---|---|---|
| `conductor_pat.txt` | **ANO** (HTTP 201) | fine-grained; **umí** `Contents: write`, **neumí** číst secrets |
| `github_pat.txt` | **ANO** (HTTP 201) | klasický PAT (`repo`, `workflow`) — umí i secrets |
| `conductor_github_token.txt` | **NE** (HTTP 403 „Resource not accessible") | ⚠ **tahle hodnota nejspíš byla v secretu** |
| `coin-picker_forge_pat.txt` | **NE** (HTTP 403) | fine-grained **bez** `Contents: write` |

**Proč to nevypadá jako chyba tokenu:** u coin-pickeru PR vznikají, protože tam
je v secretu jiná (funkční) hodnota. Stejný workflow, jiný secret — a výsledek
se čte jako „orchestra je rozbitá", i když je rozbitá jen jedna hodnota.

## 3. Co se opravilo

1. **Secret `FORGE_PAT` nastaven na ověřenou hodnotu** (`conductor_pat.txt`,
   ověřeno testem „vytvoř větev a smaž ji"). Nástroj:
   `_analyza/PRACE-2026-10-15/nastav-forge-pat.py` (dry-run bez `--zapis`,
   hodnotu nikdy nevypisuje).
2. **`RETRY_HOURS` 3 h → 30 min** (`forge-orchestra/conductor/wrangler.toml`,
   commit `7cae0f3`). Důvod: 15. 10. spadly tři granule třikrát za sebou a mezi
   pokusy se čekalo 3 h — přitom šlo o dvě syntaktické chyby opravitelné hned.
   Stropy `MAX_ATTEMPTS` (5) a `GRAIN_MAX_RUNS` (8) zůstávají, takže kratší
   cooldown nevyrobí nekonečnou smyčku. **Cesta zpět:** `RETRY_HOURS = "3"`.

### 3.1 OVĚŘENO: PR se zakládá a samo se slučuje (16. 10. 2026)

Naměřeno po opravě secretu:

| Co | Hodnota |
|---|---|
| Běh | `#546`, granule `engine.input` (úloha #269) |
| Výsledek | **`success`** |
| PR | **#38** — `merged: true`, `merged_by: ssevcikm-spec`, merge commit `39f4e03` |
| CI na PR | `Testy a build = completed/success` |
| Doručeno do `main` | **`scripts/input.gd`** (26 řádků) |
| Ověření lokálně | `[test] 113 kontrol, 0 selhání`; `check-wiring` **105 funkcí v 18 souborech** |
| `/health` | **`forge.ok = true`, `selhání v řadě = 0`** (bylo 20) |

**Kvalita kódu od agenta je čistá** — používá přesně to, co se doplnilo do
`CONVENTIONS.md`: `var direction: Vector2 = …` (žádné `:=` u hodnoty bez typu),
žádný typ z cizího skriptu v anotaci a **vlastnost `global_position`** místo
neexistujícího `get_global_position()`. To je přímý důkaz, že oprava zadání
a konvencí měla efekt — ne že se „něco opravilo samo".

> **Poznámka k `*.uid`/`*.import`:** PR přineslo i pět takových souborů a může to
> vypadat jako smetí od agenta. **Není to nová vada:** v repu jich je trackovaných
> **přes 250** (`.gitignore` kryje jen `.godot/`), takže je to zavedená konvence
> projektu — agent se chová stejně jako všechno před ním. Měnit ji (a mazat
> 250 souborů) je samostatné rozhodnutí, ne součást téhle opravy.

## 4. Co ještě blokuje (a co s tím)

| # | Věc | Naměřeno | Návrh |
|---|---|---|---|
| 1 | **Limit poskytovatele 8 000 tokenů/request** (Groq, `gpt-oss-120b`) | `Limit 8000, Requested 40537` u granule se dvěma soubory; `engine.input` posílá 32 000 | granule s **jedním** souborem (uděláno: `shell.coins` → `shell.nocoins` + `shell.save`); u velkých granul volit poskytovatele s vyšším limitem |
| 2 | **`scripts/game.gd` je 377 řádků** (monolit) | aider si ho přidá celý (~3 940 t) a někdy dvakrát (k editaci i `--read` závislosti) | rozdělit monolit (`sim.wire` a `shell.nocoins` jsou první kroky) |
| 3 | **`CONVENTIONS.md` se posílá celý** (4 590 t = 56 % limitu) | `--read CONVENTIONS.md` v `agent.yml:227` | filtr `.forge/node/konvence-pro-granuli.mjs` **je hotový**, ale měří úsporu jen **8–15 %** — většina sekcí jsou pasti parsování, které se vyplatí posílat vždy. **Zúžení má smysl až po rozdělení monolitu**, ne místo něj |
| 4 | **Model dělá malé chyby, které gate chytí** | `Cannot infer type` (2×), `Could not find type "Level"`, `get_global_position()` | dopsáno do `CONVENTIONS.md` §1 a §1h; funguje to — `#391` (`engine.input`) vyrobil kód, který prošel testy |

## 5. Past, na kterou jsem u toho narazil (a je přenositelná)

**Když v JS čteš CRLF soubor, `$` v regulárním výrazu NETREFÍ před `\r`.**
`/^##\s*(.*)$/` na řádku `## 1. …\r` vrátí `null` (v Pythonu by prošel).
Následek v mém filtru: místo 14 sekcí našel **jednu** a poslal 147 znaků místo
celého souboru — **tichá ztráta kontextu**, kterou by nikdo nepoznal, protože
nástroj hlásil úspěch. Řešení: `text.replace(/\r\n/g, '\n')` **před** dělením.

**A druhá past téhož druhu:** `console.log` formátuje podle počtu argumentů;
když jich dáš víc, vypíše **format string doslova** (`%-22s %8d …`) a tabulka
vypadá jako vada dat, i když jsou data správná.
