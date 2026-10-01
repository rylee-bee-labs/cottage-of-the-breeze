# Making art for Cottage

How we make the pictures, so a person or an agent can pick it up and have a good time.
The look itself is in [STYLE.md](STYLE.md). The pipeline in one line:
**proof with Codex, Rylee picks, bulk with Wan 2.7 Image Pro, process, check it in the real build, keep the record.**

## The loop

1. **Brief one asset.** What it is, its size (tiles 96 px, characters and items 128 px), what has to show at that size.
2. **Proof with Codex, in a batch.** Ask for several variations in one call:

   ```sh
   art/tools/codex_batch.sh art/source/round4 wood 3 "top-down game floor tile, weathered wooden floorboards ... (see STYLE.md for the shared style words)"
   ```

   One call, several images: Codex charges per tool call, so this is cheaper than one call per picture
   (measured: about 40% fewer tokens per image for a pair). Pass reference images after the brief:
   the first says who or what, the second says the style.
3. **Look at it properly.** A single tile hides problems:

   ```sh
   uv run --with pillow art/tools/contact_sheet.py sheet.jpg art/source/round4/wood_v*.png
   uv run --with pillow art/tools/contact_sheet.py tiled.jpg art/source/round4/wood_v*.png --tile2x2
   uv run --with pillow art/tools/mock_room.py room.jpg --wall wall.png --floor wood.png --rug rug.png
   ```
4. **Rylee picks.** Nothing is approved until she says so. Update `status:` in the credits line.
5. **Bulk with Wan 2.7 Image Pro** once proofs are approved, using them as style references. (The
   2026-09-30 bake-off found Wan Pro follows layout specs best and keeps sprite frames most consistent.
   How it takes reference images is not yet tested here.)
6. **Process and check in the real build:** size, cut-out, then weave and screenshot (`../vefr`: `ratatoskr weave`).
7. **Keep the record.** Every picture has a `name.credits.txt` beside it: who made it, the tool, the
   references, the exact prompt, the date, and its status. The script writes it for you.

## Swappable by design

Every piece here can be replaced without touching the others, so the same studio can make very different games:

| Piece | What it is | How to swap it |
|---|---|---|
| **Style kit** | The look: `STYLE.md` (palette, rules, never-list), the anchor pictures (a ground and a wall) and the shared style words | A new game gets its own kit in its own `art/`. Kits are never mixed inside one game. |
| **Generator backend** | The tool that makes pictures | Any script with the same shape as `codex_batch.sh`: `OUTDIR NAME COUNT "BRIEF" [REFS...]` in, `NAME_vN.png` plus `NAME_vN.credits.txt` out. A Wan or local-painter backend drops in beside it. |
| **Sizes** | Tile and character size | Pack data, not engine code (a region's contract already carries `tile`). Cottage uses 96 px tiles and 128 px characters; a pixel-art game might use 32 and 32. |
| **Tile set** | Floors, walls, grounds, with variants | A pack's own `tiles/` (proposed in `../vefr/design/pack-art-proposal.md`). |
| **Characters** | Single drawing, or a sheet of walk frames | A sprite and an optional sheet next to it (same proposal). |
| **Credits record** | Who made it, how, when | The same one-line format for every backend. |

The rule that keeps this honest: **the engine never learns a game's look, and a kit never learns another game's.**

## What we learned (2026-10-01)

- **Saturated wood looks orange.** Ask for muted tones by naming the palette (STYLE.md has the hex values).
- **Size the shapes for the tile.** "Only 3 planks across the whole tile" or "only 4 or 5 big stones" works;
  without it you get 8 tiny planks that turn to noise at 96 px.
- **An object is not a tile.** A rug repeated 2x2 looks like a window. Draw it once.
- **Repeats show in a room.** One tile per surface makes a grid; the plan is 3 variants per surface.
- **"Pixel art" from a painter is not pixel art.** It came back as a detailed painting with heavy outlines.
- **A reference is the strongest instruction.** Give the first image as "who" and the second as "style".
- **Sheets work.** Codex kept one character consistent across a four-view turnaround and a four-frame
  walk strip. Frames still need cutting out and aligning to a baseline before the engine can use them.
- **Codex waits on stdin if you let it.** A call run in a foreground shell hung for the full 15-minute timeout with the log saying "Reading additional input from stdin". The tool now reads from `/dev/null`; do the same in any script you write.
- **Animals can come out human.** The bake-off's image models drew a person when asked for a crab; test
  monsters early.

## For AI assistants

- **Ask before spending.** Quota is the owner's. State the count of images before you start, batch them,
  and report what it used.
- **Never approve a picture.** Only Rylee does. Leave `status: draft`.
- **Always save the prompt and credits line.** That is how a picture stays explainable later.
- **Show, do not describe.** She is a visual learner: send a contact sheet or a mock room, not a paragraph.
- **One variable per round.** Change the colour or the scale or the outline, not all three, so she can see why.
- **Keep the style board in step:** decisions go in STYLE.md; the pretty version is the private style board.

## Where things live

| What | Where |
|---|---|
| Proofs (webp copies) and their credits | `art/source/roundN/` |
| Full-size originals | the machine that generated them (Codex's output folder) |
| Style and decisions | `art/STYLE.md` |
| The engine side (what the player can show) | `../vefr/design/pack-art-proposal.md` |
