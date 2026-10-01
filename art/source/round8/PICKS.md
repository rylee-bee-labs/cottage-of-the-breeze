# Round 8 picks (Rylee, 2026-10-01)

Codex proofs in 13 batched calls plus one redo (`training: not cleared`; see each `.credits.txt`). Not final art for release.

## Residents (first people in Cottage)
Kept: the old keeper with the staff, the tavern regular with the mug, the trader with the backpack, the tabby cat, the fisher with the rod,
the gardener with the trowel, and the dwarf smith (redrawn chibi). Cut to 128 px in `characters/picked-128px/`:
`keeper.png` (people_v4), `tavern-regular.png` (people_v2), `trader.png` (people_v1), `cat.png` (folk_v2), `fisher.png` (folk_v3),
`gardener.png` (folk_v4), `dwarf-smith.png` (characters-redo/dwarf_chibi_v1).
Not in the first set: the child with the kite (people_v3), kept as a candidate. The first, more realistic dwarf (folk_v1) is superseded by the redo.
The dwarf redo has two versions; Rylee chose **version 1** (2026-10-01); version 2 stays as a variant.

## Ground tiles (3x3 grid pictures, 288 x 288)
`town-surfaces/ready-288px-3x3/`: cobblestone street, meadow grass, packed dirt, tavern planks, cellar flagstone, stream bank.
Notes: the dirt, grass and stream bank show a faint diagonal streak when repeated; the flagstone trips the seam heuristic (strong slab edges; it looks fine by eye).
Not yet picked: which to use where.

## Everything else (not yet picked)
Monsters and the Cellar King (`monsters-and-boss/`), furniture, doors, window, well and sign (`props-and-furniture/`), and the spellbook, gear, clothes
and trinkets (`spellbook-and-inventory/`).

Tools: `process_sprites.py` (128 px, clears a drawn checkerboard), `process_tiles.py --grid 3x3`, `check_sprites.py`, `check_tiles.py`.
