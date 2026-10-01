#!/usr/bin/env python3
"""check_ui.py: check a UI skin folder (skin.json and its pictures) against the rules.

  check_ui.py SKIN_DIR [--ink-on-panel #RRGGBB] [--ink-on-panel-dim #RRGGBB]

A skin is a folder of pictures plus one skin.json that says which picture is
which part of the interface. The tool only reads: it prints one problem per
line as `part: what is wrong` and exits 1 when the skin is bad; a good skin
prints one `ok <part>` line per part and exits 0 (usage errors exit 2). It
checks that every named picture exists and ends in .webp or .png, that pieces
stay under 128 KB and textures under 256 KB, that each slice fits the real
picture, that the four button states share one size and differ visibly, that
the panel's border ring is mirror-symmetric (process_ui.py box builds it that
way, so only the ring is compared; the inside is left alone because a tiled
texture fill cannot be mirror-symmetric by nature), that the ink reads on the
panel's inside at 4.5:1 and 3:1 WCAG contrast, and that a cursor hotspot lies
inside its picture. The --ink-on-panel* flags override skin.json's ink. Needs
Pillow:
  uv run --offline --with pillow art/tools/check_ui.py art/skins/parchment
"""
import argparse
import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from process_sprites import fail

PICTURE_SUFFIXES = (".webp", ".png")
# The keys that name a picture file even when the value has no picture suffix;
# `fill` alone decides by suffix, because a panel's fill may be a texture.
FILE_KEYS = ("file", "hover", "pressed", "disabled", "selected", "off", "on", "frame")
STATE_KEYS = ("file", "hover", "pressed", "disabled")
KB_UNIT = 1024                 # bytes in the KB this tool reports
PIECE_CAP = 128 * KB_UNIT      # a named picture must stay under 128 KB
TEXTURE_CAP = 256 * KB_UNIT    # a texture must stay under 256 KB
MIN_STATE_DIFF = 3.0           # button states must differ by more than this (of 255)
SYMMETRY_TOLERANCE = 2.0       # the border ring may differ by less than this per channel
PATCH = 16                     # centre patch that gives the panel's inside colour
MIN_ON_PANEL = 4.5             # WCAG contrast ratio required for ink.on_panel
MIN_ON_PANEL_DIM = 3.0         # WCAG contrast ratio required for ink.on_panel_dim


def read_picture(skin_dir, name):
    """Open a named picture as RGBA, returning (image, None) or (None, a reason)."""
    path = os.path.join(skin_dir, name)
    try:
        with Image.open(path) as im:
            return im.convert("RGBA"), None
    except FileNotFoundError:
        return None, "not found"
    except (OSError, ValueError) as exc:
        # A problem line, not fail(): a bad skin is a failed check (exit 1),
        # never a usage error (exit 2), so read failures need a reason instead.
        return None, str(exc)


def has_picture_suffix(name):
    """True when a file name ends in .webp or .png, ignoring case."""
    return os.path.splitext(name)[1].lower() in PICTURE_SUFFIXES


def is_whole(value):
    """True when a JSON value is a whole number (an int, or a float with nothing after it)."""
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return True
    if isinstance(value, float):
        return value.is_integer()
    return False


def parse_hex(spec):
    """Parse #RRGGBB into an RGB tuple, or return None when it is not that shape."""
    if not isinstance(spec, str) or len(spec) != 7 or spec[0] != "#":
        return None
    try:
        return tuple(int(spec[i:i + 2], 16) for i in (1, 3, 5))
    except ValueError:
        return None


def parse_ink_flag(value, flag_name):
    """Validate an --ink-on-panel* flag as #RRGGBB, or fail plainly (usage)."""
    if value is None:
        return None
    if parse_hex(value) is None:
        fail(f"{flag_name} wants #RRGGBB like #2B2118, got {value!r}")
    return value


def split_values(spec):
    """Split a part's string values into the picture files it names and the textures it uses."""
    files, textures = [], []
    for key, value in spec.items():
        if not isinstance(value, str):
            continue  # slice, hotspot and other structured values
        if key in FILE_KEYS:
            files.append(value)  # a bad suffix is the file check's job to report
        elif key == "fill" and not has_picture_suffix(value):
            textures.append(value)  # a panel's "fill": "parchment" names a texture
        elif has_picture_suffix(value):
            files.append(value)  # any other key naming a picture is still checked
        else:
            textures.append(value)  # a declared texture like "parchment"
    return files, textures


def gather_files(parts):
    """Collect the picture file names every part names, in order, without repeats."""
    files = []
    for spec in parts.values():
        for name in split_values(spec)[0]:
            if name not in files:
                files.append(name)
    return files


