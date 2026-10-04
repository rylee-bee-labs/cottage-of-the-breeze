#!/usr/bin/env python3
"""door_tile.py: set a cut-out door (from process_sprites.py) on a dark floor-coloured square tile.

  door_tile.py DOOR.png OUT.webp [--bg 1a1d22]

The door is a sprite with a transparent background; a grid tile must be opaque, so this flattens it on the
floor colour the region's legend uses. Needs Pillow:  uv run --with pillow art/tools/door_tile.py ...
"""
import argparse

from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("door")
ap.add_argument("out")
ap.add_argument("--bg", default="1a1d22")
a = ap.parse_args()
door = Image.open(a.door).convert("RGBA")
bg = Image.new("RGBA", door.size, tuple(int(a.bg[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
bg.alpha_composite(door)
bg.convert("RGB").save(a.out)
print("wrote", a.out, bg.size)
