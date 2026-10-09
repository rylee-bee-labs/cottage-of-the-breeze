#!/usr/bin/env python3
"""mock_skin.py: draw a finished skin the way the player will, at a real viewport size.

  mock_skin.py SKIN_DIR OUT.png [--size 390x844 | --size 1280x800]

  mock_skin.py SKIN_DIR OUT.png --parts banner,divider,corner,cursor,gold-plate

The skin folder holds small pictures and a skin.json; what matters is whether the
chrome *reads* once it is assembled - a nine-slice rim that thins out when the box
is wide, two tab chips that stop being the same shape, a cursor too faint on the
backdrop. `preview.html` draws the parts one by one, which hides exactly those
problems, so this draws them assembled at the size a phone or a desktop actually
gives them, over the skin's own backdrop, with real text in the skin's ink.

It is a mock, not the engine: it reads slice values out of skin.json and mirrors
the boxes the way CSS border-image does, so a part that looks right here looks
right in the player. It does not read VEFR, and it is not a validator - run
`check_ui.py` for the checks that decide whether a skin is legal. Its job is
looking. Needs Pillow:
  uv run --offline --with pillow art/tools/mock_skin.py art/skins/parchment-and-wood look.png --size 390x844
"""
import argparse
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

PANELS = ("panel", "speech", "tooltip", "button", "tab", "slot", "gold-plate", "bar")
SIZES = {"phone": (390, 844), "desktop": (1280, 800)}


def fail(message):
    """A plain one-line problem, exit 2, with no traceback."""
    print(message, file=sys.stderr)
    raise SystemExit(2)


def parse_size(spec):
    if spec.lower() in SIZES:
        return SIZES[spec.lower()]
    bits = spec.lower().split("x")
    if len(bits) != 2 or not all(b.isdigit() for b in bits):
        fail(f"--size wants WxH like 390x844, or one of {', '.join(SIZES)}, got {spec!r}")
    return int(bits[0]), int(bits[1])