def load_skin(skin_dir):
    """Read skin.json, returning (skin, problems); the skin is None when it cannot be checked."""
    path = os.path.join(skin_dir, "skin.json")
    if not os.path.isfile(path):
        return None, ["skin.json: not found"]
    try:
        with open(path, "r", encoding="utf-8") as fh:
            skin = json.load(fh)
    except json.JSONDecodeError as exc:
        return None, [f"skin.json: not valid JSON ({exc})"]
    except (OSError, ValueError) as exc:
        return None, [f"skin.json: cannot read it ({exc})"]
    if not isinstance(skin, dict):
        return None, ["skin.json: not a JSON object"]
    parts = skin.get("parts")
    if not isinstance(parts, dict):
        return None, ['skin.json: no "parts" object']
    problems = [f"{name}: not a JSON object" for name, spec in parts.items()
                if not isinstance(spec, dict)]
    if problems:
        return None, problems
    return skin, []


def resolve_inks(skin, flag_on_panel, flag_on_panel_dim):
    """The ink colours to check: a flag wins over the ink block in skin.json."""
    declared = skin.get("ink")
    if not isinstance(declared, dict):
        declared = {}
    return {
        "on_panel": flag_on_panel if flag_on_panel is not None else declared.get("on_panel"),
        "on_panel_dim": (flag_on_panel_dim if flag_on_panel_dim is not None
                         else declared.get("on_panel_dim")),
    }


def check_files(skin_dir, parts):
    """Check 1: every named picture exists in the skin folder and ends in .webp or .png."""
    problems = []
    for name in gather_files(parts):
        if not has_picture_suffix(name):
            problems.append(f"{name}: not a .webp or .png picture")
        elif not os.path.isfile(os.path.join(skin_dir, name)):
            problems.append(f"{name}: not found")
    return problems


def check_sizes(skin_dir, parts):
    """Check 2: pieces stay under 128 KB and textures under 256 KB and resolve to a file."""
    problems = []
    for name in gather_files(parts):
        if not has_picture_suffix(name):
            continue  # a bad suffix is already a problem above
        path = os.path.join(skin_dir, name)
        if not os.path.isfile(path):
            continue  # a missing file is already a problem above
        size = os.path.getsize(path)
        if size >= PIECE_CAP:
            cap = PIECE_CAP // KB_UNIT
            problems.append(f"{name}: {size / KB_UNIT:.1f} KB is over the {cap} KB cap for a piece")
    seen = []
    for spec in parts.values():
        for texture in split_values(spec)[1]:
            if texture in seen:
                continue
            seen.append(texture)
            path, suffix = None, None
            for ext in PICTURE_SUFFIXES:
                candidate = os.path.join(skin_dir, texture + ext)
                if os.path.isfile(candidate):
                    path, suffix = candidate, ext
                    break
            if path is None:
                problems.append(f"{texture}: not a texture here "
                                f"(no {texture}.webp or {texture}.png)")
                continue
            size = os.path.getsize(path)
            if size >= TEXTURE_CAP:
                cap = TEXTURE_CAP // KB_UNIT
                problems.append(f"{texture}{suffix}: {size / KB_UNIT:.1f} KB is over the "
                                f"{cap} KB cap for a texture")
    return problems


def check_slices(skin_dir, parts):
    """Check 3: a slice is a whole number and fits the real picture it names."""
    problems = []
    for part, spec in parts.items():
        if "slice" not in spec:
            continue
        slice_value = spec["slice"]
        if not is_whole(slice_value):
            problems.append(f"{part}: slice {slice_value!r} is not a whole number")
            continue
        name = spec.get("file")
        if not isinstance(name, str):
            problems.append(f"{part}: has a slice but no file to check it against")
            continue
        img, reason = read_picture(skin_dir, name)
        if img is None:
            problems.append(f"{name}: cannot read: {reason}")
            continue
        w, h = img.size
        if not (2 * slice_value < w and 2 * slice_value < h):
            problems.append(f"{name}: slice {slice_value} does not fit a {w}x{h} picture "
                            f"(2 * slice must be smaller than both)")
    return problems


def mean_abs_diff(a, b):
    """Mean absolute per-channel difference between two equally sized pictures, of 255."""
    pa = a.convert("RGB").tobytes()
    pb = b.convert("RGB").tobytes()
    if not pa:
        return 0.0
    total = 0
    for i in range(len(pa)):
        total += abs(pa[i] - pb[i])
    return total / len(pa)


