#!/usr/bin/env python3
"""Tests for art/tools/process_tiles.py.

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

TOOL_PATH = Path(__file__).resolve().parents[1] / "tools" / "process_tiles.py"
_spec = importlib.util.spec_from_file_location("process_tiles_tool", TOOL_PATH)
process_tiles = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(process_tiles)

TILE = 16


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(TOOL_PATH), *args],
        capture_output=True, text=True)


class ParseGridTests(unittest.TestCase):
    def test_good_spec(self):
        self.assertEqual(process_tiles.parse_grid("3x3"), (3, 3))

    def test_bad_spec_exits_two(self):
        with self.assertRaises(SystemExit) as cm:
            process_tiles.parse_grid("3")
        self.assertEqual(cm.exception.code, 2)


class ProcessTilesTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def save(self, im, name):
        path = self.dir / name
        im.save(path)
        return path

    def test_output_is_exactly_grid_times_tile(self):
        src = self.save(Image.new("RGB", (100, 70), (90, 70, 50)), "wide.png")
        out = self.dir / "tile.png"
        result = run_cli(str(src), str(out), "--grid", "3x3", "--tile", str(TILE))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with Image.open(out) as im:
            self.assertEqual(im.size, (3 * TILE, 3 * TILE))

    def test_output_is_fully_opaque(self):
        im = Image.new("RGBA", (80, 60), (200, 100, 50, 255))
        for corner in ((0, 0), (79, 0), (0, 59), (79, 59)):
            im.putpixel(corner, (0, 0, 0, 0))
        src = self.save(im, "holed.png")
        out = self.dir / "tile.png"
        result = run_cli(str(src), str(out), "--grid", "2x2", "--tile", str(TILE))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with Image.open(out) as im:
            alpha = im.convert("RGBA").getchannel("A")
        self.assertEqual(alpha.getextrema(), (255, 255))

    def test_centre_crop_keeps_the_middle_square(self):
        im = Image.new("RGB", (200, 100), (200, 50, 50))
        middle = Image.new("RGB", (100, 100), (30, 120, 60))
        im.paste(middle, (50, 0))  # the largest centred square is exactly this patch
        src = self.save(im, "wide.png")
        out = self.dir / "tile.png"
        result = run_cli(str(src), str(out), "--grid", "2x2", "--tile", str(TILE))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with Image.open(out) as im:
            rgb = im.convert("RGB")
            self.assertEqual(rgb.getpixel((0, 0)), (30, 120, 60))
            self.assertEqual(rgb.getpixel((TILE - 1, TILE - 1)), (30, 120, 60))

    def test_bad_grid_exits_two(self):
        src = self.save(Image.new("RGB", (40, 40), (10, 10, 10)), "in.png")
        result = run_cli(str(src), str(self.dir / "out.png"), "--grid", "3")
        self.assertEqual(result.returncode, 2)
        self.assertIn("COLSxROWS", result.stderr)

    def test_zero_grid_exits_two(self):
        src = self.save(Image.new("RGB", (40, 40), (10, 10, 10)), "in.png")
        result = run_cli(str(src), str(self.dir / "out.png"), "--grid", "0x3")
        self.assertEqual(result.returncode, 2)

    def test_missing_input_exits_two(self):
        result = run_cli(str(self.dir / "nope.png"), str(self.dir / "out.png"),
                         "--grid", "3x3")
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot read", result.stderr)

    def test_unsupported_output_suffix_exits_two(self):
        src = self.save(Image.new("RGB", (40, 40), (10, 10, 10)), "in.png")
        result = run_cli(str(src), str(self.dir / "out.gif"), "--grid", "3x3")
        self.assertEqual(result.returncode, 2)
        self.assertIn(".png or .webp", result.stderr)

    def test_help_exits_zero(self):
        result = run_cli("--help")
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
