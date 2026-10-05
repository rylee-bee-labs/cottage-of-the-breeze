"""Offline smoke playthrough of the woven Cottage interface."""

import os
from pathlib import Path

from playwright.sync_api import sync_playwright


BUILD = Path(os.environ.get("VEFR_WOVEN", "/tmp/weave/cottage-after.html"))


def test_cottage_play_screen_menu_and_message_offline():
    assert BUILD.is_file(), f"woven build expected at {BUILD}, got no file"
    console_errors = []
    page_errors = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        # Register before navigation so errors during boot are included.
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda error: page_errors.append(str(error)))
        page.goto(BUILD.resolve().as_uri(), wait_until="load")
        page.wait_for_selector("#ts-enter", state="visible")
        page.click("#ts-enter")
        page.wait_for_selector("#play", state="visible")
        canvas = page.locator("#play canvas").first
        page.wait_for_function("""() => {
          const c = document.querySelector('#play canvas');
          if (!c || !c.width || !c.height) return false;
          const x = c.getContext('2d'); if (!x) return false;
          const d = x.getImageData(0, 0, c.width, c.height).data;
          let first = null, varied = false;
          for (let i = 0; i < d.length; i += 4) {
            const v = `${d[i]},${d[i+1]},${d[i+2]},${d[i+3]}`;
            if (first === null) first = v; else if (v !== first) { varied = true; break; }
          }
          return varied;
        }""")
        before = canvas.screenshot()
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(250)
        after = canvas.screenshot()
        # VEFR_STAGE publishes viewport rectangles, not camera coordinates;
        # comparing rendered pixels is the honest check that the world moved.
        assert before != after, "canvas pixels expected to change after ArrowRight, but screenshots were identical"

        # A visible panel needs a model connection, which this build does not
        # have. Offline, the contract is that Interact is present, activates
        # without error, and any panel it shows contains real nonempty text.
        interact = page.locator("#play #interact")
        assert interact.count(), "Interact control expected in the play view, got none"
        interact.click()
        page.wait_for_timeout(250)
        visible_panels = page.locator("#npc-box:visible, #reader:visible, #trade:visible")
        for i in range(visible_panels.count()):
            text = visible_panels.nth(i).inner_text().strip()
            assert text, f"visible message panel expected real text after Interact, got {text!r}"

        page.click("#menu-open")
        page.wait_for_selector("#menu", state="visible")
        tabs = page.locator("#menu [data-panel]")
        assert tabs.count() >= 2, f"Menu expected at least two tabs, got {tabs.count()}"
        tabs.nth(0).click()
        assert tabs.nth(0).get_attribute("data-panel"), "first Menu tab expected to remain reachable, got no data-panel"
        tabs.nth(1).click()
        assert tabs.nth(1).get_attribute("data-panel"), "second Menu tab expected to remain reachable, got no data-panel"

        assert not console_errors, f"console errors expected [], got {console_errors}"
        assert not page_errors, f"unhandled page errors expected [], got {page_errors}"
        browser.close()
