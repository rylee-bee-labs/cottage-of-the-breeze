#!/usr/bin/env python3
"""Tests that no committed credits file leaks a machine-local path.

A `.credits.txt` is the provenance record for a picture: who drew it, from
which reference images, and with which prompt. Until 2026-10-16 the generator
wrote the references exactly as it received them, so the credits files for art
rounds 11 through 13 name absolute paths from the machine that drew the
pictures - a Codex session scratch folder under /tmp, and the author's home
directory inside it. A path that only one machine can resolve is private
layout, not provenance, and the repo may be distributed one day. The existing
files were rewritten to repo-relative references (or to the marker
"session scratch; not retained" when the reference was never kept) and
`art/tools/codex_batch.sh` was fixed to write that form; these tests keep it so.

Text only: no network, no Pillow, no image files.
"""
import re
import unittest
from pathlib import Path

ART_DIR = Path(__file__).resolve().parents[1]          # the art/ folder
SOURCE_DIR = ART_DIR / "source"                        # art/source/

# Every committed credits file, whichever round it came from. One that arrives
# in a later round is covered on arrival.
CREDITS = tuple(sorted(SOURCE_DIR.rglob("*.credits.txt")))

# An absolute path into the drawing machine: a scratch folder under /tmp, or a
# home directory (/home/..., /Users/...). None of these names anything a reader
# of the repo can resolve.
MACHINE_PATH = re.compile(r"/(?:tmp|home|Users)/")

# The whole-file scan is deliberate: a machine path is private wherever it
# appears in the line, not only in the references field.


def read(path):
    return path.read_text(encoding="utf-8", errors="replace")


def line_of(text, pattern):
    """The 1-based number of the first line `pattern` matches, for the message."""
    for number, line in enumerate(text.splitlines(), start=1):
        if pattern.search(line):
            return number
    return 0


class CreditsCleanTests(unittest.TestCase):
    maxDiff = None

    def test_there_are_credits_files_to_check(self):
        self.assertTrue(CREDITS, "no .credits.txt under art/source/")

    def test_no_credits_file_names_a_machine_local_path(self):
        for path in CREDITS:
            text = read(path)
            match = MACHINE_PATH.search(text)
            with self.subTest(credits=str(path.relative_to(SOURCE_DIR))):
                self.assertIsNone(
                    match,
                    "%s:%d names the machine-local path %r; references are "
                    "written from the repo root, or marked "
                    "\"session scratch; not retained\""
                    % (path, line_of(text, MACHINE_PATH),
                       match.group(0) if match else ""))


if __name__ == "__main__":
    unittest.main()
