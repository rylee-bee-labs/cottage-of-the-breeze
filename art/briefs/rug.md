# Rug brief

`status: draft` — Rylee picks; nothing here is approved by a machine.
`training: not cleared` — Codex output is game art only until its terms are
read at the source (`art/STYLE.md`, Licensing note).

## Purpose

One rug for the cottage and temple floors, drawn as a single woven object so it
reads as a rug and never as a repeating tile.

## Size

288 x 192 px: 3 tiles wide by 2 tiles tall at the 96 px tile size. At that size
the border, the woven texture and the dusk teal `#3F7E84` pattern must still
read from across the room, so keep the shapes big and few. **A rug is one
object, not a repeating tile** — a rug repeated 2x2 looks like a window
(`art/README.md`, "What we learned").

## Pictures wanted

Three different designs, one batch of three (never one picture per call):

- `rug` COUNT 3 — picture 1 of 3, design A: the plain worn weave (`rug_v1`).
- `rug` COUNT 3 — picture 2 of 3, design B: a bolder teal `#3F7E84` geometric pattern (`rug_v2`).
- `rug` COUNT 3 — picture 3 of 3, design C: a faded floral pattern (`rug_v3`).

Keep `rug_v1`, the plain worn weave, as the room's rug. `rug_v2` and `rug_v3`
are variants to swap in when a room wants a different floor covering. Do not ask
for the same design twice: the three pictures are three different designs.

## References

Pass these two files, in this order:

- `art/source/round2/rug_v1.webp` — the **who/what** one: a woven rug in this game's kit.
- `art/source/round2/wall_v1.webp` — the **style** one (round 2 sets the look): painted storybook, muted earth tones, soft darker-brown outlines.

## Batches

One batch, three pictures. Written to run from the repo root; it writes into
`art/source/round7/rug/`:

```sh
art/tools/codex_batch.sh art/source/round7/rug rug 3 "one rug drawn as a single flat object, seen from straight above, 3 tiles wide by 2 tiles tall (288x192), woven and worn, with dusk teal #3F7E84 in the pattern; not a repeating tile and not a square, because a rug repeated 2x2 looks like a window; three different designs in these three images: image 1 the plain worn weave, image 2 a bolder dusk teal geometric pattern, image 3 a faded floral pattern; cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, moss greens #4F7870 and #648B77, earth browns #433A2A and #76633E, a touch of lantern amber #B79D51, warm calm light, plain flat background, no text" art/source/round2/rug_v1.webp art/source/round2/wall_v1.webp
```

## After the batch

After the batch, work through the pictures in this order. All commands run from
the repo root.

Cut out and size each design:

```sh
uv run --offline --with pillow art/tools/process_sprites.py art/source/round7/rug/rug_v1.png art/source/round7/rug/rug_v1_cut.png --size 288
uv run --offline --with pillow art/tools/process_sprites.py art/source/round7/rug/rug_v2.png art/source/round7/rug/rug_v2_cut.png --size 288
uv run --offline --with pillow art/tools/process_sprites.py art/source/round7/rug/rug_v3.png art/source/round7/rug/rug_v3_cut.png --size 288
```

Check the cut-outs against the art rules:

```sh
uv run --offline --with pillow art/tools/check_sprites.py art/source/round7/rug/rug_v1_cut.png art/source/round7/rug/rug_v2_cut.png art/source/round7/rug/rug_v3_cut.png --size 288
```

Look at them by eye, then in a real room:

```sh
uv run --offline --with pillow art/tools/contact_sheet.py art/source/round7/rug/sheet.jpg art/source/round7/rug/rug_v1_cut.png art/source/round7/rug/rug_v2_cut.png art/source/round7/rug/rug_v3_cut.png
uv run --offline --with pillow art/tools/mock_room.py art/source/round7/rug/room.jpg --wall art/source/round2/wall_v1.webp --floor art/source/round2/wood_v1.webp --rug art/source/round7/rug/rug_v1_cut.png
```

A rug is 3x2 tiles, not a square. `process_sprites.py` works on a square
canvas, so trim the cut-out to 288x192 before it goes into the pack.
