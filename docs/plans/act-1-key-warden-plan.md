# Act 1 rebuild: 8–11 floors with a Key Warden — plan

**Status: PLANNING ONLY.** Nothing in this repository was changed by the work
that wrote it: no pack file, no story text, no canon. This file is the bounded
plan the issue asks for, so that the first implementation step is a decision
with evidence behind it.

**Decision this implements** (Rylee, rolling interview #11, 2026-10-16,
cottage#173 comment 6221797831), verbatim:

> "For Cottage #173, I choose A: rebuild Act 1 into an 8–11-floor Key Warden
> adventure and move the Cellar King to Act 3, with story/canon changes
> separately reviewed."

**What that authorises here:** writing this plan, comparing the shipped Act 1
to the goal, identifying engine dependencies in VEFR, and saying what needs
Rylee's words. **What it does not authorise:** rewording dialogue, character
lore, preserved text or story beats; any content edit; publication; a merge or
deploy. The A/B/C structural question is settled — do not re-ask it without
materially new evidence. The canon gate in the decision stands: structure is
approved, **words are not**.

---

## 1. What the playable Act 1 is today

All verified against this tree on 2026-10-16; the commands are in §9.

| Thing | Where | Fact |
|---|---|---|
| Act 1's descent | `world.json:817-833` (`descent`) | `run_seed: "breeze"`, entry `cottage [1,1]`, `story_end: "act-1-complete"`, four Sections: `cellar`, `rootworks`, `siltworks`, `emberhall` |
| Act 1's own regions | `acts/act-1/world.json` | `town`, `cottage`, `tavern`, `town-after-the-cellar`; `town_states` swaps in the last on `act-1-complete` (`world.json:834-843`) |
| Section 1's shape | `sections/cellar.json:3-71` | `floors: 9`; `pattern` is 9 entries and its last is `warden` |
| The warden | `sections/cellar.json:87-94` | an object, not a family name: `family: cellar-king`, `id: cellar-king`, `carries: crown-seal`, `challenge: rule`, `yields: true`, `fightable: false` |
| The Cellar King beat | `world.json:528-546` | rule `cellar-king-yields` fires on `reads forty-winters`, sets `warden:cellar-king:c0` (`world.json:265`) |
| How Act 1 ends | `world.json:313-331` | reading `a-note-under-the-seal` sets `act-1-complete`, fires `complete-act: act-1`, shows one narrator line |
| The ending room | `library/a-note-under-the-seal.md`, `library/forty-winters.md` | both `region: cellar-0-9`, `place: near-up`; the note is a chest that drops `cellar-gems` |
| Keys already in the pack | `world.json:245-259`, rules `:548-586` | `lantern-key`, `bell-key`, `helmet-key`, each given by reading one of three Keybearer notes |
| Whether the Keybearers are placed | `grep keybearer sections/ acts/` | **no hit.** The families exist in `blueprint.json:96-128` and the notes place them narratively, but no Section spawns them. Nothing gates on the three keys either (`grep requires` finds nothing) |

So today's Act 1 is a nine-floor generated Section whose last floor holds the
Cellar King, his seal note, and the note that ends the act. That is the whole
structure the decision replaces — and it is worth saying plainly that **almost
all of it is recoverable**: no authored floor contracts exist (cottage#118
deleted `floor-1..floor-6` and `king-room`), the descent is generated from
`sections/*.json`, and the only floor-bound hand content is nine library notes'
`region:` lines.

## 2. The delta, as a table

| | Shipped Act 1 | Owner-approved Act 1 |
|---|---|---|
| Floors | 9 (`sections/cellar.json:4`) | 8–11 (decision) |
| Last floor | `warden` = the Cellar King | `warden` = the Key Warden |
| The King | yields his seal on floor 9 | belongs to Act 3 |
| Act 1's ending note | `a-note-under-the-seal` on `cellar-0-9` | must end on the Key Warden beat — **which note is Rylee's call** (§5) |
| Total 1.0 floors | 4 × 9 = 36 (ROADMAP) | 35–38. A scope consequence to record, not to resolve here |

## 3. The one hard constraint that decides the shape of the work

**A Section's `pattern` is one entry per floor and its last entry must be the
kind of floor that ends the Section** (`sections/cellar.json:62-71`). `floors`
and `pattern` cannot disagree. So a floor-count change is *not* one number: it
is one number plus a rebuilt `pattern`, and every `cellar-0-N` string in the
pack has to be re-pointed at the new floor it names.

This is the whole migration surface, and it is nine lines:

| Note | Region today | What breaks if the floor moves |
|---|---|---|
| `a-letter-in-a-chest.md` | `cellar-0-1` | floor 1 is stable under any 8–11 choice |
| `a-scrap-in-the-dust.md` | `cellar-0-1` | same |
| `a-coin-face-down.md` | `cellar-0-3` | stable while the count is ≥ 3 |
| `a-candle-and-a-note.md` | `cellar-0-5` | stable; the `landing` on 5 is the recorded way back |
| `the-pale-moth.md` | `cellar-0-5` | same |
| `the-old-mushroom.md` | `cellar-0-7` | **breaks at `floors: 8`** — the note is unreadable and the rule that gives `bell-key` never fires |
| `the-stag-beetle.md` | `cellar-0-8` | **breaks at `floors: 8`** |
| `forty-winters.md` | `cellar-0-9` | **breaks at any count below 9**; it is also the Cellar King's beat |
| `a-note-under-the-seal.md` | `cellar-0-9` | **breaks at any count below 9**; it is also Act 1's ending |

Two of those nine are the Cellar King's, and the decision says he leaves Act 1.
That is why this is not a one-line change, and why §5 is the owner's question
rather than an agent's.

## 4. Recommended first implementation step (smallest thing that is real)

**Recommendation: Act 1 = `cellar` at `floors: 8`, ending on a Key Warden
warden beat.** 8 is the bottom of the approved range, which keeps the run as
near to its shipped length as the decision allows and leaves 9/10/11 available
as a later tuning step rather than forcing the decision now.

The machinery this needs already ships and is proven by the King:

- `sections/cellar.json:87-94`'s `warden` block is a slot, not a hard-coded
  boss. A new `key-warden` family in `blueprint.json` fills that slot with
  `challenge: rule`, `yields: true`, `fightable: false`.
- `yields` already means "no fight, the hero is given something"
  (`world.json:528-546`), so the Key Warden arc starts from working code.
- The `landing` on floor 5 (the recorded way back) is kept, so recovery is
  unchanged.

Then, still pack-only, in order: re-point the four floor-bound notes; give the
Key Warden his own flag in the `warden:<id>:c0` form the King already uses;
leave the Cellar King family in `blueprint.json` untouched (unplaced is
recoverable — that is how the Keybearers have sat since 2026-10-04).

**What this step deliberately does not do.** It does not place the three
Keybearers. They need a named, asleep, non-fight guardian slot that does not
exist yet (`docs/plans/section-1-beta/GAP.md` slice 6); the Key Warden is the
`warden` slot, which works today. Keeping the two apart is what makes this the
*first* step.

## 5. The one question this plan cannot answer for Rylee

If the Cellar King leaves Act 1, the seal note that currently ends the act has
two honest homes and both cost something:

- **(a) Re-home.** The existing `a-note-under-the-seal` and `forty-winters`
  notes move to the Key Warden's floor, unchanged. No new words, Act 1 keeps a
  tested ending and the end card, and the King waits for Act 3 with his beat
  intact. Cost: Act 1's last page still talks about a crown in red wax, so the
  Key Warden arc ends on the King's seal — a structural inconsistency the
  owner may or may not want on screen.
- **(b) Re-cut.** Act 1 ends on a Key Warden note that is new words, and the
  King's two notes move wholesale to Act 3. Cost: new player-facing text, so
  it goes through the canon gate in the decision, and the end card is a beat
  nobody has played yet.

(b) is the shape the decision describes more faithfully. (a) is the smaller
step and needs no new words. **Rylee chose (b) Re-cut, 2026-10-16** (recorded on #173): Act 1 ends on a new Key Warden note, the King's
two notes move to Act 3, and the new note goes through the canon review before it ships. Everything in §4
except the last bullet is safe to build under either.

## 6. Saves

Storage surface, verified from this tree: browser `localStorage`, keys prefixed
`vefr-` (`tests/playthrough/run.py:1299-1303`); the pack declares
`saves: {rules: "persist", legacy: "from-log"}` (`world.json:609-612`).

What a floor-count change touches:

- **Floors are part of a save's identity.** A region's name carries its floor
  (`cellar-0-9`), and a save records the hero's region and per-region explored
  bitsets (the bot reads them back at `run.py:381-388`). A save made standing
  on `cellar-0-9` names a region an eight-floor Section cannot produce. What the
  engine does with that — clamp, drop or refuse — is **UNKNOWN** until the
  engine is read (§7, U-S1).
- **Rule state persists.** `rules: persist` means a rule that fired stays
  fired, so an old save will not replay `cellar-king-yields` even though its
  text moved. `legacy: from-log` reconstructs from the Why log, which keeps 20
  entries (`NOTES.md:1206`), so a beat older than the log can replay once.
- **The flag vocabulary carries across.** `act-1-complete`,
  `warden:cellar-king:c0` and every album sticker (`world.json:261-266`) are
  saved. A save that already read the seal note is already "Act 1 complete"
  under any new shape, which is the recoverable part: her bag, level and
  discoveries are intact and Rylee's "Keep and it moves on" direction
  (`NOTES.md:55`) is not in question.
- **Floors repopulate anyway.** New or changed enemies change signatures, so
  floors repopulate on an old save; the standing guidance is "start over for a
  clean run" (`NOTES.md:1195`).

Migration options, in the order this plan would test them: **(i)** leave an
orphaned floor orphaned and say so in `DEMO.md` — honest, costs an old save's
descent position; **(ii)** clamp the hero to the deepest floor the new Section
can produce, in the engine, so old descent saves remain loadable and the
town side of the save is never at risk; **(iii)** version the save and refuse
old ones with a clear message. (ii) is the recommended target behaviour, and
it is an engine change, so it is a companion change, never an edit to
`../vefr/`.

**Preservation rule for whoever builds this:** no save may be made worse by
the rebuild. Losing a floor's position is acceptable; losing the bag, the level,
the flags or the ability to return to town is not, and neither is a silent
soft-lock on a region that no longer exists.

## 7. VEFR dependencies (companion changes, not edits here)

| # | Dependency | Why Act 1 needs it | State |
|---|---|---|---|
| E1 | Act advance (ADR 0006) | The Cellar King cannot be *played* in Act 3 until `complete-act` can hand the hero to another act's start region | **UNBUILT** per `docs/plans/acts-2-3/PLAN.md:9`; Act 1's King therefore becomes unplaced data until it exists |
| E2 | Descent reads Section fields | `warden`, `specials`, `curve`, `tiles`, family `depth` are not all read at play time (`docs/plans/section-1-beta/GAP.md` slice 5, U2). The Key Warden itself only needs `warden`, which works | UNKNOWN from here |
| E3 | Named asleep guardian slot | Only if the Keybearer ladder joins Act 1. GAP slice 6. **Not needed for §4** | UNBUILT |
| E4 | Save clamping on an orphaned region | §6 (ii) | UNKNOWN (U-S1) |
| E5 | Draft listing for new text | Any new Key Warden words must reach `vefr check --release`'s draft list, as cottage#159 did for books | Works for `library/` front matter; formats without front matter are open |

This clone has no `../vefr` and no `~/code/Rylee-Bee/vefr`, and no `uv`, so
none of E1–E5 could be read or run here. They are UNKNOWN from this tree, not
absent from the engine.

## 8. Needs separate review before any of it is written

- **Every new word.** The Key Warden's name, anything he says, anything a new
  note says. Draft, held for Rylee, per `AGENTS.md` and the decision's own gate.
- **The §5 choice** — whether the seal note keeps ending Act 1 or its ending
  moves to Act 3.
- **The Cellar King's Act 3 home.** Section 3's wardens already exist
  (`root-warden`, `silt-warden`, `ember-warden`); placing a `cellar-king`
  Section is an owner-level placement call, and it cannot ship before E1.
- **Canon conflicts the move touches**, from
  `docs/plans/section-1-beta/GAP.md` (C1–C3): the stair's location, whose
  letter it is, and the crown seal that canon does not have. `docs/story/STORY.md`
  is Rylee's; this plan does not touch it or root `STORY.md`.
- **Gate 0 evidence must not certify the superseded build.** The 2026-10-13
  40/40 bot run and Rylee's phone/desktop play are evidence *for the nine-floor
  descent*; the decision says human beta must reflect the revised Act 1, so
  Gate 0 re-opens against whatever actually ships.

## 9. Checks this plan was written against

```
$ python3 tests/assert_chest_drops.py
blueprint families checked: 33 … ok: every drop the pack names resolves to a real item with a real sprite   (exit 0)

$ python3 tests/assert_draft_text.py
books marked status: draft: 14 of 14; pack text files inventoried: 35 of 35
ok: every book is a marked draft and the inventory names every text file in the pack   (exit 0)

$ python3 tests/assert_tutorial_line.py
ok: tutorial walking line names the arrow keys, W A S D and the joystick   (exit 0)

$ grep -rn "keybearer" worlds/cottage-of-the-breeze/sections/ worlds/cottage-of-the-breeze/acts/
(no hit — the three Keybearer families are placed by no Section)

$ grep -rn "requires" worlds/cottage-of-the-breeze/
(no hit — no transition gates on a key)
```

Not runnable from this sandbox, and the host re-runs them:
`norns validate --pack worlds/cottage-of-the-breeze` (needs a VEFR checkout
and `uv`), and `tests/playthrough/run.py` on desktop and phone (needs Playwright).
The bot derives floors from each Section's `floors` and `pattern` and re-points
itself at the vault, so it should follow a floor-count change — that has to be
**proved by running it**, not assumed.