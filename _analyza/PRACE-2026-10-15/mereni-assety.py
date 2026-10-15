# mereni-assety.py -- meri PNG assety hry uo-shadows a jejich pouziti
# Spusteni: $env:PYTHONIOENCODING='utf-8'; python _analyza\PRACE-2026-10-15\mereni-assety.py
import hashlib
import json
import re
import subprocess
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
out = []


def p(s=""):
    out.append(str(s))
    print(s)


# ---------------------------------------------------------------- 1) pocty ---
p("=" * 78)
p("1) POCTY PNG")
p("=" * 78)

def pngs(d: Path):
    return sorted(d.rglob("*.png")) if d.exists() else []

sprites_all = pngs(ROOT / "assets" / "sprites")
sprites_top = [f for f in sprites_all if f.parent == ROOT / "assets" / "sprites"]
sprites_sub = [f for f in sprites_all if f.parent != ROOT / "assets" / "sprites"]
tiles = pngs(ROOT / "assets" / "tiles")
bl_all = pngs(ROOT / "tools" / "blender" / "sprites")
bl_root = [f for f in bl_all if f.parent == ROOT / "tools" / "blender" / "sprites"]
bl_sub = [f for f in bl_all if f.parent != ROOT / "tools" / "blender" / "sprites"]

p(f"assets/sprites/ rekurzivne   : {len(sprites_all)}   ( primo v assets/sprites: {len(sprites_top)}, v podadresarich: {len(sprites_sub)})")
p(f"  podadresare: {sorted({str(f.parent.relative_to(ROOT/'assets'/'sprites')) for f in sprites_sub})}")
p(f"assets/tiles/ rekurzivne     : {len(tiles)}")
p(f"tools/blender/sprites/ rekurz.: {len(bl_all)}   ( koren: {len(bl_root)}, podadresare: {len(bl_sub)})")
p(f"  podadresare: {sorted({str(f.parent.relative_to(ROOT/'tools'/'blender'/'sprites')) for f in bl_sub})}")
p(f"assets/sprites/items/        : {len(pngs(ROOT/'assets'/'sprites'/'items'))}")

# rozmer + hash kazdeho PNG v assets/sprites
p()
p("PNG v assets/sprites (rozmer, bajty, sha256 prvnich 12):")
for f in sprites_all:
    im = Image.open(f)
    h = hashlib.sha256(f.read_bytes()).hexdigest()[:12]
    rel = f.relative_to(ROOT).as_posix()
    p(f"  {rel:44s} {im.size[0]:5d}x{im.size[1]:<5d} {f.stat().st_size:9d} B  {h}")

# ------------------------------------------------- 2) co hra skutecne pouzije -
p()
p("=" * 78)
p("2) KTERE ASSETY HRA SKUTECNE ODEBIRA (staticky ze kodu)")
p("=" * 78)

gd_files = sorted((ROOT / "scripts").glob("*.gd"))
code = {f.name: f.read_text(encoding="utf-8") for f in gd_files}
allcode = "\n".join(code.values())

visual = re.findall(r'_visual\(\s*"([^"]+)"', allcode)
texture = re.findall(r'_texture\(\s*"([^"]+)"', allcode)
anim = re.findall(r'_animation_visual\(\s*"([^"]+)"', allcode)
p(f'_visual("X")        -> {sorted(set(visual))}   (volani: {len(visual)})')
p(f'_texture("X")       -> {sorted(set(texture))}  (volani: {len(texture)})')
p(f'_animation_visual() -> {sorted(set(anim))} -> hleda assets/<X>.tres')

