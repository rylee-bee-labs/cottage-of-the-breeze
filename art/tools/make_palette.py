#!/usr/bin/env python3
"""make_palette.py: build the one master GBA palette for the cottage art set.

  make_palette.py [--pack DIR] [--out FILE] [--check] [--report]

The palette is the storybook palette every shipped picture is locked to: the
exact opaque colours of the pictures that were cut with the palette lock
(`worlds/cottage-of-the-breeze/{props,tiles}` and the item and creature
sprites), plus the blue ramp added on 2026-10-14 so the pond, a lit window and
the potion glow have colours to sit on.

The ramp is the reason this tool exists rather than a hand-kept list, so the
ramp lives here as the one place it is written down.

  --check   build the palette and compare it with the committed file; exit 1 on
            any difference, and print the summary line either way
  --report  print how many colours of every shipped picture are off the
            palette, including the cast pictures that were cut without the lock

Needs Pillow. Exit 0 on success, 1 on drift or a picture that cannot be read.
"""
import argparse
import json
import sys
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[2]
DEFAULT_PACK = REPO / "worlds" / "cottage-of-the-breeze"
DEFAULT_OUT = REPO / "art" / "palette.json"

ALPHA_OPAQUE = 128  # alpha below this is transparent, so the colour is not in the picture

# The cast pictures, cut without the palette lock (see art/palette.RECORD.md).
# They are reported by --report but their colours do not enter the palette.
CAST_STEMS = (
    "hero", "cat", "keeper", "trader", "fisher", "gardener",
    "tavern-regular", "dwarf-smith",
)

# The blue ramp (2026-10-14, "Widen the palette with a blue ramp"). Ten steps
# around the dusk teal accent #3F7E84, deepest to lightest: water in shadow, the
# pond at dusk, a lit window, the potion glow. Blue is the largest channel of
# every step, so each one reads as blue against the storybook greens and
# browns rather than as one more green.
BLUE_RAMP = (
    ("#0D1A26", "deep water in shadow"),
    ("#15293C", "night water"),
    ("#1D3A55", "deep blue"),
    ("#274C6B", "blue, before the teal"),
    ("#2F6079", "blue-teal"),
    ("#3F7E84", "dusk teal, the accent"),
    ("#4A97A0", "pond surface at dusk"),
    ("#5FB0B8", "lit window, glow mid"),
    ("#86CBD1", "potion glow"),
    ("#C4E8EA", "glow core, moonlight"),
)

RAMP_SIZE = (8, 12)  # the size the decision allows the ramp to be


def hex_of(rgb):
    """(r, g, b) to '#RRGGBB'."""
    return "#%02X%02X%02X" % rgb


def rgb_of(text):
    """'#RRGGBB' to (r, g, b)."""
    text = text.lstrip("#")
    return tuple(int(text[i:i + 2], 16) for i in (0, 2, 4))


def is_blue(rgb):
    """True when blue is the largest channel of the colour."""
    r, g, b = rgb[:3]
    return b > r and b > g


def picture_colours(path):
    """The set of opaque (r, g, b) colours of one picture."""
    with Image.open(path) as im:
        rgba = im.convert("RGBA")
    return {(r, g, b) for r, g, b, a in rgba.getdata() if a >= ALPHA_OPAQUE}


def is_cast(path):
    """True for a cast picture (cut without the palette lock)."""
    stem = path.stem
    return any(stem == s or stem.startswith(s + "-") for s in CAST_STEMS)


def locked_pictures(pack):
    """The shipped pictures whose colours the palette must keep, in a stable order."""
    pictures = sorted(pack.glob("props/*.webp")) + sorted(pack.glob("tiles/*.webp"))
    pictures += [p for p in sorted(pack.glob("sprites/*.webp")) if not is_cast(p)]
    return pictures


def cast_pictures(pack):
    """The shipped cast pictures, which were cut without the palette lock."""
    return [p for p in sorted(pack.glob("sprites/*.webp")) if is_cast(p)]


