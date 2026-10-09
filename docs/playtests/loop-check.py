#!/usr/bin/env python3
"""One-off checks on the descent loop: can the hero get home from the
generated floors, and does the descent menu remember how deep she got?"""
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
          text: (document.getElementById('combat-live')||{}).textContent || ''};
}"""
LINE = "() => { const e = document.getElementById('descent-line'); return e ? e.textContent : ''; }"

def menu_line(page):
    page.keyboard.press("Escape"); page.wait_for_timeout(250)
    stale = page.evaluate(LINE)
    page.click("#menu-descent"); page.wait_for_timeout(300)
    opened = page.evaluate(LINE)
    page.keyboard.press("Escape"); page.wait_for_timeout(250)
    return {"on_menu_open": stale, "in_descent_panel": opened}

with sync_playwright() as pw:
    b = pw.chromium.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1280, "height": 720})
    page = ctx.new_page()
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.goto(f"file://{html_path}")
    page.wait_for_timeout(400)
    page.click("#ts-enter"); page.wait_for_timeout(500)

    print("MENU LINE BEFORE:", json.dumps(menu_line(page)))
    page.keyboard.press("Escape"); page.wait_for_timeout(200)
    page.click("#menu-descent"); page.wait_for_timeout(250)
    page.click("#descent-new"); page.wait_for_timeout(1000)
    if page.evaluate("() => { const m = document.getElementById('menu');"
                     " return !!(m && !m.hidden); }"):
        page.keyboard.press("Escape"); page.wait_for_timeout(300)
    print("AFTER NEW DESCENT:", json.dumps(page.evaluate(STATE)))
    print("MENU LINE ON FLOOR 1:", json.dumps(menu_line(page)))

    bot = COT.Bot(page, max_steps=20000, wall_seconds=300.0, delay_ms=40)
    bot._regions = None; bot._transitions = None
    r = page.evaluate("""(n) => { const r = window.VEFR_REGIONS[n];
        const out = {up: null, down: null};
        for (let y=0;y<r.map.length;y++) for (let x=0;x<r.map[y].length;x++) {
          if (r.map[y][x]==='u' && !out.up) out.up=[x,y];
          if (r.map[y][x]==='d' && !out.down) out.down=[x,y]; }
        return out; }""", "cellar-0-1")
    print("STAIRS cellar-0-1:", r)

    # 1. go HOME from floor 1 of the descent
    bot.navigate_to("cellar-0-1", r["up"][0], r["up"][1])
    print("AT UP STAIR:", json.dumps(bot.state()["combat"]["region"]),
          bot.state()["combat"]["hero"]["at"])
    bot.interact(); page.wait_for_timeout(1200)
    s = page.evaluate(STATE)
    print("WALKED UP FROM DESCENT FLOOR 1 ->", json.dumps(s))
    b.close()
os.unlink(html_path)