# dlazdice: level.gd sklada TILE_DIR + tile_name + ".png"; jmena dlaždic jsou v assets/levels/*.json
lv = json.loads((ROOT / "assets" / "levels" / "main.json").read_text(encoding="utf-8"))
tile_names = set()
def walk_tiles(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("tile", "tiles", "dlazdice") and isinstance(v, str):
                tile_names.add(v)
            walk_tiles(v)
    elif isinstance(o, list):
        for v in o:
            walk_tiles(v)
walk_tiles(lv)
p(f"jmena dlazdic z assets/levels/main.json: {sorted(tile_names)}")

used_names = set(visual) | set(texture) | {t.replace("tiles/", "") for t in texture if t.startswith("tiles/")}
p(f"SKUTECNE ODEBIRANE (jmena): {sorted(used_names)}")
p(f"  z toho sprity: {sorted(set(visual))}")
p(f"  z toho dlazdice: {sorted({t for t in texture if t.startswith('tiles/')})}")

# ------------------------------------------------------- 3) odkazovanost PNG -
p()
p("=" * 78)
p("3) KOLIK PNG JE ODKAZOVANYCH -- dve meritka")
p("=" * 78)

# (A) PRISNE: jmeno souboru se objevi v kodu, ktery ho umi nacist
strict = set(visual) | {Path(t).name for t in texture} | set(anim)

# (B) SIROKE: jmeno (stem) se objevi kdekoliv v repu mimo samotny PNG a .godot cache
def repo_texts():
    seen = {}
    for pat in ("*.gd", "*.json", "*.tscn", "*.tres", "*.cfg", "*.md", "*.py", "*.mjs", "*.sh", "*.cmd", "*.yml", "*.txt", "*.godot"):
        for f in ROOT.rglob(pat):
            s = f.as_posix()
            if "/.git/" in s or "/.godot/" in s:
                continue
            try:
                seen[f] = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                pass
    return seen

texts = repo_texts()
p(f"prohledavanych textovych souboru v repu (bez .git a .godot): {len(texts)}")

strict_hits, broad_hits, nowhere = [], [], []
for f in sprites_all:
    stem = f.stem
    rel = f.relative_to(ROOT).as_posix()
    in_strict = stem in strict
    hits = []
    for tf, txt in texts.items():
        if tf == f:
            continue
        if stem in txt:
            hits.append(tf.relative_to(ROOT).as_posix())
    if in_strict:
        strict_hits.append(rel)
    if hits:
        broad_hits.append((rel, hits))
    else:
        nowhere.append(rel)

p(f"(A) PRISNE -- jmeno je v kodu, ktery ho nacita (_visual/_texture): {len(strict_hits)} z {len(sprites_all)}")
for s in sorted(strict_hits):
    p(f"      {s}")
p(f"(B) SIROKE -- jmeno se vyskytuje v NEJAKEM textovem souboru repa: {len(broad_hits)} z {len(sprites_all)}")
p(f"    nikde v repu (mimo .git/.godot) se nevyskytuje: {len(nowhere)}")
for s in sorted(nowhere)[:15]:
    p(f"      {s}")
if len(nowhere) > 15:
    p(f"      ... a dalsich {len(nowhere)-15}")

p()
p("Detail (B) -- kde vsude je jmeno zmínene (jen soubory, kde jde o realny odkaz):")
for rel, hits in sorted(broad_hits):
    interesting = [h for h in hits if not h.startswith("tools/") or h.endswith(".py")]
    p(f"  {rel}")
    p(f"      vsechny: {hits}")
    p(f"      mimo tools/blender/sprites: {interesting}")

# ------------------------------------------------- 4) player.png vs d0_f1 -----
p()
p("=" * 78)
p("4) assets/sprites/player.png vs slozenina vrstev d0_f1 (tvrzeni HANDOFF.md:170)")
p("=" * 78)
p("Postup: tools/blender/postprocess.py compose() sklada vrstvy v poradi")
p("        body, legs, torso, weapon pres sebe (alpha_composite). Vrstvy v")
p("        tools/blender/sprites/ jsou UZ zmensene na 128x128 platno")

SP = ROOT / "tools" / "blender" / "sprites"
for target, sub in [("assets/sprites/player.png", "."), ("assets/sprites/npc.png", "npc")]:
    tgt_path = ROOT / target
    base = SP / sub if sub != "." else SP
    layers = ["body", "legs", "torso", "weapon"]
    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    missing = []
    for lay in layers:
        f = base / f"{lay}_d0_f1.png"
        if not f.exists():
            missing.append(str(f))
            continue
        comp.alpha_composite(Image.open(f).convert("RGBA"))
    if missing:
        p(f"{target}: NEMERENO -- chybi vrstvy {missing}")
        continue
    tgt = Image.open(tgt_path).convert("RGBA")
    p(f"{target}: rozmer cil {tgt.size}, rozmer slozeniny {comp.size}")
    if tgt.size != comp.size:
        p("  -> rozmery se LISI, nelze porovnat pixel po pixelu")
        continue
    tb = tgt.tobytes()
    cb = comp.tobytes()
    same = tb == cb
    p(f"  pixel-identicke (RGBA bytes): {same}")
    p(f"  sha256 cil       : {hashlib.sha256(tb).hexdigest()}")
    p(f"  sha256 slozenina : {hashlib.sha256(cb).hexdigest()}")
    if not same:
        diff = sum(1 for a, b in zip(tb, cb) if a != b)
        # pocet lisi­cich se pixelu
        tp, cp = tgt.load(), comp.load()
        px = sum(1 for y in range(128) for x in range(128) if tp[x, y] != cp[x, y])
        p(f"  lisi se pixelu: {px} z 16384; bajtu: {diff}")
        comp.save(Path(__file__).with_name(f"rekonstrukce-{tgt_path.stem}.png"))
        p(f"  rekonstrukce ulozena: rekonstrukce-{tgt_path.stem}.png")

# ---------------------------------------------------- 5) kde je save.cfg -------
p()
p("=" * 78)
p("5) user:// -- kam se uklada (Godot ignoruje --user-data-dir)")
p("=" * 78)
p(f"APPDATA = {Path.home()/'AppData'/'Roaming'}")
ud = Path.home() / "AppData" / "Roaming" / "Godot" / "app_userdata"
if ud.exists():
    for d in sorted(ud.iterdir()):
        p(f"  {d.name}/")
        for f in sorted(d.rglob("*")):
            if f.is_file():
                p(f"      {f.relative_to(ud).as_posix()}  {f.stat().st_size} B")
else:
    p("  NEMERENO: slozka app_userdata neexistuje")

p()
head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True)
p(f"git rev-parse --short HEAD -> {head.stdout.strip()}")

(Path(__file__).with_name("vysledek-assety.txt")).write_text("\n".join(out), encoding="utf-8")
