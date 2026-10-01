#!/usr/bin/env python3
"""process_sprites.py: cut a sprite out of a picture and set it on the game's canvas.

  process_sprites.py IN.png OUT.png [--size 128] [--tolerance 28]
  process_sprites.py --grid COLSxROWS SHEET.png OUTDIR PREFIX [--size 128]
                     [--names down,left,right,up]

Background removal floods in from the four corners, so only background that touches an
edge goes away: a hole inside the subject stays opaque. The cut-out is trimmed, scaled to
fit inside SIZE x SIZE (never upscaled more than 2x) and pasted bottom-aligned on a
transparent canvas, feet on the floor. --grid cuts a COLSxROWS sheet into
cells (an uneven size is cut on rounded edges, with a note, because generated sheets are never exact) and writes PREFIX_<row>_<col>.png for each, row names from --names (top row first),
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


def _near(c1, c2, tolerance):
    return (abs(c1[0] - c2[0]) <= tolerance and abs(c1[1] - c2[1]) <= tolerance
            and abs(c1[2] - c2[2]) <= tolerance)


def _is_neutral(c):
    """A grey or white pixel (the colours a drawn 'transparent' checkerboard uses)."""
    return max(c[:3]) - min(c[:3]) <= 14


def _checker_partner(px, w, h, corner, tolerance):
    """The second colour of a drawn checkerboard that starts at this corner, or None.

    Some generators draw the grey-and-white 'transparent' pattern as real pixels. Walk along the edge row
    from the corner: if two neutral colours alternate in at least four runs of three or more pixels, the
    other colour is a background colour too. Plain backgrounds, and subjects at the edge, return None.
    """
    x0, y0 = corner
    step = 1 if x0 == 0 else -1
    base = px[x0, y0]
    if base[3] < 128 or not _is_neutral(base):
        return None
    other, runs, run_len, current = None, 0, 0, "a"
    for i in range(min(w, 160)):
        c = px[x0 + step * i, y0]
        if c[3] < 128:
            return None
        kind = "a" if _near(c, base, tolerance) else ("b" if _is_neutral(c) and (other is None or _near(c, other, tolerance)) else "x")
        if kind == "x":
            break
        if kind == "b" and other is None:
            other = c
        if kind == current:
            run_len += 1
        else:
            if run_len >= 3:
                runs += 1
            current, run_len = kind, 1
    if run_len >= 3:
        runs += 1
    return other if other is not None and runs >= 4 else None


def remove_background(img, tolerance):
    """Flood-fill in from the four corners, matching the corner colour per channel.

    Only pixels reached from a corner are cleared, so an enclosed hole of the background
    colour stays opaque. If the corners are already transparent, keep the existing alpha.
    A drawn checkerboard (two neutral colours alternating) is cleared as one background.
    """
    img = img.convert("RGBA")
    w, h = img.size
    px = img.load()
    corners = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    if all(px[x, y][3] < 128 for x, y in corners):
        return img  # already a cut-out
    bgs = []
    for x, y in corners:
        if px[x, y][3] >= 128:
            bgs.append(px[x, y][:3])
            partner = _checker_partner(px, w, h, (x, y), tolerance)
            if partner is not None:
                bgs.append(partner[:3])
    seen = bytearray(w * h)
    queue = deque()
    for x, y in corners:
        if px[x, y][3] >= 128 and not seen[y * w + x]:
            seen[y * w + x] = 1
            queue.append((x, y))
    while queue:
        x, y = queue.popleft()
        r, g, b, _ = px[x, y]
        px[x, y] = (r, g, b, 0)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                n = px[nx, ny]
                if n[3] >= 128 and any(_near(n, c, tolerance) for c in bgs):
                    seen[ny * w + nx] = 1
                    queue.append((nx, ny))
    return img


def process_one(img, size, tolerance, holes=False):
    """One sprite: background off, trimmed, fitted inside size x size, feet on the floor."""
    cut = remove_background(img, tolerance)
    if holes:
        src = img.convert("RGBA")
        sw, sh = src.size
        sp = src.load()
        bg = sp[0, 0][:3]
        cp = cut.load()
        for y in range(sh):
            for x in range(sw):
                r, g, b, a = sp[x, y]
                if a >= 128 and abs(r - bg[0]) <= tolerance and abs(g - bg[1]) <= tolerance and abs(b - bg[2]) <= tolerance:
                    cp[x, y] = (r, g, b, 0)
    bbox = cut.getchannel("A").getbbox()
    if bbox is None:
        fail("no content to cut out (every pixel is transparent)")
    cut = cut.crop(bbox)
    w, h = cut.size
    # A small margin (size / 64, at least 1 px) on the top and both sides, so a figure never touches
    # the edge of its canvas; the bottom is left open because the feet stand on it.
    margin = max(1, size // 64)
    room_w, room_h = size - 2 * margin, size - margin
    scale = min(room_w / w, room_h / h)
    if scale > 2.0:
        scale = 2.0  # never upscale more than 2x
    new_w = max(1, min(room_w, round(w * scale)))
    new_h = max(1, min(room_h, round(h * scale)))
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
    ap.add_argument("--clear-holes", action="store_true", help="also clear background-coloured holes inside the subject (a ring, a handle)")
    ap.add_argument("args", nargs="*")
    a = ap.parse_args(argv)

    if a.size < 1:
        fail("--size must be 1 or more")

    if a.grid is None:
        if len(a.args) != 2:
            ap.error("single mode needs IN.png OUT.png")
        in_path, out_path = a.args
        out = process_one(open_image(in_path), a.size, a.tolerance, a.clear_holes)
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
    if w < cols or h < rows:
        fail(f"sheet {w}x{h} is smaller than a {cols}x{rows} grid")
    if w % cols or h % rows:
        print(f"note: sheet {w}x{h} does not divide evenly by {cols}x{rows}; cells are cut on rounded edges "
              f"(each cell is within 1 px of {w / cols:.1f}x{h / rows:.1f})", file=sys.stderr)
    os.makedirs(outdir, exist_ok=True)
    xs = [round(i * w / cols) for i in range(cols + 1)]
    ys = [round(i * h / rows) for i in range(rows + 1)]
    for r in range(rows):
        for c in range(cols):
            cell = sheet.crop((xs[c], ys[r], xs[c + 1], ys[r + 1]))
            out = process_one(cell, a.size, a.tolerance)
            path = os.path.join(outdir, f"{prefix}_{names[r]}_{c + 1}.png")
            out.save(path)
            print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
