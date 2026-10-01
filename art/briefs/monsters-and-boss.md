# Monsters and boss brief

`status: draft` — Rylee picks; nothing here is approved by a machine.
`training: not cleared` — Codex output is game art only until its terms are
read at the source (`art/STYLE.md`, Licensing note).

## Purpose

Five dungeon creatures for the cellar floors — a swarm of tiny shade moths, a
big leafy rustle, a mushroom sprite, and the boss: the Cellar King, drawn
twice — so they match the hero and the round 7 monsters.

## Size

128 x 128 px (the character size) for the three ordinary monsters. Each one
must be itself at that size: the swarm's small scattered wings, the rustle's
leaves and two bright eyes, the mushroom's cap over its stem. Front-facing
three-quarter view, friendly-spooky, never gory. Keep big shapes and few
details.

The boss gets its own paragraph because it is drawn larger: the Cellar King is
256 x 256 px, twice the ordinary monster, so it sits over them on the screen.
It keeps the same front-facing three-quarter view, the same friendly-spooky
feeling and the same never-gory rule, with big shapes and few details. At
256 px what has to read is the bottle-cap crown, the round heavy body, the four
legs, the long thin tail and the face.

## Pictures wanted

Two batches: three monsters, then two (one of which is the boss). Five
pictures, never one picture per call.

The pictures in a batch come back in any order; identify each by looking, then rename.
`art/tools/codex_batch.sh` saves a batch's pictures in the order
the image files sort, NOT the order requested, so `_v1` is NOT the first item
asked for. Open each saved file, decide what it actually shows, and rename it
before processing. The file names below are the eventual names — which saved
file ends up with which name is not promised.

Batch `cellar_dungeon`, COUNT 3 — the set of three:

- A swarm of tiny shade moths: a few small moths grouped together, not one big
  moth. At 128 px it has to read as a scatter of small wings with a few dim
  bright eyes. NOT wanted: one giant moth, text, a border, a ground or cast
  shadow, anything gory. (eventual name `cellar_dungeon_v1`)
- A big leafy rustle: a clump of moving leaves with two bright eyes, noticeably
  BIGGER than the round 7 rustle in
  `art/source/round7/monsters/monsters_moth_rustle_v2.webp` — it should fill
  more of its square than that one does. At 128 px it has to read as one big
  leafy mass with two bright eyes in it. NOT wanted: a person, text, a border,
  a ground or cast shadow, anything gory. (eventual name `cellar_dungeon_v2`)
- A mushroom sprite: a small standing mushroom with a cap, a stubby stem and a
  friendly-spooky face. At 128 px it has to read as a clear cap-over-stem
  silhouette. NOT wanted: a person in a costume, text, a border, a ground or
  cast shadow, anything gory. (eventual name `cellar_dungeon_v3`)

Batch `cellar_king`, COUNT 2 — the set of two. Both pictures in this batch are
the SAME boss, the Cellar King, so identify them by looking, not by number.

- The Cellar King: a plump rat wearing a bottle-cap crown, friendly-spooky at
  256 x 256 px. Still an animal: four legs, a long thin tail, NOT a person —
  the bake-off lesson from `art/README.md`, "Animals can come out human", said
  here plainly because image models do it. At 256 px it has to read as a round
  heavy body under a crown, with four legs and a long thin tail. NOT wanted: a
  person, text, a border, a ground or cast shadow, anything gory. (eventual
  name `cellar_king_v1`)
- A second variation of the Cellar King: the same boss drawn again, a second
  take on the same creature — same crown, same animal body, different pose or
  weight. At 256 px it has to read as the same boss as the first picture. NOT
  wanted: a different creature, a person, text, a border, a ground or cast
  shadow, anything gory. (eventual name `cellar_king_v2`)

## References

Pass these two files, in this order:

- `art/source/round7/monsters/monsters_moth_rustle_v2.webp` — the **who/what**
  one: this game's monsters, painted in this game's kit at the right scale; the
  new rustle must be noticeably bigger than the rustle in this picture.
