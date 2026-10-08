# Skins: a game's interface as pictures

A skin is a folder of small pictures and one file, `skin.json`, that says which picture is which part of the interface. This one, `parchment-and-wood/`, is Cottage of the Breeze's look: aged parchment and carved dark wood with brass studs. The plan for how the VEFR player will use a skin is `design/ui-skin.md` in the VEFR repository. **The player does not load skins yet**; this folder is the pictures, the tools and the proof they hold together.

## What is in a skin

Panels (`panel`, `speech`, `tooltip`), buttons in four states, tabs, toggles, a bar frame and fill, a gold plate, an inventory slot, a divider, a banner, a corner piece, a cursor, and three seamless textures (`parchment.png`, `wood.png`, `brass.png`). `skin.json` lists each part, the `slice` width for the stretchable ones, the ink colours used on panels, and the credit line.

## Rebuild it

```sh
uv run --offline --with pillow art/tools/build_skin.py art/source/round18/ui-soft/skin-source art/skins/parchment-and-wood --name parchment-and-wood
uv run --offline --with pillow art/tools/check_ui.py art/skins/parchment-and-wood
```

Sources: round 18 picks (`art/source/round18/ui-soft/PICKS.md`); eleven pieces cut from the picked sheets, five carry-overs from round 10 (`PROVENANCE.md` / `PROVENANCE.tsv`).

`build_skin.py` turns the raw drawings into a perfectly symmetric nine-slice (it takes one good corner and edge and mirrors them, because a generated border is close to even but never exact). `check_ui.py` refuses a bad skin with a plain sentence: a missing file, a slice that does not fit, button states that are not the same size or not visibly different, ink that is too faint on the panel (4.5 to 1 for body text, 3 to 1 for the dim ink), or a cursor hotspot outside the picture. Running the build twice gives identical files.

## See it

`preview.html` draws the skin the way the player will, with CSS `border-image`, real text on a panel, the four button states, tabs, toggles, a bar, slots and the small pieces. `preview.png` is a screenshot of it.

## What the preview showed (2026-10-01)

- Panels, speech box, buttons, tabs, bar, slots and the small pieces all read well and stay sharp when stretched.
- The panel's drawn rim is a flat parchment colour, so the mottled parchment texture inside it shows a faint inset rectangle. Two ways out, for whoever builds the loader: use a flat fill colour for panel insides, or bake the texture into the rim when the skin is built. A stretched `fill` made a visible quilt, so do not use it.
- The cursor is cream with a thin brown outline; check it is visible on parchment before it ships.
- The buttons are a little glossier than the painted pieces. Judge them beside the panels in the real game.
