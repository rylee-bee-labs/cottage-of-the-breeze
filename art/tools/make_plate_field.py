#!/usr/bin/env python3
"""make_plate_field.py: the soft parchment field inside a framed ornament.

  make_plate_field.py INPUT OUTPUT [--inset L,T,R,B] [--feather FRACTION]
                                  [--flatten FRACTION]

Some skin parts are not nine-slices. The player lays them across a whole box
and stretches the picture to fit it (`plate()` in
`vefr/web/player/parts/540-the-skin.js`): the message strip gets `.toasts`,
the bag rows get `.equip-row`. Neither box has a shape a picture can assume
- `.toasts` is `width: min(210px, 36%)` and as tall as the messages make it,
and an equip row is a list line about 510x32 - so every pixel of the picture
is scaled by a different, and often large, factor in each direction.

A framed ornament cannot survive that. A square slot drawn at 64x64 and
stretched across a 510x32 row turns its bevelled corners and its corner
highlight into long horizontal bars of glare; a ribbon drawn at 192x48 and
stretched over a 210x153 stack drags its swallow tails out past the panel.
Both read as a rendering fault, which is worse than the plain player.

What survives stretching is a field with nothing in it but colour, because a
soft gradient scaled by ten in one direction is still a soft gradient. So
this tool takes the parchment field drawn *inside* an ornament's frame -
the one part of Rylee's pick that is plain - crops to it, feathers its alpha
so the picture has no edge to give away, and with `--flatten` smooths the
mottling out of the colour so that scaling the field by eleven in one
direction cannot turn a faint mark into a band of glare. It is a crop and two
blurs: the colours are the sheet's own, nothing is redrawn, and the frame
that was cut away is still kept beside it in `skin-source/`, so the ornament
can be put back if the engine ever gives it a box of its own shape.

Running it twice on the same input gives identical bytes: a crop, a Gaussian
blur and a fixed save. A `.webp` output is saved with `lossless=True` on
purpose - Pillow's default for WebP is lossy, which would put a second,
unintended quantisation between the drawing and the part - and a `.png` output
is lossless whatever the settings, so in both cases the file round-trips the
field exactly. A missing input, an input with no alpha channel, an OUT that is
not .png or .webp, an inset outside 0..0.5, a feather outside 0..0.25 or a
flatten outside 0..1 is a plain one-line message with exit 2. Needs Pillow:
  uv run --offline --with pillow art/tools/make_plate_field.py IN.webp OUT.webp
"""
import argparse
import os
import sys
from PIL import Image, ImageFilter

# How far inside the frame the plain field sits, per part, as a fraction of
# each side. Measured off the built parts, row by row: the slot's parchment
# runs from row 9 to row 54 of 64 and the ribbon's from row 13 to row 30 of 48
# and column 14 to column 158 of 192, so both clear their frame by a few
# pixels of parchment rather than catching a pixel of wood.
INSETS = {
    "slot": (0.14, 0.14, 0.14, 0.14),
    "banner": (0.09, 0.27, 0.17, 0.36),
}
# The feather as a fraction of the field's short side. Big enough that the
# edge cannot be seen, small enough that the flat middle of the wash survives.
DEFAULT_FEATHER = 0.09
MAX_INSET = 0.5         # a field must keep a pixel of the middle
MAX_FEATHER = 0.25      # past this the field has no flat middle left
MAX_FLATTEN = 1.0       # past this there is nothing left but the average


def fail(message):
    """A plain one-line problem, exit 2, with no traceback."""
    print(message, file=sys.stderr)
    raise SystemExit(2)


def parse_inset(spec, default):
    """Parse 'L,T,R,B' fractions, or take the default for this part."""
    if spec is None:
        return default
    bits = spec.split(",")
    if len(bits) != 4:
        fail(f"--inset wants four fractions like 0.17,0.17,0.17,0.17, got {spec!r}")
    try:
        inset = tuple(float(b) for b in bits)
    except ValueError:
        fail(f"--inset wants four numbers, got {spec!r}")
    if any(not 0.0 <= v <= MAX_INSET for v in inset):
        fail(f"--inset wants 0..{MAX_INSET} on every side, got {spec!r}")
    return inset


