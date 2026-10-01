#!/usr/bin/env python3
"""contact_sheet.py: lay pictures out in one labelled sheet so you can compare them by eye.

  contact_sheet.py OUT.jpg IMAGE [IMAGE ...] [--cell 250] [--cols 4] [--tile2x2]

--tile2x2 shows each picture repeated 2x2, the quick way to spot seams and obvious repetition.
Needs Pillow:  uv run --with pillow art/tools/contact_sheet.py ...
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("images", nargs="+")
ap.add_argument("--cell", type=int, default=250); ap.add_argument("--cols", type=int, default=4)
ap.add_argument("--tile2x2", action="store_true")
a = ap.parse_args()
try:
    small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
except OSError:
    small = ImageFont.load_default()
C, PAD, LAB = a.cell, 12, 22
inner = C // 2 if a.tile2x2 else C
rows = (len(a.images) + a.cols - 1) // a.cols
sheet = Image.new("RGB", (PAD + a.cols * (C + PAD), PAD + rows * (C + LAB + PAD)), (24, 32, 34))
d = ImageDraw.Draw(sheet)
for i, p in enumerate(a.images):
    r, c = divmod(i, a.cols)
    x, y = PAD + c * (C + PAD), PAD + r * (C + LAB + PAD)
    im = Image.open(p).convert("RGB").resize((inner, inner), Image.LANCZOS)
    for dx in range(2 if a.tile2x2 else 1):
        for dy in range(2 if a.tile2x2 else 1):
            sheet.paste(im, (x + dx * inner, y + dy * inner))
    d.text((x, y + C + 3), Path(p).stem + (" (tiled 2x2)" if a.tile2x2 else ""), fill=(157, 176, 176), font=small)
sheet.save(a.out, quality=88)
print(a.out, sheet.size)
