#!/usr/bin/env python3
"""make_selected_tab.py: the "selected" chip for a tab, from the tab chip itself.

  make_selected_tab.py INPUT OUTPUT [--amount 0.34]

A tab strip needs two chips: the tab at rest, and the same tab when it is the one
you are looking at. Rylee's round-two pick for the selected tab
(`ui-soft/missing/tab-selected/tab-selected_v3.png`) asked for "the same tab but
selected: lighter honey wood, parchment face", and the drawing that came back is
a large parchment *panel* with a tab bump along its top edge - the content panel
that sits under a chosen tab, not the chip itself. Built into the tab slot it is
squashed into a 96x40 box and mirrored, and it reads as a pale stepped blob with
its rim sliced away, next to a perfectly good `tab.webp`.

So the chip is made the way the prompt asked for it: from the tab chip Rylee did
pick (`tab_v3`), lightened toward the honey cream that `tab-selected_v3` is drawn
in, which is the one thing that pick is good for. Every pixel keeps its alpha, so
the silhouette is unchanged and the two chips are the same shape - which is what
the player sees when they move between tabs.

Blending toward a light warm cream keeps the drawn outlines readable (blending
toward white at this strength keeps them too) and reads as "lighter honey wood"
beside the at-rest chip rather than as a different piece. Nothing is redrawn,
reshaped or resampled: the output is the input's pixels, moved one step along the
line to the cream. A `.webp` output is saved with `lossless=True` on purpose -
Pillow's default for WebP is lossy, which would put a second, unintended
quantisation between the drawing and the part - and a `.png` output is lossless
whatever the settings, so in both cases the file round-trips the blend exactly.

Running it twice on the same input gives identical bytes: the blend is a fixed
per-pixel arithmetic step and there is no randomness or timestamp. A missing
input, an input with no alpha channel, or an OUT that is not .png or .webp is a
plain one-line message with exit 2. Needs Pillow:
  uv run --offline --with pillow art/tools/make_selected_tab.py IN.webp OUT.webp
"""
import argparse
import os
import sys
from PIL import Image

# The cream the selected chip is drawn toward: warm parchment, not white, so the
# chip reads as lighter honey wood rather than as a bleached copy. Chosen against
# tab-selected_v3.png, whose face is exactly this pale.
CREAM = (246, 231, 201)
DEFAULT_AMOUNT = 0.34    # 0.22 barely differs from the at-rest chip; 0.46 washes out


def fail(message):
    """A plain one-line problem, exit 2, with no traceback."""
    print(message, file=sys.stderr)
    raise SystemExit(2)


def lighten(im, amount):
    """Return a copy of RGBA `im` with every colour one step `amount` toward CREAM.

    Alpha is carried across untouched, so the shape and every transparent pixel
    come out exactly as they went in; only the colour of the opaque ones moves.
    """
    out = Image.new("RGBA", im.size)
    src, dst = im.load(), out.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = src[x, y]
            dst[x, y] = (
                round(r + (CREAM[0] - r) * amount),
                round(g + (CREAM[1] - g) * amount),
                round(b + (CREAM[2] - b) * amount),
                a,
            )
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True, description=__doc__.splitlines()[0])
    ap.add_argument("input", metavar="INPUT", help="the tab chip at rest, as RGBA .png or .webp")
    ap.add_argument("output", metavar="OUT", help="where to write the selected chip")
    ap.add_argument("--amount", type=float, default=DEFAULT_AMOUNT,
                    help=f"how far toward the cream to move each colour (default {DEFAULT_AMOUNT})")
    a = ap.parse_args(argv)

    if os.path.splitext(a.output)[1].lower() not in (".png", ".webp"):
        fail(f"OUT must end in .png or .webp, got {a.output!r}")
    if not 0.0 <= a.amount <= 1.0:
        fail(f"--amount must be between 0 and 1, got {a.amount!r}")
    try:
        with Image.open(a.input) as opened:
            if opened.mode != "RGBA":
                fail(f"{a.input} must be RGBA (it keeps the chip's transparent surround), "
                     f"got {opened.mode}")
            out = lighten(opened, a.amount)
    except OSError:
        fail(f"cannot read {a.input!r}")

    out.save(a.output, **({"lossless": True} if a.output.lower().endswith(".webp") else {}))
    print(f"wrote {a.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())