def check_button_states(skin_dir, parts):
    """Check 4: the four button states share one size and every pair differs visibly."""
    problems = []
    for part, spec in parts.items():
        if any(key not in spec for key in STATE_KEYS):
            continue  # a part naming only some of the four is not checked
        if any(not isinstance(spec[key], str) for key in STATE_KEYS):
            problems.append(f"{part}: a button state is not a file name")
            continue
        images = {}
        readable = True
        for key in STATE_KEYS:
            name = spec[key]
            img, reason = read_picture(skin_dir, name)
            if img is None:
                if reason != "not found":
                    problems.append(f"{name}: cannot read: {reason}")
                readable = False  # a missing file is already the file check's problem
            images[key] = (name, img)
        if not readable:
            continue
        sizes = {key: images[key][1].size for key in STATE_KEYS}
        if len(set(sizes.values())) > 1:
            detail = ", ".join(f"{key} {sizes[key][0]}x{sizes[key][1]}" for key in STATE_KEYS)
            problems.append(f"{part}: the four button states are not all the same size "
                            f"({detail})")
            continue
        pairs = (("file", "hover"), ("file", "pressed"), ("file", "disabled"),
                 ("hover", "pressed"), ("hover", "disabled"), ("pressed", "disabled"))
        for first, second in pairs:
            diff = mean_abs_diff(images[first][1], images[second][1])
            if diff <= MIN_STATE_DIFF:
                problems.append(f"{part}: {images[first][0]} and {images[second][0]} are "
                                f"too alike (mean difference {diff:.1f} of 255, "
                                f"needs above {MIN_STATE_DIFF})")
    return problems


def ring_mean_diff(raw, w, h, slice_size, vertical):
    """Mean per-channel difference between the border ring and one flip, of 255."""
    total = 0
    count = 0
    for y in range(h):
        for x in range(w):
            if slice_size <= x < w - slice_size and slice_size <= y < h - slice_size:
                continue  # inside the ring, deliberately not compared
            if vertical:
                fx, fy = x, h - 1 - y
            else:
                fx, fy = w - 1 - x, y
            i = 4 * (y * w + x)
            j = 4 * (fy * w + fx)
            total += (abs(raw[i] - raw[j])
                      + abs(raw[i + 1] - raw[j + 1])
                      + abs(raw[i + 2] - raw[j + 2]))
            count += 1
    return total / (3.0 * count) if count else 0.0


def check_panel_symmetry(skin_dir, parts):
    """Check 5: the panel's border ring mirrors on both axes within tolerance 2.

    process_ui.py `box` rebuilds a border from one corner and one band per edge,
    mirrored, so a panel made by the tool is symmetric by construction. A panel
    that is NOT symmetric was not made by the tool, or its inside was filled with
    a tiled texture - and a tiled texture cannot be mirror-symmetric by nature.
    So only the BORDER RING (the pixels within slice of any edge) is compared:
    the inside is deliberately left out, because a texture-filled inside would
    fail the mirror test through no fault of the border itself.
    """
    problems = []
    spec = parts.get("panel")
    if spec is None or "slice" not in spec:
        return problems
    slice_value = spec["slice"]
    name = spec.get("file")
    if not is_whole(slice_value) or not isinstance(name, str):
        return problems  # the slice check and the file check report these
    img, reason = read_picture(skin_dir, name)
    if img is None:
        return problems  # the slice check reports the read failure for this same picture
    w, h = img.size
    raw = img.tobytes()
    for label, vertical in (("left-right", False), ("top-bottom", True)):
        mean = ring_mean_diff(raw, w, h, slice_value, vertical)
        if mean >= SYMMETRY_TOLERANCE:
            problems.append(f"{name}: the border ring is not symmetric {label} "
                            f"(mean difference {mean:.2f}, tolerance "
                            f"{SYMMETRY_TOLERANCE:g})")
    return problems


def centre_average(img):
    """The average RGB colour of the PATCH x PATCH patch at the centre of a picture."""
    w, h = img.size
    side = min(PATCH, w, h)
    x0, y0 = (w - side) // 2, (h - side) // 2
    raw = img.crop((x0, y0, x0 + side, y0 + side)).convert("RGB").tobytes()
    count = side * side
    return (sum(raw[0::3]) / count, sum(raw[1::3]) / count, sum(raw[2::3]) / count)


def relative_luminance(rgb):
    """The WCAG relative luminance of an RGB colour."""
    def channel(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_ratio(a, b):
    """The WCAG contrast ratio of two RGB colours, the lighter one on top."""
    la, lb = relative_luminance(a), relative_luminance(b)
    lighter, darker = max(la, lb), min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)


