#!/usr/bin/env python3
"""Tests for art/tools/pixel_downscale.py.

Only synthetic Pillow images and a tiny generated palette are used, in a
TemporaryDirectory. No network, no art/source/ files, and no real palette: the
tool must not hard-code one. The CLI is driven with subprocess for exit codes.
"""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

TOOL_PATH = Path(__file__).resolve().parents[1] / "tools" / "pixel_downscale.py"
_spec = importlib.util.spec_from_file_location("pixel_downscale_tool", TOOL_PATH)
pixel_downscale = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pixel_downscale)


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(TOOL_PATH), *args],
        capture_output=True, text=True)


class DownscaleTests(unittest.TestCase):
    def test_block_output_is_exactly_the_target(self):
        src = Image.new("RGBA", (64, 64), (10, 20, 30, 255))
        out = pixel_downscale.downscale(src, block=8)
        self.assertEqual(out.size, (8, 8))

    def test_height_output_is_exactly_the_target(self):
        src = Image.new("RGBA", (64, 96), (10, 20, 30, 255))
        out = pixel_downscale.downscale(src, height=48)
        self.assertEqual(out.size, (32, 48))  # width follows the 64:96 aspect

    def test_non_square_source_keeps_aspect_in_height_mode(self):
        src = Image.new("RGBA", (100, 40), (1, 2, 3, 255))
        out = pixel_downscale.downscale(src, height=10)
        self.assertEqual(out.size, (25, 10))

    def test_2x2_block_of_distinct_colours_yields_one_source_colour(self):
        colours = [(255, 0, 0, 255), (0, 255, 0, 255),
                   (0, 0, 255, 255), (255, 255, 0, 255)]
        src = Image.new("RGBA", (2, 2))
        for i, c in enumerate(colours):
            src.putpixel((i % 2, i // 2), c)
        out = pixel_downscale.downscale(src, block=1)
        self.assertEqual(out.size, (1, 1))
        got = out.getpixel((0, 0))
        self.assertIn(got, colours)          # no new colour made
        self.assertEqual(got, colours[3])    # the block centre, bottom right

    def test_block_sampling_never_invents_a_colour(self):
        # Four flat 2x2 blocks; each output pixel must be one of the four.
        colours = [(200, 0, 0, 255), (0, 200, 0, 255),
                   (0, 0, 200, 255), (200, 200, 0, 255)]
        src = Image.new("RGBA", (4, 4))
        for by in range(2):
            for bx in range(2):
                c = colours[by * 2 + bx]
                for y in range(by * 2, by * 2 + 2):
                    for x in range(bx * 2, bx * 2 + 2):
                        src.putpixel((x, y), c)
        out = pixel_downscale.downscale(src, block=2)
        self.assertEqual(out.size, (2, 2))
        seen = {out.getpixel((x, y)) for y in range(2) for x in range(2)}
        self.assertTrue(seen.issubset(set(colours)))
        self.assertEqual(len(seen), 4)       # all four blocks kept

    def test_averaging_would_show_but_does_not(self):
        # Two-colour 2x2 block: a blend would be a third colour, a centre sample
        # is exactly (0, 0, 255), one of the two.
        src = Image.new("RGBA", (2, 2), (255, 255, 255, 255))
        src.putpixel((1, 1), (0, 0, 255, 255))
        out = pixel_downscale.downscale(src, block=1)
        self.assertEqual(out.getpixel((0, 0)), (0, 0, 255, 255))

    def test_alpha_is_preserved(self):
        # 4x4, alphas 10, 20, 30, 40 at the centre of each 2x2 block.
        src = Image.new("RGBA", (4, 4), (50, 60, 70, 255))
        want = {}
        for by in range(2):
            for bx in range(2):
                a = 10 * (by * 2 + bx + 1)
                src.putpixel((bx * 2 + 1, by * 2 + 1), (50, 60, 70, a))
                want[(bx, by)] = a
        out = pixel_downscale.downscale(src, block=2)
        for (bx, by), a in want.items():
            self.assertEqual(out.getpixel((bx, by)), (50, 60, 70, a))

    def test_exactly_one_of_block_or_height(self):
        src = Image.new("RGBA", (8, 8), (1, 1, 1, 255))
        with self.assertRaises(ValueError):
            pixel_downscale.downscale(src)
        with self.assertRaises(ValueError):
            pixel_downscale.downscale(src, block=2, height=4)

    def test_zero_target_is_refused(self):
        src = Image.new("RGBA", (8, 8), (1, 1, 1, 255))
        with self.assertRaises(ValueError):
            pixel_downscale.downscale(src, block=0)
        with self.assertRaises(ValueError):
            pixel_downscale.downscale(src, height=0)


class PaletteLockTests(unittest.TestCase):
    PALETTE = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)]

    def test_lock_maps_only_to_palette_entries(self):
        src = Image.new("RGBA", (4, 1))
        off = [(250, 10, 12, 255), (12, 240, 8, 255), (9, 9, 250, 255), (30, 30, 30, 255)]
        for x, c in enumerate(off):
            src.putpixel((x, 0), c)
        out = pixel_downscale.lock_palette(src, self.PALETTE)
        for x in range(4):
            rgb = out.getpixel((x, 0))[:3]
            self.assertIn(rgb, self.PALETTE)

    def test_lock_keeps_alpha(self):
        src = Image.new("RGBA", (2, 1))
        src.putpixel((0, 0), (250, 0, 0, 17))
        src.putpixel((1, 0), (0, 0, 0, 0))
        out = pixel_downscale.lock_palette(src, self.PALETTE)
        self.assertEqual(out.getpixel((0, 0))[3], 17)
        self.assertEqual(out.getpixel((1, 0))[3], 0)

    def test_nearest_colour_picks_the_closest(self):
        self.assertEqual(pixel_downscale.nearest_colour((250, 5, 5), self.PALETTE), (255, 0, 0))
        self.assertEqual(pixel_downscale.nearest_colour((5, 5, 250), self.PALETTE), (0, 0, 255))

    def test_downscale_without_palette_skips_the_lock(self):
        src = Image.new("RGBA", (2, 2), (12, 34, 56, 255))
        out = pixel_downscale.downscale(src, block=1)
        self.assertEqual(out.getpixel((0, 0)), (12, 34, 56, 255))

    def test_downscale_with_palette_locks_the_result(self):
        src = Image.new("RGBA", (2, 2), (250, 8, 8, 255))
        out = pixel_downscale.downscale(src, block=1, palette=self.PALETTE)
        self.assertEqual(out.getpixel((0, 0)), (255, 0, 0, 255))


class LoadPaletteTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, name, text):
        path = self.dir / name
        path.write_text(text)
        return path

    def test_json_list_of_hex(self):
        path = self.write("p.json", json.dumps(["#000000", "#ff0000"]))
        self.assertEqual(pixel_downscale.load_palette(path), [(0, 0, 0), (255, 0, 0)])

    def test_json_list_of_rgb_lists(self):
        path = self.write("p.json", json.dumps([[1, 2, 3], [4, 5, 6]]))
        self.assertEqual(pixel_downscale.load_palette(path), [(1, 2, 3), (4, 5, 6)])

    def test_json_dict_with_colors_key_and_objects(self):
        path = self.write("p.json", json.dumps({"colors": [{"r": 9, "g": 8, "b": 7}]}))
        self.assertEqual(pixel_downscale.load_palette(path), [(9, 8, 7)])

    def test_plain_text_lines(self):
        path = self.write("p.txt", "#102030\n40,50,60\n")
        self.assertEqual(pixel_downscale.load_palette(path), [(16, 32, 48), (40, 50, 60)])

    def test_duplicates_are_dropped(self):
        path = self.write("p.json", json.dumps(["#000000", "#000000"]))
        self.assertEqual(pixel_downscale.load_palette(path), [(0, 0, 0)])

    def test_missing_palette_exits_two(self):
        with self.assertRaises(SystemExit) as cm:
            pixel_downscale.load_palette(self.dir / "nope.json")
        self.assertEqual(cm.exception.code, 2)

    def test_empty_palette_exits_two(self):
        path = self.write("p.json", json.dumps([]))
        with self.assertRaises(SystemExit) as cm:
            pixel_downscale.load_palette(path)
        self.assertEqual(cm.exception.code, 2)


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

    def test_block_writes_exact_size(self):
        src = self.save(Image.new("RGBA", (64, 64), (90, 70, 50, 255)), "in.png")
        out = self.dir / "out.png"
        result = run_cli(str(src), str(out), "--block", "16")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with Image.open(out) as im:
            self.assertEqual(im.size, (16, 16))

    def test_height_writes_exact_size(self):
        src = self.save(Image.new("RGBA", (64, 96), (90, 70, 50, 255)), "in.png")
        out = self.dir / "out.png"
        result = run_cli(str(src), str(out), "--height", "48")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with Image.open(out) as im:
            self.assertEqual(im.size, (32, 48))

    def test_palette_flag_locks_colours(self):
        src = self.save(Image.new("RGBA", (4, 4), (250, 8, 8, 255)), "in.png")
        pal = self.dir / "p.json"
        pal.write_text(json.dumps(["#000000", "#ff0000", "#00ff00", "#0000ff"]))
        out = self.dir / "out.png"
        result = run_cli(str(src), str(out), "--block", "2", "--palette", str(pal))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with Image.open(out) as im:
            self.assertEqual(im.convert("RGBA").getpixel((0, 0)), (255, 0, 0, 255))

    def test_neither_target_exits_two(self):
        src = self.save(Image.new("RGBA", (8, 8), (1, 1, 1, 255)), "in.png")
        result = run_cli(str(src), str(self.dir / "out.png"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("--block or --height", result.stderr)

    def test_both_targets_exits_two(self):
        src = self.save(Image.new("RGBA", (8, 8), (1, 1, 1, 255)), "in.png")
        result = run_cli(str(src), str(self.dir / "out.png"), "--block", "2", "--height", "2")
        self.assertEqual(result.returncode, 2)

    def test_bad_output_suffix_exits_two(self):
        src = self.save(Image.new("RGBA", (8, 8), (1, 1, 1, 255)), "in.png")
        result = run_cli(str(src), str(self.dir / "out.gif"), "--block", "2")
        self.assertEqual(result.returncode, 2)
        self.assertIn(".png or .webp", result.stderr)

    def test_missing_input_exits_two(self):
        result = run_cli(str(self.dir / "nope.png"), str(self.dir / "out.png"), "--block", "2")
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot read", result.stderr)

    def test_help_exits_zero(self):
        result = run_cli("--help")
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
