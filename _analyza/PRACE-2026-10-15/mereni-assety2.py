# mereni-assety2.py -- druhe, prisnejsi mereni odkazovanosti assetu
# Odstranuje kontaminaci: vylucuje VLASTNI vystupy v _analyza/PRACE-2026-10-15/
# a pouziva hranice slov (\b), aby "coin" netrefilo "coin_final".
# Spusteni: $env:PYTHONIOENCODING='utf-8'; python _analyza\PRACE-2026-10-15\mereni-assety2.py
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MYDIR = (Path(__file__).parent).relative_to(ROOT).as_posix()
out = []


def p(s=""):
    out.append(str(s))
    print(s)


p("=" * 78)
p("0) KONTAMINACE: vylucuji vlastni vystupy")
p("=" * 78)
p(f"vylouceny adresar: {MYDIR}/  (jinak by si skript nasel vlastni vystup)")

p()
p("=" * 78)
p("1) SPRITY, KTERE HRA NACITA -- autorita je KOD, ktery je nacita")
p("=" * 78)
game = (ROOT / "scripts" / "game.gd").read_text(encoding="utf-8")
used = re.findall(r'_visual\(\s*"([^"]+)"', game)
anim = re.findall(r'_animation_visual\(\s*"([^"]+)"', game)
p(f"game.gd _visual(...) volani: {used}")
p(f"game.gd _animation_visual(...): {anim} -> hleda res://assets/{anim[0]}.tres, existuje={(ROOT/'assets'/(anim[0]+'.tres')).exists()}")
p(f"  => _visual('player') na 2 mistech: radek 283 (hráč) a 327 (NPC!)")
for i, ln in enumerate(game.splitlines(), 1):
    if "_visual(" in ln:
        p(f"     radek {i}: {ln.strip()}")
p()
p("DUSLEDEK: hra nacita presne tato jmena spritu:")
for n in sorted(set(used)):
    f = ROOT / "assets" / "sprites" / f"{n}.png"
    p(f"   {n:8s} -> assets/sprites/{n}.png  existuje={f.exists()}")

p()
p("=" * 78)
p("2) DLAZDICE, KTERE HRA NACITA")
p("=" * 78)
lv = json.loads((ROOT / "assets" / "levels" / "main.json").read_text(encoding="utf-8"))
p(f"main.json 'tiles' (kod dlazdice -> jmeno souboru): {lv['tiles']}")
p(f"main.json 'legend' (kod -> vyznam): {lv['legend']}")
grid = lv["grid"]
p(f"grid: {len(grid)} radku, delky radku: {sorted({len(r) for r in grid})}")
znaky = sorted({c for r in grid for c in r})
p(f"znaky pouzite v mrizce: {znaky}")
p(f"kody v 'tiles', ktere se v mrizce REALNE vyskytuji: {sorted(set(znaky) & set(lv['tiles']))}")
kod_na_dlazdici = lv["tiles"]
pouzite_dlazdice = sorted({kod_na_dlazdici[c] for c in znaky if c in kod_na_dlazdici})
p(f"  => dlazdice pouzite mapou: {pouzite_dlazdice}")
p(f"level.gd: TILE_DIR = {re.search(r'TILE_DIR := \"([^\"]+)\"', (ROOT/'scripts'/'level.gd').read_text(encoding='utf-8')).group(1)}")
p("level.gd sklada: TILE_DIR + tile_name + '.png'")
p()
p("game.gd pozadi: _texture('tiles/grass') -> assets/tiles/grass.png")
p(f"vsechny dlazdice pouzite hrou: {sorted(set(pouzite_dlazdice) | {'grass'})}")
tl = sorted((ROOT / "assets" / "tiles").glob("*.png"))
p(f"existujici PNG v assets/tiles/: {[f.stem for f in tl]}")
nep = [f.stem for f in tl if f.stem not in set(pouzite_dlazdice) | {"grass"}]
p(f"NEPOUZITE dlazdice (zmereno, ne odhad): {nep}")

p()
p("=" * 78)
p("3) KOLIK PNG V assets/sprites HRA ODKAZUJE -- dve meritka, obe dolozene")
p("=" * 78)

spr = sorted((ROOT / "assets" / "sprites").rglob("*.png"))
game_names = set(used)  # jmena, ktera projdou do _texture("sprites/<jmeno>")

# konfigurace, ktera o spritech mluvi cisly, ale nenacita je
cfg_files = ["assets/spec.json", "project.godot", "sprites.json"]
cfg_txt = {c: (ROOT / c).read_text(encoding="utf-8") for c in cfg_files if (ROOT / c).exists()}

p("(A) PRISNE -- soubor se skutecne nacte kodem hry (game.gd/level.gd):")
nA = 0
for f in spr:
    hit = f.stem in game_names
    if hit:
        nA += 1
    p(f"    {f.relative_to(ROOT).as_posix():44s} nacte hra: {hit}")
