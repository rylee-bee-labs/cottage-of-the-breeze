# The master GBA palette (2026-10-14)

`art/palette.json` is the **one** palette for the shipped GBA art set: the colours
the existing pictures already use, plus the blue ramp. It is built, never hand-edited:

```sh
python3 art/tools/make_palette.py            # writes art/palette.json
python3 art/tools/make_palette.py --check    # drift check, exits 1 if the file is not what the tool builds
python3 art/tools/make_palette.py --report   # also prints off-palette colours per picture group
```

Its check line is the summary the coordinator reads:

```
ok: 77 colours in art/palette.json - 67 from the shipped art, 10 in the blue ramp, 0 off-palette in 110 pictures
```

**Where the 67 come from.** Every opaque colour of the pictures that were cut with
the palette lock: `worlds/cottage-of-the-breeze/props/` (42), `tiles/` (11) and the
item and creature sprites (57) — 110 pictures, 67 distinct colours. Those are the
same 67 the round 23 record names (the decal lock, `art/source/round23-gba/RECORD.md`).
Nothing the shipped art uses was dropped, so no picture has to be redrawn to fit
this palette.

## The blue ramp

Rylee's decision (2026-10-14, Project Home, HERO owner decision): **"Widen the
palette with a blue ramp (Recommended)"**. Ten steps around the dusk teal accent
`#3F7E84` that Rylee picked on 2026-09-26, deepest to lightest. Blue is the largest
channel of every step, so each reads as blue beside the storybook greens (`#4B9B5B`,
`#8C9A2B`) and browns (`#803316`) instead of as one more green; the hue turns from
navy to cyan as it lightens, so the ramp runs from water in shadow to lit glass.

| Hex | What it is for |
|---|---|
| `#0D1A26` | deep water in shadow |
| `#15293C` | night water |
| `#1D3A55` | deep blue |
| `#274C6B` | blue, before the teal |
| `#2F6079` | blue-teal |
| `#3F7E84` | dusk teal, the accent |
| `#4A97A0` | pond surface at dusk |
| `#5FB0B8` | a lit window, glow mid |
| `#86CBD1` | the potion glow |
| `#C4E8EA` | glow core, moonlight |

The pond, a lit window and the potion glow are the three things the ramp was widened
for. The ramp is written down in `art/tools/make_palette.py` (`BLUE_RAMP`), which
refuses to build a palette whose ramp is not 8–12 colours or holds a colour blue does
not lead. A ramp colour that the art already uses is listed once, not twice.

## Using it

`art/tools/pixel_downscale.py --palette art/palette.json` snaps every pixel to the
nearest palette colour, so new art is cut straight onto this palette. Base colours are
plain `"#RRGGBB"`; ramp colours carry a name. The file is one palette: there is no
second palette file, and neither worker's private copy is kept.

## What is NOT in it, and why

- **The cast pictures** — `sprites/hero*`, the seven residents and `cat*` (16 pictures)
  were cut before the lock existed and hold **10,860** distinct colours of their own
  (`hero-sheet.webp` alone holds 6,116). Their colours do not enter the palette; a
  palette of 10,900 would be no palette at all. Re-cut them with
  `pixel_downscale.py --palette art/palette.json` and they land on these 77 like every
  other picture. `--report` prints the number until that is done.
- **`assets/title.webp`**, the dusk cottage painting (56,885 colours). It is a
  painting, not GBA pixel art.
- Both workers' palette files (the HERO worker's 64 colours from the approved
  style-test-B sheet, the ITEMS worker's 64 from the shipped art) were never on
  `main` and their branches were not reachable from this worktree, so the 67 shipped
  colours were read back out of the pictures themselves — the same rule the ITEMS
  side used, and a superset of its 64.

Checked: `python3 -m unittest discover -s art/tests -t .` (the suite needs Pillow and
`uv`, per `docs/commands.md`).