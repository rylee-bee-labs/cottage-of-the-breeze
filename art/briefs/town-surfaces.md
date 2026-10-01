# Town surfaces brief

`status: draft` — Rylee picks; nothing here is approved by a machine.
`training: not cleared` — Codex output is game art only until its terms are
read at the source (`art/STYLE.md`, Licensing note).

## Purpose

Six ground surfaces for the town — the street, the meadow, the path, the
tavern floor, the cellar floor and the stream bank — each drawn as one 3 x 3
grid tile picture so the engine can lay it under the hero and the town folk.

## Size

288 x 288 px: a 3 x 3 grid of 96 px cells, drawn as ONE continuous scene so
the cut reads as one place. The engine draws cell (x mod 3, y mod 3), so the
picture has to tile by itself — no frame, no border, no edge that gives the
grid away, and the surface carries on off all four sides the way it starts.

Flat top-down ground, seen from straight above. **No objects on the ground** —
no furniture, no characters, no items, no grass tufts standing up; just the
surface. Keep the shapes big and few ("only 4 or 5 big stones"): tiny detail
turns to noise at 96 px (`art/README.md`, "What we learned").

## Pictures wanted

Six pictures in two batches of three (never one picture per call). Each batch
is a set: one whole surface per picture.

**`town_ground` COUNT 3 — the outdoor set.** This batch contains three
pictures: a cobblestone street, a meadow grass, a packed dirt path.

The pictures in a batch come back in any order; identify each by looking, then
rename. `_v1` is not the first item asked for: `codex_batch.sh` saves a
batch's pictures in the order the image files sort, not the order requested,
so `town_ground_v1.png` is NOT necessarily the cobblestone street.

**`town_indoor` COUNT 3 — the indoor set.** This batch contains three
pictures: a tavern plank floor, a cellar flagstone, a shallow stream bank.

The pictures in a batch come back in any order; identify each by looking, then
rename. `_v1` is not the first item asked for: `codex_batch.sh` saves a
batch's pictures in the order the image files sort, not the order requested,
so `town_indoor_v1.png` is NOT necessarily the tavern plank floor.

Each surface, in plain words — what it is, what has to read at 96 px, and what
is not wanted:

- **Cobblestone street** (batch `town_ground`) — a worn town street of big rounded stones laid close together with wide joints, in earth browns and grey-browns. Has to read: the stones themselves, only 4 or 5 big stones to a cell, each big enough to count. Not wanted: anything standing on it — no cart, no lamp, no barrels, no loose rubble — and no pure black in the joints.
- **Meadow grass** (batch `town_ground`) — soft grass mown flat, in the moss greens #4F7870 and #648B77 with a little earth brown showing through. Has to read: the green, and a soft mottled sweep of growth carried evenly across the whole picture. Not wanted: blades drawn one by one, tufts standing up, flowers, fences, stones standing proud.
- **Packed dirt path** (batch `town_ground`) — dry packed earth trodden smooth, earth browns #76633E over #433A2A, a touch paler where it is most worn. Has to read: broad smooth bands of trodden earth and at most a couple of big pebbles pressed flat into the surface. Not wanted: footprints, deep ruts that read as holes, grass creeping over it, anything lying on it.
- **Tavern plank floor** (batch `town_indoor`) — wooden floorboards running in wide strips, noticeably DARKER than the cottage wood in `art/source/round2/wood_v1.webp`: a deep smoked brown led by #433A2A, the darkest floor of the six. Has to read: a few wide planks and their joins running right across the picture. Not wanted: brighter or more orange than `wood_v1`, eight tiny planks, nails, spills, furniture of any kind.
- **Cellar flagstone** (batch `town_indoor`) — big flat quarried slabs under the cottage, cool greyed earth tones with a touch of dusk teal in the shade. Has to read: the slab shapes and their joints, only 4 or 5 big stones to a cell — like the street, but flatter and square-cut. Not wanted: moss tufts, cracks full of pure black, sand, or anything standing on it.
- **Shallow stream bank** (batch `town_indoor`) — where a thin sheet of water slips over gravel at the bank's edge: damp shingle and wet earth, the water reading as a paler teal-tinted band across the picture. Has to read: the change from wet to dry and the soft line where water meets bank. Not wanted: reeds or grass standing up, rocks standing proud, fish, splashes, sky reflections — nothing but the ground.

**Never:** anything from *Castle of the Winds* — we remake the systems, not the
property (`art/STYLE.md`, Never). Rarity is never shown by colour alone, and no
picture carries text.

## References

Pass these two files, in this order:

- `art/source/round2/wood_v1.webp` — the **who/what** one: the painted floor surface of this game's kit (material and palette); the tavern floor is its darker cousin.
- `art/source/round2/wall_v1.webp` — the **style** one (round 2 sets the look): painted storybook, muted earth tones, soft darker-brown outlines.

