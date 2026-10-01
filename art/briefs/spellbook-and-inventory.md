# Spellbook and inventory brief

`status: draft` — Rylee picks; nothing here is approved by a machine.
`training: not cleared` — Codex output is game art only until its terms are
read at the source (`art/STYLE.md`, Licensing note).

## Purpose

Sixteen things the hero carries, reads and wears — the spellbook and its runes,
trinkets, gear and clothes — drawn to the item size so each one reads alone in
the bag, in a slot and on the floor.

## Size

128 x 128 px (the item size). One object per picture, centred, on a plain flat
light background, transparent-ready: no ground, no cast shadow, no border, no
text. Each object must be itself at that size — the closed book's clasps, the
open book's glowing runes, the quill's nib in the inkpot, the rune stone's cut
marks, the ring's band, the amulet's cord, the purse's mouth with coins
spilling, the bow's curve, the dagger's edge, the shield's boss, the boots'
tops, the cloak's hood, the cap's brim, the gem's facets, the flask's cork and
its cloudy liquid. Keep big shapes and few details.

**Rarity is never shown by colour alone** (`art/STYLE.md`, Never): do not paint
a rarity glow or a colour code into an object. A rank, if one is ever needed,
is a glow, a word and a frame shape — three things together, never the colour
of the thing itself. A potion and a gem are exactly where this temptation comes
up: a green flask or a bright stone must stay a plain painted object, not a
signal of how good it is.

## Pictures wanted

Sixteen pictures across four batches of four (never one picture per call).

The pictures in a batch come back in any order; identify each by looking, then rename.
`art/tools/codex_batch.sh` saves a batch's pictures in the order
the image files sort, NOT the order requested, so `_v1` is NOT the first item
asked for. Open each saved file, decide what it actually shows, and rename it
before processing. The file names below are the eventual names — which saved
file ends up with which name is not promised.

Batch `spellbook`, COUNT 4 — the set of four:

- A closed spellbook: a closed book with a heavy cover and straps. At 128 px
  it has to read as a solid rectangle with a spine and a clasp. NOT wanted:
  text or letters on the cover, a border, a ground or cast shadow, a rarity
  glow. (eventual name `spellbook_v1`)
- A spellbook open showing glowing runes: the same kind of book lying open,
  with abstract glowing rune marks on its pages. At 128 px it has to read as
  two open pages with light in the middle. NOT wanted: readable words or
  letters — the runes are marks, not text — a border, a ground or cast shadow,
  a rarity glow. (eventual name `spellbook_v2`)
- A quill in an inkpot: a feather quill standing in a small inkpot. At 128 px
  it has to read as a tall feather over a squat pot. NOT wanted: any written
  marks, a border, a ground or cast shadow. (eventual name `spellbook_v3`)
- A rune stone: a flat stone with cut rune marks on its face. At 128 px it has
  to read as a rounded stone with a few deep marks. NOT wanted: readable words
  or letters, a border, a ground or cast shadow, a rarity glow.
  (eventual name `spellbook_v4`)

Batch `trinkets`, COUNT 4 — the set of four:

- A wooden staff: a tall straight wooden staff with a knob at its top. At 128
  px it has to read as one long vertical shaft with a head. NOT wanted: text,
  a border, a ground or cast shadow, a rarity glow. (eventual name
  `trinkets_v1`)
- A ring: a simple ring with a small setting. At 128 px it has to read as a
  clear circle with a bump on top. NOT wanted: text, a border, a ground or
  cast shadow, a rarity glow signalled by its colour. (eventual name
  `trinkets_v2`)
- An amulet on a cord: a pendant hanging from a cord. At 128 px it has to read
  as a loop of cord with a weight at the bottom. NOT wanted: text, a border, a
  ground or cast shadow, a rarity glow. (eventual name `trinkets_v3`)
- A coin purse with coins spilling at its mouth: a soft purse with a few coins
  spilling out of its mouth. At 128 px it has to read as a round bag with a
  small scatter of round coins. NOT wanted: text or stamps on the coins, a
  border, a ground or cast shadow, a rarity glow. (eventual name
  `trinkets_v4`)

Batch `gear`, COUNT 4 — the set of four:

- A short bow: a short curved bow with a string. At 128 px it has to read as a
  clean curve with a thin line across it. NOT wanted: text, a border, a ground
  or cast shadow, a rarity glow. (eventual name `gear_v1`)
- A dagger: a short blade with a guard and a grip. At 128 px it has to read
  as a wide blade over a short handle. NOT wanted: text or runes on the blade,
  a border, a ground or cast shadow, blood, a rarity glow. (eventual name
  `gear_v2`)
