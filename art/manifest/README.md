# The art manifest

One place that knows every picture the game uses, and exactly what to draw
next. It exists so an image-generation agent can be handed a single page and
come back with a sheet that cuts straight into the game, with no guessing about
sizes, order, background or where the file goes.

## The three commands

```sh
# what the game uses today, and anything it names but lacks (fails on a missing picture)
python3 art/tools/art_manifest.py audit

# what is still to draw (filter by kind or by loop)
python3 art/tools/art_manifest.py wanted --kind mob
python3 art/tools/art_manifest.py wanted --loop 3

# write the image-agent briefs into art/requests/ (one .md and one .plan.json per batch)
python3 art/tools/art_manifest.py brief --all
python3 art/tools/art_manifest.py brief wardens-well-fire
```

Stdlib only. The tests (`art/tests/test_art_manifest.py`) run with the rest of
the art tests and also fail when `art/requests/` is stale.

## The files

| File | What it is | Who edits it |
|---|---|---|
| `slots.json` | `wanted`: art the game needs and does not have, one slot per picture, each tied to a loop in [`LOOPS.md`](../../docs/plans/release-1-0/LOOPS.md). `batches`: which slots share one generated sheet. `status`: notes on shipped art (`interim`, `redo`). | people and agents; Rylee decides what ships |
| `TEMPLATE.md` | the brief every request is filled from: style contract, references, the cell table, the prompt, saving, the cut plan, the checklist | rarely; regenerate after |
| `../requests/*.md` | **generated.** Hand one to the image agent as it is | nobody: regenerate |
| `../requests/*.plan.json` | **generated.** The cut plan for VEFR's `tools/art/process_kit.py`, or the strip heights for creatures | nobody: regenerate |

## The kinds

Every slot is one kind. The kind fixes the sheet layout, the native size, the
reference sheet passed to the model, where the cut file lands and how the pack
points at it. The table is `KINDS` in `art/tools/art_manifest.py`.

| Kind | In the game | Sheet the agent draws | Lands in the pack |
|---|---|---|---|
| `item` | ≤ 24 × 24 px icon | 4 × 3 grid on `#00FF00` | `sprites/ID.webp` |
| `mob` | still 24–40 px tall + six-frame strip | stills grid, then one strip each | `sprites/ID.webp`, `ID-sheet.webp`, `ID.sheet.json` |
| `boss` | still 64–96 px tall + six-frame strip | 2 × 2 stills, then one strip each | same as `mob` |
| `person` | 48 px tall in 64 × 64 frames, three facings | one 4 × 3 sheet per resident | same as `mob` |
| `prop` | its own size in whole tiles | 4 × 3 grid, front face down the screen | `props/ID.webp` |
| `decor` | ≤ 32 × 32 decal | 4 × 3 grid | `props/ID.webp` |
| `tile` | 96 × 96: 3 × 3 cells of 32 px, wraps | 2 × 2 textures, edge to edge | `tiles/ID.grid3x3.webp` |
| `way` | 32 × 32 door or stair | 2 × 2 grid | `tiles/way-ID.webp` |
| `ui` | 16–24 px icon | 4 × 3 grid | **needs VEFR first**: no pack slot for interface icons yet |
| `card` | 1600 × 900 picture | one per call | `assets/ID.webp` |

## Adding a slot

1. Add it to `wanted` in `slots.json`: `id` (an asset id, never a
   player-facing name), `kind`, `loop`, `native` `[w, h]`, `subject` (what to
   draw, in plain words: say only what you want), `why`.
2. Put it in exactly one batch (one kind per batch, at most the kind's grid).
3. `python3 art/tools/art_manifest.py brief --all`, then run the art tests.

When the sheet comes back and Rylee picks it: cut it with the plan, wire it into
the pack as the brief says, delete the slot from `wanted`, regenerate, and run
`audit` and the validator.

## Rules this keeps

- Art we ship is art we made, credited "Rylee and Claude", with a credits line
  beside every sheet (`AGENTS.md`). Kenney and LimeZu are never used here.
- One style: the GBA contract in [`art/STYLE.md`](../STYLE.md). Rarity is never
  colour alone: a glow, a word and a frame shape.
- Nothing from *Castle of the Winds*.
- A request is not an approval. Names, and anything that becomes canon, are
  Rylee's.
