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

    def test_uneven_grid_exits_2(self):
        with tempfile.TemporaryDirectory() as d:
            sheet = os.path.join(d, "sheet.png")
            flat(40, 30).save(sheet)                       # 40 does not divide by 3
            with self.assertRaises(SystemExit) as cm:
                ps.main(["--grid", "3x2", sheet, os.path.join(d, "out"), "hero",
                         "--size", "32"])
            self.assertEqual(cm.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
