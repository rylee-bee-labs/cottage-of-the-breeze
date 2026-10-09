# Skins: a game's interface as pictures

A skin is a folder of small pictures and one file, `skin.json`, that says which picture is which part of the interface. This one, `parchment-and-wood/`, is Cottage of the Breeze's look: aged parchment and carved dark wood with brass studs. The plan for how the VEFR player uses a skin is `design/ui-skin.md` in the VEFR repository, and the player does load one: `web/player/parts/540-the-skin.js` paints every part a pack's manifest names, and `look-*.png` below are that player running with this skin on it.

## What is in a skin

Panels (`panel`, `speech`, `tooltip`), buttons in four states, tabs, toggles, a bar frame and fill, a gold plate, an inventory slot, a divider, a banner, a corner piece, a cursor, and three seamless textures (`parchment.png`, `wood.png`, `brass.png`). `skin.json` lists each part, the `slice` width for the stretchable ones, the ink colours used on panels, and the credit line.

## Rebuild it

```sh
uv run --offline --with pillow art/tools/build_skin.py art/source/round18/ui-soft/skin-source art/skins/parchment-and-wood --name parchment-and-wood
uv run --offline --with pillow art/tools/check_ui.py art/skins/parchment-and-wood
```

Sources: round 18 picks (`art/source/round18/ui-soft/PICKS.md`); eight pieces cut straight from the picked sheets, three (`tab-selected`, `banner`, `slot`) made *from* a picked sheet by a tool in `art/tools/` and kept beside their untouched cuts as `-v3` pictures, five carry-overs from round 10. Provenance and the `derived` marker: `art/source/round18/ui-soft/skin-source/PROVENANCE.md` / `.tsv`.

The build writes the *parts*; it does not write `skin.json`'s fonts, backdrop or credit line, and it does not copy the result into the pack. Those three the pack needs are set by hand (the backdrop is `backdrop-alt-1.webp`), and the pictures are copied into `worlds/cottage-of-the-breeze/skins/parchment-and-wood/` — so this folder's own `skin.json` is the studio copy and is **not** the one that ships. The pack's is the one to read.

`build_skin.py` turns the raw drawings into a perfectly symmetric nine-slice (it takes one good corner and edge and mirrors them, because a generated border is close to even but never exact). `check_ui.py` refuses a bad skin with a plain sentence: a missing file, a slice that does not fit, button states that are not the same size or not visibly different, ink that is too faint on the panel (4.5 to 1 for body text, 3 to 1 for the dim ink), or a cursor hotspot outside the picture. Running the build twice gives identical files.

Every WebP is written with `lossless=True`. That is not Pillow's default for WebP, which is lossy, and a part that has been through two quantisations is a part nobody chose.

## See it

There are two kinds of picture of this skin in this repository, and they are kept apart on purpose.

**Play evidence** — `parchment-and-wood/look-*.png` are screenshots of the woven player, taken by running it:

```sh
cd ~/code/Rylee-Bee/vefr
PACK="$PWD/../cottage-of-the-breeze/worlds/cottage-of-the-breeze"
uv run vefr look --pack "$PACK" --out .../look-desktop.png     # the desktop shot, the engine's own tool
uv run vefr weave --pack "$PACK" --out /tmp/player.html
uv run --with playwright python .../art/tools/real_look.py --html /tmp/player.html --out .../look-phone.png --size 390x844
```

`real_look.py` is a thin stand-in for `vefr look` at a viewport `vefr look` does not offer: its `_session` in `src/vefr/devtools.py` fixes the viewport at 1280x800 and there is no flag for a phone. At 1280x800 with no `--steps` and no `--click` the two produce the same bytes (checked on this pack: both `6e596106239591edb7cb23b718ee7cf1672e44b4d71c0d7a6433ea2f047bffbc`), so the phone shot is the engine and not a drawing of it. It also takes `--click`, repeatable, which is how the rest of the shots were taken: `--click '#menu-open'` for the two `-menu` shots (tabs and corner studs), and `--click '#menu-open' --click '#menu .pm button:has-text("Bag")'` for the two `-bag` shots, which are the only place the slot is drawn.

**Rendering aids** — everything in `mock-renders/`: `mock-look-phone.png` and `mock-look-desktop.png` are drawn by `art/tools/mock_skin.py`, and `preview.html` (with its dated screenshot, `preview-2026-10-01-round-10.png`, which still shows the round-10 art) draws the parts one at a time. They are useful — `preview.html` hides the faults that only appear once the chrome is assembled, and the mocks got the round-two `tab-selected` pick caught — but they are not play evidence and they are not kept where a reader would take them for it. `mock-renders/README.md` says so at the top of that folder.

