# Items and containers brief

`status: draft` — Rylee picks; nothing here is approved by a machine.
`training: not cleared` — Codex output is game art only until its terms are
read at the source (`art/STYLE.md`, Licensing note).

## Purpose

The ten small things the hero finds, carries and opens, drawn to the item size
so they read in the bag and on the floor.

## Size

128 x 128 px (the item size). Each object must be itself at that size: a chest's
lid and lock, a jar's mouth, a key's teeth, a scroll's rolled ends. Keep big
shapes and few details. Everything is **one object, centred, on a plain flat
background, transparent-ready** — no ground, no shadow, no border.

## Pictures wanted

Ten pictures across three batches of three, three and four (never one picture
per call):

- `storage` COUNT 3 — picture 1 of 3: a closed chest (`storage_v1`).
- `storage` COUNT 3 — picture 2 of 3: an open chest (`storage_v2`).
- `storage` COUNT 3 — picture 3 of 3: a jar (`storage_v3`).
- `carry` COUNT 3 — picture 1 of 3: a sack (`carry_v1`).
- `carry` COUNT 3 — picture 2 of 3: a barrel (`carry_v2`).
- `carry` COUNT 3 — picture 3 of 3: a key (`carry_v3`).
- `supplies` COUNT 4 — picture 1 of 4: a lantern (`supplies_v1`).
- `supplies` COUNT 4 — picture 2 of 4: a bread loaf (`supplies_v2`).
- `supplies` COUNT 4 — picture 3 of 4: a potion (`supplies_v3`).
- `supplies` COUNT 4 — picture 4 of 4: a scroll (`supplies_v4`).

The full list, in order: chest closed, chest open, jar, sack, barrel, key,
lantern, bread, potion, scroll.

**Rarity is never shown by colour alone** (`art/STYLE.md`, Never): do not paint
a rarity glow or a colour code into an object. A rank, if one is ever needed,
is a glow, a word and a frame shape.

## References

Pass these two files, in this order:

- `art/source/round2/wood_v1.webp` — the **who/what** one: no item proof exists yet, so this stands in as the painted wooden object in this game's kit (material and palette).
- `art/source/round2/wall_v1.webp` — the **style** one (round 2 sets the look): painted storybook, muted earth tones, soft darker-brown outlines.

## Batches

Three batches. Written to run from the repo root; all three write into
`art/source/round7/items-containers/`:

```sh
art/tools/codex_batch.sh art/source/round7/items-containers storage 3 "three separate game items, one object per image, 128x128 each, centred on a plain flat background, transparent-ready, no ground and no shadow and no border; image 1 a closed wooden chest, image 2 an open wooden chest with the lid up, image 3 a clay jar; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, no text" art/source/round2/wood_v1.webp art/source/round2/wall_v1.webp
```

```sh
art/tools/codex_batch.sh art/source/round7/items-containers carry 3 "three separate game items, one object per image, 128x128 each, centred on a plain flat background, transparent-ready, no ground and no shadow and no border; image 1 a tied cloth sack, image 2 a wooden barrel with iron bands, image 3 an iron key; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, no text" art/source/round2/wood_v1.webp art/source/round2/wall_v1.webp
```

```sh
art/tools/codex_batch.sh art/source/round7/items-containers supplies 4 "four separate game items, one object per image, 128x128 each, centred on a plain flat background, transparent-ready, no ground and no shadow and no border; image 1 a small lantern with a warm flame, image 2 a round bread loaf, image 3 a potion bottle of cloudy liquid, image 4 a rolled paper scroll; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, no text" art/source/round2/wood_v1.webp art/source/round2/wall_v1.webp
```

## After the batch

After the batches, work through the pictures in this order. All commands run
from the repo root.

Cut out and size each object:

```sh
uv run --offline --with pillow art/tools/process_sprites.py art/source/round7/items-containers/storage_v1.png art/source/round7/items-containers/storage_v1_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round7/items-containers/storage_v2.png art/source/round7/items-containers/storage_v2_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round7/items-containers/storage_v3.png art/source/round7/items-containers/storage_v3_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round7/items-containers/carry_v1.png art/source/round7/items-containers/carry_v1_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round7/items-containers/carry_v2.png art/source/round7/items-containers/carry_v2_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round7/items-containers/carry_v3.png art/source/round7/items-containers/carry_v3_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round7/items-containers/supplies_v1.png art/source/round7/items-containers/supplies_v1_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round7/items-containers/supplies_v2.png art/source/round7/items-containers/supplies_v2_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round7/items-containers/supplies_v3.png art/source/round7/items-containers/supplies_v3_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round7/items-containers/supplies_v4.png art/source/round7/items-containers/supplies_v4_cut.png --size 128
```

Check the cut-outs against the art rules:

```sh
uv run --offline --with pillow art/tools/check_sprites.py art/source/round7/items-containers/ --size 128
```

Look at them by eye, then in a real room:

```sh
uv run --offline --with pillow art/tools/contact_sheet.py art/source/round7/items-containers/sheet.jpg art/source/round7/items-containers/storage_v1_cut.png art/source/round7/items-containers/storage_v2_cut.png art/source/round7/items-containers/storage_v3_cut.png art/source/round7/items-containers/carry_v1_cut.png art/source/round7/items-containers/carry_v2_cut.png art/source/round7/items-containers/carry_v3_cut.png art/source/round7/items-containers/supplies_v1_cut.png art/source/round7/items-containers/supplies_v2_cut.png art/source/round7/items-containers/supplies_v3_cut.png art/source/round7/items-containers/supplies_v4_cut.png
uv run --offline --with pillow art/tools/mock_room.py art/source/round7/items-containers/room.jpg --wall art/source/round2/wall_v1.webp --floor art/source/round2/wood_v1.webp
```
