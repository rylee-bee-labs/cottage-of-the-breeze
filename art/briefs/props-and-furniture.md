# Props and furniture brief

`status: draft` — Rylee picks; nothing here is approved by a machine.
`training: not cleared` — Codex output is game art only until its terms are
read at the source (`art/STYLE.md`, Licensing note).

## Purpose

Ten things a room is furnished with — a hearth, a table, a bookshelf, a bed, a
window, a door, a plant pot, a chair, a shop sign and a stone well — drawn to
the item size so they read on the floor of a room and in the yard.

## Size

128 x 128 px (the character and item size). One object per picture, centred,
on a plain flat light background, transparent-ready: no ground, no cast
shadow, no border. Each object must be itself at that size — the hearth's fire
mouth, the table's round top, the shelf's rows of book spines, the quilt's
patchwork squares, the curtain folds, the door's planks and handle, the pot's
rim and its plant, the chair's back and legs, the sign's blank board on its
bracket, the well's stone ring and bucket. Keep big shapes and few details.

## Pictures wanted

Ten pictures across three batches of four, four and two (never one picture per
call).

The pictures in a batch come back in any order; identify each by looking, then rename.
`art/tools/codex_batch.sh` saves a batch's pictures in the order
the image files sort, NOT the order requested, so `_v1` is NOT the first item
asked for. Open each saved file, decide what it actually shows, and rename it
before processing. The file names below are the eventual names — which saved
file ends up with which name is not promised.

Batch `furnishings`, COUNT 4 — the set of four:

- A hearth with a small fire in it: a stone fireplace with a small warm fire
  burning in its mouth. At 128 px it has to read as a squat stone block with a
  glowing opening. NOT wanted: text, a border, a ground or cast shadow, a room
  around it. (eventual name `furnishings_v1`)
- A round wooden table: a plain round tabletop on sturdy legs. At 128 px it has
  to read as a round top over a leg base. NOT wanted: text, a border, a ground
  or cast shadow, a cloth or clutter on it. (eventual name `furnishings_v2`)
- A bookshelf full of books: a wooden shelf case packed with books, spines
  out. At 128 px it has to read as a rectangle of shelves with rows of spines.
  NOT wanted: readable titles, text, a border, a ground or cast shadow.
  (eventual name `furnishings_v3`)
- A bed with a patchwork quilt: a small wooden bed with a patchwork quilt over
  it. At 128 px it has to read as a low block with a pillow at one end and
  patch squares over it. NOT wanted: text, a border, a ground or cast shadow, a
  person in it. (eventual name `furnishings_v4`)

Batch `fittings`, COUNT 4 — the set of four (a stool is left over for later;
this batch stays at four):

- A window with curtains: a small window with a pair of curtains hanging at
  its sides. At 128 px it has to read as a bright square framed by two strips
  of cloth. NOT wanted: text, a border frame around the picture, a ground or
  cast shadow, a view of a landscape in it. (eventual name `fittings_v1`)
- A wooden door: a plank door with a handle. At 128 px it has to read as a
  tall rectangle of vertical planks with a handle. NOT wanted: text, letters,
  a number, a border, a ground or cast shadow, a wall around it.
  (eventual name `fittings_v2`)
- A plant pot: a clay pot with a small green plant growing out of it. At 128
  px it has to read as a tapering pot with a few big leaves. NOT wanted: text,
  a border, a ground or cast shadow, a shelf under it. (eventual name
  `fittings_v3`)
- A chair: a plain wooden chair with a back. At 128 px it has to read as a
  seat on four legs with a back rising from it. NOT wanted: text, a border, a
  ground or cast shadow, a cushion. (eventual name `fittings_v4`)

Batch `buildings`, COUNT 2 — the set of two:

- A shop sign, hanging from a bracket: a wooden board hanging from an iron
  bracket, with NO words and NO letters on it — the board is blank; no text is
  not wanted. At 128 px it has to read as a bracket arm with a board hanging
  under it. NOT wanted: any words, letters or symbols on the board, a border,
  a ground or cast shadow, a wall behind it. (eventual name `buildings_v1`)
- A stone well with a bucket on it: a round stone well ring with a bucket
  resting on its edge. At 128 px it has to read as a low stone ring with a
  bucket over it. NOT wanted: text, a border, a ground or cast shadow, a roof
  frame of any kind. (eventual name `buildings_v2`)

## References

Pass these three files, in this order:

- `art/source/round7/items-containers/storage_v1.webp` — the **who/what** one:
  the item style anchor, a painted object in this game's kit (material and
  palette); the furniture belongs to the same shelf of things.
- `art/source/round2/wood_v1.webp` — the **style** one (round 2 sets the look):
  painted storybook, muted earth tones, soft darker-brown outlines; most of
  this batch is wooden.
