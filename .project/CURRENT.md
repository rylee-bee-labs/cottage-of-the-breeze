# CURRENT — Cottage of the Breeze

This file is a **router, not a snapshot**.

Cottage of the Breeze is a VEFR game/world pack. Game content and canon live
here; reusable engine capability lives in VEFR.

## Stage

**Act 1 is a cottage, a town, and one way down.** The door on town `[1,1]` is
the generated descent, and the descent is four Sections end to end — **cellar,
rootworks, siltworks, emberhall** — nine floors each, 36 floors down, then it
cycles. The hand-authored cellar (`floor-1`..`floor-6`, `king-room`) is gone,
and with it the Keybearer ladder, the three locked cellar stairs and the sealed
door. The Cellar King survives only as the cellar Section's `warden` key; the
other three Sections name their wardens the same way, and the descent does not
read that key at play time yet.

**Act 1 still ends.** The note under the wax seal lies in a chest on
`cellar-0-9`, and reading it fires `complete-act` — floor 9 of the first
Section, not the bottom of the 36-floor chain. The vault chest drops
`cellar-gems`. The hero starts at 10 hp. Every book the descent offers is in
the **cellar**; rootworks, siltworks and emberhall currently differ by their
creatures, their fog and their floor shape.

**How anything here is known.** `tests/playthrough/run.py` is how this game is
played and checked: it weaves the pack, plays it in headless Chromium with the
keyboard only, reads its route out of the pack itself rather than a list in the
bot, and writes `report.json` (`tests/playthrough/README.md`). A claim about
the game at play is that bot's or a player's, and it is written down where it
happened. `tests/assert_chest_drops.py` gates every PR.

## The one next step

**Play the descent on current `main` with the monsters in, at 1280×720 and at
390×844, and record what happens in `NOTES.md`.**

Two things make this the next step rather than another. The gentle start
(`world.json` → `player.hp` 6 → 10; the cellar's family weights 5/3/2/2 →
6/4/1/1) has never been walked — its own entry ends *Not proven: any walk*. And
the play-test report on file was written against `c1b645a`, before the authored
cellar went, so its top finding is already fixed and its "floors 3–9 are
unreachable" has never been tested against a 36-floor chain. The bot that can
do the walk is green on `main` as of cottage#122.

## Where to look

| Question | Source |
| --- | --- |
| what is fun and what is boring | `docs/playtests/2026-10-09-descent.md` — written against `c1b645a`, so read its ranked list against the pack as it is now |
| dated decisions, playtest history, what was tried and not proven | `NOTES.md`, newest first |
| canon | `STORY.md` — Rylee's alone; agents read it, never write it |
| story work | `docs/story/RESEARCH.md` (a study, not canon). **No story draft is on `main`.** Drafts live beside it as `DRAFT*.md`, are held for Rylee, and never auto-merge (`AGENTS.md`) |
| how the game is played and checked | `tests/playthrough/` — `README.md`, and `negative_control.py`, which breaks the route on purpose to prove the bot can fail |
| art and its provenance | `art/source/`, `art/skins/`, and the dated entries in `NOTES.md` |
| open work | GitHub Issues. The issues closed as not planned on 2026-10-07 are in `docs/BACKLOG.md` |
| engine capability and the limits below | `Rylee-Bee/vefr` — nothing in this repo edits it |
| a plan already written | `docs/plans/` (`release-1`, `acts-2-3`, `native-ui`), with its owning issue |
| game identity and scope | `BRIEF.md` + `DESIGN.md` |

## Not established

Say **UNKNOWN** rather than guessing any of these.

- **No build is claimed here.** `bin/publish-build.sh` and the gallery CLI are
  not runnable from an agent session, so this file asserts no milestone build
  and no gallery URL.
- **Half a Section is data the descent does not read.** `id`, `floors`, `size`,
  `rooms`, `fog`, `families` and `pattern` are read; `curve`, `loot.tier`, a
  family's `depth` range, `specials`, `tiles`, `warden`, `vault`, `elites`,
  `groups`, `stamps` and `pois` are not. No new tile art was cut for the three
  new Sections, because nothing would draw it.
- **A generated monster carries no `xp`,** so nothing on the descent levels the
  hero. The engine gaps found while repairing the bot are written up in
  `NOTES.md`.
- **`crown-seal` still drops nothing.** The `cellar-king` family names it and it
  is not in the item catalog. `tests/assert_chest_drops.py` passes because it
  does not read `blueprint.json`'s families — its known edge, in `NOTES.md`.
- **The seven engine limits in the play-test report are not filed as issues**
  (`gh` was not available to the worker). They are written out in full in the
  report; the coordinator must file them.
- **The deepest walk on record took the monsters away** — the bot's own
  default — so it proves the route, not a fight. What the 36 floors feel like
  with a hollow cricket in them is exactly the next step above.

## Resume

Run `lab enter` or `now-block --print .`, then inspect the issue/PR you are
actually working on. Read only the matching plan and the newest relevant owner
decision.

The previous Release-1 snapshot and dated NEXT/verification ledger remain in
Git history. Do not recreate a rolling build/status ledger here.

## Latest activity

All on `main`; each is written up in `NOTES.md` under its own date.

- **2026-10-08:** the descent is four Sections and 36 floors — `rootworks`,
  `siltworks` and `emberhall` after the cellar (cottage#118). The six books
  orphaned by the authored cellar's removal were re-homed and proved findable
  (cottage#113); the vault chest holds `cellar-gems` again (cottage#114).
- **2026-10-08:** the play-test report on the descent, with its evidence in
  `docs/playtests/logs/` and `screenshots/` (cottage#116).
- **2026-10-08:** all eleven round-two decorations are cut into the soft-wood
  skin and were seen in the running game at 1280×800 and 390×844 (cottage#117).
- **2026-10-08:** `tests/assert_chest_drops.py` runs on every PR (cottage#120).
- **2026-10-08:** the gentle start — `player.hp` 6 → 10 and the cellar's family
  weights reweighted, because the hero died on floor 2 (cottage#121). Not yet
  walked; that is the next step above.
- **2026-10-08:** `tests/playthrough/run.py` was red on `main` and is repaired;
  it reads its route out of the pack (cottage#122).