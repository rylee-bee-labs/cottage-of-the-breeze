# Characters brief

`status: draft` — Rylee picks; nothing here is approved by a machine.
`training: not cleared` — Codex output is game art only until its terms are
read at the source (`art/STYLE.md`, Licensing note).

## Purpose

Eight people and animals for the town — a keeper, a trader, a tavern regular,
a child, a cat, a gardener, a fisher and a dwarf smith — drawn to the
character size so they stand beside the hero and read the same way.

## Size

128 x 128 px (the character size). Front-facing, chibi proportions like the
hero (`art/source/round7/hero-walk/hero_walk_v1.webp`): big head, small body,
simple shapes, few details so each figure reads at 128 px. One figure centred
on a plain flat light background, transparent-ready — no ground, no cast
shadow, no border, no frame.

## Pictures wanted

Eight pictures in two batches of four (never one picture per call). Each batch
is a set: one figure per picture.

**`people` COUNT 4 — the town people set.** This batch contains four figures:
the Keeper (an old calm keeper of the stone, steady and kindly, not scary), a
trader with a laden backpack, a tavern regular holding a mug, a child with a
kite.

The pictures in a batch come back in any order; identify each by looking, then
rename. `_v1` is not the first item asked for: `codex_batch.sh` saves a
batch's pictures in the order the image files sort, not the order requested,
so `people_v1.png` is NOT necessarily the Keeper.

**`folk` COUNT 4 — the animal and the workers set.** This batch contains four
figures: a tabby cat, a gardener, a fisher, a friendly dwarf smith.

The pictures in a batch come back in any order; identify each by looking, then
rename. `_v1` is not the first item asked for: `codex_batch.sh` saves a
batch's pictures in the order the image files sort, not the order requested,
so `folk_v1.png` is NOT necessarily the cat.

The file names below are the slots a figure goes into once it has been
identified by looking and renamed; until then no saved file is promised to be
any particular figure.

Each figure, in plain words — what it is, what has to read at 128 px, and what
is not wanted:

Batch `people`:

- **The Keeper** — eventual file `people_v1.png` — an old calm keeper of the stone: grey-haired, in a plain robe, standing steady with both hands settled. Has to read: the calm open face and the still, unhurried pose, kind at 128 px. Not wanted: a face hidden under a hood, glowing eyes, anything frightening, skull-like or deathly — steady and kindly, never scary.
- **A trader with a laden backpack** — eventual file `people_v2.png` — a road trader carrying a load strapped high on the back. Has to read: the pack's silhouette, wider than the body and rising above the shoulders, with the straps crossing the chest. Not wanted: goods floating free of the pack, price tags, signs, text, a second figure.
- **A tavern regular holding a mug** — eventual file `people_v3.png` — a friendly regular in an apron, standing easy with a mug up in one hand. Has to read: the mug in the hand and the relaxed front-facing stance. Not wanted: no table, no spilled drink, no staggering, nothing gory.
- **A child with a kite** — eventual file `people_v4.png` — a small child holding a kite by its string, the kite up beside the figure. Has to read: the small scale against the adults and the kite's simple diamond shape. Not wanted: a kite flying loose off the picture, a second figure, a landscape behind — the background stays plain.

Batch `folk`:

- **A tabby cat** — eventual file `folk_v1.png` — a cat, four legs, a striped tabby coat, tail up: **a cat, four legs, NOT a person**. Image models sometimes draw an animal as a person (a real lesson from the bake-off, `art/README.md`, "Animals can come out human"), so the brief says it plainly. Has to read: the four-legged silhouette, the tail and the stripes across the back. Not wanted: standing upright, clothes, a human face, fangs.
- **A gardener** — eventual file `folk_v2.png` — a working gardener in a straw hat and a canvas apron, a trowel or hand fork in one hand. Has to read: the hat brim, the apron and the small tool held clear of the body. Not wanted: no plants, no flowerbeds, no wheelbarrow, nothing growing around the feet — one figure on a plain background.
- **A fisher** — eventual file `folk_v3.png` — a quiet fisher in a flat hat and a waxed coat, a rod shouldered and a creel at the hip. Has to read: the long rod and its line, the hat, the creel. Not wanted: no boat, no water, no landscape, no fish dangling — one figure on a plain background.
- **A friendly dwarf smith** — eventual file `folk_v4.png` — a dwarf smith: short and stocky, a big beard to the belt, a leather apron, a hammer in one hand. Has to read: the short wide silhouette, the beard and the hammer. Not wanted: not scary, no horned helmet, no sparks, no forge — friendly, like the rest of the town.

