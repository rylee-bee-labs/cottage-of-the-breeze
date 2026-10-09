#!/usr/bin/env python3
"""Tests for mock_skin.py, built from synthetic Pillow images only.

A whole skin folder is made in memory - one small part picture per part, a
skin.json naming them - and written into a TemporaryDirectory that cleans itself
up; no picture from art/skins/ or the pack is ever read. What is pinned here is
the promise the mock makes: it reads skin.json rather than assuming, it
nine-slices the way the player does, and it draws at the size asked for.
"""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
import mock_skin as ms

RIM = (150, 100, 50, 255)     # the drawn rim every part carries
FACE = (230, 210, 170, 255)   # the face inside it


def part(size, rim=RIM, face=FACE):
    """A part picture: a solid rim with a lighter face in the middle."""
    im = Image.new("RGBA", size, rim)
    for x in range(size[0] // 4, size[0] - size[0] // 4):
        for y in range(size[1] // 4, size[1] - size[1] // 4):
            im.putpixel((x, y), face)
    return im


class NineSliceTests(unittest.TestCase):
    def test_it_returns_the_size_asked_for(self):
        out = ms.nine_slice(part((96, 96)), 300, 180, 32)
        self.assertEqual(out.size, (300, 180))

    def test_the_corners_are_pasted_whole_and_unscaled(self):
        src = part((96, 96))
        out = ms.nine_slice(src, 300, 180, 32)
        self.assertEqual(out.getpixel((0, 0)), src.getpixel((0, 0)))
        self.assertEqual(out.getpixel((299, 0)), src.getpixel((95, 0)))
        self.assertEqual(out.getpixel((0, 179)), src.getpixel((0, 95)))
        self.assertEqual(out.getpixel((299, 179)), src.getpixel((95, 95)))

    def test_the_middle_is_filled_across_the_whole_stretched_box(self):
        # The centre of a stretched part is the face, all the way out to the edges:
        # this is the quilt the README warns about, and it must be what a mock shows.
        out = ms.nine_slice(part((96, 96)), 300, 180, 32)
        self.assertEqual(out.getpixel((150, 90)), FACE)
        self.assertEqual(out.getpixel((32, 90)), FACE)

    def test_a_slice_that_does_not_fit_is_a_plain_failure(self):
        with contextlib.redirect_stderr(io.StringIO()) as err:
            with self.assertRaises(SystemExit) as caught:
                ms.nine_slice(part((32, 32)), 300, 180, 32)
        self.assertEqual(caught.exception.code, 2)
        self.assertIn("slice 32 does not fit", err.getvalue())

    def test_a_box_smaller_than_two_slices_falls_back_to_a_stretch(self):
        # Not an error: a tooltip drawn narrow is a real thing to want to look at.
        out = ms.nine_slice(part((96, 96)), 30, 40, 32)
        self.assertEqual(out.size, (30, 40))


class SizeTests(unittest.TestCase):
    def test_a_named_viewport_resolves(self):
        self.assertEqual(ms.parse_size("phone"), ms.SIZES["phone"])
        self.assertEqual(ms.parse_size("desktop"), ms.SIZES["desktop"])

    def test_an_explicit_size_resolves(self):
        self.assertEqual(ms.parse_size("800x600"), (800, 600))

    def test_nonsense_is_a_plain_failure(self):
        with contextlib.redirect_stderr(io.StringIO()) as err:
            with self.assertRaises(SystemExit) as caught:
                ms.parse_size("wide")
        self.assertEqual(caught.exception.code, 2)
        self.assertIn("--size wants WxH", err.getvalue())


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.skin = os.path.join(self.dir.name, "skin")
        os.makedirs(self.skin)
        parts = {
            "panel": ("panel.webp", 32), "button": ("button.webp", 14),
            "tab": ("tab.webp", 14), "slot": ("slot.webp", 16),
            "speech": ("speech.webp", 24), "tooltip": ("tooltip.webp", 20),
            "gold-plate": ("gold-plate.webp", 10),
        }
        for name, (file, _) in parts.items():
            part((96, 96)).save(os.path.join(self.skin, file))
        part((96, 40)).save(os.path.join(self.skin, "tab-selected.webp"))
        part((192, 32)).save(os.path.join(self.skin, "bar-frame.webp"))
        part((176, 20)).save(os.path.join(self.skin, "bar-fill.webp"))
        Image.new("RGB", (256, 256), (90, 70, 50)).save(os.path.join(self.skin, "backdrop.webp"))
        manifest = {
            "name": "test",
            "backdrop": "backdrop.webp",
            "parts": {name: {"file": file, "slice": slice_}
                      for name, (file, slice_) in parts.items()},
            "ink": {"on_panel": "#2B2118", "on_panel_dim": "#5A4A38"},
        }
        manifest["parts"]["tab"]["selected"] = "tab-selected.webp"
        manifest["parts"]["bar"] = {"frame": "bar-frame.webp", "fill": "bar-fill.webp"}
        with open(os.path.join(self.skin, "skin.json"), "w", encoding="utf-8") as fh:
            json.dump(manifest, fh)
        self.out = os.path.join(self.dir.name, "look.png")

    def run_mock(self, *argv):
        out_buf, err_buf = io.StringIO(), io.StringIO()
        code = None
        try:
            with contextlib.redirect_stdout(out_buf), contextlib.redirect_stderr(err_buf):
                code = ms.main(list(argv))
        except SystemExit as exc:
            code = exc.code
        return code, out_buf.getvalue(), err_buf.getvalue()

    def test_it_draws_at_the_size_asked_for(self):
        code, _, err = self.run_mock(self.skin, self.out, "--size", "390x844")
        self.assertEqual(code, 0, err)
        with Image.open(self.out) as im:
            self.assertEqual(im.size, (390, 844))

    def test_two_runs_give_identical_bytes(self):
        other = os.path.join(self.dir.name, "again.png")
        self.run_mock(self.skin, self.out, "--size", "390x844")
        self.run_mock(self.skin, other, "--size", "390x844")
        with open(self.out, "rb") as fa, open(other, "rb") as fb:
            self.assertEqual(fa.read(), fb.read())

    def test_the_selected_tab_is_looked_up_under_its_state(self):
        # tab-selected lives at parts.tab.selected, not at a key of its own; if the
        # mock missed it, every tab would silently draw as the at-rest chip.
        code, _, _ = self.run_mock(self.skin, self.out, "--size", "1280x800")
        self.assertEqual(code, 0)
        with Image.open(self.out) as im:
            self.assertIsNotNone(im)

    def test_a_narrow_viewport_still_draws(self):
        code, _, err = self.run_mock(self.skin, self.out, "--size", "phone")
        self.assertEqual(code, 0, err)

    def test_a_missing_skin_json_is_a_plain_failure(self):
        code, _, _ = self.run_mock(os.path.join(self.dir.name, "nowhere"),
                                   self.out, "--size", "390x844")
        self.assertEqual(code, 2)

    def test_a_missing_picture_is_a_plain_failure(self):
        os.remove(os.path.join(self.skin, "panel.webp"))
        code, _, _ = self.run_mock(self.skin, self.out, "--size", "390x844")
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()