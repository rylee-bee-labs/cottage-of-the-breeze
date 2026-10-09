#!/usr/bin/env python3
"""One-off: enter the generated descent and walk, logging hp and the last
line of the combat log, to see what a fresh hero meets on floor 1."""
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
          max: c.hero && c.hero.max, lvl: c.hero && (c.hero.level || c.hero.lvl),
          text: (document.getElementById('combat-live')||{}).textContent || '',
          foes: (c.enemies||[]).filter(e => e.alive)
                .map(e => `${e.id}@${e.at} hp${e.hp}`),
          why: (window.VEFR_WHY || []).slice(-4)};
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

    bot = COT.Bot(page, max_steps=5000, wall_seconds=300.0, delay_ms=60)
    region = page.evaluate("() => window.VEFR_COMBAT.region")
    print("region", region)
    # walk to the middle of the floor and back, printing every step
    prev_hp = None
    for i in range(120):
        s = bot.state()
        c = s["combat"]
        if c["region"] != region:
            print(f"step {i}: LEFT {region} -> {c['region']} at={c['hero']['at']} "
                  f"text={s['combat_text'][:160]!r}")
            break
        if c["hero"]["hp"] != prev_hp:
            print(f"step {i}: hp={c['hero']['hp']}/{c['hero']['max']} "
                  f"at={c['hero']['at']} foes={len([e for e in c['enemies'] if e['alive']])} "
                  f"text={s['combat_text'][:120]!r}")
            prev_hp = c["hero"]["hp"]
        near = min(c["enemies"], key=lambda e: abs(e["at"][0]-c["hero"]["at"][0])
                   + abs(e["at"][1]-c["hero"]["at"][1]))
        d = bot.next_dir(region, tuple(c["hero"]["at"]), tuple(near["at"]))
        if d is None:
            print("no path to nearest foe", near)
            break
        bot.press_dir(d)
    else:
        print("120 steps, still alive")
    s = page.evaluate(STATE)
    print("FINAL", json.dumps(s)[:900])
    print("ERRORS", errs[:5])
    b.close()
os.unlink(html_path)