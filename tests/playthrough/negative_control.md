# Negative control for `tests/playthrough/run.py`

## 1. the way down is walled in

Broken on purpose: descent.entry moved from cottage [1, 1] to cottage [0, 0], a wall.

- result: `ok: False` (109 steps)
- checks that went red: ['the whole route completed', 'the sound cues fired as the route was played', 'every album sticker this route can be sure of was found (chance drops are reported, not required)', "nothing is painted over the note dialog's own buttons"]

## 2. the route is pointed at a room that does not exist

Broken on purpose: `--entry-at attic,1,1`. Nothing in the pack has an `attic`, so the descent has no route to it at all.

- result: `ok: False` (78 steps)
- `the whole route completed`: 'no open route from tavern to attic'
- checks that went red: ['the whole route completed', 'the sound cues fired as the route was played', 'every album sticker this route can be sure of was found (chance drops are reported, not required)', "nothing is painted over the note dialog's own buttons"]

## Verdict

The bot can fail.