def check_contrast(skin_dir, parts, inks):
    """Check 6: each declared ink reads against the panel's inside at its WCAG ratio."""
    problems = []
    spec = parts.get("panel")
    if spec is None:
        return problems  # no panel: there is no inside to read text against
    wanted = (("on_panel", MIN_ON_PANEL, "4.5"),
              ("on_panel_dim", MIN_ON_PANEL_DIM, "3"))
    valid = []
    for key, minimum, shown in wanted:
        ink = inks.get(key)
        if ink is None:
            problems.append(f"panel: no ink.{key} declared, so contrast cannot be checked")
            continue
        rgb = parse_hex(ink)
        if rgb is None:
            problems.append(f"panel: ink.{key} {ink!r} is not a #RRGGBB colour")
            continue
        valid.append((key, ink, rgb, minimum, shown))
    if not valid:
        return problems
    name = spec.get("file")
    if not isinstance(name, str):
        problems.append("panel: no file to read the inside colour from")
        return problems
    img, reason = read_picture(skin_dir, name)
    if img is None:
        if reason != "not found":
            problems.append(f"{name}: cannot read: {reason}")
        return problems  # a missing file is already the file check's problem
    inside = centre_average(img)
    for key, ink, rgb, minimum, shown in valid:
        ratio = contrast_ratio(rgb, inside)
        if ratio < minimum:
            problems.append(f"panel: ink.{key} {ink} is {ratio:.2f}:1 on the panel, "
                            f"needs {shown}:1")
    return problems


def check_hotspots(skin_dir, parts):
    """Check 7: every declared hotspot lies inside its picture; a cursor declares one."""
    problems = []
    for part, spec in parts.items():
        hotspot = spec.get("hotspot")
        if hotspot is None:
            if part == "cursor":
                problems.append("cursor: no hotspot declared")
            continue
        if not (isinstance(hotspot, list) and len(hotspot) == 2
                and all(is_whole(value) for value in hotspot)):
            problems.append(f"{part}: hotspot {hotspot!r} is not a list of two whole numbers")
            continue
        name = spec.get("file")
        if not isinstance(name, str):
            problems.append(f"{part}: a hotspot but no file to check it against")
            continue
        img, reason = read_picture(skin_dir, name)
        if img is None:
            if reason != "not found":
                problems.append(f"{name}: cannot read: {reason}")
            continue  # a missing file is already the file check's problem
        w, h = img.size
        x, y = hotspot
        if not (0 <= x < w and 0 <= y < h):
            problems.append(f"{part}: hotspot [{x:g}, {y:g}] is outside the {w}x{h} picture")
    return problems


def main(argv=None):
    """Run the check_ui.py command line and return its exit code."""
    ap = argparse.ArgumentParser(
        description="Check a UI skin folder (skin.json plus its pictures) against the rules.")
    ap.add_argument("skin_dir", metavar="SKIN_DIR",
                    help="folder holding skin.json and the skin's pictures")
    ap.add_argument("--ink-on-panel", metavar="#RRGGBB", dest="ink_on_panel",
                    help="ink colour on the panel, overriding skin.json")
    ap.add_argument("--ink-on-panel-dim", metavar="#RRGGBB", dest="ink_on_panel_dim",
                    help="dim ink colour on the panel, overriding skin.json")
    a = ap.parse_args(argv)

    if not os.path.isdir(a.skin_dir):
        fail(f"no such directory: {a.skin_dir}")
    flag_on = parse_ink_flag(a.ink_on_panel, "--ink-on-panel")
    flag_dim = parse_ink_flag(a.ink_on_panel_dim, "--ink-on-panel-dim")

    skin, problems = load_skin(a.skin_dir)
    if skin is None:
        for line in problems:
            print(line)
        return 1

    parts = skin["parts"]
    inks = resolve_inks(skin, flag_on, flag_dim)
    problems = []
    problems += check_files(a.skin_dir, parts)
    problems += check_sizes(a.skin_dir, parts)
    problems += check_slices(a.skin_dir, parts)
    problems += check_button_states(a.skin_dir, parts)
    problems += check_panel_symmetry(a.skin_dir, parts)
    problems += check_contrast(a.skin_dir, parts, inks)
    problems += check_hotspots(a.skin_dir, parts)

    unique = []
    for line in problems:
        if line not in unique:
            unique.append(line)
    if unique:
        for line in unique:
            print(line)
        return 1
    for part in parts:
        print("ok %s" % part)
    return 0


if __name__ == "__main__":
    sys.exit(main())
