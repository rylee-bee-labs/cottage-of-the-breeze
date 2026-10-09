#!/usr/bin/env python3
"""The negative control: prove the playthrough bot can go red.

A harness that has only ever gone green proves nothing.  This breaks the
route on purpose, twice, in two different ways, runs the real bot against
each, and fails unless each run really did come back red *and* failed for
the reason it was broken.

1. **Two ways out of the entry tile.**  A copy of the pack with the
   authored `town [1,1] -> floor-1` transition put back - the exact thing
   cottage#110 deleted and the exact thing that broke this bot before.
   The bot's "one way down" check has to catch it.
2. **The route names a door that is not there.**  The same pack with
   `--entry-at attic,1,1`; nothing in the pack has an `attic`, so the
   descent has no route to it at all.  The route has to fail to find the
   way down.

Run it from a VEFR checkout so the venv has Playwright::

    uv run --offline --group test python \\
        <this-repo>/tests/playthrough/negative_control.py

Writes `negative_control.md` beside this file with the observed output.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_PACK = HERE.resolve().parents[1] / "worlds" / "cottage-of-the-breeze"
sys.path.insert(0, str(HERE))

import run as bot  # noqa: E402


def pack_with_a_second_door(pack: Path, dest: Path) -> str:
    """A copy of the pack with the authored cellar door back on [1,1]."""
    shutil.copytree(pack, dest)
    act = dest / "acts" / "act-1" / "world.json"
    doc = json.loads(act.read_text(encoding="utf-8"))
    doc["transitions"].insert(
        0,
        {"from": "town", "at": [1, 1], "to": "floor-1", "to_at": [3, 3]},
    )
    act.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    return f"authored transition re-added: town [1,1] -> floor-1"


def red_checks(report: dict) -> list:
    return [c["name"] for c in report["checks"] if not c["ok"]]


def run_bot(pack: Path, report_path: Path, extra: list) -> dict:
    args = bot.parse_args(
        ["--pack", str(pack), "--report", str(report_path), "--timeout", "900"] + extra
    )
    return bot.run(args)


def main(argv=None) -> int:
    pack = Path(argv[0]).resolve() if argv else DEFAULT_PACK
    if not pack.is_dir():
        raise SystemExit(f"pack not found: {pack}")
    log: list[str] = ["# Negative control for `tests/playthrough/run.py`", ""]
    failures: list[str] = []

    with tempfile.TemporaryDirectory(prefix="cottage-negative-") as tmp:
        # ---- control 1: two ways out of the entry tile ----------------
        broken = Path(tmp) / "two-doors"
        what = pack_with_a_second_door(pack, broken)
        report = run_bot(broken, Path(tmp) / "two-doors.json", [])
        reds = red_checks(report)
        log += [
            "## 1. the entry tile has two ways out",
            "",
            f"Broken on purpose: {what}.",
            "",
            f"- result: `ok: {report['ok']}` ({report['steps']} steps)",
            f"- checks that went red: {reds}",
            "",
        ]
        if report["ok"]:
            failures.append("control 1 went green")
        elif not any("one way down" in n for n in reds):
            failures.append(f"control 1 went red, but not on the one-way-down check: {reds}")

        # ---- control 2: the route names a door that is not there ------
        report = run_bot(pack, Path(tmp) / "wrong-entry.json", ["--entry-at", "attic,1,1"])
        reds = red_checks(report)
        detail = next(
            (c["detail"] for c in report["checks"] if c["name"] == "the whole route completed"),
            "",
        )
        log += [
            "## 2. the route is pointed at a room that does not exist",
            "",
            "Broken on purpose: `--entry-at attic,1,1`. Nothing in the pack "
            "has an `attic`, so the descent has no route to it at all.",
            "",
            f"- result: `ok: {report['ok']}` ({report['steps']} steps)",
            f"- `the whole route completed`: {detail!r}",
            f"- checks that went red: {reds}",
            "",
        ]
        if report["ok"]:
            failures.append("control 2 went green")
        elif "no open route" not in detail:
            failures.append(f"control 2 went red for the wrong reason: {detail!r}")

    log += [
        "## Verdict",
        "",
        "The bot can fail." if not failures else "FAILED: " + "; ".join(failures),
        "",
    ]
    (HERE / "negative_control.md").write_text("\n".join(log), encoding="utf-8")
    print("\n".join(log))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))