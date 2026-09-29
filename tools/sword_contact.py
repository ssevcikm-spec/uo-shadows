# -*- coding: utf-8 -*-
"""Kontaktní list kandidátů meče (plné rendery, uživatel vybere)."""
import os
from PIL import Image, ImageDraw, ImageFont

SRC = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(SRC, "..", "assets", "sprites", "items")

def font(size):
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def main():
    names = [f"asword{i}.png" for i in range(1, 7)]
    cell = 300
    cols, rows = 3, 2
    pad = 12
    bg = (40, 44, 52, 255)
    fnt = font(22)
    w = cols * cell + (cols + 1) * pad
    h = rows * cell + (rows + 1) * pad + 8
    sheet = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(sheet)
    for i, name in enumerate(names):
        p = os.path.join(SRC, name)
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGB")
        im.thumbnail((cell - 8, cell - 8), Image.LANCZOS)
        c, r = i % cols, i // cols
        x = pad + c * (cell + pad) + (cell - im.width) // 2
        y = pad + r * (cell + pad) + (cell - im.height) // 2
        sheet.paste(im, (x, y))
        draw.text((pad + c * (cell + pad) + 4, pad + r * (cell + pad) + 4),
                  f"{i+1}", font=fnt, fill=(255, 255, 0))
    out = os.path.join(SRC, "_arming_sword_candidates.png")
    sheet.save(out)
    print("saved", out, sheet.size)

if __name__ == "__main__":
    main()
