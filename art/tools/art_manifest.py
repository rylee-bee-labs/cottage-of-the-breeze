#!/usr/bin/env python3
"""art_manifest.py: every picture the game uses, and exactly what to draw next.

    art_manifest.py audit  [--pack DIR] [--json]
    art_manifest.py wanted [--kind KIND] [--loop N]
    art_manifest.py brief  BATCH [--out DIR]
    art_manifest.py brief  --all [--out DIR]

`audit` walks the pack and lists every art slot the game reads: each sprite
key, item icon, creature, resident, ground tile, door/stair tile, prop and
decal, with the file it resolves to, its native size and, for an animated
sprite, its frames. It fails (exit 1) when the pack names a picture that has
no file or no `player.sprites` entry, because the engine then draws a
fallback dot and validates clean. Shared pictures (a warden wearing another
creature's sprite) and files nothing reads are reported, not failed.

`wanted` lists the slots in `art/manifest/slots.json` that are not drawn yet.

`brief` fills `art/manifest/TEMPLATE.md` for one batch in `slots.json` and
writes two files an image-generation agent can be handed as they are:
`art/requests/BATCH.md` (what to draw, cell by cell, the style contract,
how to save, how it is checked) and `art/requests/BATCH.plan.json` (the cut
plan for VEFR's `tools/art/process_kit.py`, or the strip heights for
creatures). Nothing is generated or approved here: Rylee picks.

Stdlib only: sizes are read from the PNG and WebP headers, so this runs in
CI and on a phone-sized VM with no Pillow.
"""
import argparse
import json
import re
import struct
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PACK = REPO / "worlds" / "cottage-of-the-breeze"
MANIFEST_DIR = REPO / "art" / "manifest"
REQUESTS_DIR = REPO / "art" / "requests"

