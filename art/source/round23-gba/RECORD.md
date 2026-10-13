# Round 23: the rest of the Game Boy Advance art set (2026-10-12)

Rylee asked for the GBA art set (cottage#147) to be made through OpenDesign. Batch 1 (the cottage room and four
cellar creatures) went to her for a style check first; her answer was "Yes, keep going" and "Yes!".

**Credit:** Rylee and Claude. Drawn with Codex image (gpt-image-2) inside OpenDesign (project "Cottage GBA art
set", whose brief is `prompts/DESIGN.md`), with round 22's style test and town sheets as references. Cut,
cleaned into native pixels, palette-locked to the town's 64 colours and animated by Claude with VEFR's
`tools/art` (`process_kit.py`, `pixel_common.py`) and the two helpers in `tools/`.

| Sheet | Prompt | Used for |
|---|---|---|
| `cottage-props`, `cottage-tiles`, `cellar-creatures-a` | `prompts/batch-1.prompt.txt` | the cottage room (`props/`, the cottage's `tiles/`), four creature stills; the worn planks were not used |
| `tavern-props`, `tavern-tiles` | `prompts/tavern-*.prompt.txt` | the tavern room; the chandelier and the stained planks were not used |
| `cellar-tiles-a`, `cellar-tiles-b` | `prompts/cellar-tiles-*.prompt.txt` | floors and walls of the four Sections (`tiles/*.grid3x3.webp`); walls darkened to read against floors |
| `cellar-props` | `prompts/cellar-props.prompt.txt` | the door and stair pictures (`tiles/way-*.webp`); the eight decals are `props/` (cut 2026-10-13 with `tools/plan-decor.json`), six of them scattered over generated floors by each Section's `decor` (vefr#442); `fallen-stones` and `sheeted-crates` read as obstacles, so they wait for a hand-placed room |
| `cellar-creatures-b`, `cellar-bosses` | `prompts/cellar-*.prompt.txt` | who each creature is (the stills come from the motion strips) |
| `motion/<name>` | `prompts/motion-<name>.prompt.txt` | each creature's sheet: idle (breathing), move, attack, hurt |
| `items-a`, `items-b`, `items-fix` | `prompts/items-*.prompt.txt` | the 25 item pictures; `items-fix` redrew the poker, the spring, the cold ember and the moth swarm |
| `temple-door-open` | `prompts/temple-door-open.prompt.txt` | the temple in the town after the cellar |

`tools/declutter.py` gives each grid cell only its own subject (a blob belongs to the cell its centre falls in);
`tools/build_sheets.py` scales a creature's six frames by one factor, so the attack frame is not shrunk to fit.
The source sheets are kept here as WebP (quality 90); the game's pictures are lossless WebP at native size.

**The decals (2026-10-13).** `palette.json` was never committed, so the decals were locked to the colours the
pack's own pictures already use (67, read from `props/` and `tiles/`), then cut with `tools/declutter.py` and
VEFR's `tools/art/process_kit.py tools/plan-decor.json` from the same `cellar-props` sheet. Nothing new was drawn.
