#!/usr/bin/env python3
"""Play the generated descent with keys only and record what happened.

Throwaway play harness for the 2026-10-08 play-test report. It reuses the
Cottage playthrough bot's navigation (`tests/playthrough/run.py`, imported
rather than copied) so the routes walked here are the same keyboard-only
routes that bot walks, and writes one plain-text log per run so a finding
in `2026-10-09-descent.md` can quote a real line instead of a memory.

Run it from a VEFR checkout whose venv has Playwright::

    uv run --group test python <repo>/docs/playtests/descent-probe.py \
        --pack <repo>/worlds/cottage-of-the-breeze --viewport desktop \
        --out <repo>/docs/playtests/logs/descent-desktop-seed-breeze.txt

`--seed-run N` presses the player's own "New descent" control N times
first, which is how a second and third seed are reached without editing
the pack.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import tempfile
from collections import deque
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[2]
BOT = REPO / "tests" / "playthrough" / "run.py"


def load_bot():
    spec = importlib.util.spec_from_file_location("cottage_bot", BOT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


COT = load_bot()
VIEWPORTS = COT.VIEWPORTS

DESCENT_JS = """() => {
  const c = window.VEFR_COMBAT || null;
  const d = window.VEFR_DESCENT || null;
  let doc = null, lsKeys = [];
  try {
    const raw = localStorage.getItem('vefr-descent-cottage-of-the-breeze');
    doc = raw ? JSON.parse(raw) : null;
    lsKeys = Object.keys(localStorage).filter(x => x.startsWith('vefr-'));
  } catch (e) { doc = {error: String(e)}; }
  return {
    region: c && c.region,
    hero: c && c.hero,
    bag: c && c.bag,
    enemies: c && c.enemies,
    floor: c && c.floor,
    combat_text: (document.getElementById('combat-live') || {}).textContent || '',
    regions: Object.keys(window.VEFR_REGIONS || {}),
    transitions: window.VEFR_TRANSITIONS || [],
    descent_on: !!d,
    descent_line: (document.getElementById('descent-line') || {}).textContent || '',
    descent_doc: doc,
    ls_keys: lsKeys,
  };
}"""

REGION_JS = """(name) => {
  const r = (window.VEFR_REGIONS || {})[name];
  if (!r) return null;
  return {name: name, w: r.map[0].length, h: r.map.length,
          legend: r.legend, map: r.map, title: r.title || null};
}"""


def log(fh, *parts):
    line = " ".join(str(p) for p in parts)
    print(line)
    fh.write(line + "\n")
    fh.flush()


def safe_dir(page, region, cur, target, margin=2):
    """One step toward `target` that keeps `margin` tiles of distance from
    every living monster - the walk a careful explorer makes."""
    grid = page.evaluate(
        """(name) => {
             const r = (window.VEFR_REGIONS || {})[name];
             const c = window.VEFR_COMBAT || {};
             return {map: r.map, legend: r.legend,
                     foes: (c.enemies || []).filter(e => e.alive).map(e => e.at)};
           }""", region)
    rows, legend, foes = grid["map"], grid["legend"], grid["foes"]
    h, w = len(rows), len(rows[0])
    start, goal = tuple(cur), tuple(target)
    if start == goal:
        return None
    blocked = set()
    for fx, fy in foes:
        for dy in range(-margin, margin + 1):
            for dx in range(-margin, margin + 1):
                blocked.add((fx + dx, fy + dy))
    blocked.discard(start)
    prev = {start: None}
    q = deque([start])
    while q:
        cx, cy = q.popleft()
        if (cx, cy) == goal:
            break
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nx, ny = cx + dx, cy + dy
            if not (0 <= nx < w and 0 <= ny < h) or (nx, ny) in prev:
                continue
            if (nx, ny) in blocked:
                continue
            if (legend.get(rows[ny][nx]) or {}).get("solid"):
                continue
            prev[(nx, ny)] = (cx, cy)
            q.append((nx, ny))
    if goal not in prev:
        return None
    node = goal
    while prev[node] != start:
        node = prev[node]
    return (node[0] - start[0], node[1] - start[1])


def walk_safely(page, bot, region, target, margin=2, limit=1500):
    """Walk to `target` avoiding monsters; returns 'arrived' or 'stuck'."""
    for _ in range(limit):
        s = bot.state()
        c = s["combat"]
        if c["region"] != region:
            return "left"
        if bot.handle_overlay(s):
            continue
        at = tuple(c["hero"]["at"])
        if at == tuple(target):
            return "arrived"
        d = safe_dir(page, region, at, target, margin)
        if d is None:
            d = bot.next_dir(region, at, target)
        if d is None:
            return "stuck"
        bot.press_dir(d)
    return "stuck"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--out", required=True, help="log file")
    ap.add_argument("--viewport", default="desktop", choices=sorted(VIEWPORTS))
    ap.add_argument("--floors", type=int, default=4, help="how many floors to descend")
    ap.add_argument("--seed-run", type=int, default=0,
                    help="press New descent this many times before playing")
    ap.add_argument("--shots", default=None, help="screenshot directory")
    ap.add_argument("--delay-ms", type=float, default=1.0)
    ap.add_argument("--sneak", action="store_true",
                    help="walk around monsters instead of through them")
    ap.add_argument("--no-fight", action="store_true",
                    help="skip clearing the floor; walk straight to the stair")
    ap.add_argument("--tag", default="run")
    args = ap.parse_args()

    from vefr.cli import weave_html
    pack = Path(args.pack).resolve()
    html = weave_html(pack)
    fd, html_path = tempfile.mkstemp(prefix="cottage-descent-", suffix=".html")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(html)

    shots = Path(args.shots) if args.shots else None
    if shots:
        shots.mkdir(parents=True, exist_ok=True)

    outfh = open(args.out, "w", encoding="utf-8")
    log(outfh, f"== {args.tag} viewport={args.viewport} pack={pack}")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport=VIEWPORTS[args.viewport])
        page = ctx.new_page()
        errors = []
        page.on("console", lambda m: errors.append(f"console.error: {m.text}")
                if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.goto(f"file://{html_path}")
        page.wait_for_timeout(400)
        page.click("#ts-enter")
        page.wait_for_timeout(500)

        bot = COT.Bot(page, max_steps=100000, wall_seconds=1500.0,
                      delay_ms=args.delay_ms)

        # A region-change trace, so a bot error that says "routing loop"
        # can say which region it was in and how it got there.
        page.evaluate("""() => {
          window.__trace = [];
          let last = (window.VEFR_COMBAT || {}).region || '';
          setInterval(() => {
            const c = window.VEFR_COMBAT || {};
            const now = c.region || '';
            if (now !== last) {
              window.__trace.push({from: last, to: now,
                                   hero: c.hero ? c.hero.at : null,
                                   hp: c.hero ? c.hero.hp : null,
                                   t: Date.now()});
              last = now;
            }
          }, 30);
        }""")

        state = page.evaluate(DESCENT_JS)
        log(outfh, "DESCENT_ON", state["descent_on"])
        log(outfh, "DESCENT_DOC", json.dumps(state["descent_doc"]))
        log(outfh, "REGIONS_AT_START", state["regions"])

        for i in range(args.seed_run):
            page.keyboard.press("Escape")
            page.wait_for_timeout(200)
            # `menu-descent` opens the panel that holds `descent-new`.
            menu_item = page.evaluate(
                "() => { const m = document.getElementById('menu-descent');"
                " const r = document.getElementById('menu-descent-row');"
                " return {exists: !!m, visible: m ? !!(m.offsetParent) : false,"
                " rowHidden: r ? !!r.hidden : null,"
                " label: m ? m.textContent : ''}; }")
            log(outfh, f"NEW_DESCENT_ROW[{i}]", json.dumps(menu_item))
            if menu_item["visible"]:
                page.click("#menu-descent")
                page.wait_for_timeout(250)
            got = page.evaluate(
                "() => { const b = document.getElementById('descent-new');"
                " return {exists: !!b, visible: b ? !!(b.offsetParent) : false,"
                " label: b ? b.textContent : '',"
                " line: (document.getElementById('descent-line')||{}).textContent||''}; }")
            log(outfh, f"NEW_DESCENT_MENU[{i}]", json.dumps(got))
            if got["exists"] and got["visible"]:
                page.click("#descent-new")
                page.wait_for_timeout(900)
                # The control closes the menu itself; only press Escape when
                # the menu is somehow still open, or Escape would re-open it.
                if page.evaluate(
                        "() => { const m = document.getElementById('menu');"
                        " return !!(m && !m.hidden); }"):
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(300)
                st = page.evaluate(DESCENT_JS)
                log(outfh, f"NEW_DESCENT_DOC[{i}]", json.dumps(st["descent_doc"]))
            else:
                page.keyboard.press("Escape")
                page.wait_for_timeout(200)

        entry = page.evaluate("() => (window.VEFR_DESCENT_DEF || {}).entry || null")
        log(outfh, "ENTRY_DEF", json.dumps(entry))
        authored = {"town", "cottage", "tavern", "king-room"}
        where = page.evaluate("() => (window.VEFR_COMBAT || {}).region")
        # A pressed New-descent control drops the hero straight into floor 1
        # of the fresh run, so the town entry tile is only the way in when
        # the run was started from the town door.
        if where and where not in authored and not where.startswith("floor-"):
            log(outfh, "ENTRY_SKIPPED already inside the generated descent", where)
        else:
            try:
                bot.ensure_region("town")
                bot.navigate_to("town", entry["at"][0], entry["at"][1])
                st = bot.state()
                log(outfh, "AT_ENTRY", st["combat"]["region"],
                    st["combat"]["hero"]["at"])
                bot.interact()
                page.wait_for_timeout(1200)
                st = page.evaluate(DESCENT_JS)
                log(outfh, "AFTER_ENTRY_REGION", st["region"], st["combat_text"][:200])
                log(outfh, "AFTER_ENTRY_REGIONS", st["regions"])
                log(outfh, "AFTER_ENTRY_TRANSITIONS", json.dumps(
                    [{k: v for k, v in t.items()
                      if k in ("from", "at", "to", "to_at", "requires")}
                     for t in st["transitions"]]))
                if shots:
                    page.wait_for_timeout(600)
                    page.screenshot(path=str(
                        shots / f"{args.tag}-entry-{args.viewport}.png"))
            except COT.RouteError as err:
                log(outfh, "ENTRY_FAILED", repr(err))
                if shots:
                    page.screenshot(path=str(
                        shots / f"{args.tag}-entryfail-{args.viewport}.png"))
                browser.close()
                outfh.close()
                return 1

        deaths = 0
        for depth in range(args.floors):
            # The bot caches the region table once; a generated floor is
            # added to window.VEFR_REGIONS only when the hero arrives, so
            # the cache is dropped before every floor's routing.
            bot._regions = None
            bot._transitions = None
            st = bot.state()
            region = st["combat"]["region"]
            r = page.evaluate(REGION_JS, region)
            if not r:
                log(outfh, f"FLOOR depth={depth} region={region} NO_REGION_DATA")
                break
            walkable = sum(row.count(".") for row in r["map"])
            foes = st["combat"]["enemies"]
            log(outfh, f"FLOOR depth={depth} region={region} size={r['w']}x{r['h']} "
                       f"walkable={walkable} legend={sorted(r['legend'])} "
                       f"enemies={len(foes)} "
                       f"foe_ids={sorted({e['id'] for e in foes})[:8]} "
                       f"foe_hp={sorted({e['hp'] for e in foes})} "
                       f"foe_atk={sorted({e['atk'] for e in foes})} "
                       f"floor_items={len(st['combat']['floor'])} "
                       f"bag={st['combat']['bag']} "
                       f"hp={st['combat']['hero']['hp']}/{st['combat']['hero']['max']}")
            down = up = None
            for y, row in enumerate(r["map"]):
                for x, c in enumerate(row):
                    if c == "d" and down is None:
                        down = (x, y)
                    if c == "u" and up is None:
                        up = (x, y)
            log(outfh, f"STAIRS depth={depth} region={region} up={up} down={down}")
            if shots:
                page.wait_for_timeout(700)
                page.screenshot(
                    path=str(shots / f"{args.tag}-f{depth}-{region}-{args.viewport}.png"))
            if down is None:
                log(outfh, f"NO_DOWN_STAIR depth={depth} region={region}")
                break

            # Play the floor the way a person would: fight what is on it,
            # then take the stair. A hero that wakes in town mid-floor is
            # the game saying the floor beat her, so count it.
            if not args.no_fight:
                try:
                    bot.clear_floor(region, "no-such-foe")
                except COT.RouteError as err:
                    log(outfh, f"CLEAR_STOPPED depth={depth} region={region} {err!r}")
                now = bot.state()
                log(outfh, f"AFTER_FIGHT depth={depth} region={now['combat']['region']} "
                           f"hp={now['combat']['hero']['hp']}/{now['combat']['hero']['max']} "
                           f"bag={now['combat']['bag']} "
                           f"floor_items={len(now['combat']['floor'])} "
                           f"text={now['combat_text'][:120]!r}")
                if now["combat"]["region"] != region:
                    deaths += 1
                    log(outfh, f"DIED_ON depth={depth} region={region} "
                               f"woke_in={now['combat']['region']} "
                               f"at={now['combat']['hero']['at']}")
                    if shots:
                        page.wait_for_timeout(500)
                        page.screenshot(path=str(
                            shots / f"{args.tag}-death-f{depth}-{args.viewport}.png"))
                    break

            try:
                pre = bot.state()
                log(outfh, f"WALK_TO_DOWN depth={depth} region={region} "
                           f"hero={pre['combat']['hero']['at']} target={down}")
                if args.sneak:
                    how = walk_safely(page, bot, region, down)
                    log(outfh, f"SNEAK_TO_DOWN depth={depth} region={region} "
                               f"result={how}")
                    if how != "arrived":
                        log(outfh, f"DESCEND_FAILED depth={depth} region={region} "
                                   f"could not reach the stair ({how})")
                        break
                else:
                    bot.navigate_to(region, down[0], down[1])
                at_down = bot.state()
                log(outfh, f"AT_DOWN depth={depth} region={region} "
                           f"hero={at_down['combat']['hero']['at']} "
                           f"text={at_down['combat_text'][:120]!r}")
                bot.interact()
                page.wait_for_timeout(1400)
                nxt = bot.state()
                log(outfh, f"DESCENDED depth={depth} from={region} at={down} "
                           f"to={nxt['combat']['region']} "
                           f"text={nxt['combat_text'][:160]!r}")
                if nxt["combat"]["region"] == region:
                    log(outfh, f"STAIR_DID_NOT_TAKE depth={depth} region={region}")
            except COT.RouteError as err:
                log(outfh, f"DESCEND_FAILED depth={depth} region={region} {err!r}")
                break
        log(outfh, "DEATHS_TOTAL", deaths)

        trace = page.evaluate("() => window.__trace || []")
        for t in trace:
            log(outfh, "REGION_CHANGE", json.dumps(t))
        final = page.evaluate(DESCENT_JS)
        log(outfh, "FINAL", json.dumps({k: final[k]
                                        for k in ("region", "descent_line")}))
        log(outfh, "ERRORS", json.dumps(errors[:20]))
        browser.close()
    outfh.close()
    try:
        os.unlink(html_path)
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())