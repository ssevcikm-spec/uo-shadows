#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""over-dokumenty.py — kontrola dokumentů: proti ZDROJŮM a NAVZÁJEM.

Co to je: ověřovací nástroj (kandidát na bránu `check-docs-refs` z
`_analyza/DESIGN-REVIZE-2.md` §15.2). Není to brána projektu — žije
v `_analyza/`, protože ověřuje DOKUMENTY, ne kód hry.

PROČ JE NAPSANÝ TAKHLE (a ne s čísly napevno):
  Pravidlo stanice je, že TVRZENÍ SE ČTE Z DOKUMENTU. Kdyby měl nástroj čísla
  napsaná v sobě, měřil by zdroj a porovnával ho sám se sebou — vrácená vada
  v dokumentu by mu prošla. Proto se číslo vytáhne REGEXEM Z DOKUMENTU
  (pojmenovaná skupina `v`) a porovná se s hodnotou ZMĚŘENOU ve zdroji.

TŘI PASTI, KTERÉ TENHLE NÁSTROJ ŘEŠÍ (všechny naměřené při jeho psaní):
  1. Tvrzení může být na jiném řádku než jméno souboru (nadpis
     `### 3.17 \`Hud\` — \`scripts/hud.gd\`` a číslo až v textu pod ním).
     → hledá se v OKNĚ a **velikost okna se vypisuje** (velkorysé okno není
     opatrnost, je to slepota).
  2. Okno přes CELÝ dokument chytne číslo, které patří jinam (naměřeno:
     „`game.gd`; naměřeno 8. 10. 2026: `main.tscn` má **6 řádků**“ → nástroj
     hlásil „game.gd má 6 řádků“). → hledá se PO ODDÍLECH a mezi kotvou
     a číslem nesmí být jiný soubor (`forbid`).
  3. „Dnešní stav“ a „cíl“ vypadají stejně („4 materiály“ vs. „11 materiálů“).
     → tvrzení o DNEŠKU se anchoruje na `naměřeno`/`dnes`/`dnešní`.

Stavy (třetí stav je důležitý):
  OK        — tvrzení je v dokumentu a souhlasí se zdrojem
  FAIL      — tvrzení je v dokumentu a NESOUHLASÍ
  NEMĚŘENO — tvrzení se v dokumentu nenašlo (to NENÍ zelená, hlásí se)

CO NÁSTROJ MĚŘÍ (pět tříd; každá hlásí svou skupinu, aby bylo vidět, KTERÁ
kontrola mluví — bez toho by `[CHYCENO]` v sabotéru mohla vyrobit jiná kontrola):

  čísla / odkazy / cesty / hlavička
      původní kontroly: tvrzení o počtech proti ZMĚŘENÉMU zdroji, odkazy `§N`
      proti oddílům, které v cíli existují, cesty v backtickách proti repu
      a hlavička kdekoliv v textu.

  hlavicka — NOVÉ: hlavička, ale PŘESNĚ: v prvních `HEADER_LINES` řádcích
      musí být značka „Co tenhle dokument JE“, DRUH z uzavřeného slovníku
      (zdroj pravdy / historie / brána / záznam / …) a „Odkud brát stav“.
      Dokument, který svou roli nemá v hlavičce, je FAIL. (`docs/DESIGN.md`
      a `docs/ARCHITEKTURA.md` jsou historie a v `DEFAULT_DOCS` NEJSOU.)

  soulad — NOVÉ: vnitřní soulad dokumentů. Zákazy z tabulky non-goals
      (`N1`–`N11`) v `docs/GDD.md` se hledají jako tvrzení ve VŠECH ostatních
      měřených dokumentech (`TDD`, `ADD`, `BRANY-HRY`, `README`). Chytají se
      DVĚ vady:
        * POVOLENÍ ZAKÁZANÉHO — jiný dokument staví zakázanou věc do hry
          („lektvary jsou v MVP povolené“ proti `N11`);
        * ZAKÁZÁNÍ POVOLENÉHO — jiný dokument zakazuje ŠÍŘEJI, než GDD.
          Sem patří přeformulované `N9` (`GDD.md:432–446` povoluje asistenci,
          která jen provede, co hráč rozhodl, ale věta „hra nesmí asistovat
          hráči“ v TDD je širší zákaz, než jaký dnes platí).
      Co zákaz ZUŽUJE (výjimku), se ČTE Z GDD — nástroj si ji nevymýšlí.
      FAIL vypisuje OBĚ místa (`soubor:řádek` + citace).

  neměřeno — NOVÉ: tvrzení o počtech, pro které brána měření NEMÁ
      („N kontrol“, „M funkcí“, „N nálezů“). Když text v okolí NEUVÁDÍ, odkud
      číslo je („naměřeno“, „běh hlásí“, …) a není to citace výstupu
      v backtickách, končí to jako NEMĚŘENO (`exit 2`) — ne jako tiché OK.
      Cíl: nezměřené číslo nesmí být zaměnitelné se změřeným.

CO TENHLE NÁSTROJ NEUMÍ (pojmenované meze, ne „snad to nevadí“):
  * Neumí poznat, že interní odkaz je MYŠLENÝ jinak, když jeho číslo v cíli
    náhodou existuje (naměřeno: `ADD` §4/§5/§11/§12 a `GDD` §6 mají stejné
    číslo jako oddíl zdroje rozhodnutí). Tyhle případy se našly RUČNÍM čtením
    a jsou opravené; nástroj chytí jen ten případ, kdy číslo v cíli NENÍ.
  * Neměří běhové chování (Godot se nespouští) — jen soubory a jejich obsah.
  * `soulad` je VZOROVÝ, ne sémantický. Měří:
      – jen PŘEDMĚTOVÁ slova názvu zákazu (obecná slova jako „soubor“,
        „engine“, „předmět“, „hráč“ se zahazují — nesou ho všude). Zákaz,
        jehož název je CELÝ z obecných slov, proto hlásí NEMĚŘENO, ne zelenou.
      – jen tvrzení, která obsahují některý z cue vzorců `ZAKAZ_CUE`/`POVOL_CUE`
        v JEDNÉ klauzuli spolu s předmětem. Jiná formulace téhož rozporu
        (synonymum, opis, dvě věty) zůstane nenalezena.
      – výjimku hledá jen v GDD, jen v okně ±10 řádků od zmínky kódu zákazu
        a jen ve větách za slovem „nesmí/zakaz…“. Výjimka formulovaná jinak
        se nepozná → hrozí slepé místo i falešný poplach (obojí se vypisuje).
      – blokové citace (`>` na začátku řádku) a HTML komentáře `<!-- -->`
        PŘESKAKUJE. Je to záměr (citace není tvrzení dokumentu), ale znamená
        to, že rozpor ukrytý v citaci nástroj nenajde.
      – tvrzení, které se odvolává na zdroj (`N9`, „non-goal“, `GDD`, „podle“),
        bere jako CITACI. Rozpor schovaný za odvoláním na GDD se nenajde.
      – nástroj NEVÍ, kdo má pravdu: směr je daný (GDD je zdroj pravdy
        o designu). Když je zastaralé GDD, je to nález pro člověka.
  * `neměřeno` zná jen uzavřený registr jednotek `GATE_UNIT_RX` (kontrol,
    testů, selhání, funkcí, volání, nálezů, chyb). Ostatní počty („18 smluv“,
    „9 ms“, „60 FPS“) zůstávají NEMĚŘENÉ TICHE — to je slepé místo.
  * ⚠ PAST „N řádků s X“ (naměřeno 15. 10. 2026): věta „`tests/run_tests.gd`
    má **28 řádků s `has_method`**“ znamená 28 řádků, NA KTERÝCH se něco
    vyskytuje — ale parser ji čte jako TVRZENÍ O DÉLCE SOUBORU a hlásí
    `dokument 28 != zdroj 1569`. Je to falešný poplach z CHYBY ČTENÍ, ne vada
    dokumentu. `check_line_claims` proto tvrzení ve tvaru „N řádků s/se …“
    PŘESKAKUJE (počítá je do `kvalifikováno` v souhrnu). Cena: skutečné tvrzení
    o délce souboru napsané jako „má 30 řádků s kódem“ se taky přeskočí.
    Kdo v dokumentu vidí „28 vs 1569“, ať neopravuje dokument — je to tenhle čtenář.
  * Měřené okno je `DEFAULT_DOCS` (5 dokumentů: GDD, ADD, TDD, BRANY-HRY,
    README). `docs/DESIGN.md` a `docs/ARCHITEKTURA.md` jsou **historie**
    a vědomě se neměří — kdo je do okna přidá přes `--docs`, dostane nálezy,
    které platí pro historii, ne pro dnešek.
  * Výjimky nových kontrol (citace, blok `>`, HTML komentář, povolená výjimka)
    zkouší `_analyza/test-over-dokumenty.py` — sabotér je neumí vyjádřit,
    protože ten umí jen vložit vadu a čekat FAIL.
  * Ověřuje jen to, co je v `MUTATIONS` (sabotér) — nová třída tvrzení
    potřebuje novou mutaci, jinak může být kontrola slepá. Sabotér navíc
    ověřuje, že mutaci chytila SKUPINA, která ji chytit má (jinak by se
    „chyceno“ mohlo opřít o jinou kontrolu).

