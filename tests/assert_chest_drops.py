"""Assert every `drops` id in the pack names a real item with a real sprite.

Covers every place the pack names an item a mob or a chest can drop:
the Blueprint's families (`defaults.drops`, which is what the generated
descent's mobs and the Section's warden draw on), a Section's own
records, an act region's `enemies[].drops`, and a chest book's `drops`
in its front matter.

Neither validator does this. `_drop_ids` in vefr/cli.py keeps a drop
only when the catalog names it, and `placeDrops` in `web/packaged.html`
does the same again in the client, so a mob that drops an id the catalog
does not name silently drops nothing and the pack validates clean. That
is the defect `crown-seal`, `bell-key`, `lantern-key` and `helmet-key`
were in; this is the check that catches it. It also asserts every
sprite a named item carries is a real entry in `player.sprites` with a
real file in the pack, so an item never ships as a fallback dot.

The filename says "chest" but the check has outgrown it: it is the
pack-wide drop check. Renaming it is left to the coordinator.

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


def check(where, pid):
    """One named id: it must be a catalog item with a real sprite."""
    if pid not in items:
        bad.append(f"{where}: names {pid!r}, not in world.json items")
        return
    sprite = items[pid].get("sprite")
    if not sprite:
        bad.append(f"{where}: item {pid!r} has no sprite")
    elif sprite not in sprites:
        bad.append(f"{where}: item {pid!r} sprite {sprite!r} not in player.sprites")
    elif not (pack / "sprites" / f"{sprite}.png").exists():
        bad.append(f"{where}: item {pid!r} sprite {sprite!r} has no file")


def named_ids(value):
    """A `drops` value is a list (contract/Blueprint) or a comma-separated
    string (book front matter). Both are read here."""
    if isinstance(value, str):
        parts = value.split(",")
    elif isinstance(value, list):
        parts = value
    else:
        return []
    return [str(p).strip() for p in parts if str(p).strip()]


# 1. The Blueprint's families: what the generated descent's mobs drop, and
#    what the Section's warden drops. A family `extends` another and may
#    inherit its drops, so the walk follows `extends`.
blueprint_path = pack / "blueprint.json"
families = {}
if blueprint_path.is_file():
    families = (json.loads(blueprint_path.read_text(encoding="utf-8")) or {}).get("families") or {}


def family_drops(family, seen=None):
    seen = seen or set()
    if family in seen or family not in families:
        return []
    seen.add(family)
    spec = families[family] or {}
    parent = family_drops(spec.get("extends"), seen) if spec.get("extends") else []
    return named_ids((spec.get("defaults") or {}).get("drops")) + parent


for family in sorted(families):
    for pid in family_drops(family):
        check(f"blueprint family {family!r}", pid)

# 2. Sections: every family and the warden must be a family the Blueprint
#    defines. A Section that names a family that is not there draws no
#    such mob and says nothing, exactly like a drop that resolves to no
#    item.
sections = pack / "sections"
section_files = sorted(sections.glob("*.json")) if sections.is_dir() else []
for path in section_files:
    section = json.loads(path.read_text(encoding="utf-8"))
    named = [f.get("family") for f in section.get("families") or [] if f.get("family")]
    if section.get("warden"):
        named.append(section["warden"])
    for family in named:
        if family not in families:
            bad.append(f"sections/{path.name}: names family {family!r}, not in the Blueprint")

# 3. Act regions: a contract enemy's own `drops`.
for contract in sorted(pack.glob("acts/*/*/contract.json")):
    spec = json.loads(contract.read_text(encoding="utf-8"))
    where = f"{contract.parent.name}/contract.json"
    for enemy in spec.get("enemies") or []:
        for pid in named_ids(enemy.get("drops")):
            check(f"{where} enemy {enemy.get('id') or enemy.get('name')!r}", pid)

# 4. Chest books: `drops` in front matter.
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
    names = named_ids(extra.get("drops", ""))
    if not names:
        bad.append(f"{book.name}: chest with no drops")
    for pid in names:
        check(book.name, pid)

print(f"blueprint families checked: {len(families)}")
print(f"sections checked: {len(section_files)}")
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
print("\nok: every drop the pack names resolves to a real item with a real sprite")