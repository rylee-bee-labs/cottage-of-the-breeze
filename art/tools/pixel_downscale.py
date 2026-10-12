#!/usr/bin/env python3
"""pixel_downscale.py: turn a painted sheet into native pixels, pixel-exact.

  pixel_downscale.py IN OUT (--block N | --height N) [--palette PALETTE]

Every other Cottage art tool resizes with Image.LANCZOS, which smooths pixel
art. This is the pixel-exact step instead: the picture is downscaled by
nearest-neighbour block sampling, so each output pixel is the source pixel at
the centre of its block. No averaging and no interpolation, so the result holds
only colours the source already had, and alpha is copied through unchanged.
Optionally every pixel is then snapped to the nearest colour of a palette read
from a file, so the result sits exactly on the palette; with no --palette the
step is skipped. No palette is built in.

  --block N   the native size of the square output (a tile is 32).
  --height N  the native height of the output; width follows the source aspect
              (a person is 48 art pixels tall).

A palette file is JSON (a list of entries, or {"colors": [...]}) or one entry
per line of plain text. An entry is "#rrggbb", "r,g,b", [r, g, b] or
{"r": .., "g": .., "b": ..}. Needs Pillow:
  uv run --with pillow art/tools/pixel_downscale.py ...
"""
import argparse
import json
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


def _clean_colour(value):
    """One palette entry to (r, g, b), or None when it is not a colour."""
    if isinstance(value, dict):
        for key in ("rgb", "colour", "color"):
            if key in value:
                return _clean_colour(value[key])
        if "hex" in value:
            return _clean_colour(value["hex"])
        if all(k in value for k in ("r", "g", "b")):
            return _clean_colour([value["r"], value["g"], value["b"]])
        return None
    if isinstance(value, str):
        text = value.strip()
        if "," in text:
            parts = [p.strip() for p in text.split(",")]
            if len(parts) >= 3:
                return _clean_colour(parts[:3])
        text = text.lstrip("#")
        if len(text) == 6:
            try:
                return tuple(int(text[i:i + 2], 16) for i in (0, 2, 4))
            except ValueError:
                return None
        return None
    if isinstance(value, (list, tuple)) and len(value) >= 3:
        try:
            rgb = tuple(int(c) for c in value[:3])
        except (TypeError, ValueError):
            return None
        if all(0 <= c <= 255 for c in rgb):
            return rgb
    return None


def load_palette(path):
    """Read a palette file into a list of (r, g, b), in file order and unique."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        fail(f"cannot read palette {path}: {exc}")
    if text.lstrip()[:1] in "[{":
        try:
            data = json.loads(text)
        except ValueError as exc:
            fail(f"palette {path} is not valid JSON: {exc}")
        if isinstance(data, dict):
            for key in ("colors", "colours", "palette"):
                if key in data:
                    data = data[key]
                    break
            else:
                data = [data]
        entries = data if isinstance(data, list) else [data]
    else:
        entries = [line for line in text.splitlines() if line.strip()]
    colours = []
    for entry in entries:
        colour = _clean_colour(entry)
        if colour is not None and colour not in colours:
            colours.append(colour)
    if not colours:
        fail(f"palette {path} has no colours")
    return colours


def nearest_colour(rgb, palette):
    """The palette entry closest to rgb by squared RGB distance (ties: first)."""
    r, g, b = rgb
    best, best_d = palette[0], None
    for colour in palette:
        d = (r - colour[0]) ** 2 + (g - colour[1]) ** 2 + (b - colour[2]) ** 2
        if best_d is None or d < best_d:
            best, best_d = colour, d
    return best


def lock_palette(img, palette):
    """Snap every pixel to its nearest palette colour; alpha is left alone."""
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    cache = {}
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            key = (r, g, b)
            if key not in cache:
                cache[key] = nearest_colour(key, palette)
            nr, ng, nb = cache[key]
            px[x, y] = (nr, ng, nb, a)
    return img


def _centre_index(src_len, out_len, i):
    """The source pixel nearest the centre of output pixel i's block."""
    return min(int((i + 0.5) * src_len / out_len), src_len - 1)


def _sample_blocks(img, out_w, out_h, palette):
    """Copy the centre source pixel of each block into an out_w x out_h image."""
    src = img.load()
    w, h = img.size
    out = Image.new("RGBA", (out_w, out_h), (0, 0, 0, 0))
    dst = out.load()
    xs = [_centre_index(w, out_w, i) for i in range(out_w)]
    ys = [_centre_index(h, out_h, i) for i in range(out_h)]
    for y in range(out_h):
        sy = ys[y]
        for x in range(out_w):
            dst[x, y] = src[xs[x], sy]
    if palette is not None:
        out = lock_palette(out, palette)
    return out


def downscale(img, block=None, height=None, palette=None):
    """Nearest-neighbour block downscale of an RGBA image, alpha kept as-is.

    Exactly one of block (the native size of the square output, e.g. a 32 px
    tile) or height (the native height; width follows the source aspect, e.g. a
    48 px person) is given. Each output pixel takes the source pixel at the
    centre of its block, so no new colours are made. When palette is a list of
    (r, g, b), the result is snapped to it with lock_palette; when it is None
    the lock is skipped.
    """
    img = img.convert("RGBA")
    if (block is None) == (height is None):
        raise ValueError("give exactly one of block or height")
    w, h = img.size
    if block is not None:
        if block < 1:
            raise ValueError("block must be 1 or more")
        out_w = out_h = block
    else:
        if height < 1:
            raise ValueError("height must be 1 or more")
        out_h = height
        out_w = max(1, round(w * height / h))
    return _sample_blocks(img, out_w, out_h, palette)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Downscale art to native pixels by nearest-neighbour block sampling.")
    ap.add_argument("input", metavar="IN", help="source picture")
    ap.add_argument("output", metavar="OUT", help="output .png or .webp")
    ap.add_argument("--block", type=int,
                    help="native size of the square output in art pixels (a tile is 32)")
    ap.add_argument("--height", type=int,
                    help="native height in art pixels; width follows the source aspect (a person is 48)")
    ap.add_argument("--palette", metavar="PALETTE",
                    help="palette file to snap colours to; without it the lock is skipped")
    a = ap.parse_args(argv)

    if (a.block is None) == (a.height is None):
        fail("give exactly one of --block or --height")
    suffix = os.path.splitext(a.output)[1].lower()
    if suffix not in (".png", ".webp"):
        fail("OUT must end in .png or .webp")

    palette = load_palette(a.palette) if a.palette else None
    try:
        out = downscale(open_image(a.input), block=a.block, height=a.height, palette=palette)
    except ValueError as exc:
        fail(str(exc))
    out.save(a.output)
    print(f"wrote {a.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
