# Soft-wood skin picks (Rylee, 2026-10-04, via the skin picker artifact)

Chosen: panels **v3**, buttons **v1**, bars and slots **v2**, tabs and toggles **v2**, textures **v1**.
Dividers and cursor: **redraw**. Her note: "these are all radically different ideas. can you split it up some?" -> separate dividers (a stitched line with a small knot) and cursor sets, four close variations each (`dividers/`, `cursor/`).
All pieces are agent-drafted images (Codex), status draft until approved.

## Round two

Chosen by Rylee in the 2026-10-04 round-two picker (Codex vs Wan Pro): **All Codex. Wan Pro was not picked for any piece.** These are chosen drafts awaiting Rylee's cut-into-the-kit step.

| Part | Chosen sheet (under `ui-soft/`) |
| --- | --- |
| Title banner | `missing/banner/banner_v3.png` |
| Speech box | `missing/speech/speech_v3.png` |
| Tooltip | `missing/tooltip/tooltip_v2.png` |
| Panel corner | `missing/corner/corner_v3.png` |
| Bar frame | `missing/bar-frame/bar-frame_v2.png` |
| Bar fill | `missing/bar-fill/bar-fill_v1.png` |
| Item slot | `missing/slot/slot_v3.png` |
| Tab | `missing/tab/tab_v3.png` |
| Tab, chosen | `missing/tab-selected/tab-selected_v3.png` |
| Divider | `dividers/dividers_v2.png` |
| Cursor | `cursor/cursor_v2.png` |

## Backdrop

Both `backdrop-1.jpg` and `backdrop-alt-1.jpg` exist as draft options. `backdrop-alt-1.jpg` is wired into the skin for review; Rylee picks between them before either ships.

## Status

- **2026-10-08:** the eleven round-two picks are cut into `art/source/round18/ui-soft/skin-source/` (commit `9657082`, the round-two cut step), with `PROVENANCE.md` and `PROVENANCE.tsv` naming the sheet each cut came from; the skin is built from those cuts into `art/skins/parchment-and-wood/` and the part pictures copied into the pack's copy of the skin (`worlds/cottage-of-the-breeze/skins/parchment-and-wood/`), still on Crimson Pro and `backdrop-alt-1.webp`. The five pieces round 18 did not draw (`button-hover`, `button-pressed`, `button-disabled`, `toggle-off`, `wood.png`) are round-10 carry-overs, unchanged. Picks themselves unchanged.
- **2026-10-08 (second pass, looking at it in play):** ten of the eleven are cuts and are unchanged. The eleventh, **tab-selected**, is not: the sheet `missing/tab-selected/tab-selected_v3.png` came back as the *panel* half of its prompt ("a parchment panel below" the tab) rather than as the tab chip, so built into the 96x40 tab slot it read as a pale stepped shape with its rim cut off. The pick is unchanged and still hers; the cut is kept as `tab-selected-panel-v3.webp`, and the chip `tab-selected.webp` is now derived from the tab pick (`tab_v3`, which she also chose) lightened toward that sheet's honey cream, by `art/tools/make_selected_tab.py`. Same silhouette as the tab at rest, so the two chips read as one tab in two states. See `skin-source/PROVENANCE.md`.
- **2026-10-08 (third pass, looking at it in the actual game):** all eleven have now been seen in the running player at 1280x800 and 390x844, and two more could not be drawn as cut. The player lays the **banner** and the **slot** across a whole box rather than nine-slicing them, and neither box has a shape a picture can assume (`.toasts` is 210x153 on a desktop, 156x194 on a phone, and taller again with more messages; `.equip-row` is a bag line about 510x32), so the ribbon's tails smeared into flanges and the slot's bevelled corner into a band of glare. Both now ship as the parchment field inside the ornament's own frame, made by `art/tools/make_plate_field.py`, with the untouched cuts kept beside them as `banner-v3.webp` and `slot-v3.webp`. Picks themselves unchanged and still hers. Also recorded now: the **divider** is right but the engine never draws it during play, and the **speech** box cannot be seen at all because this pack has no NPCs. See `skin-source/PROVENANCE.md` and `art/skins/README.md`.
