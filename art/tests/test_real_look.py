#!/usr/bin/env python3
"""Tests for real_look.py, and for the promise the look-*.png files keep.

The first half is about the tool: a size it will not accept is refused, and -
the one that matters - a run that cannot take a picture says so and writes no
file, because a stale `look.png` left behind by a failed run is exactly the
sort of thing this repository has been bitten by.

The second half is about what sits in `art/skins/parchment-and-wood/`. Those
files are the pack's play evidence: pictures of the woven player, taken by
running it. The cost of that being wrong is a person reading a drawing and
believing they had seen the game, so the folder is pinned here - every PNG in it
is a screenshot at one of the two viewport sizes the README names, and no
mock- or preview- named drawing is allowed back into it.

Neither half needs a browser: the browser path is exercised for real by
`vefr look` and by art/tools/real_look.py itself when the evidence is taken.
"""
import contextlib
import io
import os
import sys
import tempfile
import unittest

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
import real_look as rl

SKIN_DIR = os.path.join(REPO, "art", "skins", "parchment-and-wood")
MOCK_DIR = os.path.join(REPO, "art", "skins", "mock-renders")
# The viewports the README promises, and the evidence file each one is.
VIEWPORTS = {
    "look-desktop.png": (1280, 800),
    "look-desktop-menu.png": (1280, 800),
    "look-desktop-bag.png": (1280, 800),
    "look-phone.png": (390, 844),
    "look-phone-menu.png": (390, 844),
    "look-phone-bag.png": (390, 844),
}
# The one PNGs in the folder that are art rather than evidence: the skin's own
# seamless textures, which the player paints and which nobody could mistake for
# a screenshot of the game.
TEXTURES = ("parchment.png", "wood.png", "brass.png")


class SizeTests(unittest.TestCase):
    def setUp(self):
        # fail() writes to stderr on purpose; the tests are not about its prose.
        self._err = contextlib.redirect_stderr(io.StringIO())
        self._err.__enter__()
        self.addCleanup(self._err.__exit__, None, None, None)

    def test_a_size_is_read_as_a_pair(self):
        self.assertEqual(rl.parse_size("1280x800"), (1280, 800))
        self.assertEqual(rl.parse_size("390X844"), (390, 844))

    def test_a_size_that_is_not_a_pair_is_refused(self):
        for bad in ("1280", "1280x", "x800", "1280x800x600"):
            with self.assertRaises(SystemExit) as caught:
                rl.parse_size(bad)
            self.assertEqual(caught.exception.code, 2, f"{bad!r} should be refused")

    def test_a_size_that_is_not_whole_numbers_is_refused(self):
        for bad in ("axb", "1280x8oo", "-1x10", "0x10", "10x0"):
            with self.assertRaises(SystemExit):
                rl.parse_size(bad)


class RunTests(unittest.TestCase):
    """The promise that matters: a run that fails writes no picture."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()

    def run_tool(self, *argv):
        code = None
        with contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            try:
                code = rl.main(list(argv))
            except SystemExit as exc:
                code = exc.code
        return code

    def test_a_woven_file_that_is_not_there_is_refused_and_writes_nothing(self):
        out = os.path.join(self.dir, "look.png")
        code = self.run_tool("--html", os.path.join(self.dir, "nope.html"),
                             "--out", out)
        self.assertEqual(code, 2)
        self.assertFalse(os.path.exists(out),
                         "a refused run must not leave a picture a reader would trust")

    def test_yesterdays_picture_is_removed_before_a_run_that_then_fails(self):
        out = os.path.join(self.dir, "look.png")
        with open(out, "wb") as fh:
            fh.write(b"\x89PNG yesterday")
        with open(os.path.join(self.dir, "w.html"), "w", encoding="utf-8") as fh:
            fh.write("<html></html>")
        code = self.run_tool("--html", os.path.join(self.dir, "w.html"),
                             "--out", out, "--element", "#nope")
        self.assertEqual(code, 2)
        self.assertFalse(os.path.exists(out),
                         "a stale picture must not outlive a run that could not "
                         "replace it; it would read as this run's evidence")

    def test_a_bad_size_is_refused_and_writes_nothing(self):
        out = os.path.join(self.dir, "look.png")
        with open(os.path.join(self.dir, "w.html"), "w", encoding="utf-8") as fh:
            fh.write("<html></html>")
        code = self.run_tool("--html", os.path.join(self.dir, "w.html"),
                             "--out", out, "--size", "wide")
        self.assertEqual(code, 2)
        self.assertFalse(os.path.exists(out))

    def test_an_element_that_is_not_there_is_refused_and_writes_nothing(self):
        out = os.path.join(self.dir, "part.png")
        with open(os.path.join(self.dir, "w.html"), "w", encoding="utf-8") as fh:
            fh.write("<html></html>")
        code = self.run_tool("--html", os.path.join(self.dir, "w.html"),
                             "--out", out, "--element", "#nope")
        self.assertEqual(code, 2)
        self.assertFalse(os.path.exists(out),
                         "a refused run must not leave a picture a reader would trust")


class EvidenceTests(unittest.TestCase):
    """What `art/skins/parchment-and-wood/` is allowed to contain."""

    def test_the_folder_holds_every_named_screenshot(self):
        for name in VIEWPORTS:
            self.assertTrue(os.path.isfile(os.path.join(SKIN_DIR, name)),
                            f"{name} is missing; the README promises it")

    def test_every_png_in_the_folder_is_a_screenshot_at_a_promised_viewport(self):
        for name in os.listdir(SKIN_DIR):
            if not name.lower().endswith(".png") or name in TEXTURES:
                continue
            self.assertIn(name, VIEWPORTS,
                          f"{name} is a PNG in the evidence folder that no README "
                          f"entry vouches for")
            with Image.open(os.path.join(SKIN_DIR, name)) as im:
                self.assertEqual(im.format, "PNG")
                self.assertEqual(im.size, VIEWPORTS[name],
                                 f"{name} is not the size it claims to be")

    def test_no_drawing_is_allowed_to_masquerade_as_a_screenshot(self):
        for name in os.listdir(SKIN_DIR):
            stem = name.split(".")[0].lower()
            for banned in ("mock", "preview"):
                self.assertFalse(stem.startswith(banned),
                                 f"{name} is a drawing; it belongs in mock-renders/")

    def test_the_mocks_live_in_mock_renders_and_say_what_they_are(self):
        mocks = [n for n in os.listdir(MOCK_DIR) if n.lower().endswith(".png")]
        self.assertTrue(mocks, "the mocks are a rendering aid and should still be kept")
        for name in mocks:
            self.assertTrue(name.lower().startswith(("mock-", "preview")),
                            f"{name} is in mock-renders/ but is not named as a drawing")
        self.assertTrue(os.path.isfile(os.path.join(MOCK_DIR, "README.md")),
                        "mock-renders/ must say in writing that it is not evidence")


if __name__ == "__main__":
    unittest.main()