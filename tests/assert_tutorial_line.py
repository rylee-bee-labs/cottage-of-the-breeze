"""Assert the tutorial's walking line is Rylee's approved universal wording.

cottage#158: the line names the arrow keys, W A S D and the joystick, so a
phone player and a keyboard player read the same true sentence. The line is
preserved text (NOTES.md, 2026-10-16); change it only with her wording.

usage: python3 tests/assert_tutorial_line.py [REPO_ROOT]
"""
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent)
world = json.loads((root / "worlds" / "cottage-of-the-breeze" / "world.json").read_text(encoding="utf-8"))
rules = [r for r in world.get("rules", []) if r.get("id") == "tutorial-begin"]
if len(rules) != 1:
    sys.exit(f"FAIL: expected one tutorial-begin rule, found {len(rules)}")
says = [t["say"] for t in rules[0].get("then", []) if "say" in t]
want = "Walk with the arrow keys, W A S D, or the joystick."
if not any(s.startswith(want) for s in says):
    sys.exit(f"FAIL: tutorial-begin does not open with {want!r}: {says!r}")
print("ok: tutorial walking line names the arrow keys, W A S D and the joystick")
