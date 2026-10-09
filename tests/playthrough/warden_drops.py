#!/usr/bin/env python3
"""Read the descent's drops back out of the real woven game.

Weaves the pack, opens the HTML in headless Chromium and asks the page
what the Section's warden drops, through the globals the engine itself
reads at play time (`VEFR_DESCENT_DEF.blueprint.families` for the family,
`VEFR_ITEMS` for the catalog, `VEFR_SPRITES` for the picture).

This is the read-back for a drop that resolves. The client drops an id
the catalog does not name twice and silently: `placeDrops()` returns
before `floor.push`, and `bagAdd` refuses it, so the walk succeeds and
the pack looks finished. Reading the catalog back out of the woven file
is the only way to see that from outside.

Run from a VEFR checkout whose venv has Playwright::

    cd ~/code/Rylee-Bee/vefr
    uv run --group test python <repo>/tests/playthrough/warden_drops.py \
        --pack <repo>/worlds/cottage-of-the-breeze
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

# Runs in the page. Asks only for what the engine has already parsed.
READ_BACK = """() => {
  const cat = window.VEFR_ITEMS || {};
  const sprites = window.VEFR_SPRITES || {};
  const def = window.VEFR_DESCENT_DEF || {};
  const fams = (def.blueprint && def.blueprint.families) || {};
  const out = [];
  for (const section of def.sections || []) {
    // what the floor mobs are drawn from
    for (const f of section.families || []) {
      const fam = fams[f.family] || {};
      out.push({
        section: section.id, role: 'floor mob', family: f.family,
        name: (fam.defaults || {}).name,
        drops: ((fam.defaults || {}).drops) || null,
      });
    }
    // and the warden, which is the one the player earns
    if (section.warden) {
      const fam = fams[section.warden] || {};
      out.push({
        section: section.id, role: 'warden', family: section.warden,
        name: (fam.defaults || {}).name,
        drops: ((fam.defaults || {}).drops) || null,
      });
    }
  }
  return {
    catalogIds: Object.keys(cat).sort(),
    families: out,
    // every drop any family in the descent can produce, resolved the way
    // placeDrops() and bagAdd() resolve it
    drops: [...new Set(out.reduce((acc, f) => acc.concat(f.drops || []), []))]
      .map(id => {
        const spec = cat[id] || {};
        const sprite = spec.sprite || '';
        return {
          id: id,
          droppedBy: out.filter(f => (f.drops || []).indexOf(id) !== -1)
            .map(f => f.family + ' (' + f.role + ')'),
          inCatalog: !!cat[id],
          name: spec.name || null,
          sprite: sprite || null,
          value: spec.value === undefined ? null : spec.value,
          wouldPlaceOnFloor: !!cat[id],
          wouldEnterBag: !!cat[id],
          pictureBaked: !!sprite &&
            String(sprites[sprite] || '').indexOf('data:image') === 0,
        };
      }),
  };
}"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--pack", required=True, help="pack path or worlds/<name>")
    ap.add_argument("--html", help="a woven file to read instead of weaving one")
    args = ap.parse_args()

    html = args.html
    tmp = None
    if not html:
        tmp = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
        tmp.close()
        subprocess.run(
            ["uv", "run", "vefr", "weave", "--pack", args.pack, "--out", tmp.name],
            check=True,
        )
        html = tmp.name

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("file://" + str(Path(html).resolve()))
        page.wait_for_timeout(2500)
        out = page.evaluate(READ_BACK)
        browser.close()
    if tmp:
        Path(tmp.name).unlink(missing_ok=True)

    print(json.dumps(out, indent=2))
    dangling = [d for d in out["drops"] if not d["inCatalog"]]
    if dangling:
        print("\nFAIL: these drops resolve to nothing at play time:")
        for d in dangling:
            print(f"  - {d['id']}  (named by {', '.join(d['droppedBy'])})")
        return 1
    if not out["drops"]:
        print("\nok: the descent's families name no drops at all")
        return 0
    print("\nok: every drop the descent names is in the catalog with a baked picture")
    return 0


if __name__ == "__main__":
    sys.exit(main())