#!/usr/bin/env python3
"""process_tiles.py: make a grid tile picture the exact size the engine draws.

  process_tiles.py IN OUT --grid COLSxROWS [--tile 96]

A grid tile is ONE picture drawn as COLSxROWS cells; the engine draws cell
(x mod cols, y mod rows), so a 3x3 grid of 96 px cells is 288x288. The picture
is centre-cropped to a square, resized to exactly COLS*TILE by ROWS*TILE,
flattened onto an opaque background (no alpha holes), and saved as webp or png
by OUT's suffix. Needs Pillow:
  uv run --with pillow art/tools/process_tiles.py ...
"""
import argparse
import os
import sys

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


def parse_grid(spec):
    """COLSxROWS like 3x3, or fail plainly."""
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


def centre_square(img):
    """Crop the largest centred square of the picture, with no margin."""
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    return img.crop((left, top, left + side, top + side))


def flatten(img):
    """Put the picture on an opaque white background, dropping any alpha."""
    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    bg.alpha_composite(img)
    return bg.convert("RGB")


def process_one(img, cols, rows, tile):
    """Centre-crop, resize to cols*tile by rows*tile, and make it opaque."""
    square = flatten(centre_square(img))
    return square.resize((cols * tile, rows * tile), Image.LANCZOS)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Make a grid tile picture the exact size the engine draws.")
    ap.add_argument("input", metavar="IN", help="source picture")
    ap.add_argument("output", metavar="OUT", help="output .png or .webp")
    ap.add_argument("--grid", metavar="COLSxROWS", required=True,
                    help="cells across and down, like 3x3")
    ap.add_argument("--tile", type=int, default=96, help="pixels per cell (default 96)")
    a = ap.parse_args(argv)

    if a.tile < 1:
        fail("--tile must be 1 or more")
    cols, rows = parse_grid(a.grid)
    suffix = os.path.splitext(a.output)[1].lower()
    if suffix not in (".png", ".webp"):
        fail("OUT must end in .png or .webp")

    out = process_one(open_image(a.input), cols, rows, a.tile)
    out.save(a.output)
    print(f"wrote {a.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
