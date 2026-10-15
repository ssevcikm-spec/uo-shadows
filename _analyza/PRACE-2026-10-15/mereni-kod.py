# mereni-kod.py -- meri kod hry uo-shadows pro FAKTA.md
# Spusteni: $env:PYTHONIOENCODING='utf-8'; python _analyza\PRACE-2026-10-15\mereni-kod.py
# Autorita pro pocet radku je splitlines() (ne split("\n"), ne Measure-Object -Line).
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
out = []


def p(s=""):
    out.append(str(s))
    print(s)


def lines_of(pth: Path):
    return len(pth.read_text(encoding="utf-8").splitlines())


def head_comment(pth: Path):
    """Prvni smysluplny komentar/docstring souboru = co soubor dela jednou vetou."""
    txt = pth.read_text(encoding="utf-8").splitlines()
    for ln in txt[:12]:
        s = ln.strip()
        if s.startswith("##"):
            return s.lstrip("#").strip()
        if s.startswith("#") and len(s) > 3:
            return s.lstrip("#").strip()
    return "(bez hlavicky)"


p("=" * 78)
p("1) SKRIPTY scripts/*.gd -- radky splitlines()")
p("=" * 78)

gd = sorted((ROOT / "scripts").glob("*.gd"))
total_gd = 0
for f in gd:
    n = lines_of(f)
    total_gd += n
    p(f"{f.name:16s} {n:5d} radku  {f.stat().st_size:6d} B  | {head_comment(f)[:70]}")
p(f"CELKEM scripts/*.gd: {len(gd)} souboru, {total_gd} radku")

tests = ROOT / "tests" / "run_tests.gd"
p(f"tests/run_tests.gd: {lines_of(tests)} radku, {tests.stat().st_size} B")

p()
p("=" * 78)
p("2) DOSAZITELNOST Z main.tscn (produkcni cesta vs. mrtva knihovna)")
p("=" * 78)

scene = (ROOT / "main.tscn").read_text(encoding="utf-8")
roots = re.findall(r'path="res://([^"]+)"', scene)
p(f"main.tscn ext_resource: {roots}")

# Reference na skripty: load("res://...") / preload("res://...") a set_script
ref_re = re.compile(r'(?:load|preload)\("res://([^"]+\.gd)"\)')


def refs_of(pth: Path):
    try:
        txt = pth.read_text(encoding="utf-8")
    except Exception:
        return set()
    return set(ref_re.findall(txt))


reachable = set()
queue = [r for r in roots if r.endswith(".gd")]
reachable.update(queue)
while queue:
    cur = queue.pop()
    fp = ROOT / cur
    if not fp.exists():
        p(f"  !! main.tscn/retěz odkazuje na neexistujici {cur}")
        continue
    for r in refs_of(fp):
        if r not in reachable:
            reachable.add(r)
            queue.append(r)

p(f"Dosazitelne z main.tscn ({len(reachable)}): {sorted(reachable)}")

# kdo koho referencuje
p()
p("Kdo koho referencuje (load/preload z jinych .gd):")
for f in gd:
    r = sorted(refs_of(f))
    if r:
        p(f"  {f.name:16s} -> {r}")

p()
p("Kdo je referencovany z main.tscn nebo z jineho .gd (dopredny graf):")
referenced = set()
for f in gd:
    referenced |= refs_of(f)
p(f"  referencovane: {sorted(referenced)}")

p()
prod, dead = [], []
for f in gd:
    rel = f"scripts/{f.name}"
    n = lines_of(f)
    if rel in reachable:
        prod.append((f.name, n))
    else:
        dead.append((f.name, n))
p(f"PRODUKCNI CESTA ({len(prod)} souboru, {sum(n for _, n in prod)} radku):")
for name, n in prod:
    p(f"   {name:16s} {n:5d}")
p(f"MIMO PRODUKCNI CESTU ({len(dead)} souboru, {sum(n for _, n in dead)} radku):")
for name, n in dead:
    refs = sorted(x for x in referenced if x.endswith(name))
    p(f"   {name:16s} {n:5d}  referencuje ho: {refs if refs else 'NIKDO (ani load/preload)'}")

# .tres / .tscn / ostatni resource v repu, ktere hlavni scena pouziva
p()
p("Dalsi resourcy zminene v kodu (load/preload mimo .gd):")
other = set()
for f in gd + [tests]:
    for m in re.finditer(r'(?:load|preload)\("res://([^"]+)"\)', f.read_text(encoding="utf-8")):
        if not m.group(1).endswith(".gd"):
            other.add(m.group(1))
for o in sorted(other):
    p(f"   {o}  existuje={ (ROOT/o).exists() }")

p()
p("=" * 78)
p("3) STATICKA METRIKA TESTU (pocet z BEHU je jinde -- viz [test] N kontrol)")
p("=" * 78)

tlines = tests.read_text(encoding="utf-8").splitlines()
hm_lines = [i + 1 for i, ln in enumerate(tlines) if "has_method" in ln]
hm_occ = sum(ln.count("has_method") for ln in tlines)
chk_occ = sum(ln.count("_check(") for ln in tlines)
chk_lines = [i + 1 for i, ln in enumerate(tlines) if "_check(" in ln]
p(f"radku obsahujicich 'has_method' : {len(hm_lines)}")
p(f"vyskytu 'has_method'            : {hm_occ}")
p(f"volani '_check(' (vyskytu)      : {chk_occ}")
p(f"radku obsahujicich '_check('    : {len(chk_lines)}")
p("POZOR: staticke cislo NENI pocet kontrol z behu.")

p()
p("=" * 78)
p("4) TESTOVANE SOUBORY A PRISTUP DO KODU")
p("=" * 78)
ttxt = tests.read_text(encoding="utf-8")
for f in gd:
    name = f.name
    n_load = len(re.findall(re.escape(f"scripts/{name}"), ttxt))
    p(f"  {name:16s} zminek v run_tests.gd: {n_load}")

p()
p("=" * 78)
p("5) KDO VOLA _save_state / _load_state (mrtvy kod?)")
p("=" * 78)
for f in gd:
    txt = f.read_text(encoding="utf-8")
    for fn in ["_save_state", "_load_state", "play_sfx", "save", "load"]:
        c = len(re.findall(r"\b" + re.escape(fn) + r"\s*\(", txt))
        if c:
            p(f"  {f.name:16s} {fn:18s} vyskytu volani: {c}")

p()
p("=" * 78)
p("6) HEAD pri behu skriptu")
p("=" * 78)
head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True)
p(f"git rev-parse --short HEAD -> {head.stdout.strip()} (exit {head.returncode})")

(Path(__file__).with_name("vysledek-kod.txt")).write_text("\n".join(out), encoding="utf-8")