def load_font(size):
    """The closest serif we can find to the skin's Crimson Pro; a mock, not a proof."""
    for path in ("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def nine_slice(part, width, height, slice_):
    """Stretch `part` to width x height the way CSS border-image does with `slice_`.

    The four corners are pasted whole and unscaled; the four edges stretch to the
    space between them; the middle stretches to fill what is left. That is exactly
    what the player does, so a rim that thins out at a given size shows up here.
    """
    im = part.convert("RGBA")
    w, h = im.size
    if 2 * slice_ >= min(w, h):
        fail(f"slice {slice_} does not fit the {w}x{h} part")
    mid_w, mid_h = width - 2 * slice_, height - 2 * slice_
    if mid_w <= 0 or mid_h <= 0:
        return im.resize((width, height), Image.LANCZOS)
    out = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    # corners: (left, upper, right, lower) of the source, pasted as drawn
    for box, where in (((0, 0, slice_, slice_), (0, 0)),
                       ((w - slice_, 0, w, slice_), (width - slice_, 0)),
                       ((0, h - slice_, slice_, h), (0, height - slice_)),
                       ((w - slice_, h - slice_, w, h), (width - slice_, height - slice_))):
        out.paste(im.crop(box), where)
    # edges: stretched to the gap between the corners
    for box, size, where in (
            ((slice_, 0, w - slice_, slice_), (mid_w, slice_), (slice_, 0)),
            ((slice_, h - slice_, w - slice_, h), (mid_w, slice_), (slice_, height - slice_)),
            ((0, slice_, slice_, h - slice_), (slice_, mid_h), (0, slice_)),
            ((w - slice_, slice_, w, h - slice_), (slice_, mid_h), (width - slice_, slice_))):
        out.paste(im.crop(box).resize(size, Image.LANCZOS), where)
    # middle: stretched to fill
    out.paste(im.crop((slice_, slice_, w - slice_, h - slice_)).resize((mid_w, mid_h), Image.LANCZOS),
              (slice_, slice_))
    return out


def wrap(draw, text, font, width):
    words, lines, line = text.split(), [], ""
    for word in words:
        if draw.textlength(line + " " + word, font=font) <= width or not line:
            line = (line + " " + word).strip()
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("skin", metavar="SKIN_DIR", help="a built skin folder, with skin.json")
    ap.add_argument("out", metavar="OUT.png", help="where to write the mock")
    ap.add_argument("--size", default="1280x800", help="viewport, WxH or 'phone' / 'desktop'")
    ap.add_argument("--parts", default=",".join(PANELS),
                    help="comma-separated parts to draw, or 'none' for the backdrop alone")
    a = ap.parse_args(argv)

    width, height = parse_size(a.size)
    try:
        skin = json.loads(open(os.path.join(a.skin, "skin.json"), encoding="utf-8").read())
    except OSError:
        fail(f"cannot read {os.path.join(a.skin, 'skin.json')}")

    def part(name):
        # A part is named in skin.json under its own key, or under a state of
        # another part: tab-selected is "tab" -> "selected", a bar is "frame"/"fill".
        node = skin["parts"].get(name, {})
        file = node.get("file")
        if not file and "-" in name:
            base, state = name.split("-", 1)
            file = skin["parts"].get(base, {}).get(state)
        if not file:
            return None
        try:
            return Image.open(os.path.join(a.skin, file)).convert("RGBA")
        except OSError:
            fail(f"cannot read the {name} picture {file!r}")

    backdrop = None
    if skin.get("backdrop"):
        try:
            backdrop = Image.open(os.path.join(a.skin, skin["backdrop"])).convert("RGB")
        except OSError:
            fail(f"cannot read the backdrop {skin['backdrop']!r}")
    canvas = backdrop.resize((width, height), Image.LANCZOS) if backdrop \
        else Image.new("RGB", (width, height), (58, 44, 32))
    draw = ImageDraw.Draw(canvas)
    ink = skin.get("ink", {}).get("on_panel", "#2B2118")
    dim = skin.get("ink", {}).get("on_panel_dim", "#5A4A38")
    wanted = [] if a.parts.strip().lower() == "none" else [p.strip() for p in a.parts.split(",")]

    def put(im, x, y, w, h, name=None):
        if name and name not in wanted:
            return
        slice_ = skin["parts"].get(name, {}).get("slice") if name else None
        box = nine_slice(im, w, h, slice_) if slice_ else im.resize((w, h), Image.LANCZOS)
        canvas.paste(box, (x, y), box)

    # Rows flow down a cursor rather than sitting at fixed offsets, so the mock
    # still reads on a narrow viewport instead of running its parts into each other.
    narrow = width < 700
    row = 300

    # A dialogue panel with real text: the part that carries the most text, so the
    # first thing that breaks if a rim or an ink colour is off.
    if "panel" in wanted and part("panel"):
        box_h = min(240 if narrow else 260, height // 2)
        put(part("panel"), 24, 24, width - 48, box_h, "panel")
        f1, f2 = load_font(22), load_font(16)
        draw.text((48, 60), "The Spell Keeper", font=f1, fill=ink)
        for i, line in enumerate(wrap(draw, "Back up already? Sit a while. The kettle's still warm, "
                                        "and the beans have opinions about the hour.", f2, width - 110)):
            draw.text((48, 100 + i * 24), line, font=f2, fill=dim)
        row = 24 + box_h + 24

    if "tab" in wanted and part("tab"):
        sel = part("tab-selected") or Image.new("RGBA", part("tab").size)
        f = load_font(16)
        x = 24
        for label, chip in (("Bag", part("tab")), ("Journal", sel), ("Books", part("tab"))):
            w = max(96, 24 + int(draw.textlength(label, font=f)) + 24)
            put(chip, x, row, w, 40, "tab")
            draw.text((x + w // 2 - int(draw.textlength(label, font=f)) // 2, row + 12), label, font=f, fill=ink)
            x += w + 8
        row += 64

    if "button" in wanted and part("button"):
        f = load_font(16)
        x = 24
        for label in ("Strike", "Console", "Whisper"):
            put(part("button"), x, row, 110, 40, "button")
            draw.text((x + 55 - int(draw.textlength(label, font=f)) // 2, row + 12), label, font=f, fill=ink)
            x += 120
        row += 64

    speech_w = min(340, width - 48)
    if "speech" in wanted and part("speech"):
        put(part("speech"), 24, row, speech_w, 96, "speech")
        draw.text((44, row + 40), "Mind the beans.", font=load_font(16), fill=ink)
        # On a phone there is no room beside the speech box, so the tooltip drops
        # under it rather than landing on top of it; on a desktop it sits opposite.
        if not narrow:
            if "tooltip" in wanted and part("tooltip"):
                put(part("tooltip"), width - 240, row, 200, 64, "tooltip")
                draw.text((width - 224, row + 24), "a plain brass ring", font=load_font(14), fill=ink)
            row += 120
        else:
            row += 112

    if narrow and "tooltip" in wanted and part("tooltip"):
        put(part("tooltip"), 24, row, speech_w, 64, "tooltip")
        draw.text((44, row + 24), "a plain brass ring", font=load_font(14), fill=ink)
        row += 88

    if "gold-plate" in wanted and part("gold-plate"):
        put(part("gold-plate"), 24, row, 160, 32, "gold-plate")
        draw.text((44, row + 8), "12 gold", font=load_font(14), fill=ink)
        row += 56

    if "slot" in wanted and part("slot"):
        for i in range(5):
            put(part("slot"), 24 + i * 68, row, 64, 64, "slot")
        row += 88

    # The bar, drawn at a real health width so the fill/frame seam shows. The fill
    # goes *over* the frame's dark trough, the way the player draws it - the other
    # way round the frame's opaque middle hides the fill completely.
    if "bar" in wanted and part("bar-frame") and part("bar-fill"):
        frame, fill = part("bar-frame"), part("bar-fill")
        bar = Image.new("RGBA", (240, 32), (0, 0, 0, 0))
        bar.alpha_composite(frame.resize((240, 32), Image.LANCZOS))
        bar.alpha_composite(fill.resize((150, 12), Image.LANCZOS), (45, 10))
        canvas.paste(bar, (24, row), bar)

    canvas.save(a.out)
    print(f"wrote {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())