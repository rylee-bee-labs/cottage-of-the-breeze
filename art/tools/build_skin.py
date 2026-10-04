#!/usr/bin/env python3
"""build_skin.py: turn a folder of raw drawn pictures into a finished skin folder.

  build_skin.py SOURCE_DIR OUT_DIR --name parchment-and-wood
                [--credit TEXT] [--backdrop TEXT] [--font ROLE=FAMILY]...

One command walks the geometry table below: every box piece goes through
process_ui.process_box and every ornament through process_ui.process_strip
(process_ui.py is the single source of truth for how a panel becomes a
nine-slice - this tool never reimplements the mirroring), the three textures
are copied byte for byte with shutil.copyfile, and skin.json is written LAST
from the same table, so its slices can never disagree with the pictures. It
prints one `wrote ...` line per file and nothing else; a missing SOURCE_DIR
or a missing source picture is a plain one-line message with exit 2.

The three optional flags write the settings a skin may declare, and every one
of them is off by default: --credit replaces the credit line (the CREDIT
constant below stays the default, byte for byte), --backdrop names a texture
in the skin folder as the skin's backdrop and adds one top-level "backdrop"
key, and a repeated --font ROLE=FAMILY fills a top-level "fonts" object
(display=Crimson Pro writes "display": "Crimson Pro"), one family per role.
Two --font flags for one role, or a flag that is not ROLE=FAMILY with a
non-empty role and family, are each a plain one-line message with exit 2.
Without the flags skin.json is exactly what it has always been: its keys come
out in one fixed order - name, credit, backdrop, fonts, parts, ink - and
"backdrop" and "fonts" join that order only when their flag asked for them.

Running it twice into the same folder is byte-identical (idempotent): nothing
varies from run to run - no timestamps, no randomness, and the JSON keys are
inserted in one fixed order - and the pieces are saved as LOSSLESS WebP,
which Pillow encodes deterministically for the same pixels and settings and
which round-trips the picture exactly, so the built panel decodes to the
mirror-symmetric image process_box made (lossy WebP would not). The test in
art/tests/test_build_skin.py proves both runs byte for byte. Needs Pillow:
  uv run --offline --with pillow art/tools/build_skin.py SOURCE_DIR OUT_DIR
                                     --name parchment-and-wood
"""
import argparse
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import process_ui
from process_ui import fail, open_image

# The geometry table: (source name, output name, kind, (width, height), slice,
# fill texture). kind is "box", "strip" or "copy"; only a box has a slice, and
# only the panel and the slot fill their inside from a texture. skin.json's
# slices are read from here, so the JSON and the pictures cannot disagree.
PICTURES = (
    ("panel.webp", "panel.webp", "box", (96, 96), 32, "parchment.png"),
    ("speech.webp", "speech.webp", "box", (192, 96), 24, ""),
    ("tooltip.webp", "tooltip.webp", "box", (96, 64), 20, ""),
    ("button.webp", "button.webp", "box", (96, 40), 14, ""),
    ("button-hover.webp", "button-hover.webp", "box", (96, 40), 14, ""),
    ("button-pressed.webp", "button-pressed.webp", "box", (96, 40), 14, ""),
    ("button-disabled.webp", "button-disabled.webp", "box", (96, 40), 14, ""),
    ("tab.webp", "tab.webp", "box", (96, 40), 14, ""),
    ("tab-selected.webp", "tab-selected.webp", "box", (96, 40), 14, ""),
    ("toggle-off.webp", "toggle-off.webp", "strip", (64, 32), 0, ""),
    ("toggle-on.webp", "toggle-on.webp", "strip", (64, 32), 0, ""),
    ("bar-frame.webp", "bar-frame.webp", "box", (192, 32), 10, ""),
    ("bar-fill.webp", "bar-fill.webp", "strip", (176, 20), 0, ""),
    ("gold-plate.webp", "gold-plate.webp", "box", (96, 32), 10, ""),
    ("slot.webp", "slot.webp", "box", (64, 64), 16, "parchment.png"),
    ("divider.webp", "divider.webp", "strip", (192, 16), 0, ""),
    ("banner.webp", "banner.webp", "strip", (192, 48), 0, ""),
    ("corner.webp", "corner.webp", "strip", (48, 48), 0, ""),
    ("cursor.webp", "cursor.webp", "strip", (32, 32), 0, ""),
    ("parchment.png", "parchment.png", "copy", (0, 0), 0, ""),
    ("wood.png", "wood.png", "copy", (0, 0), 0, ""),
    ("brass.png", "brass.png", "copy", (0, 0), 0, ""),
)

TOLERANCE = 28              # the colour match process_ui.py uses, passed on every call
FILL_NAME = "parchment"     # the texture name skin.json declares for panel and slot
CREDIT = "Rylee and Claude; Codex proofs, training: not cleared"
INK = {"on_panel": "#2B2118", "on_panel_dim": "#5A4A38"}


def slice_of(name):
    """The slice of an output picture, read straight from the geometry table."""
    for _, output, _, _, slice_size, _ in PICTURES:
        if output == name:
            return slice_size
    fail(f"the geometry table has no picture called {name}")


