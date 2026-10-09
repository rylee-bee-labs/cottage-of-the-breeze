#!/usr/bin/env python3
"""One-off: enter the generated descent and press single keys, logging where
the hero actually ends up. Used to pin down the first-step-out-of-descent."""
import importlib.util, json, os, sys, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("cottage_bot", REPO / "tests/playthrough/run.py")
COT = importlib.util.module_from_spec(spec); spec.loader.exec_module(COT)

from vefr.cli import weave_html
pack = Path(sys.argv[1]).resolve()
html = weave_html(pack)
fd, html_path = tempfile.mkstemp(suffix=".html")
os.write(fd, html.encode()); os.close(fd)

STATE = """() => {
  const c = window.VEFR_COMBAT || {};
  return {region: c.region, at: c.hero && c.hero.at, hp: c.hero && c.hero.hp,
          text: (document.getElementById('combat-live')||{}).textContent || '',
          regions: Object.keys(window.VEFR_REGIONS||{}),
          trans: (window.VEFR_TRANSITIONS||[]).filter(t => String(t.from).startsWith('cellar')
                  || (t.from==='town' && String(t.at)==='1,1'))
                  .map(t => `${t.from} ${JSON.stringify(t.at)} -> ${t.to} ${JSON.stringify(t.to_at)}`)};
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1280, "height": 720})
    page = ctx.new_page()
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    page.goto(f"file://{html_path}")
    page.wait_for_timeout(400)
    page.click("#ts-enter"); page.wait_for_timeout(500)

    page.keyboard.press("Escape"); page.wait_for_timeout(250)
    page.click("#menu-descent"); page.wait_for_timeout(250)
    page.click("#descent-new"); page.wait_for_timeout(900)
    if page.evaluate("() => { const m = document.getElementById('menu');"
                     " return !!(m && !m.hidden); }"):
        page.keyboard.press("Escape"); page.wait_for_timeout(300)
    print("AFTER NEW DESCENT:", json.dumps(page.evaluate(STATE), indent=1)[:1400])

    for key in ["ArrowRight", "ArrowRight", "ArrowDown", "ArrowUp", "e"]:
        page.keyboard.press(key)
        page.wait_for_timeout(500)
        s = page.evaluate(STATE)
        print(f"AFTER {key}: region={s['region']} at={s['at']} hp={s['hp']} "
              f"text={s['text'][:90]!r}")
    print("TRANS:", json.dumps(page.evaluate(STATE)["trans"], indent=1))
    print("ERRORS:", errs[:5])
    b.close()
os.unlink(html_path)