# Release 1 handoff (overnight 2026-10-03/04)

Mission `cottage-release-1`. Plan: `PLAN.md` (Opus, with corrections found while building). Everything below is on `release-1/ladder` (Cottage) and merged to VEFR `main`.

## What was built, by workstream
| Task | What | Where | Evidence |
|---|---|---|---|
| V1 | `complete-act` rule action (end card, once per save) | VEFR #252 | `tests/test_complete_act.py` (11), tests first |
| V2 | `vefr check` follows locks (unreachable key, behind its own lock, sellable key) | VEFR #253 | `tests/test_lock_reachability.py`, foreman-built, reviewed |
| A1 | Album slice 1 (stickers by rule events, Menu > Album) | VEFR #254 | `tests/test_album.py` (12), foreman-built, reviewed; full suite 1652 pass |
| fix | Up-stairs say "Go up the stairs" | VEFR #255 | found from playthrough screenshots |
| C1/C3 | Keybearer ladder, locks, keys, King | Cottage pack | `vefr check`, bot |
| C4 | King's room, sealed door, ending rule | Cottage pack | bot reaches the end card and home |
| C5 | Tutorial lines, About book, reactions, ring as charm | Cottage pack | validator |
| C7 | Keyboard-only playthrough bot | `tests/playthrough/` | desktop and phone, all checks |
| C8-C10 | Deep tiles, 8 cast monsters, 7 gear items (Codex art), album stickers | Cottage pack, `art/source/round14-15` | contact sheets reviewed |
| C2 | Art briefs tests repaired (#63) | `art/tests` | 121 pass |

## Gaps Cottage taught VEFR (and what was done)
- A story beat had no way to end: added `complete-act` (reusable; no Cottage names in VEFR).
- Nothing caught a softlocked lock: added the lock reachability check; it also refuses a sellable key.
- No sticker shelf for a game: added the album.
- Up-stairs said "down": fixed.
- **Not done, recorded:** `point-to` shows raw region ids (no region display names); no teleport/`--at` for `vefr look` (the `wake` setting did not move the start); music (sound cues were added later in the night: VEFR `sound`, nine synthesized cues, one switch); status effects and act advance (needed for acts 2 and 3, see `docs/plans/acts-2-3/PLAN.md`).

## Decisions made without Rylee (reversible)
- Guardian art picks: moth, mushroom elder, stag beetle; mole and robed rat held back (`art/source/round11/PICKS.md`).
- The Keybearers and King are asleep until bumped (`sight: 0`); the King is 36 hp / 3 atk, found by the bot (40/4 beat a level-8 hero).
- Treasure is gems; the lore note, the Keeper/Regular lines, tutorial lines, About book, sticker names and gear names are **agent drafts** (flagged in `NOTES.md`; nothing in `STORY.md`).
- Gear icons: Codex set (round 15) chosen over the MiniMax set (round 14, kept as alternates).
- Merging: Rylee approved merges in chat; VEFR PRs were merged after green CI and a hand review of every foreman diff. The Cottage PR (#78) is left for her unless it merged.
- Cottage CI pin moved from a916ce4 to VEFR main (it must be repinned deliberately after VEFR changes the pack contract).

## How the night went (tools)
Opus planned once. Foremen/workers on Bazzite built V2 (MiniMax foreman), A1 (foreman), the bot and the art-test repair (workers); each diff was read before use and two needed fixes (bot ordering, King balance). Codex drew the gear. Lessons are in VEFR `.project/DECISIONS.md`.

## Verify
`cd ../vefr && uv run vefr check --pack ../cottage-of-the-breeze/worlds/cottage-of-the-breeze`; the bot command in `.project/CURRENT.md`; `uv run --offline --with pillow python -m unittest discover -s art/tests -t .`.

## Added later in the night (after the first merge)
- VEFR `sound` (#257): nine synthesized cues, opt-in per pack, one switch in Menu > Display. Cottage opts in (`"sound": {"theme": "soft"}`). The bot checks that all nine fire.
- VEFR walk sheets (#258): the hero walks in four directions (Codex sheet, `art/source/round16/walk/`, in `sprites/hero-sheet.png` + `hero.sheet.json`). The bot checks every direction shows walk frames.
- Process slip: one art-source-only commit (the walk sheet source, `79071f7`) went straight to Cottage `main` instead of through a PR; it touches no game files. Everything after is on `release-1/polish`.