def ramp(length, feather_px):
    """A list of alpha values: 255 through the middle, fading to 0 at each end.

    A blur cannot do this job. The field is cropped from *inside* an opaque
    ornament, so its alpha is 255 from edge to edge and blurring it changes
    nothing; the fade has to be drawn, and a straight line from nothing to
    full is the one edge that survives being scaled by ten.
    """
    f = min(int(round(feather_px)), length // 2)
    if f < 1:
        return [255] * length
    head = [round(255 * i / f) for i in range(f)]
    return head + [255] * (length - 2 * f) + head[::-1]


def field(im, inset, feather, flatten):
    """Return the RGBA parchment field inside `im`'s frame, softly edged.

    The crop is the plain middle of the picture; its colour is smoothed by
    `flatten` and its edges faded by `feather`, both as a fraction of the
    crop's short side, so the picture has no detail to smear and no edge to
    give away.
    """
    w, h = im.size
    box = (round(w * inset[0]), round(h * inset[1]),
           round(w * (1.0 - inset[2])), round(h * (1.0 - inset[3])))
    if box[2] <= box[0] or box[3] <= box[1]:
        fail(f"an inset of {inset} leaves nothing of a {w}x{h} picture")
    inner = im.crop(box)
    cw, ch = inner.size
    short = min(cw, ch)
    if inner.getchannel("A").getextrema()[1] == 0:
        fail(f"an inset of {inset} lands on nothing but transparent pixels of a "
             f"{w}x{h} picture; the field is not inside it")

    out = inner
    if flatten > 0.0:
        rgb = inner.convert("RGB").filter(ImageFilter.GaussianBlur(flatten * short))
        out = Image.merge("RGBA", (*rgb.split(), inner.getchannel("A")))

    edge = feather * short
    row = ramp(cw, edge)
    col = ramp(ch, edge)
    mask = [min(a, b) for b in col for a in row]
    alpha = out.getchannel("A").tobytes()
    out.putalpha(Image.frombytes("L", (cw, ch),
                                 bytes(round(a * m / 255) for a, m in zip(alpha, mask))))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True, description=__doc__.splitlines()[0])
    ap.add_argument("input", metavar="INPUT",
                    help="the built ornament, as RGBA .png or .webp")
    ap.add_argument("output", metavar="OUT", help="where to write the field")
    ap.add_argument("--inset", default=None,
                    help="L,T,R,B fractions of the picture to keep (default: the part's own)")
    ap.add_argument("--feather", type=float, default=DEFAULT_FEATHER,
                    help=f"edge feather as a fraction of the short side (default {DEFAULT_FEATHER})")
    ap.add_argument("--flatten", type=float, default=0.0,
                    help="smooth the crop's colour by this fraction of its short "
                         f"side before feathering (default 0, off)")
    a = ap.parse_args(argv)

    if os.path.splitext(a.output)[1].lower() not in (".png", ".webp"):
        fail(f"OUT must end in .png or .webp, got {a.output!r}")
    if not 0.0 <= a.feather <= MAX_FEATHER:
        fail(f"--feather must be between 0 and {MAX_FEATHER}, got {a.feather!r}")
    if not 0.0 <= a.flatten <= MAX_FLATTEN:
        fail(f"--flatten must be between 0 and {MAX_FLATTEN}, got {a.flatten!r}")
    name = os.path.splitext(os.path.basename(a.input))[0]
    inset = parse_inset(a.inset, INSETS.get(name, (0.2, 0.2, 0.2, 0.2)))
    try:
        with Image.open(a.input) as opened:
            if opened.mode != "RGBA":
                fail(f"{a.input} must be RGBA (it keeps the ornament's transparent "
                     f"surround), got {opened.mode}")
            out = field(opened, inset, a.feather, a.flatten)
    except OSError:
        fail(f"cannot read {a.input!r}")

    out.save(a.output, **({"lossless": True} if a.output.lower().endswith(".webp") else {}))
    print(f"wrote {a.output} ({out.size[0]}x{out.size[1]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())