def ramp_colours():
    """The blue ramp as (hex, name) pairs, checked against the decision."""
    if not RAMP_SIZE[0] <= len(BLUE_RAMP) <= RAMP_SIZE[1]:
        raise ValueError(
            "the blue ramp holds %d colours, the decision allows %d to %d"
            % (len(BLUE_RAMP), RAMP_SIZE[0], RAMP_SIZE[1]))
    seen = set()
    for text, _name in BLUE_RAMP:
        if not is_blue(rgb_of(text)):
            raise ValueError("ramp colour %s is not blue-dominant" % text)
        if text in seen:
            raise ValueError("ramp colour %s is listed twice" % text)
        seen.add(text)
    return BLUE_RAMP


def build_palette(pack=DEFAULT_PACK):
    """The palette: every locked art colour, then the blue ramp."""
    ramp = ramp_colours()
    art = set()
    for path in locked_pictures(pack):
        art |= picture_colours(path)
    colours = [hex_of(c) for c in sorted(art)]
    entries = list(colours)
    for text, name in ramp:
        entries.append({"hex": text, "name": name, "group": "blue-ramp"}
                       if text not in art else {"hex": text, "name": name})
    return {
        "name": "cottage-of-the-breeze master GBA palette",
        "notes": (
            "One palette for the shipped GBA art set: the exact colours of the "
            "pictures that were cut with the palette lock, then the blue ramp "
            "of 2026-10-14 around the dusk teal accent. Base colours are plain "
            "\"#RRGGBB\"; ramp colours carry a name. Built by "
            "art/tools/make_palette.py -- do not hand-edit."
        ),
        "colors": entries,
    }, len(art), len(art) + len(ramp)


def palette_colours(palette):
    """The palette's colours as a set of (r, g, b), file order kept by list."""
    out = []
    for entry in palette["colors"]:
        text = entry["hex"] if isinstance(entry, dict) else entry
        rgb = rgb_of(text)
        if rgb not in out:
            out.append(rgb)
    return out


def summary_line(path, art_count, total, off_palette, pictures):
    """The one line this tool is checked by."""
    return ("ok: %d colours in %s - %d from the shipped art, %d in the blue "
            "ramp, %d off-palette in %d pictures"
            % (total, path, art_count, total - art_count, off_palette, pictures))


def report(pack, colours):
    """Print how many colours of each shipped picture are off the palette."""
    print("off-palette colours by group (blue ramp included)")
    for name, paths in (("locked art", locked_pictures(pack)),
                        ("cast (cut without the lock)", cast_pictures(pack)),
                        ("title painting", sorted(pack.glob("assets/*.webp")))):
        used = set()
        for path in paths:
            try:
                used |= picture_colours(path)
            except OSError as exc:
                print("  cannot read %s: %s" % (path, exc))
                return 1
        off = len([c for c in used if c not in colours])
        print("  %-30s %4d colours used, %4d off-palette (%d pictures)"
              % (name, len(used), off, len(paths)))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--pack", type=Path, default=DEFAULT_PACK,
                    help="the pack the pictures are read from")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT,
                    help="the palette file written or checked")
    ap.add_argument("--check", action="store_true",
                    help="compare with the committed file instead of writing it")
    ap.add_argument("--report", action="store_true",
                    help="also print off-palette colours by picture group")
    args = ap.parse_args(argv)

    try:
        palette, art_count, total = build_palette(args.pack)
    except (OSError, ValueError) as exc:
        print("cannot build the palette: %s" % exc)
        return 1

    colours = palette_colours(palette)
    used = set()
    pictures = locked_pictures(args.pack)
    for path in pictures:
        used |= picture_colours(path)
    off_palette = len([c for c in used if c not in colours])

    if args.check:
        if not args.out.exists():
            print("no palette at %s" % args.out)
            return 1
        with open(args.out, "r", encoding="utf-8") as fh:
            have = json.load(fh)
        if have != palette:
            print("drift: %s is not what make_palette.py builds "
                  "(%d colours in the file, %d built)"
                  % (args.out, len(have.get("colors", [])), total))
            return 1
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(palette, fh, indent=2)
            fh.write("\n")

    print(summary_line(args.out, art_count, total, off_palette, len(pictures)))
    if off_palette:
        print("the locked art has colours the palette does not hold")
        return 1
    if args.report:
        return report(args.pack, set(colours))
    return 0


if __name__ == "__main__":
    sys.exit(main())