#!/usr/bin/env python3
"""Keyboard-only playthrough bot for Cottage of the Breeze.

Plays the real woven game in a real browser, from the cottage to the end
card and back to town, reading state only from the page globals
(``window.VEFR_COMBAT`` and friends) and pressing keys.  Writes
``report.json`` next to this file.  See README.md.

Run it from a VEFR checkout so the venv has Playwright::

    uv run --offline --group test python <this-repo>/tests/playthrough/run.py \
        --pack <this-repo>/worlds/cottage-of-the-breeze --viewport desktop
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import time
from collections import deque
from pathlib import Path

from playwright.sync_api import sync_playwright

VIEWPORTS = {
    "desktop": {"width": 1280, "height": 720},
    "phone": {"width": 390, "height": 844},
}
# Direction -> key.
KEYS = {
    (0, -1): "ArrowUp",
    (0, 1): "ArrowDown",
    (-1, 0): "ArrowLeft",
    (1, 0): "ArrowRight",
}

# One round trip returns everything the bot reads from the page.  State
# comes from the harness globals; the visibility flags are the game's own
# overlays (a book reader, a speech box, a shop, the menu, the end card).
STATE_JS = """() => {
  const vis = (id) => { const e = document.getElementById(id); return !!(e && !e.hidden); };
  const c = window.VEFR_COMBAT || null;
  return {
    combat: c,
    reader: vis('reader'),
    npc: vis('npc-box'),
    trade: vis('trade'),
    menu: vis('menu'),
    act_end: vis('act-end'),
    act_complete: window.VEFR_ACT_COMPLETE || null,
    combat_text: (document.getElementById('combat-live') || {}).textContent || '',
    scroll_w: document.documentElement.scrollWidth,
    inner_w: window.innerWidth,
  };
}"""


class RouteError(RuntimeError):
    """The pack or engine would not let the bot take the route."""


class StallError(RouteError):
    """The hero stopped making progress; something is stuck."""


class Bot:
    def __init__(self, page, *, max_steps: int, wall_seconds: float, delay_ms: float):
        self.page = page
        self.max_steps = max_steps
        self.wall_seconds = wall_seconds
        self.delay_ms = delay_ms
        self.steps = 0
        self.checks: list[dict] = []
        self.console_errors: list[str] = []
        self.request_failures: list[str] = []
        self._start = time.time()
        self._stuck = 0
        self._last_sig = None
        self._regions = None
        self._transitions = None

    # ---- reporting -------------------------------------------------
    def check(self, name: str, ok: bool, detail: str = "") -> None:
        self.checks.append({"name": name, "ok": bool(ok), "detail": detail})

    def report(self, viewport: str) -> dict:
        return {
            "viewport": viewport,
            "steps": self.steps,
            "checks": self.checks,
            "console_errors": self.console_errors,
            "ok": all(c["ok"] for c in self.checks),
        }

    # ---- page event capture ---------------------------------------
    def on_console(self, msg) -> None:
        if msg.type == "error":
            self.console_errors.append(f"console.error: {msg.text}")

    def on_pageerror(self, err) -> None:
        self.console_errors.append(f"pageerror: {err}")

    def on_requestfailed(self, request) -> None:
        self.request_failures.append(f"{request.url} ({request.failure})")

    # ---- page primitives ------------------------------------------
    def wait(self, ms: float) -> None:
        self.page.wait_for_timeout(ms)

    def state(self) -> dict:
        return self.page.evaluate(STATE_JS)

    def press(self, key: str) -> None:
        self.steps += 1
        if self.steps > self.max_steps:
            raise StallError(f"step cap reached ({self.max_steps})")
        if time.time() - self._start > self.wall_seconds:
            raise StallError(f"wall-clock cap reached ({self.wall_seconds:.0f}s)")
        self.page.keyboard.press(key)
        if self.delay_ms:
            self.page.wait_for_timeout(self.delay_ms)
        self._observe_progress()
        self._shot()

    def _shot(self) -> None:
        """With COTTAGE_SHOTS=<dir>, save one screenshot the first time each region is seen (for a human)."""
        d = os.environ.get("COTTAGE_SHOTS")
        if not d:
            return
        seen = getattr(self, "_seen_regions", set())
        try:
            region = self.page.evaluate("() => window.VEFR_COMBAT && window.VEFR_COMBAT.region")
            if region and region not in seen and self.steps > 3:
                seen.add(region)
                self._seen_regions = seen
                self.page.wait_for_timeout(500)
                Path(d).mkdir(parents=True, exist_ok=True)
                self.page.screenshot(path=str(Path(d) / f"{len(seen):02d}-{region}.png"))
        except Exception:
            pass

    def press_dir(self, direction) -> None:
        self.press(KEYS[direction])

    def interact(self) -> None:
        self.press("e")

    # A coarse progress signature: a press that changes none of these made
    # no progress (a wall bump, a refused lock).  50 in a row is a stall.
    def _observe_progress(self) -> None:
        s = self.state()
        c = s["combat"] or {}
        sig = (
            c.get("region"),
            tuple(c.get("hero", {}).get("at", [])),
            tuple(sorted((e["id"], e["hp"], e["alive"]) for e in c.get("enemies", []))),
            tuple(c.get("bag", [])),
            tuple(sorted((tuple(d["at"]), d["item"]) for d in c.get("floor", []))),
            s["reader"], s["npc"], s["trade"], s["menu"], s["act_end"],
            s["combat_text"],
        )
        if sig == self._last_sig:
            self._stuck += 1
        else:
            self._stuck = 0
            self._last_sig = sig
        if self._stuck >= 50:
            raise StallError(
                f"no progress for 50 presses (region {c.get('region')}, "
                f"hero {c.get('hero', {}).get('at')})"
            )

    # ---- overlays --------------------------------------------------
    # A walk that meets a book, a speech box, a shop or the menu handles
    # it with keys and carries on.  The end card is never dismissed here.
    def handle_overlay(self, s: dict) -> bool:
        if s["reader"] or s["npc"]:
            self.interact()
            return True
        if s["trade"] or s["menu"]:
            self.press("Escape")
            return True
        return False

    # ---- maps and transitions -------------------------------------
    def regions(self) -> dict:
        if self._regions is None:
            self._regions = self.page.evaluate("window.VEFR_REGIONS")
        return self._regions

    def transitions(self) -> list:
        if self._transitions is None:
            self._transitions = self.page.evaluate("window.VEFR_TRANSITIONS")
        return self._transitions

    def _solid(self, region: str, x: int, y: int) -> bool:
        r = self.regions()[region]
        rows = r["map"]
        sym = rows[y][x]
        return bool((r["legend"].get(sym) or {}).get("solid"))

    def next_dir(self, region: str, cur, target):
        """BFS over the baked rows; living enemies are walked through."""
        rows = self.regions()[region]["map"]
        h, w = len(rows), len(rows[0])
        start, goal = tuple(cur), tuple(target)
        if start == goal:
            return None
        prev = {start: None}
        q = deque([start])
        while q:
            cx, cy = q.popleft()
            if (cx, cy) == goal:
                break
            for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                nx, ny = cx + dx, cy + dy
                if not (0 <= nx < w and 0 <= ny < h):
                    continue
                if self._solid(region, nx, ny):
                    continue
                if (nx, ny) in prev:
                    continue
                prev[(nx, ny)] = (cx, cy)
                q.append((nx, ny))
        if goal not in prev:
            return None
        node = goal
        while prev[node] != start:
            node = prev[node]
        return (node[0] - start[0], node[1] - start[1])

    def lock_open(self, trans: dict) -> bool:
        req = trans.get("requires")
        if not req:
            return True
        item = req.get("item")
        if item:
            s = self.state()
            if item in ((s["combat"] or {}).get("bag") or []):
                return True
        flag = req.get("flag")
        if flag:
            state = self.page.evaluate(
                "window.VEFR_RULES_STATE ? window.VEFR_RULES_STATE.flags : null"
            )
            if state and state.get(flag) is True:
                return True
        return False

    def region_path(self, src: str, dst: str) -> list:
        """Transitions from src to dst whose locks are open, or []."""
        edges: dict[str, list] = {}
        for t in self.transitions():
            edges.setdefault(t["from"], []).append(t)
        q = deque([src])
        prev = {src: None}
        while q:
            here = q.popleft()
            if here == dst:
                break
            for t in edges.get(here, []):
                if t["to"] in prev or not self.lock_open(t):
                    continue
                prev[t["to"]] = t
                q.append(t["to"])
        if dst not in prev:
            return []
        path = []
        node = dst
        while prev[node] is not None:
            path.append(prev[node])
            node = prev[node]["from"]
        path.reverse()
        return path

    # ---- movement --------------------------------------------------
    def navigate_to(self, region: str, tx: int, ty: int) -> None:
        """Walk to (tx, ty) in `region`, routing back if a death moved us."""
        target = (tx, ty)
        for _ in range(4000):
            s = self.state()
            c = s["combat"]
            if c is None:
                raise RouteError("window.VEFR_COMBAT is missing")
            if c["region"] != region:
                self.ensure_region(region)
                continue
            # Clear any overlay a step just opened (a map book, a speech box)
            # before treating arrival as done: an open reader would eat the
            # Interact that uses the stair.
            if self.handle_overlay(s):
                continue
            at = tuple(c["hero"]["at"])
            if at == target:
                return
            d = self.next_dir(region, at, target)
            if d is None:
                raise RouteError(
                    f"no walkable path in {region} from {at} to {target}"
                )
            self.press_dir(d)
        raise RouteError(f"navigation loop in {region} to {target}")

    def ensure_region(self, region: str) -> None:
        """Take open doors until we are in `region`."""
        for _ in range(40):
            s = self.state()
            c = s["combat"]
            here = c["region"]
            if here == region:
                return
            if self.handle_overlay(s):
                continue
            path = self.region_path(here, region)
            if not path:
                raise RouteError(f"no open route from {here} to {region}")
            hop = path[0]
            self.navigate_to(here, hop["at"][0], hop["at"][1])
            self.interact()
            s2 = self.state()
            if s2["combat"]["region"] == here:
                raise RouteError(
                    f"{here} {hop['at']} -> {hop['to']} did not open: "
                    f"{s2['combat_text'][:90]!r}"
                )
        raise RouteError(f"region routing loop reaching {region}")

    # ---- combat ----------------------------------------------------
    def drink(self, max_drinks: int = 12) -> None:
        """Drink potions from the Bag panel, keyboard only (best effort)."""
        for _ in range(max_drinks):
            s = self.state()
            c = s["combat"]
            if "cloudy-potion" not in c["bag"]:
                return
            if c["hero"]["hp"] >= c["hero"]["max"]:
                return
            self.press("b")
            if not self._focus_button(
                '#bag-list button[data-action="use"][data-item="cloudy-potion"]'
            ):
                self.press("Escape")
                return
            before = c["hero"]["hp"]
            self.press("Enter")
            self.press("Escape")
            after = self.state()["combat"]
            if after["hero"]["hp"] <= before and after["bag"] == c["bag"]:
                return

    def _focus_button(self, selector: str, tries: int = 25) -> bool:
        probe = (
            "() => { const a = document.activeElement;"
            f" return !!(a && a.matches && a.matches({selector!r})); }}"
        )
        for _ in range(tries):
            if self.page.evaluate(probe):
                return True
            self.press("Tab")
        return bool(self.page.evaluate(probe))

    def clear_floor(self, region: str, skip: str) -> None:
        """Fight every other living enemy on the floor first, as a player grinding for levels would.

        The route to a guardian is not a power curve: a hero who walks straight there arrives too weak.
        An enemy that cannot be reached is left alone (a boxed-in one is not a bug in the route)."""
        for _ in range(80):
            c = self.state()["combat"]
            if c["region"] != region:
                self.ensure_region(region)
                continue
            foes = [e for e in c["enemies"] if e["alive"] and e["id"] != skip]
            if not foes:
                return
            at = tuple(c["hero"]["at"])
            foes.sort(key=lambda e: abs(e["at"][0] - at[0]) + abs(e["at"][1] - at[1]))
            for foe in foes:
                try:
                    self.strike_until_dead(region, foe["id"])
                    break
                except RouteError:
                    self.skipped_foes = getattr(self, "skipped_foes", set()) | {foe["id"]}
                    foes = [e for e in foes if e["id"] != foe["id"]]
            else:
                return
        self.drink()

    def strike_until_dead(self, region: str, enemy_id: str) -> None:
        cleared = getattr(self, "_cleared", set())
        if (enemy_id.endswith("-keybearer") or "cellar-king" in enemy_id) and region not in cleared:
            cleared.add(region)
            self._cleared = cleared
            self.clear_floor(region, enemy_id)
        for _ in range(600):
            s = self.state()
            c = s["combat"]
            if c["region"] != region:
                self.ensure_region(region)
                continue
            if self.handle_overlay(s):
                continue
            foe = next((e for e in c["enemies"] if e["id"] == enemy_id), None)
            if foe is None or not foe["alive"]:
                return
            # Heal when hurt and able; otherwise fight on (no potion, no wait).
            if c["hero"]["hp"] * 5 < c["hero"]["max"] * 2 and "cloudy-potion" in c["bag"]:
                self.drink()
                continue
            at = tuple(c["hero"]["at"])
            d = self.next_dir(region, at, tuple(foe["at"]))
            if d is None:
                raise RouteError(f"no path to {enemy_id} at {foe['at']}")
            self.press_dir(d)
        c = self.state()["combat"]
        foe = next((e for e in c["enemies"] if e["id"] == enemy_id), {})
        raise RouteError(f"{enemy_id} would not die (hero {c['hero']}, foe {foe}, bag {c['bag']}, near {[e for e in c['enemies'] if e['alive'] and abs(e['at'][0]-c['hero']['at'][0])<=4 and abs(e['at'][1]-c['hero']['at'][1])<=4]})")

    def pickup(self, region: str, item_id: str) -> None:
        for _ in range(40):
            s = self.state()
            c = s["combat"]
            if c["region"] != region:
                self.ensure_region(region)
                continue
            if item_id in c["bag"]:
                return
            drops = [d for d in c["floor"] if d["item"] == item_id]
            if not drops:
                raise RouteError(f"{item_id} is neither carried nor on {region}'s floor")
            at = drops[0]["at"]
            self.navigate_to(region, at[0], at[1])
            if item_id in self.state()["combat"]["bag"]:
                return
        raise RouteError(f"could not pick up {item_id}")

    # ---- the route -------------------------------------------------
    def _trans(self, frm: str, at) -> dict:
        for t in self.transitions():
            if t["from"] == frm and tuple(t["at"]) == tuple(at):
                return t
        raise RouteError(f"no transition {frm} {at}")

    def attempt_locked(self, region: str, at, key_id: str, label: str) -> None:
        self.navigate_to(region, at[0], at[1])
        bag = self.state()["combat"]["bag"]
        self.check(
            f"{label}: the key is not carried when the lock is tried",
            key_id not in bag,
            f"bag={bag}",
        )
        self.interact()
        s = self.state()
        text = s["combat_text"]
        locked_text = self._trans(region, at).get("locked_text", "")
        ok = s["combat"]["region"] == region and locked_text in text
        self.check(
            f"{label} refuses with the locked text",
            ok,
            f"region={s['combat']['region']} text={text!r}",
        )

    def floor_key_sequence(
        self, region: str, at, key_id: str, next_region: str, label: str
    ) -> None:
        self.attempt_locked(region, at, key_id, label)
        foe = next(
            (e for e in self.state()["combat"]["enemies"] if e["id"].endswith("-keybearer")),
            None,
        )
        if foe is None:
            raise RouteError(f"no Keybearer on {region}")
        self.check(
            f"{key_id}: not carried before its Keybearer dies",
            key_id not in self.state()["combat"]["bag"],
            "fresh key, drop not taken yet",
        )
        self.strike_until_dead(region, foe["id"])
        s = self.state()
        drops = [d for d in s["combat"]["floor"] if d["item"] == key_id]
        self.check(
            f"{key_id}: appears (on the floor or in the bag) once the Keybearer dies",
            bool(drops) or key_id in s["combat"]["bag"],
            f"floor={[d['item'] for d in s['combat']['floor']]} bag={s['combat']['bag']}",
        )
        self.pickup(region, key_id)
        self.check(
            f"{key_id}: carried once picked up",
            key_id in self.state()["combat"]["bag"],
            f"bag={self.state()['combat']['bag']}",
        )
        self.ensure_region(next_region)

    def open_chest_and_read(self, region: str, at) -> None:
        self.navigate_to(region, at[0], at[1])
        self.interact()  # open the chest -> the reader opens
        for _ in range(200):
            s = self.state()
            if s["act_end"]:
                break
            if s["reader"]:
                self.interact()  # next page, then close (which fires `reads`)
            else:
                self.wait(40)
                if not self.state()["act_end"]:
                    raise RouteError("the chest reader closed without the end card")
        self.wait(120)  # let openActEnd's focus settle
        s = self.state()
        complete = s["act_complete"] or {}
        focused = self.page.evaluate(
            "document.activeElement ? document.activeElement.id : ''"
        )
        self.check(
            "the end card shows once, role=dialog, focus on Keep exploring",
            bool(
                s["act_end"]
                and complete.get("shown") is True
                and self.page.get_attribute("#act-end", "role") == "dialog"
                and focused == "act-end-keep"
            ),
            f"visible={s['act_end']} complete={complete} focus={focused!r}",
        )
        # Close it with Interact; it must not come back.
        self.interact()
        self.wait(300)
        after = self.state()
        self.check(
            "the end card stays closed after Interact",
            (not after["act_end"]) and (after["act_complete"] or {}).get("shown") is False,
            f"visible={after['act_end']} complete={after['act_complete']}",
        )

    def run_route(self) -> None:
        # Cottage -> town -> floor-1 -> floor-2 -> floor-3.
        self.ensure_region("town")
        s = self.state()
        self.check(
            "started in the cottage and reached the town",
            s["combat"]["region"] == "town",
            f"region={s['combat']['region']}",
        )
        for region in ("floor-1", "floor-2", "floor-3"):
            self.ensure_region(region)
        self.check(
            "descended to floor 3",
            self.state()["combat"]["region"] == "floor-3",
            f"region={self.state()['combat']['region']}",
        )

        # Floors 3, 4, 5: try the locked stair, beat the Keybearer, take its key.
        self.floor_key_sequence(
            "floor-3", (2, 2), "bell-key", "floor-4", "floor-3's locked stair"
        )
        self.floor_key_sequence(
            "floor-4", (30, 10), "lantern-key", "floor-5", "floor-4's locked stair"
        )
        self.floor_key_sequence(
            "floor-5", (16, 16), "helmet-key", "floor-6", "floor-5's locked stair"
        )

        # Floor 6: the sealed door refuses without the seal, the Cellar King
        # drops it, and then the door opens into the king-room.
        door_at = (11, 1)
        self.attempt_locked(
            "floor-6", door_at, "crown-seal", "floor-6's sealed door"
        )
        king = next(
            (e for e in self.state()["combat"]["enemies"] if e["id"] == "floor-6-cellar-king"),
            None,
        )
        if king is None:
            raise RouteError("no Cellar King on floor-6")
        self.strike_until_dead("floor-6", "floor-6-cellar-king")
        self.pickup("floor-6", "crown-seal")
        self.check(
            "the crown seal is carried",
            "crown-seal" in self.state()["combat"]["bag"],
            f"bag={self.state()['combat']['bag']}",
        )
        self.navigate_to("floor-6", door_at[0], door_at[1])
        self.interact()
        s = self.state()
        self.check(
            "the seal opens the sealed door into the king-room",
            s["combat"]["region"] == "king-room",
            f"region={s['combat']['region']} text={s['combat_text']!r}",
        )

        # King-room: open the chest, read the note to the end, see the card.
        self.open_chest_and_read("king-room", (6, 2))

        # Home again.
        self.ensure_region("town")
        self.check(
            "the route ends back in the town",
            self.state()["combat"]["region"] == "town",
            f"region={self.state()['combat']['region']}",
        )

        # Reload at the end: the card does not return and the global is gone.
        self.page.reload()
        self.wait(300)
        self.page.click("#ts-enter")
        self.wait(300)
        s = self.state()
        absent = self.page.evaluate("typeof window.VEFR_ACT_COMPLETE === 'undefined'")
        self.check(
            "after a reload the end card does not show and VEFR_ACT_COMPLETE is absent",
            (not s["act_end"]) and absent,
            f"visible={s['act_end']} absent={absent}",
        )

        # Start over asks first; Cancel clears nothing.
        before = self.page.evaluate(
            "() => Object.fromEntries(Object.keys(localStorage)"
            ".filter(k => k.startsWith('vefr-'))"
            ".map(k => [k, localStorage.getItem(k)]))"
        )
        self.press("Escape")  # open the menu
        self.press("Shift+Tab")  # menu-close -> the last panel item (Start over)
        self.press("Enter")
        self.wait(80)
        panel = self.state()
        focused = self.page.evaluate(
            "document.activeElement ? document.activeElement.id : ''"
        )
        asks = panel["menu"] and self.page.is_visible("#startover-body") and focused == "startover-cancel"
        self.press("Escape")  # Cancel
        self.wait(80)
        after = self.page.evaluate(
            "() => Object.fromEntries(Object.keys(localStorage)"
            ".filter(k => k.startsWith('vefr-'))"
            ".map(k => [k, localStorage.getItem(k)]))"
        )
        self.check(
            "'Start over' asks first, Cancel leaves every save untouched",
            asks and after == before,
            f"confirmVisible/focusOk={asks} saves_unchanged={after == before}",
        )
        self.press("Escape")  # close the menu
        self.wait(60)

        # Phone: the page must not scroll sideways.
        s = self.state()
        self.check(
            f"no horizontal page scroll at {s['inner_w']}px",
            s["scroll_w"] <= s["inner_w"],
            f"scrollWidth={s['scroll_w']} innerWidth={s['inner_w']}",
        )

    # ---- closing checks -------------------------------------------
    def closing_checks(self) -> None:
        self.check(
            "zero console.error / pageerror events",
            not self.console_errors,
            "; ".join(self.console_errors[:5]) or "none",
        )
        self.check(
            "no failed network requests",
            not self.request_failures,
            "; ".join(self.request_failures[:5]) or "none",
        )


def parse_args(argv=None) -> argparse.Namespace:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pack", required=True, help="path to the world pack")
    ap.add_argument("--viewport", choices=sorted(VIEWPORTS), default="desktop")
    ap.add_argument("--max-steps", type=int, default=20000)
    ap.add_argument("--timeout", type=float, default=600.0, help="wall-clock cap, seconds")
    ap.add_argument("--delay-ms", type=float, default=1.0)
    ap.add_argument("--headed", action="store_true")
    ap.add_argument("--report", default=str(here / "report.json"))
    return ap.parse_args(argv)


def run(args: argparse.Namespace) -> dict:
    from vefr.cli import weave_html  # imported here so --help needs no VEFR

    pack = Path(args.pack).resolve()
    if not pack.is_dir():
        raise SystemExit(f"pack not found: {pack}")
    html = weave_html(pack)

    fd, html_path = tempfile.mkstemp(prefix="cottage-playthrough-", suffix=".html")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(html)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not args.headed)
        context = browser.new_context(viewport=VIEWPORTS[args.viewport])
        page = context.new_page()
        print(f"[bot] chromium {browser.version}", file=sys.stderr)
        bot = Bot(
            page,
            max_steps=args.max_steps,
            wall_seconds=args.timeout,
            delay_ms=args.delay_ms,
        )
        page.on("console", bot.on_console)
        page.on("pageerror", bot.on_pageerror)
        page.on("requestfailed", bot.on_requestfailed)
        page.goto(f"file://{html_path}")
        bot.wait(300)
        bot.check(
            "title screen shows the Begin button",
            page.is_visible("#ts-enter"),
            "found #ts-enter",
        )
        page.click("#ts-enter")
        bot.wait(300)
        try:
            bot.run_route()
            bot.check("the whole route completed", True, f"{bot.steps} steps")
        except RouteError as err:
            bot.check("the whole route completed", False, str(err))
            try:
                page.screenshot(path=str(Path(args.report).with_name("failure.png")))
            except Exception:
                pass
        bot.closing_checks()
        report = bot.report(args.viewport)
        browser.close()

    try:
        os.unlink(html_path)
    except OSError:
        pass
    return report


def main(argv=None) -> int:
    args = parse_args(argv)
    report = run(args)
    Path(args.report).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    pass_n = sum(1 for c in report["checks"] if c["ok"])
    print(
        f"\n{pass_n}/{len(report['checks'])} checks passed, "
        f"{report['steps']} steps, ok={report['ok']}",
        file=sys.stderr,
    )
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
