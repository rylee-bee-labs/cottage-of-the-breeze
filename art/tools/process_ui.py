#!/usr/bin/env python3
"""process_ui.py: turn a drawn UI picture into a clean, symmetric nine-slice.

  process_ui.py box IN OUT --size WxH --slice N [--fill TEXTURE.png]
                 [--fill-colour #RRGGBB] [--trim|--no-trim] [--tolerance 28]
  process_ui.py strip IN OUT --size WxH [--tolerance 28]

A generated panel is close to a nine-slice but never exact: one border comes out
wider, the corners do not match, an edge has a stud in it. CSS border-image wants a
perfectly symmetric picture, so `box` does not trust the drawing: it clears the flat
or drawn-checkerboard background (process_sprites.remove_background), trims to the
content box (--trim, on by default; --no-trim keeps the whole picture), resizes to
exactly WxH, then rebuilds the border from ONE corner and ONE band of each edge,
mirrored, so the result is symmetric by construction. The inside is filled with
--fill TEXTURE.png (tiled, its alpha kept), with --fill-colour (opaque), or by
default with the average colour of the picture's centre patch; the fill never crosses
the border, and transparent (rounded) corners stay transparent. It prints the file
and the slice line for the CSS:

  wrote out/panel.webp
  border-image-slice: 32

`strip` clears the background, trims to the content box, scales the piece to fit
inside WxH without changing its aspect ratio (never upscaled more than 2x) and
centres it on a fully transparent canvas. Needs Pillow:
  uv run --with pillow art/tools/process_ui.py ...
"""
import argparse
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from process_sprites import fail, open_image, remove_background

BAND = 16               # one band taken from the middle of an edge
PATCH = 16              # centre patch that gives the default fill colour
DEFAULT_TOLERANCE = 28  # the same colour match process_sprites.py uses
MAX_UPSCALE = 2.0       # never enlarge a piece more than 2x


def parse_size(spec):
    """Parse a WxH size like 320x180, or fail plainly."""
    bits = spec.lower().split("x")
    if len(bits) != 2:
        fail(f"--size wants WxH like 320x180, got {spec!r}")
    try:
        width, height = int(bits[0]), int(bits[1])
    except ValueError:
        fail(f"--size wants whole numbers like 320x180, got {spec!r}")
    if width < 1 or height < 1:
        fail(f"--size needs positive numbers, got {spec!r}")
    return width, height


def parse_colour(spec):
    """Parse #RRGGBB into an opaque RGBA colour, or fail plainly."""
    if len(spec) != 7 or spec[0] != "#":
        fail(f"--fill-colour wants #RRGGBB like #3a2f28, got {spec!r}")
    try:
        r, g, b = (int(spec[i:i + 2], 16) for i in (1, 3, 5))
    except ValueError:
        fail(f"--fill-colour wants #RRGGBB like #3a2f28, got {spec!r}")
    return (r, g, b, 255)


def average_colour(img):
    """The average colour of the centred patch of the picture, opaque."""
    w, h = img.size
    side = min(PATCH, w, h)
    x0, y0 = (w - side) // 2, (h - side) // 2
    patch = img.crop((x0, y0, x0 + side, y0 + side))
    px = patch.load()
    count = side * side
    r = sum(px[x, y][0] for x in range(side) for y in range(side)) // count
    g = sum(px[x, y][1] for x in range(side) for y in range(side)) // count
    b = sum(px[x, y][2] for x in range(side) for y in range(side)) // count
    return (r, g, b, 255)


def tile_edge(strip, length, anchor):
    """Tile the strip from the corner of an edge to its centre and mirror it across."""
    band = Image.new("RGBA", (length, strip.height), (0, 0, 0, 0))
    half = (length + 1) // 2
    x = anchor
    while x < half:
        tile = strip
        if x + strip.width > half:
            tile = strip.crop((0, 0, half - x, strip.height))
        band.paste(tile, (x, 0))
        x += strip.width
    near = band.crop((0, 0, half, strip.height))
    band.paste(near.transpose(Image.FLIP_LEFT_RIGHT), (length - half, 0))
    return band


def inside_fill(cut, width, height, slice_size, fill, fill_colour):
    """Build the inside picture: a tiled texture, a flat colour, or the centre average."""
    inner_w = width - 2 * slice_size
    inner_h = height - 2 * slice_size
    if fill_colour is not None:
        return Image.new("RGBA", (inner_w, inner_h), fill_colour)
    if fill is not None:
        tex = open_image(fill)
        tiled = Image.new("RGBA", (inner_w, inner_h), (0, 0, 0, 0))
        tw, th = tex.size
        y = 0
        while y < inner_h:
            x = 0
            while x < inner_w:
                tiled.paste(tex, (x, y))  # pasted raw, so the texture keeps its alpha
                x += tw
            y += th
        return tiled
    return Image.new("RGBA", (inner_w, inner_h), average_colour(cut))