def build_parts():
    """The skin.json parts block, every slice read from the geometry table."""
    return {
        "panel": {"file": "panel.webp", "slice": slice_of("panel.webp"),
                  "fill": FILL_NAME},
        "button": {"file": "button.webp", "slice": slice_of("button.webp"),
                   "hover": "button-hover.webp", "pressed": "button-pressed.webp",
                   "disabled": "button-disabled.webp"},
        "tab": {"file": "tab.webp", "slice": slice_of("tab.webp"),
                "selected": "tab-selected.webp"},
        "toggle": {"off": "toggle-off.webp", "on": "toggle-on.webp"},
        "bar": {"frame": "bar-frame.webp", "fill": "bar-fill.webp"},
        "slot": {"file": "slot.webp", "slice": slice_of("slot.webp")},
        "speech": {"file": "speech.webp", "slice": slice_of("speech.webp")},
        "tooltip": {"file": "tooltip.webp", "slice": slice_of("tooltip.webp")},
        "gold-plate": {"file": "gold-plate.webp",
                       "slice": slice_of("gold-plate.webp")},
        "divider": {"file": "divider.webp"},
        "banner": {"file": "banner.webp"},
        "corner": {"file": "corner.webp"},
        "cursor": {"file": "cursor.webp", "hotspot": [4, 4]},
    }


def parse_fonts(specs):
    """The skin.json fonts block from --font ROLE=FAMILY flags, or fail plainly."""
    fonts = {}
    for spec in specs:
        bits = spec.split("=")
        if len(bits) != 2 or not bits[0] or not bits[1]:
            fail(f"--font wants ROLE=FAMILY like display=Crimson Pro, got {spec!r}")
        role, family = bits
        if role in fonts:
            fail(f"--font {role} is given twice, one family per role: {family!r}")
        fonts[role] = family
    return fonts


def skin_document(name, credit=CREDIT, backdrop=None, fonts=None):
    """The whole skin.json contents, keys in one fixed order: name, credit,
    backdrop, fonts, parts, ink - backdrop and fonts join that order only
    when their flag asked for them, so a build with no flags writes what it
    always wrote."""
    doc = {"name": name, "credit": credit}
    if backdrop is not None:
        doc["backdrop"] = backdrop
    if fonts:
        doc["fonts"] = fonts
    doc["parts"] = build_parts()
    doc["ink"] = INK
    return doc


def build_picture(source_path, out_path, kind, size, slice_size, fill_path):
    """Make one output picture with process_ui, or copy a texture byte for byte."""
    if kind == "copy":
        shutil.copyfile(source_path, out_path)
        return
    if kind == "strip":
        out = process_ui.process_strip(open_image(source_path),
                                       size[0], size[1], TOLERANCE)
    elif kind == "box":
        out = process_ui.process_box(open_image(source_path), size[0], size[1],
                                     slice_size, fill_path, None, TOLERANCE, True)
    else:
        fail(f"unknown picture kind: {kind!r}")
    out.save(out_path, lossless=True)  # deterministic, and the pixels round-trip exactly


def main(argv=None):
    """Run the build_skin.py command line and return its exit code."""
    ap = argparse.ArgumentParser(
        description="Turn a folder of raw drawn pictures into a finished skin folder.")
    ap.add_argument("source_dir", metavar="SOURCE_DIR",
                    help="folder of raw drawn pictures")
    ap.add_argument("out_dir", metavar="OUT_DIR",
                    help="folder to write the finished skin into (made if missing)")
    ap.add_argument("--name", required=True,
                    help="the skin's name, written into skin.json")
    ap.add_argument("--credit", metavar="TEXT", default=CREDIT,
                    help="the credit line written into skin.json (default: the "
                         "CREDIT line above)")
    ap.add_argument("--backdrop", metavar="TEXT",
                    help="name a texture in the skin folder as the skin's backdrop, "
                         "adding one top-level \"backdrop\" key to skin.json "
                         "(no key when not given)")
    ap.add_argument("--font", action="append", dest="fonts", metavar="ROLE=FAMILY",
                    help="a font family for one text role, like display=Crimson Pro; "
                         "repeat for more roles to fill one top-level \"fonts\" object "
                         "in skin.json (no key when not given)")
    a = ap.parse_args(argv)

    if not os.path.isdir(a.source_dir):
        fail(f"no such directory: {a.source_dir}")
    fonts = parse_fonts(a.fonts or ())
    for source_name, _, _, _, _, _ in PICTURES:
        path = os.path.join(a.source_dir, source_name)
        if not os.path.isfile(path):
            fail(f"missing source picture: {path}")

    os.makedirs(a.out_dir, exist_ok=True)
    for source_name, output_name, kind, size, slice_size, fill in PICTURES:
        source_path = os.path.join(a.source_dir, source_name)
        out_path = os.path.join(a.out_dir, output_name)
        fill_path = os.path.join(a.source_dir, fill) if fill else None
        build_picture(source_path, out_path, kind, size, slice_size, fill_path)
        print(f"wrote {out_path}")

    # skin.json last, after every picture, so a failed build never leaves one behind.
    skin_path = os.path.join(a.out_dir, "skin.json")
    doc = skin_document(a.name, credit=a.credit, backdrop=a.backdrop, fonts=fonts)
    with open(skin_path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {skin_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