- A round shield: a round shield with a boss in the middle. At 128 px it has
  to read as a plain circle with a bump at its centre. NOT wanted: text or
  letters on the face, a border, a ground or cast shadow, a rarity glow.
  (eventual name `gear_v3`)
- A pair of boots: two boots side by side. At 128 px it has to read as two
  matching shapes with flat soles. NOT wanted: text, a border, a ground or
  cast shadow, a rarity glow. (eventual name `gear_v4`)

Batch `clothes`, COUNT 4 — the set of four:

- A green hooded cloak: the hero's own green hooded cloak, hanging open with
  its hood up. At 128 px it has to read as a draped green shape with a hood at
  the top. NOT wanted: a person wearing it, text, a border, a ground or cast
  shadow, a rarity glow. (eventual name `clothes_v1`)
- A leather cap: a soft leather cap with a small brim. At 128 px it has to
  read as a rounded dome with a brim. NOT wanted: text, a border, a ground or
  cast shadow, a rarity glow. (eventual name `clothes_v2`)
- A gem: a cut gem with a few big facets. At 128 px it has to read as a small
  solid shape with two or three facet planes. NOT wanted: a rarity glow or any
  colour code on it — it is a painted stone, and its colour says nothing about
  its rank — text, a border, a ground or cast shadow. (eventual name
  `clothes_v3`)
- A health potion: a round flask with a cork and cloudy green liquid. At 128
  px it has to read as a round body, a narrow neck and a cork. NOT wanted: a
  rarity glow or a colour code — the green is the liquid, not a rank — text or
  a label, a border, a ground or cast shadow. (eventual name `clothes_v4`)

The full list, in order asked: spellbook closed, spellbook open with runes,
quill in inkpot, rune stone, staff, ring, amulet, coin purse, short bow,
dagger, round shield, pair of boots, green hooded cloak, leather cap, gem,
health potion.

## References

Pass these two files, in this order:

- `art/source/round7/items-containers/storage_v1.webp` — the **who/what** one:
  the item style anchor, painted objects in this game's kit at the right scale
  (material and palette).
- `art/source/round2/wall_v1.webp` — the **style** one (round 2 sets the look):
  painted storybook, muted earth tones, soft darker-brown outlines.

## Batches

Four batches of four. Written to run from the repo root; all four write into
`art/source/round8/spellbook-and-inventory/`:

```sh
art/tools/codex_batch.sh art/source/round8/spellbook-and-inventory spellbook 4 "four separate spellbook items, one object per image, 128x128 each, centred on a plain flat light background, transparent-ready, no ground and no cast shadow and no border, no text, big shapes and few details; image 1 a closed spellbook with a heavy cover and straps, image 2 the same kind of spellbook lying open with abstract glowing rune marks on its pages, marks and never readable letters, image 3 a feather quill standing in a small inkpot, image 4 a flat stone with cut rune marks on its face; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, no rarity glow and no colour-coded rarity, never anything from Castle of the Winds" art/source/round7/items-containers/storage_v1.webp art/source/round2/wall_v1.webp
```

```sh
art/tools/codex_batch.sh art/source/round8/spellbook-and-inventory trinkets 4 "four separate trinkets, one object per image, 128x128 each, centred on a plain flat light background, transparent-ready, no ground and no cast shadow and no border, no text, big shapes and few details; image 1 a tall straight wooden staff with a knob at its top, image 2 a simple ring with a small setting, image 3 a pendant hanging from a cord, image 4 a soft coin purse with a few coins spilling out of its mouth; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, no rarity glow and no colour-coded rarity, never anything from Castle of the Winds" art/source/round7/items-containers/storage_v1.webp art/source/round2/wall_v1.webp
```

```sh
art/tools/codex_batch.sh art/source/round8/spellbook-and-inventory gear 4 "four separate pieces of adventuring gear, one object per image, 128x128 each, centred on a plain flat light background, transparent-ready, no ground and no cast shadow and no border, no text, big shapes and few details; image 1 a short curved bow with a string, image 2 a dagger with a short blade, a guard and a grip, image 3 a round shield with a boss in the middle, image 4 a pair of boots standing side by side; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, no rarity glow and no colour-coded rarity, never anything from Castle of the Winds" art/source/round7/items-containers/storage_v1.webp art/source/round2/wall_v1.webp
```

