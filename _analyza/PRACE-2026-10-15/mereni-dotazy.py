# mereni-dotazy.py -- otevrene otazky: _check def, export_presets, roadmap dump, sprites.json
# Spusteni: $env:PYTHONIOENCODING='utf-8'; python _analyza\PRACE-2026-10-15\mereni-dotazy.py
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
out = []


def p(s=""):
    out.append(str(s))
    print(s)


p("=" * 78)
p("A) _check( v tests/run_tests.gd -- je 155 vyskytu 155 VOLANI, nebo i definice?")
p("=" * 78)
t = (ROOT / "tests" / "run_tests.gd").read_text(encoding="utf-8")
lines = t.splitlines()
p(f"radku celkem (splitlines): {len(lines)}")
for i, ln in enumerate(lines, 1):
    if re.search(r"func\s+_check", ln):
        p(f"  DEFINICE na radku {i}: {ln.strip()}")
p(f"vyskytu retezce '_check('                  : {t.count('_check(')}")
p(f"z toho radku s 'func _check'               : {len([1 for ln in lines if re.search(r'func\\s+_check', ln)])}")
p(f"radku obsahujicich '_check('               : {len([1 for ln in lines if '_check(' in ln])}")
p(f"=> VOLANI _check( (vyskyt mimo definici)   : {t.count('_check(') - len([1 for ln in lines if re.search(r'func\\s+_check', ln)])}")
# kolik _check je podminenych has_method
p()
p("Podminene kontroly: _check( uvnitr bloku, ktery predtim testoval has_method")
p("  (hruby odhad: radky _check, ktere nasleduji po has_method ve stejnem if-bloku se stejnym odsazenim)")
hm = [i for i, ln in enumerate(lines) if "has_method" in ln]
p(f"  radku s has_method: {len(hm)}")

p()
p("=" * 78)
p("B) export_presets.cfg -- je v nem 'uo-shadows'? (HANDOFF.md:183 tvrdi, ze ano)")
p("=" * 78)
ep = (ROOT / "export_presets.cfg").read_text(encoding="utf-8")
p(f"obsahuje 'uo-shadows': {'uo-shadows' in ep}")
p(f"obsahuje 'uo-sandbox': {'uo-sandbox' in ep}")
p(f"vsechny radky s 'name':")
for i, ln in enumerate(ep.splitlines(), 1):
    if re.search(r"(^|\s)(name|application/config/name)\s*=", ln) or "name=" in ln:
        p(f"   {i}: {ln.strip()}")
p(f"export_path radky:")
for ln in ep.splitlines():
    if "export_path" in ln:
        p(f"   {ln.strip()}")
# uo-shadows kdekoliv v repu
p()
p("Kde vsude je 'uo-shadows' (jen konfiguracni soubory):")
for c in ["project.godot", "export_presets.cfg", "assets/spec.json", "forge.json", "hra.cmd", ".forge/roadmap.json"]:
    f = ROOT / c
    if f.exists():
        txt = f.read_text(encoding="utf-8", errors="ignore")
        p(f"   {c:28s} 'uo-shadows'={'uo-shadows' in txt}  'uo-sandbox'={'uo-sandbox' in txt}")

p()
p("=" * 78)
p("C) ROADMAP -- vsechny granule (id, done, depends_on)")
p("=" * 78)
rm = json.loads((ROOT / ".forge" / "roadmap.json").read_text(encoding="utf-8"))
grains = rm["grains"]
doneset = {g["id"] for g in grains if g.get("done") is True}
for g in grains:
    deps = g.get("depends_on") or []
    unmet = [d for d in deps if d not in doneset]
    st = "DONE" if g.get("done") is True else ("READY" if not unmet else "BLOKOVANA")
    p(f"  {g['id']:22s} done={str(g.get('done')):5s} {st:9s} kind={str(g.get('kind')):9s} deps={deps} unmet={unmet}")
    if g.get("done_note"):
        p(f"      done_note: {g['done_note'][:150]}")
p()
p(f"_popis roadmapy: {rm.get('_popis')}")

p()
p("=" * 78)
p("D) sprites.json v koreni repa -- co to je a pouziva ho neco?")
p("=" * 78)
sj = ROOT / "sprites.json"
p(f"existuje: {sj.exists()}, B={sj.stat().st_size}")
p(sj.read_text(encoding="utf-8")[:600])
p()
used_by = []
for f in ROOT.rglob("*"):
    if not f.is_file() or f == sj:
        continue
    s = f.as_posix()
    if "/.git/" in s or "/.godot/" in s or "_analyza/PRACE-2026-10-15" in s:
        continue
    if f.suffix not in (".gd", ".py", ".mjs", ".json", ".tscn", ".cfg", ".yml", ".sh", ".cmd", ".godot", ".md"):
        continue
    try:
        if "sprites.json" in f.read_text(encoding="utf-8", errors="ignore"):
            used_by.append(f.relative_to(ROOT).as_posix())
    except Exception:
        pass
p(f"'sprites.json' je zmineno v: {used_by}")

p()
p("=" * 78)
p("E) check-assets.py -- slouzi k tomu? (spustit znovu nize v pwsh)")
p("=" * 78)
p("(viz vystup v FAKTA.md)")

(Path(__file__).with_name("vysledek-dotazy.txt")).write_text("\n".join(out), encoding="utf-8")
