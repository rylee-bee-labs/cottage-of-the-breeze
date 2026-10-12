#!/usr/bin/env python3
"""Keyboard-only playthrough bot for Cottage of the Breeze.

Plays the real woven game in a real browser, from the cottage to the end
card and back to town, reading state only from the page globals
(``window.VEFR_COMBAT`` and friends) and pressing keys.  Writes
``report.json`` next to this file.  See README.md.

The route is read out of the pack the game bakes, never hardcoded: the
descent's entry tile comes from ``world.json`` -> ``descent.entry``, the
floors come from each Section's own ``floors`` and ``pattern``, and the
books come from ``VEFR_LIBRARY``.  A pack that moves a floor, a landing
or a book is walked correctly by this bot without being edited here.

Run it from a VEFR checkout so the venv has Playwright::

    uv run --offline --group test python <this-repo>/tests/playthrough/run.py \
        --pack <this-repo>/worlds/cottage-of-the-breeze --viewport desktop
"""

from __future__ import annotations

import argparse
import base64
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

# The nine seams of play the engine records a sound cue at, named in
# `web/player/parts/120-sound.js`.  Seven of the nine have a subject on
# this route and are required below.
# The other two are not, and are NOT quietly forgotten: `cues_without_a_
# subject()` asserts from the game's own tables why each of them cannot
# fire, so a pack that grows one back turns that check red instead of
# leaving the cue untested and unnoticed.
#   `locked` - fires only when a door refuses for want of something the
#     hero has not got.  No transition in this pack names a `requires`;
#     the three locked cellar stairs went with the authored floors
#     (cottage#110).
#   `pickup` - fires for an item lying on the floor underfoot.  The
#     families the Sections draw name `drops`, and the combat probe walks
#     onto what they leave behind, so the cue is checked in closing_checks.
#   `level`  - fires when `growAward` pays a level, which is paid in the
#     monster's `xp`, and a generated monster is built without one.
SOUND_CUES_NEEDED = (
    "hit",
    "defeat",
    "door",
    "sticker",
    "end",
)
SOUND_CUES_WITHOUT_A_SUBJECT = ("locked", "level")

