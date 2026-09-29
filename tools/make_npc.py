# -*- coding: utf-8 -*-
"""NPC = přebarvená postava (hue rotace tuniky, desaturace kalhot)."""
import os
from PIL import Image

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools", "blender", "sprites")
DST = os.path.join(SRC, "npc")
os.makedirs(DST, exist_ok=True)

DIRS, FRAMES = 4, 8
LAYERS = ["body", "torso", "legs", "weapon"]

def hue_shift(im, delta_deg):
    rgb = im.convert("RGB")
    alpha = im.split()[3]
    hsv = rgb.convert("HSV")
    h, s, v = hsv.split()
    shift = int(round(delta_deg * 255.0 / 360.0))
    h = h.point(lambda x: (x + shift) % 256)
    out = Image.merge("HSV", (h, s, v)).convert("RGB")
    out.putalpha(alpha)
    return out

def desaturate(im, factor=0.25):
    rgb = im.convert("RGB")
    alpha = im.split()[3]
    hsv = rgb.convert("HSV")
    h, s, v = hsv.split()
    s = s.point(lambda x: int(x * factor))
    out = Image.merge("HSV", (h, s, v)).convert("RGB")
    out.putalpha(alpha)
    return out

def main():
    for d in range(DIRS):
        for f in range(FRAMES):
            for layer in LAYERS:
                p = os.path.join(SRC, f"{layer}_d{d}_f{f}.png")
                if not os.path.exists(p):
                    continue
                im = Image.open(p).convert("RGBA")
                if layer == "torso":
                    im = hue_shift(im, -93)      # modrá -> zelená
                elif layer == "legs":
                    im = desaturate(im, 0.30)     # hnědá -> šedá
                # body i weapon zůstávají
                im.save(os.path.join(DST, f"{layer}_d{d}_f{f}.png"))
    print("NPC sprites ->", DST)

if __name__ == "__main__":
    main()
