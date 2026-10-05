"""Stage containment contract for the woven Cottage interface."""

import os
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright


BUILD = Path(os.environ.get("VEFR_WOVEN", "/tmp/weave/cottage-after.html"))
SIZES = (
    (1920, 1080), (1366, 768), (1280, 720), (1024, 600),
    (844, 390), (390, 844), (360, 640),
)
# 844x390 is deliberately excluded: it is landscape at width 844.
PORTRAIT = {(390, 844), (360, 640)}
SELECTORS = (
    "#play .hud .glass", "#play .hud button", "#play .gbtn",
    "#play .toasts p", "#play .toasts-toggle", "#dpad button",
    "#play #interact", "#play .actions button",
)


@pytest.mark.parametrize(("width", "height"), SIZES)
def test_stage_contains_visible_hud_and_controls(width, height):
    assert BUILD.is_file(), f"woven build expected at {BUILD}, got no file"
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(BUILD.resolve().as_uri(), wait_until="load")
        # Woven builds are self-contained/offline: the playable view appears
        # after the title screen's Enter button is clicked; wait for #play so
        # we never measure the empty title document.
        if page.locator("#ts-enter").count():
            page.locator("#ts-enter").click()
        page.wait_for_selector("#play", state="visible")
        page.wait_for_function("() => !!window.VEFR_STAGE")
        result = page.evaluate(
            r"""(selectors) => {
              const stage = window.VEFR_STAGE;
              const box = stage && [stage.x, stage.y, stage.w, stage.h].every(Number.isFinite) ?
                [stage.x, stage.y, stage.x + stage.w, stage.y + stage.h] : null;
              const items = [];
              for (const selector of selectors) for (const el of document.querySelectorAll(selector)) {
                if (el.closest('.sr-only') || el.getClientRects().length === 0) continue;
                const s = getComputedStyle(el);
                if (s.display === 'none' || s.visibility === 'hidden' || Number(s.opacity) === 0) continue;
                const r = el.getBoundingClientRect();
                items.push({selector, text: (el.innerText || el.getAttribute('aria-label') || '').trim(),
                  rect: [r.left, r.top, r.right, r.bottom]});
              }
              const map = stage && stage.map;
              const mr = map && [map.x, map.y, map.w, map.h].every(Number.isFinite) ?
                [map.x, map.y, map.x + map.w, map.y + map.h] : null;
              const controls = items.filter(x => /button|#dpad|#interact|\.gbtn|toasts-toggle/.test(x.selector));
              return {box, items,
                scrollWidth: document.documentElement.scrollWidth, innerWidth,
                map: mr,
                overlaps: mr ? controls.filter(c => c.rect[0] < mr[2] && c.rect[2] > mr[0] &&
                  c.rect[1] < mr[3] && c.rect[3] > mr[1]) : []};
            }""",
            list(SELECTORS),
        )
        assert result["box"], f"window.VEFR_STAGE expected a rectangle from stage.x, stage.y, stage.w, stage.h, got {result['box']}"
        left, top, right, bottom = result["box"]
        for item in result["items"]:
            x1, y1, x2, y2 = item["rect"]
            assert x1 >= left - 1 and y1 >= top - 1 and x2 <= right + 1 and y2 <= bottom + 1, (
                f"{item['selector']} ({item['text']!r}) expected inside stage {result['box']} "
                f"within 1px, got {item['rect']}"
            )
        assert result["scrollWidth"] <= result["innerWidth"], (
            f"document scrollWidth expected <= innerWidth ({result['innerWidth']}), got {result['scrollWidth']}"
        )
        if (width, height) in PORTRAIT:
            assert result["map"], f"portrait window.VEFR_STAGE.map expected a visible letterboxed map, got {result['map']}"
            assert not result["overlaps"], (
                f"portrait controls expected not to overlap the map {result['map']}, got {result['overlaps']}"
            )
        browser.close()
