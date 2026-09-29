# -*- coding: utf-8 -*-
"""Cesta B: odstranění pozadí (flood-fill) + Lanczos zmenšení předmětů na spec velikost."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "assets", "sprites", "items")
CHARS = os.path.join(HERE, "..", "tools", "blender", "sprites")

# visual_height, canvas (ze spec.json)
ITEMS = {
    "sword":  {"h": 48, "canvas": 64},
    "potion": {"h": 32, "canvas": 48},
    "coin":   {"h": 24, "canvas": 32},
    "ore":    {"h": 48, "canvas": 64},
    "chest":  {"h": 48, "canvas": 64},
}

def remove_bg(rgb):
    """Adaptivní odstranění pozadí podle barvy okraje (ne podle jasu!).
    Flood-fill od okrajů: odstraní pixely barevně blízké barvě pozadí."""
    border_px = np.concatenate([
        rgb[0, :, :], rgb[-1, :, :], rgb[:, 0, :], rgb[:, -1, :]
    ]).astype(np.float32)
    bg_color = border_px.mean(axis=0)
    bd = np.sqrt(((border_px - bg_color) ** 2).sum(axis=1))
    tol = float(max(18.0, np.percentile(bd, 90) * 3.0 + 12.0))
    dist = np.sqrt(((rgb.astype(np.float32) - bg_color) ** 2).sum(axis=2))
    bg = dist < tol
    lab, n = ndimage.label(bg)
    border = set(lab[0, :].tolist()) | set(lab[-1, :].tolist()) | \
             set(lab[:, 0].tolist()) | set(lab[:, -1].tolist())
    border.discard(0)
    mask = np.ones(bg.shape, dtype=bool)
    if border:
        mask[np.isin(lab, list(border))] = False
    return mask

def process(name):
    src = os.path.join(SRC, f"{name}.png")
    im = Image.open(src).convert("RGB")
    rgb = np.array(im)
    mask = remove_bg(rgb)
    alpha = (mask * 255).astype(np.uint8)
    rgba = np.dstack([rgb, alpha])

    ys, xs = np.where(alpha > 8)
    if len(ys) == 0:
        print(f"[{name}] PRAZDNY predmet, preskakuji")
        return None
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    crop = Image.fromarray(rgba[y0:y1 + 1, x0:x1 + 1], "RGBA")

    spec = ITEMS[name]
    bh = y1 - y0
    scale = spec["h"] / bh
    nw = max(1, round((x1 - x0) * scale))
    resized = crop.resize((nw, spec["h"]), Image.LANCZOS)

    canvas = Image.new("RGBA", (spec["canvas"], spec["canvas"]), (0, 0, 0, 0))
    cx = (spec["canvas"] - nw) // 2
    cy = spec["canvas"] - spec["h"] - 2  # spodek blízko dna canvasu
    canvas.alpha_composite(resized, (cx, cy))

    # metrika: zbytky pozadí = neprůhledné pixely u okrajů canvasu (do 3px)
    ca = np.array(canvas)[:, :, 3]
    border = np.concatenate([ca[0:3, :].ravel(), ca[-3:, :].ravel(),
                             ca[:, 0:3].ravel(), ca[:, -3:].ravel()])
    remnants = (border > 8).sum() / border.size
    out = os.path.join(SRC, f"{name}_final.png")
    canvas.save(out)
    print(f"[{name}] bbox {x1-x0}x{bh} -> {nw}x{spec['h']} v canvasu {spec['canvas']}, zbytky okraje {remnants*100:.1f}%")
    return canvas

def font(size):
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def main():
    finals = {}
    for name in ITEMS:
        c = process(name)
        if c:
            finals[name] = c

    # srovnávací list: předměty + postava (nahá / ve zbroji)
    bg = (66, 70, 78, 255)
    fnt = ImageFont.load_default()
    pad = 8
    cell = 128

    # načti postavu (nahá = body, ve zbroji = body+legs+torso+weapon) frame 1, zepředu
    def load_char(d, f):
        p = os.path.join(CHARS, f"{d}_d0_f{f}.png")
        return Image.open(p).convert("RGBA") if os.path.exists(p) else None

    def compose_char(d, f):
        out = Image.new("RGBA", (cell, cell), (0, 0, 0, 0))
        for layer in ("body", "legs", "torso", "weapon"):
            p = os.path.join(CHARS, f"{layer}_d{d}_f{f}.png")
            if os.path.exists(p):
                out.alpha_composite(Image.open(p).convert("RGBA"))
        return out

    naked = load_char("body", 1)
    armored = compose_char(0, 1)

    cols = 5
    w = cols * cell + (cols + 1) * pad
    h = cell + 2 * pad + 26
    sheet = Image.new("RGBA", (w, h), bg)
    draw = ImageDraw.Draw(sheet)
    cells = [("postava naha", naked), ("postava ve zbroji", armored)]
    for name in ITEMS:
        if name in finals:
            cells.append((name, finals[name]))
    for i, (label, im) in enumerate(cells):
        x = pad + i * (cell + pad)
        if im:
            # předměty centrovat, postavu nechat
            sheet.alpha_composite(im, (x, pad + 24))
        draw.text((x + 2, pad + 2), label, font=fnt, fill=(255, 255, 255, 255))
    out = os.path.join(SRC, "_items_compare.png")
    sheet.convert("RGB").save(out)
    print("saved", out)

if __name__ == "__main__":
    main()
