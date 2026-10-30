# Cottage of the Breeze: from a slice to a game

Written 2026-10-01 from Rylee's picks: the story spine and ending; progression and stakes; more world; polish; and the random dungeon floor generator. The demo today is a vertical slice (see `DEMO.md`).

> **History (2026-10-12).** This plan's status column stopped being kept on 2026-10-04. The authored cellar it describes was replaced by the generated descent on 2026-10-08, and the release target is now "Section 1, story complete" (Rylee, 2026-10-11). Where things stand: `.project/CURRENT.md`.

> **2026-10-04:** Release 1 completed Act 1. Acts 2 and 3 are part of the plan and were left for later by Rylee's decision (`docs/plans/acts-2-3/PLAN.md`). The status column below is current; older notes elsewhere are history.

## The order, and why

| # | Piece | What it means | Status (2026-10-02) | Who |
| --- | --- | --- | --- | --- |
| 1 | Story spine | Working notes: `docs/story-spine-notes.md` (the root `STORY.md` stays Rylee's). | Beats written as agent drafts: the letter, the Keeper's replies, the King's-room note, a floor-2 note is still unwritten. Rylee chooses and rewrites. | Claude writes, Rylee chooses |
| 2 | Reactions and rules | The cat notices you; a note appears after a truth; the ending fires. `design/rules-when-then.md` in the vefr repo. | 12 rules: tutorial lines, key pick-ups, the ending (`complete-act`), the cat, and the Keeper and Regular after the end. All draft lines. | Claude and foremen |
| 3 | Equipment and progression | Growth (levels) and five slots of findable gear. | Growth (8 levels) and equipment are on: seven pieces of gear in five slots, four sold, three dropped. | foreman |
| 4 | Stakes | Turn the act's setting from "costume" (you cannot lose) to "story" or "stakes". | Not yet: needs an engine stakes mechanic. The King is tuned so a level-8 hero wins. | Claude and Rylee, by playing |
| 5 | Random floors | A new descent each run, from a seed. `design/random-floors.md` in the vefr repo. | **Phase 1 built** (the generator in Python and an exact browser twin). Floors 4-6 are generated once at build time meanwhile. Phase 2 (drawing a descent each run) is next. | foreman |
| 6 | More world | Monsters, items, notes, guardians and keys. | **Act 1 is complete (2026-10-04):** 6 floors, 3 Keybearers and the Cellar King, locks, the King's room and an ending, 8 unique cast monsters, the album (25 stickers). Acts 2 and 3: see `docs/plans/acts-2-3/PLAN.md`. | Claude and foremen |
| 7 | Polish | Walking frames, sound, the UI skin, a small tutorial moment, "this whole game is one file". | Skin, quiet screen, WASD, tutorial lines, About book, walk cycles in four directions, and nine soft synthesized sounds (one switch) are in. Music is not. | mixed |

## Rules for this plan

- Each step ends with a playable build in the gallery and a note in `DEMO.md` of what changed and what is still rough.
- Story passes go to Rylee one at a time. Nothing is canon until she picks it.
- Random floors keep the authored parts authored. The town, the tavern, the cottage and the last room are fixed. Only the cellar floors between them are generated.
- The ending must be reachable on every seed: the last room is placed by the generator, never left to chance.
