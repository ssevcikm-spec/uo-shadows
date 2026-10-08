#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""over-dokumenty.py — kontrola dokumentů GDD/ADD/TDD proti ZDROJŮM.

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

CO TENHLE NÁSTROJ NEUMÍ (pojmenované meze, ne „snad to nevadí“):
  * Neumí poznat, že interní odkaz je MYŠLENÝ jinak, když jeho číslo v cíli
    náhodou existuje (naměřeno: `ADD` §4/§5/§11/§12 a `GDD` §6 mají stejné
    číslo jako oddíl zdroje rozhodnutí). Tyhle případy se našly RUČNÍM čtením
    a jsou opravené; nástroj chytí jen ten případ, kdy číslo v cíli NENÍ.
  * Neměří běhové chování (Godot se nespouští) — jen soubory a jejich obsah.
  * Ověřuje jen to, co je v `MUTATIONS` (sabotér) — nová třída tvrzení
    potřebuje novou mutaci, jinak může být kontrola slepá.

Použití:
  python _analyza/over-dokumenty.py [--docs docs/GDD.md,docs/ADD.md,docs/TDD.md]
  python _analyza/over-dokumenty.py --selftest      # sabotér: vloží vady a čeká FAIL
Exit: 0 = vše změřeno a v pořádku · 1 = něco nesouhlasí · 2 = něco zůstalo neměřeno
"""

import argparse
import io
import json
import os
import re
import sys

DEFAULT_DOCS = ["docs/GDD.md", "docs/ADD.md", "docs/TDD.md"]
REVIZE = "_analyza/DESIGN-REVIZE-2.md"

OK, FAIL, UNMEASURED = "OK", "FAIL", "NEMĚŘENO"
WINDOW = 160          # znaků pro běžná tvrzení; u čísel v oddílu je větší
SECTION_WINDOW = 2500  # znaků uvnitř jednoho oddílu (stavové řádky smluv)


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
    rx = re.compile(r"`([A-Za-z0-9_\-./]+)`")
    checked = bad = 0
    for rel, text in docs:
        for i, line in enumerate(text.splitlines(), start=1):
            for m in rx.finditer(line):
                p = m.group(1)
                if not p.startswith(prefixes) or "*" in p or p.endswith("/"):
                    continue
                checked += 1
                if os.path.exists(os.path.join(root, p.replace("/", os.sep))):
                    continue
                if any(w in line for w in missing_words):
                    rep.add(OK, "cesty", "%s:%d `%s`" % (rel, i, p),
                            "cesta neexistuje a dokument to ŘÍKÁ | %s" % line.strip()[:110])
                else:
                    bad += 1
                    rep.add(FAIL, "cesty", "%s:%d `%s`" % (rel, i, p),
                            "cesta NEEXISTUJE a dokument to neříká | %s" % line.strip()[:110])
    rep.add(OK if bad == 0 else FAIL, "cesty", "cesty v backtickách",
            "zkontrolováno %d cest, vadných %d" % (checked, bad))


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
    claim_rx = re.compile(r"(?P<v>\d+) (?P<unit>řádk|klíč)")
    # tvrzení kvalifikované symbolem není tvrzení o souboru
    # (naměřeno: „`tests/run_tests.gd` … `has_method` má **26 řádků**“ se
    #  přiřadilo souboru a hlásilo 26 != 1406)
    qualified_rx = re.compile(r"(has_method|`\w+`)\s*(má|na)?\s*\**\s*$")
    checked = skipped = 0
    for rel, base, text in blocks:
        for mv in claim_rx.finditer(text):
            if qualified_rx.search(text[max(0, mv.start() - 40):mv.start()]):
                skipped += 1
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
            if unit == "klíč":
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
            "zkontrolováno %d (nepřiřazeno %d — bez blízkého souboru)" % (checked, skipped))


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
    rows, occ = measure_has_method(root)
    report_claims(rep, "has_method řádků",
                  claims(blocks, r"has_method", r"(?P<v>\d+) řádků", window=30), rows)
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
    for rel, text in docs:
        for needle, label in (("Co tenhle dokument JE", "hlavička: čím je"),
                              ("Odkud brát stav", "hlavička: odkud stav"),
                              ("ZÁMĚRNĚ NENÍ", "sekce: co tam záměrně není")):
            state = OK if needle in text else FAIL
            rep.add(state, "hlavička", "%s: %s" % (rel, label),
                    "nalezeno" if state == OK else "CHYBÍ")


def check_language(docs, rep):
    diac = set("áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ")
    for rel, text in docs:
        n = sum(1 for ch in text if ch in diac)
        rep.add(OK if n > 200 else FAIL, "jazyk", "%s: diakritika" % rel,
                "%d znaků s diakritikou" % n)
    for rel in [d[0] for d in docs] + [REVIZE, "_analyza/over-dokumenty.py",
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


def run_checks(root, docs):
    blocks = sections(docs)
    rep = Report()
    check_cross_refs(root, docs, rep)
    check_paths(root, docs, rep)
    check_numbers(root, docs, blocks, rep)
    check_placeholders(docs, rep)
    check_header_and_sections(docs, rep)
    check_language(docs, rep)
    check_json(rep)
    return rep


# Sabotér: kdyby kontrola neměla jak selhat, byla by zelená vždycky.
# Každá mutace vrací do dokumentu VADU a kontrola ji MUSÍ chytit.
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
]


def selftest(root):
    """Ověří, že kontrola SKUTEČNĚ měří: vloží vadu a čeká FAIL."""
    base = {}
    for rel in DEFAULT_DOCS:
        base[rel] = read_text(os.path.join(root, rel))
    print("=" * 78)
    print("SABOTÉR — každá mutace musí být chycena (jinak je kontrola slepá)")
    print("=" * 78)
    uncaught = 0
    for rel, old, new, label in MUTATIONS:
        if old not in base[rel]:
            print("[NEPROVEDLA SE] %-42s — vzor v dokumentu není: %s" % (label, old[:40]))
            uncaught += 1
            continue
        docs = [(r, base[r].replace(old, new, 1) if r == rel else base[r])
                for r in DEFAULT_DOCS]
        rep = run_checks(root, docs)
        fails = rep.count(FAIL)
        if fails > 0:
            first = next(r for r in rep.rows if r[0] == FAIL)
            print("[CHYCENO] %-42s FAIL=%d | %s" % (label, fails, first[2]))
        else:
            print("[NECHYCENO] %-40s — kontrola vadu NEVIDÍ" % label)
            uncaught += 1
    print("-" * 78)
    if uncaught:
        print("SABOTÉR: %d z %d mutací NEBYLO chyceno — kontrola je slepá."
              % (uncaught, len(MUTATIONS)))
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

    blocks = sections(docs)
    rep = run_checks(root, docs)

    print("=" * 78)
    print("KONTROLA DOKUMENTŮ proti zdrojům — %d souborů: %s" % (len(docs), ", ".join(rels)))
    print("okna: běžné tvrzení %d znaků · tvrzení v oddílu %d znaků · oddílů %d"
          % (WINDOW, SECTION_WINDOW, len(blocks)))
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
