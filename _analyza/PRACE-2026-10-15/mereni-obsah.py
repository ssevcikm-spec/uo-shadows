# mereni-obsah.py -- obsah, plan, konfigurace, ukladani, CI pro FAKTA.md
# Spusteni: $env:PYTHONIOENCODING='utf-8'; python _analyza\PRACE-2026-10-15\mereni-obsah.py
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
out = []


def p(s=""):
    out.append(str(s))
    print(s)


p("=" * 78)
p("1) OBSAH assets/data/*.json")
p("=" * 78)
for f in sorted((ROOT / "assets" / "data").glob("*.json")):
    raw = f.read_text(encoding="utf-8")
    try:
        d = json.loads(raw)
        valid = "JSON VALIDNI"
    except Exception as e:
        p(f"{f.name}: JSON NEROZBITNE -- {e}")
        continue
    kind = type(d).__name__
    n = len(d) if isinstance(d, (list, dict)) else "?"
    p(f"{f.name:16s} {valid}  typ={kind}  zaznamu={n}  radku={len(raw.splitlines())}  B={f.stat().st_size}")
    p(f"    klice: {list(d.keys()) if isinstance(d, dict) else 'ARRAY'}")
    if isinstance(d, list) and d and isinstance(d[0], dict):
        p(f"    klice prvku: {list(d[0].keys())}")
        for it in d[:12]:
            ident = it.get("id") or it.get("nazev") or it.get("name")
            nm = it.get("name") or it.get("nazev")
            p(f"      - id={ident!r} name={nm!r}")

p()
p("=" * 78)
p("2) OBSAH assets/levels/*.json")
p("=" * 78)
for f in sorted((ROOT / "assets" / "levels").glob("*.json")):
    raw = f.read_text(encoding="utf-8")
    d = json.loads(raw)
    p(f"{f.name}: JSON VALIDNI, B={f.stat().st_size}, radku={len(raw.splitlines())}")
    p(f"    klice: {list(d.keys())}")
    for k, v in d.items():
        if isinstance(v, list):
            p(f"    {k}: ARRAY delka {len(v)}")
            if v and isinstance(v[0], dict):
                p(f"        klice prvku: {list(v[0].keys())}")
                from collections import Counter
                p(f"        pocty podle typu: {dict(Counter(str(x.get('type') or x.get('typ')) for x in v))}")
        elif isinstance(v, dict):
            p(f"    {k}: DICT {json.dumps(v, ensure_ascii=False)[:200]}")
        else:
            p(f"    {k}: {v!r}")

# rozmery mapy z data
main_lv = json.loads((ROOT / "assets" / "levels" / "main.json").read_text(encoding="utf-8"))
p()
p("ROZMERY MAPY (ze main.json, autorita je soubor):")
def find_grid(o, path=""):
    res = []
    if isinstance(o, dict):
        for k, v in o.items():
            res += find_grid(v, f"{path}.{k}")
    elif isinstance(o, list) and o and isinstance(o[0], list):
        res.append((path, len(o), len(o[0])))
    return res
for path, h, w in find_grid(main_lv):
    p(f"    {path}: {w} sloupcu x {h} radku = {w*h} policek")

# ------------------------------------------------------------- 3) roadmapa ---
p()
p("=" * 78)
p("3) PLAN .forge/roadmap.json")
p("=" * 78)
rm_raw = (ROOT / ".forge" / "roadmap.json").read_text(encoding="utf-8")
try:
    rm = json.loads(rm_raw)
    p(f"VALIDACE JSON: OK  (B={len(rm_raw.encode('utf-8'))}, radku={len(rm_raw.splitlines())})")
except Exception as e:
    p(f"VALIDACE JSON: SELHALA -- {e}")
    rm = None

