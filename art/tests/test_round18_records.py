#!/usr/bin/env python3
"""Tests for the round 18 source tree and the record that describes it.

`art/source/round18/RECORD.md` is the round's record: what was drawn, what was
picked, what was cut, and what each sheet became. Two things it has to stay true
about, because a file in the tree that the record does not account for is a
file nobody can place:

- every folder committed under the round is named in the record, and
- every `.credits.txt` in the round names references that are actually in the
  repo. A reference to a path that is not there is the same defect as a sheet
  with no credits: the picture cannot be traced back to what it was drawn from.

Round 18 only. The round 7 and 8 credits files name a few references with the
wrong extension (`.png` for a `.webp`); they predate this tree and are left as
they are rather than rewritten here.

Pure text checks: no network, no Pillow, no image files.
"""
import re
import unittest
from pathlib import Path

ART_DIR = Path(__file__).resolve().parents[1]          # the art/ folder
ROUND_DIR = ART_DIR / "source" / "round18"             # art/source/round18/
UI_SOFT_DIR = ROUND_DIR / "ui-soft"                    # the sheets
RECORD = ROUND_DIR / "RECORD.md"
REPO_ROOT = ART_DIR.parent                              # the parent of art/

# Every folder under the round, as a path relative to `ui-soft/`: "panels",
# "missing/tooltip". That is how the record writes them - the sheet table is
# headed "Sheet (under `ui-soft/`)" - so that is what has to be in the text for
# a reader to know what a folder holds.
FOLDERS = tuple(sorted(
    str(folder.relative_to(UI_SOFT_DIR))
    for folder in UI_SOFT_DIR.rglob("*") if folder.is_dir()))

# Every credits file in the round.
CREDITS = tuple(sorted(ROUND_DIR.rglob("*.credits.txt")))

# The credits line shape: "<picture> · <who> · tool: ... · references: a b c ·
# prompt: ... · <date> · status: ...". Everything up to the next "· " is the
# references field.
REFERENCES = re.compile(r"references: ([^·]*)")

# Only references written from the repo root can be checked: a credit line
# drawn from a session scratch folder marks it "session scratch; not retained"
# rather than naming the path, so there is nothing here to resolve. The
# separate `test_credits_clean` keeps absolute machine paths out of every
# credits file under art/source/.
REPO_REF = re.compile(r"^(?:art|worlds)/")


def read(path):
    return path.read_text(encoding="utf-8", errors="replace")


class Round18RecordTests(unittest.TestCase):
    maxDiff = None

    def test_the_record_is_here_and_there_is_a_tree_to_check(self):
        self.assertTrue(RECORD.is_file(), "missing %s" % RECORD)
        self.assertTrue(FOLDERS, "no folders under art/source/round18/")
        self.assertTrue(CREDITS, "no .credits.txt under art/source/round18/")

    def test_every_folder_in_the_round_is_named_in_the_record(self):
        # The round's own sheets, their redraws, the pieces cut out of them and
        # the run logs beside them: all of it has to be accounted for. A folder
        # the record never mentions is a set of pictures with no stated purpose.
        text = read(RECORD)
        for folder in FOLDERS:
            with self.subTest(folder=folder):
                self.assertTrue(
                    folder in text,
                    "RECORD.md never names ui-soft/%s; a folder in the round "
                    "that the record does not describe" % folder)

    def test_every_sheet_picture_has_a_credits_file_beside_it(self):
        # AGENTS.md: art we ship is art we made, every piece attributed. A
        # sheet folder is one that holds a run log; each picture in it is a
        # sheet round 18 drew, so each needs its own .credits.txt beside it.
        for log in sorted(ROUND_DIR.rglob("*_batch.log")):
            folder = log.parent
            with self.subTest(folder=str(folder.relative_to(UI_SOFT_DIR))):
                pictures = {p.stem for p in folder.glob("*.png")}
                pictures |= {p.stem for p in folder.glob("*.jpg")}
                self.assertTrue(pictures, "%s: a run log with no sheets" % folder)
                for picture in sorted(pictures):
                    self.assertTrue((folder / (picture + ".credits.txt")).is_file(),
                                    "%s: %s has no .credits.txt beside it"
                                    % (folder, picture))

    def test_every_credits_file_names_references_that_exist(self):
        for path in CREDITS:
            text = read(path)
            match = REFERENCES.search(text)
            with self.subTest(credits=str(path.relative_to(ROUND_DIR))):
                self.assertIsNotNone(match, "%s: no references field" % path)
                for reference in match.group(1).split():
                    if not REPO_REF.match(reference):
                        continue          # a scratch path from the drawing machine
                    self.assertTrue(
                        (REPO_ROOT / reference).exists(),
                        "%s references %s, which is not in the repo"
                        % (path, reference))


if __name__ == "__main__":
    unittest.main()