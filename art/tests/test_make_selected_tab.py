#!/usr/bin/env python3
"""Tests for make_selected_tab.py, built from synthetic Pillow images only.

The chip is made in memory with Image.new/putpixel and written into a
TemporaryDirectory that cleans itself up; no picture from art/source/ is ever
read. What is pinned here is the promise the tool makes: the alpha is carried
across untouched (so the selected chip is the *same shape* as the tab chip, which
is the whole reason the tool exists), every colour moves toward the cream, and
two runs give identical bytes.
"""
import contextlib
import io
import os
import sys
import tempfile
import unittest

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
import make_selected_tab as mst


def chip():
    """A small RGBA chip: an opaque block, a clear one, and a fully transparent one."""
    im = Image.new("RGBA", (8, 4), (0, 0, 0, 0))
    for x in range(4):
        for y in range(4):
            im.putpixel((x, y), (120, 80, 40, 255))
    for x in range(4, 8):
        for y in range(4):
            im.putpixel((x, y), (60, 40, 20, 0))     # colour under a clear pixel
    return im


class LightenTests(unittest.TestCase):
    def test_alpha_is_carried_across_untouched(self):
        out = mst.lighten(chip(), mst.DEFAULT_AMOUNT)
        for y in range(4):
            for x in range(8):
                self.assertEqual(out.getpixel((x, y))[3], chip().getpixel((x, y))[3],
                                 f"alpha moved at ({x}, {y})")

    def test_size_is_unchanged(self):
        self.assertEqual(mst.lighten(chip(), 0.5).size, (8, 4))

    def test_every_opaque_colour_moves_toward_the_cream(self):
        out = mst.lighten(chip(), mst.DEFAULT_AMOUNT)
        src = chip()
        for x in range(4):
            for y in range(4):
                before, after = src.getpixel((x, y))[:3], out.getpixel((x, y))[:3]
                for b, a, cream in zip(before, after, mst.CREAM):
                    # closer to the cream than it was, and never past it
                    self.assertLess(abs(a - cream), abs(b - cream))
                    self.assertEqual(a, round(b + (cream - b) * mst.DEFAULT_AMOUNT))

    def test_an_amount_of_zero_changes_nothing(self):
        out = mst.lighten(chip(), 0.0)
        self.assertEqual(list(out.convert("RGBA").tobytes()), list(chip().convert("RGBA").tobytes()))

    def test_an_amount_of_one_reaches_the_cream(self):
        out = mst.lighten(chip(), 1.0)
        for x in range(4):
            for y in range(4):
                self.assertEqual(out.getpixel((x, y)), mst.CREAM + (255,))


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.src = os.path.join(self.dir.name, "tab.webp")
        chip().save(self.src)

    def run_tool(self, *argv):
        """Run the tool with both streams captured, returning (code, stdout)."""
        out_buf, err_buf = io.StringIO(), io.StringIO()
        code = None
        try:
            with contextlib.redirect_stdout(out_buf), contextlib.redirect_stderr(err_buf):
                code = mst.main(list(argv))
        except SystemExit as exc:
            code = exc.code
        return code, out_buf.getvalue()

    def test_it_writes_the_chip_and_prints_one_line(self):
        dest = os.path.join(self.dir.name, "sel.webp")
        code, printed = self.run_tool(self.src, dest)
        self.assertEqual(code, 0)
        self.assertEqual(printed, f"wrote {dest}\n")
        self.assertTrue(os.path.exists(dest))

    def test_running_twice_gives_identical_bytes(self):
        a, b = (os.path.join(self.dir.name, n) for n in ("a.webp", "b.webp"))
        self.run_tool(self.src, a)
        self.run_tool(self.src, b)
        with open(a, "rb") as fa, open(b, "rb") as fb:
            self.assertEqual(fa.read(), fb.read())

    def test_the_amount_is_honoured(self):
        weak, strong = (os.path.join(self.dir.name, n) for n in ("weak.webp", "strong.webp"))
        self.run_tool(self.src, weak, "--amount", "0.1")
        self.run_tool(self.src, strong, "--amount", "0.9")
        with Image.open(weak) as weak_im, Image.open(strong) as strong_im:
            weak_px, strong_px = weak_im.getpixel((0, 0))[:3], strong_im.getpixel((0, 0))[:3]
        self.assertGreater(strong_px[0], weak_px[0])

    def test_an_unreadable_input_is_a_plain_failure(self):
        code, _ = self.run_tool(os.path.join(self.dir.name, "nope.webp"),
                                os.path.join(self.dir.name, "out.webp"))
        self.assertEqual(code, 2)

    def test_an_input_without_alpha_is_a_plain_failure(self):
        rgb = os.path.join(self.dir.name, "flat.png")
        Image.new("RGB", (4, 4), (10, 10, 10)).save(rgb)
        self.addCleanup(lambda: os.path.exists(rgb) and os.remove(rgb))
        code, _ = self.run_tool(rgb, os.path.join(self.dir.name, "out.webp"))
        self.assertEqual(code, 2)

    def test_an_output_that_is_not_a_picture_is_a_plain_failure(self):
        code, _ = self.run_tool(self.src, os.path.join(self.dir.name, "out.gif"))
        self.assertEqual(code, 2)

    def test_an_amount_outside_zero_to_one_is_a_plain_failure(self):
        code, _ = self.run_tool(self.src, os.path.join(self.dir.name, "out.webp"),
                                "--amount", "1.4")
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()