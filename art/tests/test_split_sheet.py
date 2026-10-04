#!/usr/bin/env python3
"""Tests for art/tools/split_sheet.py.

Only synthetic Pillow images are used, in a TemporaryDirectory. No network and
no files from art/source/. The CLI is driven with subprocess to check exit codes.
"""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

TOOL_PATH = Path(__file__).resolve().parents[1] / "tools" / "split_sheet.py"
_spec = importlib.util.spec_from_file_location("split_sheet_tool", TOOL_PATH)
split_sheet = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(split_sheet)

GROUND = (216, 215, 213)     # the light neutral grey the pieces stand on
MOSS = (176, 92, 46)         # saturated piece colours: nothing like the ground
BLUE = (64, 110, 176)
OLIVE = (150, 140, 60)
SPECK = (200, 40, 40)        # the colour a stray speck is drawn in


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(TOOL_PATH), *args],
        capture_output=True, text=True)


def paint(im, box, colour):
    """Fill box (left, top, right, bottom) with one colour, hard edges."""
    for x in range(box[0], box[2]):
        for y in range(box[1], box[3]):
            im.putpixel((x, y), colour)


def uneven_ground(width, height):
    """A grey ground that is slightly uneven and slightly warm."""
    im = Image.new("RGB", (width, height))
    for y in range(height):
        for x in range(width):
            v = 210 + ((x * 7 + y * 3) % 13)
            im.putpixel((x, y), (v, v - 1, v - 3))
    return im


def soft_shadow(im, rect, past, depth=8):
    """A neutral grey shadow in rect: darkest at the piece's edge (past), fading to the ground."""
    left, top, right, bottom = rect
    for y in range(top, bottom):
        for x in range(left, right):
            d = max(x - past[0], y - past[1], 0)
            v = round(176 + (GROUND[0] - 176) * min(d, depth) / depth)
            im.putpixel((x, y), (v, v, v))


def disc(im, cx, cy, r, colour):
    """A hard-edged disc."""
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                im.putpixel((x, y), colour)


class FailTests(unittest.TestCase):
    def test_fail_is_a_plain_exit_two(self):
        with self.assertRaises(SystemExit) as cm:
            split_sheet.fail("a thing went wrong")
        self.assertEqual(cm.exception.code, 2)


class FindPiecesTests(unittest.TestCase):
    def test_pieces_come_back_in_reading_order(self):
        sheet = Image.new("RGB", (60, 40), GROUND)
        paint(sheet, (30, 5, 50, 20), BLUE)   # top right
        paint(sheet, (5, 25, 25, 38), OLIVE)  # bottom left
        paint(sheet, (5, 5, 20, 20), MOSS)    # top left
        mask = split_sheet.piece_mask(sheet.convert("RGBA"), 14)
        pieces, owner = split_sheet.find_pieces(mask, 60, 40, 64)
        self.assertEqual([p[:4] for p in pieces],
                         [(5, 5, 20, 20), (30, 5, 50, 20), (5, 25, 25, 38)])
        self.assertEqual(len(owner), 60 * 40)


class SplitSheetTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def save(self, im, name):
        path = self.dir / name
        im.save(path)
        return path

    def cut(self, src, *extra):
        """Run the CLI on src into a fresh directory and return (result, outdir)."""
        out = self.dir / "cut"
        return run_cli(str(src), str(out), *extra), out

    def written(self, out):
        return sorted(p.name for p in out.iterdir())

    def test_several_pieces_come_back_as_several_pictures(self):
        sheet = Image.new("RGB", (160, 100), GROUND)
        paint(sheet, (10, 10, 50, 40), MOSS)
        paint(sheet, (70, 10, 110, 40), BLUE)
        paint(sheet, (10, 60, 40, 90), OLIVE)
        result, out = self.cut(self.save(sheet, "sheet.png"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.written(out),
                         ["piece-1.png", "piece-2.png", "piece-3.png"])
        for name, size, colour in (("piece-1.png", (40, 30), MOSS),
                                   ("piece-2.png", (40, 30), BLUE),
                                   ("piece-3.png", (30, 30), OLIVE)):
            with Image.open(out / name) as im:
                self.assertEqual(im.size, size, name)
                self.assertEqual(im.convert("RGB").getpixel((0, 0)), colour, name)

    def test_names_run_left_to_right_then_top_to_bottom(self):
        sheet = Image.new("RGB", (160, 100), GROUND)
        paint(sheet, (10, 10, 50, 40), MOSS)    # top left
        paint(sheet, (70, 10, 110, 40), BLUE)   # top right
        paint(sheet, (10, 60, 40, 90), OLIVE)   # below
        result, out = self.cut(self.save(sheet, "sheet.png"),
                               "--names", "panel,button,cursor")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.written(out),
                         ["button.png", "cursor.png", "panel.png"])
        for name, colour in (("panel.png", MOSS),
                             ("button.png", BLUE),
                             ("cursor.png", OLIVE)):
            with Image.open(out / name) as im:
                self.assertEqual(im.convert("RGB").getpixel((0, 0)), colour, name)

    def test_a_piece_touching_the_edge_comes_back_whole(self):
        sheet = Image.new("RGB", (60, 50), GROUND)
        paint(sheet, (0, 0, 25, 18), BLUE)      # touches the left and top edges
        result, out = self.cut(self.save(sheet, "edge.png"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with Image.open(out / "piece-1.png") as im:
            self.assertEqual(im.size, (25, 18))
            rgb = im.convert("RGB")
            self.assertEqual(rgb.getpixel((0, 0)), BLUE)
            self.assertEqual(rgb.getpixel((24, 17)), BLUE)

    def test_the_grey_ground_is_gone_from_the_saved_picture(self):
        sheet = Image.new("RGB", (80, 60), GROUND)
        paint(sheet, (10, 10, 60, 50), MOSS)
        result, out = self.cut(self.save(sheet, "sheet.png"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with Image.open(out / "piece-1.png") as im:
            for r, g, b in im.convert("RGB").getdata():
                self.assertGreater(max(r, g, b) - min(r, g, b), 14,
                                   "a grey ground pixel is left in the picture")

    def test_the_crop_is_tight_around_the_piece(self):
        sheet = uneven_ground(80, 60)           # the ground is slightly uneven
        paint(sheet, (10, 12, 40, 42), MOSS)
        result, out = self.cut(self.save(sheet, "uneven.png"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with Image.open(out / "piece-1.png") as im:
            self.assertEqual(im.size, (30, 30))  # exactly the piece, no margin
            self.assertEqual(im.convert("RGB").getpixel((0, 0)), MOSS)

    def test_a_plain_rgb_sheet_is_saved_as_rgb(self):
        sheet = Image.new("RGB", (80, 60), GROUND)
        paint(sheet, (20, 15, 60, 45), MOSS)
        result, out = self.cut(self.save(sheet, "rgb.png"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with Image.open(out / "piece-1.png") as im:
            self.assertEqual(im.mode, "RGB")

    def test_a_sheet_with_alpha_keeps_the_piece_alpha(self):
        sheet = Image.new("RGBA", (80, 60), GROUND + (255,))
        paint(sheet, (10, 10, 50, 40), MOSS + (255,))
        paint(sheet, (10, 10, 50, 25), MOSS + (128,))   # the top half is see-through
        result, out = self.cut(self.save(sheet, "alpha.png"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with Image.open(out / "piece-1.png") as im:
            self.assertEqual(im.mode, "RGBA")
            self.assertEqual(im.getpixel((10, 5)), MOSS + (128,))
            self.assertEqual(im.getpixel((10, 25)), MOSS + (255,))

    def test_specks_are_dropped(self):
        sheet = Image.new("RGB", (160, 100), GROUND)
        paint(sheet, (10, 10, 50, 40), MOSS)
        paint(sheet, (70, 50, 110, 80), BLUE)
        paint(sheet, (60, 15, 61, 16), SPECK)   # a 1-pixel speck
        paint(sheet, (60, 45, 62, 47), SPECK)   # 4 pixels
        paint(sheet, (60, 20, 63, 23), SPECK)   # 9 pixels
        result, out = self.cut(self.save(sheet, "specks.png"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.written(out),
                         ["piece-1.png", "piece-2.png"])

    def test_a_shadow_is_not_its_own_piece_and_stays_out_of_the_crop(self):
        sheet = Image.new("RGB", (120, 80), GROUND)
        soft_shadow(sheet, (34, 24, 74, 54), past=(70, 50))
        paint(sheet, (30, 20, 70, 50), MOSS)    # the piece sits on its shadow
        result, out = self.cut(self.save(sheet, "shadow.png"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.written(out), ["piece-1.png"])   # the shadow is not a piece
        with Image.open(out / "piece-1.png") as im:
            self.assertEqual(im.size, (40, 30))  # the shadow is not in the box
            self.assertEqual(im.mode, "RGB")
            for r, g, b in im.convert("RGB").getdata():
                self.assertEqual((r, g, b), MOSS, "a grey fringe is left around the crop")

    def test_a_shadow_inside_the_crop_is_keyed_out(self):
        sheet = Image.new("RGB", (80, 80), GROUND)
        disc(sheet, 34, 34, 14, (176, 176, 176))  # a shadow showing in the box's corners
        disc(sheet, 30, 30, 14, MOSS)
        result, out = self.cut(self.save(sheet, "round.png"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.written(out), ["piece-1.png"])
        with Image.open(out / "piece-1.png") as im:
            self.assertEqual(im.size, (29, 29))   # the round piece's own box
            self.assertEqual(im.mode, "RGBA")
            self.assertEqual(im.getpixel((14, 14)), MOSS + (255,))  # the middle
            self.assertEqual(im.getpixel((0, 0))[3], 0)             # ground in the corner
            self.assertEqual(im.getpixel((27, 27))[3], 0)           # the shadow in the corner
            for r, g, b, a in im.getdata():
                if a:
                    self.assertGreater(max(r, g, b) - min(r, g, b), 14,
                                       "a grey pixel is left opaque in the picture")

    def test_uneven_ground_still_splits(self):
        sheet = uneven_ground(90, 70)
        paint(sheet, (10, 12, 40, 42), MOSS)
        paint(sheet, (50, 20, 75, 50), BLUE)
        result, out = self.cut(self.save(sheet, "uneven2.png"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.written(out), ["piece-1.png", "piece-2.png"])
        with Image.open(out / "piece-1.png") as im:
            self.assertEqual(im.size, (30, 30))
        with Image.open(out / "piece-2.png") as im:
            self.assertEqual(im.size, (25, 30))

    def test_a_margin_keeps_a_transparent_ring(self):
        sheet = Image.new("RGB", (80, 60), GROUND)
        paint(sheet, (20, 15, 60, 45), MOSS)
        result, out = self.cut(self.save(sheet, "margin.png"), "--margin", "2")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with Image.open(out / "piece-1.png") as im:
            self.assertEqual(im.size, (44, 34))
            self.assertEqual(im.mode, "RGBA")
            self.assertEqual(im.getpixel((0, 0))[3], 0)      # the kept ground is clear
            self.assertEqual(im.getpixel((22, 17)), MOSS + (255,))

    def test_a_sheet_of_plain_ground_fails_with_one_plain_line(self):
        src = self.save(Image.new("RGB", (60, 40), GROUND), "ground.png")
        result, _ = self.cut(src)
        self.assertEqual(result.returncode, 2)
        lines = [ln for ln in result.stderr.splitlines() if ln.strip()]
        self.assertEqual(len(lines), 1, result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("no pieces", lines[0])

    def test_a_missing_path_fails_with_one_plain_line(self):
        result, _ = self.cut(self.dir / "nope.png")
        self.assertEqual(result.returncode, 2)
        lines = [ln for ln in result.stderr.splitlines() if ln.strip()]
        self.assertEqual(len(lines), 1, result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("cannot read", lines[0])

    def test_a_wrong_number_of_names_fails_with_one_plain_line(self):
        sheet = Image.new("RGB", (160, 100), GROUND)
        paint(sheet, (10, 10, 50, 40), MOSS)
        paint(sheet, (70, 10, 110, 40), BLUE)
        paint(sheet, (10, 60, 40, 90), OLIVE)
        result, _ = self.cut(self.save(sheet, "sheet.png"), "--names", "one,two")
        self.assertEqual(result.returncode, 2)
        lines = [ln for ln in result.stderr.splitlines() if ln.strip()]
        self.assertEqual(len(lines), 1, result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("--names", lines[0])

    def test_the_same_sheet_gives_the_same_pictures(self):
        sheet = Image.new("RGB", (160, 100), GROUND)
        paint(sheet, (10, 10, 50, 40), MOSS)
        paint(sheet, (70, 10, 110, 40), BLUE)
        paint(sheet, (10, 60, 40, 90), OLIVE)
        src = self.save(sheet, "sheet.png")
        first, out1 = self.cut(src)
        second, out2 = run_cli(str(src), str(self.dir / "cut2")), self.dir / "cut2"
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        names1 = self.written(out1)
        self.assertEqual(names1, self.written(out2))
        for name in names1:
            self.assertEqual((out1 / name).read_bytes(), (out2 / name).read_bytes(),
                             name)

    def test_help_exits_zero_and_explains_the_flags(self):
        result = run_cli("--help")
        self.assertEqual(result.returncode, 0)
        for flag in ("--names", "--min-area", "--neutral", "--margin"):
            self.assertIn(flag, result.stdout)


if __name__ == "__main__":
    unittest.main()