def process_box(img, width, height, slice_size, fill, fill_colour, tolerance, trim):
    """Clear, trim, resize and rebuild the border from one corner and two bands."""
    cut = remove_background(img, tolerance)
    if trim:
        bbox = cut.getchannel("A").getbbox()
        if bbox is None:
            fail("no content to cut out (every pixel is transparent)")
        cut = cut.crop(bbox)
    cut = cut.resize((width, height), Image.LANCZOS)

    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    # One band from the middle of the top edge: tiled to the centre, then mirrored.
    x0 = (width - BAND) // 2
    top_strip = cut.crop((x0, 0, x0 + BAND, slice_size))
    top_band = tile_edge(top_strip, width, slice_size)
    canvas.paste(top_band, (0, 0))
    canvas.paste(top_band.transpose(Image.FLIP_TOP_BOTTOM), (0, height - slice_size))

    # One band from the middle of the left edge, built the same way on its side.
    y0 = (height - BAND) // 2
    left_strip = cut.crop((0, y0, slice_size, y0 + BAND))
    left_band = tile_edge(left_strip.transpose(Image.TRANSPOSE), height, slice_size)
    left_band = left_band.transpose(Image.TRANSPOSE)
    canvas.paste(left_band, (0, 0))
    canvas.paste(left_band.transpose(Image.FLIP_LEFT_RIGHT), (width - slice_size, 0))

    # The inside, clipped to the inside rectangle exactly.
    inside = inside_fill(cut, width, height, slice_size, fill, fill_colour)
    canvas.paste(inside, (slice_size, slice_size))

    # One corner mirrored into the other three, written last over the band ends.
    corner = cut.crop((0, 0, slice_size, slice_size))
    canvas.paste(corner, (0, 0))
    canvas.paste(corner.transpose(Image.FLIP_LEFT_RIGHT), (width - slice_size, 0))
    canvas.paste(corner.transpose(Image.FLIP_TOP_BOTTOM), (0, height - slice_size))
    canvas.paste(corner.transpose(Image.ROTATE_180),
                 (width - slice_size, height - slice_size))
    return canvas


def process_strip(img, width, height, tolerance):
    """Clear, trim, fit inside width x height and centre on a transparent canvas."""
    cut = remove_background(img, tolerance)
    bbox = cut.getchannel("A").getbbox()
    if bbox is None:
        fail("no content to cut out (every pixel is transparent)")
    cut = cut.crop(bbox)
    w, h = cut.size
    scale = min(width / w, height / h)
    if scale > MAX_UPSCALE:
        scale = MAX_UPSCALE
    new_w = max(1, min(width, round(w * scale)))
    new_h = max(1, min(height, round(h * scale)))
    cut = cut.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    canvas.paste(cut, ((width - new_w) // 2, (height - new_h) // 2))
    return canvas


def main(argv=None):
    """Run the box or strip command line, one picture in, one picture out."""
    ap = argparse.ArgumentParser(
        description="Turn a drawn UI picture into a symmetric nine-slice panel.")
    sub = ap.add_subparsers(dest="mode", required=True)

    bx = sub.add_parser("box", help="rebuild a panel as a symmetric nine-slice")
    bx.add_argument("input", metavar="IN", help="source picture")
    bx.add_argument("output", metavar="OUT", help="output .png or .webp")
    bx.add_argument("--size", metavar="WxH", required=True, help="panel size, like 320x180")
    bx.add_argument("--slice", metavar="N", type=int, required=True,
                    help="border width in pixels")
    fills = bx.add_mutually_exclusive_group()
    fills.add_argument("--fill", metavar="TEXTURE.png", help="texture tiled inside")
    fills.add_argument("--fill-colour", metavar="#RRGGBB", dest="fill_colour",
                       help="flat colour inside, like #3a2f28")
    bx.add_argument("--trim", action=argparse.BooleanOptionalAction, default=True,
                    help="trim to the content box (default; --no-trim keeps the whole picture)")
    bx.add_argument("--tolerance", type=int, default=DEFAULT_TOLERANCE,
                    help=f"per-channel colour match (default {DEFAULT_TOLERANCE})")

    st = sub.add_parser("strip", help="fit an ornament inside the size")
    st.add_argument("input", metavar="IN", help="source picture")
    st.add_argument("output", metavar="OUT", help="output .png or .webp")
    st.add_argument("--size", metavar="WxH", required=True, help="canvas size, like 320x32")
    st.add_argument("--tolerance", type=int, default=DEFAULT_TOLERANCE,
                    help=f"per-channel colour match (default {DEFAULT_TOLERANCE})")

    a = ap.parse_args(argv)

    width, height = parse_size(a.size)
    suffix = os.path.splitext(a.output)[1].lower()
    if suffix not in (".png", ".webp"):
        fail("OUT must end in .png or .webp")

    if a.mode == "strip":
        out = process_strip(open_image(a.input), width, height, a.tolerance)
        out.save(a.output)
        print(f"wrote {a.output}")
        return 0

    if a.slice < 1:
        fail("--slice must be 1 or more")
    if 2 * a.slice >= width or 2 * a.slice >= height:
        fail(f"--slice {a.slice} does not fit a {width}x{height} box: 2 * slice must be "
             f"smaller than size in both directions, so this box is impossible")
    fill_colour = None
    if a.fill_colour is not None:
        fill_colour = parse_colour(a.fill_colour)
    out = process_box(open_image(a.input), width, height, a.slice, a.fill, fill_colour,
                      a.tolerance, a.trim)
    out.save(a.output)
    print(f"wrote {a.output}")
    print(f"border-image-slice: {a.slice}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
