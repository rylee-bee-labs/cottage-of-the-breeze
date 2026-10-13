"""Make each grid cell of a #00FF00 sheet hold only its own subject: every blob (8-connected non-green
pixels) belongs to the cell its centre of mass falls in; parts of it in other cells are painted green there,
and its own cell is grown to hold all of it by re-centring. Writes a new sheet with even cells."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

src, cols, rows, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
im = np.array(Image.open(src).convert("RGB")).astype(int)
r, g, b = im[..., 0], im[..., 1], im[..., 2]
fg = ~((g > 150) & (r < 120) & (b < 120) & (g - np.maximum(r, b) > 80))
fg = ndimage.binary_opening(fg, iterations=1) | (fg & ndimage.binary_dilation(ndimage.binary_opening(fg, iterations=1), iterations=3))
lab, n = ndimage.label(fg, structure=np.ones((3, 3)))
H, Wd = fg.shape
cw, ch = Wd / cols, H / rows
sizes = ndimage.sum(fg, lab, range(1, n + 1))
coms = ndimage.center_of_mass(fg, lab, range(1, n + 1))
# each cell's biggest blob anchors it; small blobs join the cell of the nearest anchor
cells = {}
for i, (cy, cx) in enumerate(coms):
    c = (min(int(cx // cw), cols - 1), min(int(cy // ch), rows - 1))
    cells.setdefault(c, []).append(i)
CW, CH = int(cw * 1.5), int(ch * 1.5)
sheet = np.zeros((CH * rows, CW * cols, 3), np.uint8); sheet[..., 1] = 255
for (cx, cy), ids in cells.items():
    big = max(ids, key=lambda i: sizes[i])
    keep = [i for i in ids if sizes[i] > 0.002 * sizes[big] and sizes[i] > 30]
    mask = np.isin(lab, [i + 1 for i in keep])
    ys, xs = np.nonzero(mask)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    patch = np.where(mask[y0:y1, x0:x1, None], im[y0:y1, x0:x1], [0, 255, 0]).astype(np.uint8)
    ph, pw = patch.shape[:2]
    ox = cx * CW + (CW - pw) // 2; oy = cy * CH + (CH - ph) // 2
    sheet[oy:oy + ph, ox:ox + pw] = patch[:CH, :CW]
Image.fromarray(sheet).save(out)
print(out, {k: len(v) for k, v in sorted(cells.items())})
