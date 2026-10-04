# Guardians brief: the Cellar King's court

`status: draft` — Rylee picks; nothing here is approved by a machine. Codex
draws the pictures; distribution: we may ship what we generate, with attribution
(`AGENTS.md` art rule).

## Purpose

The cellar has five or six floors. Each floor ends with a guardian who carries the key to the stair down; the last is the Cellar King (already drawn, `source/round8/monsters-and-boss/cellar_king_v1`). They are the King's court, weakest to strongest, and their ranks are the names Rylee picked on 2026-10-02: the Reeve, the Bailiff, the Warden, the Marshal, the Seneschal.

## Size

256 x 256 px (the boss size, like the King — twice an ordinary monster, so each guardian sits over the ordinary cast on the screen). Each must read at small size by its silhouette and carries ONE visible sign of its rank: a ring of keys, a bell, a lantern, a helmet, a candle and a ledger. Front-facing three-quarter view, friendly-spooky and never gory, big shapes and few details. Transparent or plain teal background, no text.

## Pictures wanted

Two batches (three, then two): five guardians in all, never one picture per call. Weakest to strongest.

The pictures in a batch come back in any order; identify each by looking, then rename.

**`guardians_low` COUNT 3:**

- **The Reeve** (floor 1, gentlest): a stout, whiskered old mole in a patched apron and round spectacles, a big ring of iron keys at his belt, clutching a lantern.
- **The Bailiff** (floor 2): a very large pale moth, plump and furry, with a tiny brass bell hung at its throat and a small stern frown, wings half folded like a coat.
- **The Warden** (floor 3): a tall old mushroom elder, a wide mossy cap with a small glowing lantern hanging from its edge, a walking stick, kind but watchful eyes.

**`guardians_high` COUNT 2:**

- **The Marshal** (floor 4): a stout armoured stag beetle with a polished teal helmet and a short blunt lance, standing square and proud, round and heavy.
- **The Seneschal** (floor 5, the King's right hand): a tall, thin shade in a steward's long robe, holding a single candle in one hand and a heavy ledger in the other, hollow glowing eyes, calm and formal.

## References

Pass these two files, in this order:

- `art/source/round8/monsters-and-boss/cellar_king_v1.webp` — the **who/what** one: the King the court serves; the style anchor.
- `art/source/round8/monsters-and-boss/cellar_dungeon_v3.webp` — the **scale** one: the mushroom creature, the ordinary-monster scale and line weight the guardians are drawn larger than.

## Batches

Two batches, three then two. Written to run from the repo root; both write into
`art/source/round11/guardians/`:

```sh
art/tools/codex_batch.sh art/source/round11/guardians guardians_low 3 "three friendly-spooky cellar guardians, one per image, 256x256 each, drawn larger than an ordinary monster like the attached King picture, front-facing three-quarter view, big shapes and few details, each reads by its silhouette and ONE visible sign of rank, never gory; image 1 the Reeve, gentlest: a stout whiskered old mole in a patched apron and round spectacles with a big ring of iron keys at his belt, clutching a lantern; image 2 the Bailiff: a very large pale moth, plump and furry, with a tiny brass bell hung at its throat and a small stern frown, wings half folded like a coat; image 3 the Warden: a tall old mushroom elder with a wide mossy cap, a small glowing lantern hanging from the cap edge, a walking stick and kind but watchful eyes; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, plain flat teal background, no text" art/source/round8/monsters-and-boss/cellar_king_v1.webp art/source/round8/monsters-and-boss/cellar_dungeon_v3.webp
```

```sh
art/tools/codex_batch.sh art/source/round11/guardians guardians_high 2 "two friendly-spooky cellar guardians, one per image, 256x256 each, drawn larger than an ordinary monster like the attached King picture, front-facing three-quarter view, big shapes and few details, each reads by its silhouette and ONE visible sign of rank, never gory; image 1 the Marshal: a stout armoured stag beetle with a polished teal helmet and a short blunt lance, standing square and proud, round and heavy; image 2 the Seneschal, the King's right hand: a tall thin shade in a steward's long robe, holding a single candle in one hand and a heavy ledger in the other, hollow glowing eyes, calm and formal; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal #3F7E84 accent, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, plain flat teal background, no text" art/source/round8/monsters-and-boss/cellar_king_v1.webp art/source/round8/monsters-and-boss/cellar_dungeon_v3.webp
```

## After the batch

After the batches, work through the pictures in this order. All commands run
from the repo root. Rename each file first: which saved file is which guardian
is decided by looking, not by the order the batch came back in.

Cut out and size each guardian to 256 px:

```sh
uv run --offline --with pillow art/tools/process_sprites.py art/source/round11/guardians/guardians_low_v1.png art/source/round11/guardians/guardians_low_v1_cut.png --size 256
uv run --offline --with pillow art/tools/process_sprites.py art/source/round11/guardians/guardians_low_v2.png art/source/round11/guardians/guardians_low_v2_cut.png --size 256
uv run --offline --with pillow art/tools/process_sprites.py art/source/round11/guardians/guardians_low_v3.png art/source/round11/guardians/guardians_low_v3_cut.png --size 256
uv run --offline --with pillow art/tools/process_sprites.py art/source/round11/guardians/guardians_high_v1.png art/source/round11/guardians/guardians_high_v1_cut.png --size 256
uv run --offline --with pillow art/tools/process_sprites.py art/source/round11/guardians/guardians_high_v2.png art/source/round11/guardians/guardians_high_v2_cut.png --size 256
```

Check the cut-outs against the art rules:

```sh
uv run --offline --with pillow art/tools/check_sprites.py art/source/round11/guardians/ --size 256
```

Look at them by eye, then in a real room:

```sh
uv run --offline --with pillow art/tools/contact_sheet.py art/source/round11/guardians/sheet.jpg art/source/round11/guardians/guardians_low_v1_cut.png art/source/round11/guardians/guardians_low_v2_cut.png art/source/round11/guardians/guardians_low_v3_cut.png art/source/round11/guardians/guardians_high_v1_cut.png art/source/round11/guardians/guardians_high_v2_cut.png
uv run --offline --with pillow art/tools/mock_room.py art/source/round11/guardians/room.jpg --wall art/source/round2/wall_v1.webp --floor art/source/round2/wood_v1.webp
```

Rylee picks; nothing is approved until she says so.
