#!/usr/bin/env python3
"""split_sheet.py: cut one batch sheet of interface pieces into single pictures.

  split_sheet.py SHEET.png OUTDIR [--names panel,button,...] [--min-area 64]
                 [--neutral 14] [--margin 0]

A batch sheet is one or more pieces standing on a flat light-grey ground (the
soft-wood sheets in art/source/round18/ui-soft/, cut the way round 10 kept its
skin-source pictures). The pieces are found by connected components: the ground
and its soft drop shadows are neutral grey, so any pixel more coloured than
--neutral is a piece. Each piece is cut out on its own, tight to its box, with
the grey ground and any shadow keyed out from around it, and written to OUTDIR
as its own .png - named from --names in reading order (left to right, then top
to bottom), or piece-1.png, piece-2.png, ... A picture with alpha keeps the
piece's alpha; a piece that comes out fully opaque is plain RGB. Stray specks
of a few pixels are dropped. Needs Pillow:
  uv run --offline --with pillow art/tools/split_sheet.py --help
"""
import argparse
import os
import sys
from array import array
from collections import deque

from PIL import Image, ImageChops

MIN_AREA = 64       # pieces smaller than this are stray specks, not pictures
NEUTRAL = 14        # max-minus-min channel: this grey or less is the ground
ALPHA_OPAQUE = 8    # a pixel fainter than this is not part of a piece


def fail(message):
    """A plain one-line problem, exit 2, with no traceback."""
    print(message, file=sys.stderr)
    raise SystemExit(2)


def open_sheet(path):
    """Open a sheet as RGBA, plus whether the picture had an alpha channel of its own."""
    try:
        im = Image.open(path)
        has_alpha = (im.mode in ("RGBA", "LA", "PA")
                     or (im.mode == "P" and "transparency" in im.info))
        return im.convert("RGBA"), has_alpha
    except (OSError, ValueError) as exc:
        fail(f"cannot read {path}: {exc}")


def piece_mask(sheet, neutral):
    """One byte per pixel: 255 where the pixel looks like a piece, 0 for the ground.

    A piece is coloured (warm wood, saturated paint); the ground and its soft
    drop shadows are neutral grey, however light, dark or uneven, so the test is
    the channel spread, not the brightness.
    """
    r, g, b, a = sheet.split()
    high = ImageChops.lighter(ImageChops.lighter(r, g), b)
    low = ImageChops.darker(ImageChops.darker(r, g), b)
    coloured = ImageChops.subtract(high, low).point(
        lambda v: 255 if v > neutral else 0)
    opaque = a.point(lambda v: 255 if v >= ALPHA_OPAQUE else 0)
    return bytearray(ImageChops.multiply(coloured, opaque).tobytes())


def find_pieces(mask, w, h, min_area):
    """Connected patches of piece pixels, in reading order (top row, then left to right).

    Returns (pieces, owner): pieces is a list of (left, top, right, bottom, tag)
    boxes; owner holds one int per pixel, the tag of its patch or -1 for the
    ground. Patches smaller than min_area are left out of pieces but still
    tagged, so a speck inside a piece's box can be cleared away with the ground.
    """
    owner = array("i", [-1]) * (w * h)
    found = []
    for start in range(w * h):
        if not mask[start] or owner[start] != -1:
            continue
        tag = len(found)
        owner[start] = tag
        queue = deque([start])
        count = 0
        left = right = start % w
        top = bottom = start // w
        while queue:
            i = queue.popleft()
            count += 1
            x = i % w
            y = i // w
            if x < left:
                left = x
            elif x > right:
                right = x
            if y < top:
                top = y
            elif y > bottom:
                bottom = y
            for dy in (-1, 0, 1):
                ny = y + dy
                if ny < 0 or ny >= h:
                    continue
                for dx in (-1, 0, 1):
                    nx = x + dx
                    if (dx or dy) and 0 <= nx < w:
                        j = ny * w + nx
                        if mask[j] and owner[j] == -1:
                            owner[j] = tag
                            queue.append(j)
        found.append(((left, top, right + 1, bottom + 1), count))
    pieces = [(box[0], box[1], box[2], box[3], tag)
              for tag, (box, count) in enumerate(found) if count >= min_area]
    pieces.sort(key=lambda piece: (piece[1], piece[0]))
    return pieces, owner