# The engine's own fallback for a Section that names no `floors`
# (`vefr.sections.floors`), so a pack that leaves it out is walked as
# deep as the engine will draw rather than one floor deep.
DEFAULT_SECTION_FLOORS = 9

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
    def __init__(self, page, *, max_steps: int, wall_seconds: float, delay_ms: float,
                 entry_at=None):
        self.page = page
        self.max_steps = max_steps
        self.wall_seconds = wall_seconds
        self.delay_ms = delay_ms
        self.entry_at = entry_at
        self.steps = 0
        self.checks: list[dict] = []
        self.console_errors: list[str] = []
        self.request_failures: list[str] = []
        self._start = time.time()
        self._stuck = 0
        self._last_sig = None
        self._regions = None
        self._transitions = None
        self._people_block = None
        self._speakers = None
        self._maps_region = None
        self._families = None
        # What the descent saved about where the hero actually walked,
        # snapshotted as each floor is played: the engine drops those
        # records the moment the Section it hashed stops matching, so
        # they cannot be read back at the end of the run.
        self.footprints: list[dict] = []

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
        self._note_cues()
        self._shot()

    def _note_cues(self) -> None:
        """Remember every sound cue and every hero walk frame the page reports (the log keeps only 50)."""
        try:
            got = self.page.evaluate(
                "() => ({cues: (window.VEFR_SOUND && window.VEFR_SOUND.played) || [],"
                " frame: window.VEFR_HERO_FRAME || null})"
            )
        except Exception:
            return
        cues = getattr(self, "cues", set())
        cues.update(got["cues"])
        self.cues = cues
        if got["frame"]:
            frames = getattr(self, "frames", set())
            frames.add((got["frame"]["dir"], got["frame"]["state"], got["frame"]["frame"]))
            self.frames = frames

    def shot(self, name: str) -> None:
        d = os.environ.get("COTTAGE_SHOTS")
        if not d:
            return
        try:
            self.page.wait_for_timeout(400)
            Path(d).mkdir(parents=True, exist_ok=True)
            self.page.screenshot(path=str(Path(d) / f"{name}.png"))
        except Exception:
            pass

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
    # no progress (a wall bump, a refused lock). 50 in a row is a stall.
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

    # ---- what the pack baked ---------------------------------------
    def regions(self) -> dict:
        if self._regions is None:
            self._sync_maps(None)
        return self._regions or {}

    def transitions(self) -> list:
        if self._transitions is None:
            self._sync_maps(None)
        return self._transitions or []

    def _sync_maps(self, here) -> None:
        """Re-read the page's region and transition tables when the hero moves.

        A generated floor is grown at the moment its stair is used - the
        engine wires the floor's stairs and puts its map in `VEFR_REGIONS`
        only on arrival (`397-the-descent.js` `ensureRegion`/`wireFloor`) -
        so the tables read at page load do not contain it, and a bot that
        cached them can never route to a floor below the one it stands on.
        Re-reading on every lookup would cost an evaluate per tile of
        every BFS, so the tables are refreshed when the hero's region
        changes and not otherwise.
        """
        if self._regions is not None and here == self._maps_region:
            return
        self._regions = self.page.evaluate("window.VEFR_REGIONS") or {}
        self._transitions = self.page.evaluate("window.VEFR_TRANSITIONS") or []
        self._maps_region = here

    def descent(self) -> dict:
        return self.page.evaluate("window.VEFR_DESCENT_DEF") or {}

    def library(self) -> list:
        return self.page.evaluate("window.VEFR_LIBRARY") or []

    def album_def(self) -> list:
        return self.page.evaluate("window.VEFR_ALBUM_DEF") or []

    def found_books(self) -> set:
        return set(
            self.page.evaluate(
                "() => { const w = (window.VEFR_WORLD || {}).name || 'world';"
                " try { return JSON.parse(localStorage.getItem('vefr-library-' + w)"
                " || '[]'); } catch (e) { return []; } }"
            )
            or []
        )

    def saved_floors(self) -> dict:
        return self.page.evaluate(
            "() => { try { return (window.VEFR_DESCENT || {}).loadDoc() || {}; }"
            " catch (e) { return {}; } }"
        ).get("floors", {}) or {}

    def sections(self) -> list:
        return list(self.descent().get("sections") or [])

    def section_floors(self, section: dict) -> int:
        """How many floors a Section has - the engine's own default when
        it names none (`vefr.sections.floors`)."""
        value = section.get("floors")
        if isinstance(value, int) and not isinstance(value, bool) and value > 0:
            return value
        return DEFAULT_SECTION_FLOORS

    @staticmethod
    def floor_name(section: dict, k: int, cycle: int = 0) -> str:
        """The name the engine gives floor `k` (`397-the-descent.js` `floorName`)."""
        return f"{section.get('id')}-{cycle}-{k}"

    @staticmethod
    def floor_kind(section: dict, k: int) -> str:
        """What floor `k` is FOR, read off the Section's own `pattern`."""
        pattern = section.get("pattern")
        if isinstance(pattern, list) and 1 <= k <= len(pattern):
            return str(pattern[k - 1])
        return "n"

    def books_in(self, region: str) -> list:
        """Every book the pack places in `region`, in map order."""
        found = [
            b
            for b in self.library()
            if b.get("region") == region and isinstance(b.get("at"), list) and len(b["at"]) == 2
        ]
        return sorted(found, key=lambda b: (b["at"][0], b["at"][1]))

    def descent_entry(self) -> dict:
        """The tile the pack says the descent starts from.

        `--entry-at` overrides it. That flag exists for the negative
        control in `tests/playthrough/negative_control.md`: it points the
        bot at a tile that is not the way down so the route has to go red.
        """
        entry = dict(self.descent().get("entry") or {})
        region, at = entry.get("region"), entry.get("at")
        if self.entry_at:
            region = self.entry_at[0] or region
            at = self.entry_at[1]
        if not isinstance(region, str) or not region:
            raise RouteError("the pack bakes no descent entry region")
        if not isinstance(at, list) or len(at) != 2:
            raise RouteError(f"the descent entry tile of {region} is not a tile: {at!r}")
        return {"region": region, "at": [int(at[0]), int(at[1])]}

    # ---- maps and transitions -------------------------------------
    def _solid(self, region: str, x: int, y: int) -> bool:
        r = self.regions().get(region)
        if r is None:
            raise RouteError(
                f"{region} is not in the page's region table; the hero cannot "
                f"be walked there"
            )
        rows = r["map"]
        sym = rows[y][x]
        if (r["legend"].get(sym) or {}).get("solid"):
            return True
        return (x, y) in self._prop_cells(region) or (x, y) in self._people_cells(region)

    def _prop_cells(self, region: str) -> set:
        """Every tile a prop's footprint blocks in `region`.

        The same reading as the player's `readProps` (`455-the-props.js`):
        a prop covers `size` tiles from `at`, and its `block` rows say
        which of them are solid ('#'); a prop with no `block` is solid
        all over. A map row cannot show this, so a BFS over the rows
        alone walks the hero into the side of a house.
        """
        cells: set = set()
        for p in (self.regions().get(region) or {}).get("props") or []:
            if not isinstance(p, dict) or not isinstance(p.get("at"), list):
                continue
            w, h = (p.get("size") or [1, 1])[:2]
            ax, ay = int(p["at"][0]), int(p["at"][1])
            block = p.get("block") if isinstance(p.get("block"), list) else None
            for dy in range(int(h)):
                for dx in range(int(w)):
                    row = (block[dy] if dy < len(block) else "") if block else None
                    if row is None or row[dx:dx + 1] == "#":
                        cells.add((ax + dx, ay + dy))
        return cells

    def _people_cells(self, region: str) -> set:
        """The tiles residents stand on, when the pack makes people solid.

        `player.people_block` turns a resident's tile into a wall the hero
        faces instead of entering (`480-town-input-and-turns.js` `move`).
        """
        if self._people_block is None:
            self._people_block = bool(self.page.evaluate(
                "() => ((window.VEFR_WORLD || {}).player || {}).people_block === true"
            ))
        if not self._people_block:
            return set()
        if self._speakers is None:
            self._speakers = self.page.evaluate("() => window.VEFR_SPEAKERS || {}") or {}
        out = set()
        for spec in (self._speakers.get(region) or {}).values():
            at = (spec or {}).get("at")
            if isinstance(at, list) and len(at) == 2:
                out.add((int(at[0]), int(at[1])))
        return out

    def _open(self, region: str, x: int, y: int) -> bool:
        """Inside the map and not solid: a tile the hero can stand on."""
        rows = self.regions()[region]["map"]
        return 0 <= y < len(rows) and 0 <= x < len(rows[0]) and not self._solid(region, x, y)

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
            self._sync_maps(c["region"])
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
        for _ in range(200):
            s = self.state()
            c = s["combat"]
            if c is None:
                raise RouteError("window.VEFR_COMBAT is missing")
            here = c["region"]
            self._sync_maps(here)
            if here == region:
                return
            if self.handle_overlay(s):
                continue
            path = self.region_path(here, region)
            if not path:
                # The tables are re-read once before this is called a
                # dead end: a floor wires its own stairs on arrival, and a
                # route computed a moment before that has to be allowed to
                # see them.  A second empty answer is the truth.
                self._sync_maps(None)
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

    def strike_until_dead(self, region: str, enemy_id: str) -> None:
        """Walk into a monster until it falls, the way a player fights."""
        for _ in range(600):
            s = self.state()
            c = s["combat"]
            self._sync_maps(c["region"])
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
        raise RouteError(
            f"{enemy_id} would not die (hero {c['hero']}, foe {foe}, bag {c['bag']}, "
            f"near {[e for e in c['enemies'] if e['alive'] and abs(e['at'][0]-c['hero']['at'][0])<=4 and abs(e['at'][1]-c['hero']['at'][1])<=4]})"
        )

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

    # ---- books -----------------------------------------------------
    def open_book(self, region: str, book: dict) -> dict:
        """Walk a book tile and read it, keys only.

        A `map` book is found by standing on it - the hero steps on the
        tile and the game records it - so Interact on one that is already
        found does nothing at all.  A `chest` book opens its chest, and
        the reader that comes up has to be paged to the end and closed:
        a chest book is recorded the moment its chest opens, so the found
        list cannot be the loop's stopping condition - the reader going
        down can, because that is what fires `reads`.
        """
        at = book["at"]
        self.navigate_to(region, at[0], at[1])
        for _ in range(400):
            s = self.state()
            if s["reader"]:
                self.interact()  # next page, then the close
                continue
            if book["id"] in self.found_books():
                break
            if self.handle_overlay(s):
                continue
            self.interact()
            self.wait(40)
        self.wait(120)  # let a chest's drops land in the bag
        s = self.state()
        found = self.found_books()
        self.check(
            f"{book.get('id')} can be found and read on {region}",
            book["id"] in found,
            f"region={region} at={at} found={sorted(found)}",
        )
        return s["combat"]

    def ending_book(self) -> str:
        """Which book ends the act - the pack's own rules say, not a guess.

        `complete-act` fires from a rule whose `when` is a `reads`; that
        book is the ending, and the descent walk leaves it alone so that
        the ending is played once, by `read_the_vault`.
        """
        for rule in self.page.evaluate("() => window.VEFR_RULES || []") or []:
            if not any("complete-act" in t for t in (rule.get("then") or [])):
                continue
            what = ((rule.get("when") or {}).get("reads") or {}).get("what")
            if what:
                return str(what)
        raise RouteError("no rule in the pack completes the act")

    def talk_to_nearby(self, region: str, at, who: str) -> bool:
        """Stand where a speaker is and press the Talk control.

        `comes-near` - the seam behind "the cat noticed you" and the
        Keeper's line about the letter - fires from `tryNPC`, which only
        the `#talk` control and a canvas click run: Interact's own
        resident branch goes straight to `talkToSpeaker` and never fires
        the rule.  So the bot walks up, Tabs to the button and presses
        it, which is what a keyboard player does.

        Returns whether the button was reachable, so a caller can say
        which speaker it could not talk to.

        A pack with `player.people_block` keeps the hero off a resident's
        tile, so the walk stops on an open tile beside them instead: the
        Talk reach is two tiles and every `comes-near` rule here reads one.
        """
        x, y = int(at[0]), int(at[1])
        if (x, y) in self._people_cells(region):
            self.ensure_region(region)
            here = tuple(self.state()["combat"]["hero"]["at"])
            beside = [
                (x + dx, y + dy)
                for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))
                if self._open(region, x + dx, y + dy)
            ]
            if not beside:
                raise RouteError(f"no open tile beside {who} at {list(at)} in {region}")
            if here in beside:
                x, y = here
            else:
                x, y = beside[0]
        self.navigate_to(region, x, y)
        reached = self._focus_button("#talk")
        if reached:
            self.press("Enter")
        else:
            self.press("Escape")
        for _ in range(20):
            s = self.state()
            if s["reader"] or s["npc"]:
                self.interact()
                continue
            break
        return reached

    def tile_beside(self, region: str, who: str) -> tuple:
        """An open tile next to the monster or warden `who`, so the walk stops short of it."""
        self.ensure_region(region)
        foe = next((e for e in self.state()["combat"]["enemies"] if e["id"] == who), None)
        if foe is None:
            raise RouteError(f"{who} is not on {region}")
        x, y = foe["at"]
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if not self._solid(region, x + dx, y + dy):
                return (x + dx, y + dy)
        raise RouteError(f"no open tile beside {who} at {foe['at']} in {region}")

    # ---- the route -------------------------------------------------
    def cues_without_a_subject(self) -> None:
        """The sound cues this pack cannot fire, and why, asserted not assumed.

        The old route hardcoded three locked cellar stairs and their
        Keybearers; those floors are gone, so there is nothing to walk to
        and nothing to fight.  Rather than delete the coverage quietly,
        this asks the game's own tables whether a subject has come back -
        so a pack that brings a locked door turns this check red and says
        which cue now needs a route.
        """
        locked = [t for t in self.transitions() if t.get("requires")]
        self.check(
            "no door in the game is locked, so the 'locked' cue has no subject",
            not locked,
            f"locked transitions={locked or 'none'}",
        )

    def family_drop_names(self) -> list:
        """Every family the Sections draw, resolved, that names a `drops`."""
        block = self.descent()
        base = (block.get("blueprint") or {}).get("families") or {}
        out = []
        for section in block.get("sections") or []:
            for entry in section.get("families") or []:
                entry = entry if isinstance(entry, dict) else {"family": entry}
                name = entry.get("family")
                if not isinstance(name, str) or not name:
                    continue
                root = name
                record, seen = {}, set()
                # `extends` is the Blueprint's own inheritance; a drops
                # two steps up a chain is still a drops.
                while isinstance(name, str) and name not in seen:
                    seen.add(name)
                    one = base.get(name) or {}
                    record = {**record, **(one.get("defaults") or {}), **entry}
                    name = one.get("extends")
                if record.get("drops") and root not in out:
                    out.append(root)
        return out

    def explore_home(self) -> None:
        """The cozy half: the cat on the rug, the cloth book, the town's own notes."""
        start = self.state()["combat"]["region"]
        speakers = self.page.evaluate("() => (window.VEFR_SPEAKERS || {}).cottage || {}") or {}
        unreached = []
        for who, spec in sorted(speakers.items()):
            at = (spec or {}).get("at")
            if isinstance(at, list) and len(at) == 2:
                if not self.talk_to_nearby(start, at, who):
                    unreached.append(who)
        self.check(
            "every speaker in the cottage can be talked to with the keyboard",
            not unreached,
            f"unreachable by keyboard={unreached or 'none'} "
            f"(speakers: {sorted(speakers)})",
        )
        for book in self.books_in(start):
            self.open_book(start, book)
        self.ensure_region("town")
        s = self.state()
        self.check(
            "started in the cottage and reached the town",
            s["combat"]["region"] == "town",
            f"from={start} region={s['combat']['region']}",
        )
        for book in self.books_in("town"):
            self.open_book("town", book)

    def step_into_the_descent(self, entry: dict, first_floor: str) -> None:
        """Stand on the entry tile and go down; the tile has one way out."""
        region, at = entry["region"], entry["at"]
        self.ensure_region(region)
        self.navigate_to(region, at[0], at[1])
        outs = [
            t
            for t in self.transitions()
            if t["from"] == region and list(t["at"]) == at
        ]
        self.check(
            f"{region} {at} is one way down, and it goes to {first_floor}",
            len(outs) == 1 and outs[0]["to"] == first_floor,
            f"{len(outs)} exits from the entry tile: "
            f"{[(t['at'], t['to']) for t in outs]}",
        )
        self.interact()
        s = self.state()
        self.check(
            "the door the pack names walks the hero into the descent",
            s["combat"]["region"] == first_floor,
            f"region={s['combat']['region']} text={s['combat_text'][:90]!r}",
        )

    def act_sections(self) -> list:
        """The Sections the act runs through: up to the one whose last floor holds its ending."""
        ending = self.ending_book()
        sections = self.sections()
        for k, section in enumerate(sections):
            last = self.floor_name(section, self.section_floors(section))
            # by region alone: a book placed on a generated floor (place: near-up, a vault) has no fixed tile
            if any(b.get("id") == ending and b.get("region") == last for b in self.library()):
                return sections[: k + 1]
        raise RouteError(f"the act ends on {ending!r}, which is on no Section's last floor")

    def descend_every_floor(self, sections: list) -> list:
        """Walk down every floor of the given Sections, opening what is on the way.

        Returns the names walked.  The footprint of the last floor of each
        Section is taken in `read_the_vault`, which is what walks to it.
        """
        ending = self.ending_book()
        walked: list[str] = []
        for section in sections:
            floors = self.section_floors(section)
            for k in range(1, floors + 1):
                region = self.floor_name(section, k)
                self.ensure_region(region)
                for book in self.books_in(region):
                    # The book that ends the act is left for
                    # `read_the_vault`: reading it here would put the end
                    # card up nine floors early and close it again.
                    if book["id"] != ending:
                        self.open_book(region, book)
                walked.append(region)
                if k < floors:
                    hop = self.down_hop(region, k, section)
                    self.navigate_to(region, hop["at"][0], hop["at"][1])
                    # Read the floor's explored map *after* the walk, not
                    # before: the stair is only in it once the hero has
                    # stood on it.
                    self.footprints.append(self.footprint(region, hop["at"]))
                    self.interact()
                    below = self.floor_name(section, k + 1)
                    if self.state()["combat"]["region"] != below:
                        raise RouteError(
                            f"the stair at {region} {hop['at']} did not go down to {below}"
                        )
        # The bot's own list, cross-checked against the order the descent saved
        # for itself: two independent records of the same walk, so a
        # floor the bot thinks it reached but the engine did not is red.
        order = self.page.evaluate(
            "() => ((window.VEFR_DESCENT || {}).loadDoc() || {}).order || []"
        )
        self.check(
            "every floor of the act's "
            f"{len(sections)} Section{'s' if len(sections) != 1 else ''} was walked: "
            + ", ".join(f"{s['id']}×{self.section_floors(s)}" for s in sections),
            bool(walked)
            and len(walked) == len(set(walked))
            and sorted(walked) == sorted(order),
            f"the bot walked {walked}; the descent's own record of the run is {order}",
        )
        return walked

    def check_footprints(self) -> None:
        """Every floor's far end is inside the explored map the descent saved."""
        self.check(
            "each floor was walked, not only stood on (the far end of it is "
            "inside the fog the descent saved)",
            bool(self.footprints) and all(f["reached"] for f in self.footprints),
            "; ".join(
                f"{f['region']}: {f['what']} {f['tile']} "
                f"{'seen' if f['reached'] else 'NOT seen'}"
                for f in self.footprints
            ),
        )

    def down_hop(self, region: str, k: int, section: dict) -> dict:
        """The stair from floor `k` to the floor below it."""
        below = self.floor_name(section, k + 1)
        for t in self.transitions():
            if t["from"] == region and t["to"] == below:
                return t
        raise RouteError(f"{region} has no stair down to {below}")

    def footprint(self, region: str, tile) -> dict:
        """Has the hero's own record of this floor kept `tile`?

        The engine saves a bitset of every tile the hero has laid eyes on
        (`VEFR_DESCENT` `saveFog`).  Asking whether the stair - or the
        vault - is inside it is the engine's own answer to "was this floor
        walked", and it is the question vefr's own
        `tests/test_descent_bot.py` asks of its three floors.
        """
        record = self.saved_floors().get(region) or {}
        fog = record.get("fog") or ""
        width = self.page.evaluate(
            "(n) => { const p = window.VEFR_DESCENT.floorPlan("
            "window.VEFR_DESCENT.depthOfName(n)); return p ? p.w : 0; }",
            region,
        )
        return {
            "region": region,
            "what": "stair",
            "tile": list(tile) if tile else None,
            "reached": _fog_says(fog, width, tile),
        }

    def read_the_vault(self, last: dict) -> None:
        """Open the last floor's chest and read whatever is in it to the end.

        Act 1's ending is the note the vault holds.  The note lived in
        `king-room`, which went with the authored floors, and was
        re-homed to the Section's `warden` floor - the chest a hero walks
        nine floors down to reach.  The end card is the same card; only
        the door to it moved.
        """
        region = self.floor_name(last, self.section_floors(last))
        ending = self.ending_book()
        book = next((b for b in self.books_in(region) if b["id"] == ending), None)
        if book is None:
            raise RouteError(
                f"the act ends on {ending!r}, which is not on the last floor "
                f"({region}) of the last Section"
            )
        # The King yields when his tally (forty-winters, by the up stair) is read, which the walk down
        # already did; a yielded warden is no longer a foe, so he is looked for, never required.
        foes = [e["id"] for e in self.state()["combat"]["enemies"]]
        if "cellar-king" in foes:
            self.navigate_to(region, *self.tile_beside(region, "cellar-king"))
        bag = self.state()["combat"]["bag"]
        self.check(
            "the Cellar King yields: his wax seal is in the bag",
            "crown-seal" in bag,
            f"bag has crown-seal={'crown-seal' in bag}; foes on {region}={foes}",
        )
        before = bag
        self.navigate_to(region, book["at"][0], book["at"][1])
        self.footprints.append(
            dict(self.footprint(region, book["at"]), what="vault")
        )
        # The Section's own pattern says where its end is.  If a pack
        # moves the ending off the `warden` floor, that is a story
        # decision, not a harness one - but the bot should notice and
        # say so rather than quietly walk to the deepest floor.
        kind = self.floor_kind(last, self.section_floors(last))
        self.check(
            f"the act ends on the Section's `warden` floor ({region} is `{kind}`)",
            kind == "warden",
            f"{region} is `{kind}` under the pattern "
            f"{last.get('pattern')}; the ending book {ending!r} is here",
        )
        self.interact()
        # Page the note out.  The card is the only thing that stops this
        # loop: the reader closing is not enough, because the `reads`
        # rule that fires `complete-act` lands a beat later, and a vault
        # that ended the act silently has to fail here rather than pass.
        for _ in range(400):
            s = self.state()
            if s["act_end"]:
                break
            if s["reader"]:
                self.interact()
                continue
            self.wait(40)
        else:
            raise RouteError(f"reading {book.get('id')} never showed the end card")
        self.wait(120)  # let openActEnd's focus settle
        s = self.state()
        complete = s["act_complete"] or {}
        focused = self.page.evaluate(
            "document.activeElement ? document.activeElement.id : ''"
        )
        self.check(
            "the vault's note ends the act: the end card shows once, role=dialog, "
            "focus on Keep exploring",
            bool(
                s["act_end"]
                and complete.get("shown") is True
                and self.page.get_attribute("#act-end", "role") == "dialog"
                and focused == "act-end-keep"
            ),
            f"book={book.get('id')} region={region} visible={s['act_end']} "
            f"complete={complete} focus={focused!r}",
        )
        after = self.state()["combat"]["bag"]
        drops = book.get("drops") or []
        self.check(
            f"the vault chest drops {drops or 'nothing'} into the bag",
            all(d in after for d in drops),
            f"before={before} after={after} drops={drops}",
        )
        # Close it with Interact; it must not come back.
        self.interact()
        self.wait(300)
        after2 = self.state()
        self.check(
            "the end card stays closed after Interact",
            (not after2["act_end"]) and (after2["act_complete"] or {}).get("shown") is False,
            f"visible={after2['act_end']} complete={after2['act_complete']}",
        )

    def go_home(self) -> None:
        self.ensure_region("town")
        self.check(
            "the route ends back in the town",
            self.state()["combat"]["region"] == "town",
            f"region={self.state()['combat']['region']}",
        )

    def check_the_town_after_the_cellar(self) -> None:
        """Once act 1 is complete the town loads its after-the-cellar state.

        Every state is in `VEFR_REGIONS` from page load, so finding its
        text there proves nothing. Instead the pack's own `town_states`
        name the state the flags now choose, the bot finds a place whose
        `poi_text` that state changes, walks up to it and reads it with
        Interact, the way a player does. Nothing about the door is
        written here: change the state's words and this follows them.
        """
        flags = self.page.evaluate("() => (window.VEFR_RULES_STATE || {}).flags || {}") or {}
        blocks = self.page.evaluate("() => window.VEFR_TOWN_STATES || null")
        blocks = blocks if isinstance(blocks, list) else [blocks] if blocks else []
        regions = self.regions()
        base, use = None, None
        for block in blocks:
            if not isinstance(block, dict) or not block.get("region"):
                continue
            for one in block.get("states") or []:
                if flags.get((one or {}).get("when")) is True and one.get("use") in regions:
                    base, use = block["region"], one["use"]
        changed = {}
        if use:
            before = regions[base].get("poi_text") or {}
            changed = {
                k: v for k, v in sorted((regions[use].get("poi_text") or {}).items())
                if before.get(k) != v
            }
        read = ""
        if changed:
            key, want = next(iter(changed.items()))
            x, y = (int(n) for n in key.split(","))
            self.ensure_region(base)
            if self._open(base, x, y):
                self.navigate_to(base, x, y)
            else:
                beside = [
                    (x + dx, y + dy, (-dx, -dy))
                    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))
                    if self._open(base, x + dx, y + dy)
                ]
                if not beside:
                    raise RouteError(f"no open tile beside {base} {key} to read it from")
                bx, by, face = beside[0]
                self.navigate_to(base, bx, by)
                self.press_dir(face)   # a bump turns the hero to face it
            self.interact()
            read = self.page.evaluate(
                "() => { const b = document.getElementById('npc-box');"
                " return b && !b.hidden ? document.getElementById('npc-line').textContent : ''; }"
            ) or ""
            self.handle_overlay(self.state())
        self.check(
            "the town after the cellar is loaded: act 1 is complete and a place it changes reads its new words",
            flags.get("act-1-complete") is True and bool(changed) and read == next(iter(changed.values()), None),
            f"act-1-complete={flags.get('act-1-complete')} state={use!r} "
            f"changed={sorted(changed)} read={read[:70]!r}",
        )

    def survives_a_reload(self) -> None:
        """Reload at the end: the card does not return and the global is gone."""
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

    def start_over_asks_first(self) -> None:
        """Start over asks first; Cancel clears nothing."""
        before = self.saves()
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
        after = self.saves()
        self.check(
            "'Start over' asks first, Cancel leaves every save untouched",
            asks and after == before,
            f"confirmVisible/focusOk={asks} saves_unchanged={after == before}",
        )
        self.press("Escape")  # close the menu
        self.wait(60)

    def saves(self) -> dict:
        return self.page.evaluate(
            "() => Object.fromEntries(Object.keys(localStorage)"
            ".filter(k => k.startsWith('vefr-'))"
            ".map(k => [k, localStorage.getItem(k)]))"
        )

    def no_sideways_scroll(self) -> None:
        """The page must not scroll sideways."""
        s = self.state()
        self.check(
            f"no horizontal page scroll at {s['inner_w']}px",
            s["scroll_w"] <= s["inner_w"],
            f"scrollWidth={s['scroll_w']} innerWidth={s['inner_w']}",
        )

    # ---- the monsters ----------------------------------------------
    def set_monsters(self, quiet: bool) -> None:
        """Give the descent's floors monsters, or take them away.

        `tests/test_descent_bot.py` in vefr empties a Section's families
        so that the walk a test performs is the walk the generator drew
        and not a detour around a fight, because the fight is proved
        elsewhere.  This bot proves it elsewhere too, and in view:
        `combat_probe()` at the end of the run puts the families back and
        fights.  The lever is the engine's own documented harness hook -
        `397-the-descent.js` reads `VEFR_DESCENT_DEF` at call time "and a
        harness may plant its own" - so the pack on disk is untouched and
        `vefr check` still passes on it.  A Section with no families draws
        no monsters at all: `mobsAt` stops at the first index.
        """
        if self._families is None:
            self._families = self.page.evaluate(
                "() => ((window.VEFR_DESCENT_DEF || {}).sections || [])"
                ".map(s => s.families || [])"
            )
        families = [[] for _ in self._families] if quiet else self._families
        self.page.evaluate(
            "(families) => { const d = window.VEFR_DESCENT_DEF;"
            " if (!d || !d.sections) return;"
            " d.sections.forEach((s, i) => { s.families = families[i]; }); }",
            families,
        )

    def combat_probe(self, entry: dict) -> None:
        """Fight on a real descent floor, so the combat evidence survives.

        The route itself walks floors with the monsters taken away, which
        is what makes it a route test rather than a fight test.  This puts
        them back, walks down the first floor again and kills what is on
        it - the checks the walk-and-fight loop of Rylee's 2026-10-01 note
        ("the wander around and fight things loop feels VERY castle of
        the winds to me") was covered by before the descent existed.
        """
        self.page.reload()
        self.wait(300)
        self.page.click("#ts-enter")
        self.wait(300)
        self.set_monsters(False)
        region, at = entry["region"], entry["at"]
        self.ensure_region(region)
        self.navigate_to(region, at[0], at[1])
        self.interact()
        floor = self.state()["combat"]["region"]
        self.check(
            "the descent's floors carry monsters again once the harness puts "
            "the Section's families back",
            bool(self.state()["combat"]["enemies"]),
            f"floor={floor} enemies={len(self.state()['combat']['enemies'])}",
        )
        killed = 0
        # Three is enough to prove the loop and little enough that a
        # 6-HP hero survives it on the deepest-first order the engine
        # hands enemies out in.
        for _ in range(3):
            c = self.state()["combat"]
            if c["region"] != floor:
                self.ensure_region(floor)
                continue
            foes = [e for e in c["enemies"] if e["alive"]]
            if not foes:
                break
            at_hero = tuple(c["hero"]["at"])
            foes.sort(key=lambda e: abs(e["at"][0] - at_hero[0]) + abs(e["at"][1] - at_hero[1]))
            self.strike_until_dead(floor, foes[0]["id"])
            killed += 1
            for item in {d["item"] for d in self.state()["combat"]["floor"]}:
                self.pickup(floor, item)
            self.drink()
        heard = getattr(self, "cues", set())
        self.check(
            "a monster on a descent floor can be fought, and the fight is heard",
            killed >= 1 and {"hit", "defeat"} <= heard,
            f"killed={killed} hero={self.state()['combat']['hero']} "
            f"heard={sorted(heard & {'hit', 'defeat', 'hurt', 'level'})}",
        )
        # The third cue with no subject.  `growAward` is paid in `e.xp`
        # (`430-loot-on-the-floor.js:101`), and a generated monster is
        # built by `enemyEntry`, which copies id, name, at, hp, atk,
        # sight and drops - and no xp, even though the Blueprint family
        # behind it carries one.  So a hero grinding the descent cannot
        # level, and `level` cannot fire.  When the engine starts paying
        # it this check goes red and the probe has to fight to a level.
        foes = self.state()["combat"]["enemies"]
        carriers = [e["id"] for e in foes if "xp" in e]
        self.check(
            "a descent monster carries no xp, so the 'level' cue has no subject",
            not carriers,
            f"enemies carrying xp={carriers or 'none'} (killed {killed} of "
            f"{len(foes)})",
        )

    # ---- the route, in order ---------------------------------------
    def run_route(self, *, quiet: bool = True) -> None:
        self.set_monsters(quiet)
        entry = self.descent_entry()
        sections = self.sections()
        if not sections:
            raise RouteError("the pack bakes no descent Section")
        first = self.floor_name(sections[0], 1)

        self.explore_home()
        self.cues_without_a_subject()
        self.step_into_the_descent(entry, first)
        act = self.act_sections()
        self.descend_every_floor(act)
        self.read_the_vault(act[-1])
        self.check_footprints()
        self.go_home()
        self.check_the_town_after_the_cellar()
        self.survives_a_reload()
        self.start_over_asks_first()
        self.combat_probe(entry)
        self.no_sideways_scroll()

    # ---- closing checks -------------------------------------------
    def closing_checks(self) -> None:
        need = set(SOUND_CUES_NEEDED)
        have = getattr(self, "cues", set())
        self.check(
            "the sound cues fired as the route was played",
            need <= have,
            f"heard {sorted(have)}; missing {sorted(need - have)}; not "
            f"required (no subject in this pack: "
            f"{', '.join(SOUND_CUES_WITHOUT_A_SUBJECT)})",
        )
        carriers = self.family_drop_names()
        if carriers:
            self.check(
                "the 'pickup' cue fired: the descent's families drop things "
                f"({', '.join(carriers)})",
                "pickup" in have,
                f"heard {sorted(have)}",
            )
        frames = getattr(self, "frames", set())
        dirs_walked = {d for (d, st, _f) in frames if st == "walk"}
        self.check(
            "the hero's walk frames showed for every direction she walked",
            {"down", "up", "left", "right"} <= dirs_walked,
            f"walked in {sorted(dirs_walked)}; {len(frames)} distinct poses",
        )
        album = self.page.evaluate("() => window.VEFR_ALBUM || null")
        if album is not None:
            # Every sticker the pack defines, not a hand-picked few: the
            # descent left five behind and the route reaches all five.
            need = {str(s["id"]) for s in self.album_def()}
            have = set(album.get("found", []))
            self.check(
                "every album sticker the pack defines was found on this route",
                need <= have,
                f"{len(have)} of {album.get('total')} found; missing {sorted(need - have)}",
            )
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


