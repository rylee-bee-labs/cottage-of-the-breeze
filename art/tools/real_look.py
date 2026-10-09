#!/usr/bin/env python3
"""real_look.py: screenshot the REAL woven player, at any viewport size.

  real_look.py --html woven.html --out look.png [--size 1280x800] [--steps e,o]
  real_look.py --html woven.html --out look.png --element '#menu .carved'
  real_look.py --html woven.html --out look.png --click '#menu-open'

Why this exists. `vefr look` (in the VEFR repository) is the tool that
screenshots the woven player, and its viewport is fixed at 1280x800 inside
`src/vefr/devtools.py::_session` - there is no flag for a phone. This tool
does the same three things it does, in the same order, at any size: open the
woven HTML in headless Chromium, click `#ts-enter` (Begin), let the game
settle, optionally click something (`--click '#menu-open'`, repeatable) and
press keys (`--steps`), then screenshot. At `--size 1280x800` with no
`--steps` and no `--click` it produces the same picture `vefr look --html`
produces; that equality is checked by art/tests/test_real_look.py, which runs
`vefr look` and this tool over the same file and compares the bytes.

It is a screenshot of the game, not a drawing of one. `mock_skin.py` draws a
plausible interface from the skin's pictures and is a useful rendering aid;
this one shows what a player would actually see, which is the only way to
catch a decoration that is legal as a file and wrong on screen.

Needs the engine's own dev dependencies (playwright and a Chromium it has
downloaded), so it is run from a VEFR checkout:

  uv run --project ~/code/Rylee-Bee/vefr --with playwright \\
      python art/tools/real_look.py --html dist/player.html --out look.png

and weaves the pack first, with the engine's own weaver:

  uv run --project ~/code/Rylee-Bee/vefr vefr weave --pack worlds/... --out dist/player.html
"""
import argparse
import os
import sys
from pathlib import Path

# The wait `vefr look` gives the game after Begin, and the settle it gives
# after the last key. Kept identical so the two tools photograph the same
# moment; a skin picture with a picture still decoding is not the fault.
SETTLE_MS = 800
FINAL_MS = 3000
STEP_MS = 250
DEFAULT_SIZE = (1280, 800)   # the viewport vefr look hard-codes


def fail(message):
    """A plain one-line problem, exit 2, with no traceback."""
    print(message, file=sys.stderr)
    raise SystemExit(2)


def parse_size(spec):
    """Parse a WxH size like 1280x800, or fail plainly."""
    bits = spec.lower().split("x")
    if len(bits) != 2:
        fail(f"--size wants WxH like 1280x800, got {spec!r}")
    try:
        width, height = int(bits[0]), int(bits[1])
    except ValueError:
        fail(f"--size wants whole numbers like 1280x800, got {spec!r}")
    if width < 1 or height < 1:
        fail(f"--size needs positive numbers, got {spec!r}")
    return width, height


def shoot(html, out, size, steps, element, clicks):
    """Open `html`, press Begin, click and press, screenshot to `out`.

    Returns nothing. Any missing dependency is a plain one-line message and
    exit 2 - never a picture that looks fine and is not the game.

    Anything already at `out` is removed before the browser opens, not after
    it closes. A run that fails with yesterday's `look-phone.png` still lying
    there would leave a file that reads as today's evidence and is not; the
    rule is that a failed run leaves no picture at all.
    """
    if os.path.exists(out):
        os.remove(out)

    try:
        from playwright.sync_api import sync_playwright
    except Exception:  # noqa: BLE001 - missing is a report, not a crash
        fail("playwright is not installed; run this from a VEFR checkout with "
             "`uv run --with playwright`, after `playwright install chromium`")
        return

    if not os.path.isfile(html):
        fail(f"no such file: {html!r} (weave the pack first: `vefr weave --pack ... --out ...`)")

    width, height = size
    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch()
            except Exception:  # noqa: BLE001 - Chromium not downloaded
                fail("chromium is not installed for playwright; run "
                     "`playwright install chromium`")
                return
            try:
                page = browser.new_page(viewport={"width": width, "height": height})
                page.goto(Path(html).resolve().as_uri())
                page.click("#ts-enter")
                page.wait_for_timeout(SETTLE_MS)
                for selector in clicks:
                    try:
                        page.click(selector)
                    except Exception:  # noqa: BLE001 - a wrong selector is a report
                        fail(f"{selector!r} matched nothing to click in the running game")
                    page.wait_for_timeout(STEP_MS)
                for key in (k.strip() for k in steps.split(",") if k.strip()):
                    page.keyboard.press(key)
                    page.wait_for_timeout(STEP_MS)
                page.wait_for_timeout(FINAL_MS)
                if element:
                    handle = page.query_selector(element)
                    if handle is None:
                        fail(f"no element matches {element!r} in the running game")
                        return
                    handle.screenshot(path=out)
                else:
                    page.screenshot(path=out)
            finally:
                browser.close()
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001 - a broken run must not print a picture
        fail(f"the screenshot failed: {type(e).__name__}: {e}")


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True, description=__doc__.splitlines()[0])
    ap.add_argument("--html", required=True, metavar="FILE",
                    help="a woven player HTML file (from `vefr weave`)")
    ap.add_argument("--out", required=True, metavar="OUT",
                    help="where to write the PNG screenshot")
    ap.add_argument("--size", default=f"{DEFAULT_SIZE[0]}x{DEFAULT_SIZE[1]}",
                    help=f"viewport as WxH (default {DEFAULT_SIZE[0]}x{DEFAULT_SIZE[1]})")
    ap.add_argument("--steps", default="",
                    help="comma-separated keys to press after Begin (as `vefr look --steps`)")
    ap.add_argument("--click", action="append", default=[], metavar="SELECTOR",
                    help="click this before the screenshot; repeat for more than one")
    ap.add_argument("--element", default=None, metavar="SELECTOR",
                    help="screenshot just this element instead of the whole viewport")
    a = ap.parse_args(argv)

    shoot(a.html, a.out, parse_size(a.size), a.steps, a.element, a.click)
    print(f"screenshot: {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())