# Round 10: UI skin source pictures (2026-10-01)

Codex proofs in 6 batched calls, 22 pictures (`training: not cleared`; each `.credits.txt` holds the exact prompt). Source for the parchment-and-carved-wood skin described in
`design/ui-skin.md` in the vefr repo. **Nothing is picked or processed into a skin yet.**

Pictures in a batch come back in any order, so the table says what each file turned out to be (identified by looking). `skin-source/` holds the same pictures under the
file names the skin design uses (`panel`, `button`, `button-hover`, ...), plus the three textures sized to exactly 288 x 288 as 3x3 grids (`check_tiles.py` clean).

| Batch | v1 | v2 | v3 | v4 |
| --- | --- | --- | --- | --- |
| `panels` | dialog panel | speech box with tail | tooltip | |
| `buttons` | pressed | normal | hover | disabled |
| `tabs-toggles` | selected tab | toggle ON | toggle OFF | unselected tab |
| `bars-slots` | gold plate | bar fill | bar frame | slot frame |
| `dividers-cursor` | title banner | corner ornament | vine divider | cursor arrow |
| `textures` | wood | brass | parchment | |

## Notes from review
- The panels' borders are close to uniform, which is what a nine-slice needs, but not exact. The planned `process_ui.py` mirror-fix (take one corner and edge, mirror them) is still untested on these.
- The four buttons are clearly one shape in four states. They are more glossy and 3D than the painted pieces; judge them against the panels before the skin ships.
- The cursor arrow is cream with a thin brown outline: check it is visible on parchment (it may need a darker outline).
- The slot frame is much bolder than the five slot outlines from round 9; they will need to be used as a pair (the frame around, the outline inside) or one of them redrawn.
- Textures tile without visible seams (2x2 check and `check_tiles.py`).
