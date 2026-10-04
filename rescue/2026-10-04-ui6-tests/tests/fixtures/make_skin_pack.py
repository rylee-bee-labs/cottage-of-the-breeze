"""Build a skinned fixture pack (sample world + a tiny synthetic skin).

Neutral engine-test canon only: solid-colour PNGs written with the standard library, so no image
library is needed. `build(dest)` returns the pack dir; its world.json declares
`"skin": "skins/test-skin"` and the skin folder sits inside the pack.
"""

import base64
import json
import shutil
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "worlds" / "sample-world"


def png(w: int, h: int, rgb=(200, 170, 120)) -> bytes:
    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    raw = b"".join(b"\x00" + bytes(rgb) * w for _ in range(h))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


SKIN = {
    "name": "test-skin",
    "credit": "Rylee and Claude (a synthetic test skin)",
    "parts": {
        "panel": {"file": "panel.png", "slice": 16},
        "button": {"file": "button.png", "slice": 12, "hover": "button-hover.png",
                   "pressed": "button-pressed.png", "disabled": "button-disabled.png"},
        "bar": {"frame": "bar-frame.png", "fill": "bar-fill.png"},
        "cursor": {"file": "cursor.png", "hotspot": [2, 2]},
    },
    "ink": {"on_panel": "#2B2118", "on_panel_dim": "#5A4A38"},
}
FILES = {"panel.png": (64, 64), "button.png": (48, 32), "button-hover.png": (48, 32),
         "button-pressed.png": (48, 32), "button-disabled.png": (48, 32),
         "bar-frame.png": (96, 16), "bar-fill.png": (96, 16), "cursor.png": (32, 32)}

# The colour every fixture picture is drawn in unless `colours` says otherwise.
PARCHMENT = (200, 170, 120)

# ---- interface slice 4: the parts a skin may carry and the player ignores ----
# design/ui-skin.md ships these nine in Cottage's skin and `maplab.SKIN_PARTS`
# already accepts them; today only panel, button, bar and cursor are drawn. Every
# picture here is its own solid colour, so "this rule carries the slot picture"
# is a plain string test rather than a guess at a shape.
PARTS_SIZES = {
    "slot.png": (64, 48), "slot-hover.png": (64, 48), "slot-selected.png": (64, 48),
    "tab.png": (64, 40), "tab-selected.png": (64, 40),
    "toggle-off.png": (48, 28), "toggle-on.png": (48, 28),
    "tooltip.png": (72, 32),
    "speech.png": (96, 64),
    "divider.png": (96, 8),
    "banner.png": (128, 32),
    "corner.png": (16, 16),
    "gold-plate.png": (64, 40),
}
PARTS_COLOURS = {
    "slot.png": (36, 78, 120),          # a blue
    "slot-hover.png": (48, 96, 144),    # the same blue, one step up
    "slot-selected.png": (60, 116, 170),  # and one more: the worn row
    "tab.png": (24, 108, 72),           # a green
    "tab-selected.png": (36, 132, 92),
    "toggle-off.png": (150, 40, 40),     # a red
    "toggle-on.png": (190, 66, 52),
    "tooltip.png": (92, 60, 148),       # a violet
    "speech.png": (24, 112, 112),       # a teal
    "divider.png": (110, 74, 40),       # a brown
    "banner.png": (140, 40, 120),       # a magenta
    "corner.png": (110, 110, 110),      # a grey
    # a dark gold, not a bright one: the words on a gold control are the light
    # button ink, and this plate keeps them at 5.8:1.
    "gold-plate.png": (120, 88, 24),
}
# One entry per part, with the picture keys the contract names. `toggle` has no
# `file`: a switch is its two states (design/ui-skin.md's toggle-off/toggle-on).
PARTS_SKIN = {
    "slot": {"file": "slot.png", "slice": 12, "hover": "slot-hover.png",
             "selected": "slot-selected.png"},
    "tab": {"file": "tab.png", "slice": 12, "selected": "tab-selected.png"},
    "toggle": {"off": "toggle-off.png", "on": "toggle-on.png"},
    "tooltip": {"file": "tooltip.png", "slice": 8},
    "speech": {"file": "speech.png", "slice": 16},
    "divider": {"file": "divider.png"},
    "banner": {"file": "banner.png"},
    "corner": {"file": "corner.png"},
    "gold-plate": {"file": "gold-plate.png"},
}
# The whole skin: the four parts the player draws today, plus the nine it does not.
ALL_SKIN = {**SKIN, "parts": {**SKIN["parts"], **PARTS_SKIN}}
ALL_FILES = {**FILES, **PARTS_SIZES}


def colour_of(fname: str) -> tuple:
    """The solid colour a fixture picture is drawn in."""
    return PARTS_COLOURS.get(fname, PARCHMENT)


def picture_uri(fname: str) -> str:
    """The data URI `cli._baked_skin` bakes for a fixture picture.

    The tests that pin "this rule carries THIS part's picture" compare against
    this string, so it is built from the same bytes the pack is written with.
    """
    size = ALL_FILES[fname]
    blob = base64.b64encode(png(size[0], size[1], colour_of(fname))).decode("ascii")
    return f"data:image/png;base64,{blob}"


def build(dest: Path, skin=None, files=None, name="skin-test", colours=None) -> Path:
    pack = dest / "worlds" / name
    if pack.exists():
        shutil.rmtree(pack)
    pack.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SAMPLE, pack)
    world = json.loads((pack / "world.json").read_text(encoding="utf-8"))
    world["name"] = name
    world["skin"] = "skins/test-skin"
    (pack / "world.json").write_text(json.dumps(world), encoding="utf-8")
    sk = pack / "skins" / "test-skin"
    sk.mkdir(parents=True)
    (sk / "skin.json").write_text(json.dumps(skin if skin is not None else SKIN), encoding="utf-8")
    for fname, (w, h) in (files if files is not None else FILES).items():
        (sk / fname).write_bytes(png(w, h, (colours or {}).get(fname, PARCHMENT)))
    return pack


def build_parts(dest: Path, name: str = "skin-parts") -> Path:
    """A pack carrying every part a skin may name: the four already drawn, plus
    the nine of interface slice 4."""
    return build(dest, skin=ALL_SKIN, files=ALL_FILES, name=name, colours=PARTS_COLOURS)


if __name__ == "__main__":
    print(build(Path(sys.argv[1])))
