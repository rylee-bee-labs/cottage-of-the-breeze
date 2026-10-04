# Release 1 handoff (overnight 2026-10-03/04)

> Release 1 is a complete, polished Act 1. Acts 2 and 3 were left for later by Rylee's decision and remain part of the game. Current state lives in `.project/CURRENT.md`; this file is the record of the night.

## Morning report (written 2026-10-04 ~01:00; the game was done and published by then)
- **Play it:** https://gallery.hulganfamily.duckdns.org/cottage-of-the-breeze/builds/2026-10-04-26c21ee/ (build `26c21ee`, VEFR `77d8f68`-era main). Walk, E/F to interact, B for the bag, Menu for the Album and the Sound switch.
- **What it is now:** a complete act 1. Cottage, town, tavern, six floors; three sleeping Keybearers (moth, mushroom elder, beetle) each carry a key to the next stair; the Cellar King carries the crown seal; the sealed door opens a room with gems, a note and a way home; reading the note ends the act with an end card. Eight unique cast monsters, seven pieces of gear (Codex art), a 25-sticker album, nine soft synthesized sounds, a hero who walks in four directions, tutorial lines and an About book.
- **VEFR gained (all merged, tests first):** `complete-act` (#252), lock reachability in `vefr check` (#253), the album (#254), up-stairs label fix (#255), docs (#256), sound (#257), walk sheets (#258).
- **Checks run:** VEFR full suite 1682 passed; Cottage art tests 121 pass; `vefr check` and `norns validate` ok; a keyboard-only bot plays cottage to ending and home on desktop (1280) and phone (390), 34 checks, 0 console errors; axe-core 0 violations on the play screen, seven menu panels and the end card.
- **Merges and publish:** you approved merging in chat; every PR was merged after green CI (VEFR #252-#258, Cottage #78-#80) and a hand review of each worker diff. One build was published to the dev gallery (twice: release and polish).
- **Cleanup:** my merged worktrees, branches and foreman clones on Bazzite removed; local branches whose PRs had merged deleted (VEFR 6, Cottage 3). Kept: `olympics-2026-09-26` (no PR, 381 commits ahead) and the remote `vefr` branch `release-1` (my integration branch, merged; delete when you like).
- **Needs you:** keep/rewrite/bin every agent draft (see NOTES.md), name the three Keybearers, decide where acts 2 and 3 begin (`docs/plans/acts-2-3/PLAN.md`). Issues filed: vefr #259 (region display names for hints), #260 (`vefr look --at`).
- **Intentionally left for later:** acts 2 and 3 (Rylee's decision after Act 1; they stay part of the game, and act advance and status effects are the next capabilities because they will want them), music, stakes, walk frames for the other characters, a floor-2 note and the Keeper's long talk (Rylee's story).

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
*(A ranked discovery record of ten findings is in VEFR: `docs/research/cottage-release-1-learnings.md`.)*
- A story beat had no way to end: added `complete-act` (reusable; no Cottage names in VEFR).
- Nothing caught a softlocked lock: added the lock reachability check; it also refuses a sellable key.
- No sticker shelf for a game: added the album.
- Up-stairs said "down": fixed.
- **Not done, recorded:** `point-to` shows raw region ids (no region display names); no teleport/`--at` for `vefr look` (the `wake` setting did not move the start); music (the nine sound cues were added later in the night); act advance and status effects, which the later acts will need (`docs/plans/acts-2-3/PLAN.md`).

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