# What each kind of picture is, how big it is drawn in the game, how the
# image agent lays it out, and where it lands in the pack. The numbers are
# the GBA contract in art/STYLE.md (32 px tile, people 48 px tall in 64 x 64
# frames) and what the shipped files measure (`audit` prints them).
KINDS = {
    "item": {
        "title": "item icons",
        "native": "fits inside 24 x 24 px (a 32 px tile with room around it)",
        "sheet": "1536 x 1536, a 4 x 3 grid (12 cells at most)",
        "grid_max": 12,
        "cell": "one isolated, centred, fully visible chunky item icon, all icons at one consistent scale",
        "lands": "sprites/{id}.webp",
        "wire": "add `\"{id}\": \"sprites/{id}.webp\"` to `player.sprites` and set the item's `sprite`",
        "pipeline": "process_kit",
        "references": ["art/source/round22-gba/sheets/style-b.webp", "art/source/round23-gba/sheets/items-a.webp"],
    },
    "mob": {
        "title": "descent creatures",
        "native": "a still about 24 to 40 px tall; the six-frame strip at the same scale",
        "sheet": "step A: 1536 x 1536 stills, a 4 x 3 grid; step B: one 1536 x 512 strip per creature",
        "grid_max": 12,
        "cell": "one cute storybook creature, facing the viewer, standing on the cell's ground line",
        "lands": "sprites/{id}.webp, sprites/{id}-sheet.webp, sprites/{id}.sheet.json",
        "wire": "add the sprite to `player.sprites` (and `player.sprite_scale` if it should draw larger or smaller), then point the Blueprint family's `sprite` at it",
        "pipeline": "motion",
        "references": ["art/source/round22-gba/sheets/style-b.webp", "art/source/round23-gba/sheets/cellar-creatures-b.webp"],
    },
    "boss": {
        "title": "wardens and named guardians",
        "native": "a still about 64 to 96 px tall; the six-frame strip at the same scale",
        "sheet": "step A: 1536 x 1536 stills, a 2 x 2 grid; step B: one 1536 x 512 strip per guardian",
        "grid_max": 4,
        "cell": "one large, memorable, still-cute guardian, facing the viewer, standing on the cell's ground line",
        "lands": "sprites/{id}.webp, sprites/{id}-sheet.webp, sprites/{id}.sheet.json",
        "wire": "add the sprite to `player.sprites` with a `player.sprite_scale` of 1.2 to 1.7, then point the warden's Blueprint family `sprite` at it",
        "pipeline": "motion",
        "references": ["art/source/round22-gba/sheets/style-b.webp", "art/source/round23-gba/sheets/cellar-bosses.webp"],
    },
    "person": {
        "title": "residents",
        "native": "48 px tall in 64 x 64 frames",
        "sheet": "1536 x 1152, a 4 x 3 grid of the SAME person: row 1 facing down (idle, idle breathing, talk, talk), row 2 facing right, row 3 facing up",
        "grid_max": 1,
        "cell": "the same resident in every cell, at one consistent size",
        "lands": "sprites/{id}.webp, sprites/{id}-sheet.webp, sprites/{id}.sheet.json",
        "wire": "add the sprite to `player.sprites` under the speaker's id in `acts/*/world.json` `speakers`",
        "pipeline": "person",
        "references": ["art/source/round22-gba/sheets/style-b.webp", "art/source/round22-gba/sheets/npc-keeper.webp"],
    },
    "prop": {
        "title": "props (furniture and buildings)",
        "native": "its own size in whole tiles: `size` in the plan is pixels, 32 per tile",
        "sheet": "1536 x 1536, a 4 x 3 grid (12 cells at most)",
        "grid_max": 12,
        "cell": "one object, its front face straight down the screen, NOT isometric, never at an angle",
        "lands": "props/{id}.webp",
        "wire": "place it in a region's `contract.json` `props` as `{{\"pic\": \"{id}\", \"at\": [x, y], \"size\": [w, h]}}` (size in tiles)",
        "pipeline": "process_kit",
        "references": ["art/source/round22-gba/sheets/style-b.webp", "art/source/round23-gba/sheets/cottage-props.webp"],
    },
    "decor": {
        "title": "floor and wall decals",
        "native": "at most 32 x 32 px; wall decals hang from the top of the tile",
        "sheet": "1536 x 1536, a 4 x 3 grid (12 cells at most)",
        "grid_max": 12,
        "cell": "one small decal, seen from above for floors and front-on for walls",
        "lands": "props/{id}.webp",
        "wire": "add `{{\"pic\": \"{id}\", \"on\": \"floor\" or \"wall\", \"every\": N}}` to a Section's `decor`",
        "pipeline": "process_kit",
        "references": ["art/source/round22-gba/sheets/style-b.webp", "art/source/round23-gba/sheets/cellar-props.webp"],
    },
    "tile": {
        "title": "ground and wall surfaces",
        "native": "96 x 96 px: a 3 x 3 grid of 32 px cells that wraps without a seam",
        "sheet": "1536 x 1536, a 2 x 2 grid of textures, each filling its cell edge to edge",
        "grid_max": 4,
        "cell": "one surface texture filling the whole cell edge to edge, evenly lit, no objects, so it repeats without seams",
        "lands": "tiles/{id}.grid3x3.webp",
        "wire": "name it in a Section's `tiles` legend (or a region contract's legend `tile`)",
        "pipeline": "process_kit",
        "references": ["art/source/round22-gba/sheets/style-b.webp", "art/source/round23-gba/sheets/cellar-tiles-a.webp"],
    },
    "way": {
        "title": "doors and stairs",
        "native": "32 x 32 px, one tile",
        "sheet": "1536 x 1536, a 2 x 2 grid",
        "grid_max": 4,
        "cell": "one doorway or stair seen from above, front face straight down the screen",
        "lands": "tiles/way-{id}.webp",
        "wire": "drop it in the region's or the pack's `tiles/` folder; the engine draws `way-*` on transitions",
        "pipeline": "process_kit",
        "references": ["art/source/round22-gba/sheets/style-b.webp", "art/source/round23-gba/sheets/cellar-props.webp"],
    },
    "ui": {
        "title": "interface icons",
        "native": "16 x 16 or 24 x 24 px, readable at one glance",
        "sheet": "1536 x 1536, a 4 x 3 grid (12 cells at most)",
        "grid_max": 12,
        "cell": "one bold, simple icon with a thick outline, centred, readable at 16 px",
        "lands": "ui/{id}.webp",
        "wire": "NEEDS VEFR: the player has no pack slot for interface icons yet; record the companion engine change before drawing",
        "pipeline": "process_kit",
        "references": ["art/source/round22-gba/sheets/style-b.webp", "art/source/round23-gba/sheets/items-a.webp"],
    },
    "card": {
        "title": "illustrated cards",
        "native": "1600 x 900 px",
        "sheet": "one 1600 x 900 picture per call",
        "grid_max": 1,
        "cell": "one storybook scene",
        "lands": "assets/{id}.webp",
        "wire": "the title card is `player.title_art`",
        "pipeline": "none",
        "references": ["worlds/cottage-of-the-breeze/assets/title.webp"],
    },
}

