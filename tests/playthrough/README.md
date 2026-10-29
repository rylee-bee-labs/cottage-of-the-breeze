# Cottage playthrough bot

`run.py` weaves the pack, opens the HTML in headless Chromium, and plays
to the end with keys only (arrows, `e`, `Tab`, `Enter`, `Escape`), reading
state from `window.VEFR_COMBAT`/`VEFR_REGIONS`/`VEFR_TRANSITIONS`. Writes
`report.json`.

Run from a VEFR checkout whose venv has Playwright (`--viewport phone` = 390x844):

    cd ~/worktrees/vefr-r1
    uv run --offline --group test python <repo>/tests/playthrough/run.py \
        --viewport desktop

`--pack` defaults to this repo's `worlds/cottage-of-the-breeze`.

## The route, and where it comes from

cottage (the cat, the little cloth book) → town (its two notes) → the tile
`world.json` → `descent.entry` names → **every floor of the Section the act
ends in**, opening every book the pack puts on the way → the Key Warden on
the last floor, whose challenge comes first: keeping the rule it keeps sets
its flag, and that flag is what puts the gems it carries in the bag → the
vault there, whose note ends the act → back up to town, which must now load
its after-the-cellar state → a
reload → the menu's Start
over → a fight on the way down.

Walking it reads what the player reads as solid: map tiles, prop footprints
(VEFR's object layer) and, when the pack sets `player.people_block`, the
tiles residents stand on. To talk, the bot stops on an open tile beside a
resident. The after-the-cellar town is checked by walking up to a place its
`town_states` state rewrites and reading it with Interact.

Nothing on that route is written down here. The entry tile comes from
`VEFR_DESCENT_DEF.entry`, the floor names from each Section's `id`,
`floors` and `pattern`, the stairs from the transitions the engine wires
on arrival, and the books from `VEFR_LIBRARY`. The book that ends the act
is found by reading the pack's own rules for `complete-act`. Move a floor,
a book or a landing in the pack and this bot follows it.

**Monsters.** The descent is walked with the Section's families taken away,
which is what vefr's own `tests/test_descent_bot.py` does and why: the
thing under test is the route, not a fight. The lever is the engine's
documented harness hook (`VEFR_DESCENT_DEF` is read at call time, "and a
harness may plant its own"), so **nothing on disk changes**. The run puts
the families back at the end and fights, so the walk-and-fight loop is
still proved. `--monsters` walks the whole descent with them in place.

**Falls.** With monsters in place the hero can fall. The fall card ("You
fell. ...") is closed with a key, as a player closes it, and the walk carries
on from where the hero woke: the floor's own stair, or home when the pack's
descent says `fall: "home"`, from where the bot walks back down through the
town stair (which starts at the deepest landing when the pack says
`resume: "deepest-landing"`). `report.json` counts them as `falls`.

## Checked

the entry tile has exactly one way down and it is the descent; every floor
of the act's Section is walked, and each one's far end is inside the
explored map the descent itself saved; every book the pack places on the
route can be found and read; the Key Warden's challenge sets its flag on the
warden's floor and the gems it carries are in the bag before the ending note
is read; the vault's note ends the act — end card once, focus on Keep
exploring, gone after Interact, gone after a reload; the vault chest drops
its treasure into the bag; the town after the cellar is loaded; Start over
asks first and Cancel clears nothing; each resident who hands over a book
gives it and it can be read; every album sticker the route can be sure of is
found (a sticker whose item only a descent family drops is a chance drop, or
sits in a later Section: it is listed, not required); a descent monster can still be fought; the sound cues fire; the
hero's walk frames show in all four directions; no console errors, no
failed requests, no sideways scroll.

**Overlay layering** (cottage#165). Every time a note dialog is open the
bot hit-tests it: the topmost element at the centre of each of the
dialog's own controls has to belong to the dialog, and the on-screen
Interact button must not be the topmost thing at its own centre while a
dialog is up. It is asked of the DOM rather than of a screenshot, because a
screenshot cannot say whether a blob belongs there. The first check needs a
dialog to have been open during the run and goes red on an empty sample
rather than passing vacuously; the Interact rule is sampled only while the
page has no toast or message line of its own showing.

The 'RE●D ON' defect the 2026-10-14 phone UAT recorded was **not** a
stacking problem, as the first triage assumed. A real browser found that
the reader card's `max-height` pushed the READ ON control *below the fold*
in a long note, so it was off the visible area rather than painted over.
That was fixed in the engine's stylesheet (`vefr` `web/player/parts/
020-style.css`) and merged as **vefr#509 on 2026-10-15** — engine work, so
it lands as a companion change and never as an edit to `../vefr/`. What
this probe is now for is regression: the dialog's controls have to stay
reachable and un-painted-over. The assertions are unchanged and are not to
be weakened to make a run go green (`NOTES.md`, 2026-10-15).

Two of the nine sound cues have **no subject in this pack** and are
asserted as such rather than quietly dropped: `locked` (no transition
names a `requires` since the authored floors went), `level` (a generated
monster is built without an `xp`). `pickup` has a subject now: the
families name `drops`, so the cue is required, and the fight at the end
of the run picks up what its kills leave. Each has a check that goes red
the day the pack changes its subject.

## Proving it can fail

`negative_control.py` breaks the route on purpose, twice — once by putting
the authored `town [1,1] -> floor-1` door back (the exact thing that broke
this bot), once with `--entry-at 4,5`, a tile that is not the way down —
and fails unless each run comes back red for the right reason. It writes
`negative_control.md`.

    uv run --offline --group test python <repo>/tests/playthrough/negative_control.py