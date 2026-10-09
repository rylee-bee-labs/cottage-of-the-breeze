#!/usr/bin/env python3
"""One-off: where does the combat verb row land on a phone, next to the
d-pad, the Interact button and the toasts?"""
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

BOXES = """() => {
  const box = (sel) => { const e = document.querySelector(sel);
    if (!e || e.offsetParent === null) return null;
    const r = e.getBoundingClientRect();
    return {sel, x: Math.round(r.x), y: Math.round(r.y),
            w: Math.round(r.width), h: Math.round(r.height)}; };
  const vr = document.getElementById('verb-row');
  const buttons = vr ? [...vr.querySelectorAll('button')].map(b => {
    const r = b.getBoundingClientRect();
    return {t: b.textContent.trim(), x: Math.round(r.x), y: Math.round(r.y),
            w: Math.round(r.width), h: Math.round(r.height),
            clipped: b.scrollWidth > b.clientWidth + 1}; }) : [];
  return {viewport: {w: innerWidth, h: innerHeight},
          boxes: ['#verb-row', '#interact', '.dpad', '#toasts', '.acts']
                 .map(box).filter(Boolean),
          verbButtons: buttons,
          interactClipped: (() => { const e = document.getElementById('interact');
            return e ? {w: e.clientWidth, scrollW: e.scrollWidth,
                        clipped: e.scrollWidth > e.clientWidth + 1,
                        label: (e.textContent||'').trim().slice(0,30)} : null; })()};
}"""

def overlap(a, b):
    ax2, ay2 = a['x']+a['w'], a['y']+a['h']
    bx2, by2 = b['x']+b['w'], b['y']+b['h']
    return max(0, min(ax2, bx2)-max(a['x'], b['x'])) * max(0, min(ay2, by2)-max(a['y'], b['y']))

with sync_playwright() as pw:
    b = pw.chromium.launch(headless=True)
    for name, vp in (("phone", {"width": 390, "height": 844}),
                     ("desktop", {"width": 1280, "height": 720})):
        ctx = b.new_context(viewport=vp)
        page = ctx.new_page()
        page.goto(f"file://{html_path}")
        page.wait_for_timeout(400)
        page.click("#ts-enter"); page.wait_for_timeout(500)
        bot = COT.Bot(page, max_steps=20000, wall_seconds=300.0, delay_ms=50)
        bot.ensure_region("town")
        bot.navigate_to("town", 1, 1)
        bot.interact(); page.wait_for_timeout(1200)
        # walk down until the verb row appears (a monster is in range)
        found = False
        for _ in range(40):
            m = page.evaluate(BOXES)
            if any(b['w'] for b in m['verbButtons']):
                found = True
                break
            bot.press("ArrowDown")
        print(f"### {name} {vp} verb row visible: {found}")
        print(json.dumps(m, indent=1))
        def contains(a, c):
            return (a['x'] <= c['x'] and a['y'] <= c['y']
                    and a['x']+a['w'] >= c['x']+c['w']
                    and a['y']+a['h'] >= c['y']+c['h'])
        pairs = [(a, c) for i, a in enumerate(m['boxes'])
                 for c in m['boxes'][i+1:]]
        for a, c in pairs:
            if contains(a, c) or contains(c, a):
                continue   # a box and its own container are not an overlap
            ov = overlap(a, c)
            if ov:
                print(f"OVERLAP {a['sel']} x {c['sel']} = {ov}px2")
        for a in m['boxes']:
            for bt in m['verbButtons']:
                ov = overlap(a, {'x': bt['x'], 'y': bt['y'], 'w': bt['w'], 'h': bt['h']})
                if ov:
                    print(f"OVERLAP {a['sel']} x verb '{bt['t']}' = {ov}px2")
        ctx.close()
    b.close()
os.unlink(html_path)