"""zkontroluj-plan.py — kontrola plánu granulí (`.forge/roadmap.json`) PŘED vydáním.

PROČ TO EXISTUJE (15. 10. 2026):
  Plán je to jediné, co agent orchestry dostane jako zadání. Když je v něm chyba,
  projeví se jako spálené běhy — a to se platí (naměřeno: 20 běhů selhalo na tom,
  že request měl 25–39 k tokenů proti stropu 8 000 → model zadání NIKDY neviděl).

CO MĚŘÍ:
  1. JSON je validní a má klíč `grains` (orchestra čte přes GitHub API).
  2. Každá granule má povinná pole a `id` je jedinečné.
  3. `depends_on` ukazuje na existující id (visící závislost = granule se nikdy nevydá).
  4. `done: true` u předka — když ne, granule NENÍ připravená (nevydá se, i když `ready`).
  5. `owns` je disjunktní mezi DVĚMA PŘIPRAVENÝMI granulemi (jinak si dvě sahají na soubor).
  6. `size_lines` > 60 vyžaduje `model: strong` (jinak ji dostane slabý model).
  7. Rozpočet zadání: prompt ~400 tokenů, strop 1200 znaků (český text ≈ 3,03 znaku/token).
  8. V zadání nemá být cesta k souboru (přitáhne celý dokument: naměřeno +8 000 t).

POUŽITÍ:  python .forge/zkontroluj-plan.py [--json]
EXIT:     0 = plán je v pořádku · 1 = vada · 2 = něco zůstalo neměřeno
"""

import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN = os.path.join(ROOT, ".forge", "roadmap.json")

POVINNA = ["id", "title", "kind", "owns", "depends_on", "acceptance", "prompt"]
ZNAKU_NA_TOKEN = 3.03          # naměřeno pro český text (ne znaky/4)
STROP_TOKENU = 400
STROP_ZNAKU = 1200
CESTY_V_ZADANI = ["docs/", "scripts/", "assets/", ".forge/", "tests/"]


def main():
    if not os.path.exists(PLAN):
        print("NEMĚŘENO: %s neexistuje" % PLAN)
        return 2
    try:
        with io.open(PLAN, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:
        print("CHYBA: plán není validní JSON: %s" % exc)
        return 1
    if "grains" not in data:
        print("CHYBA: plán nemá klíč 'grains' (orchestra ho čte)")
        return 1

    grains = data["grains"]
    if not grains:
        print("NEMĚŘENO: plán nemá žádné granule")
        return 2

    chyby, poznamky, cekani = [], [], []
    id_set = {g.get("id") for g in grains}
    hotove = {g["id"] for g in grains if g.get("done") is True}

    print("=" * 96)
    print("KONTROLA PLÁNU — %d granulí v .forge/roadmap.json" % len(grains))
    print("=" * 96)
    print("%-22s %-6s %-14s %8s %7s %s" % ("id", "done", "milník", "znaků", "~token", "stav"))
    print("-" * 96)

    pripravene = []
    for g in grains:
        gid = g.get("id", "?")
        problemy = []
        for p in POVINNA:
            if p not in g:
                problemy.append("chybí pole '%s'" % p)
        if not isinstance(g.get("owns"), list) or not g.get("owns"):
            problemy.append("owns není neprázdný seznam")
        for d in g.get("depends_on", []):
            if d not in id_set:
                problemy.append("visící závislost '%s'" % d)
            elif d not in hotove and g.get("done") is not True:
                # NENÍ vada: granule čeká na předka a conductor ji vydá, až bude hotový.
                # Kdyby to byla vada, gate by křičela na správně postavený plán.
                cekani.append("%s čeká na '%s'" % (gid, d))
        if (g.get("size_lines") or 0) > 60 and g.get("model") != "strong":
            problemy.append("size_lines > 60 bez model: strong")
        prompt = g.get("prompt", "")
        tokenu = int(len(prompt) / ZNAKU_NA_TOKEN)
        if len(prompt) > STROP_ZNAKU:
            problemy.append("zadání %d znaků (~%d t) > strop %d" % (len(prompt), tokenu, STROP_ZNAKU))
        # Riziko je v tom, že zadání POŠLE nástroj pro soubor (aider si podle cesty
        # přidá celý dokument). Proto se hlásí cesta s příponou `.md`/`.json`/`.gd`
        # a cesta s `@`; holé odvolání na oddíl („docs/TDD.md §3.16“) je jen citace
        # a nechává se být — smlouva je v zadání VLOŽENÁ, ne odkazem.
        import re as _re
        for cesta in _re.findall(r"[\w./\\-]+\.(?:md|json|gd|cfg|tscn)\b", prompt):
            poznamky.append("%s: zadání odkazuje na soubor '%s' (přitáhne celý dokument)"
                            % (gid, cesta))
            break
        stav = "OK" if not problemy else "VADA"
        if g.get("done") is True:
            stav = "hotová"
        elif not problemy:
            pripravene.append(gid)
        print("%-22s %-6s %-14s %8d %7d %s" % (
            gid, str(g.get("done")), g.get("milestone", "—"), len(prompt), tokenu, stav))
        for p in problemy:
            chyby.append("%s: %s" % (gid, p))

    print("-" * 96)
    # kolize owns mezi připravenými granulemi
    for i, a in enumerate(grains):
        for b in grains[i + 1:]:
            if a.get("done") is True or b.get("done") is True:
                continue
            spolecne = set(a.get("owns", [])) & set(b.get("owns", []))
            if spolecne:
                if b.get("id") in a.get("depends_on", []) or a.get("id") in b.get("depends_on", []):
                    poznamky.append("%s a %s sdílejí %s — je to v pořadí (depends_on), ne souběh"
                                    % (a["id"], b["id"], ", ".join(sorted(spolecne))))
                else:
                    chyby.append("%s a %s vlastní TENTÝŽ soubor bez depends_on: %s"
                                 % (a["id"], b["id"], ", ".join(sorted(spolecne))))

    print()
    print("PŘIPRAVENÉ K VYDÁNÍ (%d): %s" % (len(pripravene), ", ".join(pripravene) or "—"))
    print("HOTOVÉ (conductor přeskočí): %d" % len(hotove))
    if cekani:
        print("ČEKÁ NA PŘEDKA (%d) — není vada, conductor je vydá později:" % len(cekani))
        for c in cekani:
            print("  · %s" % c)
    print()
    for p in poznamky:
        print("  poznámka: %s" % p)
    for c in chyby:
        print("  VADA: %s" % c)

    print("-" * 96)
    if chyby:
        print("VÝSLEDEK: 1 — %d vad v plánu." % len(chyby))
        return 1
    print("VÝSLEDEK: 0 — plán je v pořádku (%d granulí, %d připravených)."
          % (len(grains), len(pripravene)))
    if "--json" in sys.argv:
        print(json.dumps({"pripravene": pripravene, "hotove": sorted(hotove)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
