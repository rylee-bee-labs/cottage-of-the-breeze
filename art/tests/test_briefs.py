#!/usr/bin/env python3
"""Tests for the four art briefs in art/briefs/.

Pure text checks: no network, no Pillow, no image files. Each brief must say
what it is for (the reader can find the sections), its size, the pictures it
wants, the references to pass, and at least one batched codex_batch.sh command.
The batch count is checked so a one-picture call cannot slip in: Codex bills per
tool call, so briefs always ask for 2 to 4 pictures at once.
"""
import re
import unittest
from pathlib import Path

BRIEF_DIR = Path(__file__).resolve().parents[1] / "briefs"

BRIEFS = ("rug.md", "monsters.md", "items-containers.md", "hero-walk.md")

# A section runs from its "## Heading" to the next "## " heading (or the end).
def section(text, heading):
    pattern = r"^##\s+" + re.escape(heading) + r"\b(.*?)(?=^##\s|\Z)"
    match = re.search(pattern, text, re.M | re.S)
    return match.group(1) if match else None


def read(name):
    return (BRIEF_DIR / name).read_text(encoding="utf-8")


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

    def test_each_brief_says_training_not_cleared(self):
        for name in BRIEFS:
            with self.subTest(brief=name):
                self.assertIn("training: not cleared", read(name),
                              "%s: missing 'training: not cleared'" % name)

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


if __name__ == "__main__":
    unittest.main()