```sh
art/tools/codex_batch.sh art/source/round8/spellbook-and-inventory clothes 4 "four separate pieces of clothing and treasure, one object per image, 128x128 each, centred on a plain flat light background, transparent-ready, no ground and no cast shadow and no border, no text, big shapes and few details; image 1 a green hooded cloak hanging open with its hood up, nobody wearing it, image 2 a soft leather cap with a small brim, image 3 a cut gem with two or three big facets, a plain painted stone with no rarity glow and no colour code, image 4 a health potion: a round flask with a cork and cloudy green liquid, the green is the liquid and not a rarity colour; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, no rarity glow and no colour-coded rarity, never anything from Castle of the Winds" art/source/round7/items-containers/storage_v1.webp art/source/round2/wall_v1.webp
```

## After the batch

After the batches, work through the pictures in this order. All commands run
from the repo root. Rename each file first — the names below are the eventual
names, and which picture got which name is decided by looking, not by the order
the batch came back in.

Cut out and size each object:

```sh
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/spellbook-and-inventory/spellbook_v1.png art/source/round8/spellbook-and-inventory/spellbook_v1_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/spellbook-and-inventory/spellbook_v2.png art/source/round8/spellbook-and-inventory/spellbook_v2_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/spellbook-and-inventory/spellbook_v3.png art/source/round8/spellbook-and-inventory/spellbook_v3_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/spellbook-and-inventory/spellbook_v4.png art/source/round8/spellbook-and-inventory/spellbook_v4_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/spellbook-and-inventory/trinkets_v1.png art/source/round8/spellbook-and-inventory/trinkets_v1_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/spellbook-and-inventory/trinkets_v2.png art/source/round8/spellbook-and-inventory/trinkets_v2_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/spellbook-and-inventory/trinkets_v3.png art/source/round8/spellbook-and-inventory/trinkets_v3_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/spellbook-and-inventory/trinkets_v4.png art/source/round8/spellbook-and-inventory/trinkets_v4_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/spellbook-and-inventory/gear_v1.png art/source/round8/spellbook-and-inventory/gear_v1_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/spellbook-and-inventory/gear_v2.png art/source/round8/spellbook-and-inventory/gear_v2_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/spellbook-and-inventory/gear_v3.png art/source/round8/spellbook-and-inventory/gear_v3_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/spellbook-and-inventory/gear_v4.png art/source/round8/spellbook-and-inventory/gear_v4_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/spellbook-and-inventory/clothes_v1.png art/source/round8/spellbook-and-inventory/clothes_v1_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/spellbook-and-inventory/clothes_v2.png art/source/round8/spellbook-and-inventory/clothes_v2_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/spellbook-and-inventory/clothes_v3.png art/source/round8/spellbook-and-inventory/clothes_v3_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/spellbook-and-inventory/clothes_v4.png art/source/round8/spellbook-and-inventory/clothes_v4_cut.png --size 128
```

Check the cut-outs against the art rules:

```sh
uv run --offline --with pillow art/tools/check_sprites.py art/source/round8/spellbook-and-inventory/ --size 128
```

Look at them by eye, then in a real room:

```sh
uv run --offline --with pillow art/tools/contact_sheet.py art/source/round8/spellbook-and-inventory/sheet.jpg art/source/round8/spellbook-and-inventory/spellbook_v1_cut.png art/source/round8/spellbook-and-inventory/spellbook_v2_cut.png art/source/round8/spellbook-and-inventory/spellbook_v3_cut.png art/source/round8/spellbook-and-inventory/spellbook_v4_cut.png art/source/round8/spellbook-and-inventory/trinkets_v1_cut.png art/source/round8/spellbook-and-inventory/trinkets_v2_cut.png art/source/round8/spellbook-and-inventory/trinkets_v3_cut.png art/source/round8/spellbook-and-inventory/trinkets_v4_cut.png art/source/round8/spellbook-and-inventory/gear_v1_cut.png art/source/round8/spellbook-and-inventory/gear_v2_cut.png art/source/round8/spellbook-and-inventory/gear_v3_cut.png art/source/round8/spellbook-and-inventory/gear_v4_cut.png art/source/round8/spellbook-and-inventory/clothes_v1_cut.png art/source/round8/spellbook-and-inventory/clothes_v2_cut.png art/source/round8/spellbook-and-inventory/clothes_v3_cut.png art/source/round8/spellbook-and-inventory/clothes_v4_cut.png
uv run --offline --with pillow art/tools/mock_room.py art/source/round8/spellbook-and-inventory/room.jpg --wall art/source/round2/wall_v1.webp --floor art/source/round2/wood_v1.webp
```

`mock_room.py` shows the room the bag empties into (96 px tiles); check the
128 px items against that scale by eye. Rylee picks; nothing is approved until
she says so.