The difference is not fussiness. The mock got **both** of the round-two parts it could check wrong, in the same direction: `mock_skin.py` stretches a picture across a box it has no shape for, and so does the player — but the player's boxes are real, and they turned out to be 210x153 and 510x32 (desktop) and 156x194 and 308x32 (phone).

## What the preview showed (2026-10-01)

- Panels, speech box, buttons, tabs, bar, slots and the small pieces all read well and stay sharp when stretched.
- The panel's drawn rim is a flat parchment colour, so the mottled parchment texture inside it shows a faint inset rectangle. Two ways out, for whoever builds the loader: use a flat fill colour for panel insides, or bake the texture into the rim when the skin is built. A stretched `fill` made a visible quilt, so do not use it.
- The cursor is cream with a thin brown outline; check it is visible on parchment before it ships.
- The buttons are a little glossier than the painted pieces. Judge them beside the panels in the real game.

## What the game showed (2026-10-08, the round-two skin, in play)

Taken from the pack's own copy of the skin, in the running player, at 1280x800 and 390x844. One line per pick; "seen where" says which shot.

| Pick | What the running game did with it |
| --- | --- |
| **banner** | **Wrong as cut.** The player lays it across `.toasts` with `background-size: 100% 100%`, and that box is 210x153 on a desktop and 156x194 on a phone and a different height again per message. The ribbon's swallow tails dragged out past the panel as long flanges and its hems smeared into bars. Rebuilt as the parchment field inside the frame (`make_plate_field.py`), which reads as a clean warm face behind the message stack. Both sizes, `look-desktop.png`, `look-phone.png`. |
| **slot** | **Wrong as cut.** Same cause, worse: the player stretches it across `.equip-row`, a bag line 510x32 on a desktop and 308x32 on a phone, so a 64x64 framed slot became a hard band of glare down one side of every row. Rebuilt as the field inside the frame; the rows are now quiet parchment bands. `look-desktop-bag.png`, `look-phone-bag.png`. |
| **speech** | Legal and `check_ui`-clean, and **this pack cannot show it**: the box it paints is `#npc-box`, and `grep -ri npc worlds/cottage-of-the-breeze/` finds nothing — the pack has no NPCs, so there is nothing to say. Unproven in play, and it will stay that way until the pack has someone in it. |
| **tooltip** | Reads well. The 96x64 plate stretched onto the tool button's tooltip at 390x844 and 1280x800 stays a clean honey-rimmed card behind the word. `look-phone.png`. |
| **corner** | Reads well. The player draws it at a fixed 18x18 on `.carved` and `#config`, and the 48x48 cut scales down to a legible brass stud at the four panel corners. `look-desktop-menu.png`. |
| **bar-frame** + **bar-fill** | Read well. The fill sits in the frame's trough and the seam is invisible at both sizes, in the HUD health bar. Note for whoever builds the loader: the fill goes *over* the frame; the other way round the frame's opaque middle hides it. `look-desktop.png`. |
| **tab** + **tab-selected** | Read as one tab in two states, at both sizes — the selected chip is the same silhouette, lighter. The selected chip is derived, not cut; see `PROVENANCE.md` for why. `look-desktop-menu.png`. |
| **divider** | Legal, wired up, and **never seen**: the player paints it on `header.game-head`, which its own stylesheet hides with `body.in-game header.game-head { display: none }` for the whole of play, and on the title screen the header sits under `#title-screen` at `z-index: 100`. Photographing the header on its own shows the stitch, so the picture is right and the slot is unreachable. Left in place for whoever changes the engine; nothing in the art can fix it. |
| **cursor** | Legal and `check_ui` says `ok cursor` (hotspot `[4, 4]` is inside the 32x32 picture), but **a screenshot does not photograph the pointer** — the cursor is a CSS `cursor:` URL. Unproven in play, and no screenshot can prove it. |

Two things in the shots are the player's own, not this skin, and are left for the engine: the `.toasts-toggle` "Messages" button is still the flat dark `var(--glass)` and is the one dark thing on a parchment screen; and the panel's middle is the flat `var(--vefr-skin-ground)` sampled from the picture, which is why a wide panel shows a soft inner rectangle (still true from 2026-10-01). One thing checked and found fine: the `fonts` block asks for Crimson Pro, and the player does bundle it (`web/fonts/CrimsonPro-Variable.woff2`; `document.fonts` lists the face as loaded in the woven game).