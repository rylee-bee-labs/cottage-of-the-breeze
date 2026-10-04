# CURRENT — Cottage of the Breeze (handoff, 2026-10-04)

**Stage: Release 1 is a complete, polished Act 1, published and playable.** Start in the cottage, go down six cellar floors, beat three Keybearers for three keys, beat the Cellar King for the crown seal, open the sealed door on floor 6, read the note in the King's room, see the end card, walk home. One offline HTML file. It was built through VEFR (new capabilities went into VEFR first) over the night of 2026-10-03/04.

**Acts 2 and 3 are part of the larger game and were deliberately left for later: stopping after Act 1 was Rylee's decision.** Release 1 is not evidence that VEFR could not support more acts. Act advance (VEFR ADR 0006) and status effects (fire first) are the next capabilities *because* the future acts will want them. Plan: `docs/plans/acts-2-3/PLAN.md`.

**Verified state (2026-10-04):** latest published build `26c21ee` — https://gallery.hulganfamily.duckdns.org/cottage-of-the-breeze/builds/2026-10-04-26c21ee/ . Cottage #78-#81 and VEFR #252-#258 merged after green CI. `vefr check` and `norns validate` pass; art tests 121 pass; a keyboard-only bot plays cottage-to-ending-and-home on desktop (1280) and phone (390), 34 checks, 0 console errors; axe-core reports 0 violations on the play screen, seven menu panels and the end card; VEFR full suite 1682 passed. (Anything newer than `26c21ee` is docs and tests only until the native-UI work starts.)

## Start here
1. `AGENTS.md` (rules, art rights), then `NOTES.md` newest first (Rylee's words and decisions; agent drafts are marked).
2. Validate: `cd ../vefr && uv run vefr check --pack ../cottage-of-the-breeze/worlds/cottage-of-the-breeze` (VEFR on `main`; `check` also follows the locks).
3. Play it without a browser in front of you: from `../vefr`, `uv run --group test python ../cottage-of-the-breeze/tests/playthrough/run.py --pack ../cottage-of-the-breeze/worlds/cottage-of-the-breeze --viewport desktop` (also `phone`; `COTTAGE_SHOTS=<dir>` saves a screenshot per region and per fight). About three minutes; writes `tests/playthrough/report.json`. Accessibility: `tests/playthrough/axe_panels.py` beside it.
4. Publish a build after a merge: `bin/publish-build.sh` (records the cottage and VEFR revisions in `build-info.txt`). CI pins VEFR in `.github/workflows/validate-pack.yml` (`VEFR_REF`); repin deliberately when the pack contract changes.
5. The VM is small: do not run VEFR's full suite or the bot while a Codex or other heavy job runs.

## What is built (all in `worlds/cottage-of-the-breeze/`)
- Six floors, the King's room, town, tavern, cottage. 22 Blueprint families and 73 creature instances in `blueprint.json` (edit it, then `vefr normalize --pack <pack> --out <pack>` and `vefr check`). Eight unique cast monsters; three Keybearers and the Cellar King sleep until bumped (`sight: 0`); the King is 36 hp / 3 atk.
- Locks on stairs 3-4 (bell key), 4-5 (lantern key), 5-6 (helmet key) and the sealed door on floor 6 (crown seal). Keys are `keep` and carry no `value`; `vefr check` proves they are reachable and unsellable.
- Twelve rules in `world.json`: the letter and the Keeper, tutorial lines, key pickups, the cat, the ending (`the-seal-note-read` fires VEFR's `complete-act`), and two reactions after the end. 
- Eight wearable items in all five slots (four sold by the Trader, three dropped, the ring is a charm); an album of 25 stickers; nine soft synthesized sounds with a switch in Menu > Display (`"sound": {"theme": "soft"}`); a four-direction walk cycle for the hero (`sprites/hero-sheet.png` + `hero.sheet.json`); an About book.
- The floor 6 map was hand-edited for the sealed door at (11,1); a `vefr delve` rerun would overwrite it.

## Story status: playable draft is not canon
- **Canon:** `STORY.md` is empty. Nothing is canon until Rylee writes or picks it.
- **Approved by Rylee (decisions, not necessarily final words):** the Spell Keeper draft (2026-10-01), the story spine picks, the guardians' art and the last room's structure (a seal opens a treasure room with a lore note and a way back to town).
- **Playable agent drafts (marked in `NOTES.md`):** the King's-room note and the gems, the Keeper and Regular lines after the ending, the tutorial and key lines, the About book, the sticker, gear and Keybearer names (Keybearers ship as plain descriptions). Keep, rewrite or bin each; they are data and swap in minutes.

## Waiting on Rylee
- Keep/rewrite/bin every agent draft above, and name the three Keybearers and their keys.
- Where acts 2 and 3 begin and their themes (`docs/plans/acts-2-3/PLAN.md`); fire is the first effect (chosen 2026-10-04).
- Her interface direction (2026-10-04): everything inside the game in the game's own themed UI, no literal device frame, native to the world, cute and minimal. Plan: `docs/plans/native-ui/PLAN.md`; a Codex kit of soft HUD pieces is being drawn for a mock.

## Next, in order (Rylee's order, 2026-10-04)
1. VEFR: the in-world interface work and the `web/packaged.html` split (`../vefr/docs/plans/player-split/PLAN.md`), then act advance and status effects for the next acts. The VEFR roadmap board lists the rest.
2. Art: portraits in speech, hit and heal flashes, HUD icons, the mole and robed rat as town folk, walk sheets for other characters.
3. Story, written by Rylee: the floor-2 note (truth one), the Keeper after the letter (truth two), the final words.

## Known rough edges
- Region ids show raw in hints ("To reach floor-1"): VEFR #259.
- Existing saves repopulate the floors (new enemies change signatures). Start over for a clean run.
- The skin's slot, tab, toggle, tooltip, divider and banner pictures exist but the player does not draw them yet; the Messages button and the touch d-pad keep the plain style (native-UI plan).
