# CURRENT — Cottage of the Breeze

This file is a **router, not a snapshot**. Gameplay evidence below is from 2026-10-13 against Cottage `164fc81` and VEFR `84e61d1`; the **release-direction update** is from owner decisions on 2026-10-14. Do not treat these historical SHAs as current runtime pins.

Cottage of the Breeze is a VEFR game/world pack. Game content and canon live
here; reusable engine capability lives in VEFR.

## Stage

**Section 1 beta, with Gate 0 ACTIVE.** The owner revised the **1.0 release target on 2026-10-14** to a polished **complete four-Section / 36-floor story adventure**. The earlier 2026-10-11 **"Section 1, story complete"** target is now the **first quality gate**, not the public 1.0 finish line. No additional Section or gameplay system is declared finished by this decision.

**Active, owner-approved delivery plan:** [`docs/plans/release-1-0/ROADMAP.md`](../docs/plans/release-1-0/ROADMAP.md). **Confirmed game decisions:** [Cottage #168](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/168). **Engine dependency:** [VEFR #489](https://github.com/rylee-bee-labs/vefr/issues/489). **One rule:** polish beats expansion; protect existing canon and park non-essential features.

- **The way down is in the cottage kitchen**, `cottage [1,1]` (`world.json` →
  `descent.entry`; cottage#142). The town has no stair.
- **The descent** is four Sections, nine floors each: `cellar`, `rootworks`,
  `siltworks`, `emberhall` (`sections/*.json`). The pattern ends each one in a
  warden floor, and the landing on floor 5 records a way back.
  Each Section scatters its own decals (cobwebs, torches, puddles, cracks)
  over its floors through `decor` (vefr#442).
- **The Cellar King yields** (cottage#143). The cellar's warden is a `rule`
  challenge, not a fight. He gives `crown-seal` and sleeps.
- **The vault on `cellar-0-9`** holds the seal note. Reading it fires
  `complete-act` and sets `act-1-complete`, which is also the descent's
  `story_end`, so the stair past the cellar opens only after it.
- **The town changes once:** `town_states` loads `town-after-the-cellar` (the
  temple door propped open) after `act-1-complete`.
- **The town is GBA pixel art** (cottage#146): 34×26 tiles on VEFR's object
  layer. Residents stand in the way (`player.people_block`), and the hero
  starts with 10 gold. The cottage, the tavern and the cellar are still
  painted, and monsters and items are interim shrunk paintings (`*.px.webp`).
  The rest of the art set landed in cottage#151.
- **The interface is VEFR's storybook layout** (vefr#445, #446): the dark look
  first (`display.look`), the camera following her on a phone (`phone_tile`
  52) and at a desk (`desk_tile` 48), two buttons on a phone, and one message
  line that fades.

## The one next step

**Gate 0: complete and document the Section 1 beta human playthrough on desktop and a real phone**, with monsters enabled, then fix the witnessed blockers. Work starts at [Cottage #161](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/161); review [#157](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/157), [#165](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/165), and [#166](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/166). Do not call Gate 0 verified until the evidence exists.

The bot plays it end to end. On 2026-10-13 `tests/playthrough/run.py` passed
40 of 40 checks at 1280×720 and 390×844, with no console errors. Rylee played
the town on a phone and at a desk on 2026-10-13 and shaped the interface
(`NOTES.md`); a full Section 1 run by a person is still to come.

## Where to look

| Question | Source |
| --- | --- |
| active 1.0 delivery roadmap | `docs/plans/release-1-0/ROADMAP.md` (five quality gates; active Gate 0) |
| owner-confirmed 1.0 scope | Cottage GitHub issue #168; VEFR engine issue #489 |
| canon | `docs/story/STORY.md`, promoted 2026-10-09. The root `STORY.md` is an empty placeholder that is Rylee's to fill or retire; agents never write either |
| dated decisions and what was tried | `NOTES.md`, newest first |
| how the game is played and checked | `tests/playthrough/` (`README.md`, and `negative_control.py`, which proves the bot can fail) |
| Section 1 against canon | `docs/plans/section-1-beta/GAP.md` (written before cottage#142/#143/#146; read its slices against `main`) |
| what is fun and what is boring | `docs/playtests/2026-10-09-descent.md` (written against an older pack; history) |
| art and its provenance | `art/STYLE.md`, `art/source/`, `art/skins/`, and the dated entries in `NOTES.md` |
| open work | GitHub Issues. Issues closed as not planned on 2026-10-07 are in `docs/BACKLOG.md` |
| engine capability | `rylee-bee-labs/vefr`. Nothing in this repo edits it |
| older plans | `docs/plans/` (`release-1`, `acts-2-3`, `native-ui`) and `docs/GAME-PLAN.md`, **historical / superseded for 1.0 scope** |
| game identity and scope | `BRIEF.md` + `DESIGN.md` |

## Not established

Say **UNKNOWN** rather than guessing any of these.

- **No build is claimed here.** `bin/publish-build.sh` and the gallery CLI need
  Rylee's host, so this file asserts no build and no gallery URL.
- **Album stickers** (cottage#148, settled 2026-10-12). Six are chance drops
  from cellar rats, moths and spiders: a player gets them by playing, and the
  bot lists them without requiring them. `a-cold-ember` and
  `a-music-box-spring` now drop from the siltworks' deep shade (Section 3),
  Rylee's pick, so Section 1's album has 17 to find. The bot asks the tavern
  keeper for the tab and reads it.
- **The three Keybearers** (Ashwing, Brother Sporeling, Sir Hollowhorn; Rylee
  named them 2026-10-04, `NOTES.md`) are in canon and in `blueprint.json`,
  but no Section places them. Whether they belong in Section 1 is Rylee's
  call; placing a sleeping, non-fight guardian off the warden floor needs
  engine work (`docs/plans/section-1-beta/GAP.md` slice 6).
- **Every player-facing name and line is a draft** until Rylee approves it
  (`DEMO.md` says so to players).
- **Licence and audience.** `LICENSE.md` is all rights reserved; who the
  release is for and where the file lives are Rylee's to decide.

## Resume

Read `AGENTS.md`, then this file, then the issue you are working on. Validate
with `docs/commands.md`. Play with `tests/playthrough/README.md`.

The rolling dated ledger this file used to carry is in Git history and in
`NOTES.md`; do not rebuild it here.
