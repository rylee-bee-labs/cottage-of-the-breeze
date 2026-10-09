#!/usr/bin/env python3
"""One-off: walk through the town door into floor-1 and screenshot the
first few steps, to see whether the arrival view recovers."""
import importlib.util, os, sys, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("cottage_bot", REPO / "tests/playthrough/run.py")
COT = importlib.util.module_from_spec(spec); spec.loader.exec_module(COT)

from vefr.cli import weave_html
pack = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2])
html = weave_html(pack)
fd, html_path = tempfile.mkstemp(suffix=".html")
os.write(fd, html.encode()); os.close(fd)

STATE = """() => {
  const c = window.VEFR_COMBAT || {};
  const vr = document.getElementById('verb-row');
  const v = vr && !vr.hidden ? vr.getBoundingClientRect() : null;
  const shell = vr ? vr.offsetParent : null;
  const sr = shell ? shell.getBoundingClientRect() : null;
  return {region: c.region, at: c.hero && c.hero.at,
          viewport: {w: window.innerWidth, h: window.innerHeight},
          verbRow: v ? {x: Math.round(v.x), y: Math.round(v.y),
                        w: Math.round(v.width), h: Math.round(v.height),
                        buttons: [...vr.querySelectorAll('button')].map(b => {
                          const r = b.getBoundingClientRect();
                          return {t: b.textContent.trim(),
                                  x: Math.round(r.x), y: Math.round(r.y),
                                  w: Math.round(r.width), h: Math.round(r.height),
                                  clipped: b.scrollWidth > b.clientWidth + 1};
                        })} : null,
          toasts: [...document.querySelectorAll('.toasts, #toasts, .toast')]
                   .filter(e => e.offsetParent)
                   .map(e => { const r = e.getBoundingClientRect();
                     return {id: e.id || e.className, x: Math.round(r.x),
                             y: Math.round(r.y), w: Math.round(r.width),
                             h: Math.round(r.height)}; }),
          playPanel: (() => { const e = document.getElementById('stage');
                     const r = e ? e.getBoundingClientRect() : null;
                     const dark = r ? {x: Math.round(r.x), y: Math.round(r.y),
                                       w: Math.round(r.width), h: Math.round(r.height)} : null;
                     return dark; })(),
          canvasBox: (() => { const e = document.getElementById('town-canvas');
                     const r = e ? e.getBoundingClientRect() : null;
                     return r ? {x: Math.round(r.x), y: Math.round(r.y),
                                 w: Math.round(r.width), h: Math.round(r.height)} : null; })(),
          offsetParent: shell ? (shell.id || shell.className || shell.tagName) : null,
          parent: sr ? {x: Math.round(sr.x), y: Math.round(sr.y),
                        w: Math.round(sr.width), h: Math.round(sr.height)} : null};
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1280, "height": 720})
    page = ctx.new_page()
    page.goto(f"file://{html_path}")
    page.wait_for_timeout(400)
    page.click("#ts-enter"); page.wait_for_timeout(500)
    bot = COT.Bot(page, max_steps=20000, wall_seconds=300.0, delay_ms=60)
    bot.ensure_region("town")
    bot.navigate_to("town", 1, 1)
    bot.interact(); page.wait_for_timeout(1200)
    page.screenshot(path=str(out / "arrival-floor1-step0.png"))
    import json; print("step0", json.dumps(page.evaluate(STATE)))
    for i in (1, 2, 4):
        for _ in range(i if i == 1 else 1):
            pass
        for _ in range({1: 1, 2: 1, 4: 2}[i]):
            bot.press("ArrowDown")
        page.wait_for_timeout(700)
        page.screenshot(path=str(out / f"arrival-floor1-step{i}.png"))
        print(f"step{i}", json.dumps(page.evaluate(STATE)))
    b.close()
os.unlink(html_path)