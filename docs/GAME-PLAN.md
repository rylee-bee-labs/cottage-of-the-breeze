# Cottage of the Breeze: from a slice to a game

Written 2026-10-01 from Rylee's picks: the story spine and ending; progression and stakes; more world; polish; and the random dungeon floor generator. The demo today is a vertical slice (see `DEMO.md`).

## The order, and why

| # | Piece | What it means | Depends on | Who |
| --- | --- | --- | --- | --- |
| 1 | **Story spine** | Written: `docs/STORY.md`. Next: write the six small passes in its list. | nothing | Claude writes, Rylee chooses |
| 2 | **Reactions and rules** | The cat notices you; a note appears after a truth; the ending fires. `design/rules-when-then.md` in the vefr repo. | the rules foreman (in progress) | foreman, then review |
| 3 | **Equipment and progression** | Five slots, findable gear that changes attack and health, so the cellar is worth going down. `design/equipment.md`. | 2 not required, but shares the player | foreman |
| 4 | **Stakes** | Turn the act's setting from "costume" (you cannot lose) to "story" or "stakes" once there is gear and healing to balance it. One setting, plus tuning. | 3 | Claude and Rylee, by playing |
| 5 | **Random floors** | A new descent each run, from a seed. `design/random-floors.md` in the vefr repo. | the generator exists; needs a player-side port and parity tests | foreman |
| 6 | **More world** | Monsters, items, notes and a hidden room on every floor. Uses the named edits, so a person can do the same. | 2 for the hidden room | Claude and foremen |
| 7 | **Polish** | Walking frames, sound, the UI skin, the rain, a small tutorial moment, "this whole game is one file". | the skin tools (in progress) | mixed |

## Rules for this plan

- Each step ends with a playable build in the gallery and a note in `DEMO.md` of what changed and what is still rough.
- Story passes go to Rylee one at a time. Nothing is canon until she picks it.
- Random floors keep the authored parts authored: the town, the tavern, the cottage and the last room are fixed; only the cellar floors between them are generated.
- The ending must be reachable on every seed: the last room is placed by the generator, never left to chance.
