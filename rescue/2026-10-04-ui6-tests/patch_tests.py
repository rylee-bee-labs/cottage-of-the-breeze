"""Reapply the UI6 interface slice 4/5 tests to a fresh vefr checkout.

The worktree this was written in was deleted from disk after it was committed,
so this script rebuilds it: it copies the two fixture files verbatim and makes
the same surgical edits to the two test files. Every edit is asserted, so a
checkout that has drifted fails loudly instead of half-applying.

    python3 patch_tests.py /path/to/vefr

Then:  bash tests/run.sh tests/test_skin_apply.py tests/test_skin_validator.py
"""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def replace(text, old, new, where, count=1):
    if text.count(old) != count:
        raise SystemExit(
            f"FAIL {where}: expected {count} match(es) of the anchor, found "
            f"{text.count(old)}. The file has drifted; re-apply by hand.")
    return text.replace(old, new)


def patch_apply(text):
    # 1. the module docstring names the two new slices
    text = replace(text, '''and looks exactly as it did.
"""
''', '''and looks exactly as it did.

Interface slices 4 and 5 are here too: the nine parts a skin may carry and the player did not
draw, the five HUD icons, and the speech box's portrait.
"""
''', "test_skin_apply.py docstring")
    # 2. the WCAG maths, reused as it is
    text = replace(text, '''ROOT = Path(__file__).resolve().parents[1]
''', '''ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(Path(__file__).parent))
from test_teal_contrast import contrast  # noqa: E402  (the WCAG maths, used as it is)
''', "test_skin_apply.py teal import")
    # 3. the constants the new section reads
    text = replace(text, '''BACKDROP_FILES = {**mk.FILES, "backdrop.png": (288, 288)}
''', '''BACKDROP_FILES = {**mk.FILES, "backdrop.png": (288, 288)}

# ---- interface slices 4 and 5 ----
# The nine parts a skin may carry and the player does not draw, in the order
# design/ui-skin.md lists them. `mk.PARTS_SKIN` owns the parts, their picture
# keys and their sizes; every picture is its own solid colour, so "this rule
# carries the slot picture" is a string test and not a guess at a shape.
NEW_PARTS = ("slot", "tab", "toggle", "tooltip", "speech",
             "divider", "banner", "corner", "gold-plate")
GUARD = "@media (prefers-contrast: no-preference) and (not (forced-colors: active))"
PLAYER_CSS = (ROOT / "web" / "player" / "parts" / "020-style.css").read_text(encoding="utf-8")
# The five HUD words an icon sits beside, and what each icon is called.
ICONS = ("heart", "star", "coin", "bag", "door")
# Anything the player's own sheet treats as a control. A skin may not set a
# size below the 44 px floor on one of these (the picture can be smaller than
# its hit area, the hit area may not).
CONTROLS = ("button", ".cta", ".gbtn", "input", "select", "textarea",
            "toggle", 'role="button"')
''', "test_skin_apply.py constants")
    # 4. the harness grows a sixth page: the skin that carries every part
    text = replace(text, '''    run = subprocess.run(
        ["node", str(ROOT / "tests/fixtures/skin_apply_harness.mjs"),
         "skinned", str(skinned), "plain", str(plain), "backdrop", str(backdrop),
         "fonts", str(fonts), "crimson", str(crimson)],''', '''    # every part the skin contract names: the four already drawn, plus the nine
    # of interface slice 4.
    parts = home / "parts.html"
    parts.write_text(cli.weave_html(mk.build_parts(home)), encoding="utf-8")
    run = subprocess.run(
        ["node", str(ROOT / "tests/fixtures/skin_apply_harness.mjs"),
         "skinned", str(skinned), "plain", str(plain), "backdrop", str(backdrop),
         "fonts", str(fonts), "crimson", str(crimson), "parts", str(parts)],''',
                  "test_skin_apply.py harness args")
    # 5. the new section, appended
    text = text.rstrip("\n") + (HERE / "blocks/skin_apply_append.py").read_text()
    return text


def patch_validator(text):
    text = replace(text, '''woven file as data URIs (`window.VEFR_SKIN`); a pack with no skin bakes `window.VEFR_SKIN = null;`.
"""

import copy
import json
import re
import sys
from pathlib import Path
''', '''woven file as data URIs (`window.VEFR_SKIN`); a pack with no skin bakes `window.VEFR_SKIN = null;`.

Interface slice 4 also lives here: the nine parts the validator already accepts and the baker
already inlines, and the one thing that is still missing - a part the validator accepts is a
part the player draws.
"""

import copy
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
''', "test_skin_validator.py docstring and imports")
    return text.rstrip("\n") + (HERE / "blocks/skin_validator_append.py").read_text()


def main():
    root = Path(sys.argv[1]).resolve()
    for name in ("skin_apply_harness.mjs", "make_skin_pack.py"):
        shutil.copyfile(HERE / "tests/fixtures" / name, root / "tests/fixtures" / name)
        print("copied tests/fixtures/" + name)
    apply_file = root / "tests/test_skin_apply.py"
    apply_file.write_text(patch_apply(apply_file.read_text(encoding="utf-8")),
                          encoding="utf-8")
    print("patched tests/test_skin_apply.py")
    validator_file = root / "tests/test_skin_validator.py"
    validator_file.write_text(patch_validator(validator_file.read_text(encoding="utf-8")),
                              encoding="utf-8")
    print("patched tests/test_skin_validator.py")
    print("\\nnow: bash tests/run.sh tests/test_skin_apply.py tests/test_skin_validator.py")


if __name__ == "__main__":
    main()