if rm:
    p(f"koren: typ={type(rm).__name__}, klice={list(rm.keys()) if isinstance(rm, dict) else 'ARRAY'}")
    grains = rm["grains"] if isinstance(rm, dict) and "grains" in rm else rm
    p(f"pocet granul (klice 'grains'): {len(grains)}")
    ids = [g.get("id") for g in grains]
    dup = {i for i in ids if ids.count(i) > 1}
    p(f"unikátních id: {len(set(ids))}, duplicit: {sorted(dup) if dup else 'zadne'}")
    done = [g for g in grains if g.get("done") is True]
    notdone = [g for g in grains if g.get("done") is not True]
    p(f"done: true .......... {len(done)}")
    p(f"done != true ........ {len(notdone)}")
    p(f"  z toho done chybi/None: {len([g for g in notdone if 'done' not in g])}, done: false: {len([g for g in notdone if g.get('done') is False])}")
    dep_key = "depends_on" if any("depends_on" in g for g in grains) else ("blocked_by" if any("blocked_by" in g for g in grains) else None)
    p(f"klic zavislosti: {dep_key}")
    depmap = {g["id"]: list(g.get(dep_key) or []) for g in grains} if dep_key else {}
    doneset = {g["id"] for g in done}
    ready, blocked = [], []
    for g in grains:
        if g.get("done") is True:
            continue
        unmet = [d for d in depmap.get(g["id"], []) if d not in doneset]
        (blocked if unmet else ready).append((g["id"], unmet))
    p(f"READY (nedone a vsechny zavislosti done) ... {len(ready)}")
    for i, u in ready:
        p(f"      {i}")
    p(f"BLOKOVANE (nedone a nejaka zavislost neni done) ... {len(blocked)}")
    for i, u in blocked:
        p(f"      {i}  chybi: {u}")
    # visici zavislosti (odkaz na neexistujici id)
    dangling = sorted({d for v in depmap.values() for d in v if d not in set(ids)})
    p(f"VISICI zavislosti (odkaz na neexistujici id): {dangling if dangling else 'zadne'}")
    p(f"granule s 'provides' .... {len([g for g in grains if g.get('provides')])}  (celkem polozek: {sum(len(g.get('provides') or []) for g in grains)})")
    p(f"granule s 'consumes' .... {len([g for g in grains if g.get('consumes')])}  (celkem polozek: {sum(len(g.get('consumes') or []) for g in grains)})")
    p(f"granule s 'acceptance' .. {len([g for g in grains if g.get('acceptance')])}  (celkem polozek: {sum(len(g.get('acceptance') or []) for g in grains)})")
    p(f"granule s 'owns' ........ {len([g for g in grains if g.get('owns')])}")
    p(f"granule s 'size_lines' .. {len([g for g in grains if g.get('size_lines')])}")
    p(f"granule s 'model' ....... {len([g for g in grains if g.get('model')])}")
    allkeys = sorted({k for g in grains for k in g})
    p(f"vsechny klice granul: {allkeys}")

# ------------------------------------------------------------ 4) konfigurace --
p()
p("=" * 78)
p("4) KONFIGURACE")
p("=" * 78)
pg = (ROOT / "project.godot").read_text(encoding="utf-8")
p(f"project.godot: radku={len(pg.splitlines())}, B={len(pg.encode('utf-8'))}")
for m in re.finditer(r"^\[([^\]]+)\]", pg, re.M):
    p(f"    sekce: [{m.group(1)}]")
p(f"    config/name: {re.search(r'config/name=\"([^\"]+)\"', pg).group(1)}")
p(f"    run/main_scene: {re.search(r'run/main_scene=\"([^\"]+)\"', pg).group(1)}")
p(f"    config/features: {re.search(r'config/features=(.+)', pg).group(1)}")
p(f"    [autoload] sekce pritomna: {'[autoload]' in pg}  -> autoloadu: {len(re.findall(r'^[A-Za-z_]\\w*=\"\\*res://', pg, re.M))}")
acts = re.findall(r"^(input/[^\s=]+)", pg, re.M)
p(f"    input/* akce: {len(acts)}  {acts}")
p(f"    input_devices: {re.search(r'input_devices=(.+)', pg).group(1)}")
for k in ["window/size/viewport_width", "window/size/viewport_height", "window/stretch/mode",
          "window/stretch/aspect", "renderer/rendering_method", "default_texture_filter",
          "common/physics_ticks_per_second"]:
    m = re.search(re.escape(k) + r"=(.+)", pg)
    p(f"    {k} = {m.group(1).strip() if m else 'NENALEZENO'}")

p()
ep = (ROOT / "export_presets.cfg").read_text(encoding="utf-8")
p(f"export_presets.cfg: radku={len(ep.splitlines())}, B={len(ep.encode('utf-8'))}")
for k in ["name=", "platform=", "export_path=", "export_filter=", "application/config/name="]:
    vs = re.findall(r"^" + re.escape(k) + r"(.*)$", ep, re.M)
    p(f"    {k} -> {vs}")

p()
p("assets/spec.json -- jen cisla:")
sp = json.loads((ROOT / "assets" / "spec.json").read_text(encoding="utf-8"))
p(f"    viewport: {sp['viewport']}")
p(f"    tile: {sp['tile']}")
p(f"    role ({len(sp['role'])}):")
for k, v in sp["role"].items():
    p(f"      {k:8s} visual_height={v['visual_height']:4d} canvas={v['canvas']:4d} smery={v['smery']} framy={v['framy']} stin={v['stin']}")
