#!/usr/bin/env python3
"""mock_room.py: a quick room mock at the game's REAL tile size, to judge scale and repetition.

  mock_room.py OUT.jpg --wall W.png --floor F.png [--rug R.png] [--grass G.png] [--path P.png]
                       [--tile 96] [--cols 14] [--rows 9]

Single tiles hide problems a whole room shows: a floor that reads as stripes, a wall that repeats in a
grid, an object (like a rug) that is not a tile. Needs Pillow.
"""
import argparse
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("out")
for k in ("wall", "floor", "rug", "grass", "path"):
    ap.add_argument("--" + k)
ap.add_argument("--tile", type=int, default=96); ap.add_argument("--cols", type=int, default=14); ap.add_argument("--rows", type=int, default=9)
a = ap.parse_args()
T = a.tile
def load(p): return Image.open(p).convert("RGB").resize((T, T), Image.LANCZOS) if p else None
wall, floor, rug, grass, path = (load(getattr(a, k)) for k in ("wall", "floor", "rug", "grass", "path"))
if not (wall and floor):
    raise SystemExit("--wall and --floor are required")
room = Image.new("RGB", (a.cols * T, a.rows * T))
mid = a.cols // 2
for y in range(a.rows):
    for x in range(a.cols):
        t = wall if x in (0, a.cols - 1) or y in (0, a.rows - 1) else floor
        if path and y == a.rows - 1 and x in (mid - 1, mid):
            t = path
        if grass and y > a.rows - 3 and (x < 3 or x > a.cols - 4):
            t = grass
        room.paste(t, (x * T, y * T))
if rug:
    for dx in (mid - 1, mid):
        for dy in (a.rows // 2 - 1, a.rows // 2):
            room.paste(rug, (dx * T, dy * T))
room.save(a.out, quality=88)
print(a.out, room.size)
