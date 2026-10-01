#!/usr/bin/env python3
"""Tests for process_sprites.py, built from synthetic Pillow images only."""
import os
import sys
import tempfile
import unittest

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
import process_sprites as ps

BACKGROUND = (210, 60, 60)
SUBJECT = (30, 90, 200)


def flat(width, height, colour=BACKGROUND):
    return Image.new("RGB", (width, height), colour)


def paint(img, box, colour=SUBJECT):
    for x in range(box[0], box[2]):
        for y in range(box[1], box[3]):
            img.putpixel((x, y), colour)


class BackgroundTest(unittest.TestCase):
    def test_flat_background_becomes_transparent(self):
        img = flat(40, 40)
        paint(img, (10, 10, 30, 30))
        out = ps.remove_background(img, tolerance=0)
        for corner in ((0, 0), (39, 0), (0, 39), (39, 39)):
            self.assertEqual(out.getpixel(corner)[3], 0)
        self.assertEqual(out.getpixel((0, 20))[3], 0)      # an edge pixel
        self.assertEqual(out.getpixel((20, 20))[3], 255)   # the subject

    def test_hole_inside_subject_stays_opaque(self):
        img = flat(40, 40)
        paint(img, (5, 5, 35, 35))
        paint(img, (15, 15, 25, 25), BACKGROUND)           # enclosed hole
        out = ps.remove_background(img, tolerance=0)
        self.assertEqual(out.getpixel((20, 20))[3], 255)   # the hole stays
        self.assertEqual(out.getpixel((8, 20))[3], 255)    # the subject ring stays
        self.assertEqual(out.getpixel((0, 0))[3], 0)       # outside goes


class FitTest(unittest.TestCase):
    def test_output_is_exactly_size(self):
        img = flat(40, 40)
        paint(img, (10, 5, 30, 35))
        out = ps.process_one(img, size=64, tolerance=0)
        self.assertEqual(out.size, (64, 64))

    def test_content_is_bottom_aligned_and_centred(self):
        img = flat(40, 40)
        paint(img, (15, 5, 25, 35))                        # 10 wide, 30 tall
        out = ps.process_one(img, size=128, tolerance=0)
        self.assertEqual(out.size, (128, 128))
        bbox = out.getchannel("A").getbbox()
        self.assertEqual(bbox[3], 128)                     # bottom row is the last row
        self.assertEqual(bbox[0], 128 - bbox[2])           # left and right margins match


class GridTest(unittest.TestCase):
    def _sheet(self, path):
        img = flat(40, 40)
        for cx, cy in ((0, 0), (20, 0), (0, 20), (20, 20)):
            paint(img, (cx + 5, cy + 5, cx + 15, cy + 15))
        img.save(path)

    def test_grid_makes_cols_times_rows_files_with_right_names(self):
        with tempfile.TemporaryDirectory() as d:
            sheet = os.path.join(d, "sheet.png")
            self._sheet(sheet)
            outdir = os.path.join(d, "named")
            rc = ps.main(["--grid", "2x2", sheet, outdir, "hero",
                          "--size", "32", "--names", "down,left"])
            self.assertEqual(rc, 0)
            self.assertEqual(sorted(os.listdir(outdir)),
                             ["hero_down_1.png", "hero_down_2.png",
                              "hero_left_1.png", "hero_left_2.png"])
            outdir = os.path.join(d, "default")
            rc = ps.main(["--grid", "2x2", sheet, outdir, "hero", "--size", "32"])
            self.assertEqual(rc, 0)
            self.assertEqual(sorted(os.listdir(outdir)),
                             ["hero_r1_1.png", "hero_r1_2.png",
                              "hero_r2_1.png", "hero_r2_2.png"])

    def test_uneven_grid_is_cut_on_rounded_edges_with_a_note(self):
        with tempfile.TemporaryDirectory() as d:
            sheet = os.path.join(d, "sheet.png")
            im = flat(40, 30)                              # 40 does not divide by 3
            for cx in (7, 20, 33):                         # a subject in each of the 6 cells
                for cy in (7, 22):
                    paint(im, (cx - 3, cy - 3, cx + 3, cy + 3))
            im.save(sheet)
            outdir = os.path.join(d, "out")
            self.assertEqual(ps.main(["--grid", "3x2", sheet, outdir, "hero", "--size", "32"]), 0)
            self.assertEqual(len(os.listdir(outdir)), 6)

    def test_a_sheet_smaller_than_the_grid_exits_2(self):
        with tempfile.TemporaryDirectory() as d:
            sheet = os.path.join(d, "sheet.png")
            flat(2, 30).save(sheet)                        # 2 columns of pixels cannot make 3 cells
            with self.assertRaises(SystemExit) as cm:
                ps.main(["--grid", "3x2", sheet, os.path.join(d, "out"), "hero", "--size", "32"])
            self.assertEqual(cm.exception.code, 2)


