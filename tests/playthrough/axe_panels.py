"""Accessibility pass over the surfaces the playthrough bot cannot judge: runs axe-core (vendored in the VEFR
checkout) on the play screen and on each Menu panel and the end card, in the real browser, and fails on any
serious or critical violation.

usage (from the VEFR checkout):
  uv run --group test python <this-repo>/tests/playthrough/axe_panels.py --pack <this-repo>/worlds/cottage-of-the-breeze
"""
import argparse
import json
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright
from vefr.cli import weave_html

AXE = Path(__file__).resolve().parents[3] / "vefr" / "scripts" / "vendor" / "axe.min.js"
RUN = ("() => axe.run(document, { resultTypes: ['violations'] }).then(r => r.violations.map(v => "
       "({ id: v.id, impact: v.impact, nodes: v.nodes.map(n => n.target.join(' ')).slice(0, 3) })))")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    args = ap.parse_args()
    html = weave_html(Path(args.pack).resolve())
    fd = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8")
    fd.write(html); fd.close()
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(Path(fd.name).as_uri())
        page.click("#ts-enter")
        page.wait_for_timeout(800)
        page.add_script_tag(path=str(AXE))

        def audit(name):
            v = page.evaluate(RUN)
            results.append({"surface": name, "violations": v})

        audit("play screen")
        page.click("#menu-open")
        page.wait_for_timeout(200)
        for panel in ("journal", "books", "album", "bag", "display", "help", "startover"):
            btn = page.query_selector(f'#menu [data-panel="{panel}"]')
            if btn:
                btn.click()
                page.wait_for_timeout(200)
                audit(f"menu: {panel}")
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        page.evaluate("() => window.openActEnd && window.openActEnd('act-1')")
        page.wait_for_timeout(200)
        audit("end card")
        browser.close()
    bad = 0
    for r in results:
        serious = [v for v in r["violations"] if v["impact"] in ("serious", "critical")]
        bad += len(serious)
        print(f"{r['surface']}: {len(r['violations'])} violation(s), {len(serious)} serious/critical")
        for v in r["violations"]:
            print("   ", v["impact"], v["id"], v["nodes"])
    print(json.dumps({"serious_or_critical": bad}))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
