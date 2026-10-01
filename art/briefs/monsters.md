# Monsters brief

`status: draft` — Rylee picks; nothing here is approved by a machine.
`training: not cleared` — Codex output is game art only until its terms are
read at the source (`art/STYLE.md`, Licensing note).

## Purpose

Four small monsters for the dungeon floors — a cellar rat, a shade, a moth and
a "rustle" (a bush that moves) — drawn so they match the hero and the tiles.

## Size

128 x 128 px (the character and item size). Each one must be itself at that
size: the rat's thin tail and ears, the shade's soft drifting shape, the moth's
wings, the rustle's leaves and two bright eyes. Keep big shapes and few
details. Front-facing three-quarter view, friendly-spooky, never gory.

## Pictures wanted

Four pictures, two batches of two (never one picture per call):

- `monsters_rat_shade` COUNT 2 — picture 1 of 2: a cellar rat (`monsters_rat_shade_v1`).
- `monsters_rat_shade` COUNT 2 — picture 2 of 2: a shade (`monsters_rat_shade_v2`).
- `monsters_moth_rustle` COUNT 2 — picture 1 of 2: a moth (`monsters_moth_rustle_v1`).
- `monsters_moth_rustle` COUNT 2 — picture 2 of 2: a rustle, a low bush that moves (`monsters_moth_rustle_v2`).

A rat is an animal, not a person: **a rat, four legs, a long thin tail, NOT a
person**. Image models sometimes draw an animal as a person (a real lesson from
the bake-off, `art/README.md`, "Animals can come out human"), so the brief says
it plainly. The rustle is a bush, not a person. Nothing is gory.

## References

Pass these two files, in this order:

- `art/source/round3/turn_v1.webp` — the **who/what** one: the hero turnaround, a figure painted in this game's kit at the right scale.
- `art/source/round2/wall_v1.webp` — the **style** one (round 2 sets the look): painted storybook, muted earth tones, soft darker-brown outlines.

## Batches

Two batches of two. Written to run from the repo root; both write into
`art/source/round7/monsters/`:

```sh
art/tools/codex_batch.sh art/source/round7/monsters monsters_rat_shade 2 "two friendly-spooky dungeon monsters, one per image, 128x128 each, front-facing three-quarter view, not gory; image 1 a cellar rat: a rat, four legs, a long thin tail, NOT a person; image 2 a shade: a soft dark drifting figure, not gory; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, plain flat background, no text" art/source/round3/turn_v1.webp art/source/round2/wall_v1.webp
```

```sh
art/tools/codex_batch.sh art/source/round7/monsters monsters_moth_rustle 2 "two friendly-spooky dungeon monsters, one per image, 128x128 each, front-facing three-quarter view, not gory; image 1 a moth: a small fuzzy moth with pale wings; image 2 a rustle: a low bush that moves, a clump of leaves with two bright eyes, a bush and not a person, not gory; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, plain flat background, no text" art/source/round3/turn_v1.webp art/source/round2/wall_v1.webp
```

## After the batch

After the batches, work through the pictures in this order. All commands run
from the repo root.

Cut out and size each monster:

```sh
uv run --offline --with pillow art/tools/process_sprites.py art/source/round7/monsters/monsters_rat_shade_v1.png art/source/round7/monsters/monsters_rat_shade_v1_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round7/monsters/monsters_rat_shade_v2.png art/source/round7/monsters/monsters_rat_shade_v2_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round7/monsters/monsters_moth_rustle_v1.png art/source/round7/monsters/monsters_moth_rustle_v1_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round7/monsters/monsters_moth_rustle_v2.png art/source/round7/monsters/monsters_moth_rustle_v2_cut.png --size 128
```

Check the cut-outs against the art rules:

```sh
uv run --offline --with pillow art/tools/check_sprites.py art/source/round7/monsters/ --size 128
```

Look at them by eye, then in a real room:

```sh
uv run --offline --with pillow art/tools/contact_sheet.py art/source/round7/monsters/sheet.jpg art/source/round7/monsters/monsters_rat_shade_v1_cut.png art/source/round7/monsters/monsters_rat_shade_v2_cut.png art/source/round7/monsters/monsters_moth_rustle_v1_cut.png art/source/round7/monsters/monsters_moth_rustle_v2_cut.png
uv run --offline --with pillow art/tools/mock_room.py art/source/round7/monsters/room.jpg --wall art/source/round2/wall_v1.webp --floor art/source/round2/wood_v1.webp
```
