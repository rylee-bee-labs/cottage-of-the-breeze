#!/usr/bin/env python3
"""process_sprites.py: cut a sprite out of a picture and set it on the game's canvas.

  process_sprites.py IN.png OUT.png [--size 128] [--tolerance 28]
  process_sprites.py --grid COLSxROWS SHEET.png OUTDIR PREFIX [--size 128]
                     [--names down,left,right,up]

Background removal floods in from the four corners, so only background that touches an
edge goes away: a hole inside the subject stays opaque. The cut-out is trimmed, scaled to
fit inside SIZE x SIZE (never upscaled more than 2x) and pasted bottom-aligned on a
transparent canvas, feet on the floor. --grid cuts an evenly divided COLSxROWS sheet into
cells and writes PREFIX_<row>_<col>.png for each, row names from --names (top row first),
columns counted from 1. Needs Pillow:  uv run --with pillow art/tools/process_sprites.py ...
"""
import argparse
import os
import sys
from collections import deque

from PIL import Image


def fail(message):
    """A plain one-line problem, exit 2, with no traceback."""
    print(message, file=sys.stderr)
    raise SystemExit(2)


def open_image(path):
    """Open a picture as RGBA, or fail plainly if it cannot be read."""
    try:
        return Image.open(path).convert("RGBA")
    except (OSError, ValueError) as exc:
        fail(f"cannot read {path}: {exc}")


def remove_background(img, tolerance):
    """Flood-fill in from the four corners, matching the corner colour per channel.

    Only pixels reached from a corner are cleared, so an enclosed hole of the background
    colour stays opaque. If the corners are already transparent, keep the existing alpha.
    """
    img = img.convert("RGBA")
    w, h = img.size
    px = img.load()
    corners = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    if all(px[x, y][3] < 128 for x, y in corners):
        return img  # already a cut-out
    seen = bytearray(w * h)
    queue = deque()
    for x, y in corners:
        r, g, b, a = px[x, y]
        if a >= 128 and not seen[y * w + x]:
            seen[y * w + x] = 1
            queue.append((x, y, r, g, b))
    while queue:
        x, y, r, g, b = queue.popleft()
        px[x, y] = (r, g, b, 0)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                nr, ng, nb, na = px[nx, ny]
                if (na >= 128
                        and abs(nr - r) <= tolerance
                        and abs(ng - g) <= tolerance
                        and abs(nb - b) <= tolerance):
                    seen[ny * w + nx] = 1
                    queue.append((nx, ny, r, g, b))
    return img


def process_one(img, size, tolerance):
    """One sprite: background off, trimmed, fitted inside size x size, feet on the floor."""
    cut = remove_background(img, tolerance)
    bbox = cut.getchannel("A").getbbox()
    if bbox is None:
        fail("no content to cut out (every pixel is transparent)")
    cut = cut.crop(bbox)
    w, h = cut.size
    scale = min(size / w, size / h)
    if scale > 2.0:
        scale = 2.0  # never upscale more than 2x
    new_w = max(1, min(size, round(w * scale)))
    new_h = max(1, min(size, round(h * scale)))
    cut = cut.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(cut, ((size - new_w) // 2, size - new_h), cut)
    return canvas


def parse_grid(spec):
    """COLSxROWS like 4x4, or fail plainly."""
    bits = spec.lower().split("x")
    if len(bits) != 2:
        fail(f"--grid wants COLSxROWS like 4x4, got {spec!r}")
    try:
        cols, rows = int(bits[0]), int(bits[1])
    except ValueError:
        fail(f"--grid wants whole numbers like 4x4, got {spec!r}")
    if cols < 1 or rows < 1:
        fail(f"--grid needs positive numbers, got {spec!r}")
    return cols, rows


def main(argv=None):
    ap = argparse.ArgumentParser(description="Cut sprites out and size them for the game.")
    ap.add_argument("--grid", metavar="COLSxROWS", help="cut a sheet into equal cells")
    ap.add_argument("--size", type=int, default=128, help="canvas size in pixels (default 128)")
    ap.add_argument("--tolerance", type=int, default=28, help="per-channel colour match (default 28)")
    ap.add_argument("--names", help="comma-separated row names, top row first (grid mode)")
    ap.add_argument("args", nargs="*")
    a = ap.parse_args(argv)

    if a.size < 1:
        fail("--size must be 1 or more")

    if a.grid is None:
        if len(a.args) != 2:
            ap.error("single mode needs IN.png OUT.png")
        in_path, out_path = a.args
        out = process_one(open_image(in_path), a.size, a.tolerance)
        out.save(out_path)
        print(f"wrote {out_path}")
        return 0

    cols, rows = parse_grid(a.grid)
    if len(a.args) != 3:
        ap.error("--grid mode needs SHEET.png OUTDIR PREFIX")
    sheet_path, outdir, prefix = a.args
    if a.names is None:
        names = [f"r{i + 1}" for i in range(rows)]
    else:
        names = [n.strip() for n in a.names.split(",")]
        if len(names) != rows:
            fail(f"--names has {len(names)} entries but the grid has {rows} rows")

    sheet = open_image(sheet_path)
    w, h = sheet.size
    if w % cols:
        fail(f"sheet width {w} does not divide evenly by {cols} columns")
    if h % rows:
        fail(f"sheet height {h} does not divide evenly by {rows} rows")
    os.makedirs(outdir, exist_ok=True)
    cw, ch = w // cols, h // rows
    for r in range(rows):
        for c in range(cols):
            cell = sheet.crop((c * cw, r * ch, (c + 1) * cw, (r + 1) * ch))
            out = process_one(cell, a.size, a.tolerance)
            path = os.path.join(outdir, f"{prefix}_{names[r]}_{c + 1}.png")
            out.save(path)
            print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
