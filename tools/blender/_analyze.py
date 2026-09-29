import sys
from PIL import Image
import numpy as np

im = Image.open(r'C:\Users\Ssevc\Local-Deepseek\gameforge\projects\uo-sandbox\tools\blender\preview.png').convert('RGBA')
a = np.array(im)
alpha = a[:, :, 3]
rgb = a[:, :, :3].astype(np.int32)
H, W = alpha.shape
mask = alpha > 10
ys, xs = np.where(mask)
top, bot = ys.min(), ys.max()
left, right = xs.min(), xs.max()
print('bbox x', left, right, 'y', top, bot, 'h', bot-top, 'w', right-left)

# profil sirky po radcich (odshora dolu)
height = bot - top
print('height/head_count: height=', height)
for i in range(12):
    y0 = top + height * i // 12
    y1 = top + height * (i + 1) // 12
    band = mask[y0:y1, :]
    if band.any():
        cols = np.where(band.any(axis=0))[0]
        print(f'  band {i:2d} y{y0:4d}-{y1:4d}: width {cols.max()-cols.min()} center {cols.mean():.0f}')
    else:
        print(f'  band {i:2d} y{y0:4d}-{y1:4d}: EMPTY')

# barvy (jen neprůhledné pixely)
op = rgb[mask]
print('opaque px', len(op))
# vzorek dominantnich barev (kvatizace)
q = (op // 32) * 32
uniq, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
order = np.argsort(-counts)[:8]
for i in order:
    print('  color', tuple(uniq[i]), 'count', counts[i], f'{counts[i]/len(op)*100:.1f}%')
