# CURRENT — Cottage of the Breeze

This file is a **router, not a snapshot**. Gameplay evidence below is from 2026-10-13 against Cottage `164fc81` and VEFR `84e61d1`; the **release-direction update** is from owner decisions on 2026-10-14. Do not treat these historical SHAs as current runtime pins.

Cottage of the Breeze is a VEFR game/world pack. Game content and canon live
here; reusable engine capability lives in VEFR.

## Stage

**Section 1 beta, with Gate 0 ACTIVE.** The owner revised the **1.0 release target on 2026-10-14** to a polished **complete four-Section / 36-floor story adventure**. The earlier 2026-10-11 **"Section 1, story complete"** target is now the **first quality gate**, not the public 1.0 finish line. No additional Section or gameplay system is declared finished by this decision.

**Active, owner-approved delivery plan:** [`docs/plans/release-1-0/ROADMAP.md`](../docs/plans/release-1-0/ROADMAP.md). **Confirmed game decisions:** [Cottage #168](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/168). **Engine dependency:** [VEFR #489](https://github.com/rylee-bee-labs/vefr/issues/489). **One rule:** polish beats expansion; protect existing canon and park non-essential features.

- **The way down is in the cottage kitchen**, `cottage [1,1]` (`world.json` →
  `descent.entry`; cottage#142). The town has no stair.
- **The descent** is four Sections: `cellar` is eight floors, the other
  three nine each: `rootworks`, `siltworks`, `emberhall`
  (`sections/*.json`). The pattern ends each one in a
  warden floor, and the landing on floor 5 records a way back.
  Each Section scatters its own decals (cobwebs, torches, puddles, cracks)
  over its floors through `decor` (vefr#442).
- **The Key Warden yields** (cottage#173). The cellar's warden is a `rule`
  challenge, not a fight. The challenge comes first: the hero keeps the
  rule the warden keeps, which sets `warden:key-warden:c0`, and that flag
  is what awards the `cellar-gems` the warden carries.
- **The vault on `cellar-0-8`** holds the ending note. Reading it fires
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

## Gate 1 (the RPG core), built; not yet played by a person

The engine half is
[VEFR #586](https://github.com/rylee-bee-labs/vefr/pull/586) (ADR 0021, merged
2026-10-29 as `275a6ff`, which `validate-pack.yml` pins), and the cellar uses it
from cottage#220 (rolled blows, guard, a read `curve`, drops and gold, a stocked
Trader, traits and curses, mana and three spells, the deepest-landing stair,
falls that wake at home). On 2026-10-29 the playthrough bot passed 44/44 with
monsters at 1280×720 and 390×844, with two falls each. Rylee approved every new
word as written
([`WORDS-BATCH-1.md`](../docs/plans/release-1-0/WORDS-BATCH-1.md), 2026-10-29).
Balance is a first guess; Gate 0's human run below is still the gate that
decides "ready".

## The one next step

**Gate 0: complete and document the Section 1 beta human playthrough on desktop and a real phone**, with monsters enabled, then fix the witnessed blockers. Work starts at [Cottage #161](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/161); review [#157](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/157), [#165](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/165), and [#166](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/166). Do not call Gate 0 verified until the evidence exists.

The bot plays it end to end. On 2026-10-13 `tests/playthrough/run.py` passed
40 of 40 checks at 1280×720 and 390×844, with no console errors. Rylee played
the town on a phone and at a desk on 2026-10-13 and shaped the interface
(`NOTES.md`). **Rylee's first full Section 1 run came on 2026-10-30** (cottage#161): "feels easy" and "almost straight lines to every staircase". The fix is winding floors (vefr#589, ADR 0022) and a harder cellar (cottage#222); the bot passes it 44/44 at both sizes, with 4 falls. Her later notes ("spells and combat and gear weren't really there", monster skills, ranged attacks) and her picks are on #161. The "show it" pass is VEFR #590 (ADR 0023): a spell card, "Wear it?", hit numbers and a quick bar, all four turned on in `world.json`. Monster skills are VEFR #591 (ADR 0024): web and spit, a festering bite, dust and a squeal, carried by the four cellar families. Throwing waits for her pick of the thing's name (`WORDS-BATCH-2.md`). Gate 0 is not verified until she plays the new build.

## Where to look

| Question | Source |
| --- | --- |
| active 1.0 delivery roadmap | `docs/plans/release-1-0/ROADMAP.md` (five quality gates; active Gate 0) |
| the fifteen player loops, what the engine does today, and the engine companion list | `docs/plans/release-1-0/LOOPS.md` (2026-10-29; analysis and plan, nothing built by it) |
| what art the game uses and what to draw next | `python3 art/tools/art_manifest.py audit`, `art/manifest/` (slots, template), `art/requests/` (generated image-agent briefs) |
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
  (`DEMO.md` says so to players). The pack's books carry `status: draft` so the
  release check lists them (cottage#159,
  [`docs/plans/release-1-0/DRAFT-TEXT.md`](../docs/plans/release-1-0/DRAFT-TEXT.md));
  voice prompts, whispers, `world.json` lines and Section labels are the same
  unapproved words in formats with no place to put the mark yet.
- **Licence and audience.** `LICENSE` is MPL-2.0 for code; creative content is CC BY-SA 4.0 (`LICENSE-CONTENT.md`), chosen by Rylee 2026-10-17; who the
  release is for and where the file lives are Rylee's to decide.

## Resume

Read `AGENTS.md`, then this file, then the issue you are working on. Validate
with `docs/commands.md`. Play with `tests/playthrough/README.md`.

The rolling dated ledger this file used to carry is in Git history and in
`NOTES.md`; do not rebuild it here.
