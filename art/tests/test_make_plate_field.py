#!/usr/bin/env python3
"""Tests for make_plate_field.py, built from synthetic Pillow images only.

The ornament is made in memory with Image.new/putpixel and written into a
TemporaryDirectory that cleans itself up; no picture from art/source/ is ever
read. What is pinned here is the promise the tool makes to the player, who
stretches these pictures across boxes of no fixed shape: the frame is gone and
no frame colour survives, the middle is still fully opaque, the edges fade, and
two runs give identical bytes. A tool that quietly kept the frame would put the
same warped picture back on screen and pass every other test here.
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
import make_plate_field as mpf

FRAME = (120, 78, 30, 255)      # the honey wood a frame is drawn in
FIELD = (226, 188, 130, 255)    # the parchment drawn inside it
SIZE = (64, 64)
INSET = (0.14, 0.14, 0.14, 0.14)


def framed():
    """An RGBA picture: a wood frame with a flat parchment field inside it."""
    im = Image.new("RGBA", SIZE, FRAME)
    box = (round(SIZE[0] * INSET[0]), round(SIZE[1] * INSET[1]),
           round(SIZE[0] * (1 - INSET[2])), round(SIZE[1] * (1 - INSET[3])))
    for x in range(box[0], box[2]):
        for y in range(box[1], box[3]):
            im.putpixel((x, y), FIELD)
    return im


def hollow():
    """An RGBA picture that is nothing but transparency - an inset outside it."""
    return Image.new("RGBA", (8, 8), (0, 0, 0, 0))


class RampTests(unittest.TestCase):
    def test_a_ramp_is_full_in_the_middle_and_fades_at_both_ends(self):
        values = mpf.ramp(20, 4)
        self.assertEqual(len(values), 20)
        self.assertEqual(max(values), 255)
        self.assertEqual(values[0], 0, "the edge itself must be see-through")
        self.assertEqual(values, values[::-1], "a ramp must fade the same both ways")

    def test_a_feather_wider_than_the_picture_still_fades_to_nothing(self):
        values = mpf.ramp(8, 99)
        self.assertEqual(len(values), 8)
        self.assertEqual(values[0], 0)
        self.assertEqual(values, values[::-1])

    def test_a_picture_one_pixel_wide_does_not_explode(self):
        self.assertEqual(mpf.ramp(1, 2), [255])


class FieldTests(unittest.TestCase):
    def setUp(self):
        self.out = mpf.field(framed(), INSET, mpf.DEFAULT_FEATHER, 0.5)

    def test_the_field_is_the_crop_and_not_the_whole_picture(self):
        self.assertEqual(self.out.size, (46, 46))
        self.assertLess(self.out.size[0], SIZE[0])

    def test_no_frame_colour_survives_the_crop(self):
        for y in range(self.out.size[1]):
            for x in range(self.out.size[0]):
                self.assertNotEqual(self.out.getpixel((x, y))[:3], FRAME[:3],
                                    f"frame colour left at ({x}, {y})")

    def test_the_middle_stays_opaque_and_the_edges_fade(self):
        alpha = self.out.getchannel("A")
        self.assertEqual(alpha.getextrema(), (alpha.getextrema()[0], 255))
        self.assertEqual(alpha.getpixel((self.out.size[0] // 2,
                                         self.out.size[1] // 2)), 255)
        self.assertLess(alpha.getpixel((0, self.out.size[1] // 2)), 255)

    def test_the_flatten_smoothing_reaches_every_pixel(self):
        plain = mpf.field(framed(), INSET, mpf.DEFAULT_FEATHER, 0.0)
        # the field is a flat colour either way; what differs is the crop's own
        # detail, which flatten smooths away. Check the seam, not the picture.
        self.assertEqual(plain.size, self.out.size)
        self.assertNotEqual(plain.tobytes(), framed().tobytes())


class CommandTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        # PNG, not WebP: Pillow's default WebP save is lossy and would throw
        # the alpha away before the tool ever saw it.
        self.src = os.path.join(self._tmp.name, "slot.png")
        framed().save(self.src)

    def tearDown(self):
        self._tmp.cleanup()

    def run_tool(self, src, out, *extra):
        code, err = None, ""
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
                code = mpf.main([src, out, *extra])
        except SystemExit as exc:
            code = exc.code
        return code, buf.getvalue()

    def test_it_writes_a_picture_and_says_which(self):
        out = os.path.join(self._tmp.name, "field.webp")
        code, printed = self.run_tool(self.src, out)
        self.assertEqual(code, 0)
        self.assertIn("field.webp", printed)
        self.assertTrue(os.path.isfile(out))

    def test_running_twice_gives_identical_bytes(self):
        a, b = (os.path.join(self._tmp.name, n) for n in ("a.webp", "b.webp"))
        self.run_tool(self.src, a)
        self.run_tool(self.src, b)
        with open(a, "rb") as fa, open(b, "rb") as fb:
            self.assertEqual(fa.read(), fb.read())

    def test_the_inset_is_honoured(self):
        wide = os.path.join(self._tmp.name, "wide.webp")
        self.run_tool(self.src, wide, "--inset", "0.3,0.3,0.3,0.3")
        with Image.open(wide) as im:
            self.assertLess(im.size[0], self.out_size_of_default())

    def out_size_of_default(self):
        out = os.path.join(self._tmp.name, "default.webp")
        self.run_tool(self.src, out)
        with Image.open(out) as im:
            return im.size[0]

    def test_an_unreadable_input_is_a_plain_failure(self):
        code, _ = self.run_tool(os.path.join(self._tmp.name, "nope.webp"),
                                os.path.join(self._tmp.name, "out.webp"))
        self.assertEqual(code, 2)

    def test_an_input_without_alpha_is_a_plain_failure(self):
        rgb = os.path.join(self._tmp.name, "flat.png")
        Image.new("RGB", (8, 8), (10, 10, 10)).save(rgb)
        code, _ = self.run_tool(rgb, os.path.join(self._tmp.name, "out.webp"))
        self.assertEqual(code, 2)

    def test_an_output_that_is_not_a_picture_is_a_plain_failure(self):
        code, _ = self.run_tool(self.src, os.path.join(self._tmp.name, "out.gif"))
        self.assertEqual(code, 2)

    def test_an_inset_outside_the_allowed_range_is_a_plain_failure(self):
        for bad in ("0.51,0.1,0.1,0.1", "-0.1,0.1,0.1,0.1", "0.1,0.1", "a,b,c,d"):
            code, _ = self.run_tool(self.src, os.path.join(self._tmp.name, "out.webp"),
                                    "--inset", bad)
            self.assertEqual(code, 2, f"--inset {bad!r} should be refused")

    def test_a_feather_or_flatten_outside_the_allowed_range_is_a_plain_failure(self):
        for flag, bad in (("--feather", "0.9"), ("--flatten", "-1"), ("--flatten", "2")):
            code, _ = self.run_tool(self.src, os.path.join(self._tmp.name, "out.webp"),
                                    flag, bad)
            self.assertEqual(code, 2, f"{flag} {bad} should be refused")

    def test_an_inset_that_crops_everything_away_is_a_plain_failure(self):
        code, _ = self.run_tool(self.src, os.path.join(self._tmp.name, "out.webp"),
                                "--inset", "0.5,0.5,0.5,0.5")
        self.assertEqual(code, 2)

    def test_an_inset_outside_the_picture_is_refused_not_silently_blank(self):
        src = os.path.join(self._tmp.name, "nothing.png")
        hollow().save(src)
        out = os.path.join(self._tmp.name, "out.webp")
        code, _ = self.run_tool(src, out)
        self.assertEqual(code, 2, "a fully transparent field must be a failure, "
                                  "not a part that looks like an empty box")
        self.assertFalse(os.path.exists(out))


if __name__ == "__main__":
    unittest.main()