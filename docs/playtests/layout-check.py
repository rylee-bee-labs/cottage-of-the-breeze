#!/usr/bin/env python3
"""One-off: measure the player's bottom control row and HUD at phone and
desktop sizes, so the report can quote boxes rather than an eyeball."""
import json, os, sys, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[2]
from vefr.cli import weave_html
pack = Path(sys.argv[1]).resolve()
html = weave_html(pack)
fd, html_path = tempfile.mkstemp(suffix=".html")
os.write(fd, html.encode()); os.close(fd)

MEASURE = """() => {
  const out = [];
  const ids = ['interact','dpad','dpad-up','dpad-down','dpad-left','dpad-right',
               'btn-talk','btn-whisper','btn-bag','btn-explore','toasts-toggle',
               'menu-open','menu','hud','status'];
  document.querySelectorAll('button,[id]').forEach(() => {});
  for (const id of ids) {
    const e = document.getElementById(id);
    if (!e) continue;
    const r = e.getBoundingClientRect();
    out.push({id, x: Math.round(r.x), y: Math.round(r.y),
              w: Math.round(r.width), h: Math.round(r.height),
              label: (e.textContent||'').trim().slice(0,24),
              clipped: e.scrollWidth > e.clientWidth + 1,
              scrollW: e.scrollWidth, clientW: e.clientWidth});
  }
  // every control that is on screen and smaller than 44px on its short side
  const small = [];
  document.querySelectorAll('button, [role=button]').forEach(e => {
    const r = e.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    if (r.height < 44 || r.width < 44)
      small.push({id: e.id, cls: e.className, w: Math.round(r.width),
                  h: Math.round(r.height), label: (e.textContent||'').trim().slice(0,20)});
  });
  const cv = document.getElementById('town-canvas');
  const cr = cv ? cv.getBoundingClientRect() : null;
  const canvas = cr ? {x: Math.round(cr.x), y: Math.round(cr.y),
                       w: Math.round(cr.width), h: Math.round(cr.height),
                       share: Math.round(100 * cr.height / window.innerHeight)}
                   : null;
  const combat = [];
  document.querySelectorAll('button').forEach(e => {
    const t = (e.textContent||'').trim();
    if (!/strike|console|insult/i.test(t)) return;
    const r = e.getBoundingClientRect();
    combat.push({id: e.id, cls: e.className, text: t.slice(0,24),
                 x: Math.round(r.x), y: Math.round(r.y),
                 w: Math.round(r.width), h: Math.round(r.height)});
  });
  return {combat, canvas, w: window.innerWidth, h: window.innerHeight,
          scrollW: document.documentElement.scrollWidth,
          boxes: out, small};
}"""

def overlap(a, b):
    ax1, ay1, ax2, ay2 = a['x'], a['y'], a['x']+a['w'], a['y']+a['h']
    bx1, by1, bx2, by2 = b['x'], b['y'], b['x']+b['w'], b['y']+b['h']
    return max(0, min(ax2, bx2)-max(ax1, bx1)) * max(0, min(ay2, by2)-max(ay1, by1))

with sync_playwright() as pw:
    b = pw.chromium.launch(headless=True)
    for name, vp in (("phone", {"width": 390, "height": 844}),
                     ("desktop", {"width": 1280, "height": 720})):
        ctx = b.new_context(viewport=vp)
        page = ctx.new_page()
        page.goto(f"file://{html_path}")
        page.wait_for_timeout(400)
        page.click("#ts-enter"); page.wait_for_timeout(600)
        m = page.evaluate(MEASURE)
        print(f"### {name} {vp} scrollW={m['scrollW']} canvas={m['canvas']}")
        print("combat buttons:", json.dumps(m['combat']))
        print("boxes:", json.dumps(m["boxes"], indent=1))
        ids = {x['id']: x for x in m['boxes']}
        pairs = [('interact','dpad-up'), ('interact','dpad-left'),
                 ('interact','dpad-right'), ('interact','dpad-down'),
                 ('interact','btn-talk'), ('btn-talk','btn-bag')]
        for x, y in pairs:
            if x in ids and y in ids:
                a = overlap(ids[x], ids[y])
                if a:
                    print(f"OVERLAP {x} x {y} = {a}px2")
        print("clipped:", [x['id'] for x in m['boxes'] if x['clipped']])
        print("under 44px:", json.dumps(m['small'])[:600])
        print()
        ctx.close()
    b.close()
os.unlink(html_path)