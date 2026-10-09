"""Assert every id in a chest book's `drops` exists in world.json's items.

The pack validator and `vefr check` do not do this: `_drop_ids` in
vefr/cli.py silently discards an id the catalog does not name, so a
chest can validate clean and open empty. This is the check that catches
it. It also asserts every sprite a named item carries is a real entry in
player.sprites with a real file in the pack.

usage: python3 tests/assert_chest_drops.py [REPO_ROOT]
"""
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent)
pack = root / "worlds" / "cottage-of-the-breeze"
if not pack.is_dir():                      # tolerate being handed the pack itself
    pack = root
world = json.loads((pack / "world.json").read_text(encoding="utf-8"))
items = world.get("items") or {}
sprites = (world.get("player") or {}).get("sprites") or {}

bad = []
seen_chests = 0
for book in sorted((pack / "library").glob("*.md")):
    head = book.read_text(encoding="utf-8").split("---")
    if len(head) < 3:
        continue
    extra = {}
    for line in head[1].splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            extra[k.strip()] = v.strip()
    if str(extra.get("chest", "")).lower() not in ("yes", "true", "1"):
        continue
    seen_chests += 1
    names = [p.strip() for p in str(extra.get("drops", "")).split(",") if p.strip()]
    if not names:
        bad.append(f"{book.name}: chest with no drops")
    for pid in names:
        if pid not in items:
            bad.append(f"{book.name}: drops names {pid!r}, not in world.json items")
            continue
        sprite = items[pid].get("sprite")
        if sprite and sprite not in sprites:
            bad.append(f"{book.name}: item {pid!r} sprite {sprite!r} not in player.sprites")
        elif sprite and not (pack / "sprites" / f"{sprite}.png").exists():
            bad.append(f"{book.name}: item {pid!r} sprite {sprite!r} has no file")

print(f"chest books checked: {seen_chests}")
print("item                        name                          value sprite")
for pid, spec in items.items():
    print(f"{pid:<26} {spec.get('name',''):<28} "
          f"{str(spec.get('value','-')):>5} {spec.get('sprite','-')}")

if bad:
    print("\nFAIL")
    for line in bad:
        print("  -", line)
    raise SystemExit(1)
print("\nok: every chest drop resolves to a real item with a real sprite")