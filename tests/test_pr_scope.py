#!/usr/bin/env python3
"""The subject of this pull request, written down as a test.

The second review of cottage-of-the-breeze#96 sent it back for one reason
besides the build bug: the change the brief described was not the change the
branch carried. A browser harness, a capture script and twelve before/after
screenshots had ridden along on a branch whose whole subject is the pack's
skin opt-in (fonts, backdrop, and the one lossy save in build_skin.py), and a
VEFR pin bump besides. A reviewer cannot check a description against a diff
they have to guess at, so the subject is pinned here instead: every file this
branch changes has to be one of these, each with the reason it belongs.

Adding a file to the branch means adding it to SCOPE in the same commit, with
its reason. That is the point. If the file is not part of the skin opt-in -
browser checks, capture tooling, screenshots, engine pins that are not about
this pack - it belongs on its own branch, and ui4-proof (from this branch's
head at e84487d) is where the UI4 proof went.

    python3 -m unittest tests.test_pr_scope

Skips itself, rather than failing, in a clone that cannot answer the question:
no git, a shallow clone that has no BASE, or a checkout where this branch has
already been merged and the diff is empty.
"""
import os
import subprocess
import unittest

# The last commit on main before this branch: cottage-of-the-breeze#95, "pin
# ci-harness to ede6c5c and pass the Bazzite runner switch". Override with
# SCOPE_BASE=<sha or ref> to check a branch against a different base.
BASE = os.environ.get("SCOPE_BASE", "9bbde38")

SCOPE = {
    # The pack opts into the two things the engine has supported and the pack
    # never used: a Crimson Pro "fonts" object and a wood "backdrop".
    "worlds/cottage-of-the-breeze/skins/parchment-and-wood/skin.json":
        "the opt-in itself: fonts and backdrop keys",
    "worlds/cottage-of-the-breeze/skins/parchment-and-wood/backdrop-alt-1.webp":
        "the backdrop picture skin.json now names",
    # The backdrop draft and its provenance stay in art/source, as every other
    # piece of art in this repo does.
    "art/source/round18/RECORD.md": "the round 18 record line for the backdrop",
    "art/source/round18/ui-soft/PICKS.md": "the draft sheet naming the two backdrops",
    "art/source/round18/ui-soft/backdrop/backdrop-alt-1.jpg": "the backdrop source",
    "art/source/round18/ui-soft/backdrop/backdrop-alt-1.credits.txt":
        "attribution for the backdrop, which travels with the art",
    "art/source/round18/ui-soft/backdrop/backdrop-alt.json":
        "the brief the backdrop was drawn from",
    # The one lossy save in the tool, and the rebuild guarantee beside it.
    "art/tools/build_skin.py": "lossy WebP for the backdrop; no stale manifest",
    "art/tests/test_build_skin.py": "the cases that pin both of the above",
    "art/tests/test_skin_contract.py": "the contract cases for the two new keys",
    # The pin: this pack's skin is only readable on an engine that keeps the
    # contrast-aware panel fallback (vefr #306, then #316), and CI validates
    # the pack against the engine it will be played on.
    ".github/workflows/validate-pack.yml": "VEFR_REF moved to 61490b0 (vefr #316)",
    # The record of where the UI4 proof went.
    "docs/plans/native-ui/PLAN.md": "says the UI4 checks and captures live elsewhere",
    "tests/test_pr_scope.py": "this file",
}

# Where the UI4 proof went, spelled out so it cannot creep back in by accident.
PROOF_ONLY = ("docs/screenshots/ui4/", "scripts/capture_ui4.py", "tests/browser/")


REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def git(*args):
    """One git call, or None when git cannot answer (no git, shallow clone)."""
    try:
        done = subprocess.run(("git",) + args, cwd=REPO, capture_output=True,
                              text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    if done.returncode != 0:
        return None
    return done.stdout


class PullRequestScopeTest(unittest.TestCase):
    """Every file on this branch is a file this pull request is about."""

    def changed_files(self):
        """The files this branch changed against BASE, or skip the test."""
        listing = git("diff", "--name-only", f"{BASE}..HEAD")
        if listing is None:
            self.skipTest(f"git cannot diff {BASE}..HEAD here (no git, or a "
                          f"shallow clone with no base commit)")
        files = {line for line in listing.splitlines() if line}
        if not files:
            self.skipTest(f"{BASE}..HEAD is empty: this branch is merged, or "
                          f"already reverted, and there is nothing to police")
        return files

    def test_every_changed_file_is_named_here(self):
        changed = self.changed_files()
        undeclared = sorted(changed - set(SCOPE))
        self.assertEqual(undeclared, [], f"this branch changes files that are "
                                          f"not part of the pack's skin opt-in: "
                                          f"{undeclared}. Add each to SCOPE with "
                                          f"its reason if it belongs, or move it "
                                          f"to its own branch if it does not.")
        unknown = sorted(set(SCOPE) - changed)
        self.assertEqual(unknown, [], f"SCOPE names files this branch does not "
                                      f"change: {unknown}. Drop them from SCOPE, "
                                      f"or bring back what they were keeping honest.")

    def test_the_ui4_proof_is_not_carried_on_this_branch(self):
        """The artifacts the review named, checked by where they live.

        Screenshot sheets, the capture script and the browser harness are
        proof of the interface work; they live on ui4-proof. This one does not
        need a base commit, so it still says something in a shallow clone.
        """
        listing = git("ls-files")
        if listing is None:
            self.skipTest("git cannot list the tracked files here")
        tracked = {line for line in listing.splitlines() if line}
        for path in PROOF_ONLY:
            with self.subTest(path=path):
                carried = sorted(p for p in tracked if p.startswith(path))
                self.assertEqual(carried, [], f"{carried} are UI4 proof, not part "
                                              f"of the pack's skin opt-in; they "
                                              f"belong on ui4-proof")


if __name__ == "__main__":
    unittest.main()