- `art/source/round2/wall_v1.webp` — the **style** one (round 2 sets the look):
  painted storybook, muted earth tones, soft darker-brown outlines.

## Batches

Two batches of three and two. Written to run from the repo root; both write
into `art/source/round8/monsters-and-boss/`:

```sh
art/tools/codex_batch.sh art/source/round8/monsters-and-boss cellar_dungeon 3 "three friendly-spooky dungeon monsters, one per image, 128x128 each, front-facing three-quarter view, big shapes and few details, never gory; image 1 a swarm of tiny shade moths: a few small moths grouped together, not one big moth; image 2 a big leafy rustle: a clump of moving leaves with two bright eyes, noticeably bigger than the rustle in the attached monster picture, a bush and not a person; image 3 a mushroom sprite: a small standing mushroom with a cap, a stubby stem and a friendly face; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, plain flat background, no text, never anything from Castle of the Winds" art/source/round7/monsters/monsters_moth_rustle_v2.webp art/source/round2/wall_v1.webp
```

```sh
art/tools/codex_batch.sh art/source/round8/monsters-and-boss cellar_king 2 "two pictures of the same boss, one per image, 256x256 each, drawn larger than an ordinary monster; the Cellar King: a plump rat wearing a bottle-cap crown, friendly-spooky, still an animal with four legs and a long thin tail, NOT a person, big shapes and few details, never gory; image 1 one take on this boss, image 2 a second variation of the SAME boss; front-facing three-quarter view; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, plain flat background, no text, never anything from Castle of the Winds" art/source/round7/monsters/monsters_moth_rustle_v2.webp art/source/round2/wall_v1.webp
```

## After the batch

After the batches, work through the pictures in this order. All commands run
from the repo root. Rename each file first — the names below are the eventual
names, and which picture got which name is decided by looking, not by the order
the batch came back in.

Cut out and size each picture — `--size 128` for the three monsters, `--size
256` for the king, each written beside its source with a `_cut` suffix:

```sh
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/monsters-and-boss/cellar_dungeon_v1.png art/source/round8/monsters-and-boss/cellar_dungeon_v1_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/monsters-and-boss/cellar_dungeon_v2.png art/source/round8/monsters-and-boss/cellar_dungeon_v2_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/monsters-and-boss/cellar_dungeon_v3.png art/source/round8/monsters-and-boss/cellar_dungeon_v3_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/monsters-and-boss/cellar_king_v1.png art/source/round8/monsters-and-boss/cellar_king_v1_cut.png --size 256
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/monsters-and-boss/cellar_king_v2.png art/source/round8/monsters-and-boss/cellar_king_v2_cut.png --size 256
```

Check the cut-outs against the art rules, over the directory at the monster
size, then over the king at its own size (the directory run is one size for
everything, so it calls the two king files the wrong size on purpose):

```sh
uv run --offline --with pillow art/tools/check_sprites.py art/source/round8/monsters-and-boss/ --size 128
uv run --offline --with pillow art/tools/check_sprites.py art/source/round8/monsters-and-boss/cellar_king_v1_cut.png art/source/round8/monsters-and-boss/cellar_king_v2_cut.png --size 256
```

Look at them by eye, then in a real room:

```sh
uv run --offline --with pillow art/tools/contact_sheet.py art/source/round8/monsters-and-boss/sheet.jpg art/source/round8/monsters-and-boss/cellar_dungeon_v1_cut.png art/source/round8/monsters-and-boss/cellar_dungeon_v2_cut.png art/source/round8/monsters-and-boss/cellar_dungeon_v3_cut.png art/source/round8/monsters-and-boss/cellar_king_v1_cut.png art/source/round8/monsters-and-boss/cellar_king_v2_cut.png
uv run --offline --with pillow art/tools/mock_room.py art/source/round8/monsters-and-boss/room.jpg --wall art/source/round2/wall_v1.webp --floor art/source/round2/wood_v1.webp
```

`mock_room.py` shows the room they stand in (96 px tiles); check the 128 px
monsters and the 256 px king against that scale by eye. Rylee picks; nothing is
approved until she says so.
