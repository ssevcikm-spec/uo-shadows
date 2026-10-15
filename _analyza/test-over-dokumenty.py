#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""test-over-dokumenty.py — zkouší VÝJIMKY nových kontrol (`soulad`, `hlavicka`,
`neměřeno`) přímo, na vstupech, které si test sám sestaví.

PROČ TENHLE SOUBOR JE (a proč to nestačí sabotérem):
  `--selftest` umí jen mutace, které vloží vadu do SKUTEČNÝCH dokumentů a čekají
  FAIL. Neumí ale dobře vyjádřit ZÁPORNÉ případy — že text, který zákaz CITUJE
  nebo popisuje POVOLENOU VÝJIMKU, hlásit NESMÍ. A právě falešný poplach je
  dražší než slepé místo (nutil by „opravovat“ správný dokument).
  Testy níž proto jedou na TEXtech vložených v testu, ne na dokumentech repa —
  přežijí jejich přepsání. Jediná výjimka je test 7: ten naopak hlídá, že se
  tabulka non-goals v dnešním GDD pořád PARSuje; kdyby ne, kontrola `soulad`
  by byla slepá a `exit 0` by to nerozlišil.

Test bez `assert` a bez `sys.exit` není test — proto obojí.
Použití: python _analyza/test-over-dokumenty.py     (exit 0 = prošlo, 1 = ne)
"""

import io
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

_spec = importlib.util.spec_from_file_location(
    "over_dokumenty", os.path.join(HERE, "over-dokumenty.py"))
od = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(od)

# `N9` je v GDD zužováno na „hra nesmí ROZHODNOUT za hráče“ — kmen `rozho`.
TERMS = {"asist"}
NARROW = {"rozho"}


def fires(text, terms=TERMS, narrow=NARROW):
    return od.scan_contradictions(text, terms, narrow)[0]


# 1 ─ holý (necitovaný) zákaz šířeji, než GDD povoluje → CHYCEN
def t_bare_prohibition():
    assert fires("Hra nesmí asistovat hráči."), "holý zákaz se nenašel (slepé místo)"


# 2 ─ citace zákazu v TÉŽE klauzuli → NESMÍ hlásit
def t_citation_same_clause():
    assert not fires("`N9` zakazuje automatickou asistenci."), \
        "citace zákazu se hlásí jako rozpor (falešný poplach)"


# 3 ─ klauzule se zužujícím slovem z GDD = povolená výjimka → NESMÍ hlásit
def t_allowed_exception():
    text = ("`N9` (GDD §11) zakazuje, aby hra rozhodla za hráče. "
            "Asistenci, která jen provede, co hráč rozhodl, GDD dovoluje.")
    assert not fires(text), "povolená výjimka se hlásí jako rozpor (falešný poplach)"


# 4 ─ bloková citace (`>`) → NESMÍ hlásit
def t_blockquote_ignored():
    assert not fires("> Hra nesmí asistovat hráči."), \
        "citace v bloku `>` se hlásí jako tvrzení dokumentu"


# 5 ─ HTML komentář → NESMÍ hlásit
def t_html_comment_ignored():
    text = "<!-- Hra nesmí asistovat hráči. -->\nAsistence je smysl.\n"
    assert not fires(text), "text v HTML komentáři se hlásí jako tvrzení"


# 6 ─ povolení zakázaného (zákaz bez zužující výjimky) → CHYCEN
def t_permission_of_forbidden():
    found = od.scan_contradictions("Lektvary jsou v MVP povolené.", {"lektv"}, set())[0]
    assert found, "povolení zakázané věci se nenašlo (slepé místo)"
    # a nesmí se to splést: klauzule o povolení NENÍ rozpor u zužovaného zákazu,
    # když nese zužující slovo
    assert not od.scan_contradictions(
        "Asistence smí provést, co hráč rozhodl.", TERMS, NARROW)[0], \
        "povolená výjimka se hlásí jako povolení zakázaného"


# 7 ─ tabulka non-goals se v DNEŠNÍM GDD pořád parsuje (jinak je `soulad` slepý)
def t_nongoal_table_parses():
    gdd = io.open(os.path.join(ROOT, "docs", "GDD.md"), encoding="utf-8").read()
    rows = od.nongoal_rows(gdd)
    codes = sorted(r["code"] for r in rows)
    assert len(rows) >= 11, "tabulka non-goals dala %d řádků: %s" % (len(rows), codes)
    for row in rows:
        assert od.subject_terms(row["bold"]), \
            "zákaz %s nemá předmětová slova — kontrola by ho neměřila" % row["code"]


# 8 ─ `hlavicka`: hlavička až za 20. řádkem NENÍ hlavička; v okně projde
def t_header_window():
    late = ("# X\n" + "text\n" * 19
            + "**Co tenhle dokument JE:** zdroj pravdy\n**Odkud brát stav:** GDD\n")
    rep = od.Report()
    od.check_hlavicka([("x.md", late)], rep)
    assert rep.count(od.FAIL) == 1, "hlavička pod oknem %d řádků nehlásí FAIL" % od.HEADER_LINES
    early = ("**Co tenhle dokument JE:** zdroj pravdy o designu\n"
             "**Odkud brát stav:** `docs/GDD.md`\n" + "text\n" * 30)
    rep2 = od.Report()
    od.check_hlavicka([("x.md", early)], rep2)
    assert rep2.count(od.OK) == 1, "správná hlavička v okně hlásí FAIL"


# 9 ─ `neměřeno`: číslo bez zdroje je NEMĚŘENO, se zdrojem je OK
def t_unmeasured_counts():
    rep = od.Report()
    od.check_unmeasured_counts([("x.md", "Hra má 500 kontrol a všechny jsou zelené.")], rep)
    assert rep.count(od.UNMEASURED) == 1, "číslo bez zdroje nehlásí NEMĚŘENO"
    assert rep.count(od.FAIL) == 0, "číslo bez zdroje hlásí FAIL (nemá)"
    rep2 = od.Report()
    od.check_unmeasured_counts([("x.md", "Naměřeno 8. 10. 2026: 113 kontrol prošlo.")], rep2)
    assert rep2.count(od.UNMEASURED) == 0, "číslo se ZDROJEM hlásí NEMĚŘENO (falešný poplach)"
    assert rep2.count(od.OK) == 2, "doložené číslo nemá OK řádek pro tvrzení i souhrn"


# 10 ─ past „N řádků s X“: kvalifikované tvrzení NENÍ délka souboru,
#      ale holé „má N řádků“ délka JE (známý správný i známý chybný případ)
def t_qualified_line_claim():
    def run(text):
        rep = od.Report()
        od.check_line_claims(ROOT, od.sections([("x.md", text)]), rep)
        return rep
    good = run("`scripts/game.gd` má **28 řádků s `has_method`**.\n")
    assert good.count(od.FAIL) == 0, \
        "„N řádků s X“ se čte jako délka souboru (falešný poplach z chyby čtení)"
    bad = run("`scripts/game.gd` má **28 řádků**.\n")
    assert bad.count(od.FAIL) == 1, \
        "holé „má N řádků“ se NEMĚŘÍ — kontrola je slepá (28 != skutečná délka)"


CHECKS = [
    ("holý zákaz šířeji, než GDD povoluje, je chycen", t_bare_prohibition),
    ("citace zákazu v téže klauzuli se nehlásí", t_citation_same_clause),
    ("povolená výjimka (zužující slovo z GDD) se nehlásí", t_allowed_exception),
    ("bloková citace `>` se přeskočí", t_blockquote_ignored),
    ("HTML komentář se přeskočí", t_html_comment_ignored),
    ("povolení zakázaného je chyceno", t_permission_of_forbidden),
    ("tabulka non-goals v GDD se parsuje", t_nongoal_table_parses),
    ("hlavička pod oknem hlásí FAIL, v okně OK", t_header_window),
    ("počet bez zdroje = NEMĚŘENO, se zdrojem = OK", t_unmeasured_counts),
    ("„N řádků s X“ není délka souboru (a holé „má N řádků“ je)", t_qualified_line_claim),
]


def main():
    bad = 0
    print("=" * 78)
    print("TEST VÝJIMEK — texty si test sestavuje sám (přežije přepsání dokumentů)")
    print("=" * 78)
    for name, fn in CHECKS:
        try:
            fn()
        except AssertionError as exc:
            bad += 1
            print("[FAIL] %-56s %s" % (name, exc))
        else:
            print("[OK]   %s" % name)
    print("-" * 78)
    if bad:
        print("TEST: %d z %d kontrol SELHALO — výjimky nedrží." % (bad, len(CHECKS)))
        return 1
    print("TEST: všech %d kontrol prošlo — výjimky drží." % len(CHECKS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