STATUSES = ("shipped", "interim", "redo", "wanted")

# The style contract every brief carries, short enough to paste into one
# prompt. The long form is art/STYLE.md and round 23's prompts/DESIGN.md.
STYLE = (
    "True Game Boy Advance era pixel art in a warm storybook palette (like The Minish Cap and Mother 3). "
    "Crisp hard-edged square pixels, every pixel visible, no anti-aliasing, no blur, no gradients. "
    "1-pixel dark warm-brown outline (never pure black). Limited warm palette: umber, rust, amber, cream, "
    "soft moss green, with dusk teal #3F7E84 as the accent. Light from the top left. No ground shadows. "
    "Classic top-down RPG view, never isometric. Creatures are cute storybook mobs, not naturalistic animals. "
    "No text, letters, numbers, labels or frames anywhere. Nothing from Castle of the Winds."
)


# ---------------------------------------------------------------- sizes ---

def image_size(path):
    """(w, h) of a PNG or WebP from its header, or None if unreadable."""
    try:
        with open(path, "rb") as fh:
            head = fh.read(64)
    except OSError:
        return None
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", head[16:24])
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        chunk = head[12:16]
        if chunk == b"VP8X":
            w = int.from_bytes(head[24:27], "little") + 1
            h = int.from_bytes(head[27:30], "little") + 1
            return w, h
        if chunk == b"VP8L":
            b = head[21:25]
            w = 1 + (((b[1] & 0x3F) << 8) | b[0])
            h = 1 + (((b[3] & 0x0F) << 10) | (b[2] << 2) | ((b[1] & 0xC0) >> 6))
            return w, h
        if chunk == b"VP8 ":
            w, h = struct.unpack("<HH", head[26:30])
            return w & 0x3FFF, h & 0x3FFF
    return None


# ------------------------------------------------------------- the pack ---

def _json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _families(pack):
    path = pack / "blueprint.json"
    return (_json(path).get("families") or {}) if path.is_file() else {}


def _family_field(families, name, field, seen=None):
    seen = seen or set()
    if name in seen or name not in families:
        return None
    seen.add(name)
    spec = families[name] or {}
    value = (spec.get("defaults") or {}).get(field)
    if value is not None:
        return value
    parent = spec.get("extends")
    return _family_field(families, parent, field, seen) if parent else None


def _sections(pack):
    out = {}
    for path in sorted((pack / "sections").glob("*.json")):
        out[path.stem] = _json(path)
    return out


def _regions(pack):
    """(region name, its folder, its contract) for every act region."""
    out = []
    for contract in sorted((pack / "acts").glob("*/*/contract.json")):
        out.append((contract.parent.name, contract.parent, _json(contract)))
    return out


def _speakers(pack):
    ids = set()
    for act in sorted((pack / "acts").glob("*/world.json")):
        ids.update((_json(act).get("speakers") or {}).keys())
    return ids


