# Gaps brief (round 13): the deep zone, doors, keys, treasure, props

`status: draft` — Rylee picks; nothing here is approved by a machine. Codex
draws the pictures; we may ship what we generate, with attribution (`AGENTS.md`
art rule). Rylee, 2026-10-02: "feel free to do more art passes to fill in gaps too. we have tokens to spend with codex."

## Gaps (found 2026-10-02)

- Floors 4-6 use the engine's flat dungeon colours; floors 1-3 have the authored flagstone. The deep zone wants its own ground and a plainer wall (the engine wall has a lantern on every tile).
- The door art "could use some work" (Rylee); there is no sealed door for the Cellar King.
- Six keys (five guardians and the King's seal) have no pictures; the treasure room has no chest or coins.
- Dungeon decoration is bare: barrels, crates, a sconce, cobwebs, mushrooms, a broken pot, a puddle, roots.

## Size

Ground tiles: 288 x 288 px, a 3 x 3 grid of 96 px cells that tiles by itself. Wall tiles: a front-on 96 px wall tile. Doors and props: 96-128 px game objects on a plain teal background. Items: 128 px icons. No text in any picture.

## Pictures wanted

Nine batches, 2 to 4 pictures each, to fill the gaps found above. Never one picture per call.

The pictures in a batch come back in any order; identify each by looking, then rename.

- `deep_ground` COUNT 3 — Deeper cellar flagstone (damper, darker, moss in the seams); cracked flagstone with thin roots; wet flagstone with a puddle sheen.
- `deep_wall` COUNT 3 — A plain dark cut-stone wall tile with no lanterns; the same mossy; the same with pale roots creeping through.
- `doors` COUNT 4 — A wooden cellar door, iron-banded, arched, closed; the same door open onto darkness; a trapdoor in the floor with an iron ring; the Cellar King's sealed stone door with a crown-shaped wax-and-iron seal in the middle.
- `keys_a` COUNT 3 — The Reeve's heavy iron key; the Bailiff's small brass key with a bell-shaped head; the Warden's glass lantern-key that glows softly.
- `keys_b` COUNT 3 — The Marshal's blunt steel key with a helmet-shaped head; the Seneschal's key sealed in candle wax with a ribbon; the Cellar King's seal, a round wax seal pressed with a crown.
- `treasure` COUNT 4 — A closed wooden treasure chest with brass corners; the same chest open with a warm glow; a small heap of gold coins; a few cut gems (teal, amber, rose) on a scrap of cloth.
- `props_a` COUNT 4 — Two barrels with iron hoops; a stack of crates and grain sacks; a wall torch in an iron sconce, lit; a cobweb in a stone corner.
- `props_b` COUNT 4 — A cluster of glowing cellar mushrooms; a broken clay pot with shards; a small puddle with a dripping drop; a tangle of pale roots pushing through stone.

## Look

Painted storybook, soft darker-brown outlines (never black), muted earth tones with dusk teal `3F7E84` accents. Ground tiles: one continuous flat top-down scene (a 3 x 3 grid of 96 px cells that tiles by itself, no frame, no objects, big shapes only; see `town-surfaces.md`). Wall tiles: a front-on 96 px wall tile. Doors and props: 96-128 px game objects on a plain teal background. Items: 128 px icons in the style of the round 8 and delve item icons. No text in any picture.

## References

Pass these three files, in this order:

- `art/source/round8/town-surfaces/town_ground_v1.webp` — the **who/what** one: the game's authored top-down ground, for the new deep floor and wall.
- `art/source/round9/sentence-items/gems_v1.webp` — the **item** one: a delve item icon in this game's kit, for the keys, treasure and props.
- `art/source/round2/wall_v1.webp` — the **style** one (round 2 sets the look): painted storybook, muted earth tones, soft darker-brown outlines.

## Batches

Nine batches. Written to run from the repo root; each writes into its own
folder under `art/source/round13/`:

```sh
art/tools/codex_batch.sh art/source/round13/deep_ground deep_ground 3 "three top-down game ground surfaces, one picture per image, each 288x288 and a 3 by 3 grid of 96 px cells, all nine cells drawn as ONE continuous flat top-down scene so the picture reads as one place and tiles by itself; ground surface only, no frame, no objects, big shapes only; image 1 deeper cellar flagstone, damper and darker than the attached ground picture with moss in the seams; image 2 cracked flagstone with thin roots; image 3 wet flagstone with a puddle sheen; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, no text" art/source/round8/town-surfaces/town_ground_v1.webp art/source/round2/wall_v1.webp
```

```sh
art/tools/codex_batch.sh art/source/round13/deep_wall deep_wall 3 "three front-on game wall tiles, one per image, 96x96 each, plain dark cut stone with no lanterns and no frame; image 1 a plain dark cut-stone wall tile; image 2 the same mossy; image 3 the same with pale roots creeping through; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, no text" art/source/round8/town-surfaces/town_ground_v1.webp art/source/round2/wall_v1.webp
```

```sh
art/tools/codex_batch.sh art/source/round13/doors doors 4 "four separate game objects, one per image, 96-128 px each, centred on a plain flat teal background, no text; image 1 a wooden cellar door, iron-banded, arched and closed; image 2 the same door open onto darkness; image 3 a trapdoor in the floor with an iron ring; image 4 the Cellar King's sealed stone door with a crown-shaped wax-and-iron seal in the middle; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light" art/source/round2/wall_v1.webp
```

```sh
art/tools/codex_batch.sh art/source/round13/keys_a keys_a 3 "three separate game item icons, one per image, 128x128 each, centred on a plain flat background, no text; image 1 the Reeve's heavy iron key; image 2 the Bailiff's small brass key with a bell-shaped head; image 3 the Warden's glass lantern-key that glows softly; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light" art/source/round9/sentence-items/gems_v1.webp art/source/round2/wall_v1.webp
```

```sh
art/tools/codex_batch.sh art/source/round13/keys_b keys_b 3 "three separate game item icons, one per image, 128x128 each, centred on a plain flat background, no text; image 1 the Marshal's blunt steel key with a helmet-shaped head; image 2 the Seneschal's key sealed in candle wax with a ribbon; image 3 the Cellar King's seal, a round wax seal pressed with a crown; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light" art/source/round9/sentence-items/gems_v1.webp art/source/round2/wall_v1.webp
```

```sh
art/tools/codex_batch.sh art/source/round13/treasure treasure 4 "four separate game item icons, one per image, 128x128 each, centred on a plain flat background, no text; image 1 a closed wooden treasure chest with brass corners; image 2 the same chest open with a warm glow; image 3 a small heap of gold coins; image 4 a few cut gems (teal, amber, rose) on a scrap of cloth; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light" art/source/round9/sentence-items/gems_v1.webp art/source/round2/wall_v1.webp
```

```sh
art/tools/codex_batch.sh art/source/round13/props_a props_a 4 "four separate game props, one per image, 96-128 px each, centred on a plain flat teal background, no text; image 1 two barrels with iron hoops; image 2 a stack of crates and grain sacks; image 3 a wall torch in an iron sconce, lit; image 4 a cobweb in a stone corner; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light" art/source/round2/wall_v1.webp
```

```sh
art/tools/codex_batch.sh art/source/round13/props_b props_b 4 "four separate game props, one per image, 96-128 px each, centred on a plain flat teal background, no text; image 1 a cluster of glowing cellar mushrooms; image 2 a broken clay pot with shards; image 3 a small puddle with a dripping drop; image 4 a tangle of pale roots pushing through stone; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light" art/source/round2/wall_v1.webp
```

## After the batch

After the batches, work through the pictures in this order. All commands run
from the repo root. Rename each file first: which saved file is which picture
is decided by looking, not by the order the batch came back in.

Size the ground surfaces as 3 x 3 tiles, and cut out the wall, door, item and
prop pictures (128 px icons, 96-128 px objects):

```sh
uv run --offline --with pillow art/tools/process_tiles.py art/source/round13/deep_ground/deep_ground_v1.png art/source/round13/deep_ground/deep_ground_v1_288.png --grid 3x3
uv run --offline --with pillow art/tools/process_tiles.py art/source/round13/deep_ground/deep_ground_v2.png art/source/round13/deep_ground/deep_ground_v2_288.png --grid 3x3
uv run --offline --with pillow art/tools/process_tiles.py art/source/round13/deep_ground/deep_ground_v3.png art/source/round13/deep_ground/deep_ground_v3_288.png --grid 3x3
uv run --offline --with pillow art/tools/process_sprites.py art/source/round13/doors/doors_v1.png art/source/round13/doors/doors_v1_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round13/keys_a/keys_a_v1.png art/source/round13/keys_a/keys_a_v1_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round13/treasure/treasure_v1.png art/source/round13/treasure/treasure_v1_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round13/props_a/props_a_v1.png art/source/round13/props_a/props_a_v1_cut.png --size 128
```

Check the tiles and the cut-outs against the art rules:

```sh
uv run --offline --with pillow art/tools/check_tiles.py art/source/round13/deep_ground/ --grid 3x3
uv run --offline --with pillow art/tools/check_sprites.py art/source/round13/ --size 128
```

Look at them by eye, then in a real room:

```sh
uv run --offline --with pillow art/tools/contact_sheet.py art/source/round13/sheet.jpg art/source/round13/doors/doors_v1_cut.png art/source/round13/keys_a/keys_a_v1_cut.png art/source/round13/treasure/treasure_v1_cut.png art/source/round13/props_a/props_a_v1_cut.png
uv run --offline --with pillow art/tools/mock_room.py art/source/round13/room.jpg --wall art/source/round2/wall_v1.webp --floor art/source/round13/deep_ground/deep_ground_v1_288.png
```

Rylee picks; nothing is approved until she says so.
