# Skins: a game's interface as pictures

A skin is a folder of small pictures and one file, `skin.json`, that says which picture is which part of the interface. This one, `parchment-and-wood/`, is Cottage of the Breeze's look: aged parchment and carved dark wood with brass studs. The plan for how the VEFR player will use a skin is `design/ui-skin.md` in the VEFR repository. **The player does not load skins yet**; this folder is the pictures, the tools and the proof they hold together.

## What is in a skin

Panels (`panel`, `speech`, `tooltip`), buttons in four states, tabs, toggles, a bar frame and fill, a gold plate, an inventory slot, a divider, a banner, a corner piece, a cursor, and three seamless textures (`parchment.png`, `wood.png`, `brass.png`). `skin.json` lists each part, the `slice` width for the stretchable ones, the ink colours used on panels, and the credit line.

## Rebuild it

```sh
uv run --offline --with pillow art/tools/build_skin.py art/source/round18/ui-soft/skin-source art/skins/parchment-and-wood --name parchment-and-wood
uv run --offline --with pillow art/tools/check_ui.py art/skins/parchment-and-wood
```

Sources: round 18 picks (`art/source/round18/ui-soft/PICKS.md`); ten pieces cut from the picked sheets, one (`tab-selected`) derived from a picked sheet by `make_selected_tab.py`, five carry-overs from round 10. Provenance and the `derived` marker: `art/source/round18/ui-soft/skin-source/PROVENANCE.md` / `.tsv`.

The build writes the *parts*; it does not write `skin.json`'s fonts, backdrop or credit line, and it does not copy the result into the pack. Those three the pack needs are set by hand (the backdrop is `backdrop-alt-1.webp`), and the pictures are copied into `worlds/cottage-of-the-breeze/skins/parchment-and-wood/` — so this folder's own `skin.json` is the studio copy and is **not** the one that ships. The pack's is the one to read.

`build_skin.py` turns the raw drawings into a perfectly symmetric nine-slice (it takes one good corner and edge and mirrors them, because a generated border is close to even but never exact). `check_ui.py` refuses a bad skin with a plain sentence: a missing file, a slice that does not fit, button states that are not the same size or not visibly different, ink that is too faint on the panel (4.5 to 1 for body text, 3 to 1 for the dim ink), or a cursor hotspot outside the picture. Running the build twice gives identical files.

## See it

`preview.html` draws the skin the way the player will, with CSS `border-image`, real text on a panel, the four button states, tabs, toggles, a bar, slots and the small pieces. `preview.png` is a screenshot of it — but it is dated 2026-10-01 and still shows the round-10 art, so it is **not** a picture of the skin that ships.

`look-phone.png` and `look-desktop.png` are the current ones, drawn from the *pack's* copy of the skin by `art/tools/mock_skin.py` at a phone (390x844) and a desktop (1280x800) viewport:

```sh
uv run --offline --with pillow art/tools/mock_skin.py \
    ../../worlds/cottage-of-the-breeze/skins/parchment-and-wood look-phone.png --size 390x844
```

They exist because `preview.html` draws the parts one at a time, which hides the faults that only appear once the chrome is assembled at a real size — a rim that thins out when a panel is wide, a selected tab that stops being the shape of the tab beside it. Those two are exactly how the round-two `tab-selected` pick was caught; see `../source/round18/ui-soft/skin-source/PROVENANCE.md`. The mock is not the engine and not a validator — `check_ui.py` still decides whether a skin is legal.

## What the preview showed (2026-10-01)

- Panels, speech box, buttons, tabs, bar, slots and the small pieces all read well and stay sharp when stretched.
- The panel's drawn rim is a flat parchment colour, so the mottled parchment texture inside it shows a faint inset rectangle. Two ways out, for whoever builds the loader: use a flat fill colour for panel insides, or bake the texture into the rim when the skin is built. A stretched `fill` made a visible quilt, so do not use it.
- The cursor is cream with a thin brown outline; check it is visible on parchment before it ships.
- The buttons are a little glossier than the painted pieces. Judge them beside the panels in the real game.

## What the look showed (2026-10-08, the round-two skin)

Drawn from the pack's skin at both sizes, with the round-two picks in place.

- **Panels, speech box, tooltip, buttons, bar, gold plate and slots all read well** at 390x844 and at 1280x800, and hold up when the panel is stretched to a full-width desktop dialogue box. The rims keep their thickness.
- **The tabs now read as one tab in two states.** `tab.webp` and `tab-selected.webp` are the same silhouette, the selected one lighter — see `PROVENANCE.md` for why it had to be built that way rather than cut.
- **The bar is right.** `bar-fill` sits in `bar-frame`'s trough, and the seam between them is invisible at both sizes. Note for whoever builds the loader: the fill goes *over* the frame; the other way round the frame's opaque middle hides it completely.
- **Still true from 2026-10-01:** the panel's centre is the parchment texture stretched, so a wide panel shows a soft quilt inside the rim. It reads as parchment rather than as an error, and it is what `border-image` will do, so it is left for the loader rather than papered over here.
- **Not looked at here:** the cursor, the banner, the divider, the corner and the small ornaments are not drawn by the mock's assembled layout (they are placed by the player over the map, not in a panel flow). They were checked as parts at real size and read correctly; they are still unproven *in play*.