def _fog_says(fog: str, w: int, tile) -> bool:
    """Whether the engine's saved explored-bitset says the hero saw `tile`."""
    if not w or not fog:
        return False
    try:
        raw = base64.b64decode(fog)
    except Exception:
        return False
    i = tile[1] * int(w) + tile[0]
    return bool(raw[i >> 3] & (1 << (7 - (i & 7))))


def parse_args(argv=None) -> argparse.Namespace:
    here = Path(__file__).resolve().parent
    # tests/playthrough -> tests -> the repo root.
    default_pack = here.resolve().parents[1] / "worlds" / "cottage-of-the-breeze"
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pack", default=str(default_pack),
                    help="path to the world pack (default: this repo's)")
    ap.add_argument("--viewport", choices=sorted(VIEWPORTS), default="desktop")
    ap.add_argument("--max-steps", type=int, default=60000)
    ap.add_argument("--timeout", type=float, default=1200.0, help="wall-clock cap, seconds")
    ap.add_argument("--delay-ms", type=float, default=0.0)
    ap.add_argument("--headed", action="store_true")
    ap.add_argument("--monsters", action="store_true",
                    help="walk the descent with the families in place instead "
                         "of taking them away (slower; the combat probe at the "
                         "end of the run fights either way)")
    ap.add_argument("--entry-at", default=None, metavar="X,Y",
                    help="override the descent entry tile, as REGION,X,Y or "
                         "X,Y in --entry-at's region. The negative control in "
                         "tests/playthrough/negative_control.md uses this to "
                         "point the route at a tile that is not the way down.")
    ap.add_argument("--report", default=str(here / "report.json"))
    args = ap.parse_args(argv)
    if args.entry_at:
        parts = args.entry_at.split(",")
        if len(parts) == 2:
            args.entry_at = (None, [int(parts[0]), int(parts[1])])
        elif len(parts) == 3:
            args.entry_at = (parts[0].strip(), [int(parts[1]), int(parts[2])])
        else:
            ap.error("--entry-at wants X,Y or REGION,X,Y")
    return args


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
            entry_at=args.entry_at,
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
            bot.run_route(quiet=not args.monsters)
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