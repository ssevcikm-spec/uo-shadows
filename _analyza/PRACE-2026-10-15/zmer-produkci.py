"""zmer-produkci.py — které soubory hry jsou v PRODUKČNÍ cestě a které jsou mrtvá knihovna.

PROČ TO EXISTUJE (15. 10. 2026):
  `done: true` v `.forge/roadmap.json` je TVRZENÍ. U `uo-shadows` ho mělo 16 granul
  při dvou funkčních komponentách — a plán se podle toho vydával. Tenhle nástroj
  měří totéž, co definice hotovo v `docs/GDD.md` §12:

      hotovo = soubor je v main
               A volá ho PRODUKČNÍ kód (ne jen test)
               A jeho funkci volá produkční cesta

  Co NEMĚŘÍ: běhové chování (Godot se nespouští) — jen to, kdo koho volá ve zdrojích.
  Kdo chce víc, ať spustí testy (`tests/run_tests.gd`) a přečte `[test] N kontrol`.

POUŽITÍ:  python _analyza/PRACE-2026-10-15/zmer-produkci.py [--json]
EXIT:     0 = změřeno · 2 = něco zůstalo neměřeno (vypsáno, ne zelená)
"""

import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPTS = os.path.join(ROOT, "scripts")

# Produkční kořen: co se opravdu nainstancuje, když se hra spustí.
# `main.tscn` → `scripts/game.gd` (kostra). Vše ostatní se musí dovolat odsud.
KOREN = "scripts/game.gd"
VSTUPNI_BOD = "main.tscn"


def nacti(rel):
    with io.open(os.path.join(ROOT, rel), "r", encoding="utf-8", newline="") as f:
        return f.read()


def bez_komentaru(text):
    """Statická kontrola musí číst KÓD, ne komentáře (naměřená past)."""
    out = []
    for ln in text.splitlines():
        kod = ln.split("#", 1)[0]
        out.append(kod)
    return "\n".join(out)


def main():
    chyby = []
    soubory = sorted(f for f in os.listdir(SCRIPTS) if f.endswith(".gd"))
    if not soubory:
        print("NEMĚŘENO: v scripts/ nejsou žádné .gd soubory")
        return 2

    kody = {}
    for f in soubory:
        rel = "scripts/" + f
        kody[rel] = bez_komentaru(nacti(rel))

    koren = kody.get(KOREN)
    if koren is None:
        print("CHYBA: produkční kořen %s neexistuje" % KOREN)
        return 2

    # kdo koho zmiňuje (jméno souboru bez přípony) — z celého kódu, bez komentářů
    vsechno = "\n".join(kody.values())
    testy = bez_komentaru(nacti("tests/run_tests.gd"))

    radky = []
    for rel in sorted(kody):
        nazev = os.path.basename(rel)[:-3]
        if rel == KOREN:
            radky.append((rel, len(kody[rel].splitlines()), "PRODUKČNÍ KOŘEN",
                          "instancuje ho %s" % VSTUPNI_BOD))
            continue
        # kdo ho zmiňuje jinde než v sobě
        kde = [r for r in kody if r != rel and re.search(r"\b%s\b" % re.escape(nazev), kody[r])]
        jen_test = (not kde) and re.search(r"\b%s\b" % re.escape(nazev), testy)
        if kde:
            stav = "VOLANÝ Z KÓDU"
            detail = ", ".join(sorted(kde))
        elif jen_test:
            stav = "JEN V TESTECH"
            detail = "zmínka jen v tests/run_tests.gd"
        else:
            stav = "MRTVÝ"
            detail = "nikde se neobjevuje"
        radky.append((rel, len(kody[rel].splitlines()), stav, detail))

    # kdo je dosažitelný z produkčního kořene (tranzitivně)
    dosazene = {KOREN}
    zmena = True
    while zmena:
        zmena = False
        for rel, _r, _s, detail in radky:
            if rel in dosazene or "VOLANÝ Z KÓDU" not in _s:
                continue
            if any(z in detail for z in dosazene):
                dosazene.add(rel)
                zmena = True

    print("=" * 100)
    print("PRODUKČNÍ CESTA vs. MRTVÁ KNIHOVNA — %s (měřeno %s)" % (ROOT, "15. 10. 2026"))
    print("=" * 100)
    print("%-28s %6s %-18s %-30s %s" % ("soubor", "řádků", "stav", "kdo ho volá", "z produkce?"))
    print("-" * 100)
    prod = mrtve = 0
    for rel, n, stav, detail in radky:
        z = "ANO" if rel in dosazene else "ne"
        if rel in dosazene:
            prod += n
        else:
            mrtve += n
        print("%-28s %6d %-18s %-30s %s" % (rel, n, stav, detail[:30], z))
    print("-" * 100)
    print("z produkce dosažitelné: %d řádků · mimo produkci: %d řádků" % (prod, mrtve))

    print()
    print("CO Z TOHO PLYNE PRO PLÁN:")
    for rel, n, stav, detail in radky:
        if rel not in dosazene:
            print("  * %s (%d ř.) — %s → `done: true` by tady bylo NEPRAVDIVÉ" % (rel, n, stav))
    if not any(rel not in dosazene for rel, _n, _s, _d in radky):
        print("  (vše je dosažitelné z produkce)")

    if "--json" in sys.argv:
        print()
        print(json.dumps({"radky": [{"soubor": r, "radku": n, "stav": s, "detail": d,
                                     "z_produkce": r in dosazene}
                                    for r, n, s, d in radky]}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
