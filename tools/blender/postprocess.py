# -*- coding: utf-8 -*-
"""Post-processing: Lanczos zmenšení renderů na 96px, sestavení srovnání."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "sprites")
os.makedirs(OUT, exist_ok=True)

LAYERS = ["body", "torso", "legs", "weapon"]
DIRS, FRAMES = 4, 8
CANVAS = 128
VISUAL_H = 96
FEET_Y = 112  # baseline chodidel v canvasu (dole 16px rezerva pro stín)

def load():
    imgs = {}
    for layer in LAYERS:
        for d in range(DIRS):
            for f in range(FRAMES):
                p = os.path.join(RAW, f"{layer}_d{d}_f{f}.png")
                imgs[(layer, d, f)] = Image.open(p).convert("RGBA")
    return imgs

def union_bbox(imgs):
    x0 = y0 = 10**9
    x1 = y1 = -10**9
    for im in imgs.values():
        a = im.split()[3]
        b = a.getbbox()
        if b:
            x0 = min(x0, b[0]); y0 = min(y0, b[1])
            x1 = max(x1, b[2]); y1 = max(y1, b[3])
    return (x0, y0, x1, y1)

def scale_into(im, box):
    """Ořízne obrázek na `box`, zmenší tak, aby výška = VISUAL_H, vloží na plátno."""
    crop = im.crop(box)
    bw = box[2] - box[0]; bh = box[3] - box[1]
    scale = VISUAL_H / bh
    nw = max(1, round(bw * scale))
    resized = crop.resize((nw, VISUAL_H), Image.LANCZOS)
    canvas = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    x = (CANVAS - nw) // 2
    y = FEET_Y - VISUAL_H
    canvas.alpha_composite(resized, (x, y))
    return canvas

def compose(frame_dict, d, f):
    """Složí vrstvy v pořadí slotů na jedno plátno."""
    out = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    for layer in ["body", "legs", "torso", "weapon"]:
        out.alpha_composite(frame_dict[(layer, d, f)])
    return out

def font(size):
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def label(draw, xy, text, fnt, fill=(255, 255, 255, 255)):
    draw.text(xy, text, font=fnt, fill=fill)

def main():
    imgs = load()
    box = union_bbox(imgs)
    print("union bbox", box, "h", box[3]-box[1], "w", box[2]-box[0])

    # 1) jednotlivé sprity
    sprites = {}
    for (layer, d, f), im in imgs.items():
        sp = scale_into(im, box)
        sprites[(layer, d, f)] = sp
        sp.save(os.path.join(OUT, f"{layer}_d{d}_f{f}.png"))

    # 2) srovnávací list
    fnt = font(14)
    fnt_big = font(20)
    cell = CANVAS
    pad = 6
    bg = (66, 70, 78, 255)
    dir_names = ["predni (J)", "bocni (V)", "zadni (S)", "bocni (Z)"]

    # --- pruhy chůze (zepředu i zboku, 4 framy, plná zbroj) ---
    def walk_strip(d, title):
        sw = FRAMES * cell + (FRAMES + 1) * pad
        sh = cell + 2 * pad + 26
        s = Image.new("RGBA", (sw, sh), bg)
        drow = ImageDraw.Draw(s)
        for f in range(FRAMES):
            x = pad + f * (cell + pad)
            s.alpha_composite(compose(sprites, d, f), (x, pad + 24))
        label(drow, (pad, pad), title, fnt_big)
        return s

    strip_f = walk_strip(0, "chuze zepredu (4 framy, plna zbroj)")
    strip_s = walk_strip(1, "chuze zboku (4 framy, plna zbroj)")

    # --- nahy vs zbroj, 4 smery ---
    rows = 2
    cols = DIRS
    w = cols * cell + (cols + 1) * pad
    h = rows * cell + (rows + 1) * pad + 30
    sheet = Image.new("RGBA", (w, h), bg)
    draw = ImageDraw.Draw(sheet)
    for d in range(DIRS):
        col_x = pad + d * (cell + pad)
        # nahy (body)
        y_n = pad + 24
        sheet.alpha_composite(sprites[("body", d, 1)], (col_x, y_n))
        label(draw, (col_x + 4, y_n + 4), f"{dir_names[d]}\nnahe telo", fnt)
        # zbroj
        y_a = pad + 24 + cell + pad
        sheet.alpha_composite(compose(sprites, d, 1), (col_x, y_a))
        label(draw, (col_x + 4, y_a + 4), f"{dir_names[d]}\nve zbroji", fnt)
    label(draw, (pad, pad), "nahe telo vs ve zbroji (frame 1, 4 smery)", fnt_big)

    # --- spojit pruhy a list ---
    total_h = strip_f.height + 8 + strip_s.height + 8 + h
    total_w = max(strip_f.width, w)
    total = Image.new("RGBA", (total_w, total_h), bg)
    total.alpha_composite(strip_f, (0, 0))
    total.alpha_composite(strip_s, (0, strip_f.height + 8))
    total.alpha_composite(sheet, (0, strip_f.height + 8 + strip_s.height + 8))
    total.convert("RGB").save(os.path.join(OUT, "_compare.png"))
    print("saved sprites:", len(sprites), "->", OUT)
    print("saved compare:", os.path.join(OUT, "_compare.png"))

if __name__ == "__main__":
    main()
