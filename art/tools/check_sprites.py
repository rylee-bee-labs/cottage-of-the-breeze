#!/usr/bin/env python3
"""check_sprites.py: check sprite and tile pictures against the cottage art rules.

  check_sprites.py DIR_OR_FILES... [--size 128]

Each argument may be a single image file or a directory (a directory is checked
for its .png files, not its subdirectories). A file is good when it prints no
problem lines. Rules come from art/STYLE.md: transparent background, soft
darker-brown outlines (never pure black), and the sprite should fill some of the
tile but not all of it. Needs Pillow.
"""
import argparse
import sys
from pathlib import Path
from PIL import Image

ALPHA_TRANSPARENT = 128   # alpha below this is transparent
ALPHA_OPAQUE = 255        # alpha at this value is fully opaque
MIN_OPAQUE = 3.0          # percent; below this is "too empty"
MAX_OPAQUE = 95.0         # percent; above this is "too full"


def check_image(path, size=128):
    """Return a list of plain-language problems for one image (empty if good)."""
    problems = []
    with Image.open(path) as im:
        rgba = im.convert("RGBA")
    w, h = rgba.size
    total = w * h
    raw = rgba.tobytes()  # four bytes (r, g, b, a) per pixel, row by row

    def alpha(i):
        return raw[4 * i + 3]

    if (w, h) != (size, size):
        problems.append("wrong size (%dx%d, expected %dx%d)" % (w, h, size, size))

    if total and all(alpha(i) >= ALPHA_TRANSPARENT for i in range(total)):
        problems.append("no transparency")

    touches_edge = False
    if total:
        for i in range(w):
            if alpha(i) == ALPHA_OPAQUE:
                touches_edge = True
                break
        # NOTE: the BOTTOM row is allowed to be opaque. process_sprites.py puts the feet on the
        # bottom of the canvas on purpose, so a correct sprite always touches it.
        if not touches_edge:
            for y in range(h):
                if alpha(y * w) == ALPHA_OPAQUE or alpha(y * w + w - 1) == ALPHA_OPAQUE:
                    touches_edge = True
                    break
    if touches_edge:
        problems.append("opaque pixels touching the edge")

    opaque_pixels = 0
    blacks = 0
    for i in range(total):
        if alpha(i) >= ALPHA_TRANSPARENT:
            opaque_pixels += 1
            if (alpha(i) == ALPHA_OPAQUE
                    and raw[4 * i] == 0 and raw[4 * i + 1] == 0 and raw[4 * i + 2] == 0):
                blacks += 1
    if blacks:
        problems.append("a pure black pixel (%d of them)" % blacks)

    if total:
        percent = 100.0 * opaque_pixels / total
        if percent < MIN_OPAQUE:
            problems.append("too empty (%.1f%% opaque)" % percent)
        elif percent > MAX_OPAQUE:
            problems.append("too full (%.1f%% opaque)" % percent)
    return problems


def gather_files(paths):
    """Turn the arguments into a flat, ordered list of files to check."""
    files = []
    for arg in paths:
        p = Path(arg)
        if p.is_dir():
            files.extend(sorted(f for f in p.iterdir() if f.is_file() and f.suffix.lower() == ".png"))
        else:
            files.append(p)
    return files


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Check sprite and tile pictures against the cottage art rules.")
    ap.add_argument("paths", nargs="+", metavar="DIR_OR_FILES")
    ap.add_argument("--size", type=int, default=128,
                    help="expected width and height in pixels (default: 128)")
    a = ap.parse_args(argv)

    for arg in a.paths:
        if not Path(arg).exists():
            print("no such file or directory: %s" % arg, file=sys.stderr)
            return 2

    any_problem = False
    for path in gather_files(a.paths):
        problems = check_image(path, a.size)
        if problems:
            any_problem = True
            for problem in problems:
                print("%s: %s" % (path, problem))
        else:
            print("ok %s" % path)
    return 1 if any_problem else 0


if __name__ == "__main__":
    sys.exit(main())
