# Hero walk-sheet brief

`status: draft` — Rylee picks; nothing here is approved by a machine.
`training: not cleared` — Codex output is game art only until its terms are
read at the source (`art/STYLE.md`, Licensing note).

## Purpose

A 4 x 4 walk sheet of the same hero, so `process_sprites.py --grid 4x4` can cut
sixteen usable frames for the engine.

## Size

512 x 512 px: a 4 x 4 grid of 128 x 128 px cells. Every cell must read at
128 px as the same character — same green hooded cloak, same red braids, same
bow, same proportions, same scale and baseline. Nothing may touch the cell
edges, and the background stays flat and plain so the grid cut works.

Rows run down the sheet, in this order: row 1 faces down, row 2 faces left,
row 3 faces right, row 4 faces up. Four walk frames per row (contact, passing,
contact, passing).

## Pictures wanted

Two sheets, one batch of two (two variations of the same hero sheet; never one
picture per call):

The pictures in a batch come back in any order; identify each by looking, then rename.

`hero_walk_v1` is not the first item asked for: `codex_batch.sh` saves a batch's pictures in the order the image files sort, not the order requested, so a `hero_walk_v1` file may hold either of the two sheets asked for.

- `hero_walk` COUNT 2 — picture 1 of 2: `hero_walk_v1.png`, a 4 x 4 sheet (512x512), rows down/left/right/up, four walk frames per row.
- `hero_walk` COUNT 2 — picture 2 of 2: `hero_walk_v2.png`, a second variation of the same sheet.

## References

Pass these files, in this order:

- `art/source/round3/turn_v1.webp` — the **who/what** one: the SAME hero (the chibi archer with the red braids and the green hooded cloak and the bow). She stays the same character, redrawn in this style.
- `art/source/round2/wall_v1.webp` — the **style** one (round 2 sets the look): painted storybook, muted earth tones, soft darker-brown outlines.
- `art/source/round3/walk_v1.webp` — a **pose** reference only: the existing four-frame right-facing walk. Use the pose feel; the layout is the 4 x 4 grid in the brief, not a single row.

## Batches

One batch, two sheets. Written to run from the repo root; it writes into
`art/source/round7/hero-walk/`:

```sh
art/tools/codex_batch.sh art/source/round7/hero-walk hero_walk 2 "one character sheet, 512x512, a 4 by 4 grid of 128x128 cells, on a flat plain background so a 4x4 grid cut works; the SAME hero as the first attached image: a chibi archer with red hair in two braids, a green hooded cloak, brown boots and a wooden bow, redrawn in the painted storybook style of the second attached image; rows down the sheet in this order: row 1 facing down, row 2 facing left, row 3 facing right, row 4 facing up; four walk frames per row, contact then passing then contact then passing; identical outfit, proportions, scale and baseline in every one of the 16 cells, each cell 128x128; plain flat background, no text, no ground shadow; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light" art/source/round3/turn_v1.webp art/source/round2/wall_v1.webp art/source/round3/walk_v1.webp
```

## After the batch

After the batch, work through the sheets in this order. All commands run from
the repo root.

Cut each sheet into sixteen frames (rows named down, left, right, up):

```sh
uv run --offline --with pillow art/tools/process_sprites.py --grid 4x4 art/source/round7/hero-walk/hero_walk_v1.png art/source/round7/hero-walk/cut hero --size 128 --names down,left,right,up
uv run --offline --with pillow art/tools/process_sprites.py --grid 4x4 art/source/round7/hero-walk/hero_walk_v2.png art/source/round7/hero-walk/cut2 hero2 --size 128 --names down,left,right,up
```

Check the frames against the art rules:

```sh
uv run --offline --with pillow art/tools/check_sprites.py art/source/round7/hero-walk/cut art/source/round7/hero-walk/cut2 --size 128
```

Look at the frames by eye, then in a real room:

```sh
uv run --offline --with pillow art/tools/contact_sheet.py art/source/round7/hero-walk/frames.jpg art/source/round7/hero-walk/cut/*.png --cols 4
uv run --offline --with pillow art/tools/mock_room.py art/source/round7/hero-walk/room.jpg --wall art/source/round2/wall_v1.webp --floor art/source/round2/wood_v1.webp
```

`mock_room.py` shows the room she moves in (96 px tiles); check her 128 px
frames against that scale by eye. Once Rylee picks a sheet, keep the other one
as the variant.