class MarginTest(unittest.TestCase):
    def test_a_full_height_subject_never_touches_the_top_or_sides(self):
        img = flat(64, 64)
        paint(img, (0, 0, 64, 64))                         # a subject that fills the whole picture
        img.putpixel((0, 0), BACKGROUND)                   # corners stay background so the cut-out has an edge to flood from
        for corner in ((63, 0), (0, 63), (63, 63)):
            img.putpixel(corner, BACKGROUND)
        out = ps.process_one(img, 128, 28)
        a = out.getchannel("A")
        w, h = out.size
        self.assertEqual(a.crop((0, 0, w, 1)).getbbox(), None)     # top row empty
        self.assertEqual(a.crop((0, 0, 1, h)).getbbox(), None)     # left column empty
        self.assertEqual(a.crop((w - 1, 0, w, h)).getbbox(), None) # right column empty
        self.assertIsNotNone(a.crop((0, h - 1, w, h)).getbbox())   # feet still on the bottom row


class CheckerboardTest(unittest.TestCase):
    def _checker_sheet(self):
        im = Image.new("RGB", (80, 80), (255, 255, 255))
        for y in range(80):
            for x in range(80):
                if ((x // 6) + (y // 6)) % 2:
                    im.putpixel((x, y), (204, 204, 204))
        for x in range(28, 52):
            for y in range(20, 70):
                im.putpixel((x, y), (140, 70, 40))        # the subject
        return im

    def test_a_drawn_checkerboard_background_is_cleared(self):
        out = ps.process_one(self._checker_sheet(), 64, 28)
        a = out.getchannel("A")
        opaque = sum(1 for v in a.getdata() if v > 0)
        total = 64 * 64
        # only the subject remains: well under half the canvas, and the corners are clear
        self.assertLess(opaque, total * 0.5)
        for corner in ((0, 0), (63, 0), (0, 40)):
            self.assertEqual(a.getpixel(corner), 0)

    def test_a_plain_light_background_still_works(self):
        im = Image.new("RGB", (80, 80), (255, 255, 255))
        for x in range(28, 52):
            for y in range(20, 70):
                im.putpixel((x, y), (140, 70, 40))
        out = ps.process_one(im, 64, 28)
        self.assertEqual(out.getchannel("A").getpixel((0, 0)), 0)


class HoleTest(unittest.TestCase):
    def _ring(self):
        im = Image.new("RGB", (80, 80), (250, 250, 250))                 # light background
        for y in range(15, 65):
            for x in range(15, 65):
                im.putpixel((x, y), (180, 120, 40))                       # a gold square...
        for y in range(30, 50):
            for x in range(30, 50):
                im.putpixel((x, y), (250, 250, 250))                      # ...with a background-coloured hole
        return im

    def test_an_enclosed_hole_stays_by_default(self):
        out = ps.process_one(self._ring(), 64, 28)
        a = out.getchannel("A")
        self.assertGreater(a.getpixel((32, 40)), 0)                       # the hole is still opaque

    def test_clear_holes_removes_the_hole_but_keeps_the_ring(self):
        out = ps.process_one(self._ring(), 64, 28, holes=True)
        a = out.getchannel("A")
        self.assertEqual(a.getpixel((32, 40)), 0)                         # the hole is clear
        self.assertGreater(a.getpixel((8, 40)), 0)                        # the gold band is not


if __name__ == "__main__":
    unittest.main()
