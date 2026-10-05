#!/usr/bin/env python3
"""Capture the old and new woven Cottage UI at desktop and phone sizes."""

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


SIZES = ((1440, 900), (390, 844))


def ready(page):
    page.goto(page._capture_uri, wait_until="load")
    if page.locator("#ts-enter").count():
        page.locator("#ts-enter").click()
    # The offline woven file starts without network or a model connection;
    # #play is the live play view, so waiting for it avoids empty screenshots.
    page.wait_for_selector("#play", state="visible")
    page.wait_for_function("() => !!window.VEFR_STAGE")


def capture(browser, source: Path, out: Path, label: str, width: int, height: int):
    page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
    page._capture_uri = source.resolve().as_uri()
    ready(page)
    out.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(out / f"{label}-play-{width}.png"), full_page=True)

    page.locator("#menu-open").click()
    page.wait_for_selector("#menu", state="visible")
    tabs = page.locator("#menu [data-panel]")
    if tabs.count() < 2:
        raise AssertionError(f"Menu expected at least two tabs, got {tabs.count()} in {source}")
    tabs.nth(0).click()
    page.screenshot(path=str(out / f"{label}-menu-{width}.png"), full_page=True)
    tabs.nth(1).click()
    page.screenshot(path=str(out / f"{label}-menu-tab2-{width}.png"), full_page=True)
    page.keyboard.press("Escape")

    # Use the same real offline interaction exposed on the starting screen;
    # save a speech/message frame only when its panel contains actual text.
    page.locator("#play #interact").click()
    visible_text = page.locator("#npc-box:not([hidden]), #reader:not([hidden]), #trade:not([hidden])")
    page.wait_for_timeout(250)
    if visible_text.count() and visible_text.first.inner_text().strip():
        page.screenshot(path=str(out / f"{label}-message-{width}.png"), full_page=True)
    else:
        # Offline speech may require the model service in some builds.
        # Capture is optional for this surface; the play/menu evidence remains.
        print(f"{label} {width}: no offline message panel with speech was reachable")
    page.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", required=True, type=Path)
    parser.add_argument("--after", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    for src in (args.before, args.after):
        if not src.is_file():
            raise FileNotFoundError(f"woven build expected at {src}, got no file")
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for label, source in (("before", args.before), ("after", args.after)):
            for width, height in SIZES:
                capture(browser, source, args.out, label, width, height)
        browser.close()


if __name__ == "__main__":
    main()
