# Negative control for `tests/playthrough/run.py`

## 1. the entry tile has two ways out

Broken on purpose: authored transition re-added: town [1,1] -> floor-1.

- result: `ok: False` (46 steps)
- checks that went red: ['town [1, 1] is one way down, and it goes to cellar-0-1', 'the door the pack names walks the hero into the descent', 'the whole route completed', 'the sound cues fired as the route was played', 'every album sticker the pack defines was found on this route']

## 2. the route is pointed at a room that does not exist

Broken on purpose: `--entry-at attic,1,1`. Nothing in the pack has an `attic`, so the descent has no route to it at all.

- result: `ok: False` (33 steps)
- `the whole route completed`: 'no open route from town to attic'
- checks that went red: ['the whole route completed', 'the sound cues fired as the route was played', 'every album sticker the pack defines was found on this route']

## Verdict

The bot can fail.
