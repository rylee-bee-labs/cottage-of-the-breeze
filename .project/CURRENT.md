# CURRENT — Cottage of the Breeze (handoff, 2026-10-04)

**Stage: act 1 is a complete, playable game.** Start in the cottage, go down six cellar floors, beat three Keybearers for three keys, beat the Cellar King for the crown seal, open the sealed door on floor 6, read the note in the King's room, see the end card, walk home. All in one offline HTML file. Release 1 was built overnight 2026-10-03/04 on VEFR; plan in `docs/plans/release-1/PLAN.md`, handoff in `docs/plans/release-1/HANDOFF.md`.

## Start here
1. `AGENTS.md` (rules, art rights), then `NOTES.md` newest first (Rylee's words and decisions, and the agent drafts flagged for her).
2. Validate: `cd ../vefr && uv run vefr check --pack ../cottage-of-the-breeze/worlds/cottage-of-the-breeze` (VEFR on `main`; `check` now also follows the locks).
3. Play it through without a browser in front of you: `cd ../vefr && uv run --group test python ../cottage-of-the-breeze/tests/playthrough/run.py --pack ../cottage-of-the-breeze/worlds/cottage-of-the-breeze --viewport desktop` (also `phone`; `COTTAGE_SHOTS=<dir>` saves a screenshot of each region). It takes about three minutes and writes `tests/playthrough/report.json`.
4. Publish a build after a merge: `bin/publish-build.sh` (records the cottage and VEFR revisions in `build-info.txt`).
5. The VM is small: do not run VEFR's full suite or the bot while a Codex or other heavy job runs.

## What is built (all in `worlds/cottage-of-the-breeze/`)
- Rules: 12 in `world.json`, including `the-seal-note-read` (ends the act with VEFR's `complete-act`). All lines are agent drafts.
- Creatures come from `blueprint.json` (22 families, 73 instances; edit it, then `vefr normalize --pack <pack> --out <pack>` and `vefr check`). Keybearers and the King have `sight: 0`: they sleep until bumped. The King is 36 hp / 3 atk.
- Locks: stairs 3 to 4 (bell key), 4 to 5 (lantern key), 5 to 6 (helmet key); the sealed door on floor 6 (crown seal). Keys are `keep` and have no `value` so they cannot be sold; `vefr check` enforces it.
- Gear: hearth shovel, copper ladle, patched apron, quilted coat, cooking-pot helm, mended boots, thread bell, and the brass ring as a charm. Album: 25 stickers (`album` in `world.json`).
- The floor 6 map was hand-edited for the sealed door (11,1); a `vefr delve` rerun would overwrite it.

## Waiting on Rylee (nothing here is canon until she says)
- Keep, rewrite or bin every agent draft: the King's-room note, the treasure (gems), the end card line is VEFR's, the Keeper and Regular after the ending, the tutorial lines, the About book, the sticker names, the gear names.
- Proper names and epithets for the three Keybearers and their keys (they ship as plain descriptions).
- Where acts 2 and 3 begin, their themes, and which effect fantasy comes first (`docs/plans/acts-2-3/PLAN.md`).
- Merge `Rylee-Bee/cottage-of-the-breeze` PR for `release-1/ladder` if it is not merged yet.

## Next, in order
1. VEFR: act advance (ADR 0006), then status effects (`../vefr/design/elemental-and-status-effects.md`): both are needed for acts 2 and 3.
2. Art: walking frames; the mole and robed rat proofs as town folk; props in the King's room.
3. Sound: the engine has none; design it first (VEFR #144).
4. Story: the floor-2 note (truth one) and the Keeper after the letter, written by Rylee.

## Known rough edges
- Region names show raw in hints ("To reach floor-1, go north-west"): `point-to` accepts only region ids today.
- Existing saves repopulate the floors (new enemies change signatures). Start over for a clean run.
- The Messages panel keeps an old "found a book" line for a while.
