#!/usr/bin/env python3
"""Tests for art/tools/check_tiles.py.

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

TOOL_PATH = Path(__file__).resolve().parents[1] / "tools" / "check_tiles.py"
_spec = importlib.util.spec_from_file_location("check_tiles_tool", TOOL_PATH)
check_tiles = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_tiles)
check_image = check_tiles.check_image

COLS = 3
ROWS = 3
TILE = 16
WIDTH = COLS * TILE
HEIGHT = ROWS * TILE


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(TOOL_PATH), *args],
        capture_output=True, text=True)


def flat(width=WIDTH, height=HEIGHT, colour=(60, 40, 20, 255)):
    """A fully opaque picture of one colour."""
    return Image.new("RGBA", (width, height), colour)


def split(size, split_at, left=(200, 30, 30, 255), right=(30, 60, 200, 255)):
    """A hard two-colour split exactly on a cell edge."""
    im = Image.new("RGBA", (size, size), right)
    for y in range(size):
        for x in range(split_at):
            im.putpixel((x, y), left)
    return im


def gradient(width=WIDTH, height=HEIGHT, low=40, high=240):
    """A smooth two-way gradient, aligned to the cell edges."""
    im = Image.new("RGBA", (width, height))
    span = (width - 1) + (height - 1)
    for y in range(height):
        for x in range(width):
            v = low + round((high - low) * (x + y) / span)
            im.putpixel((x, y), (v, v, v, 255))
    return im


class CheckImageTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def save(self, im, name):
        path = self.dir / name
        im.save(path)
        return path

    def test_exact_size_passes(self):
        path = self.save(flat(), "good.png")
        self.assertEqual(check_image(path, COLS, ROWS, TILE), [])

    def test_wrong_size(self):
        path = self.save(flat(16, 16), "small.png")
        self.assertEqual(check_image(path, COLS, ROWS, TILE),
                         ["wrong size (16x16, expected 48x48)"])

    def test_transparent_pixel(self):
        im = flat()
        im.putpixel((WIDTH // 2, HEIGHT // 2), (0, 0, 0, 0))
        path = self.save(im, "clear.png")
        self.assertEqual(check_image(path, COLS, ROWS, TILE),
                         ["a transparent pixel (1 of them)"])

    def test_pure_black_pixel(self):
        im = flat()
        im.putpixel((WIDTH // 2, HEIGHT // 2), (0, 0, 0, 255))
        path = self.save(im, "black.png")
        self.assertEqual(check_image(path, COLS, ROWS, TILE),
                         ["a pure black pixel (1 of them)"])

    def test_hard_seam_between_cells(self):
        path = self.save(split(2 * TILE, TILE), "seam.png")
        self.assertEqual(check_image(path, 2, 2, TILE),
                         ["visible seam between cells"])

    def test_smooth_gradient_passes(self):
        path = self.save(gradient(), "gradient.png")
        self.assertEqual(check_image(path, COLS, ROWS, TILE), [])


class CliTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def save(self, im, name):
        path = self.dir / name
        im.save(path)
        return path

    def test_all_good_exits_zero(self):
        self.save(flat(), "a.png")
        self.save(gradient(), "b.png")
        result = run_cli(str(self.dir), "--grid", "3x3", "--tile", str(TILE))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ok ", result.stdout)

    def test_problem_exits_one_with_a_seam_line(self):
        path = self.save(split(2 * TILE, TILE), "seam.png")
        result = run_cli(str(path), "--grid", "2x2", "--tile", str(TILE))
        self.assertEqual(result.returncode, 1)
        self.assertIn("visible seam between cells", result.stdout)

    def test_gradient_file_passes(self):
        path = self.save(gradient(), "gradient.png")
        result = run_cli(str(path), "--grid", "3x3", "--tile", str(TILE))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ok ", result.stdout)

    def test_directory_checks_only_image_files(self):
        self.save(flat(), "good.png")
        (self.dir / "notes.txt").write_text("ignore me")
        (self.dir / "nested").mkdir()
        flat().save(self.dir / "nested" / "deep.png")
        result = run_cli(str(self.dir), "--grid", "3x3", "--tile", str(TILE))
        self.assertIn("good.png", result.stdout)
        self.assertNotIn("notes.txt", result.stdout)
        self.assertNotIn("deep.png", result.stdout)

    def test_default_grid_and_tile(self):
        self.save(flat(288, 288), "big.png")
        result = run_cli(str(self.dir))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_path_exits_two(self):
        result = run_cli(str(self.dir / "nope.png"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("no such file or directory", result.stderr)

    def test_no_arguments_exits_two(self):
        result = run_cli()
        self.assertEqual(result.returncode, 2)

    def test_help_exits_zero(self):
        result = run_cli("--help")
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