**Never:** anything from *Castle of the Winds* — we remake the systems, not the
property (`art/STYLE.md`, Never). Rarity is never shown by colour alone, and no
picture carries text.

## References

Pass these two files, in this order:

- `art/source/round7/hero-walk/hero_walk_v1.webp` — the **who/what** one: the same proportions and scale as the hero — big head, small body, drawn in this game's kit. The figures stand at her size.
- `art/source/round7/monsters/monsters_moth_rustle_v2.webp` — the **style** one: a figure already drawn in round 7 — painted storybook, muted earth tones, soft darker-brown outlines.

## Batches

Two batches of four. Written to run from the repo root; both write into
`art/source/round8/characters/`:

```sh
art/tools/codex_batch.sh art/source/round8/characters people 4 "four game characters, one figure per image, 128x128 each, front-facing, chibi proportions like the attached hero: big head, small body, simple shapes, few details so each figure reads at 128 px; one figure centred on a plain flat light background, transparent-ready, no ground and no cast shadow and no border and no frame; image 1 the Keeper, an old calm keeper of the stone, grey-haired and in a plain robe, steady and kindly, not scary; image 2 a road trader with a laden backpack strapped high, the pack wider than the body; image 3 a tavern regular in an apron holding a mug; image 4 a small child holding a kite by its string; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, no text" art/source/round7/hero-walk/hero_walk_v1.webp art/source/round7/monsters/monsters_moth_rustle_v2.webp
```

```sh
art/tools/codex_batch.sh art/source/round8/characters folk 4 "four game characters, one figure per image, 128x128 each, front-facing, chibi proportions like the attached hero: big head, small body, simple shapes, few details so each figure reads at 128 px; one figure centred on a plain flat light background, transparent-ready, no ground and no cast shadow and no border and no frame; image 1 a tabby cat: a cat on four legs with a striped coat and its tail up, a cat and NOT a person, not a humanoid; image 2 a gardener in a straw hat and canvas apron holding a trowel; image 3 a fisher in a flat hat and waxed coat with a rod shouldered and a creel at the hip; image 4 a friendly dwarf smith, short and stocky with a big beard to the belt, a leather apron and a hammer; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, no text" art/source/round7/hero-walk/hero_walk_v1.webp art/source/round7/monsters/monsters_moth_rustle_v2.webp
```

## After the batch

After the batches, work through the pictures in this order. All commands run
from the repo root.

Cut out and size each figure (the original is kept; the cut file gets `_cut`):

```sh
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/characters/people_v1.png art/source/round8/characters/people_v1_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/characters/people_v2.png art/source/round8/characters/people_v2_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/characters/people_v3.png art/source/round8/characters/people_v3_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/characters/people_v4.png art/source/round8/characters/people_v4_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/characters/folk_v1.png art/source/round8/characters/folk_v1_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/characters/folk_v2.png art/source/round8/characters/folk_v2_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/characters/folk_v3.png art/source/round8/characters/folk_v3_cut.png --size 128
uv run --offline --with pillow art/tools/process_sprites.py art/source/round8/characters/folk_v4.png art/source/round8/characters/folk_v4_cut.png --size 128
```

Check the cut-outs against the art rules:

```sh
uv run --offline --with pillow art/tools/check_sprites.py art/source/round8/characters/ --size 128
```

Look at them by eye, then in a real room:

```sh
uv run --offline --with pillow art/tools/contact_sheet.py art/source/round8/characters/sheet.jpg art/source/round8/characters/people_v1_cut.png art/source/round8/characters/people_v2_cut.png art/source/round8/characters/people_v3_cut.png art/source/round8/characters/people_v4_cut.png art/source/round8/characters/folk_v1_cut.png art/source/round8/characters/folk_v2_cut.png art/source/round8/characters/folk_v3_cut.png art/source/round8/characters/folk_v4_cut.png
uv run --offline --with pillow art/tools/mock_room.py art/source/round8/characters/room.jpg --wall art/source/round2/wall_v1.webp --floor art/source/round2/wood_v1.webp
```

`mock_room.py` shows the room they stand in (96 px tiles); check the 128 px
figures against that scale by eye — each one should sit beside the hero, not
tower over her. Only Rylee approves a figure; leave `status: draft` until she
picks.
