#!/usr/bin/env python3
"""Tests for art/tools/check_sprites.py.

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

TOOL_PATH = Path(__file__).resolve().parents[1] / "tools" / "check_sprites.py"
_spec = importlib.util.spec_from_file_location("check_sprites_tool", TOOL_PATH)
check_sprites = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_sprites)
check_image = check_sprites.check_image

SIZE = 10
BROWN = (60, 40, 20, 255)


def build(size, points, color=BROWN):
    """A transparent image with the given pixels set to color."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    for x, y in points:
        im.putpixel((x, y), color)
    return im


def block(x0, y0, x1, y1):
    return [(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(TOOL_PATH), *args],
        capture_output=True, text=True)


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

    def test_good_file_has_no_problems(self):
        path = self.save(build(SIZE, block(3, 3, 6, 6)), "good.png")
        self.assertEqual(check_image(path, SIZE), [])

    def test_wrong_size(self):
        path = self.save(build(5, block(1, 1, 3, 3)), "small.png")
        self.assertEqual(check_image(path, SIZE), ["wrong size (5x5, expected 10x10)"])

    def test_no_transparency(self):
        im = Image.new("RGBA", (SIZE, SIZE), (60, 40, 20, 200))
        path = self.save(im, "opaque.png")
        problems = check_image(path, SIZE)
        self.assertIn("no transparency", problems)

    def test_opaque_pixels_touching_the_edge(self):
        path = self.save(build(SIZE, [(9, y) for y in range(2, 8)]), "edge.png")
        self.assertEqual(check_image(path, SIZE), ["opaque pixels touching the edge"])

    def test_feet_on_the_bottom_row_are_fine(self):
        path = self.save(build(SIZE, block(3, 4, 6, 9)), "feet.png")  # rows 4..9: touches the bottom row
        self.assertEqual(check_image(path, SIZE), [])

    def test_opaque_pixels_touching_the_top_edge(self):
        path = self.save(build(SIZE, block(3, 0, 6, 5)), "top.png")
        self.assertEqual(check_image(path, SIZE), ["opaque pixels touching the edge"])

    def test_pure_black_pixel(self):
        im = build(SIZE, block(3, 3, 6, 6))
        im.putpixel((4, 4), (0, 0, 0, 255))
        path = self.save(im, "black.png")
        self.assertEqual(check_image(path, SIZE), ["a pure black pixel (1 of them)"])

    def test_too_empty(self):
        path = self.save(build(SIZE, [(4, 4), (5, 5)]), "empty.png")
        self.assertEqual(check_image(path, SIZE), ["too empty (2.0% opaque)"])

    def test_exactly_at_empty_bound_is_fine(self):
        path = self.save(build(SIZE, [(4, 4), (5, 5), (6, 6)]), "bound_low.png")
        self.assertEqual(check_image(path, SIZE), [])

    def test_too_full(self):
        im = Image.new("RGBA", (SIZE, SIZE), (60, 40, 20, 254))
        for x, y in [(4, 4), (5, 4), (4, 5), (5, 5)]:
            im.putpixel((x, y), (0, 0, 0, 0))
        path = self.save(im, "full.png")
        self.assertEqual(check_image(path, SIZE), ["too full (96.0% opaque)"])

    def test_exactly_at_full_bound_is_fine(self):
        im = Image.new("RGBA", (SIZE, SIZE), (60, 40, 20, 254))
        for x, y in [(4, 4), (5, 4), (6, 4), (4, 5), (5, 5)]:
            im.putpixel((x, y), (0, 0, 0, 0))
        path = self.save(im, "bound_high.png")
        self.assertEqual(check_image(path, SIZE), [])


class CliTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def good(self, name="good.png"):
        path = self.dir / name
        build(SIZE, block(3, 3, 6, 6)).save(path)
        return path

    def bad(self, name="bad.png"):
        path = self.dir / name
        build(SIZE, [(9, y) for y in range(2, 8)]).save(path)
        return path

    def test_all_good_exits_zero(self):
        self.good()
        result = run_cli(str(self.dir), "--size", str(SIZE))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ok ", result.stdout)

    def test_any_problem_exits_one(self):
        self.good()
        self.bad()
        result = run_cli(str(self.dir), "--size", str(SIZE))
        self.assertEqual(result.returncode, 1)
        self.assertIn("opaque pixels touching the edge", result.stdout)

    def test_directory_argument_checks_only_png(self):
        self.good()
        self.bad()
        (self.dir / "notes.txt").write_text("ignore me")
        (self.dir / "nested").mkdir()
        build(SIZE, block(3, 3, 6, 6)).save(self.dir / "nested" / "deep.png")
        result = run_cli(str(self.dir), "--size", str(SIZE))
        self.assertIn("good.png", result.stdout)
        self.assertIn("bad.png", result.stdout)
        self.assertNotIn("notes.txt", result.stdout)
        self.assertNotIn("deep.png", result.stdout)

    def test_single_file_argument(self):
        path = self.good()
        result = run_cli(str(path), "--size", str(SIZE))
        self.assertEqual(result.returncode, 0)
        self.assertIn("ok ", result.stdout)

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
