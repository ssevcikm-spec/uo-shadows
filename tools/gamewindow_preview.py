# -*- coding: utf-8 -*-
"""Náhled herního okna (960×540): iso dlaždice + postava + předměty v herním měřítku."""
import os
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ITEM_DIR = os.path.join(HERE, "..", "assets", "sprites", "items")
CHAR_DIR = os.path.join(HERE, "..", "tools", "blender", "sprites")

VW, VH = 960, 540
TW, TH = 96, 48   # iso dlaždice (diamant 96×48)

def diamond_tile(tex, w=TW, h=TH):
    t = tex.resize((w, h), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    d.polygon([(w // 2, 0), (w, h // 2), (w // 2, h), (0, h // 2)], fill=255)
    t.putalpha(m)
    return t

def build_floor():
    grass = Image.open(os.path.join(ITEM_DIR, "grass_tex.png")).convert("RGB")
    dirt = Image.open(os.path.join(ITEM_DIR, "dirt_tex.png")).convert("RGB")
    base = grass.resize((VW, VH), Image.LANCZOS).convert("RGBA")
    dirt_tile = diamond_tile(dirt)
    # šachovnice: dirt na lichých (i+j), jen uvnitř viewportu
    for i in range(-4, 26):
        for j in range(-4, 26):
            cx = (i - j) * (TW // 2)
            cy = (i + j) * (TH // 2)
            if -TW < cx < VW and -TH < cy < VH and (i + j) % 2 == 1:
                base.alpha_composite(dirt_tile, (int(cx - TW // 2), int(cy - TH // 2)))
    return base

def shadow(draw, cx, cy, w, opacity=0.35):
    # elipsa stínu (v kódu, ne model)
    import math
    sw = max(6, int(w * 0.7))
    sh = max(3, sw // 2)
    draw.ellipse([cx - sw // 2, cy - sh // 2, cx + sw // 2, cy + sh // 2],
                 fill=(0, 0, 0, int(255 * opacity)))

def main():
    floor = build_floor()
    draw = ImageDraw.Draw(floor)

    # postava ve zbroji (zepředu, frame 1) — 128×128, postava 96px
    char = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    for layer in ("body", "legs", "torso", "weapon"):
        p = os.path.join(CHAR_DIR, f"{layer}_d0_f1.png")
        if os.path.exists(p):
            char.alpha_composite(Image.open(p).convert("RGBA"))

    # umístění: postava uprostřed na dlaždici, nohy na baselinu
    char_x, char_feet_y = VW // 2 - 64, 300
    shadow(draw, VW // 2, char_feet_y, 40)
    floor.alpha_composite(char, (char_x, char_feet_y - 128 + 16))

    # předměty kolem
    items = [
        ("sword_final.png", VW // 2 - 160, 360, 48),
        ("potion_final.png", VW // 2 + 110, 320, 32),
        ("coin_final.png", VW // 2 + 180, 400, 24),
    ]
    for name, x, y, vh in items:
        p = os.path.join(ITEM_DIR, name)
        if os.path.exists(p):
            im = Image.open(p).convert("RGBA")
            shadow(draw, x + im.width // 2, y + im.height, vh)
            floor.alpha_composite(im, (x, y - im.height // 2))

    out = os.path.join(ITEM_DIR, "_gamewindow_preview.png")
    floor.convert("RGB").save(out)
    print("saved", out, floor.size)

if __name__ == "__main__":
    main()
