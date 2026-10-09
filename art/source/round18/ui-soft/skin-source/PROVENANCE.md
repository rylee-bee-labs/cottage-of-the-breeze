# Provenance of `skin-source/`

This folder holds one picture per part of the soft-wood skin, under the exact
source names `build_skin.py`'s `PICTURES` table looks for (`panel.webp`,
`button.webp`, ...). Every picture here came from a sheet that round 18 drew,
cut with `art/tools/split_sheet.py` and saved as lossless WebP, or from round
10 as a carry-over. None of it is hand-redrawn or rescaled — `build_skin.py`
owns the geometry and the mirroring.

## The eleven round-two picks

All eleven pieces come from the sheets Rylee picked on 2026-10-04
(`ui-soft/PICKS.md`): ten are cuts, and `tab-selected.webp` is derived from one
of them — see **The one pick that is not a straight cut** below. Each sheet has
its own `.credits.txt` beside it; that file is the attribution for the picture
here. The five picture rows the brief calls "round 18 never drew" are not from
round 18 sheets at all — see **Carry-overs** below.

| Part | Sheet (under `ui-soft/`) | Credits file |
| --- | --- | --- |
| `banner.webp` | `missing/banner/banner_v3.png` | `missing/banner/banner_v3.credits.txt` |
| `speech.webp` | `missing/speech/speech_v3.png` | `missing/speech/speech_v3.credits.txt` |
| `tooltip.webp` | `missing/tooltip/tooltip_v2.png` | `missing/tooltip/tooltip_v2.credits.txt` |
| `corner.webp` | `missing/corner/corner_v3.png` | `missing/corner/corner_v3.credits.txt` |
| `bar-frame.webp` | `missing/bar-frame/bar-frame_v2.png` | `missing/bar-frame/bar-frame_v2.credits.txt` |
| `bar-fill.webp` | `missing/bar-fill/bar-fill_v1.png` | `missing/bar-fill/bar-fill_v1.credits.txt` |
| `slot.webp` | `missing/slot/slot_v3.png` | `missing/slot/slot_v3.credits.txt` |
| `tab.webp` | `missing/tab/tab_v3.png` | `missing/tab/tab_v3.credits.txt` |
| `tab-selected.webp` | `missing/tab/tab_v3.png` (derived - see below) | `missing/tab/tab_v3.credits.txt` |
| `divider.webp` | `dividers/dividers_v2.png` | `dividers/dividers_v2.credits.txt` |
| `cursor.webp` | `cursor/cursor_v2.png` | `cursor/cursor_v2.credits.txt` |

`dividers/dividers_v2.png` came back as two pieces (a long stitched line, 2102
x 112, and a small "knot" beside it, 46 x 24). The brief asks for the cut
whose box matches the part's role in `build_skin.py` — `divider` is a `strip`
of (192, 16), a long horizontal element, so the long stitched line is the
right cut and the small knot is dropped (the same call `bars-slots_v2` made
for the three leaves: keep the big piece, drop the rest).

The other ten sheets came back as a single piece each, so the choice between
pieces did not arise.

`bar-fill.webp` was already a cut from `bar-fill_v1.png` in this folder; the
v1 pick is the round-two pick too, and re-cutting it from the same sheet
returned the same bytes (`2e59e3114e2e486f7acc6163d86bec4aaf85d81a32b9576a86de44e01b11749a`),
so the file is unchanged.

## The one pick that is not a straight cut: `tab-selected.webp`

`tab-selected.webp` is **derived, not cut**. It is `tab.webp` - Rylee's own
`tab_v3` pick - with every colour moved one step toward the honey cream that
`tab-selected_v3.png` is drawn in, by `art/tools/make_selected_tab.py`. Nothing
is redrawn, reshaped or resampled: the alpha is carried across untouched, so the
selected chip is the *same silhouette* as the tab at rest.

The reason is in the sheet. `missing/tab-selected/tab-selected_v3.png` was asked
for as "the same tab but selected: lighter honey wood, parchment face joined to a
parchment panel below", and what came back is the *panel* half of that sentence:
a 1312 x 1199 near-square parchment panel with a shallow tab bump along its top
edge, not a tab chip. Cut straight and built into the tab slot it is squeezed
into a 96 x 40 box and mirrored by `process_box`, and what reaches the player is a
pale stepped shape with its rim sliced off, sitting next to a perfectly good
`tab.webp`. A wrong-looking decoration is worse than no decoration.

So the cut is kept, under the name it actually is -
**`tab-selected-panel-v3.webp`**, byte for byte the cut of
`missing/tab-selected/tab-selected_v3.png`, sitting beside this file as the
record of the pick - and `tab-selected.webp` is built the way the prompt asked:
the tab chip she did pick, lightened toward the palette of the one she picked for
this slot. That is the whole of the adjustment, and `make_selected_tab.py` is
what makes it, so it can be re-run or undone.

The palette is the one thing `tab-selected_v3.png` is good for, and taking it from
there is why the provenance row for this part names `tab_v3.png` and its credits
rather than the sheet it was built to come from. `PROVENANCE.tsv` marks the row
`derived`, and carries `tab-selected-panel-v3` beside it as the unchanged cut.

## Carry-overs from round 10

Round 18 did not draw `button-hover`, `button-pressed`, `button-disabled`,
`toggle-off` or `wood.png` (see `ui-soft/../RECORD.md`, "Not drawn in round
18"). `build_skin.py` needs every row of `PICTURES` to build a skin, so those
five are copied **unchanged** from `art/source/round10/ui/skin-source/` into
this folder. They are round-10 carry-overs, not round-18 picks — pending
Rylee's eye, they are placeholders so the build can be run end-to-end, and
the skin is not to be built from them. The trail back to round 10 is
`art/source/round10/ui/RECORD.md`; round 10's own `.credits.txt` files sit
beside the round-10 batch sheets, not beside these cuts, and are not carried
over (the brief asks for them to travel with the art, but round 10's
attribution lives at the round-10 batch, which is the form round 10 itself
uses — see `RECORD.md`, "every `.credits.txt` holds the exact prompt").

| Part | Carried from (under `art/source/round10/ui/skin-source/`) |
| --- | --- |
| `button-hover.webp` | `button-hover.webp` |
| `button-pressed.webp` | `button-pressed.webp` |
| `button-disabled.webp` | `button-disabled.webp` |
| `toggle-off.webp` | `toggle-off.webp` |
| `wood.png` | `wood.png` |

## sha256 table

`PROVENANCE.tsv` is the machine-readable form: a header line, then one row
per source file with the part, the sheet path, the credits path, the
sha256 of the sheet (so a reviewer can check the cut against the picture it
claims to come from), and a marker in the fifth column: `carryover` on the
round-10 rows, `derived` on the one row that is not a straight cut (see above).
The table is sorted: picks first (in the order the brief lists them), then
carry-overs (in alphabetical part order). Path columns for picks are
repo-relative to `art/source/round18/ui-soft/`; the carry-overs' sheet
column is the filename in `art/source/round10/ui/skin-source/`.

`tab-selected-panel-v3` has no marker: it is an ordinary cut, kept because it is
the picture Rylee's `tab-selected` pick actually drew. It is not an input to the
build - `build_skin.py` reads `tab-selected.webp` - so it is kept beside this
file as the record of the pick, not as a part.
