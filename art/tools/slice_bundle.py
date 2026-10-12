#!/usr/bin/env python3
"""Cut a bundled Codex sheet (a grid of separate subjects on flat #00FF00) into game sprites.

Bundling (2026-10-12): one image call draws a whole lineup or icon set together, so every subject shares one
style pass; this script cuts the grid apart. Each cell is keyed, cropped to its subject and fitted into a
transparent square (default 128 px, the pack's sprite size), centred for items or standing on the bottom edge
for characters.

    python3 art/tools/slice_bundle.py SHEET.png --grid 3x3 --names a,b,c,... --out DIR [--size 128] [--stand]

A name of `-` skips that cell (pass it as --names=-,a,b so the leading dash is not read as a flag).

Why not process_sprites.py --grid: that one floods the backdrop in from the corners, so green
enclosed by the subject (between curls, inside a net) stays; a #00FF00 bundle needs every backdrop
pixel keyed. Outfit greens (moss shawls, dark boots) are far from #00FF00 and survive the key.
"""
import argparse
from pathlib import Path

from PIL import Image


def key(im):
    im = im.convert("RGBA")
    px = im.load()
    W, H = im.size
    for y in range(H):
        for x in range(W):
            r, g, b, _ = px[x, y]
            if g > 180 and r < 120 and b < 120 and g - max(r, b) > 80:   # the backdrop, and its anti-aliased rim
                px[x, y] = (0, 0, 0, 0)
    for y in range(1, H - 1):        # despill: a green-tinted edge pixel next to the cut-away backdrop
        for x in range(1, W - 1):
            r, g, b, a = px[x, y]
            if a and g > max(r, b) + 30 and any(px[x + dx, y + dy][3] == 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px[x, y] = (r, max(r, b), b, a)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sheet")
    ap.add_argument("--grid", required=True, help="COLSxROWS, e.g. 3x3")
    ap.add_argument("--names", required=True, help="comma list, row by row; '-' skips a cell")
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", type=int, default=128)
    ap.add_argument("--margin", type=int, default=4)
    ap.add_argument("--stand", action="store_true", help="characters: stand on the bottom edge instead of centring")
    a = ap.parse_args()
    cols, rows = (int(v) for v in a.grid.lower().split("x"))
    names = a.names.split(",")
    if len(names) != cols * rows:
        raise SystemExit(f"{len(names)} names for a {cols}x{rows} grid")
    sheet = Image.open(a.sheet)
    W, H = sheet.size
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for i, name in enumerate(names):
        if name == "-":
            continue
        c, r = i % cols, i // cols
        cell = key(sheet.crop((c * W // cols, r * H // rows, (c + 1) * W // cols, (r + 1) * H // rows)))
        bb = cell.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox()
        if not bb:
            raise SystemExit(f"cell {i} ({name}) is empty")
        f = cell.crop(bb)
        box = a.size - 2 * a.margin
        s = min(box / f.width, box / f.height)
        f = f.resize((max(1, round(f.width * s)), max(1, round(f.height * s))), Image.LANCZOS)
        canvas = Image.new("RGBA", (a.size, a.size), (0, 0, 0, 0))
        x = (a.size - f.width) // 2
        y = a.size - a.margin - f.height if a.stand else (a.size - f.height) // 2
        canvas.alpha_composite(f, (x, y))
        canvas.save(out / f"{name}.png", optimize=True)
        print(f"{name}.png  {f.width}x{f.height} in {a.size}")


if __name__ == "__main__":
    main()
