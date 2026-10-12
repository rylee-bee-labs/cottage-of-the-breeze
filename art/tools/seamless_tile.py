#!/usr/bin/env python3
"""Cut a painted floor texture out of a bundled sheet and make it tile without seams.

    python3 art/tools/seamless_tile.py SHEET.png --grid 2x2 --cell 0 --out tiles/NAME.webp [--size 96]

An image model paints a texture whose left edge does not meet its right edge, so a floor of them shows a
grid of seams. The fix is the old one: blend the texture with a copy of itself shifted by half its width and
height, weighted so the middle comes from the original and the edges from the shifted copy. The shifted
copy's edges are the original's middle, which is continuous across the wrap, so the result tiles. `--inset`
trims the cell first, which drops the divider lines a grid prompt draws between quarters.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageChops


def seamless(im):
    w, h = im.size
    shifted = ImageChops.offset(im, w // 2, h // 2)
    mask = Image.new("L", (w, h))
    px = mask.load()
    for y in range(h):
        for x in range(w):
            # 255 in the middle, 0 at every edge; a smooth tent, so no line shows where the two copies meet
            dx = 1 - abs(2 * x / (w - 1) - 1)
            dy = 1 - abs(2 * y / (h - 1) - 1)
            px[x, y] = round(255 * min(1.0, 2.2 * min(dx, dy)))
    return Image.composite(im, shifted, mask)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sheet")
    ap.add_argument("--grid", default="1x1", help="COLSxROWS")
    ap.add_argument("--cell", type=int, default=0, help="row-major cell index")
    ap.add_argument("--inset", type=float, default=0.04, help="fraction trimmed off each cell edge")
    ap.add_argument("--size", type=int, default=96)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cols, rows = (int(v) for v in a.grid.lower().split("x"))
    sheet = Image.open(a.sheet).convert("RGB")
    W, H = sheet.size
    c, r = a.cell % cols, a.cell // cols
    x0, y0, x1, y1 = c * W // cols, r * H // rows, (c + 1) * W // cols, (r + 1) * H // rows
    side = min(x1 - x0, y1 - y0)
    pad = round(side * a.inset)
    cell = sheet.crop((x0 + pad, y0 + pad, x0 + side - pad, y0 + side - pad))
    tile = seamless(cell.resize((512, 512), Image.LANCZOS)).resize((a.size, a.size), Image.LANCZOS)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    tile.save(out, quality=88, method=6) if out.suffix == ".webp" else tile.save(out)
    print(f"{out} {a.size}x{a.size}")


if __name__ == "__main__":
    main()
