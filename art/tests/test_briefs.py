#!/usr/bin/env python3
"""Tests for every brief in art/briefs/.

Pure text checks: no network, no Pillow, no image files. Each brief must say
what it is for (the reader can find the sections), its size, the pictures it
wants, the references to pass (each one an image file that exists on disk), the
round 7 ordering lesson, and at least one batched codex_batch.sh command. The
batch count is checked so a one-picture call cannot slip in: Codex bills per
tool call, so briefs always ask for 2 to 4 pictures at once.

A short sanity test pins the folder to the twelve briefs we know; the other
tests loop over whatever the folder actually holds, so a new brief is covered
the moment it lands.
"""
import re
import unittest
from pathlib import Path

ART_DIR = Path(__file__).resolve().parents[1]          # the art/ folder
BRIEF_DIR = ART_DIR / "briefs"
REPO_ROOT = ART_DIR.parent                              # the parent of art/

# The sanity list: exactly these briefs live in art/briefs/. Add a name here
# when a brief arrives, drop one when a brief goes, or this test fails.
EXPECTED_BRIEFS = (
    "cellar-cast.md",
    "characters.md",
    "gaps.md",
    "guardians.md",
    "hero-walk.md",
    "items-containers.md",
    "monsters-and-boss.md",
    "monsters.md",
    "props-and-furniture.md",
    "rug.md",
    "spellbook-and-inventory.md",
    "town-surfaces.md",
)

# What the other tests loop over: whatever is in the folder right now.
BRIEFS = tuple(sorted(p.name for p in BRIEF_DIR.glob("*.md")))

# The round 7 lesson, word for word. Briefs wrap it across lines, so compare
# against whitespace-normalised text rather than raw lines.
ORDERING_LESSON = ("The pictures in a batch come back in any order; "
                   "identify each by looking, then rename.")

# Backticked paths that look like pictures, e.g. `art/source/round2/wall_v1.webp`.
IMAGE_REF = re.compile(r"`([^`\s]+\.(?:webp|png|jpg|jpeg))`")

# A section runs from its "## Heading" to the next "## " heading (or the end).
def section(text, heading):
    pattern = r"^##\s+" + re.escape(heading) + r"\b(.*?)(?=^##\s|\Z)"
    match = re.search(pattern, text, re.M | re.S)
    return match.group(1) if match else None


def read(name):
    return (BRIEF_DIR / name).read_text(encoding="utf-8")


def normalised(text):
    """Whitespace collapsed, so a sentence split over two lines still matches."""
    return " ".join(text.split())


# Line shape: codex_batch.sh OUTDIR NAME COUNT "BRIEF" [REFS...]
BATCH_COUNT = re.compile(r'codex_batch\.sh\s+\S+\s+\S+\s+(\d+)\s+"')

SH_FENCE = re.compile(r"```sh\b(.*?)```", re.S)


def fenced_lines(text):
    """Every line inside a ```sh fence."""
    for block in SH_FENCE.findall(text):
        for line in block.splitlines():
            yield line


def batch_lines(text):
    """Every fenced line that calls codex_batch.sh."""
    for line in fenced_lines(text):
        if "codex_batch.sh" in line:
            yield line


class BriefTests(unittest.TestCase):
    maxDiff = None

    def test_folder_holds_exactly_the_expected_briefs(self):
        # The one place a hand list is allowed: it catches a forgotten brief.
        found = tuple(sorted(p.name for p in BRIEF_DIR.glob("*.md")))
        self.assertEqual(
            found, tuple(sorted(EXPECTED_BRIEFS)),
            "art/briefs/ does not hold exactly the expected twelve briefs; "
            "update EXPECTED_BRIEFS if a brief was added or removed")

    def test_each_brief_exists(self):
        for name in BRIEFS:
            with self.subTest(brief=name):
                self.assertTrue((BRIEF_DIR / name).is_file(),
                                "missing brief file: %s" % name)

    def test_each_brief_names_a_size(self):
        for name in BRIEFS:
            with self.subTest(brief=name):
                text = read(name)
                size = section(text, "Size")
                self.assertIsNotNone(size, "%s: no ## Size section" % name)
                self.assertTrue(re.search(r"\d", size),
                                "%s: Size section has no number" % name)
                self.assertIn("px", size, "%s: Size section has no px" % name)

    def test_each_brief_lists_its_pictures(self):
        for name in BRIEFS:
            with self.subTest(brief=name):
                text = read(name)
                wanted = section(text, "Pictures wanted")
                self.assertIsNotNone(wanted,
                                     "%s: no ## Pictures wanted section" % name)
                bullets = [ln for ln in wanted.splitlines()
                           if ln.strip().startswith("- ")]
                self.assertTrue(bullets,
                                "%s: ## Pictures wanted has no bullets" % name)

    def test_each_brief_has_a_codex_batch_command(self):
        for name in BRIEFS:
            with self.subTest(brief=name):
                self.assertTrue(list(batch_lines(read(name))),
                                "%s: no codex_batch.sh command" % name)

    def test_each_brief_names_who_made_the_pictures(self):
        # The stale "training: not cleared" line is gone (AGENTS.md: art we
        # generate is distributable with attribution). What still matters is
        # that a brief says whose work it is: Rylee's pick, and the tool that
        # draws it (Codex, or Claude).
        for name in BRIEFS:
            with self.subTest(brief=name):
                text = read(name)
                self.assertIn("Rylee", text,
                              "%s: does not name Rylee" % name)
                self.assertTrue(
                    "Claude" in text or "Codex" in text,
                    "%s: names neither Claude nor Codex" % name)

    def test_each_brief_says_status_draft(self):
        for name in BRIEFS:
            with self.subTest(brief=name):
                self.assertIn("status: draft", read(name),
                              "%s: missing 'status: draft'" % name)

    def test_every_batch_count_is_between_two_and_four(self):
        for name in BRIEFS:
            for line in batch_lines(read(name)):
                with self.subTest(brief=name, command=line.strip()[:80]):
                    match = BATCH_COUNT.search(line)
                    self.assertIsNotNone(
                        match, "%s: no COUNT argument in: %s" % (name, line))
                    count = int(match.group(1))
                    self.assertGreaterEqual(
                        count, 2, "%s: a batch asks for %d picture(s); use 2 to 4"
                        % (name, count))
                    self.assertLessEqual(
                        count, 4, "%s: a batch asks for %d pictures; use 2 to 4"
                        % (name, count))

    def test_every_brief_tells_the_round_7_ordering_lesson(self):
        for name in BRIEFS:
            with self.subTest(brief=name):
                # assertTrue, not assertIn: a missing lesson should name the
                # brief, not dump its whole text into the failure.
                self.assertTrue(
                    ORDERING_LESSON in normalised(read(name)),
                    "%s: missing the round 7 lesson: %s" % (name, ORDERING_LESSON))

    def test_each_brief_references_images_that_exist(self):
        # Only the ## References section: the after-steps name output files
        # that do not exist yet, and they are not references.
        for name in BRIEFS:
            with self.subTest(brief=name):
                refs = section(read(name), "References")
                self.assertIsNotNone(refs, "%s: no ## References section" % name)
                paths = IMAGE_REF.findall(refs)
                self.assertTrue(paths, "%s: ## References names no image file"
                                % name)
                for path in paths:
                    self.assertTrue(
                        (REPO_ROOT / path).is_file(),
                        "%s: reference image does not exist: %s" % (name, path))


if __name__ == "__main__":
    unittest.main()
