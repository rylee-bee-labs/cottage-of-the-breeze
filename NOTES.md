# NOTES — decisions and playtest notes (newest first)

## 2026-10-08 (later still) — the five descent books are pinned to a place, not a tile (agent)

VEFR `b5ed13d` (vefr#361) taught the descent to place books by **anchor**
rather than by tile: a book with `place: near-up | near-down | anywhere`
names the stair it belongs to, and the floor draws its tile from that
floor's own `book|<id>` stream every run. Five of our books still carried
an `at:` on a `cellar-0-*` floor — a tile that is redrawn on every New
descent — and the engine now refuses that outright
(`vefr/src/vefr/library.py:281`: *"a book with place takes no at"*). This
is that fix. **Front matter only: the `at:` line is deleted and replaced
by a `place:` line, and not one word of any book's prose is touched.**

| Book | Was | Now | Why there |
| --- | --- | --- | --- |
| `a-scrap-in-the-dust` | `cellar-0-1` [27,36] | `place: near-up` | "A scrap of paper on the floor, older than the stair." It lies at the foot of the stair you arrive on, which is the same reading the fixed tile gave it (two steps from where the stair puts you). |
| `a-letter-in-a-chest` | `cellar-0-1` [23,34] | `place: anywhere` | Still a chest, still `drops: brass-ring`, still mid-floor rather than at the door (the fixed tile was eight steps in). The research's own example is *the letter is in an open chest she opened for the ring*, so it belongs where the searching takes her, not at the arrival. The one floor-1 book that is not `near-up`, and the reason is the ring. |
| `a-coin-face-down` | `cellar-0-3` [52,46] | `place: near-up` | "Deliberate, not dropped", and "it reads like someone's habit, not yours" — a habit is the tile every arrival walks past. Same reading as the fixed tile (four steps off the arrival stair). |
| `a-candle-and-a-note` | `cellar-0-5` [30,41] | `place: near-up` | Floor 5 is the Section's **landing** — its up-stair goes straight back to town. "Someone sat here a long while, and never came back up" belongs by the way home, which is what `near-up` is on that floor. |
| `a-note-under-the-seal` | `cellar-0-9` [37,29] | `place: near-up` | "You made it down. Good. Sit a moment; the stairs are long." … "Take what you found. Take it up." It is written to someone who has just arrived at the foot of a stair and is being sent back up it, so it sits by the stair she came down. `near-down` is the other honest reading ("the stairs ahead are long"); this one follows the note's own "Take it up" / "it knows the way home". |

**The sixth re-homed book (`a-burned-page`, `town`) is not touched.** Town
is an authored floor and does not move, so its `at:` is still the right
field for it — and its tile names the ruin on the map.

**Does the cellar's ninth floor have a down stair?** Yes, and it is worth
saying why because `a-note-under-the-seal` is the one book whose floor is
a Section's last. `cellar` declares `floors: 9`
(`sections/cellar.json:4`) and `world.json`'s `descent.sections` chains
four Sections, so the run is 36 floors; the walk recorded above crossed
**depth 9→10** — `cellar-0-9` into `rootworks-0-1` — using that stair, on
three seeds. A `warden` floor is not the bottom of the descent (the
descent rolls on into `cellar-1-1`), so `near-down` would have been legal
there too. It is not used, for the reason in the table.

**Not run here, and not claimed.** This clone has no VEFR, no `uv` and no
network, so `norns validate`, `vefr check` and the 200-run pin sweep are
the landing machine's to run, not this entry's to assert. `python3
tests/assert_chest_drops.py` passes here, so both `drops:` books still
resolve (`brass-ring`, `cellar-gems`).

## 2026-10-08 — the Cellar King drops something real; three dead key names are gone (agent)

The entry below closed the chest and left one line on the record: *"The
Cellar King still drops `crown-seal`, and the three Keybearer families
still drop `bell-key`, `lantern-key` and `helmet-key`. None of those
four ids are in the catalog either... **It should not stay unfixed.**"*
This is that.

**The defect, confirmed rather than assumed.** Four item ids are named in
`blueprint.json` and nowhere else in the pack, and none is in
`world.json`'s `items`. `norns validate` and `vefr check` both print
`ok:` on that pack — the one-floor-up twin of the chest that shipped
green. The id is discarded twice and silently: `_drop_ids`
(`vefr/cli.py:1794`) keeps a drop only when the catalog names it, and
`placeDrops` (`web/packaged.html`) returns before `floor.push` for an id
the catalog does not have. Nothing errors; the walk succeeds; the Cellar
King simply drops nothing.

### The table, and the reason for each line

| id | verdict | what it is now, and why |
| --- | --- | --- |
| `crown-seal` | **restored as a real drop** | The Section's `warden` is `cellar-king`, so this one is actually reachable: it is the Cellar King on floor 9, the one thing at the bottom of the descent a player earns. Restored through the Blueprint's `things` list (`vefr normalize` writes `/items/crown-seal`; the lock tracks the pointer), never hand-edited into a contract. The sprite is `seal-crown`, which is the picture the art was **authored** for this exact object — `art/briefs/gaps.md`: *"the Cellar King's seal, a round wax seal pressed with a crown"* — so the name promises only itself and not a door. |
| `bell-key` | **removed** | Named by `keybearer-moth`. **That family never spawns**: the cellar Section's `families` are `cellar-rat`, `nest-of-moths`, `damp-shade` and `cellar-spider`. Its door was an authored floor cottage#110 deleted. Nothing in `acts/`, `world.json` or `sections/` gates on it (`grep -rn 'requires\|lock'` finds no gate). |
| `lantern-key` | **removed** | As above, from `keybearer-mushroom` (also never spawned). |
| `helmet-key` | **removed** | As above, from `keybearer-beetle` (also never spawned). |

**Why three names go rather than three items come back.** Guardians,
keys and vaults are Rylee's step 4, recorded in her approved order as
**E8 vaults**, and E8 is not built (filed as vefr#341). `vefr/sections.py`
says so in as many words: "The warden, the vault and the key that opens
them are E8's". Restoring three items today would put three keys in a
bag with no door to spend them on — a name promising more than the game
delivers — for three mobs that never appear. **The three families keep
their records, sprites and named characters** (Ashwing, Brother Sporeling,
Sir Hollowhorn) so E8 can draw on them; only the dangling `drops` line
is gone.

**What the Cellar King drops now: "the Cellar King's wax seal"**
(`crown-seal`, sprite `seal-crown`, `value` 150). It follows `cellar-gems`
(`value` 120, cottage#114): a treasure with a picture and no invented
mechanics. `value` 150 rather than 120 because the warden's drop should
beat the chest's — a number, not a promise. **No existing words were
changed anywhere**: no book, note, name or line was touched; the only
words added are the item's own name, which did not exist before.

### A check that was missing, now in the repo

`tests/assert_chest_drops.py` covered chest books only, so it passed on
this pack with all four ids dangling. It now asserts, for **every** place
the pack names a drop — Blueprint families (following `extends`), a
Section's `families` and `warden`, act contract `enemies[].drops`, and a
chest book's `drops` — that the id is in `world.json`'s `items`, has a
`sprite`, that the sprite is a real entry in `player.sprites`, and that
the file is on disk. A Section naming a family the Blueprint does not
define is flagged too: that draws no mob and says nothing, which is the
same defect one level up.

**Proven to bite, five ways, each reverted:** deleting `/items/crown-seal`
(the exact original defect) → `FAIL … blueprint family 'cellar-king':
names 'crown-seal', not in world.json items`; putting `bell-key` back on
a family → the same for `keybearer-moth`; an item whose sprite is not in
`player.sprites`; an item whose sprite has no file; a Section naming a
family that is not there.

**The result that matters:** with `bell-key` back on `keybearer-moth` and
the pack freshly `vefr normalize`d so nothing is stale,
`norns validate` and `vefr check` both print
`ok: … geometry, reachability, voices all pass` while the assertion exits
1. That is the whole point — the validators cannot see this class of bug.

`tests/playthrough/warden_drops.py` (new, beside the existing browser
bot) is the woven read-back: it weaves the pack, opens the HTML in
headless Chromium and asks the page what the descent's mobs drop, through
the globals the engine itself reads. On the old weave it prints
`FAIL … crown-seal (named by cellar-king (warden))`; on the new one
`ok: every drop the descent names is in the catalog with a baked picture`.

**Left out on purpose.** `tests/assert_chest_drops.py` now checks far more
than chests and its filename says otherwise — renaming it is a
coordinator's call, not something this change should make silently. It
is also not run by CI: `.github/workflows/validate-pack.yml` runs only
`norns validate`, so a dangling id could still reach `main` unless
someone wires the assertion into the workflow. And the three Keybearer
sprites (`key-bell`, `key-lantern`, `key-helmet`) are now unclaimed by
any item; they stay in `player.sprites` and on disk, waiting on E8's
decision, which is not this task's.

**Evidence, and its edge.** `norns validate` and `vefr check` print `ok:`;
`vefr normalize` reports `fresh`; the assertion exits 0; the headless
read-back resolves `crown-seal` to `{name: "the Cellar King's wax
seal", sprite: "seal-crown", value: 150}` with the picture baked into
`VEFR_SPRITES` as a real PNG, so the bag draws it and not a fallback dot.
The read-back of the *before* weave and of the *after* weave are the two
sides of the fix above. **No player fought the Cellar King**: the
read-back is the running game's own baked state read from a real
browser, which proves the id resolves and the picture is there, not that
someone walked nine floors and picked it up.
## 2026-10-08 (later still) — `.project/CURRENT.md` back to truth, and three things it had to stop saying (agent)

This entry exists because the correction needed recording, not because anything
in the pack moved. `main` did not change in this pass; `.project/CURRENT.md` and
this line are the whole diff.

**What was false.** The last "Latest activity" entry in `CURRENT.md` said the
Keybearer ladder, the Cellar King, the sealed door and Act 1's ending are gone
from the pack. Three of those four clauses were wrong and one had become true
again:

- The descent is **four Sections and 36 floors** — `cellar > rootworks >
  siltworks > emberhall` — not one cellar (cottage#118). `world.json` →
  `descent.sections` names all four.
- **Act 1 still ends.** `a-note-under-the-seal` sits in a chest on `cellar-0-9`
  and its `reads` rule fires `complete-act`; the vault chest drops
  `cellar-gems` (cottage#113, cottage#114). The claim that the generated
  descent has no ending "until E8 lands" was true when the authored cellar went
  and stopped being true when the books were re-homed.
- **The Cellar King is in the pack as data** — `sections/cellar.json` names him
  in `warden`, and `blueprint.json` carries the family. What is true is
  narrower and now says so instead: the play-time descent does not read
  `warden`, so he is named rather than spawned. The old sentence and the
  "he drops a wax seal" note could not both stand, and the wrong one went.
- The authored `floor-1`..`floor-6` and `king-room`, the Keybearer ladder, the
  locked stairs and the sealed door **are** gone (cottage#110). That clause was
  right and is kept.

**Two things the brief this pass answered from was wrong about, checked rather
than passed on:**

- **There is no `docs/story/DRAFT.md` on `main`.** `docs/story/` holds
  `RESEARCH.md` and nothing else; `git log --all -- docs/story` shows the story
  draft has never landed here. `AGENTS.md` names `DRAFT.md` as the *convention*
  for where a draft would go, which is what the brief read as a file. So
  `CURRENT.md` routes to `RESEARCH.md` and says plainly that no draft is on
  `main`, rather than pointing a reader at a path that 404s.
- **The play-through bot's recorded count is 31 checks, not 33.** `NOTES.md`
  2026-10-08 ("the play-through bot walks the descent a player walks") records
  `31/31 checks, ok=True, 897 steps` at 1280×720; the `34/34` in
  `docs/playtests/logs/authored-route-*.txt` is the pre-cottage#110 authored
  route. `CURRENT.md` therefore does not quote a check count at all — it points
  at the run and its output.

**What `CURRENT.md` says the next step is, and why.** Play the descent on
current `main` with the monsters in, at both viewports, and record it. The
gentle start (cottage#121) says *Not proven: any walk*; the play-test report on
file describes `c1b645a`, before the authored cellar went and before the gentle
start, so its top finding is fixed and its "floors 3–9 are unreachable" has
never met a 36-floor chain. The bot that can do it is green as of cottage#122.

**Not a build claim.** `bin/publish-build.sh` and the gallery CLI are not
runnable from an agent session, so no milestone build and no gallery URL is
claimed anywhere in this pass. `CURRENT.md` says so under "Not established".

**Evidence.** `world.json` → `descent.sections` and `player.hp`; `sections/*.json`
(four files, `warden` each); `blueprint.json` → `families["cellar-king"]`;
`library/a-note-under-the-seal.md` (`region: cellar-0-9`, `chest: yes`,
`drops: cellar-gems`); `world.json` → `rules` → `the-seal-note-read` fires
`complete-act`; `docs/story/` holds one file; `git log --all --oneline -- docs/story`;
`python3 tests/assert_chest_drops.py worlds/cottage-of-the-breeze` → exit 0.
**Not run here:** the walk itself, and `norns validate` / `vefr check` — there is
no VEFR checkout and no `uv` in this clone, and this pass changed no pack file.

## 2026-10-08 — the first floor is full, not strong (agent)

The descent asks: make floor 1 survivable for a brand-new hero, under Rylee's
"Rising" answer — **"gentle near the top, some fights to fear deeper down"** —
without flattening the curve. This entry answers the first half with numbers
and changes two lines. **The second half is not done here, and the reason is
not a tuning judgement: the fix that floor 1 actually needs is an engine gap,
and this clone had no engine.** Read the "What could not be done" section
before treating any of this as a finished job.

### The shape of the problem, measured

The play-test logs carry five generated floors. Their monster count against
their walkable tiles:

| floor | walkable | monsters | density |
|---|---|---|---|
| `cellar-0-1` (run-1) | 602 | 20 | 1 per 30.1 |
| `cellar-0-1` (run-2) | 855 | 28 | 1 per 30.5 |
| `cellar-0-1` (run-3) | 1065 | 35 | 1 per 30.4 |
| `cellar-0-2` (run-3) | 781 | 26 | 1 per 30.0 |

Five independent floors, one density to within half a tile: **the descent
spawns one monster per thirty walkable tiles.** That is not a number the pack
sets anywhere — it is engine policy derived from floor area, which is what
finding B3 says.

Now the same measurement on the **authored** cellar, the floors this game was
actually balanced around, from `logs/authored-route-desktop.txt`:

| floor | walkable | monsters | density |
|---|---|---|---|
| `floor-1` | 440 | 6 | 1 per 73.3 |
| `floor-2` | 592 | 10 | 1 per 59.2 |
| `floor-3` | 654 | 13 | 1 per 50.3 |

The authored cellar ran at **one monster per fifty to seventy tiles** and the
play-test bot cleared it green, floor by floor, on both viewports. The
generated cellar runs **2.4 times denser**. So the anomaly is not that the
monsters got stronger — the cellar's monsters are the softest in the descent
(4–5 hp, 1–2 attack, and two thirds of the pool is `cellar-rat` and
`nest-of-moths` at 4 hp / 1 attack) — **the anomaly is how many of them there
are.**

The sharpest single number in the logs is the one careful run:
`FLOOR depth=0 … hp=6/6` then, after crossing **one** floor, `FLOOR depth=1 …
hp=1/6`. Five of six hit points spent on floor 1, and 35 monsters still
standing behind the hero. A hero with a six-point damage budget and no healing
item anywhere on the floor cannot survive 35 encounters. That is arithmetic,
not opinion.

**So: count, not hit points, not attack.** Which is inconvenient, because
count is the one thing the pack cannot reach.

### What changed

Two lines, both in keys the play-time descent really reads (`id`, `floors`,
`size`, `rooms`, `fog`, `families`, `pattern` — the seven from the Sections
entry above; nothing was set on `depth`, `curve`, `loot.tier` or a new `mobs`
key, because the first is inert at play time (vefr#351) and the other three
are not read either. A setting the engine never reads would look exactly like
a successful fix, so none were written).

- **`world.json` — `player.hp` 6 → 10.** The hero now takes 10 hits from the
  common cellar rat (1 attack) or 5 from a cellar spider (2 attack), instead
  of 6 and 3. `atk` stays at 2, and that is deliberate: at 3 attack a 4 hp rat
  still takes two swings, so the raise buys nothing against the 77% majority
  of the pool while making the emberhall bottom measurably easier — the wrong
  direction for a "rising" curve.
- **`sections/cellar.json` — family weights 5/3/2/2 → 6/4/1/1.** The cellar's
  two gentle families carry more of the floor; the two 5 hp families are rarer,
  and with them the cellar's only `atk 2` monster. The floor's expected damage
  goes from 1.17 to **1.00** and its expected hp from 4.33 to **4.17**.

### The curve still rises

Measured the same way for every section (family weights × Blueprint stats,
`extends` resolved):

| Section | hp avg | max atk on a floor | fog | before → after |
|---|---|---|---|---|
| cellar | **4.17** | 2 | 5 | 4.33 → 4.17 |
| rootworks | 6.88 | 3 | 6 | unchanged |
| siltworks | 9.06 | 3 | 4 | unchanged |
| emberhall | 10.88 | 4 | 3 | unchanged |

Monotone on every measure, and the bottom is untouched: a hollow cricket is
still 11 hp at 4 attack and still kills the hero in **three** hits while
needing six swings to kill. Only the top moved, which is what "gentle near the
top" asks for.

### What could not be done, and why

**The engine was not in this clone, so none of this was played.** There is no
`vefr` checkout, no `uv`, no `norns`, no browser, and no network credential to
fetch one. That means `norns validate`, `vefr check`, `vefr normalize` and the
three-seed walk **were not run**. The numbers above are arithmetic over the
Blueprint and the play-test logs, not a recorded walk. **Floor 1 is not proven
survivable, and nothing here should be described as if it were.** CI will run
the validators on the pull request; the walk is still owed and is listed as the
next step below.

**The count cannot be fixed from the pack as the engine stands, and this is
the real finding.** Count comes from area at one per thirty tiles, and area
comes from `size` and `rooms`. Those are the only keys that reach it. Cutting
them to bring floor 1 near the authored cellar's six monsters means redrawing
every cellar floor — and two floor-1 books are placed at fixed tiles
(`a-scrap-in-the-dust` at `[27,36]`, the letter chest `a-letter-in-a-chest` at
`[23,34]`), coordinates that were flood-verified against **the current**
layout. Shrinking the floors would put them in walls or out of bounds, which is
the exact silent failure the "six orphaned books" entry above was written about:
a book naming a region or tile that does not resolve simply cannot be found,
and neither validator flags it. Trading "the hero dies on floor 1" for "floor 1
has nothing in it" is a loss, not a fix. **So the geometry was left alone, and
that is the one lever big enough to work is the one lever not taken.**

Two smaller things for whoever has the engine:

- **A `mobs` (or density) key the descent actually reads would close this in
  one line.** `shapes.SECTION` would validate it; the descent would have to
  read it. Until then the count is the coin-flip B3 describes and no Section
  file can stop it.
- **A heal on floor 1 was the obvious second lever and was left out on
  purpose.** `library/a-letter-in-a-chest.md` already carries `chest: yes` and
  `drops: brass-ring` on floor 1, and adding `cloudy-potion` would have been a
  front-matter-only edit. But the front matter here is `drops: <comma list>`
  and the engine's own list syntax could not be checked without it — if it
  wants a YAML list, the id parses as one string and the chest opens **empty**,
  which is the vault-chest bug from the entry below, one floor up.
  `tests/assert_chest_drops.py` parses the comma form, so it would have gone
  green and proved nothing. **Left out deliberately**, not forgotten.

**The Blueprint was not touched, on purpose.** Editing `blueprint.json` at all
changes its `source_sha256`, which `blueprint.lock.json` records; that hash is
not reproducible outside the normalizer (it is not the file's bytes, nor any
`json.dumps` form of it — checked), so any Blueprint edit here would have left
the lock stale and CI red with no way to refresh it. The family *weights* live
in the Section file, which is outside the lock, so the change above was made
where it can be made honestly.

### Not boring

The cellar keeps all four of its creatures — nothing was deleted, only
reweighted — and floor 1 still carries two found objects, the scrap and the
letter chest with its brass ring (+1 attack, a real first-floore keepsake). No
reflexes and nothing to memorize is untouched: nothing about the change asks
the player to react faster or remember anything.

**Evidence.** `sections/cellar.json:11-14`, `world.json:76`; play-test logs
`docs/playtests/logs/descent-desktop-seed-run{1,2,3-sneak}.txt`,
`docs/playtests/logs/authored-route-desktop.txt`; the Sections entry above for
the seven read keys. **Not proven:** any walk.

## 2026-10-08 — the play-through bot walks the descent a player walks (agent)

**Before:** `tests/playthrough/run.py` had been red on `main` and on the
three-Sections branch alike since cottage#110, failing on
`"no open route from town to floor-1"` — `4/8 checks, ok=False`, in two
steps. It was not a game bug. cottage#110 made the generated Section the
only way down from town `[1,1]` and deleted the authored `floor-1`..`floor-6`
and `king-room`; the bot's route was a list of those seven regions. **Now:**
`31/31 checks, ok=True, 897 steps`, at 1280×720.

**The route is read out of the pack, not written down in the bot.** The
entry tile is `world.json` → `descent.entry`; the floors are each Section's
own `id`/`floors`/`pattern`; the stairs are the transitions the engine wires
on arrival; the books are `VEFR_LIBRARY`; and **the book that ends the act is
found by reading the pack's own rules for `complete-act`**, not by a
hardcoded id. Cottage → town → `[1,1]` → every floor of every Section
(`cellar-0-1`..`cellar-0-9`), opening every book on the way → the vault on
the warden floor, whose note ends the act → back up to town → a reload →
Start over → a fight on the way down. Move a floor, a book or a landing in
the pack and this bot follows it. The loop is over Sections, not over
`floor-1`..`floor-6`, so the four-Section chain is evidenceable the day a
second Section exists; **this pack declares one** and the run says so.

**Three harness bugs the old bot would have had, found by walking the real
game rather than by reading it.** (1) It cached `VEFR_REGIONS` and
`VEFR_TRANSITIONS` at page load, but a generated floor is grown *on arrival*
(`397-the-descent.js` `ensureRegion`/`wireFloor`) — so the tables had no
`cellar-0-2` and routing could never leave floor 1. (2) A `map` book is
found by *standing on it*, so pressing Interact on one that is already found
does nothing at all; the old "open the book" loop pressed until it stalled.
A chest book is the opposite: it records the moment the chest opens, and
only the reader going down fires `reads`. (3) `comes-near` — behind "the cat
noticed you" and the Keeper's line about the letter — fires from `tryNPC`,
which only `#talk` and a canvas click run; Interact's own resident branch
goes straight to `talkToSpeaker`. A keyboard player has to Tab to the Talk
button, and the bot now does exactly that.

**Three checks have no subject left, and are asserted as such rather than
deleted.** `locked` (no transition in the pack names a `requires` since the
authored floors went), `pickup` (no family the Section draws names a
`drops`, and every descent book is a chest book — playtest finding B1
restated as an assertion), `level` (see below). Each has a check that reads
the game's own tables and goes **red** the day a subject comes back. The
album check got *stronger*, not weaker: it now requires **every sticker the
pack defines** (5 of 5) rather than five named ones out of twenty-five.

**What replaced the keybearer ladder, honestly.** The old route covered
three locked cellar stairs, three Keybearers and a sealed door to the king
room: fifteen checks. Those subjects are gone from the pack, so no route can
cover them today, and nothing here pretends otherwise. What replaced them is
the same *intent* at new addresses: the act still ends, the chest still
drops something, the end card still shows once with focus on Keep exploring
and stays gone after a reload — the vault on `cellar-0-9` instead of the
king room, and the keybearer cadence is now a named absence. **The king
room itself has no subject and is not coming back** from this route; it was
a room, and the Section has no rooms.

**Three engine gaps found while doing this. None is fixed here** — this
task repairs the harness, not the game or the engine.

- **A hero cannot gain a level anywhere on the descent.** `growAward` is
  paid in the monster's `xp` (`430-loot-on-the-floor.js:101`) and
  `enemyEntry` (`397-the-descent.js`) copies id, name, at, hp, atk, sight
  and drops — **no `xp`**, though the Blueprint family behind the monster
  carries one. So the descent's mobs die silently as far as growth is
  concerned: Rylee's "wander around and fight things loop", the thing this
  repo calls a win, pays nothing on the only floors the game now has. The
  bot asserts the absence (`a descent monster carries no xp…`) so the day
  the engine pays it, the harness says so.
- **`comes-near` is unreachable by the Interact key** (above). Every
  resident beat gated on it — `cat-notices`, `keeper-after-the-end` — is
  keyboard-unreachable except by Tab-ing to `#talk`.
- **`--monsters` exists but is not the default.** The descent is walked with
  the Section's families taken away, which is what vefr's own
  `tests/test_descent_bot.py` does and why: the thing under test is the
  route, not a fight. The lever is the engine's own documented harness hook
  (`VEFR_DESCENT_DEF` is read at call time, "and a harness may plant its
  own"), so **no pack file is touched** and `vefr check` still passes. The
  run puts the families back at the end and fights, so the fight is proved
  in view rather than assumed.

**The bot can fail.** `tests/playthrough/negative_control.py` breaks the
route on purpose twice — once by putting the authored `town [1,1] ->
floor-1` door back (the exact thing that broke this bot), once with
`--entry-at 4,5`, a tile that is not the way down — and fails unless each
run comes back red *for the reason it was broken*. Output in
`tests/playthrough/negative_control.md`.

**Evidence.** `31/31 checks, ok=True, 897 steps` from the literal
acceptance command (`python3 tests/playthrough/run.py --viewport desktop`)
in a VEFR venv; every floor's far end is inside the explored map the
descent itself saved, which is the engine's own answer to "was this floor
walked" and the same question vefr asks of its three; `norns validate` and
`vefr check` both print `ok:` on this pack, unchanged.

## 2026-10-08 — the drop check runs on every change now (agent)

**The gate exists.** `.github/workflows/validate-pack.yml` gains one step,
alongside the existing `norns validate` step and in the same job: *"Assert
every chest drop resolves to a real item"* running
`python3 tests/assert_chest_drops.py` over the same pack path
(`worlds/cottage-of-the-breeze`) the validator is handed. One job, one new
step; nothing else in the workflow moved.

**What it catches.** A drop id the pack names but the item catalog does not
hold — and, one step further, an item whose sprite is not a real entry in
`player.sprites` or has no file in the pack. Neither `norns validate` nor
`vefr check` can see this class, and that was measured rather than assumed:
with `bell-key` restored to a family in the pack and freshly normalized so
nothing was stale, **both printed `ok:` while `tests/assert_chest_drops.py`
exited 1.** The pack shipped four such ids — `crown-seal`, `bell-key`,
`lantern-key`, `helmet-key` — named by Blueprint families and by the
Section's warden, so every kill that should have dropped one dropped nothing
while CI stayed green. cottage#114 and cottage#119 fixed the instances; this
is the gate that would have caught them.

**Proven red, not asserted red.** On a copy of the pack, `/items/cellar-gems`
was deleted from `world.json` — the exact defect the entry below was written
about, and the item the chest book `a-note-under-the-seal` names. The
workflow's own command exits 1 and names the defect in the log:

```
FAIL
  - a-note-under-the-seal.md: drops names 'cellar-gems', not in world.json items
```

With the copy reverted, the same command prints `ok: every chest drop
resolves to a real item with a real sprite` and exits 0. The step is not
`continue-on-error` and takes no `if:` — if the assertion file is missing
the step fails, which is the right way round.

**Cost: about a second.** Stdlib-only Python over `world.json` and the
library's front matter; no VEFR checkout, no `uvx`, no weave, no browser.
It is placed after the validator, so a pack the engine rejects still fails
first, on the validator that has always said so. A self-hosted runner
(`vars.CI_RUNNER_LIGHT`) without `python3` on `PATH` would fail the step; that
is reported rather than papered over, since no runner is named in this repo
and the pinned alternative (a `setup-python` step) is a dependency on a runner
choice this change is not making.

**Known edge, not fixed here.** The assertion reads chest books' `drops:` and
the item catalog; it does not yet walk `blueprint.json`'s families or a
Section's `warden`, which is where `bell-key` and `crown-seal` were named.
That is a widening of the check, and `tests/**` was out of scope for this
change; it is named here so the next person knows what the green is worth.

## 2026-10-08 — the vault chest holds something again (agent)

The "six orphaned books" entry below left one thing named as
unfixed: *"The vault chest drops nothing... `a-note-under-the-seal` still
says `drops: cellar-gems`, and `cellar-gems` is not in the pack's item
catalog (it went with the authored floors), so the bake drops the id
silently."* That is the one this entry closes.

**Confirmed first, not taken on trust.** Wove the pack at `main` and read
the library back out of the woven file: `a-note-under-the-seal` baked
`"chest": true, "drops": []`. The engine's `_drop_ids` (`vefr/cli.py`)
keeps a drop only when the catalog names it, so the id vanished with no
error anywhere. `norns validate` and `vefr check` both printed `ok:`
on that broken pack — the empty chest validated perfectly.

**What the chest holds now: one thing, "a handful of cellar gems"**
(`cellar-gems`, sprite `gems`, `value` 120). Restored through the
Blueprint, not hand-edited into `world.json`: `blueprint.json` moves from
format `1` to `2` to carry a `things` list holding the one record, and
`vefr normalize` writes `/items/cellar-gems` and tracks the pointer in
`blueprint.lock.json`. The record is the authored one, recovered from
`4bed847` — the same name, sprite and value cottage#110 deleted — so no
new words were invented. The book's front matter already said
`drops: cellar-gems` and needed no edit, and the note's own prose
already calls them gems ("a note lies folded on top of the gems"), which
is why this id is the honest one. **No book's words were changed.**

**Why one thing and not a named handful.** Rylee's word for the soul is
"the thrill of opening something and finding something fun", and a chest
of one lump of treasure is thin. But `gems` is the **only** unclaimed
item sprite in the pack. The other four that look free — `key-bell`,
`key-helmet`, `key-lantern`, `seal-crown` — are the Keybearer ladder's,
and that ladder is the step Rylee ordered *later* ("E8 vaults"; loot
"Before E8 vaults"). Every other item sprite is already claimed by an
existing item. New art is not this task's, and inventing a second gem
that reuses the same picture reads as a bug. So: one real thing now, with
the best picture in the pack, at four to five times the value of any
other item — and **a second and third treasure are waiting on a sprite
decision**, not on a naming one. If Rylee wants the fuller handful, the
unblocking move is new sprite sheets (Codex first, then Wan, per
`AGENTS.md`), and the names follow in a minute after that.

**A check that was missing, now in the repo.** `tests/assert_chest_drops.py`
asserts that every id in every chest book's `drops` exists in
`world.json`'s `items`, and that its sprite is a real entry in
`player.sprites` with a real file. Neither validator does this, which is
how an empty chest shipped green. Proven to bite: deleting
`/items/cellar-gems` again makes it fail with the exact original
defect, and restoring it passes.

**Left out on purpose.** The Cellar King still drops `crown-seal`, and the
three Keybearer families still drop `bell-key`, `lantern-key` and
`helmet-key`. None of those four ids are in the catalog either, so they
are being dropped at play the same silent way this chest was — one floor
up, from the warden on `cellar-0-9`. That is the Keybearer ladder
(cottage#110 removed the items and the six rules that named them), which
Rylee ordered at step 4, and this task is the chest, so it is named here
rather than fixed here. **It should not stay unfixed.**

**Evidence, and its edge.** `norns validate` and `vefr check` both print
`ok:` on this pack; `vefr normalize` reports `fresh`; the woven read-back
goes from `drops: []` to `drops: ['cellar-gems']` resolving to
`{"name": "a handful of cellar gems", "sprite": "gems", "value": 120}`,
with `gems` baked into `VEFR_SPRITES` as a real PNG so the bag draws the
picture rather than a fallback dot. **The game was not run and there is
no screenshot**: the clone had no browser and no node, and the descent is
generated client-side, so the chest was never opened by a player in this
session. What is proven is the data and the code path that consumes it
(`giveChestDrops` in `web/packaged.html` adds each id to the bag), not a
walk.

## 2026-10-08 — three more Sections under the cellar (agent)

Built against Rylee's picker answers recorded below: mood "Change by section", danger
"Rising" — "gentle near the top, some fights to fear deeper down" — and what pulls her
deeper: "What the next floor looks like, A goal ahead, Collections".

- **What is there now.** `sections/rootworks.json`, `sections/siltworks.json` and
  `sections/emberhall.json`, chained after the cellar in `world.json`'s `descent.sections`
  so the descent runs `cellar > rootworks > siltworks > emberhall` — 36 floors. `cellar`
  itself is untouched; it stays gentle.
  - **rootworks** — the damp ground under the cottage garden; green, close, still lit
    (fog radius 6, the widest in the chain). Carries root-tangles, flowerpot toads, wick
    sprites, moths, cave crickets and the new rootwatchers.
  - **siltworks** — the flooded ground below that, older and colder; fog 4, smaller rooms.
    Carries deep shades, cobweb wraiths, cave crickets, barrel mimics, rootwatchers and
    the new mire toads. Its warden is the Silt Warden, named in the Section's `warden`
    key — see the engine gaps below for why a named warden does not spawn yet.
  - **emberhall** — the sealed fire the town kept, the bottom of this descent; fog 3, the
    darkest and smallest rooms. Carries hollow shades, howling rustles, hollow crickets,
    cobweb wraiths and barrel mimics, and it is the only place a hollow cricket — 11 hp,
    4 attack — turns up. Its warden is the Ember Warden, named in the `warden` key.
- **Every name here is an agent draft, not canon.** The three place names, the six new
  Blueprint families (`rootwatcher`, `mire-toad`, `hollow-cricket`, `silt-warden`,
  `root-warden`, `ember-warden`) and their monsters' names are all data and all changeable
  without a rewrite: the Section files name creatures by Blueprint id and carry no text.
  `STORY.md` is untouched.
- **Rising danger is done with what is there, not with a knob.** The Section loot tier and
  `mob_stats`' ramp are written into every Section as the contract asks, but neither is read
  by the play-time descent yet (see the engine gaps below), so the danger a player actually
  meets comes from the creatures each Section names and from how big its floors are.
  Measured over all 36 floors, and it rises on every measure:
  average mob hp `cellar 4.30 > rootworks 6.78 > siltworks 9.23 > emberhall 10.63`,
  highest attack on a floor `2 > 3 > 3 > 4`, fog radius `5 / 6 / 4 / 3`.
- **Six new families went in through the Blueprint** and the lock was refreshed with
  `vefr normalize --out`; no contract's `enemies` list was hand-edited.
- **Proven by walking, not by validating.** The real woven player, in VEFR's jsdom play
  kit, on three run seeds (`breeze`, `breeze/run-1`, `breeze/run-2`): out of the cottage,
  across the town to `[1,1]`, then down all 36 floors, every floor walked from its up-stair
  to its down-stair and every stair used. All three runs crossed all three Section
  boundaries (depth 9→10, 18→19, 27→28) and reached the bottom; the descent then rolled on
  into cycle 1 (`cellar-1-1`), so the chain is endless as intended.

### What the engine could not do, filed as VEFR issues rather than worked around

- **Half a Section is data the descent does not read yet.** The play-time descent (part
  397) reads only `id`, `floors`, `size`, `rooms`, `fog`, `families` and `pattern` from a
  Section. It does **not** read `curve` or `loot.tier` (`mob_stats` is never called, so the
  depth ramp is written but not applied), the `depth` range on a family entry, the
  `specials` a `special` slot draws, `tiles`, `warden`, `vault`, `elites`, `groups`,
  `stamps` or `pois`. All of those are in the files as the contract asks, and all of them
  take effect the day the engine reads them — but nothing in this pass may be described as
  working on the strength of them. One consequence caught during the work: a family listed
  in `families` with `depth: [7, 9]` spawned on **every** floor of its Section, which put
  thirteen Ember Wardens in one descent. The wardens were moved out of `families` and are
  named only in the Section's `warden` key, which is how `cellar-king` is already used.
- **A Section cannot have its own tiles.** `shapes.SECTION` accepts `tiles` and `vefr check`
  validates it, but nothing reads it: the played floor's legend is the engine's shared
  `delve.LEGEND`, and its pictures come from `VEFR_REGION_TILES[region] || VEFR_TILES` —
  so every generated floor in every Section draws the same ground. **No new tile art was
  made for this pass.** It would have shipped as art nothing draws, which is worse than
  reusing what exists. Rootworks, siltworks and emberhall currently differ by their
  creatures, their fog and their floor shape.
- **The entry stair keeps the previous run's arrival tile.** `startRun` calls
  `resetRegions`, which drops a transition only when *both* its ends are generated — the
  town is not — so `town[1,1] -> cellar-0-1` survives with the old run's `to_at` and the
  hero arrives mid-floor. On a run where the stale tile is a wall, the hero arrives inside
  one. Found while proving three seeds; the harness re-wires the entry rather than the pack
  carrying a workaround.
- **Dying on a generated floor throws you out of the descent.** `cozyDeath` returns the hero
  to where they woke, and a generated floor is not that, so they land back in town with a
  full bar and have to walk to `[1,1]` and start again at floor 1.

### Claude's note (agent): what the play-through turned up about balance

Walking the chain with the monsters left in (the proof run above uses VEFR's own
precedent of a quiet descent, so that the walk tests the chain and not a fight) the hero
died on floor 2 of the **cellar**, which this change did not touch. The hero starts at 6 hp
and 2 attack; a cellar spider is 5 hp and 2 attack, so one fight is most of the bar and two
is the run. The same holds further down: a hollow cricket in emberhall is 11 hp at 4
attack — two hits kill the 6 hp starting hero, and eleven of its own — while taking
four a swing. The growth ladder
(`0, 6, 15, 30, 55, 95, 150, 230` xp for +2 hp and +1 attack) would carry a player who
clears a floor per fight, so this reads as "the descent is not survivable if you fight
everything" — which is a tuning call for Rylee, not something to quietly patch. What it
does mean is that the new Sections were tuned against *measured* numbers rather than
against a fight, and the first person to walk down there with monsters in the dark should
say how it feels.

## 2026-10-08 (later) — the six orphaned books are findable again (agent)

The entry below ("one way down") deleted `floor-1`..`floor-6` and
`king-room` and left six books naming a region that no longer exists, so
they could not be found at all: the validator does not flag them, so
nothing caught it. Each is re-homed here. **Front matter only — no book's
words were changed**, because the story draft is Rylee's to edit and
`storywords` is held until she has.

**The rule these placements follow** (research, "Delivering a story to a
player who will not read a quest log" and "The thrill of opening
something, made of what"): *every story beat rides something she wanted
anyway; the story never asks for its own container.* So each book sits
where she is already going, and the two that were chest books stay chest
books — the thrill that carries the story is the thrill she came for.

| Book | Was | Now | Why there |
| --- | --- | --- | --- |
| `a-scrap-in-the-dust` | `floor-1` [4,4] | `cellar-0-1` [27,36] | The premise ("Two things this town will not say") two steps from where the stair puts you: she goes down wanting to go down, and the floor tells her what she is doing. |
| `a-letter-in-a-chest` | `floor-1` [20,14] | `cellar-0-1` [23,34] | Still a chest, still `drops: brass-ring`, eight steps into the first floor. This is the research's own example — *the letter is in an open chest she opened for the ring* — so it stays exactly that, and `the-letter-read` → `the-keeper-knows` → the Keeper's line works again. |
| `a-coin-face-down` | `floor-1` [3,10] | `cellar-0-3` [52,46] | Mid-descent, four steps off the arrival stair. "On the stone" is cellar flagstone, and a coin nobody dropped belongs to someone else's descent, not to a town street. |
| `a-candle-and-a-note` | `floor-1` [26,16] | `cellar-0-5` [30,41] | Floor 5 is the Section's **landing** — its up-stair goes straight back to town. "Someone sat here a long while, and never came back up" belongs by the way home. |
| `a-note-under-the-seal` | `king-room` [6,2] | `cellar-0-9` [37,29] | The bottom floor, the `warden` kind. She walks to the bottom wanting to see what is down there; the chest is the vault the note describes, and reading it still sets `act-1-complete` and fires `complete-act`. |
| `a-burned-page` | `floor-1` [12,10] | `town` [5,8] | The town's own rubble, on the tile the map already names "the old tavern, burned". It is three steps from the town centre on the road she crosses all the time, and it puts the page at the ruin while the tab stays behind the Keeper's counter — the same truth twice in different clothes, which is what the research asks for. |

**Verified, not assumed.** The floors were drawn the way the woven player
draws them (`vefr.delve.floor_plan`, the Python twin of `floorPlan` in
`web/packaged.html`, same `breeze` run seed, cycle 0), then flooded from
the stair the hero arrives on. Every tile is walkable and reachable:
2 steps (scrap), 8 (letter chest), 4 (coin), 4 (candle), 4 (seal chest);
the page is 3 steps from the town centre. `norns validate` and
`vefr check` both print `ok:`; the woven file bakes all ten books with the
regions, `chest: yes` and `drops` above.

**Two things this did not fix, said out loud.** (1) The vault chest drops
nothing: `a-note-under-the-seal` still says `drops: cellar-gems`, and
`cellar-gems` is not in the pack's item catalog (it went with the authored
floors), so the bake drops the id silently — visible in the woven
`VEFR_LIBRARY` as `drops: []`. That is a treasure decision and a
`world.json` item, both out of scope here. (2) No browser walk-through
was possible in the clone that did this (no Playwright/Chromium, no
`uv`, no node), so reachability is proven by flood fill over the exact
floors the player walks plus the baked output, not by a recorded walk.

## 2026-10-08 — one way down: town [1,1] is the generated descent (agent)

- **Her words (Rylee, cottage#104):** "All new generated so it matches." Town tile `[1,1]` had **two** doors: the hand-authored `floor-1`, and — appended at run time by the Section descent's `wireEntry()` — the generated `cellar-0-1`. VEFR's `wireEntry()` appends and never replaces, so both survived and a player walking onto that tile got two exits. Reproduced in VEFR's own play kit against a build woven from `main` (log: `docs/playtests/2026-10-08-descent-104.md`):
  `PROBE exits-from-town-[1,1] = 2 -> floor-1, cellar-0-1`.
- **Changed:** the authored cellar door and its floors are gone. `acts/act-1/world.json` no longer lists `floor-1`..`floor-6` and `king-room` and no longer transitions to or from them; those seven directories are deleted; `blueprint.json` lost its six `act-1/floor-*` region records (refreshed with `vefr normalize`, never hand-edited into a contract). All 22 Blueprint **families** are kept, including the five the Section draws on (`cellar-rat`, `nest-of-moths`, `damp-shade`, `cellar-spider`, and `cellar-king` as warden).
- **Verified, not assumed:** one exit from `[1,1]` (`cellar-0-1` only); a walked hero leaves the cottage, crosses the town and arrives in `cellar-0-1` at `[27,34]` with 20 generated enemies; `norns validate` and `vefr check` both print `ok:` on **vefr main** (`122b480`).

### What this orphaned, and why it went anyway

Removing the authored cellar removed the whole hand-built ladder with it, because it was authored *in* those floors:

- **Act 1's ending is gone from the pack.** `the-seal-note-read` (which sets `act-1-complete` and fires `complete-act`) still exists, but the note it reads lived in `king-room`. `a-note-under-the-seal.md`, `a-letter-in-a-chest.md`, `a-coin-face-down.md`, `a-burned-page.md`, `a-candle-and-a-note.md` and `a-scrap-in-the-dust.md` all name a `region:` that no longer exists, so they cannot be found. `act-1-complete`, `keeper-after-the-end` and `regular-after-the-end` are now unreachable beats. **The generated descent has no ending at all.**
- **The Keybearer ladder is gone:** `bell-key`, `lantern-key`, `helmet-key`, `crown-seal` and `cellar-gems` were only placed in the authored floors, so the items and the six rules that name them came out — 12 rules to 7, 25 album stickers to 5, 14 items to 9. The three locked stairs (3→4, 4→5, 5→6) went with them.
- **Why the engine cannot fill the gap yet:** `vefr/sections.py` says plainly, "The warden, the vault and the key that opens them are E8's", and E8 is not built. A generated Section draws floors, mobs and a warden; it cannot yet place a key, a vault or an ending. Rylee's approved order puts "E8 guardian/key/vault progression" at step 4, **after** this change — so the gap is expected and scheduled, not a regression to undo.
- **Nothing was silently dropped:** the four rules, twenty stickers and five items above are named here so the loss is on the record. `tutorial-begin` kept its line ("The stair is in the town's top left corner" — still true) and lost only its `point-to`, which named a region that no longer exists.

## 2026-10-08 (later still) — the round-two skin, played: two picks could not be drawn and the evidence is now real (agent)

The previous entry looked at this skin with a drawing of it. This one looked at it with the game. A VEFR checkout was cloned, `uv` and Playwright's Chromium installed, the pack woven, and the player opened: **all eleven of Rylee's round-two picks have now been seen in the real engine, and nine of them are right.** Two were wrong and are rebuilt; one is right but unreachable; one cannot be reached by this pack at all.

- **The mock was a mock, and the two PNGs said otherwise.** `look-phone.png` and `look-desktop.png` were drawn by `art/tools/mock_skin.py`, and they sat in `art/skins/parchment-and-wood/` under names that read as screenshots of the game. They are gone from that folder. The four files there now are `look-desktop.png`, `look-phone.png` and their two `-menu` companions, and every one of them is a screenshot of the woven player taken by running it. The drawings have moved to `art/skins/mock-renders/` under `mock-` and `preview-` names, with a `README.md` at the top of that folder saying in the first line that nothing in it is evidence. `art/tests/test_real_look.py` fails if a PNG that is not a named, correctly-sized screenshot ever reappears in the skin folder.
- **How the evidence was taken, so it can be checked.** The desktop shot is `vefr look --pack` — the engine's own tool, no local code in the path. `vefr look` fixes its viewport at 1280x800 with no flag for a phone, so `art/tools/real_look.py` is a thin stand-in that does the same three things at any size: open the woven HTML in headless Chromium, click `#ts-enter`, screenshot. At 1280x800 with no steps it reproduces `vefr look` **byte for byte** — on this pack both are `6e596106239591edb7cb23b718ee7cf1672e44b4d71c0d7a6433ea2f047bffbc`, which is also the sha256 of the shipped `look-desktop.png`. That is what makes the phone shot the engine rather than a drawing of it. The tool takes `--click`, which is how the two menu shots (tabs, corner studs, bag rows) were taken.
- **Two picks could not be drawn at the size the player gives them, and are now rebuilt.** The player lays the **banner** and the **slot** across a whole box with `background-size: 100% 100%` — not a nine-slice — and neither box has a shape a picture can assume: `.toasts` is 210x153 on a desktop and 156x194 on a phone and a different height again per message, and `.equip-row` is a bag line 510x32 on a desktop and 308x32 on a phone. Rylee's ribbon, stretched over the message stack, dragged its swallow tails out past the panel as long flanges; her square slot, stretched across a bag row, turned its bevelled corner into a hard band of glare down one side of every row. Both read, in play, as a rendering fault, which is worse than the plain player. What ships instead is the parchment field drawn *inside* each ornament's frame — the one part of each pick that is plain, and the only thing that survives being scaled by ten in one direction. `art/tools/make_plate_field.py` crops to it, smooths the colour and fades the edges; it is a crop and two blurs, deterministic, unit-tested. **The cuts are kept untouched as `banner-v3.webp` and `slot-v3.webp`** beside them, so the framed ornaments go straight back the moment the player gives either part a box of its own shape. What is lost, and said plainly: the ribbon's tails and the slot's frame. They are still hers and still on disk; a 510x32 bag line just cannot be drawn with them.
- **The nine that are right, one line each.** Panel, speech, tooltip and gold plate read well; the tab and the selected tab read as one tab in two states at both sizes; the corner reads as a legible brass stud at 18x18; the bar fill sits in the frame's trough with an invisible seam; the banner and the slot, as rebuilt, read as clean warm faces. Full table, with the shot each was seen in, in `art/skins/README.md`.
- **One pick is right and unreachable.** The **divider** is cut, wired and legal, and the player paints it on `header.game-head` — which its own stylesheet hides for the whole of play (`body.in-game header.game-head { display: none }`) and which on the title screen sits under `#title-screen` at `z-index: 100`. Photographing the header on its own shows the stitch, so the picture is right and the slot cannot be reached. Left in place; nothing in the art can fix it.
- **One pick this pack cannot show at all.** The **speech** box paints `#npc-box`, and `grep -ri npc worlds/cottage-of-the-breeze/` finds nothing: there are no NPCs in the pack, so there is nothing to say. It is `check_ui`-clean and it stays unproven until the pack has someone in it.
- **The cursor is not provable by a screenshot.** It is a CSS `cursor:` URL, and a screenshot does not photograph the pointer. `check_ui.py` says `ok cursor` and the hotspot is inside the picture; that is all that can be said, and it is said rather than implied.
- **A bug the tests caught, in a tool the last entry shipped.** `make_selected_tab.py` saved with "Pillow's defaults, which are lossless for WebP". Pillow's default for WebP is **lossy**. So the selected tab had been quantised once on the way out and again by `build_skin.py`'s lossless re-save, and the picture on screen was not the picture in the file. Both that tool and the new one now pass `lossless=True`, and `PROVENANCE.md` says why in a line, because it is not the default and the next person will hit it too.
- **What is still true from 2026-10-01.** The panel's middle is one flat colour sampled from the picture, so a wide panel shows a soft inner rectangle; it is what `border-image` will do and it is left for the loader. One thing the shots add: the `.toasts-toggle` "Messages" button is still the player's flat dark `var(--glass)` and is the one dark thing on a parchment screen. And one guess of mine checked out the other way — the manifest's `fonts` name Crimson Pro, and the player does bundle it (`web/fonts/CrimsonPro-Variable.woff2`; `document.fonts` lists the face as loaded in the woven game), so nothing is falling back to Georgia.
- **Rylee's eye is still the gate.** Nothing here changes a pick; two parts are now built from their picks rather than cut from them, both derived pictures keep their sheet's `.credits.txt` in `PROVENANCE.tsv`, and every cut she chose is still on disk under its own name.

## 2026-10-08 (later) — the picker answers, and the soft-wood skin merged as cottage#107 (Rylee)

Rylee answered the picker questions tonight. Her words, quoted exactly. `DESIGN.md` carries the same lines in the places they change.

- **Loot, order:** "Before E8 vaults".
- **Inventory:** "Simpler: slots plus bag upgrades". This **replaces** the grid containers `DESIGN.md` carried (small grids per container, shaped items, a weight limit); that line is struck in `DESIGN.md`, not left standing beside the new answer. Decided, not built yet.
- **Spells, order:** "After loot". So the order is loot → spells → E8 vaults.
- **What the town gives:** "Rest, trade, identify".
- **Danger:** "Rising" — gentle near the top, some fights to fear deeper down.
- **Mood:** "Change by section".
- **What pulls her deeper:** "What the next floor looks like, A goal ahead, Collections".
- **Devices:** "Both equally".
- **Builds:** "A link per playable milestone".
- **The soul (Rylee, 2026-10-08):** "No existing work is sacred except the soul of it". The soul, confirmed by her ("Yes, that's it"): curious, low-bandwidth exploring; the thrill of opening something and finding something fun; a cozy storybook world; no reflexes and nothing to memorize; 30 minutes that turns into four hours. Judge every change against it.
- **Also tonight:** the soft-wood skin, built from her round-two picks, merged as cottage#107.
- **Claude's note (agent):** nothing on this list is built by tonight's notes; every line above is a decision on disk only. The devices, builds and pull-deeper answers are recorded here and are not yet in the `DESIGN.md` checklist, which carries the systems answers only.
## 2026-10-08 (later) — the round-two skin, looked at: one pick did not survive being built (agent)

The skin merged in cottage#107 had never been looked at assembled. It has now been, at a phone (390x844) and a desktop (1280x800) viewport, from the pack's own copy. **Ten of Rylee's eleven round-two picks are in and read correctly. The eleventh did not, and is now built a different way.**

- **The problem.** `missing/tab-selected/tab-selected_v3.png` was asked for as "the same tab but selected: lighter honey wood, parchment face joined to a parchment panel below", and what came back is the *panel* half of that sentence — a 1312 x 1199 near-square parchment panel with a shallow tab bump along its top edge, not a tab chip. Cut straight and built into the tab slot, `process_box` squeezes it into a 96 x 40 box and mirrors it: the rim is sliced away and the player gets a pale stepped blob sitting next to a perfectly good `tab.webp`. `check_ui.py` says `ok tab`, because the file is a legal 96x40 RGBA skin part; it is the *look* that is wrong, and only looking catches it.
- **What I changed, and why.** The pick is untouched and still hers. Its cut is kept, under the name it actually is, as `skin-source/tab-selected-panel-v3.webp` (byte-for-byte the cut of `tab-selected_v3.png`). The chip that ships, `tab-selected.webp`, is now **derived from the tab pick she also chose** (`tab_v3`) with every colour moved one step toward the honey cream that `tab-selected_v3.png` is drawn in — `art/tools/make_selected_tab.py`. Alpha is carried across untouched, so the selected chip is the same silhouette as the tab at rest and the two read as one tab in two states. Nothing is redrawn, reshaped or resampled; it is a blend, so the tool that makes it is short, deterministic (two runs, identical bytes) and unit-tested, and the change can be undone by re-running the build over the kept cut.
- **What I left in, deliberately.** The panel's centre is the parchment texture stretched, so a full-width dialogue panel shows a soft quilt inside its rim. It reads as parchment rather than as an error and it is what `border-image` will do in the player, so it is left for whoever builds the loader rather than papered over in the art.
- **Provenance follows the truth.** `skin-source/PROVENANCE.md` gains a section saying plainly that `tab-selected.webp` is derived, not cut; `PROVENANCE.tsv` marks that row `derived` and names `tab_v3.png` and its `.credits.txt` as the source, because the derived chip's pixels come from that sheet, with `tab-selected-panel-v3` carried beside it as the unchanged cut of the sheet she picked. Every picture is still ours, every `.credits.txt` still sits beside its sheet, and no third-party art is involved.
- **A tool to look with, and the stale preview.** `preview.png` in `art/skins/parchment-and-wood/` is dated 2026-10-01 and still shows the round-10 art, so it is not a picture of the skin that ships; `art/skins/README.md` now says so. `art/tools/mock_skin.py` replaces it: it draws the parts *assembled*, nine-sliced the way the player does, over the skin's own backdrop with real text in the skin's ink, at whatever viewport size you ask for. `look-phone.png` and `look-desktop.png` are its output. It is a mock, not the engine — `check_ui.py` still decides whether a skin is legal.
- **Still not verified: in play.** No VEFR checkout, no network and no browser in the worktree this was cut in, so the pack was **not** validated with `norns validate` / `vefr check` here and the skin was **not** played. What *is* verified: `check_ui.py` passes every part, a full rebuild from `skin-source/` reproduces all 19 part pictures byte-for-byte against both `art/skins/` and the pack, and the two look screenshots. The cursor, banner, divider and corner are still unproven in play — the mock does not place them, because the player draws those over the map rather than in a panel flow.

## 2026-10-08 — the soft-wood skin is built from Rylee's round-two picks (Rylee)

- **Her words (2026-10-08):** "Use my picks as they are". The eleven round-two picks in `art/source/round18/ui-soft/PICKS.md` (banner `missing/banner/banner_v3.png`, speech `missing/speech/speech_v3.png`, tooltip `missing/tooltip/tooltip_v2.png`, corner `missing/corner/corner_v3.png`, bar-frame `missing/bar-frame/bar-frame_v2.png`, bar-fill `missing/bar-fill/bar-fill_v1.png`, slot `missing/slot/slot_v3.png`, tab `missing/tab/tab_v3.png`, tab-selected `missing/tab-selected/tab-selected_v3.png`, divider `dividers/dividers_v2.png`, cursor `cursor/cursor_v2.png`) are cut into `art/source/round18/ui-soft/skin-source/` with `art/tools/split_sheet.py`, saved as lossless WebP keeping alpha; `PROVENANCE.md` and `PROVENANCE.tsv` name the sheet each cut came from and the `.credits.txt` beside it.
- **Her standing rule (Rylee, 2026-10-02):** "Art we ship is art we made" — every cut keeps its `.credits.txt` beside the sheet it came from. None of the cuts are hand-redrawn or rescaled; `build_skin.py` owns the geometry.
- **Five carry-overs:** `button-hover`, `button-pressed`, `button-disabled`, `toggle-off` and `wood.png` are round-10 pictures carried over byte-for-byte so `build_skin.py` has every row of its `PICTURES` table. They are placeholders pending Rylee's eye, not round-18 picks.
- **Built and validated:** the skin is built from the new sources into `art/skins/parchment-and-wood/` (`check_ui.py` passes every part), and the part pictures are copied into `worlds/cottage-of-the-breeze/skins/parchment-and-wood/`. The pack's `skin.json` keeps `fonts` (display/body: Crimson Pro), `backdrop: backdrop-alt-1.webp`, the shorter credit line ("Rylee and Claude; Codex proofs") and `ink` exactly as PR #96 left them; the panel's `fill` is not added (VEFR reads `fill` as a picture file and the player ignores a panel fill); `backdrop-alt-1.webp` is not touched.

## 2026-10-04 (later) — interface direction: parchment and soft wood, Ledger type (Rylee)

- **Her words:** "Scrapbook pages I think is my fav. It's working better now! Can we fix the font to be a little more 'cottage' and less stardew valley?" Then: "Oh I don't like the tape. Back to parchment and soft wood. Let's say 'ledger' font?" Earlier she had said of the first painted kit: "I prefer the older style over this", and asked for "radically different ui styles to help me visually narrow down. Not a picker, a system to help me refine."
- **Claude's note (agent):** the interface lab now defaults to "Parchment & soft wood" with the Ledger voice (Crimson Pro). Nothing is built into the game yet; the plan is `docs/plans/native-ui/PLAN.md`.

## 2026-10-04 (after the first night) — what changed, and what Rylee decided

- **Release 1 is a complete polished Act 1.** After the entry below was written, the same night added the album (25 stickers), nine soft synthesized sounds with a switch in Menu > Display, a four-direction walk cycle for the hero, eight unique cast monsters, seven pieces of gear with Codex art, and an accessibility pass. Published build `26c21ee`. Verification and state: `.project/CURRENT.md`.
- **Acts 2 and 3 were left for later by Rylee's decision.** They remain part of the three-act direction. The release is not evidence that VEFR could not support them; act advance and status effects are the next engine capabilities because those acts will want them. Plan: `docs/plans/acts-2-3/PLAN.md`.
- **Her order of work (chat, 2026-10-04):** "Ship act 1, then plan 2 and 3"; refactor `web/packaged.html` first; fire is the first effect; "I'd like all of act 1 to be very high quality. With all systems and art and everything." (She also asked for a research task on RPG interface styles; the result is in the artifact she was sent.)
- **Her interface direction (chat, 2026-10-04):** "anything running 'inside the game' to be in a themed ui for that game and only controls and such", with HUD icons currently floating over the page background; then, of a handheld-frame mock: "I don't want an actual frame around it. I want the ui to pretend it's ported from another system but be native hahaha! It should feel like a part of the vefr world. This feels like a square mechanical ui overlayed over a warm soft game." Recorded as `docs/plans/native-ui/PLAN.md`.
- **Claude's note (agent):** the sound default (on where a pack opts in, with a visible switch) was my choice and is not yet ruled on by Rylee.

## 2026-10-03 (overnight) — release 1: the ladder, the King's room and an ending (agent drafts, Rylee decides)

Rylee asked for a complete, polished, playable first release built through VEFR. Built tonight (all on branch `release-1/ladder`; plan in `docs/plans/release-1/PLAN.md`). **Everything below that is story text is an agent draft, not canon. Keep, rewrite or bin any of it; each is data, so swapping words takes minutes.**

- **The Keybearer ladder.** Floors 3, 4 and 5 each hold one Keybearer, a tougher variant of an existing family carrying that floor's key; the Cellar King on floor 6 carries the crown seal. Placed by BFS in a far room (floor 3 at 6,6; floor 4 at 2,2; floor 5 at 1,29; the King at 26,3). The stairs 3 to 4, 4 to 5 and 5 to 6 now need the key (`requires`); keys are `keep` and have **no value** (a sold key would soft-lock the game). Guardian names are descriptive placeholders ("the Keybearer, a great pale moth"); **proper names and epithets are yours**. Art picks: `art/source/round11/PICKS.md` (moth, mushroom elder, stag beetle; the mole and the robed rat are held back for later).
- **The King's room and the ending.** A sealed door on floor 6 at (11,1), opened by the crown seal, leads to `king-room`: a small chest with **gems** (treasure is a draft), a draft lore note (`library/a-note-under-the-seal.md`) and a stair home to town. Reading the note fires one rule: it sets `act-1-complete`, shows the end card (VEFR's new `complete-act` action: "Keep exploring" or "Start over", once per save) and says one narrator line. It does not start act 2 (ADR 0006 is unbuilt). The Keeper and the Tavern Regular have one new draft line each after the end.
- **Tutorial moments, an About book, the cat.** Draft lines from rules (`tutorial-*`, `first-key-*`, `the-cat-notices`); an "About This Game" book on the cottage shelf (credits, tools, fonts). The brass ring is now a charm (+1 attack).
- **Deep floors dressed.** Floors 4-6 and the King's room use the round-13 deep flagstone and wall; floor 6 map was hand-edited for the sealed door (a `vefr delve` rerun would overwrite it).
- **Not done (and why).** *(Written early that night; superseded the same night: the album, sound, the hero's walking frames and the round-12 cast monsters all landed later, see the entry above.)* What remained: stakes (no engine mechanic), acts 2 and 3 (deferred by Rylee after Act 1), per-run floors, the mole and beetle proofs as town folk.
- **Existing saves:** new enemies change signatures, so floors repopulate on an old save. Start over for a clean run.

## 2026-10-02 (late) — art direction after the MiniMax test (Rylee)

- **Her words:** "I think I prefer the codex character designs. I enjoy the storybook and the cuter concepts for the mobs vs realism." And of the dressed scarred-rat guardian (a MiniMax draft): "I did rather enjoy the v6 guard style though. That was pretty cute!" And: "you're also more than welcome to use codex, was just an experiment!"
- **What that means (agent's reading):** cute, characterful storybook mobs are the target; Codex stays first choice for characters and creatures; MiniMax is for items and equipment (and cute-mob drafts when asked). Nothing from the test is in the pack. The recipe is in `art/STYLE.md` (PR for review).

## 2026-10-02 (late) — the language campaign, and the first lock (Rylee)

- **Answers, in chat:** the first lock is **floor 3 to floor 4**; the key is **an actual key**; the guardians are "variants with names based on their art/abilities". Names are not chosen yet; nothing here is canon until she says.
- **Creature records now come from a Blueprint** (VEFR's new optional source). `blueprint.json` is the edited truth for the 69 monsters; the floor contracts' `enemies` lists are generated and read-only. The trial passed its exit threshold (508 authored values became 277, 45.5% fewer, every record equal to before, the woven game identical). Follow-up (agent, for her review): the repeated potion drop moves into the families that carry it, 257 values (49.4% fewer), still every record equal and no floor contract changed. She asked for it merged: PR #68.
- **Rule state survives a reload** (`saves.rules: persist`, `legacy: from-log`): a rule that fired stays fired, so a beat she already saw does not replay (PR #70). `from-log` uses the Why log, which keeps 20 entries, so an older beat could replay once.
- **Published** for her demo: build `2026-10-02-8a48788` on the dev gallery.
- The engine can lock a stair now (VEFR #229); Cottage does not use it yet.

## 2026-10-02 — growth and the day's goal (Rylee)

Her goal for the day: "a full 1-2 act structure with multiple mobs, working inventory, and a loop that feels rewarding, some kind of experience/learning/growing methodology." On growth she chose: "can we wire in classic xp and growth and learn-by-doing into the engine, but I think that cottage should be standard. just don't lose the learn by doing.. that's important for another game I'm working on". So VEFR gets both as neutral capabilities; Cottage uses classic XP. She also asked to start with "repo health/docs/engine in offload foremen so we can work on the structure together".

- **Docs brought in line (agent):** `AGENTS.md` (art tests exist), `.project/CURRENT.md` (engine landed, Cottage has no rules yet), `docs/GAME-PLAN.md` (rules no longer blocked).
- **Letter -> Keeper wired (agent):** two rules in `world.json`. `the-letter-read` (when the hero reads "A Letter, Folded Small", set a flag, one narrator line). `the-keeper-knows` (when the hero is next to the Spell Keeper and has read it: she says her line once). Checked by firing both events into the woven file: she says nothing before the letter, and the Why record names each rule. **The two lines are agent drafts, not canon.** Keeper: "Oh. You found my letter. I did say I'd come back. I only took the long way round. Here, I kept one back for you." Hers to keep, rewrite or bin. Not yet played by walking to the chest.
- **Rylee, 2026-10-02:** "wire the letter and Keeper reaction first. and for this run let's mimic castle of the winds pretty directly to help me learn while we learn and as we build our engine". Claude's note: this means copying the systems (kills give XP, levels, town and descent loop); our own names, numbers and text, per the repo rule.
- **Fuller cellar (Rylee: "it feels empty in the dungoen right now"):** floors 1, 2 and 3 now hold 6, 10 and 12 monsters (were 1, 2, 2). Only four monster pictures exist (rat, shade, moths, rustle), so variety is name and stat variants: a fat cellar rat, a deep shade, a loud rustle (more health and bite, some carry a potion). Placed by a seeded script on open floor, at least 7 tiles from the stairs and chests and 5 apart. **Tuning numbers are first guesses**; new monster pictures are an art task.
- **Her UI notes, same day (queued in VEFR):** the bottom text is noisy ("text on the bottom of the screen that basically never goes away and you can't move it"), the hero's hop is "cute but weird" (chose: much smaller), "full wasd support", and Trade should close without Esc or the mouse. Art: "most of the art could use some love"; she chose a full art pass later.
- **Act 2, built as a deeper zone (Rylee: "Both, zone first"):** only the first act plays in VEFR today (ADR 0006, real act advance, is proposed). So floors 4, 5 and 6 hang off a new stair down at floor 3 (tile 2,2, the far corner from the arrival), generated by `vefr delve` (seed `cottage-deeper-zone`, 48x32, 10 rooms) and dressed with fog and 12, 14 and 15 tougher monsters (new: a hollow shade 12 hp / 3 atk, a howling rustle). They live in act 1's region list so they can move into a real act 2 when ADR 0006 is built (queued as the next engine job). **Looks:** the new floors use the engine's plain dungeon tiles, not the authored flagstone, so they look flatter than floors 1-3; an art task. **Not checked by eye:** I could not jump into the new floors in a browser (the region switch is private to the player), so their look is UNVERIFIED; the pack validates and bakes.
- **Open for Rylee, story:** `docs/story-spine-notes.md` put the last room (the realization) at the bottom of floor 3, which was an agent proposal and is not built. With six floors, where does the bottom of the story live: floor 3, or floor 6? Nothing is built either way; no canon changed.
- **Gating (Rylee):** after learning the word (progression gating; soft = power curve, hard = lock and key) she asked "is it more rewarding to have one tougher mob with the key that you have to find? I do want the levels and mobs to be generated, not sure how that applies here. wasn't cotw generated?". Claude's answer: yes, a key guardian is more rewarding; generate the filler, place the guardian by the generator; the engine cannot lock a stair yet. Design: `../vefr/design/gates-and-guardians.md` (proposed). Her call still open: which stair is the first lock, and what the key looks like.
- **Art rights (Rylee, 2026-10-02):** "we are allowed to distribute the art we generate, but we will attribute all of it. leave out the kenny and limezu assets, only use what we have made ourself." Then: "kenny is only for prototyping, and limezu I might use in a project and attribute it but mostly I wanted to support them and it was a sale". Recorded as a rule in `AGENTS.md`. The vendored `assets/kenney/` sheets in the pack are unused (no reference in any pack JSON); left in place, removal is hers to ask for. Art is scattered across `media_files/designs/vefr/art/`, `../vefr/web/art/` and `art/source/` (she: "sorry it's messy"); pick sheets are in the gallery (Art picks).
- **Growth is on in Cottage (Rylee: "turn on growth in cottage"):** classic levels, the Castle-of-the-Winds-style systems copy she asked for, our own numbers. `world.json` `growth`: 8 levels at 0, 6, 15, 30, 55, 95, 150, 230 experience; each level gives +2 health and +1 attack (hero starts 6 hp / 2 atk). Every monster on floors 1-6 has `xp = round(hp x atk / 2)`, at least 1 (rat 2, fat rat 3, deep shade 8, hollow shade 18; 314 in all). If you clear a floor you reach: floor 1 level 2, floor 2 level 4, floor 3 level 5, floor 4 level 6, floor 5 level 7, floor 6 level 8. **First guesses to tune by playing.** The surface is still the cozy one (you cannot lose), so levels are felt, not needed; turning on stakes and the key guardians is what makes them matter (`../vefr/design/gates-and-guardians.md`). Practice mode (learn by doing) stays in the engine for her other game; Cottage does not use it.
- **Handoff written (2026-10-02 evening):** `.project/CURRENT.md` now holds the restart steps, what is built, what waits on Rylee, and the foreman recipe; VEFR's matching refresh is in `../vefr/.project/CURRENT.md`.
- **Guardians approved, and where the story's last room goes (Rylee, 2026-10-02):** "the guardians are great" (the five round-11 proofs: the Reeve mole, the Bailiff moth, the Warden mushroom elder, the Marshal beetle, the Seneschal robed rat). On the last room: "his seal opens like a treasure room with a lore note and a 'back to town' before you start the next set of dungeons?" So: beating the Cellar King opens a room with a treasure, a lore note, and a way back to town, and act 2 (the next set of dungeons) starts after it. **Structure only; the lore note's words are not written and nothing is canon until Rylee writes or picks them.** This replaces the agent's earlier guess that the realization room sat at the bottom of floor 3 (`docs/story-spine-notes.md` is updated).
- **Round 12, the cellar cast (Codex, two batched calls, drafts; Rylee picks):** eight new regular monsters, files identified by looking (the batch returns them in any order): `cast_shallow_v1` cellar toad in a flowerpot hat, `_v2` crock mimic (a grinning clay jar), `_v3` wick sprite (a living candle stub), `_v4` cellar spider in a cobweb scarf; `cast_deep_v1` cobweb wraith, `_v2` cave cricket, `_v3` barrel mimic, `_v4` root tangle. In `art/source/round12/cast/`, gallery set "Round 12". Not yet cut to 128 px or wired; random floors will pick monsters from per-depth tables, so each depth wants its own cast.
- **Round 13, the gaps (Codex, 8 batched calls, 27 drafts; Rylee: "I will just review and tell you to remove any that are not in our style"):** none removed so far, all 27 looked on-style when checked. Files by what they show (the batch returns them in any order), in `art/source/round13/<batch>/`: `deep_ground` v1 damp flagstone with a moss sheen, v2 mossy rectangular stones, v3 cracked stone with pale roots; `deep_wall` v1 plain, v2 mossy, v3 ivy and roots; `doors` v1 cellar door closed, v2 open, v3 trapdoor, v4 the Cellar King's sealed stone door with the crown seal; `keys_a` v1 the Bailiff's bell key, v2 the Reeve's iron key, v3 the Warden's lantern key; `keys_b` v1 the Seneschal's wax-sealed key, v2 the King's crown seal, v3 the Marshal's helmet key; `treasure` v1 chest closed, v2 chest open and glowing, v3 gold coins, v4 gems; `props_a` v1 crates and sacks, v2 cobweb corner, v3 wall torch, v4 barrels; `props_b` v1 puddle with a drip, v2 broken pot, v3 glowing mushrooms, v4 roots through stone. Notes: the ground tiles are more detailed and show a faint quilted texture compared with the authored flagstone; the trapdoor is drawn in perspective. Not cut or wired yet (the 9 pictures at 288 px grid need `process_tiles.py`, items `process_sprites.py`).
- **The parchment-and-wood skin is in the game (Rylee: "GO", 2026-10-02):** the pack now carries `skins/parchment-and-wood/` (the 19 pictures `skin.json` names, 128 KB; the raw textures and preview stay in `art/skins/`) and `world.json` has `"skin": "skins/parchment-and-wood"`. Two edits to the pack's copy of `skin.json`: the panel's `fill: "parchment"` was removed (VEFR reads `fill` as a picture file; the player ignores a panel fill, so nothing changes visually) and the credit now says "Rylee and Claude; Codex proofs" (the old text said "training: not cleared", which her rights rule replaced). The source in `art/skins/` is untouched. **Rendered and measured** (real game, Playwright, desktop 1280x800 and phone 390x844): 59 and 51 text elements measured against the pixels behind them, none below 4.5:1, the lowest 5.3:1; no console errors, no missing images, no overflow, no target under 44 px; axe-core clean; keyboard focus ring visible (2 px teal); with `prefers-contrast: more` and forced colours the plain UI returns; the skin adds no animation. Getting there needed four fixes in VEFR itself (#211): the declared ink never reached the text inside panels (reader text was 1.4:1), a 32 px panel patch was tiled into stripes behind the text, the menu's left column was missed, and the gold Whisper button kept a gold background under the wood. **Honest leftovers:** a faint lighter band just inside the carved border (cosmetic; the flat fill is slightly lighter than the picture's edge); the Dusk/Dawn pills, the Messages button and the d-pad are still the plain dark style; on a phone the Dusk/Dawn rail covers the level text (127 px, identical without the skin; the planned declutter fixes it); teal headings in the plain menu measure 3.8-4.3:1 with or without the skin (Rylee's accent colour, a design decision); Cottage's `art/tests` has 19 failures on `main`, all from the three briefs written today not following the brief template (and the tests still demand the stale phrase "training: not cleared").
- **The declutter is in (Rylee: "go ahead with the declutter", 2026-10-02):** Interact is the one big button; Talk, Whisper, Bag and Explore are small icon buttons (words kept for screen readers, a tiny key letter each); the Dusk/Dawn rail moved into Menu > Display ("Time of day"); the top bar is just Menu. This fixed the phone overlap listed above (the rail covered the level text) and two more found while measuring (the health/level/gold row ran under the Menu button; the phone Messages panel sat on the wrapped HUD). Real browser, Cottage with the skin: no two controls overlap at 390/360/320 px wide or at 1280/900; 0 text elements under 4.5:1; no target under 44 px; axe clean. Still true: the Messages button and the d-pad keep the plain dark style under the skin; in phone landscape the place name can sit over the d-pad's top button for 4 seconds (taps pass through); the teal menu headings are the accent-colour decision above.
- **Claude's note:** an offload research worker failed on this VM (`no MiniMax key`); engine foremen should run on Bazzite.

## 2026-10-01 (evening) — Rylee's first playtest of the demo

Her words, in order: "the humonguously big cat made me giggle." "the little bugs were kinda fun." "the first book renders when you leave the house, so you have to walk over your front door (something with the internal vs external cells)." "the wander around and fight things loop feels VERY castle of the winds to me, which I consider a win." "the ui is... coming along <3.... it just really tickles me. the notes, the characters, the items. I can't wait to make it a full thing."

- **Fixed (agent):** the note "A Note Left at the Door" sat at town tile (4,4), which is inside the little house's footprint behind the town door at (4,5); you arrive outside at (4,6). It now sits at (5,6) in the town, one step right of where you arrive, so you find it without going through your own door. Tested by stepping right from the arrival tile.
- **Claude's note, for Rylee to decide:** the cat is drawn as tall as the hero because the player draws every character at the same height (1.5 tiles). It made her giggle, so it has not been changed. Options: keep it as a running joke, or give each sprite a size (a pack-level scale), which is a small engine change.
- **Characters have their own size now (Rylee's pick):** after the giant cat she chose "Make characters their own size". The engine now reads `player.sprite_scale` (0.2 to 2; 1 is standard, 1.5 tiles tall). Cottage sets the cat 0.45, rat 0.5, moths 0.65, rustle 0.85, shade 0.9, dwarf smith 0.85; everyone else stays 1. Claude's note: these numbers are a first guess to tune by eye (the rat may want to be a little bigger). The engine change is in VEFR (PR #186); a game on an older engine just ignores the setting.
- **What worked:** the walk-around-and-fight loop reads as Castle of the Winds, which is the goal. The monsters (the moths especially), the notes, the characters and the items landed.

## 2026-10-01 (later) — the story spine, from Rylee's picks

Rylee picked these from options the agent drafted out of the cellar notes already in the pack. Her picks, quoted exactly as she chose them:

- **Truth one** (what the town will not say about the old tavern that burned): "The fire was meant to hold something down".
- **Truth two** (what the town will not say about the one who went down on purpose): "They came back, and they are in town". **Who:** "The Spell Keeper".
- **The realization at the end:** "What is held down is the town's own kindness".

Claude's note: this matches her earlier notes ("2 pieces of truth and then a realization at the end"; the Keeper "knows what the hero learns at the end from the beginning"). Working notes and a reveal map are in `docs/story-spine-notes.md`; none of it is canon until Rylee moves it into `STORY.md`. Still hers to decide: who the letter's "keeper" is, what exactly was held down (a room, a creature, a fire or a feeling), whether the hero remembers going down before, and how long the ending is.

## 2026-10-01 (later) — the new art and residents in the game (agent drafts, waiting on Rylee)

Rylee kept seven residents from the round 8 pictures (the keeper with the staff, the tavern regular, the trader, the cat, the fisher, the gardener, and the dwarf smith redrawn chibi) and picked hero walk version 1 and the geometric rug. **The names ("The Tavern Regular", "The Cat", "The Fisher", "The Gardener", "The Dwarf Smith"), their voice files and their dusk and dawn first lines are agent drafts**, written to make the loop playable. They are hers to keep, rename, rewrite or bin. The four notes still unwritten for the story are listed in `docs/story-spine-notes.md`.

Claude's note: this repo now also holds `art/tools/` and `art/tests/` (sprite and tile and UI-skin tools with unit tests; run `uv run --offline --with pillow python -m unittest discover -s art/tests -t .`). `AGENTS.md` still says the repo has no tests of its own; that line is Rylee's to update.

## 2026-10-01 — the Spell Keeper draft is approved (Rylee)

Rylee told the agent on 2026-10-01 that she worked through the 2026-09-29 agent draft (the Spell Keeper, her lines and seed bank, the two books, the three-rule `logbok.md`, the world description and creed) with an agent and that it is **approved**. It no longer waits on her. `STORY.md` is still hers to write; nothing was added to it. If a line changes again, record it here.

Playtest note (agent, 2026-10-01, woven offline build, desktop): the title screen and the first room load with no console errors. The hero starts bottom right of the cottage room; one arrow press moves her one tile (she starts at tile 4,5; the "about four tiles" look came from the display scale of up to 3x plus held-key repeat, corrected 2026-10-01 after a foreman measured it), and the exit is a door below the bottom wall that needs the hero lined up with it and Interact (F) pressed. The Strike / Console / Hurl an insult buttons show with nothing to fight. Claude's note: both worth a look, neither is a decision.

## 2026-09-29 — agent draft: the story layer (waiting on Rylee)

Built through the studio: Act 1's town map (the Map Room's own check +
build), plus one book. The words below are an **agent draft drawn only
from Rylee's own NOTES** — not canon. `STORY.md` stays hers; every line
is hers to keep, change or bin.

Drafted (all draft):
- `world.json` description (Rylee's BRIEF pitch, verbatim) and creed.
- `logbok.md` — three plain rules.
- the spell keeper: `voices/keeper.md`, the two seed lines, the offline
  fragment bank, and the ledger anchors. Renamed "The Keeper" to
  "The Spell Keeper"; she stands at the shop door.
- one book she hands over: `library/the-burnt-taverns-tab.md`, and one lying
  by the cottage door (`library/a-note-left-at-the-door.md`, a map find).
- the Emberfield leftovers (map note, world-tree history) cleared.

The woven game now draws the people, not just the map: the Spell Keeper
appears on her tile so you can see who is there to talk to.

Read the spell keeper's lines against your notes before they ship.

## 2026-09-26
- **The pitch is written** (Rylee, BRIEF.md): "a fun, low bandwidth way to
  be able to be curious when I can't do anything but still want to do
  *something*." Verb: explore. Done when "I lost an evening to it."
- **Title picture and colour** (Rylee's picks): the dusk cottage with one
  stair going down (`assets/title.webp`), and dusk teal `#3F7E84`.
- **Things Rylee wants to find while exploring**: a piece of history (a
  story, a trinket or picture), a hidden door, a spell book, armor or a
  weapon. Painted as stickers (media_files, `designs/vefr/art/cottage/finds/`).
- **Ideas, not decided yet** (Rylee): "I always liked how there were hidden
  rooms in cotw", and "you could randomly teleport as a form of hard mode".
  Claude's note: an opt-in hard mode would keep the default low bandwidth.
- **How hidden rooms felt in CotW** (Rylee): "I used wasd mostly, lots of
  hitting walls and hoping the spiders didn't get me." Claude's note:
  walking into a wall as the only "search" keeps controls simple.
- **Progression** (Rylee): "a normal everquest-like progression is good."
- **The town** (Rylee): "a lone tavern with a few npc's in it", as an
  interior, "and evidence of an older tavern that burned down".
- **Where the stair starts** (Rylee): "right out of the cottage, like you
  just couldn't help but keep going down. maybe you're a bit of an
  outcast because of it".
- **The ending's shape** (Rylee): "2 pieces of truth and then a realization
  at the end"; the realization changes how you see the town, the cottage
  and yourself ("all of the above"). What the truths are is still open.
- **The tavern's feel** (Rylee): "cozy but wary of you".
- **The one who isn't wary** (Rylee): the spell keeper. "she gives you a
  little discount and maybe a baked good and a happy word when you see her".
  And "she's the one that probably knows what the hero learns at the end
  from the beginning".
  "She loves to bake little loaves of pound cakes with cinnamon and honey."
  Her look (Rylee's pick of three drafts, "spell keeper C"): plump and
  cheerful, dark curly hair tied in a teal scarf, freckles, a brown cardigan
  with rune buttons, a tiny glowing rune above her palm. Draft art only
  (media_files `designs/vefr/art/cottage/drafts/spell-keeper/`).
- **Decision: the release is made IN VEFR** (Rylee: "I want the actual
  release to be made IN vefr, ok?"). Hand-made pictures and notes are drafts,
  reference and templates. The shipped game comes out of the studio:
  characters through the Folks room, pictures from studio modules, the file
  from `ratatoskr weave`.
- **Playing CotW** (Rylee): most essential to recreate first are going
  down the stairs, loot and mystery items, and carrying and packing.
  Inventory in CotW and Diablo is "not terribly rewarding"; the reward is
  opening and finding something fun. Decisions in DESIGN.md.
- **Models help in the studio; the game is a finished artifact** (Rylee).
  Residents and local models help while the game is being made, inside
  templates and structure, and Rylee approves what they draft. The shared
  game plays completely without a model. Cottage of the Breeze doesn't
  offer one (VEFR's default); see VEFR `docs/adr/0003`.
- **Losing: the player chooses** (Rylee). At the start: Cozy (you faint
  and wake in the temple, losing a little gold or an unidentified item,
  never progress) or Classic (death is real; load a save). A Classic run
  can switch to Cozy later, never back.
- **Time: turn-based** (Rylee), like the original. Nothing moves until the
  player acts; then monsters take their turn.
- **Working title: Cottage of the Breeze** (Rylee). A cozy name of its own,
  so a shared version never needs renaming.
- The game's home is this private repo. The pack was scaffolded by VEFR's
  "begin a new world": it currently holds the **Emberfield demo frame**
  (CC0; see `worlds/cottage-of-the-breeze/LICENSE`) as placeholder: map,
  keeper voice, logbok. All of it is meant to be replaced by Rylee's own.
- Structural order (Rylee): this home → the Library ruleset → Spark (the
  local brain).

## 2026-09-25
- The first studio game is a *Castle of the Winds* remake, built inside
  VEFR, step by step, as the way to build VEFR (estate vision doc Q9).
- Rylee writes the stories; Urðr keeps the Library.

Also: the town is drawn (through the Map Room's own route): the cottage
with its stair down just outside the door (the real stair tile), the lone
tavern where the Spell Keeper is, a path between them, the burned walls of
the old tavern, and the temple with its rug. Grass outdoors, wood floors
inside, cobbled walls.

The map now has a camera (vefr): the town still shows whole, and a bigger
map would scroll with the hero. The characters are sprites from Rylee's art.

There are rooms inside now (vefr regions + transitions): step on the
cottage door to enter the cottage, the tavern door to enter the tavern -
the Spell Keeper is in there, behind the bar.

The stair goes down now: a first dungeon floor (30x20) hangs off the
top-left stair, with a stone floor, walls, rubble and an up-stair back to
town. The named places answer when you use them. Doors are used (press
Interact), not walked through.

**floor-1 is the authored floor.** Like the original's fixed first level,
floor-1 is written by hand, not generated - it is where the introduction
lives. Deeper floors can be built from rules later.

Intro lore drafted there (agent draft, Rylee's to keep): four notes found
on the floor - a scrap about two things the town will not say, a burned
page about the old tavern, a candle and a note left by someone who went
down before you, and a coin set face-down.

**Generated floors begin.** floor-2 and floor-3 were drawn by the engine's
new generator from the seed 'cottage-1' (norns delve), hung off floor-1's
down-stair. floor-1 stays authored; these came out of rules. Rerun with a
different seed for a different dungeon - or hand-fix any of the maps.

Fog of war on the floors (vefr): only what you have walked is drawn - a
lit radius around you, your path remembered dimmer, the rest black.
floor-1/2/3 have it; the town and rooms stay bright.

The floors are big now: 48x32, 16 rooms, and a foggy floor is read a
screen at a time and scrolls. Deeper floors can be made bigger or
tighter.

Something to fight: enemies on the three floors (a cellar rat; shades and
moths; a rustle), the hero has health 6 / attack 2, and dying is Cozy -
you wake in the temple with everything that mattered. Walk into a monster
to hit it; it will come at you when it sees you.

Things to find and carry: the rat on floor-1 drops a cloudy potion, a
floor-2 monster drops a brass ring, and the chest's letter comes with a
ring. Walk onto a drop to take it; the Bag (in the menu) lists what you
carry. Item art from the painted Delve set.

The reward end: The Trader keeps a stall on the road (Interact to trade -
sell what you carried, buy a potion). Gold and the bag persist; the Bag has
its own button and the B key. A cloudy potion can be drunk from the Bag to
heal. No identifying or haggling yet.

## 2026-10-01: the new art and residents are in the game

- **Hero** is the new idle pose (round 9). **Residents:** the Spell Keeper wears the old-keeper picture, the Trader the trader, and five new people were added with the studio's own
  `place_character` route on a copy of this pack: the Tavern Regular (tavern), the Cat (cottage, by the rug), the Fisher, the Gardener and the Dwarf Smith (town). `EDITS.md` records them.
- **Ground:** the town's grass and cobbled street, the tavern's dark planks and the cellar floors are 3x3 grid pictures (one scene, so they do not repeat tile by tile). The cottage's
  rug is ONE object (the geometric rug laid on the floor as a 3 x 2 grid), so its map block `DDD` sits at x 3 to 5 and y 2 to 3 (a grid picks its cell by position: x mod 3, y mod 2).
  The cottage, tavern and town walls and houses use the round 2 stone and wood. The tavern's tables and bar are the round table and the bookshelf on the plank floor.
- **Sprites are keyed by the speaker's id** (`hearth-cat`, `vendor`, `tavern-regular`, ...): the woven player draws a speaker with the sprite named like its id; a speaker's own `sprite` field is
  not read (the loader drops it). So the cat's picture is `sprites/cat.png` under the key `hearth-cat`.
- Two engine bugs found by doing this with the real route are fixed in vefr (#183: a write on a multi-room pack threw away the room list; #184: placement checks used the home room's map).


## 2026-10-04 — the Keybearers have names (Rylee)

Rylee picked the names: floor 3 **Ashwing** (the great pale moth), floor 4 **Brother Sporeling** (the old mushroom elder), floor 5 **Sir Hollowhorn** (the armoured stag beetle). Changed in `blueprint.json` and the album, then `vefr normalize`; `vefr check` passes. Their epithets and any lines are still open; the King's name is not chosen yet.