Použití:
  python _analyza/over-dokumenty.py [--docs docs/GDD.md,docs/ADD.md,docs/TDD.md]
  python _analyza/over-dokumenty.py --root .        # měří REPO (nic nemění)
  python _analyza/over-dokumenty.py --root . --selftest
      sabotér: vloží vady DO KOPIÍ V PAMĚTI a čeká FAIL.
      Na disku nic nemění — a sám to ověří hashem před/po (kdyby si soubor
      někdo rozepsal, hlásí `[REPO ZMĚNĚN]` a sabotér selže).
Exit: 0 = vše změřeno a v pořádku · 1 = něco nesouhlasí · 2 = něco zůstalo neměřeno
"""

import argparse
import hashlib
import io
import json
import os
import re
import sys
import unicodedata

DEFAULT_DOCS = ["docs/GDD.md", "docs/ADD.md", "docs/TDD.md",
                "docs/BRANY-HRY.md", "docs/README.md"]
REVIZE = "_analyza/DESIGN-REVIZE-2.md"
GDD = "docs/GDD.md"
# Dokumenty, které se skenují na ROZPOR se zákazy v GDD. Nejsou to primární
# dokumenty (`DEFAULT_DOCS`) — `docs/BRANY-HRY.md` se needituje stejnými
# kontrolami (nemá hlavičku ve tvaru GDD/ADD/TDD a odkazuje i mimo repo).
SOULAD_DOCS = ["docs/TDD.md", "docs/ADD.md", "docs/BRANY-HRY.md"]
# Oddíl „ZÁMĚRNĚ NENÍ“ se vyžaduje jen u ZDROJŮ PRAVDY: dokument, který něco
# tvrdí, musí říct, co do něj nepatří. Katalog bran (`BRANY-HRY.md`) a rejstřík
# (`README.md`) jsou znalost a rozcestník — jejich meze jsou v hlavičce a
# vyžadovat po nich rozsahovou sekci by byl falešný poplach (naměřeno 15. 10. 2026,
# když se oba dokumenty přidaly do `DEFAULT_DOCS`).
SCOPE_SECTION_DOCS = ["docs/GDD.md", "docs/ADD.md", "docs/TDD.md"]

OK, FAIL, UNMEASURED = "OK", "FAIL", "NEMĚŘENO"
WINDOW = 160          # znaků pro běžná tvrzení; u čísel v oddílu je větší
SECTION_WINDOW = 2500  # znaků uvnitř jednoho oddílu (stavové řádky smluv)
HEADER_LINES = 20      # hlavička dokumentu = prvních N řádků (kontrola `hlavicka`)

# --------------------------------------------------------------------------
# Slovníky pro nové kontroly (`hlavicka`, `soulad`, `neměřeno`)
# --------------------------------------------------------------------------
# `hlavicka`: DRUH dokumentu musí být pojmenovaný, ne jen „dokument“.
KIND_MARK = "Co tenhle dokument JE"
KIND_RX = re.compile(
    r"zdroj pravdy|historie|zrušen|záznam|snapshot|brán\w*|bran\w*|znalost|"
    r"katalog|rejstřík|rozcestník|zadání|návrh|katalog|design document|"
    r"specifikace|plán", re.IGNORECASE)
STAV_RX = re.compile(r"Odkud brát (?:dnešní |současný |aktuální )?stav", re.IGNORECASE)
KIND_LINES = 2         # druh se hledá na řádku značky + N následujících (okno se vypisuje)

# `soulad`: kmeny OBECNÝCH slov, která NENESOU předmět zákazu. Bere se název
# zákazu (tučná část buňky „Co tam není“) a zahodí se z něj slova, která jsou
# v dokumentech všude — jinak by „N5 UO datové soubory a klient“ sedlo na
# každou zmínku o souborech. U každého je naměřený důvod:
GENERIC_TERMS = frozenset((
    "skute",   # „skutečný obchod“, „skutečné materiály“ (N1)
    "pevne",   # „pevný tik“ (N2)
    "barev",   # „počet barev“ ve branách (N4)
    "datov",   # „datová vrstva“ (N5)
    "soubo",   # „soubor“ je v dokumentech stokrát (N5)
    "engin",   # „engine“ je jméno vrstvy v TDD (N6)
    "predm",   # „předmět“ je obsah hry, ne předmět zákazu (N6)
    "sily",    # „síla/síly“ je herní veličina (N6)
    "denni",   # „denní strop“ u offline dopočtu (N7)
    "aktiv",   # „aktivita“ je obecná (N8)
    "autom",   # „automaticky“ je obecné (N9)
    "hrace",   # „hráč“ je v každé druhé větě (N9)
    "hraji",   # dtto
    "pravid",   # „pravidlo“ je v každé druhé větě (N9)
    "pravi",   # „pravidlo“ je v každé druhé větě (N9)
    "povol",   # „povolání“ z `N2` koliduje s cue „povolené“ — naměřeno
               # 15. 10. 2026: zákaz lektvarů hlásil rozpor i u `N2`
    "jedno",   # „jeden/jednom“ je obecné (N10)
    "posta",   # „postava“ je obsah hry (N10)
    "vice",    # „více“ je obecné (N10)
    "veci", "vec",
))
# Slova, která jen nesou cue (nesmí se počítat mezi „zužující“ termíny).
CUE_WORDS = frozenset(("nesmi", "nesme", "zakaz", "nelze", "zakazan"))
STOP_TERMS = frozenset("""v ve na do pro s se si a i o u z ze k ke po pri pred
pod nad jako jsou je by byl byla bylo ne neni jen zez ktera ktery ktere kterou
toho tim tom te ten ta ty svuj sve svych ma maji mit mohl mohou muze muzou
nikdy zadny zadne vsechny vsechno take taky tedy tady tam mimo bez proti podle
pripadne ale nebo anebo""".split())

# Cue vzorce pro `soulad`. MUSÍ být úzké: široké („je součástí“, „může“) chytí
# správný text a vyrobí falešný poplach — naměřeno při psaní na GDD:60
# („Vazby mezi dovednostmi jsou součástí designu“ se četlo jako povolení).
ZAKAZ_CUE = re.compile(r"nesmi|nesmej|zakaz|zakazan|nelze|neni dovolen")
POVOL_CUE = re.compile(
    r"je v mvp|jsou v mvp|bude v mvp|budou v mvp|patri do mvp|"
    r"je povolen|jsou povolen|povolime|dovol|zaradime|bude zarazen|"
    r"zavedeme|pridame do mvp|pocita se s")
# Odvolání na zdroj = CITACE, ne tvrzení dokumentu (past (a) ze zadání).
ATRIB_RX = re.compile(r"\bn\d+\b|non-goal|non-goals|gdd|podle|cituje|doslova|zaznam")
# Markery, že GDD zákaz ZUŽUJE (výjimka) — výjimka se čte z dokumentu.
VYJIMKA_RX = re.compile(r"preformulovano|dovolen|vyjimk|plati dal pro|nove je|"
                        r"rozhodnuti uzivatele")
NONGOAL_ROW_RX = re.compile(
    r"^\|\s*(?P<code>N\d+)\s*\|\s*(?P<co>[^|]*)\|\s*(?P<proc>[^|]*)\|")
CLAUSE_RX = re.compile(r"[.;:!?—–]|\s+a\s+")

# `neměřeno`: registr jednotek, které vypadají jako VÝSLEDEK brány/testů a tudy
# měření NEMAJÍ. Jiné jednotky (smluv, ms, FPS) zůstávají tiché — viz docstring.
GATE_UNIT_RX = re.compile(
    r"(?P<v>\d+)\s+(?P<u>kontrol\w*|test(?:ů|u|y|em|ech)?|selhán\w*|funkc\w*|"
    r"volán\w*|nález\w*|chyb\w*)", re.IGNORECASE)
# Když text u čísla řekne, ODKUD je, není to nezměřené tvrzení (je to měření
# někoho jiného, které tenhle nástroj neumí zopakovat — a přiznává to).
SOURCE_RX = re.compile(r"naměřeno|měřeno|změřeno|měření|běh hlásí|staticky|výstup|"
                       r"os\.walk|grep|doloženo|z běhu|podle měření|čte z BĚHU|"
                       r"čítač|čte se")


def read_text(path):
    with io.open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def line_count(path):
    """Počet řádků podle splitlines() — NE Measure-Object -Line ani split('\\n')."""
    return len(read_text(path).splitlines())


def load_json(path):
    with io.open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class Report(object):
    def __init__(self):
        self.rows = []

    def add(self, state, group, what, detail=""):
        self.rows.append((state, group, what, detail))

    def count(self, state):
        return sum(1 for r in self.rows if r[0] == state)


def sections(docs):
    """Rozdělí dokumenty na oddíly podle nadpisů `##`/`###`/`####`.

    Vrací seznam (soubor, číslo_prvního_řádku, text_oddílu). Tvrzení o souboru
    patří do TOHOTO oddílu — okno přes celý dokument je past č. 2.
    """
    out = []
    for rel, text in docs:
        lines = text.splitlines()
        cur, start = [], 1
        for i, ln in enumerate(lines, start=1):
            if re.match(r"^#{2,4}\s", ln) and cur:
                out.append((rel, start, "\n".join(cur)))
                cur, start = [], i
            cur.append(ln)
        if cur:
            out.append((rel, start, "\n".join(cur)))
    return out


def claims(blocks, anchor, value, window=WINDOW, group="v",
           same_line=False, forbid=None):
    """Najde tvrzení `anchor` … (do `window` znaků) … `value`.

    Každá kotva se hledá SAMOSTATNĚ (ne jedním finditer přes celý text) —
    jinak by první nález „spolkl“ zbytek a další tvrzení by se nenašla.
    `forbid` je regex, který nesmí být MEZI kotvou a číslem (typicky jiný
    soubor: `\\.gd`), `same_line` zakáže přechod na další řádek.
    """
    gap_note = "na témže řádku" if same_line else "okno %d znaků" % window
    rx_a = re.compile(anchor)
    rx_v = re.compile(value)
    out, seen = [], set()
    for rel, base, text in blocks:
        for ma in rx_a.finditer(text):
            if same_line:
                # tvrzení musí být na TÉMŽE řádku (tabulkový řádek se nesmí přeskočit)
                nl = text.find("\n", ma.end())
                seg = text[ma.end(): nl if nl != -1 else len(text)][:window]
            else:
                seg = text[ma.end(): ma.end() + window]
            mv = rx_v.search(seg)
            if not mv:
                continue
            mid = seg[:mv.start()]
            if forbid and re.search(forbid, mid):
                continue
            raw = 0
            if group and group in mv.groupdict() and mv.group(group) is not None:
                raw = mv.group(group)
                try:
                    raw = int(raw)
                except ValueError:
                    pass          # hodnota je text (např. název projektu)
            ln = base + text.count("\n", 0, ma.start())
            # kontext i PŘED nálezem: rozhoduje o tom, je-li to citace, nebo
            # tvrzení o dnešku (naměřeno: „před opravou“ stálo před kotvou)
            start = max(0, ma.start() - 70)
            snippet = re.sub(r"\s+", " ", text[start: ma.end() + mv.end()]).strip()
            if start > 0:
                snippet = "…" + snippet
            key = (rel, ln, str(raw))
            if key in seen:
                continue
            seen.add(key)
            out.append((rel, ln, snippet, raw))
    return out


def claims_value(blocks, value, group="v"):
    """Tvrzení, které je SELF-CONTAINED (`8 slotů` se neplete s ničím jiným)."""
    rx = re.compile(value)
    out, seen = [], set()
    for rel, base, text in blocks:
        for m in rx.finditer(text):
            raw = m.group(group) if group in m.groupdict() else 0
            try:
                raw = int(raw)
            except (TypeError, ValueError):
                pass
            ln = base + text.count("\n", 0, m.start())
            key = (rel, ln, str(raw))
            if key in seen:
                continue
            seen.add(key)
            out.append((rel, ln, re.sub(r"\s+", " ", m.group(0)).strip(), raw))
    return out


def report_claims(rep, label, found, measured, note=""):
    if not found:
        rep.add(UNMEASURED, "čísla", label,
                "tvrzení se v dokumentech nenašlo%s" % ((" (%s)" % note) if note else ""))
        return
    for rel, ln, snippet, v in found:
        if v == measured:
            rep.add(OK, "čísla", "%s:%d %s" % (rel, ln, label),
                    "dokument %s = zdroj %s | %s" % (v, measured, snippet[:120]))
        else:
            rep.add(FAIL, "čísla", "%s:%d %s" % (rel, ln, label),
                    "dokument %s != zdroj %s | %s" % (v, measured, snippet[:120]))


# --------------------------------------------------------------------------
# Měření zdrojů
# --------------------------------------------------------------------------
def measure_script_lines(root, name):
    return line_count(os.path.join(root, "scripts", name))


def measure_json_records(root, name):
    return len(load_json(os.path.join(root, "assets", "data", name)))


def measure_has_method(root):
    lines = read_text(os.path.join(root, "tests", "run_tests.gd")).splitlines()
    return sum(1 for ln in lines if "has_method" in ln), sum(ln.count("has_method") for ln in lines)


def measure_input_actions(root):
    return len(re.findall(r"^input/", read_text(os.path.join(root, "project.godot")),
                          flags=re.MULTILINE))


def measure_config_name(root):
    m = re.search(r'config/name="([^"]*)"', read_text(os.path.join(root, "project.godot")))
    return m.group(1) if m else None


def heading_numbers(text):
    nums = set()
    for line in text.splitlines():
        m = re.match(r"^#{2,4}\s+(\d+(?:\.\d+)*)[.)]?\s", line)
        if m:
            nums.add(m.group(1))
    return nums


# --------------------------------------------------------------------------
# Kontroly
# --------------------------------------------------------------------------
def is_citation(snippet):
    """Je nález CITACE dřívějšího stavu, nebo TVRZENÍ o dnešku?

    Naměřeno 8. 10. 2026: týž vzor zabral na „před opravou říkaly
    `project.godot` a `assets/spec.json` `uo-sandbox`“ — to je **citace**
    historické hodnoty, ne tvrzení o dnešku. Brána, která to nerozliší, hlásí
    `exit 1` ze špatného důvodu. Rozhoduje KONTEXT nálezu, a proto se vypisuje.
    """
    markers = ("před opravou", "před přepsáním", "dřív", "dříve", "původně",
               "ve svém čase", "historicky", "naměřeno dřív", "bývalo", "zastaralé")
    return any(m in snippet for m in markers)


def check_cross_refs(root, docs, rep):
    revize_path = os.path.join(root, REVIZE)
    if not os.path.exists(revize_path):
        rep.add(UNMEASURED, "odkazy", "zdroj rozhodnutí %s" % REVIZE, "soubor není")
        return
    known = {
        "REVIZE": heading_numbers(read_text(revize_path)),
        "GDD": heading_numbers(read_text(os.path.join(root, "docs", "GDD.md"))),
        "TDD": heading_numbers(read_text(os.path.join(root, "docs", "TDD.md"))),
        "ADD": heading_numbers(read_text(os.path.join(root, "docs", "ADD.md"))),
    }
    checked = bad = 0
    for rel, text in docs:
        for i, line in enumerate(text.splitlines(), start=1):
            for m in re.finditer(r"[\(„]§(\d+(?:\.\d+)*)", line):
                checked += 1
                if m.group(1) not in known["REVIZE"]:
                    bad += 1
                    rep.add(FAIL, "odkazy", "%s:%d odkaz na §%s" % (rel, i, m.group(1)),
                            "v %s takový oddíl NENÍ | %s" % (REVIZE, line.strip()[:110]))
            for doc, nums in known.items():
                if doc == "REVIZE":
                    continue
                for m in re.finditer(r"`%s`\s*§(\d+(?:\.\d+)*)" % doc, line):
                    checked += 1
                    if m.group(1) not in nums:
                        bad += 1
                        rep.add(FAIL, "odkazy", "%s:%d odkaz na `%s` §%s"
                                % (rel, i, doc, m.group(1)),
                                "takový oddíl v %s.md NENÍ | %s" % (doc, line.strip()[:110]))
    rep.add(OK if bad == 0 else FAIL, "odkazy", "odkazy §N proti zdrojům",
            "zkontrolováno %d odkazů, vadných %d" % (checked, bad))


def check_paths(root, docs, rep):
    prefixes = ("scripts/", "assets/", "docs/", "tools/", ".forge/", "tests/",
                "_analyza/", "_retired/", ".github/")
    missing_words = ("neexistuje", "NEEXISTUJE", "není", "NENÍ", "chybí", "CHYBÍ",
                     "smazaný", "smazán", "0 B", "nejsou", "NENAŠEL")
    # Cesta, kterou dokument sám umisťuje MIMO tenhle rep (orchestra, šablona),
    # není tvrzení o tomhle repu — naměřeno 15. 10. 2026: `BRANY-HRY.md:41`
    # zmiňuje `tools/over-dokumentaci.py` v orchestra a brána to hlásila jako
    # neexistující cestu tady.
    foreign_words = ("v orchestra", "orchestry", "v šabloně", "šablony",
                     "mimo tenhle rep", "mimo repo", "v jiném repu", "v cizím repu")
    rx = re.compile(r"`([A-Za-z0-9_\-./]+)`")
    checked = bad = foreign = 0
    for rel, text in docs:
        for i, line in enumerate(text.splitlines(), start=1):
            for m in rx.finditer(line):
                p = m.group(1)
                if not p.startswith(prefixes) or "*" in p or p.endswith("/"):
                    continue
                checked += 1
                if os.path.exists(os.path.join(root, p.replace("/", os.sep))):
                    continue
                low = line.lower()
                if any(w in line for w in missing_words):
                    rep.add(OK, "cesty", "%s:%d `%s`" % (rel, i, p),
                            "cesta neexistuje a dokument to ŘÍKÁ | %s" % line.strip()[:110])
                elif any(w in low for w in foreign_words):
                    foreign += 1
                    rep.add(OK, "cesty", "%s:%d `%s`" % (rel, i, p),
                            "cesta je MIMO tenhle rep a dokument to říká | %s"
                            % line.strip()[:110])
                else:
                    bad += 1
                    rep.add(FAIL, "cesty", "%s:%d `%s`" % (rel, i, p),
                            "cesta NEEXISTUJE a dokument to neříká | %s" % line.strip()[:110])
    rep.add(OK if bad == 0 else FAIL, "cesty", "cesty v backtickách",
            "zkontrolováno %d cest, vadných %d (z toho mimo rep vysvětleno %d)"
            % (checked, bad, foreign))


def resolve(root, path):
    """Najde soubor z tvrzení. Když je cesta v dokumentu holé jméno
    (`main.json`), hledá se v obvyklých adresářích — jinak by se tvrzení
    TIŠE PŘESKOČILO (naměřeno: „`main.json` (87 řádků, 14 klíčů)“ se
    neověřovalo, protože `main.json` v kořeni repa není).
    Vrací (absolutní_cesta nebo None, relativní_cesta_pro_report).
    """
    direct = os.path.join(root, path.replace("/", os.sep))
    if os.path.exists(direct):
        return direct, path
    if "/" not in path:
        for d in ("assets/levels", "assets/data", "assets/tiles", "assets/sprites",
                  "tools", "tools/blender", "docs", ".forge", "tests", "scripts"):
            cand = os.path.join(root, d.replace("/", os.sep), path)
            if os.path.exists(cand):
                return cand, d + "/" + path
    return None, path


def check_line_claims(root, blocks, rep):
    """Tvrzení „N řádků“ se váže na NEJBLIŽŠÍ PŘEDCHÁZEJÍCÍ zmínku o souboru.

    Takhle to čte člověk: v oddílu `### 3.7 Player — scripts/player.gd` je
    „191 řádků“ tvrzení o `player.gd`, ne o souboru, který je o dva odstavce
    výš. Kotva na jméno souboru proto NESTAČÍ (naměřeno: „`game.gd`; naměřeno
    8. 10. 2026: `main.tscn` má **6 řádků**“ hlásilo „game.gd má 6 řádků“).
    """
    file_rx = re.compile(r"`([A-Za-z0-9_\-./]+\.[a-z]{2,4})`")
    claim_rx = re.compile(r"(?P<v>\d+) (?P<unit>řádk\w*|klíč\w*)")
    # tvrzení kvalifikované symbolem není tvrzení o souboru
    # (naměřeno: „`tests/run_tests.gd` … `has_method` má **26 řádků**“ se
    #  přiřadilo souboru a hlásilo 26 != 1406)
    qualified_rx = re.compile(r"(has_method|`\w+`)\s*(má|na)?\s*\**\s*$")
    checked = skipped = skipped_qual = 0
    for rel, base, text in blocks:
        for mv in claim_rx.finditer(text):
            if qualified_rx.search(text[max(0, mv.start() - 40):mv.start()]):
                skipped += 1
                continue
            # „N řádků s `has_method`“ NENÍ tvrzení o délce souboru, ale počet
            # řádků, na kterých se něco vyskytuje. Naměřeno 15. 10. 2026:
            # `BRANY-HRY.md` („má 28 řádků s `has_method`“) brána četla jako
            # „soubor má 28 řádků“ a hlásila `28 != 1569` — falešný poplach
            # z chyby čtení, ne vada dokumentu.
            if re.match(r"\s*(?:s|se)\s+\S", text[mv.end():mv.end() + 24]):
                skipped_qual += 1
                continue
            prev = None
            for mf in file_rx.finditer(text, 0, mv.start()):
                prev = mf
            if prev is None or mv.start() - prev.end() > 200:
                # dlouhá mezera = tvrzení se k tomu souboru neváže (naměřeno:
                # „Dnes 16 řádků × 30 znaků“ o MŘÍŽCE se přiřadilo `main.json`)
                skipped += 1
                continue
            path = prev.group(1)
            full, shown = resolve(root, path)
            if full is None:
                skipped += 1
                continue
            measured = line_count(full)
            unit = mv.group("unit")
            if unit.startswith("klíč"):
                if not full.endswith(".json"):
                    skipped += 1
                    continue
                measured = len(load_json(full))
            claimed = int(mv.group("v"))
            ln = base + text.count("\n", 0, mv.start())
            snippet = re.sub(r"\s+", " ", text[prev.start(): mv.end()]).strip()
            state = OK if claimed == measured else FAIL
            rep.add(state, "čísla", "%s:%d %s %s" % (rel, ln, unit, shown),
                    "dokument %s %s zdroj %s | %s"
                    % (claimed, "==" if state == OK else "!=", measured, snippet[:120]))
            checked += 1
    rep.add(OK, "čísla", "tvrzení o počtu řádků a klíčů",
            "zkontrolováno %d (nepřiřazeno %d — bez blízkého souboru, "
            "kvalifikováno %d — „N řádků s X“ není délka souboru)"
            % (checked, skipped, skipped_qual))


def check_numbers(root, docs, blocks, rep):
    check_line_claims(root, blocks, rep)

    # --- prázdný world.gd
    report_claims(rep, "velikost scripts/world.gd",
                  claims(blocks, r"world\.gd", r"(?P<v>\d+) B", window=200),
                  os.path.getsize(os.path.join(root, "scripts", "world.gd")))

    # --- tabulky v TDD §4.1 (záznamů na soubor) — tvrzení je na JEDNOM řádku
    for fname in ("materials.json", "skills.json", "recipes.json",
                  "monsters.json", "items.json"):
        report_claims(rep, "záznamů %s" % fname,
                      claims(blocks, re.escape(fname), r"\| (?P<v>\d+) \|", same_line=True),
                      measure_json_records(root, fname))

    # --- dnešní obsah (tvrzení o DNEŠKU, ne o cíli); kmen slova kvůli pádům
    today = r"(?:naměřeno|dnešní stav)"
    for label, stem, fname in (("materiály", "materiál", "materials.json"),
                               ("dovednosti", "dovednost", "skills.json"),
                               ("recepty", "recept", "recipes.json"),
                               ("nestvůry", "nestvůr", "monsters.json"),
                               ("předměty", "předmět", "items.json")):
        report_claims(rep, "dnešní obsah: %s" % label,
                      claims(blocks, today, r"(?P<v>\d+) %s" % stem, window=120),
                      measure_json_records(root, fname))

    # --- roadmapa (kotva „roadmapa/roadmap.json“, aby se nechytilo „13 granul je done“)
    rm = load_json(os.path.join(root, ".forge", "roadmap.json"))
    grains = rm["grains"]
    report_claims(rep, "granulí v roadmapě",
                  claims(blocks, r"roadmap(?:a|y|\.json)", r"(?P<v>\d+) granul",
                         window=200),
                  len(grains))
    report_claims(rep, "granul s done: true",
                  claims(blocks, r"done: true", r"(?P<v>\d+)", window=20),
                  sum(1 for g in grains if g.get("done") is True))

    # --- spec.json
    spec = load_json(os.path.join(root, "assets", "spec.json"))
    report_claims(rep, "rolí ve spec.json",
                  claims(blocks, r"Role \(", r"(?P<v>\d+)\)", window=8),
                  len(spec["role"]))
    report_claims(rep, "slotů vrstev",
                  claims_value(blocks, r"(?P<v>\d+) slotů"),
                  len(spec["vrstvy"]["slot_poradi"]))
    report_claims(rep, "startovní sada",
                  claims(blocks, r"startovní sada", r"(?P<v>\d+)", window=8),
                  len(spec["vrstvy"]["pocatecni_sada"]))
    report_claims(rep, "bran ve spec.json",
                  claims(blocks, r"Brány \(", r"(?P<v>\d+)\)", window=8),
                  len([k for k in spec["gates"] if not k.startswith("_")]))

    # --- testy: HRUBÝ počet has_method (řádky i výskyty)
    # Tvrzení se hledá v OBOU slovosledech: „`has_method` má 28 řádků“ i
    # „má 28 řádků s `has_method`“ (= řádky, na kterých se vyskytuje). Druhý
    # tvar `check_line_claims` přeskočí (jinak by ho četl jako délku souboru) —
    # proto se měří TADY, aby nezůstal ani falešný poplach, ani slepé místo.
    rows, occ = measure_has_method(root)
    found_rows = (claims(blocks, r"has_method", r"(?P<v>\d+) řádků", window=30)
                  + claims_value(blocks, r"(?P<v>\d+) řádků s `has_method`"))
    report_claims(rep, "has_method řádků", found_rows, rows)
    report_claims(rep, "has_method výskytů",
                  claims(blocks, r"has_method", r"(?P<v>\d+) výskytů", window=60), occ)

    # --- vstupní akce (tvrzení: [input] má jen input_devices → 0 akcí)
    acts = measure_input_actions(root)
    found = claims(blocks, r"\[input\]", r"input_devices")
    if not found:
        rep.add(UNMEASURED, "čísla", "[input] nemá vstupní akce", "tvrzení se nenašlo")
    for rel, ln, snippet, _ in found:
        rep.add(OK if acts == 0 else FAIL, "čísla", "%s:%d [input] nemá akce" % (rel, ln),
                "změřeno vstupních akcí: %d | %s" % (acts, snippet[:110]))

    # --- název projektu v project.godot
    name = measure_config_name(root)
    found = claims(blocks, r"project\.godot", r"`(?P<v>uo\-[a-z]+)`")
    if not found:
        rep.add(UNMEASURED, "čísla", "název v project.godot", "tvrzení se nenašlo")
    for rel, ln, snippet, v in found:
        if is_citation(snippet):
            rep.add(OK, "čísla", "%s:%d název v project.godot (citace)" % (rel, ln),
                    "citace dřívější hodnoty, ne tvrzení o dnešku | %s" % snippet[:110])
            continue
        rep.add(OK if v == name else FAIL, "čísla",
                "%s:%d název v project.godot" % (rel, ln),
                "dokument %s, zdroj %s | %s" % (v, name, snippet[:110]))


def check_placeholders(docs, rep):
    bad = 0
    for rel, text in docs:
        for i, line in enumerate(text.splitlines(), start=1):
            if re.search(r"\b(TODO|TBD|FIXME|XXX)\b", line):
                bad += 1
                rep.add(FAIL, "placeholdery", "%s:%d" % (rel, i), line.strip()[:130])
    rep.add(OK if bad == 0 else FAIL, "placeholdery", "TODO/TBD/FIXME",
            "nalezeno %d" % bad)


def check_header_and_sections(docs, rep):
    """Hlavička kdekoliv v textu (původní, mírnější kontrola).

    Dvě věci jsou tu schválně VOLNĚJŠÍ než dřív (naměřeno 15. 10. 2026, když se
    do `DEFAULT_DOCS` přidal `BRANY-HRY.md` a `README.md`):
      * „Odkud brát stav“ se hledá jako VZOREC — `BRANY-HRY.md` má legitimně
        „Odkud brát **dnešní** stav“ a pevný řetězec ho hlásil jako vadu.
      * oddíl „ZÁMĚRNĚ NENÍ“ se vyžaduje jen u zdrojů pravdy
        (`SCOPE_SECTION_DOCS`) — katalog bran a rejstřík ho mít nemusí.
    """
    for rel, text in docs:
        needles = [("Co tenhle dokument JE", "hlavička: čím je"),
                   (STAV_RX, "hlavička: odkud stav")]
        if rel in SCOPE_SECTION_DOCS:
            needles.append(("ZÁMĚRNĚ NENÍ", "sekce: co tam záměrně není"))
        for needle, label in needles:
            found = (needle.search(text) if hasattr(needle, "search") else needle in text)
            state = OK if found else FAIL
            rep.add(state, "hlavička", "%s: %s" % (rel, label),
                    "nalezeno" if state == OK else "CHYBÍ")


def check_language(docs, rep):
    diac = set("áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ")
    for rel, text in docs:
        n = sum(1 for ch in text if ch in diac)
        rep.add(OK if n > 200 else FAIL, "jazyk", "%s: diakritika" % rel,
                "%d znaků s diakritikou" % n)
    for rel in [d[0] for d in docs] + [REVIZE, "_analyza/over-dokumenty.py",
                                       "_analyza/test-over-dokumenty.py",
                                       "_analyza/NAVRH-ROADMAPY-M0-M6.md",
                                       "_analyza/roadmap-navrh.json"]:
        if not os.path.exists(rel):
            continue
        bad = open(rel, "rb").read(3) == b"\xef\xbb\xbf"
        rep.add(FAIL if bad else OK, "jazyk", "%s: BOM" % rel,
                "BOM nalezen (vadí!)" if bad else "bez BOM")


def check_json(rep):
    rel = "_analyza/roadmap-navrh.json"
    if not os.path.exists(rel):
        rep.add(UNMEASURED, "json", rel, "soubor není")
        return
    try:
        data = load_json(rel)
        ids = [g["id"] for g in data.get("grains", [])]
        rep.add(OK, "json", rel, "validní, %d granulí: %s" % (len(ids), ", ".join(ids)))
    except Exception as exc:  # noqa: BLE001
        rep.add(FAIL, "json", rel, "NENÍ validní JSON: %s" % exc)


def check_hlavicka(docs, rep):
    """NOVÉ: hlavička MUSÍ být v prvních `HEADER_LINES` řádcích a říct DRUH.

    Původní `check_header_and_sections` hledá značky kdekoliv v dokumentu —
    takže projde i dokument, který svou roli přizná až v polovině. Tahle
    kontrola měří totéž, ale s OKNEM: `HEADER_LINES` řádků, a DRUH bere
    z uzavřeného slovníku `KIND_RX` (ne jen „tenhle dokument“). Druh se hledá
    na řádku značky a `KIND_LINES` řádcích za ním — jinak by ho „splnilo“
    slovo „historie“ o dva odstavce níž (naměřeno: TDD ho má na řádku 9
    o `ARCHITEKTURA.md`, ADD na řádku 22 o „návrhu vzhledu“).
    """
    for rel, text in docs:
        lines = text.splitlines()
        head_lines = lines[:HEADER_LINES]
        head = "\n".join(head_lines)
        if len(lines) > HEADER_LINES:
            where = "okno: prvních %d řádků (soubor má %d)" % (HEADER_LINES, len(lines))
        else:
            where = ("okno: celý soubor (%d řádků, méně než %d)"
                     % (len(lines), HEADER_LINES))
        missing = []
        mark_i = next((i for i, ln in enumerate(head_lines) if KIND_MARK in ln), None)
        if mark_i is None:
            missing.append("značka „%s“" % KIND_MARK)
            kind_where = "druh se hledá na řádku značky + %d řádků" % KIND_LINES
            mk = None
        else:
            win = head_lines[mark_i: mark_i + KIND_LINES + 1]
            mk = KIND_RX.search("\n".join(win))
            kind_where = ("druh se hledá na řádku značky + %d řádků (řádky %d–%d)"
                          % (KIND_LINES, mark_i + 1, mark_i + len(win)))
        if mk is None:
            missing.append("DRUH dokumentu (zdroj pravdy / historie / brána / záznam)")
        ms = STAV_RX.search(head)
        if ms is None:
            missing.append("ODKUD BRÁT STAV")
        if missing:
            rep.add(FAIL, "hlavicka", rel,
                    "%s | %s | CHYBÍ: %s" % (where, kind_where, "; ".join(missing)))
        else:
            win_text = "\n".join(head_lines[mark_i: mark_i + KIND_LINES + 1])
            kind_ln = mark_i + 1 + win_text[:mk.start()].count("\n")
            stav_ln = head[:ms.start()].count("\n") + 1
            rep.add(OK, "hlavicka", rel,
                    "%s | %s na řádku %d | stav („%s“) na řádku %d"
                    % (where, "druh „%s“" % mk.group(0), kind_ln,
                       ms.group(0), stav_ln))


# --------------------------------------------------------------------------
# Vnitřní soulad dokumentů (`soulad`) — zákazy z GDD proti ostatním dokumentům
# --------------------------------------------------------------------------
def norm_cz(text):
    """Malá písmena bez diakritiky a bez markdownu — pro porovnávání kmenů."""
    low = unicodedata.normalize("NFD", text.lower())
    low = "".join(c for c in low if unicodedata.category(c) != "Mn")
    return low.replace("**", " ").replace("`", " ")


def term_stem(word):
    """Kmen slova (prvních 5 znaků). `None` = slovo je moc krátké na předmět.

    Krátká ZKRATKA se drží („MMO“ v `N1` je to, co zákaz odlišuje), ale
    dvouznaková ne — „UO“ z `N5` je v repu v názvu projektu na každém řádku.
    """
    w = re.sub(r"[^0-9a-z]+", "", norm_cz(word))
    if len(w) >= 4:
        return w[:5]
    if len(w) >= 3 and word.isupper():
        return w[:5]
    return None


def subject_terms(text, drop=GENERIC_TERMS):
    """Předmětová slova zákazu (kmeny) — bez spojek a bez obecných slov."""
    out = set()
    for w in re.findall(r"[0-9A-Za-zěščřžýáíéúůňťďóĚŠČŘŽÝÁÍÉÚŮŇŤĎÓ]+", text):
        if norm_cz(w) in STOP_TERMS:
            continue
        s = term_stem(w)
        if s and s not in drop:
            out.add(s)
    return out


def nongoal_rows(gdd_text):
    """Načte tabulku non-goals z GDD: kód, řádek a NÁZEV zákazu (tučná část)."""
    rows = []
    for i, line in enumerate(gdd_text.splitlines(), start=1):
        m = NONGOAL_ROW_RX.match(line)
        if not m:
            continue
        cell = m.group("co")
        bold = " ".join(re.findall(r"\*\*(.+?)\*\*", cell)) or cell
        rows.append({"code": m.group("code"), "line": i,
                     "cell": re.sub(r"\s+", " ", cell).strip(),
                     "bold": re.sub(r"\s+", " ", bold).strip()})
    return rows


def narrow_terms(gdd_lines, row, span=10):
    """Kmeny, kterými GDD zákaz ZUŽUJE (výjimka) — čtou se Z GDD.

    Výjimka se nepozná podle kódu nástroje, ale podle dokumentu: hledá se
    zmínka kódu zákazu (`N9`) mimo tabulku, která nese marker výjimky
    („PŘEFORMULOVÁNO“, „dovolené“, „výjimka“), a v jejím okně `span` řádků
    se vytáhnou slova za „nesmí/zakaz…“ — to je ZUŽENÝ zákaz („hra nesmí
    rozhodnout za hráče“). Odečtou se slova, která už jsou v názvu zákazu
    (ta zužovat nemohou), a slova, která jen nesou cue.
    Vrací (kmeny, velikost okna v řádcích) — okno se vypisuje, protože
    velkorysé okno není opatrnost, je to slepota.
    """
    code = row["code"]
    cell_terms = subject_terms(row["cell"], drop=frozenset())
    hits = [i for i, ln in enumerate(gdd_lines)
            if re.search(r"\b%s\b" % re.escape(code), ln)
            and VYJIMKA_RX.search(norm_cz(ln))]
    if not hits:
        return set(), 0
    lo = max(0, hits[0] - span)
    hi = min(len(gdd_lines), hits[-1] + span + 1)
    block = gdd_lines[lo:hi]
    extra = set()
    for ln in block:
        for m in re.finditer(r"(?:nesmi|nesmej|zakaz\w*)\s+(.{0,90}?)(?=[.;—]|$)",
                             norm_cz(ln)):
            extra |= subject_terms(m.group(1), drop=frozenset())
    return (extra - cell_terms - GENERIC_TERMS - CUE_WORDS), len(block)


def statement_lines(text):
    """Řádky, které jsou TVRZENÍM dokumentu.

    Bloková citace (`>` na začátku) a HTML komentář `<!-- -->` se PŘESKAKUJÍ —
    text, který zákaz jen cituje nebo se na něj odvolává, se nesmí hlásit
    jako rozpor (past (a) ze zadání).
    """
    out, in_comment = [], False
    for i, line in enumerate(text.splitlines(), start=1):
        if "<!--" in line:
            in_comment = True
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if line.lstrip().startswith(">"):
            continue
        out.append((i, line, norm_cz(line)))
    return out


def scan_contradictions(text, terms, narrow):
    """Tvrzení, která odporují zákazu s předmětovými kmeny `terms`.

    Kandidát = KLAUZULE, ve které je předmět zákazu i cue (zákaz/povolení).
    Rozpor to je jen tehdy, když se klauzule neodvolává na zdroj (to je
    citace) a nezužuje zákaz slovy z GDD (to je povolená výjimka).
    Vrací (nálezy, počet kandidátů) — počet kandidátů se vypisuje, aby bylo
    vidět, že kontrola na dokument skutečně sahala.
    """
    fires, considered = [], 0
    for ln, raw, low in statement_lines(text):
        if not any(t in low for t in terms):
            continue
        for clause in CLAUSE_RX.split(low):
            clause = clause.strip()
            if not clause:
                continue
            zak, pov = ZAKAZ_CUE.search(clause), POVOL_CUE.search(clause)
            if not (zak or pov):
                continue
            considered += 1
            if any(t in clause for t in narrow) or ATRIB_RX.search(clause):
                continue
            # ZAKÁZÁNÍ POVOLENÉHO se hlásí JEN u zákazu, který GDD zužuje
            # (výjimka). Když výjimka není, je zákaz v jiném dokumentu
            # ve SHODĚ s GDD — a hlásit shodu jako rozpor je falešný poplach
            # (naměřeno 15. 10. 2026: `N4` a „Zákazy stylu“ v ADD).
            if zak and narrow:
                fires.append((ln, raw.strip(),
                              "zakazuje šířeji, než GDD (to zužuje na: %s)"
                              % ", ".join(sorted(narrow))))
            elif pov:
                fires.append((ln, raw.strip(), "povoluje, co GDD zakazuje"))
    # jedna vada na řádek (věta může mít víc klauzulí se stejným nálezem)
    unique, seen = [], set()
    for fire in fires:
        if fire[0] in seen:
            continue
        seen.add(fire[0])
        unique.append(fire)
    return unique, considered


def check_soulad(root, docs, extra_docs, rep):
    """NOVÉ: zákazy z GDD (`N1`–`N11`) proti tvrzením v ostatních dokumentech."""
    by_rel = dict(docs)
    for rel, text in extra_docs:
        by_rel[rel] = text
    missing = [rel for rel in SOULAD_DOCS if rel not in by_rel]
    for rel in missing:
        rep.add(UNMEASURED, "soulad", "proti %s" % rel,
                "dokument pro kontrolu souladu není k dispozici — "
                "nesoulad proti němu zůstal NEMĚŘEN (to není zelená)")
    gdd_text = by_rel.get(GDD)
    if gdd_text is None:
        rep.add(UNMEASURED, "soulad", "zdroj zákazů %s" % GDD,
                "dokument není k dispozici — zákazy není odkud číst")
        return
    rows = nongoal_rows(gdd_text)
    if not rows:
        rep.add(UNMEASURED, "soulad", "tabulka non-goals v %s" % GDD,
                "řádky `| N1 | … |` se nenašly — zákazy není odkud číst")
        return
    targets = sorted((rel, text) for rel, text in by_rel.items() if rel != GDD)
    gdd_lines = gdd_text.splitlines()
    total = 0
    for row in rows:
        terms = subject_terms(row["bold"])
        label = "%s (GDD:%d)" % (row["code"], row["line"])
        if not terms:
            rep.add(UNMEASURED, "soulad", label,
                    "název zákazu „%s“ je celý z obecných slov — není co hledat"
                    % row["bold"][:60])
            continue
        narrow, win = narrow_terms(gdd_lines, row)
        fires, cand = [], 0
        for rel, text in targets:
            found, seen = scan_contradictions(text, terms, narrow)
            cand += seen
            for ln, raw, why in found:
                fires.append((rel, ln, raw, why))
        total += len(fires)
        if fires:
            for rel, ln, raw, why in fires:
                rep.add(FAIL, "soulad", "%s:%d %s" % (rel, ln, row["code"]),
                        "GDD:%d „%s“ × %s:%d „%s“ — %s"
                        % (row["line"], row["cell"][:70], rel, ln, raw[:90], why))
        else:
            rep.add(OK, "soulad", label,
                    "předmět: %s | výjimka: %s (okno %d ř.) | kandidátů %d | rozporných 0"
                    % (", ".join(sorted(terms)),
                       ", ".join(sorted(narrow)) or "—", win, cand))
    state = FAIL if total else (UNMEASURED if missing else OK)
    rep.add(state, "soulad", "zákazy N1–N11 proti %s"
            % ", ".join(rel for rel, _ in targets),
            "změřeno %d zákazů, rozporných tvrzení %d" % (len(rows), total))


def check_unmeasured_counts(docs, rep):
    """NOVÉ: počty, pro které brána měření NEMÁ — se zdrojem OK, bez zdroje NEMĚŘENO.

    Naměřeno (sabotážní pokus 15. 10. 2026): věta „Hra ma 500 kontrol a vsechny
    jsou zelene.“ v `docs/GDD.md` prošla jako tiché OK, protože na ni žádná
    kontrola nesahala. Nově každé číslo z registru `GATE_UNIT_RX` buď má
    v okně (řádek před + řádek sám) uvedený ZDROJ, nebo je to citace výstupu
    v backtickách — a jinak končí jako NEMĚŘENO, ne jako zelená.
    """
    checked = sourced = 0
    for rel, text in docs:
        lines = text.splitlines()
        for i, line in enumerate(lines, start=1):
            for m in GATE_UNIT_RX.finditer(line):
                checked += 1
                claim = re.sub(r"\s+", " ", m.group(0))
                ctx = "\n".join(lines[max(0, i - 2): i + 1])
                in_code = (line.count("`", 0, m.start()) % 2 == 1
                           and line.count("`", 0, m.end()) % 2 == 1)
                src = SOURCE_RX.search(ctx)
                if in_code or src:
                    sourced += 1
                    if src:
                        why = "text uvádí zdroj: „%s“" % src.group(0)
                    else:
                        why = "citace výstupu v backtickách"
                    rep.add(OK, "neměřeno", "%s:%d %s" % (rel, i, claim),
                            "počet mimo měření brány, ale je doložený (%s)" % why)
                else:
                    rep.add(UNMEASURED, "neměřeno", "%s:%d %s" % (rel, i, claim),
                            "počet, který brána neumí změřit, a text NEUVÁDÍ, odkud "
                            "je (okno: řádky %d–%d) | %s"
                            % (max(1, i - 1), i, line.strip()[:110]))
    if checked == 0:
        rep.add(UNMEASURED, "neměřeno", "počty z registru (kontrol/testů/funkcí/…)",
                "v dokumentech není ani jedno takové tvrzení — kontrola nemá "
                "co měřit (to není zelená)")
    else:
        rep.add(OK, "neměřeno", "počty z registru (kontrol/testů/funkcí/…)",
                "nalezeno %d tvrzení, z toho se zdrojem %d" % (checked, sourced))


def run_checks(root, docs, extra_docs=()):
    blocks = sections(docs)
    rep = Report()
    check_cross_refs(root, docs, rep)
    check_paths(root, docs, rep)
    check_numbers(root, docs, blocks, rep)
    check_placeholders(docs, rep)
    check_header_and_sections(docs, rep)
    check_hlavicka(docs, rep)
    check_soulad(root, docs, extra_docs, rep)
    check_unmeasured_counts(docs, rep)
    check_language(docs, rep)
    check_json(rep)
    return rep


# Sabotér: kdyby kontrola neměla jak selhat, byla by zelená vždycky.
# Každá mutace vrací do dokumentu VADU a kontrola ji MUSÍ chytit.
#   4 prvky = původní mutace (čeká se FAIL kdekoliv),
#   5. prvek = co se čeká (`FAIL`, `NEMĚŘENO`, nebo `CISTE` = ZÁPORNÝ test,
#              kdy kontrola hlásit NESMÍ — falešný poplach je dražší),
#   6. prvek = SKUPINA, která to má chytit — bez toho by „chyceno“ mohlo
#              znamenat cokoli (naměřeno: staré mutace chytá i jiná kontrola).
# POZOR: mutace se vkládají do KOPIÍ v paměti, ne do souborů (viz `selftest`).
MUTATIONS = [
    ("docs/TDD.md", "**377 řádků**", "**376 řádků**", "špatný počet řádků"),
    ("docs/TDD.md", "(§11)", "(§99)", "odkaz na neexistující oddíl"),
    ("docs/GDD.md", "(GDD §8.2)", "(§8.2)", "interní odkaz zapsaný jako odkaz na zdroj rozhodnutí"),
    ("docs/ADD.md", "**8 slotů**", "**9 slotů**", "špatný počet slotů vrstev"),
    ("docs/GDD.md", "**4 materiály, 4 dovednosti, 3 recepty, 1 nestvůra a 2 předměty**",
     "**5 materiálů, 4 dovednosti, 3 recepty, 1 nestvůra a 2 předměty**",
     "špatný dnešní obsah"),
    ("docs/TDD.md", "`roadmap.json`: 21 granul", "`roadmap.json`: 23 granul",
     "špatný počet granulí"),
    ("docs/ADD.md", " — a **žádný z těch tří adresářů v repu není** (naměřeno)", "",
     "cesta, která neexistuje, a dokument to neříká"),
    ("docs/TDD.md", "`project.godot` = `uo-shadows`", "`project.godot` = `uo-sandbox`",
     "tvrzení o DNEŠKU se špatným názvem (nesmí projít jako citace)"),
    ("docs/TDD.md", "## 11. Co v tomhle dokumentu ZÁMĚRNĚ NENÍ",
     "## 11. Co v tomhle dokumentu ZÁMĚRNĚ NENÍ\n\nTODO: dopsat", "placeholder TODO"),

    # --- NOVÉ (15. 10. 2026): každá nová kontrola musí mít jak selhat ---
    # (a) zákaz v TDD proti přeformulovanému N9 v GDD — ZAKÁZÁNÍ POVOLENÉHO
    ("docs/TDD.md", "## 11. Co v tomhle dokumentu ZÁMĚRNĚ NENÍ",
     "## 11. Co v tomhle dokumentu ZÁMĚRNĚ NENÍ\n\n"
     "Assist je non-goal N9 a hra nesmí asistovat hráči.",
     "zákaz `assist` v TDD proti přeformulovanému N9", "FAIL", "soulad"),
    # (a2) povolení zakázaného v ADD proti N11 — opačný směr téhož rozporu
    ("docs/ADD.md", "## 9. UI a font",
     "## 9. UI a font\n\nLektvary jsou v MVP povolené a alchymie patří do rozsahu.",
     "povolení lektvarů v ADD proti `N11` v GDD", "FAIL", "soulad"),
    # (a3) třetí dokument (`BRANY-HRY.md`) se taky skenuje — jinak by byl slepý
    ("docs/BRANY-HRY.md", "## Dvě kopie souborů: šablona vs. hra",
     "## Dvě kopie souborů: šablona vs. hra\n\nPixel art je v MVP povolený.",
     "povolení pixel artu v BRANY-HRY proti `N4`", "FAIL", "soulad"),
    # (b) vymyšlené číslo kontrol, které brána nezná → NEMĚŘENO, ne tiché OK
    ("docs/GDD.md", "## 0. Záměr jednou větou — a pro koho hra je",
     "## 0. Záměr jednou větou — a pro koho hra je\n\n"
     "Hra má 500 kontrol a všechny jsou zelené.",
     "vymyšlené číslo kontrol bez zdroje", "NEMĚŘENO", "neměřeno"),
    ("docs/GDD.md", "## 0. Záměr jednou větou — a pro koho hra je",
     "## 0. Záměr jednou větou — a pro koho hra je\n\n"
     "Hra má 137 funkcí a všechny jsou volané z produkčního kódu.",
     "vymyšlený počet funkcí bez zdroje", "NEMĚŘENO", "neměřeno"),
    # (c) hlavička: odebrání „odkud brát stav“ a odsunutí hlavičky z okna
    ("docs/ADD.md", "> **Odkud brát stav:** tenhle dokument je stav vzhledu.",
     "> **Stav.**", "hlavička bez „odkud brát stav“", "FAIL", "hlavicka"),
    ("docs/TDD.md", "# TDD — `uo-shadows`: jak je hra postavená a jaké má smlouvy",
     "# TDD — `uo-shadows`: jak je hra postavená a jaké má smlouvy\n" + "\n" * 22,
     "hlavička odsunutá pod prvních 20 řádků", "FAIL", "hlavicka"),
    # (d) ZÁPORNÝ test: citace zákazu a povolená výjimka NESMÍ vyrobit poplach
    ("docs/TDD.md", "## 11. Co v tomhle dokumentu ZÁMĚRNĚ NENÍ",
     "## 11. Co v tomhle dokumentu ZÁMĚRNĚ NENÍ\n\n"
     "`N9` (GDD §11) zakazuje, aby hra rozhodla za hráče. Asistenci, která jen "
     "provede, co hráč rozhodl, GDD dovoluje.",
     "citace `N9` a povolená výjimka (nesmí hlásit)", "CISTE"),
]


def selftest(root):
    """Ověří, že kontrola SKUTEČNĚ měří: vloží vadu a čeká FAIL.

    Vady se vkládají do KOPIÍ V PAMĚTI (`base`) — na disku se nic nemění.
    Na konci to sabotér ověří hashem před/po: kdyby soubor v repu někdo
    rozepsal (jiná session), hlásí `[REPO ZMĚNĚN]` a selže.
    Každá mutace navíc říká, KTERÁ SKUPINA ji má chytit — bez toho by se
    „chyceno“ mohlo opřít o jinou kontrolu, než která má měřit.
    """
    rels = list(DEFAULT_DOCS) + [r for r in SOULAD_DOCS if r not in DEFAULT_DOCS]
    base, before = {}, {}
    for rel in rels:
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            continue
        base[rel] = read_text(path)
        with io.open(path, "rb") as f:
            before[rel] = hashlib.sha256(f.read()).hexdigest()
    primary = [r for r in DEFAULT_DOCS if r in base]
    extra_rels = [r for r in SOULAD_DOCS if r in base and r not in primary]
    print("=" * 78)
    print("SABOTÉR — každá mutace musí být chycena (jinak je kontrola slepá)")
    print("vkládá se do KOPIÍ v paměti, souborů v repu: %d" % len(base))
    print("=" * 78)
    base_rep = run_checks(root, [(r, base[r]) for r in primary],
                          [(r, base[r]) for r in extra_rels])
    green = base_rep.count(FAIL) == 0 and base_rep.count(UNMEASURED) == 0
    print("[VÝCHOZÍ STAV] bez mutace: OK=%d FAIL=%d NEMĚŘENO=%d — %s"
          % (base_rep.count(OK), base_rep.count(FAIL), base_rep.count(UNMEASURED),
             "zelená (každá mutace je přírůstek)"
             if green else "POZOR: dokumenty hlásí nález už teď"))
    bad = 0
    for mut in MUTATIONS:
        rel, old, new, label = mut[0], mut[1], mut[2], mut[3]
        expect = mut[4] if len(mut) > 4 else FAIL
        want_group = mut[5] if len(mut) > 5 else None
        if rel not in base:
            print("[NEPROVEDLA SE] %-46s — soubor %s v repu není" % (label[:46], rel))
            bad += 1
            continue
        if old not in base[rel]:
            print("[NEPROVEDLA SE] %-46s — vzor v dokumentu není: %s"
                  % (label[:46], old[:40]))
            bad += 1
            continue
        changed = dict(base)
        changed[rel] = base[rel].replace(old, new, 1)
        if changed[rel] == base[rel]:
            print("[NEPROVEDLA SE] %-46s — nahrazení text nezměnilo" % label[:46])
            bad += 1
            continue
        rep = run_checks(root, [(r, changed[r]) for r in primary],
                         [(r, changed[r]) for r in extra_rels])
        fails, unms = rep.count(FAIL), rep.count(UNMEASURED)
        if expect == "CISTE":
            if fails == 0 and unms == 0:
                print("[TICHO OK]     %-46s — citace/výjimka nevyrobila poplach "
                      "(FAIL=0 NEMĚŘENO=0)" % label[:46])
            else:
                first = next(r for r in rep.rows if r[0] in (FAIL, UNMEASURED))
                print("[FALEŠNÝ POPLACH] %-43s — %s: %s | %s"
                      % (label[:43], first[0], first[1], first[2]))
                bad += 1
            continue
        rows = [r for r in rep.rows if r[0] == expect]
        hit = [r for r in rows if want_group is None or r[1] == want_group]
        groups = sorted({r[1] for r in rows})
        if hit:
            print("[CHYCENO]      %-46s %s=%d (skupiny: %s) | %s"
                  % (label[:46], expect, len(rows), ",".join(groups),
                     " | ".join(r[2] for r in hit[:3])))
        else:
            print("[NECHYCENO]    %-46s — %s=%d ve skupinách [%s], čekáno [%s]"
                  % (label[:46], expect, len(rows), ",".join(groups) or "—",
                     want_group or "jakákoli"))
            bad += 1
    after = {}
    for rel in base:
        with io.open(os.path.join(root, rel), "rb") as f:
            after[rel] = hashlib.sha256(f.read()).hexdigest()
    print("-" * 78)
    if after == before:
        print("REPO NEDOTČEN: hash %d souborů před/po shodný (%s)"
              % (len(before), ", ".join(sorted(before))))
    else:
        for rel in sorted(before):
            if before.get(rel) != after.get(rel):
                print("[REPO ZMĚNĚN] %s — sabotér NESMÍ sahat na skutečné dokumenty!" % rel)
        bad += 1
    if bad:
        print("SABOTÉR: %d z %d mutací NEBYLO chyceno — kontrola je slepá."
              % (bad, len(MUTATIONS)))
        return 1
    print("SABOTÉR: všech %d mutací chyceno — kontrola měří." % len(MUTATIONS))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--docs", default=",".join(DEFAULT_DOCS))
    ap.add_argument("--selftest", action="store_true",
                    help="vloží do KOPIÍ dokumentů vady a ověří, že je kontrola chytí")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    os.chdir(root)
    if args.selftest:
        return selftest(root)
    rels = [d.strip() for d in args.docs.split(",") if d.strip()]

    docs = []
    for rel in rels:
        if os.path.exists(rel):
            docs.append((rel, read_text(rel)))
        else:
            print("CHYBA: dokument %s neexistuje" % rel)
    if not docs:
        print("NEMĚŘENO: žádný dokument — to není zelená.")
        return 2

    # Dokumenty, které se berou JEN na kontrolu vnitřního souladu. Když nejsou
    # primární (--docs), načtou se z disku; když nejsou vůbec, hlásí to
    # `check_soulad` jako NEMĚŘENO (chybějící dokument není zelená).
    extra = [(rel, read_text(rel)) for rel in SOULAD_DOCS
             if rel not in rels and os.path.exists(rel)]

    blocks = sections(docs)
    rep = run_checks(root, docs, extra)

    print("=" * 78)
    print("KONTROLA DOKUMENTŮ proti zdrojům a navzájem — %d souborů: %s"
          % (len(docs), ", ".join(rels)))
    print("soulad zákazů z %s proti: %s"
          % (GDD, ", ".join([rel for rel in rels if rel != GDD]
                            + [rel for rel, _ in extra]) or "—"))
    print("okna: tvrzení %d znaků · tvrzení v oddílu %d znaků · hlavička %d řádků"
          " · oddílů %d" % (WINDOW, SECTION_WINDOW, HEADER_LINES, len(blocks)))
    print("=" * 78)
    for state, group, what, detail in rep.rows:
        if state == OK:
            continue
        print("[%s] %-12s %s\n            %s" % (state, group, what, detail))
    print("-" * 78)
    print("OK: %d   FAIL: %d   NEMĚŘENO: %d   (celkem %d kontrol)"
          % (rep.count(OK), rep.count(FAIL), rep.count(UNMEASURED), len(rep.rows)))

    if rep.count(FAIL) > 0:
        print("VÝSLEDEK: 1 — něco v dokumentech nesouhlasí se zdrojem.")
        return 1
    if rep.count(UNMEASURED) > 0:
        print("VÝSLEDEK: 2 — %d tvrzení se NENAŠLO; to není zelená."
              % rep.count(UNMEASURED))
        return 2
    print("VÝSLEDEK: 0 — vše změřeno a v pořádku.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
