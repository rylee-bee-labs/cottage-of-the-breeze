# Round 18: soft-wood UI skin source pictures (2026-10-04)

## Round two

Rylee chose all eleven round-two sheets in the picker: all Codex, with none of the Wan Pro drafts picked. They are drawn, credited and cut into `skin-source/` (2026-10-08, the round-two cut step); the build still waits on Rylee.

Ten of the eleven are straight cuts. The eleventh, `tab-selected`, is derived: `missing/tab-selected/tab-selected_v3.png` came back as the parchment *panel* its prompt describes beneath the tab, not as the tab chip, so cut straight it was sliced and mirrored into a shapeless pale blob in the 96x40 tab slot. The chip is now `missing/tab/tab_v3.png` (also Rylee's) lightened toward that sheet's honey cream by `art/tools/make_selected_tab.py`, keeping the tab's own silhouette; the original cut is kept beside it as `tab-selected-panel-v3.webp` so the pick is still traceable.

Rylee's picks of 2026-10-04, chosen in the skin picker artifact (`ui-soft/PICKS.md`): panels **v3**, buttons **v1**,
bars and slots **v2**, tabs and toggles **v2**, textures **v1**, dividers **v1**, cursor **v1**, plus the first redraw of
each part that was missing from the batch sheets (`ui-soft/missing/` — speech, tooltip, tab, tab-selected, bar-frame,
bar-fill, slot, banner, corner). Her note on the two redraw sets: "these are all radically different ideas. can you
split it up some?" -> separate dividers and cursor sets, four close variations each. All pieces are agent-drafted
(Codex), `draft` until approved; every `.credits.txt` sits beside the sheet it belongs to, where it stays.

Source for the soft-wood skin. `ui-soft/skin-source/` holds one picture per part under exactly the source names
`build_skin.py`'s `PICTURES` table looks for (`panel.webp`, `button.webp`, ...): each cut with `split_sheet.py` from
the sheet that drew the part and saved as lossless WebP keeping its alpha, plus `parchment.png` at exactly 288 x 288
as a 3x3 grid (`check_tiles.py` clean) and `brass.png` reused unchanged from round 10. **Nothing is built into a skin
yet** — that is a later step and it waits on Rylee.

Sheets come back as one picture per file here, so the table says which sheet turned out to be which part (read off the
sheet each part was drawn in, not by looking at pictures).

| Sheet (under `ui-soft/`) | Part in `skin-source/` | Cut size |
| --- | --- | --- |
| `panels/panels_v3.png` | `panel` | 1116 x 464 |
| `missing/speech/speech_v1.png` | `speech` | 1170 x 560 |
| `missing/tooltip/tooltip_v1.png` | `tooltip` | 1192 x 712 |
| `buttons/buttons_v1.png` | `button` | 1334 x 397 |
| `missing/tab/tab_v1.png` | `tab` | 1529 x 488 |
| `missing/tab-selected/tab-selected_v1.png` | `tab-selected` (superseded in round two: that cut is replaced, and the chip is derived - above) | 1204 x 1043 |
| `tabs-toggles/tabs_toggles_v2.png` | `toggle-on` | 1321 x 469 |
| `missing/bar-frame/bar-frame_v1.png` | `bar-frame` | 1666 x 253 |
| `missing/bar-fill/bar-fill_v1.png` | `bar-fill` | 1953 x 121 |
| `bars-slots/bars_slots_v2.png` | `gold-plate` | 1636 x 474 |
| `missing/slot/slot_v1.png` | `slot` | 939 x 936 |
| `dividers/dividers_v1.png` | `divider` | 2100 x 112 |
| `missing/banner/banner_v1.png` | `banner` | 1881 x 461 |
| `missing/corner/corner_v1.png` | `corner` | 608 x 603 |
| `cursor/cursor_v1.png` | `cursor` | 592 x 661 |
| `textures/textures_v1.png` | `parchment` (via `process_tiles.py --grid 3x3 --tile 96`) | 288 x 288 |

## The backdrop, which is not a draft sheet

The soft-wood backdrop is not one of these sheets: it was drawn on 2026-10-05 with `offload image` (image-01) from one
prompt asking for `--n 2`, a seamless tileable honey-wood table surface. The run came back with **one** picture, and
its own record says so (`n: 1`, `success_count: 1`, one file). There is no second backdrop draft anywhere - the two
backdrop drafts that were not chosen never existed.

That one picture is the source of the backdrop the skin ships, so the source, the run record beside it
(`backdrop.json`) and its credits travel with the skin in the skin pull request (#96), the way AGENTS.md asks: beside
the picture they describe. They are not part of this round's draft sheets, and `ui-soft/backdrop/` is not a sheet
folder here.

## Notes from cutting

- Every sheet except one came back as a single piece, named straight from the table above. `bars-slots_v2.png` came
  back as four: the gold plate (1636 x 474) plus three small leaves (104 x 43, 105 x 82, 95 x 65). Cut all four with
  four `--names` and kept the biggest — the plate — as `gold-plate.webp`; the three leaves were dropped.
- `dividers-cursor/` is the first pass at the divider, banner, corner and cursor in one brief (2026-10-04, 12:02Z,
  four variations). Her "these are all radically different ideas" note came off that batch: `dividers/` and `cursor/`
  (15:39Z and 15:41Z) are the redraws that split it, and the banner and corner were redrawn under `missing/`. The first
  pass is kept here as a draft, superseded by all three.
- Not drawn in round 18: `button-hover`, `button-pressed`, `button-disabled`, `toggle-off` and the wood texture (the
  backdrop above is a different picture, and it ships with the skin). Her picks do not include the first four, so
  `skin-source/` does not hold them in any form; the build waits on her.
- `check_tiles.py ui-soft/skin-source` reports the pieces "wrong size" and "a transparent pixel" — it is a grid-tile
  checker and a cut-out piece is not a tile. Round 10's `skin-source/` reports the same way. The two textures,
  `parchment.png` and `brass.png`, both come back `ok`.
- Sizes here are the pieces cut tight from their sheets; `build_skin.py` is what slices them down to the skin's
  geometry. Round 10's notes about uniform panel borders, button gloss and cursor contrast are worth re-reading
  against these before anything ships.
- Each sheet folder keeps the run log of the batch that drew it (`*_batch.log`). A log is a transcript of the agent's
  own session, so the author's home directory is written `$HOME` and the Codex session id `<redacted>`; nothing else
  in the log is touched. `art/tests/test_run_logs.py` keeps both out of every run log in `art/source/`.

The softer, even-toned alternate wooden backdrop is wired into the Cottage skin as a draft pending Rylee's pick.

- **2026-10-08, after the skin was played.** Three of the eleven picks are now built *from* a cut rather than cut
  straight, because the running player showed two of them cannot be drawn at the sizes it gives them and a third
  arrived as the wrong half of its prompt: `tab-selected` (already recorded), plus `banner` and `slot`, both rebuilt
  as the parchment field inside their own frame by `art/tools/make_plate_field.py`. Each untouched cut is kept beside
  its derived picture as `banner-v3.webp` / `slot-v3.webp`, and `skin-source/PROVENANCE.tsv` marks the derived rows
  and carries the cuts unmarked. No pick changed; no sheet was redrawn.