p(f"    => {nA} z {len(spr)}")

p()
p("(B) KONFIGURACE -- jmeno je zmínene v assets/spec.json / project.godot / sprites.json")
p("    (to je deklarace vzhledu, NE nacitani):")
for c, txt in cfg_txt.items():
    hits = sorted({f.stem for f in spr if re.search(r"\b" + re.escape(f.stem) + r"\b", txt)})
    p(f"    {c}: {hits}")

p()
p("(C) SIROKE -- jmeno v jakemkoliv textovem souboru repa mimo .godot, .git a {MYDIR}")
found = {f.stem: [] for f in spr}
for f in ROOT.rglob("*"):
    if not f.is_file():
        continue
    s = f.as_posix()
    if "/.git/" in s or "/.godot/" in s or MYDIR in s or f.suffix == ".png":
        continue
    if f.suffix not in (".gd", ".json", ".tscn", ".tres", ".cfg", ".md", ".py", ".mjs", ".yml", ".sh", ".cmd", ".txt", ".godot"):
        continue
    try:
        txt = f.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue
    for stem in found:
        if re.search(r"\b" + re.escape(stem) + r"\b", txt):
            found[stem].append(f.relative_to(ROOT).as_posix())
p(f"    prohledano souboru: {sum(1 for f in ROOT.rglob('*') if f.is_file())} (vsechny), z toho textovych vyse")
p(f"    PNG, jejichz jmeno se NEVYSKYTUJE NIKDE v textu repa: {[k for k, v in found.items() if not v]}")
p("    PNG, ktere se vyskytuji JEN v dokumentaci/testech/nastrojich (ne v kodu hry a ne v konfiguraci):")
for k, v in sorted(found.items()):
    if k in game_names:
        continue
    real = [x for x in v if x.startswith("scripts/") or x in cfg_files or x.startswith("assets/levels/") or x == "main.tscn"]
    if not real:
        p(f"      {k:16s} -> {v[:6]}{' ...' if len(v) > 6 else ''}")

p()
p("=" * 78)
p("4) tools/blender/sprites -- odkazuje je hra?")
p("=" * 78)
bl = sorted((ROOT / "tools" / "blender" / "sprites").rglob("*.png"))
p(f"celkem PNG: {len(bl)}")
code_scan = []
for c in ["scripts", "assets", "main.tscn", "project.godot", "export_presets.cfg"]:
    base = ROOT / c
    files = [base] if base.is_file() else [f for f in base.rglob("*") if f.is_file() and f.suffix in (".gd", ".json", ".tscn", ".cfg", ".godot")]
    for f in files:
        try:
            t = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if "tools/blender" in t or "blender/sprites" in t:
            code_scan.append(f.relative_to(ROOT).as_posix())
p(f"soubory v produkci (scripts/, assets/, main.tscn, project.godot, export_presets.cfg),")
p(f"ktere zminuji 'tools/blender' nebo 'blender/sprites': {code_scan if code_scan else 'ZADNY'}")
hry = 0
for f in bl:
    if re.search(r"\b" + re.escape(f.stem) + r"\b", (ROOT / "scripts" / "game.gd").read_text(encoding="utf-8")):
        hry += 1
p(f"PNG z tools/blender/sprites, jejichz jmeno je v game.gd: {hry}")

# duplicity mezi korenem a npc/
p()
root_png = {f.stem: hashlib.sha256(f.read_bytes()).hexdigest() for f in bl if f.parent == ROOT / "tools" / "blender" / "sprites"}
npc_png = {f.stem: hashlib.sha256(f.read_bytes()).hexdigest() for f in bl if f.parent != ROOT / "tools" / "blender" / "sprites"}
shodne = sorted(k for k in root_png if k in npc_png and root_png[k] == npc_png[k])
lisi = sorted(k for k in root_png if k in npc_png and root_png[k] != npc_png[k])
p(f"koren: {len(root_png)} PNG, npc/: {len(npc_png)} PNG")
p(f"  byte-identickych dvojic koren/npc: {len(shodne)}")
p(f"  lisi se: {len(lisi)} -> {lisi[:10]}{' ...' if len(lisi) > 10 else ''}")
p(f"  v koreni navic (mimo 128 vrstev): {sorted(set(root_png) - set(npc_png))}")

p()
p("=" * 78)
p("5) DUPLICITY uvnitr assets/sprites (stejny hash, jine jmeno)")
p("=" * 78)
byhash = {}
for f in spr:
    byhash.setdefault(hashlib.sha256(f.read_bytes()).hexdigest(), []).append(f.relative_to(ROOT).as_posix())
for h, fs in sorted(byhash.items()):
    if len(fs) > 1:
        p(f"  {h[:12]}: {fs}")

(Path(__file__).with_name("vysledek-assety2.txt")).write_text("\n".join(out), encoding="utf-8")
