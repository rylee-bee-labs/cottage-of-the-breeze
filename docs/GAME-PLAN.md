# Cottage of the Breeze: from a slice to a game

Written 2026-10-01 from Rylee's picks: the story spine and ending; progression and stakes; more world; polish; and the random dungeon floor generator. The demo today is a vertical slice (see `DEMO.md`).

## The order, and why

| # | Piece | What it means | Status (2026-10-02) | Who |
| --- | --- | --- | --- | --- |
| 1 | Story spine | Working notes: `docs/story-spine-notes.md` (the root `STORY.md` stays Rylee's). | The three beats are picked. Written so far: the letter and the Keeper's reply (drafts). Still to write: the floor-2 note, the Keeper's talk, the lore note in the King's room, the ending. | Claude writes, Rylee chooses |
| 2 | Reactions and rules | The cat notices you; a note appears after a truth; the ending fires. `design/rules-when-then.md` in the vefr repo. | Rule state now survives a reload (`saves.rules: persist`). Started: 2 rules (read the letter, then the Keeper answers). The cat, the Regular and the Smith do not react yet. | Claude and foremen |
| 3 | Equipment and progression | Growth (levels) and five slots of findable gear. | **Growth is on** (8 levels). Equipment is designed (`design/equipment.md`), not built. | foreman |
| 4 | Stakes | Turn the act's setting from "costume" (you cannot lose) to "story" or "stakes". | Not yet: it needs gear and the guardians to balance it. | Claude and Rylee, by playing |
| 5 | Random floors | A new descent each run, from a seed. `design/random-floors.md` in the vefr repo. | **Phase 1 built** (the generator in Python and an exact browser twin). Floors 4-6 are generated once at build time meanwhile. Phase 2 (drawing a descent each run) is next. | foreman |
| 6 | More world | Monsters, items, notes, guardians and keys. | 69 monsters on 6 floors (now generated from a Blueprint, `blueprint.json`); the engine can lock a stair, and the first lock will be floor 3 to 4 with an actual key (Rylee, 2026-10-02), not placed yet; 5 guardians drawn and approved; 8 more monster drafts, doors, six keys, treasure and props drawn (unwired). A real act 2 waits for the engine (ADR 0006). | Claude and foremen |
| 7 | Polish | Walking frames, sound, the UI skin, a small tutorial moment, "this whole game is one file". | **Skin in** (parchment-and-wood), the quiet screen, WASD and the declutter are done. Sound and walking frames are not. | mixed |

## Rules for this plan

- Each step ends with a playable build in the gallery and a note in `DEMO.md` of what changed and what is still rough.
- Story passes go to Rylee one at a time. Nothing is canon until she picks it.
- Random floors keep the authored parts authored. The town, the tavern, the cottage and the last room are fixed. Only the cellar floors between them are generated.
- The ending must be reachable on every seed: the last room is placed by the generator, never left to chance.
