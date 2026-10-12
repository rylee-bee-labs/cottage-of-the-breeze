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
ends in**, opening every book the pack puts on the way → the Cellar King on
the last floor, who yields his seal → the vault there, whose note ends the
act → back up to town, which must now load its after-the-cellar state → a
reload → the menu's Start
over → a fight on the way down.

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

## Checked

the entry tile has exactly one way down and it is the descent; every floor
of the act's Section is walked, and each one's far end is inside the
explored map the descent itself saved; every book the pack places on the
route can be found and read; the Cellar King yields his seal into the bag;
the vault's note ends the act — end card once, focus on Keep exploring,
gone after Interact, gone after a reload; the vault chest drops its
treasure into the bag; the town after the cellar is loaded; Start over
asks first and Cancel clears nothing; every album sticker the pack defines
is found; a descent monster can still be fought; the sound cues fire; the
hero's walk frames show in all four directions; no console errors, no
failed requests, no sideways scroll.

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