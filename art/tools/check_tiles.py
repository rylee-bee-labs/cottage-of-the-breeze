#!/usr/bin/env python3
"""check_tiles.py: check grid tile pictures against the cottage art rules.

  check_tiles.py DIR_OR_FILES... [--grid COLSxROWS] [--tile 96]

Each argument may be a single image file or a directory (a directory is checked
for its .png and .webp files, not its subdirectories). A file is good when it
prints no problem lines. A grid tile must be exactly COLS*TILE by ROWS*TILE,
fully opaque, free of pure black pixels, and free of visible seams between
cells. Needs Pillow:
  uv run --with pillow art/tools/check_tiles.py ...
"""
import argparse
import sys
from pathlib import Path
from PIL import Image

ALPHA_OPAQUE = 255        # alpha at this value is fully opaque
SEAM_FACTOR = 2.5         # an edge this many times sharper than the cells is a seam
IMAGE_SUFFIXES = (".png", ".webp")


def fail(message):
    """A plain one-line problem, exit 2, with no traceback."""
    print(message, file=sys.stderr)
    raise SystemExit(2)


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


def line_diff(raw, w, h, vertical, index):
    """Mean absolute per-channel difference between two neighbouring pixel lines.

    vertical compares pixel columns index and index+1; otherwise rows.
    """
    total = 0
    if vertical:
        for y in range(h):
            i = 4 * (y * w + index)
            j = i + 4
            total += (abs(raw[i] - raw[j])
                      + abs(raw[i + 1] - raw[j + 1])
                      + abs(raw[i + 2] - raw[j + 2]))
        return total / (3.0 * h)
    for x in range(w):
        i = 4 * (index * w + x)
        j = i + 4 * w
        total += (abs(raw[i] - raw[j])
                  + abs(raw[i + 1] - raw[j + 1])
                  + abs(raw[i + 2] - raw[j + 2]))
    return total / (3.0 * w)


def has_seam(raw, w, h, cols, rows, tile):
    """True when any internal cell edge is far sharper than the cell interiors."""
    down_edges = [k * tile for k in range(1, cols)]
    across_edges = [k * tile for k in range(1, rows)]

    interior = []
    for x in range(w - 1):
        if (x + 1) not in down_edges:
            interior.append(line_diff(raw, w, h, True, x))
    for y in range(h - 1):
        if (y + 1) not in across_edges:
            interior.append(line_diff(raw, w, h, False, y))

    edges = [line_diff(raw, w, h, True, e - 1) for e in down_edges]
    edges += [line_diff(raw, w, h, False, e - 1) for e in across_edges]
    if not edges:
        return False

    interior_mean = sum(interior) / len(interior) if interior else 0.0
    if interior_mean <= 0:
        # a flat interior: any edge at all is a seam
        return any(edge > 0 for edge in edges)
    return any(edge > SEAM_FACTOR * interior_mean for edge in edges)


def check_image(path, cols=3, rows=3, tile=96):
    """Return a list of plain-language problems for one tile picture (empty if good)."""
    problems = []
    with Image.open(path) as im:
        rgba = im.convert("RGBA")
    w, h = rgba.size
    expect_w, expect_h = cols * tile, rows * tile
    total = w * h
    raw = rgba.tobytes()  # four bytes (r, g, b, a) per pixel, row by row

    if (w, h) != (expect_w, expect_h):
        problems.append("wrong size (%dx%d, expected %dx%d)" % (w, h, expect_w, expect_h))

    transparent = 0
    blacks = 0
    for i in range(total):
        if raw[4 * i + 3] != ALPHA_OPAQUE:
            transparent += 1
        elif raw[4 * i] == 0 and raw[4 * i + 1] == 0 and raw[4 * i + 2] == 0:
            blacks += 1
    if transparent:
        problems.append("a transparent pixel (%d of them)" % transparent)
    if blacks:
        problems.append("a pure black pixel (%d of them)" % blacks)

    if (w, h) == (expect_w, expect_h) and has_seam(raw, w, h, cols, rows, tile):
        problems.append("visible seam between cells")
    return problems


def gather_files(paths):
    """Turn the arguments into a flat, ordered list of files to check."""
    files = []
    for arg in paths:
        p = Path(arg)
        if p.is_dir():
            files.extend(sorted(f for f in p.iterdir()
                                if f.is_file() and f.suffix.lower() in IMAGE_SUFFIXES))
        else:
            files.append(p)
    return files


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Check grid tile pictures against the cottage art rules.")
    ap.add_argument("paths", nargs="+", metavar="DIR_OR_FILES")
    ap.add_argument("--grid", metavar="COLSxROWS", default="3x3",
                    help="cells across and down (default: 3x3)")
    ap.add_argument("--tile", type=int, default=96,
                    help="pixels per cell (default: 96)")
    a = ap.parse_args(argv)

    for arg in a.paths:
        if not Path(arg).exists():
            print("no such file or directory: %s" % arg, file=sys.stderr)
            return 2

    if a.tile < 1:
        fail("--tile must be 1 or more")
    cols, rows = parse_grid(a.grid)

    any_problem = False
    for path in gather_files(a.paths):
        problems = check_image(path, cols, rows, a.tile)
        if problems:
            any_problem = True
            for problem in problems:
                print("%s: %s" % (path, problem))
        else:
            print("ok %s" % path)
    return 1 if any_problem else 0


if __name__ == "__main__":
    sys.exit(main())