- `art/source/round2/wall_v1.webp` — a **surface** reference only: the wall and
  floor the pieces will stand against in `mock_room.py`, for tone.

## Batches

Three batches of four, four and two. Written to run from the repo root; all
three write into `art/source/round8/props-and-furniture/`:

```sh
art/tools/codex_batch.sh art/source/round8/props-and-furniture furnishings 4 "four separate pieces of furniture, one object per image, 128x128 each, centred on a plain flat light background, transparent-ready, no ground and no cast shadow and no border, big shapes and few details; image 1 a stone hearth with a small fire burning in it, image 2 a round wooden table with sturdy legs, image 3 a wooden bookshelf full of books with the spines out, image 4 a wooden bed with a patchwork quilt; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, no text, never anything from Castle of the Winds" art/source/round7/items-containers/storage_v1.webp art/source/round2/wood_v1.webp art/source/round2/wall_v1.webp
```

```sh
art/tools/codex_batch.sh art/source/round8/props-and-furniture fittings 4 "four separate pieces of room fittings, one object per image, 128x128 each, centred on a plain flat light background, transparent-ready, no ground and no cast shadow and no border, big shapes and few details; image 1 a small window with a pair of curtains at its sides, image 2 a plank wooden door with a handle, image 3 a clay plant pot with a small green plant, image 4 a plain wooden chair with a back; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, no text, never anything from Castle of the Winds" art/source/round7/items-containers/storage_v1.webp art/source/round2/wood_v1.webp art/source/round2/wall_v1.webp
```

```sh
art/tools/codex_batch.sh art/source/round8/props-and-furniture buildings 2 "two separate outdoor props, one object per image, 128x128 each, centred on a plain flat light background, transparent-ready, no ground and no cast shadow and no border, big shapes and few details; image 1 a wooden shop sign hanging from an iron bracket, the board completely blank with no words and no letters and no symbols on it, image 2 a round stone well with a bucket resting on its edge; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, no text, never anything from Castle of the Winds" art/source/round7/items-containers/storage_v1.webp art/source/round2/wood_v1.webp art/source/round2/wall_v1.webp
```

## After the batch

After the batches, work through the pictures in this order. All commands run
from the repo root. Rename each file first — the names below are the eventual
names, and which picture got which name is decided by looking, not by the order
the batch came back in.

Cut out and size each object:

```sh
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/props-and-furniture/furnishings_v1.png art/source/round8/props-and-furniture/furnishings_v1_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/props-and-furniture/furnishings_v2.png art/source/round8/props-and-furniture/furnishings_v2_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/props-and-furniture/furnishings_v3.png art/source/round8/props-and-furniture/furnishings_v3_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/props-and-furniture/furnishings_v4.png art/source/round8/props-and-furniture/furnishings_v4_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/props-and-furniture/fittings_v1.png art/source/round8/props-and-furniture/fittings_v1_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/props-and-furniture/fittings_v2.png art/source/round8/props-and-furniture/fittings_v2_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/props-and-furniture/fittings_v3.png art/source/round8/props-and-furniture/fittings_v3_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/props-and-furniture/fittings_v4.png art/source/round8/props-and-furniture/fittings_v4_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/props-and-furniture/buildings_v1.png art/source/round8/props-and-furniture/buildings_v1_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/props-and-furniture/buildings_v2.png art/source/round8/props-and-furniture/buildings_v2_cut.png --size 128
```

Check the cut-outs against the art rules:

```sh
uv run --offline --with pillow art/tools/check_sprites.py art/source/round8/props-and-furniture/ --size 128
```

Look at them by eye, listing the cut files so each one is labelled, then in a
real room:

```sh
uv run --offline --with pillow art/tools/contact_sheet.py art/source/round8/props-and-furniture/sheet.jpg art/source/round8/props-and-furniture/furnishings_v1_cut.png art/source/round8/props-and-furniture/furnishings_v2_cut.png art/source/round8/props-and-furniture/furnishings_v3_cut.png art/source/round8/props-and-furniture/furnishings_v4_cut.png art/source/round8/props-and-furniture/fittings_v1_cut.png art/source/round8/props-and-furniture/fittings_v2_cut.png art/source/round8/props-and-furniture/fittings_v3_cut.png art/source/round8/props-and-furniture/fittings_v4_cut.png art/source/round8/props-and-furniture/buildings_v1_cut.png art/source/round8/props-and-furniture/buildings_v2_cut.png
uv run --offline --with pillow art/tools/mock_room.py art/source/round8/props-and-furniture/room.jpg --wall art/source/round2/wall_v1.webp --floor art/source/round2/wood_v1.webp
```

`mock_room.py` builds the room from the round 2 wall and floor (96 px tiles);
check the 128 px pieces against that scale by eye. Rylee picks; nothing is
approved until she says so.
