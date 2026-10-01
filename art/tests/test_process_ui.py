#!/usr/bin/env python3
"""Tests for process_ui.py, built from synthetic Pillow images only."""
import contextlib
import io
import os
import sys
import tempfile
import unittest

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
import process_ui as ui

MARGIN = (235, 228, 216)  # the flat background drawn around a panel
BORDER = (26, 30, 58)     # a dark border
INSIDE = (172, 122, 74)   # a different middle colour
STUD = (200, 60, 40)      # odd pixels in the bottom-right corner


def paint(img, box, colour):
    """Paint a rectangle into the picture."""
    for x in range(box[0], box[2]):
        for y in range(box[1], box[3]):
            img.putpixel((x, y), colour)


def uneven_panel():
    """A panel on a flat margin: uneven border, different middle, odd bottom-right."""
    img = Image.new("RGB", (72, 72), MARGIN)
    paint(img, (6, 6, 66, 66), BORDER)    # the border block, 6 px of margin all round
    paint(img, (14, 13, 60, 57), INSIDE)  # left 8, right 6, top 7, bottom 9
    paint(img, (60, 57, 66, 66), STUD)    # the bottom-right corner differs from top-left
    return img


def checkerboard(width, height, block=6):
    """A drawn grey/white 'transparent' checkerboard, like a generator draws one."""
    img = Image.new("RGB", (width, height), (255, 255, 255))
    for y in range(height):
        for x in range(width):
            if ((x // block) + (y // block)) % 2:
                img.putpixel((x, y), (204, 204, 204))
    return img


def rounded_box():
    """A box with rounded corners standing on a drawn checkerboard."""
    img = checkerboard(80, 80)
    for y in range(8, 72):
        for x in range(8, 72):
            if (x < 14 or x >= 66) and (y < 14 or y >= 66):
                continue  # a rounded-off corner, left as checkerboard
            if x < 16 or x >= 64 or y < 16 or y >= 64:
                img.putpixel((x, y), BORDER)
            else:
                img.putpixel((x, y), INSIDE)
    return img


def first_diff(a, b):
    """The first pixel where two pictures differ, or None."""
    pa, pb = a.load(), b.load()
    for y in range(a.size[1]):
        for x in range(a.size[0]):
            if pa[x, y] != pb[x, y]:
                return (x, y, pa[x, y], pb[x, y])
    return None


def pale_neutral_pixel(img):
    """The first visible pixel that looks like a leftover checkerboard, or None."""
    px = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b, a = px[x, y]
            if a >= 128 and min(r, g, b) >= 150 and max(r, g, b) - min(r, g, b) <= 14:
                return (x, y, (r, g, b, a))
    return None


class BoxTest(unittest.TestCase):
    """The box command: symmetry, size, fills and transparency."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()

    def save(self, img, name="in.png"):
        """Save a synthetic picture into the temporary directory."""
        path = os.path.join(self.dir, name)
        img.save(path)
        return path

    def box(self, img, size="80x64", slice_n=12, *extra):
        """Run the box command on a synthetic picture and return the output."""
        src = self.save(img)
        out = os.path.join(self.dir, "out.png")
        with contextlib.redirect_stdout(io.StringIO()):
            rc = ui.main(["box", src, out, "--size", size, "--slice", str(slice_n)]
                         + list(extra))
        self.assertEqual(rc, 0)
        return Image.open(out).convert("RGBA")

    def test_output_equals_its_own_flips(self):
        out = self.box(uneven_panel())
        diff = first_diff(out, out.transpose(Image.FLIP_LEFT_RIGHT))
        self.assertIsNone(diff, f"differs from its left-right flip at {diff}")
        diff = first_diff(out, out.transpose(Image.FLIP_TOP_BOTTOM))
        self.assertIsNone(diff, f"differs from its top-bottom flip at {diff}")

    def test_output_is_exactly_the_size(self):
        out = self.box(uneven_panel(), "80x64", 12)
        self.assertEqual(out.size, (80, 64))

    def test_fill_colour_fills_the_centre_not_the_border(self):
        out = self.box(uneven_panel(), "80x64", 12, "--fill-colour", "#12ab34")
        self.assertEqual(out.getpixel((40, 32)), (0x12, 0xAB, 0x34, 255))
        self.assertNotEqual(out.getpixel((40, 4)), (0x12, 0xAB, 0x34, 255))

    def test_default_fill_is_the_average_of_the_centre_patch(self):
        out = self.box(uneven_panel(), "80x64", 12)
        # The centre patch of the trimmed, resized panel is flat INSIDE, so the
        # default fill (the average of that patch) paints the middle that colour.
        self.assertEqual(out.getpixel((40, 32)), INSIDE + (255,))
        self.assertNotEqual(out.getpixel((40, 4)), INSIDE + (255,))

    def test_texture_fill_tiles_inside_and_keeps_its_alpha(self):
        tex = Image.new("RGBA", (8, 8), (10, 200, 90, 255))
        tex.putpixel((0, 0), (0, 0, 0, 0))       # a hole in the texture
        tex.putpixel((4, 4), (240, 240, 60, 255))
        out = self.box(uneven_panel(), "80x64", 12, "--fill", self.save(tex, "tex.png"))
        # The inside starts at (12, 12): (40, 32) is 28,20 in, 28 % 8 = 4, 20 % 8 = 4.
        self.assertEqual(out.getpixel((40, 32)), (240, 240, 60, 255))
        self.assertEqual(out.getpixel((12, 12))[3], 0)   # the texture's hole survives
        self.assertNotEqual(out.getpixel((40, 4))[:3], (10, 200, 90))

    def test_checkerboard_is_cleared_and_corners_stay_transparent(self):
        out = self.box(rounded_box(), "96x96", 12)
        px = out.load()
        for corner in ((0, 0), (95, 0), (0, 95), (95, 95)):
            self.assertEqual(px[corner][3], 0, f"corner {corner} is not transparent")
        leftover = pale_neutral_pixel(out)
        self.assertIsNone(leftover, f"a pale checkerboard pixel survived at {leftover}")

    def test_no_trim_keeps_the_whole_picture_and_still_symmetrises(self):
        out = self.box(uneven_panel(), "80x64", 12, "--no-trim")
        self.assertEqual(out.size, (80, 64))
        diff = first_diff(out, out.transpose(Image.FLIP_LEFT_RIGHT))
        self.assertIsNone(diff, f"differs from its left-right flip at {diff}")


class StripTest(unittest.TestCase):
    """The strip command: fit, centre, keep the aspect ratio and transparency."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()

    def run_strip(self, img, size):
        """Run the strip command on a synthetic picture, returning it and the output."""
        src = os.path.join(self.dir, "in.png")
        img.save(src)
        out = os.path.join(self.dir, "out.png")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = ui.main(["strip", src, out, "--size", size])
        self.assertEqual(rc, 0)
        return Image.open(out).convert("RGBA"), buf.getvalue().splitlines()

    def test_strip_fits_keeps_aspect_and_centres(self):
        src = Image.new("RGB", (100, 30), MARGIN)
        paint(src, (10, 5, 90, 25), STUD)      # 80x20 content: a 4:1 divider
        out, lines = self.run_strip(src, "40x40")
        self.assertEqual(out.size, (40, 40))
        self.assertEqual(lines, [f"wrote {os.path.join(self.dir, 'out.png')}"])
        bbox = out.getchannel("A").getbbox()
        self.assertEqual(bbox, (0, 15, 40, 25))
        self.assertEqual(bbox[0], 40 - bbox[2])            # equal left and right margins
        self.assertEqual(bbox[1], 40 - bbox[3])            # equal top and bottom margins
        self.assertEqual(bbox[2] - bbox[0], 4 * (bbox[3] - bbox[1]))  # aspect kept

    def test_strip_never_upscales_more_than_twice(self):
        src = Image.new("RGB", (40, 40), MARGIN)
        paint(src, (15, 15, 25, 25), BORDER)    # 10x10 content in a 40x40 margin
        out, _ = self.run_strip(src, "100x100")
        bbox = out.getchannel("A").getbbox()
        self.assertEqual(bbox, (40, 40, 60, 60))  # 20x20: doubled, not grown ten times


class ErrorTest(unittest.TestCase):
    """Bad arguments exit 2 with a plain one-line message."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = self._tmp.name
        self.src = os.path.join(self.dir, "in.png")
        uneven_panel().save(self.src)

    def tearDown(self):
        self._tmp.cleanup()

    def run_main(self, args):
        """Run main with stderr captured, returning (exit code, stderr)."""
        err = io.StringIO()
        code = None
        try:
            with contextlib.redirect_stderr(err):
                code = ui.main(args)
        except SystemExit as exc:
            code = exc.code
        return code, err.getvalue()

    def test_slice_too_large_for_the_size_exits_two(self):
        out = os.path.join(self.dir, "out.png")
        code, err = self.run_main(["box", self.src, out, "--size", "40x40",
                                   "--slice", "20"])
        self.assertEqual(code, 2)
        self.assertIn("impossible", err)

    def test_bad_size_exits_two(self):
        out = os.path.join(self.dir, "out.png")
        for bad in ("40", "0x40", "forty", "40x"):
            with self.subTest(size=bad):
                code, err = self.run_main(["box", self.src, out,
                                           "--size", bad, "--slice", "4"])
                self.assertEqual(code, 2)
                self.assertIn("--size", err)

    def test_bad_fill_colour_exits_two(self):
        out = os.path.join(self.dir, "out.png")
        code, err = self.run_main(["box", self.src, out, "--size", "40x40",
                                   "--slice", "4", "--fill-colour", "12ab34"])
        self.assertEqual(code, 2)
        self.assertIn("--fill-colour", err)

    def test_fill_and_fill_colour_are_mutually_exclusive(self):
        out = os.path.join(self.dir, "out.png")
        code, err = self.run_main(["box", self.src, out, "--size", "40x40",
                                   "--slice", "4", "--fill", self.src,
                                   "--fill-colour", "#12ab34"])
        self.assertEqual(code, 2)
        self.assertIn("not allowed with argument", err)

    def test_out_must_end_in_png_or_webp(self):
        code, err = self.run_main(["strip", self.src,
                                   os.path.join(self.dir, "out.gif"), "--size", "40x40"])
        self.assertEqual(code, 2)
        self.assertIn(".png or .webp", err)


class CliTest(unittest.TestCase):
    """The command line writes the file and prints the CSS slice line."""

    def test_main_prints_wrote_and_border_image_slice(self):
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "panel.png")
            uneven_panel().save(src)
            out = os.path.join(d, "panel.webp")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = ui.main(["box", src, out, "--size", "80x64", "--slice", "12"])
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.exists(out))
            self.assertEqual(buf.getvalue().splitlines(),
                             [f"wrote {out}", "border-image-slice: 12"])


if __name__ == "__main__":
    unittest.main()