def _sheet(pack, rel):
    """Frame info for an animated sprite: sprites/NAME.webp animates from sprites/NAME.sheet.json."""
    path = (pack / rel).with_suffix(".sheet.json")
    if not path.is_file():
        return None
    spec = _json(path)
    img = pack / "sprites" / spec.get("image", "")
    size = image_size(img)
    fw, fh = spec.get("frame", [0, 0])
    used = 0
    for anims in (spec.get("directions") or {}).values():
        for frames in anims.values():
            used = max([used] + [f + 1 for f in frames])
    have = (size[0] // fw) * (size[1] // fh) if size and fw and fh else 0
    return {"image": spec.get("image"), "frame": [fw, fh], "frames_drawn": have,
            "frames_used": used, "image_found": size is not None,
            "anims": sorted({a for d in (spec.get("directions") or {}).values() for a in d})}


def audit(pack=PACK, slots=None):
    """Every art slot the pack reads, plus problems. Returns a dict."""
    pack = Path(pack)
    world = _json(pack / "world.json")
    player = world.get("player") or {}
    sprites = player.get("sprites") or {}
    scale = player.get("sprite_scale") or {}
    families = _families(pack)
    sections = _sections(pack)
    speakers = _speakers(pack)
    status = (slots or {}).get("status") or {}

    rows = {}
    missing, shared, notes = [], [], []
    used_files = set()

    def add(slot, kind, rel, used_by):
        row = rows.get(slot)
        if row is None:
            path = pack / rel if rel else None
            size = image_size(path) if path and path.is_file() else None
            row = rows[slot] = {"slot": slot, "kind": kind, "file": rel, "size": list(size) if size else None,
                                "used_by": [], "status": status.get(slot, {}).get("status", "shipped")}
            if status.get(slot, {}).get("note"):
                row["note"] = status[slot]["note"]
            if rel:
                used_files.add(rel)
            if rel and size is None:
                missing.append(f"{slot}: file {rel} is missing (used by {used_by})")
        if used_by not in row["used_by"]:
            row["used_by"].append(used_by)
        return row

    # Who uses each sprite key decides what kind of picture it is.
    sprite_users = {}
    for iid, item in (world.get("items") or {}).items():
        sprite_users.setdefault(item.get("sprite"), []).append(("item", f"items.{iid}"))
    for fam in families:
        sprite = _family_field(families, fam, "sprite")
        boss = _family_field(families, fam, "sight") == 0
        sprite_users.setdefault(sprite, []).append(("boss" if boss else "mob", f"blueprint.{fam}"))
    for sid in speakers:
        sprite_users.setdefault(sid, []).append(("person", f"speakers.{sid}"))
    sprite_users.setdefault("hero", []).append(("person", "the hero"))

    for key, users in sorted(sprite_users.items(), key=lambda kv: str(kv[0])):
        if not key:
            for _, who in users:
                missing.append(f"{who}: names no sprite")
            continue
        kinds = {k for k, _ in users}
        kind = "person" if "person" in kinds else "item" if "item" in kinds else "mob" if "mob" in kinds else "boss"
        rel = sprites.get(key)
        if rel is None:
            for _, who in users:
                missing.append(f"{who}: sprite {key!r} is not in player.sprites (the game draws a fallback dot)")
            continue
        for _, who in users:
            row = add(f"sprite:{key}", kind, rel, who)
        sheet = _sheet(pack, rel)
        if sheet:
            row["sheet"] = sheet
            used_files.add(str(Path(rel).with_suffix(".sheet.json")))
            used_files.add(f"sprites/{sheet['image']}")
            if not sheet["image_found"]:
                missing.append(f"sprite:{key}: sheet image sprites/{sheet['image']} is missing")
            elif sheet["frames_used"] > sheet["frames_drawn"]:
                missing.append(f"sprite:{key}: sheet uses frame {sheet['frames_used'] - 1}, "
                               f"but the image holds {sheet['frames_drawn']}")
        if key in scale:
            row["scale"] = scale[key]
        # Two different creatures in one picture: fine for a variant, a gap for a warden.
        fams = [who for k, who in users if k in ("mob", "boss")]
        if len(fams) > 1:
            shared.append(f"sprite:{key} is worn by {len(fams)} families: " + ", ".join(w.split('.', 1)[1] for w in fams))

    # Sprite keys nobody reads (the player map still ships them).
    for key, rel in sorted(sprites.items()):
        if key not in sprite_users:
            add(f"sprite:{key}", "item", rel, "player.sprites only")
            notes.append(f"sprite:{key} is in player.sprites but no item, family or speaker uses it")

    # Ground tiles and decals of the four Sections.
    for sid, sec in sections.items():
        for ch, tile in (sec.get("tiles") or {}).items():
            rel = f"tiles/{tile}.grid3x3.webp"
            if (pack / rel).is_file():
                add(f"tile:{tile}", "tile", rel, f"sections.{sid}")
            else:
                notes.append(f"tile:{tile} (sections.{sid} '{ch}') has no tiles/{tile}.grid3x3.webp; the engine draws its own")
        for dec in sec.get("decor") or []:
            add(f"decor:{dec['pic']}", "decor", f"props/{dec['pic']}.webp", f"sections.{sid}.decor")

    # Region maps: legend tiles, props, and the door/stair tiles beside them.
    for name, folder, contract in _regions(pack):
        for ch, spec in (contract.get("legend") or {}).items():
            tile = spec.get("tile") if isinstance(spec, dict) else None
            if not tile:
                continue
            local = folder / "tiles" / f"{tile}.grid3x3.webp"
            rel = str(local.relative_to(pack)) if local.is_file() else f"tiles/{tile}.grid3x3.webp"
            add(f"tile:{name}/{tile}", "tile", rel, f"{name}.legend '{ch}'")
        for prop in contract.get("props") or []:
            add(f"prop:{prop['pic']}", "prop", f"props/{prop['pic']}.webp", f"{name}.props")
        for way in sorted((folder / "tiles").glob("way-*.webp")):
            add(f"way:{name}/{way.stem[4:]}", "way", str(way.relative_to(pack)), f"{name} doors and stairs")
    for way in sorted((pack / "tiles").glob("way-*.webp")):
        add(f"way:{way.stem[4:]}", "way", f"tiles/{way.name}", "the descent's doors and stairs")

    if player.get("title_art"):
        add("card:title", "card", player["title_art"], "player.title_art")

    # Files nothing reads. A .png beside the .webp the game reads is the
    # painted original (128 px) kept from before the GBA set; counted, not listed.
    orphans, legacy = [], []
    for folder in ("sprites", "props", "tiles", "assets"):
        for path in sorted((pack / folder).glob("*")):
            rel = f"{folder}/{path.name}"
            if path.suffix not in (".webp", ".png", ".json") or rel in used_files:
                continue
            if path.suffix == ".png" and str(Path(rel).with_suffix(".webp")) in used_files:
                legacy.append(rel)
            else:
                orphans.append(rel)

    return {"pack": str(pack), "slots": sorted(rows.values(), key=lambda r: (r["kind"], r["slot"])),
            "missing": missing, "shared": shared, "notes": notes, "orphans": orphans, "legacy_png": legacy}


# --------------------------------------------------------- the manifest ---

def load_slots(path=MANIFEST_DIR / "slots.json"):
    return _json(Path(path)) if Path(path).is_file() else {"status": {}, "wanted": [], "batches": []}


def check_slots(slots):
    """Plain-language problems with slots.json (empty when it is sound)."""
    problems = []
    ids = set()
    for slot in slots.get("wanted") or []:
        sid = slot.get("id")
        if not sid or sid in ids:
            problems.append(f"wanted slot {sid!r}: missing or repeated id")
        ids.add(sid)
        kind = slot.get("kind")
        if kind not in KINDS:
            problems.append(f"{sid}: unknown kind {kind!r}")
        for field in ("subject", "loop", "native"):
            if not slot.get(field):
                problems.append(f"{sid}: needs {field!r}")
        if slot.get("status", "wanted") not in STATUSES:
            problems.append(f"{sid}: unknown status {slot.get('status')!r}")
        native = slot.get("native")
        if native and not (isinstance(native, list) and len(native) == 2 and all(isinstance(n, int) for n in native)):
            problems.append(f"{sid}: native must be [w, h] in pixels")
    for key, entry in (slots.get("status") or {}).items():
        if entry.get("status") not in STATUSES:
            problems.append(f"status.{key}: unknown status {entry.get('status')!r}")
    by_id = {s.get("id"): s for s in slots.get("wanted") or []}
    for batch in slots.get("batches") or []:
        bid = batch.get("id")
        members = batch.get("slots") or []
        kinds = {by_id[m]["kind"] for m in members if m in by_id}
        for m in members:
            if m not in by_id:
                problems.append(f"batch {bid}: names unknown slot {m!r}")
        if len(kinds) > 1:
            problems.append(f"batch {bid}: mixes kinds {sorted(kinds)}; one kind per sheet")
        if kinds:
            kind = kinds.pop()
            if len(members) > KINDS[kind]["grid_max"] and KINDS[kind]["grid_max"] > 1:
                problems.append(f"batch {bid}: {len(members)} cells; a {kind} sheet holds {KINDS[kind]['grid_max']} at most")
        if batch.get("kind") and batch["kind"] not in KINDS:
            problems.append(f"batch {bid}: unknown kind {batch['kind']!r}")
    return problems


# -------------------------------------------------------------- briefs ---

def _grid(n, kind):
    """Columns x rows for n cells on this kind's sheet."""
    if kind in ("boss", "tile", "way"):
        return (2, 2) if n > 1 else (1, 1)
    if kind == "person":
        return (4, 3)
    cols = 4 if n > 4 else max(1, n)
    rows = (n + cols - 1) // cols
    return cols, max(1, rows)


def _plan(batch, members, kind):
    """The cut plan for this batch's sheet, in process_kit.py's format, or strip heights."""
    cols, rows = _grid(len(members), kind)
    if KINDS[kind]["pipeline"] == "process_kit":
        cells = []
        for slot in members:
            if kind == "tile":
                cells.append(slot["id"])
            else:
                cells.append({"name": slot["id"], "size": slot["native"]})
        cells += [None] * (cols * rows - len(cells))
        key = "ground" if kind == "tile" else "props"
        return {"palette": "palette.json", "tile": 32,
                "sheets": [{"image": f"sheets/{batch['id']}.png", "grid": f"{cols}x{rows}", key: cells}]}
    if KINDS[kind]["pipeline"] == "motion":
        return {"stills": {"image": f"sheets/{batch['id']}.png", "grid": f"{cols}x{rows}",
                           "cells": [s["id"] for s in members] + [None] * (cols * rows - len(members))},
                "strips": {s["id"]: {"image": f"sheets/motion/{s['id']}.png", "frames": 6,
                                     "height": s["native"][1],
                                     "anims": {"idle": [0, 0, 0, 0, 1, 1, 1, 1], "walk": [2, 3],
                                               "attack": [4, 4, 4], "hurt": [5, 5, 5]}}
                           for s in members}}
    if KINDS[kind]["pipeline"] == "person":
        s = members[0]
        return {"image": f"sheets/{batch['id']}.png", "grid": "4x3", "frame": [64, 64], "height": s["native"][1],
                "sheet_json": {"down": {"idle": [0, 0, 0, 0, 1, 1, 1, 1], "talk": [2, 2, 3, 3]},
                               "right": {"idle": [4, 4, 4, 4]}, "up": {"idle": [8, 8, 8, 8]}}}
    return {}


def _cell_lines(members, kind):
    cols, _ = _grid(len(members), kind)
    lines = ["| Cell | Row, column | Slot | Draw | Native size in game |", "|---|---|---|---|---|"]
    for i, s in enumerate(members):
        lines.append(f"| {i + 1} | {i // cols + 1}, {i % cols + 1} | `{s['id']}` | {s['subject']} | "
                     f"{s['native'][0]} x {s['native'][1]} px |")
    return "\n".join(lines)


def _prompt(batch, members, kind):
    spec = KINDS[kind]
    cols, rows = _grid(len(members), kind)
    order = "; ".join(s["subject"] for s in members)
    if kind == "person":
        return (f"Create a 1536 x 1152 pixel-art character sheet of ONE resident: {members[0]['subject']}. "
                f"Exact 4-column by 3-row grid with wide green gutters, the same person at one size in every cell. "
                f"Row 1 faces the viewer: idle, idle breathing (one pixel lower), talking, talking. Row 2 faces right, "
                f"the same four. Row 3 faces away, the same four. {STYLE} Pure #00FF00 background.")
    size = "1536 x 1536"
    return (f"Create a {size} pixel-art sheet of {spec['title']}. Reference 1 defines the exact GBA pixel "
            f"rendering; match it. Pure #00FF00 background. Exact {cols}-column by {rows}-row grid with wide green "
            f"gutters; {spec['cell']}; nothing touching another subject or the image edge. "
            f"Order left-to-right, top row to bottom row: {order}. "
            + ("Leave any remaining cells empty green. " if cols * rows > len(members) else "")
            + STYLE)


def _motion_prompt(slot):
    return ("Game Boy Advance era pixel art sprite strip on a flat pure #00FF00 green background: exactly ONE ROW "
            "of six frames of the exact same creature as the reference image: same face, colours, markings, "
            "proportions and pixel style, the same size in every frame, all six facing the viewer, standing on one "
            "shared ground line, evenly spaced, with green between them and nothing touching the image edges. "
            "Frame 1: idle. Frame 2: idle, breathing (one pixel lower, or its wings, leaves, flame or wisps shifted "
            "a little). Frames 3 and 4: moving toward the viewer, two steps (a hop, a scuttle, a float or a waddle "
            "as suits it). Frame 5: ATTACK, lunging forward toward the viewer, fierce but still cute. Frame 6: HURT, "
            "flinching back, eyes squeezed shut. Crisp hard-edged square pixels, 1-pixel dark warm-brown outline, "
            f"no anti-aliasing, no ground shadow, no text, no frame numbers. The creature: {slot['subject']}.")


def next_round(source=REPO / "art" / "source"):
    """The folder the next round of sheets goes in: one past the highest roundN."""
    nums = [int(m.group(1)) for p in Path(source).glob("round*") if (m := re.match(r"round(\d+)", p.name))]
    return f"art/source/round{max(nums, default=0) + 1}-gba"


def render_brief(batch, slots, template=None):
    """(markdown, plan) for one batch."""
    by_id = {s["id"]: s for s in slots.get("wanted") or []}
    members = [by_id[m] for m in batch["slots"]]
    kind = members[0]["kind"]
    spec = KINDS[kind]
    template = template or (MANIFEST_DIR / "TEMPLATE.md").read_text(encoding="utf-8")
    plan = _plan(batch, members, kind)
    steps = ""
    if spec["pipeline"] == "motion":
        steps = ("\n\n### Step B: one motion strip per creature\n\nAfter step A, crop each creature's cell and pass it "
                 "as the reference for its own strip (one call per creature, 1536 x 512):\n\n"
                 + "\n\n".join(f"**`{s['id']}`**\n\n```text\n{_motion_prompt(s)}\n```" for s in members))
    lands = "\n".join(f"- `{s['id']}` → " + ", ".join(f"`{p.strip().format(id=s['id'])}`"
                                                       for p in spec["lands"].split(","))
                      for s in members)
    wires = "\n".join(f"- `{s['id']}`: " + spec["wire"].format(id=s["id"]) for s in members)
    loops = sorted({str(s["loop"]) for s in members}, key=lambda x: (len(x), x))
    fills = {
        "batch": batch["id"],
        "round": batch.get("round") or slots.get("round") or next_round(),
        "title": batch.get("title") or spec["title"],
        "kind": kind,
        "why": batch.get("why") or "; ".join(dict.fromkeys(s.get("why", "") for s in members if s.get("why"))),
        "loops": ", ".join(f"loop {n}" for n in loops),
        "count": str(len(members)),
        "sheet": spec["sheet"],
        "native": spec["native"],
        "style": STYLE,
        "references": "\n".join(f"{i + 1}. `{r}`" for i, r in enumerate(batch.get("references") or spec["references"])),
        "cells": _cell_lines(members, kind),
        "prompt": _prompt(batch, members, kind),
        "steps": steps,
        "lands": lands,
        "wire": wires,
        "plan": dump(plan),
    }
    text = template
    for key, value in fills.items():
        text = text.replace("{{" + key + "}}", value)
    left = re.findall(r"\{\{\w+\}\}", text)
    if left:
        raise ValueError(f"brief {batch['id']}: unfilled {sorted(set(left))}")
    return text, plan


def write_brief(batch, slots, out=REQUESTS_DIR):
    text, plan = render_brief(batch, slots)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{batch['id']}.md").write_text(text, encoding="utf-8")
    (out / f"{batch['id']}.plan.json").write_text(dump(plan) + "\n", encoding="utf-8")
    return out / f"{batch['id']}.md"


def dump(value, indent=1):
    """JSON with every list of plain values on one line, so a cut plan reads at a glance."""
    text = json.dumps(value, indent=indent)
    return re.sub(r"\[\s*([^\[\]{}]*?)\s*\]",
                  lambda m: "[" + ", ".join(p.strip() for p in m.group(1).split(",")) + "]"
                  if m.group(1).strip() else "[]", text)


# ----------------------------------------------------------------- cli ---

def _print_audit(report):
    counts = {}
    for row in report["slots"]:
        counts.setdefault(row["kind"], {}).setdefault(row["status"], 0)
        counts[row["kind"]][row["status"]] += 1
    print(f"art slots in {report['pack']}: {len(report['slots'])}")
    for kind in sorted(counts):
        parts = ", ".join(f"{n} {s}" for s, n in sorted(counts[kind].items()))
        print(f"  {kind:7s} {parts}")
    for row in report["slots"]:
        if row["status"] != "shipped":
            print(f"  {row['status']:8s} {row['slot']}: {row.get('note', '')}")
    for title, key in (("MISSING (fails)", "missing"), ("shared pictures", "shared"),
                       ("notes", "notes"), ("files nothing reads", "orphans")):
        if report[key]:
            print(f"\n{title}:")
            for line in report[key]:
                print(f"  - {line}")
    if report["legacy_png"]:
        print(f"\n{len(report['legacy_png'])} painted .png originals sit beside the .webp the game reads "
              "(tests/assert_chest_drops.py still looks for them)")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("audit", help="list every art slot the pack reads; fail on a missing picture")
    a.add_argument("--pack", default=str(PACK))
    a.add_argument("--json", action="store_true")
    w = sub.add_parser("wanted", help="list the slots slots.json wants drawn")
    w.add_argument("--kind")
    w.add_argument("--loop")
    b = sub.add_parser("brief", help="write an image-agent brief for a batch")
    b.add_argument("batch", nargs="?")
    b.add_argument("--all", action="store_true")
    b.add_argument("--out", default=str(REQUESTS_DIR))
    args = ap.parse_args(argv)

    slots = load_slots()
    problems = check_slots(slots)
    if problems:
        print("slots.json:", *problems, sep="\n  - ")
        return 1

    if args.cmd == "audit":
        report = audit(args.pack, slots)
        if args.json:
            print(json.dumps(report, indent=1))
        else:
            _print_audit(report)
        if report["missing"]:
            print(f"\nfail: {len(report['missing'])} picture(s) the pack names have no file")
            return 1
        print("\nok: every picture the pack names has a file")
        return 0

    if args.cmd == "wanted":
        for s in slots.get("wanted") or []:
            if args.kind and s["kind"] != args.kind:
                continue
            if args.loop and str(s["loop"]) != str(args.loop):
                continue
            print(f"{s['kind']:7s} {s['id']:28s} loop {s['loop']:>3}  {s['native'][0]}x{s['native'][1]}  {s['subject']}")
        return 0

    batches = {b["id"]: b for b in slots.get("batches") or []}
    chosen = list(batches.values()) if args.all else [batches.get(args.batch)]
    if not args.all and chosen[0] is None:
        print(f"no batch {args.batch!r}; batches: {', '.join(batches)}")
        return 1
    for batch in chosen:
        path = write_brief(batch, slots, args.out)
        print(path.relative_to(REPO) if path.is_relative_to(REPO) else path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