## Batches

Two batches of three. Written to run from the repo root; both write into
`art/source/round8/town-surfaces/`:

```sh
art/tools/codex_batch.sh art/source/round8/town-surfaces town_ground 3 "three top-down game ground surfaces, one picture per image, each 288x288 and a 3 by 3 grid of 96 px cells, all nine cells drawn as ONE continuous flat top-down scene so the picture reads as one place and tiles by itself; ground surface only, NO objects on the ground: no furniture, no characters, no items, no grass tufts standing up, just the surface; big shapes and few of them, only 4 or 5 big stones to a cell; image 1 a cobblestone street of big rounded stones laid close with wide joints, earth browns and grey-browns; image 2 a meadow grass of soft mown grass in moss greens; image 3 a packed dirt path of dry trodden earth; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, no text" art/source/round2/wood_v1.webp art/source/round2/wall_v1.webp
```

```sh
art/tools/codex_batch.sh art/source/round8/town-surfaces town_indoor 3 "three top-down game ground surfaces, one picture per image, each 288x288 and a 3 by 3 grid of 96 px cells, all nine cells drawn as ONE continuous flat top-down scene so the picture reads as one place and tiles by itself; ground surface only, NO objects on the ground: no furniture, no characters, no items, no grass tufts standing up, just the surface; big shapes and few of them, only 4 or 5 big stones to a cell; image 1 a tavern plank floor of wide wooden floorboards, noticeably darker than pale cottage wood, a deep smoked brown; image 2 a cellar flagstone floor of big flat square-cut stone slabs, cool greyed earth tones; image 3 a shallow stream bank where a thin sheet of water slips over gravel, damp shingle and wet earth; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, no text" art/source/round2/wood_v1.webp art/source/round2/wall_v1.webp
```

## After the batch

After the batches, work through the pictures in this order. All commands run
from the repo root.

Size each picture to what the engine draws. The original is kept: the sized
copy gets `_288` on the end, one convention for all six.

```sh
uv run --offline --with pillow art/tools/process_tiles.py art/source/round8/town-surfaces/town_ground_v1.png art/source/round8/town-surfaces/town_ground_v1_288.png --grid 3x3
uv run --offline --with pillow art/tools/process_tiles.py art/source/round8/town-surfaces/town_ground_v2.png art/source/round8/town-surfaces/town_ground_v2_288.png --grid 3x3
uv run --offline --with pillow art/tools/process_tiles.py art/source/round8/town-surfaces/town_ground_v3.png art/source/round8/town-surfaces/town_ground_v3_288.png --grid 3x3
uv run --offline --with pillow art/tools/process_tiles.py art/source/round8/town-surfaces/town_indoor_v1.png art/source/round8/town-surfaces/town_indoor_v1_288.png --grid 3x3
uv run --offline --with pillow art/tools/process_tiles.py art/source/round8/town-surfaces/town_indoor_v2.png art/source/round8/town-surfaces/town_indoor_v2_288.png --grid 3x3
uv run --offline --with pillow art/tools/process_tiles.py art/source/round8/town-surfaces/town_indoor_v3.png art/source/round8/town-surfaces/town_indoor_v3_288.png --grid 3x3
```

Check the whole folder in one go:

```sh
uv run --offline --with pillow art/tools/check_tiles.py art/source/round8/town-surfaces/ --grid 3x3
```

`check_tiles.py`'s seam check is a HEURISTIC that flags plank-like art; if it
flags a picture, look by eye at the cell edges before you believe it. (The raw
`_vN.png` originals left in that folder are not 288 px yet and will report a
wrong size; only the `_288` pictures are tiles.)

Look at them together, then in a real room:

```sh
uv run --offline --with pillow art/tools/contact_sheet.py art/source/round8/town-surfaces/sheet.jpg art/source/round8/town-surfaces/town_ground_v1_288.png art/source/round8/town-surfaces/town_ground_v2_288.png art/source/round8/town-surfaces/town_ground_v3_288.png art/source/round8/town-surfaces/town_indoor_v1_288.png art/source/round8/town-surfaces/town_indoor_v2_288.png art/source/round8/town-surfaces/town_indoor_v3_288.png
uv run --offline --with pillow art/tools/mock_room.py art/source/round8/town-surfaces/room.jpg --wall art/source/round2/wall_v1.webp --floor art/source/round8/town-surfaces/town_ground_v1_288.png
```

The mock room lays the floor at 96 px across a whole room — that is where a
repeating grid or a hard cell edge shows up, so look by eye. Nothing here is
approved until Rylee picks; once she picks a surface, the other two of its
batch stay as variants (`art/STYLE.md`, several variant tiles per surface).