p(f"    vrstvy.slot_poradi ({len(sp['vrstvy']['slot_poradi'])}): {sp['vrstvy']['slot_poradi']}")
p(f"    vrstvy.pocatecni_sada ({len(sp['vrstvy']['pocatecni_sada'])}): {sp['vrstvy']['pocatecni_sada']}")
p(f"    vrstvy.render_na_vrstvu: {sp['vrstvy']['render_na_vrstvu']}, tonovani: {sp['vrstvy']['tonovani']}")
p(f"    gates ({len([k for k in sp['gates'] if not k.startswith('_')])} ciselnych):")
for k, v in sp["gates"].items():
    if not k.startswith("_"):
        p(f"      {k} = {v}")
p(f"    styl.technika: {sp['styl']['technika']}")
p(f"    stin: {sp['stin']['sirka_pomer']} / {sp['stin']['kryti']}")
p(f"    paleta.zdroj: {sp['paleta']['zdroj']}")
p(f"    celkem roli: {len(sp['role'])}, celkem slotu vrstev: {len(sp['vrstvy']['slot_poradi'])}")
p(f"    pocatecni sada je {len(sp['vrstvy']['pocatecni_sada'])} z {len(sp['vrstvy']['slot_poradi'])} slotu")

# ------------------------------------------------------------- 5) ukladani ---
p()
p("=" * 78)
p("5) UKLADANI -- co a kam se uklada")
p("=" * 78)
sg = (ROOT / "scripts" / "save.gd").read_text(encoding="utf-8")
p(f"save.gd: const SOUBOR = {re.search(r'const SOUBOR := \"([^\"]+)\"', sg).group(1)}")
p(f"save.gd: const POTREBNE = {re.search(r'const POTREBNE := (\[[^\]]*\])', sg).group(1)}")
p("save.gd -- klice zapisovane pres cfg.set_value:")
for m in re.finditer(r'cfg\.set_value\("([^"]+)",\s*"([^"]+)"', sg):
    p(f"    [{m.group(1)}] {m.group(2)}")
p("save.gd -- klice ctene pres cfg.get_value / has_section_key:")
for m in re.finditer(r'cfg\.(?:get_value|has_section_key)\("([^"]+)",\s*"([^"]+)"', sg):
    p(f"    [{m.group(1)}] {m.group(2)}")

p()
gm = (ROOT / "scripts" / "game.gd").read_text(encoding="utf-8")
p("game.gd -- DRUHE ukladani (mimo save.gd):")
for m in re.finditer(r'cfg\.set_value\("([^"]+)",\s*"([^"]+)"', gm):
    p(f"    [{m.group(1)}] {m.group(2)}")
p(f"    soubor: {sorted(set(re.findall(r'user://([A-Za-z0-9_.]+)', gm)))}")
p(f"    volani _save_state()/_load_state() v game.gd: {len(re.findall(r'_save_state\(\)|_load_state\(\)', gm))} (definice viz nize)")
for fn in ["_save_state", "_load_state"]:
    p(f"      {fn}: definice na radku {gm[:gm.find('func '+fn)].count(chr(10))+1 if ('func '+fn) in gm else 'CHYBI'}")

# ------------------------------------------------------------------ 6) CI ----
p()
p("=" * 78)
p("6) CI -- .github/workflows/*.yml")
p("=" * 78)
for f in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
    raw = f.read_text(encoding="utf-8")
    ls = raw.splitlines()
    p(f"--- {f.name}: {len(ls)} radku, {len(raw.encode('utf-8'))} B")
    for m in re.finditer(r"^(\s*)name:\s*(.+)$", raw, re.M):
        indent = len(m.group(1))
        if indent <= 4:
            p(f"    {'  '*(indent//2)}name: {m.group(2)}")
    p("    kroky (run/uses v poradi):")
    n = 0
    for i, ln in enumerate(ls):
        s = ln.strip()
        if s.startswith("- run:") or s.startswith("run: "):
            n += 1
            body = s.split("run:", 1)[1].strip()
            # vice-radkove run: -> vzit i dalsi odsazene radky
            j = i + 1
            extra = []
            while j < len(ls) and (ls[j].startswith(" " * 10) or ls[j].strip() == ""):
                if ls[j].strip():
                    extra.append(ls[j].strip())
                j += 1
            txt = " ".join(([body] if body and body != "|" else []) + extra)
            p(f"      {n:2d}. run: {txt[:150]}")
        elif re.match(r"^\s*-?\s*uses:", s):
            n += 1
            p(f"      {n:2d}. uses: {s}")
    # brany
    br = sorted(set(re.findall(r"(?:python|node)\s+([.\w/\-]*check-[.\w\-]+\.py|[.\w/\-]*\.mjs)", raw)))
    p(f"    spoustene brany/nastroje: {br}")

p()
head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True)
p(f"git rev-parse --short HEAD -> {head.stdout.strip()}")

(Path(__file__).with_name("vysledek-obsah.txt")).write_text("\n".join(out), encoding="utf-8")
