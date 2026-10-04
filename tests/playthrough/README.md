# Cottage playthrough bot

`run.py` weaves the pack, opens the HTML in headless Chromium, and plays
to the end with keys only (arrows, `e`, `Escape`), reading state from
`window.VEFR_COMBAT`/`VEFR_REGIONS`/`VEFR_TRANSITIONS`. Writes `report.json`.

Run from a VEFR checkout whose venv has Playwright (`--viewport phone` = 390x844):

    cd ~/worktrees/vefr-r1
    uv run --offline --group test python <repo>/tests/playthrough/run.py \
        --pack <repo>/worlds/cottage-of-the-breeze --viewport desktop
Checked: locked stairs refuse on floors 3-5; each key is bagged only after
its Keybearer falls; the seal opens the door; the end card shows once (focus
on Keep exploring) and stays gone after reload; Start over asks first and
Cancel clears nothing; no console errors, no failed requests, no sideways scroll.