def cut_piece(sheet, owner, w, h, box, tag, margin, keep_alpha):
    """One piece, cut tight to its box (plus margin): the ground and any shadow
    that reaches the border of the crop is cleared to transparency; an enclosed
    neutral patch (a grey button face inside a coloured border) stays; the
    piece's own alpha is kept. Fully opaque crops come out as plain RGB.
    """
    left = max(0, box[0] - margin)
    top = max(0, box[1] - margin)
    right = min(w, box[2] + margin)
    bottom = min(h, box[3] + margin)
    cw, ch = right - left, bottom - top
    crop = sheet.crop((left, top, right, bottom))

    clear = bytearray(cw * ch)
    queue = deque()

    def mark_ground(i):
        """True when this crop pixel is ground the flood can start from."""
        if owner[(top + i // cw) * w + left + i % cw] != -1:
            return False
        if clear[i]:
            return False
        clear[i] = 1
        queue.append(i)
        return True

    for i in range(cw):                 # the top and bottom rows
        mark_ground(i)
        mark_ground((ch - 1) * cw + i)
    for y in range(ch):                 # the left and right columns
        mark_ground(y * cw)
        mark_ground(y * cw + cw - 1)
    while queue:                        # flood out through the ground
        i = queue.popleft()
        x, y = i % cw, i // cw
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < cw and 0 <= ny < ch:
                mark_ground(ny * cw + nx)

    for y in range(ch):                 # another patch's pixels (a speck) go too
        base = (top + y) * w + left
        for x in range(cw):
            o = owner[base + x]
            if o != -1 and o != tag:
                clear[y * cw + x] = 1

    alpha = bytearray(crop.getchannel("A").tobytes())
    for i, c in enumerate(clear):
        if c:
            alpha[i] = 0
    crop.putalpha(Image.frombytes("L", (cw, ch), bytes(alpha)))
    if keep_alpha or any(v != 255 for v in alpha):
        return crop
    return crop.convert("RGB")


def cut_sheet(sheet_path, outdir, names=None, min_area=MIN_AREA,
              neutral=NEUTRAL, margin=0):
    """Split one sheet into its pieces under outdir; return the paths written."""
    sheet, keep_alpha = open_sheet(sheet_path)
    w, h = sheet.size
    mask = piece_mask(sheet, neutral)
    pieces, owner = find_pieces(mask, w, h, min_area)
    if not pieces:
        fail(f"no pieces found in {sheet_path}")
    if names is None:
        names = [f"piece-{i + 1}" for i in range(len(pieces))]
    elif len(names) != len(pieces):
        fail(f"--names has {len(names)} entries but the sheet has {len(pieces)} pieces")
    try:
        os.makedirs(outdir, exist_ok=True)
    except OSError as exc:
        fail(f"cannot make {outdir}: {exc}")

    written = []
    for name, piece in zip(names, pieces):
        left, top, right, bottom, tag = piece
        out = cut_piece(sheet, owner, w, h, (left, top, right, bottom),
                        tag, margin, keep_alpha)
        path = os.path.join(outdir, f"{name}.png")
        out.save(path)
        written.append(path)
    return written


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Cut one batch sheet of interface pieces into single pictures.")
    ap.add_argument("sheet", metavar="SHEET",
                    help="the batch sheet: one or more pieces on a light grey ground")
    ap.add_argument("outdir", metavar="OUTDIR",
                    help="directory for the cut-out pictures (made if needed)")
    ap.add_argument("--names", metavar="A,B,C",
                    help="comma-separated piece names in reading order "
                         "(left to right, then top to bottom); default piece-1, piece-2, ...")
    ap.add_argument("--min-area", type=int, default=MIN_AREA, metavar="N",
                    help=f"drop specks smaller than this many pixels (default {MIN_AREA})")
    ap.add_argument("--neutral", type=int, default=NEUTRAL, metavar="N",
                    help=f"how grey the ground is, max minus min channel (default {NEUTRAL}; "
                         "raise it if the ground comes back as one big piece)")
    ap.add_argument("--margin", type=int, default=0, metavar="N",
                    help=f"ground kept around each piece in pixels (default 0, cut tight)")
    a = ap.parse_args(argv)

    if a.min_area < 1:
        fail("--min-area must be 1 or more")
    if not 0 <= a.neutral <= 255:
        fail("--neutral must be between 0 and 255")
    if a.margin < 0:
        fail("--margin must be 0 or more")
    names = None
    if a.names is not None:
        names = [n.strip() for n in a.names.split(",")]

    for path in cut_sheet(a.sheet, a.outdir, names, a.min_area, a.neutral, a.margin):
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
