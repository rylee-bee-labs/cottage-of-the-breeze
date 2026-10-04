# Cellar cast brief: more kinds of ordinary monster

`status: draft` — Rylee picks; nothing is approved by a machine. Codex draws the
pictures; we may ship what we generate, with attribution (`AGENTS.md` art rule).

## Purpose

The cellar has four ordinary monster pictures (rat, shade, moths, rustle) plus the mushroom sprite (round 8, unused). Random floors will pick monsters from per-depth tables, so each depth wants its own cast. Eight new creatures, two batches of four: shallow pests, then deeper things.

## Size

128 x 128 px (ordinary-monster size, cut to 128 px later). Each must read by its silhouette and ONE feature, so keep big simple shapes and few details. Front-facing three-quarter view, friendly-spooky and never gory. Plain teal background, no text.

## Pictures wanted

Two batches of four: shallow pests, then deeper things. Eight new creatures, never one picture per call.

The pictures in a batch come back in any order; identify each by looking, then rename.

**`cast_shallow` COUNT 4 (floors 1-3), four different creatures:**

- **Cellar spider**: a plump, fuzzy, many-legged spider with a dusty cobweb draped like a scarf and two big curious eyes.
- **Crock mimic**: a round clay storage jar with a wide grin, two eyes peeking over the rim and little stubby clay feet.
- **Wick sprite**: a small living candle stub, a flame for hair, melted wax drips for arms, a mischievous smile.
- **Cellar toad**: a squat warty toad wearing a tiny upturned flowerpot as a helmet, calm and heavy-lidded.

**`cast_deep` COUNT 4 (floors 4-6), four different creatures:**

- **Cave cricket**: a big pale cricket with very long curled antennae and a hunched, ready-to-spring pose.
- **Barrel mimic**: a small wooden barrel with iron hoops, slat-plank teeth in a crooked mouth, two glowing eyes in the bung-hole, short wooden legs.
- **Root tangle**: a knot of pale glowing roots shaped loosely like a crouching creature, one bright eye in the middle.
- **Cobweb wraith**: a ragged hooded figure made of grey cobweb, empty hood with two soft glowing eyes, trailing threads instead of feet.

## References

Pass these two files, in this order:

- `art/source/round8/monsters-and-boss/cellar_king_v1.webp` — the **who/what** one: the Cellar King, the world's style anchor.
- `art/source/round8/monsters-and-boss/cellar_dungeon_v3.webp` — the **scale** one: the mushroom creature, for ordinary-monster scale and line weight.

## Batches

Two batches of four. Written to run from the repo root; both write into
`art/source/round12/cast/`:

```sh
art/tools/codex_batch.sh art/source/round12/cast cast_shallow 4 "four friendly-spooky ordinary cellar monsters, one per image, 128x128 each, front-facing three-quarter view, big simple shapes and few details, each reads by its silhouette and ONE feature, never gory; image 1 a plump fuzzy many-legged cellar spider with a dusty cobweb draped like a scarf and two big curious eyes; image 2 a round clay crock mimic jar with a wide grin, two eyes peeking over the rim and little stubby clay feet; image 3 a wick sprite, a small living candle stub with a flame for hair, melted wax-drip arms and a mischievous smile; image 4 a squat warty cellar toad wearing a tiny upturned flowerpot as a helmet, calm and heavy-lidded; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, plain flat teal background, no text" art/source/round8/monsters-and-boss/cellar_king_v1.webp art/source/round8/monsters-and-boss/cellar_dungeon_v3.webp
```

```sh
art/tools/codex_batch.sh art/source/round12/cast cast_deep 4 "four friendly-spooky ordinary cellar monsters, one per image, 128x128 each, front-facing three-quarter view, big simple shapes and few details, each reads by its silhouette and ONE feature, never gory; image 1 a big pale cave cricket with very long curled antennae and a hunched ready-to-spring pose; image 2 a small wooden barrel mimic with iron hoops, slat-plank teeth in a crooked mouth, two glowing eyes in the bung-hole and short wooden legs; image 3 a root tangle, a knot of pale glowing roots shaped loosely like a crouching creature with one bright eye in the middle; image 4 a cobweb wraith, a ragged hooded figure made of grey cobweb with an empty hood, two soft glowing eyes and trailing threads instead of feet; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, plain flat teal background, no text" art/source/round8/monsters-and-boss/cellar_king_v1.webp art/source/round8/monsters-and-boss/cellar_dungeon_v3.webp
```

## After the batch

After the batches, work through the pictures in this order. All commands run
from the repo root. Rename each file first: which saved file is which creature
is decided by looking, not by the order the batch came back in.

Cut out and size each creature to 128 px:

```sh
uv run --offline --with pillow art/tools/process_sprites.py art/source/round12/cast/cast_shallow_v1.png art/source/round12/cast/cast_shallow_v1_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round12/cast/cast_shallow_v2.png art/source/round12/cast/cast_shallow_v2_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round12/cast/cast_shallow_v3.png art/source/round12/cast/cast_shallow_v3_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round12/cast/cast_shallow_v4.png art/source/round12/cast/cast_shallow_v4_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round12/cast/cast_deep_v1.png art/source/round12/cast/cast_deep_v1_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round12/cast/cast_deep_v2.png art/source/round12/cast/cast_deep_v2_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round12/cast/cast_deep_v3.png art/source/round12/cast/cast_deep_v3_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round12/cast/cast_deep_v4.png art/source/round12/cast/cast_deep_v4_cut.png --size 128
```

Check the cut-outs against the art rules:

```sh
uv run --offline --with pillow art/tools/check_sprites.py art/source/round12/cast/ --size 128
```

Look at them by eye, then in a real room:

```sh
uv run --offline --with pillow art/tools/contact_sheet.py art/source/round12/cast/sheet.jpg art/source/round12/cast/cast_shallow_v1_cut.png art/source/round12/cast/cast_shallow_v2_cut.png art/source/round12/cast/cast_shallow_v3_cut.png art/source/round12/cast/cast_shallow_v4_cut.png art/source/round12/cast/cast_deep_v1_cut.png art/source/round12/cast/cast_deep_v2_cut.png art/source/round12/cast/cast_deep_v3_cut.png art/source/round12/cast/cast_deep_v4_cut.png
uv run --offline --with pillow art/tools/mock_room.py art/source/round12/cast/room.jpg --wall art/source/round2/wall_v1.webp --floor art/source/round2/wood_v1.webp
```

Rylee picks; nothing is approved until she says so.
