"""aktualizuj-cisla-planu.py — srovná čísla o PLÁNU v dokumentech s dnešním stavem.

PROČ: plán se 15. 10. 2026 večer změnil (11 granulí, 6 hotových — přibyla
`world.bodies` a `shell.coins` se rozdělila), a dokumenty tvrdily 10/5. Brána
`_analyza/over-dokumenty.py` to hlásí jako rozchod se zdrojem — a to je správně:
dokument, který tvrdí starý počet, se čte jako dnešek.

PRAVIDLO: historická čísla se NEPŘEPISUJÍ, jen se označí datem. Proto se mění
jen tvrzení o DNEŠKU (věty s „dnes"/„Naměřeno 15. 10."), ne archiv.

POUŽITÍ: python _analyza/PRACE-2026-10-15/aktualizuj-cisla-planu.py
"""

import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# (soubor, co nahradit, čím, popis)
ZAMENY = [
    ("docs/README.md",
     "`.forge/roadmap.json` (dnes **10 granulí**, z toho 5 k vydání)",
     "`.forge/roadmap.json` (dnes **11 granulí**, z toho 5 k vydání)",
     "README: počet granulí v rejstříku"),
    ("docs/GDD.md",
     "Naměřeno 15. 10. 2026: `.forge/roadmap.json` má **10 granulí** a `done: true` u **5**",
     "Naměřeno 15. 10. 2026 (večer): `.forge/roadmap.json` má **11 granulí** a `done: true` u **6**",
     "GDD: dnešní počet granulí a hotových"),
    ("docs/GDD.md",
     "`game.gd` vlastní granule `engine.shell`, `shell.coins` a `sim.wire`",
     "`game.gd` vlastní granule `engine.shell`, `shell.nocoins` a `sim.wire`",
     "GDD: jméno granule po rozdělení"),
    ("docs/TDD.md",
     "naměřeno 15. 10. 2026: plán má **10 granulí**",
     "naměřeno 15. 10. 2026: plán má **11 granulí**",
     "TDD §3.5: počet granulí"),
    ("docs/TDD.md",
     "dnešní `.forge/roadmap.json` má **10 granulí** a `done: true` u **5**",
     "dnešní `.forge/roadmap.json` má **11 granulí** a `done: true` u **6**",
     "TDD §10: dnešní počet granulí a hotových"),
]


def main():
    chyby = 0
    for rel, stary, novy, popis in ZAMENY:
        cesta = os.path.join(ROOT, rel.replace("/", os.sep))
        with io.open(cesta, encoding="utf-8", newline="") as f:
            text = f.read()
        if stary not in text:
            print("[NEPROVEDLO SE] %-42s — vzor v dokumentu není" % popis)
            print("                 hledáno: %s" % stary[:90])
            chyby += 1
            continue
        pocet = text.count(stary)
        with io.open(cesta, "w", encoding="utf-8", newline="") as f:
            f.write(text.replace(stary, novy))
        print("[OK] %-52s (%d×)" % (popis, pocet))
    print("-" * 78)
    if chyby:
        print("NEPROVEDLO SE: %d záměn — text dokumentu se liší od očekávaného." % chyby)
        return 1
    print("Všech %d záměn provedeno." % len(ZAMENY))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
