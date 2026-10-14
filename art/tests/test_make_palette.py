#!/usr/bin/env python3
"""Tests for art/tools/make_palette.py.

Synthetic Pillow pictures in a TemporaryDirectory drive the generator; the
committed art/palette.json is checked against the shipped pictures it covers.
No network. The CLI is driven with subprocess to check exit codes.
"""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[2]
TOOL_PATH = REPO / "art" / "tools" / "make_palette.py"
PALETTE_PATH = REPO / "art" / "palette.json"
PACK = REPO / "worlds" / "cottage-of-the-breeze"

_spec = importlib.util.spec_from_file_location("make_palette_tool", TOOL_PATH)
make_palette = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(make_palette)

_downscale_spec = importlib.util.spec_from_file_location(
    "pixel_downscale_tool", REPO / "art" / "tools" / "pixel_downscale.py")
pixel_downscale = importlib.util.module_from_spec(_downscale_spec)
_downscale_spec.loader.exec_module(pixel_downscale)


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-W", "ignore", str(TOOL_PATH), *args],
        capture_output=True, text=True)


def picture(path, colours, size=4):
    """A small opaque lossless picture, one colour per row."""
    im = Image.new("RGBA", (size, len(colours)), (0, 0, 0, 255))
    for y, colour in enumerate(colours):
        for x in range(size):
            im.putpixel((x, y), colour)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, lossless=True)
    return path


def synthetic_pack(root):
    """A pack-shaped tree with one locked picture, one cast picture, one painting."""
    picture(root / "props" / "pond.webp", [(20, 60, 40, 255), (200, 180, 120, 255)])
    picture(root / "tiles" / "way-stairs-up.webp", [(20, 60, 40, 255), (90, 60, 30, 255)])
    picture(root / "sprites" / "bird-feather.webp", [(200, 180, 120, 255)])
    picture(root / "sprites" / "hero-sheet.webp", [(1, 2, 3, 255), (250, 240, 230, 255)])
    picture(root / "assets" / "title.webp", [(9, 8, 7, 255), (250, 240, 230, 255)])
    return root


class RampTests(unittest.TestCase):
    def test_ramp_size_is_inside_the_decision(self):
        low, high = make_palette.RAMP_SIZE
        self.assertTrue(low <= len(make_palette.BLUE_RAMP) <= high,
                        "the ramp holds %d colours" % len(make_palette.BLUE_RAMP))

    def test_every_ramp_colour_is_blue_dominant(self):
        for text, name in make_palette.BLUE_RAMP:
            self.assertTrue(make_palette.is_blue(make_palette.rgb_of(text)),
                            "%s (%s) is not blue-dominant" % (text, name))

    def test_ramp_carries_the_dusk_teal_accent(self):
        self.assertIn("#3F7E84", [text for text, _ in make_palette.BLUE_RAMP])

    def test_ramp_colours_are_unique(self):
        texts = [text for text, _ in make_palette.BLUE_RAMP]
        self.assertEqual(len(set(texts)), len(texts))

    def test_a_ramp_that_is_too_small_is_refused(self):
        saved = make_palette.BLUE_RAMP
        make_palette.BLUE_RAMP = saved[:3]
        try:
            with self.assertRaises(ValueError):
                make_palette.ramp_colours()
        finally:
            make_palette.BLUE_RAMP = saved

    def test_a_ramp_colour_that_is_not_blue_is_refused(self):
        saved = make_palette.BLUE_RAMP
        make_palette.BLUE_RAMP = saved[:-1] + (("#8C9A2B", "a storybook green"),)
        try:
            with self.assertRaises(ValueError):
                make_palette.ramp_colours()
        finally:
            make_palette.BLUE_RAMP = saved


class BuildPaletteTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.pack = synthetic_pack(self.root / "pack")

    def tearDown(self):
        self._tmp.cleanup()

    def test_every_locked_picture_colour_is_kept(self):
        palette, art_count, total = make_palette.build_palette(self.pack)
        used = set()
        for path in make_palette.locked_pictures(self.pack):
            used |= make_palette.picture_colours(path)
        held = set(make_palette.palette_colours(palette))
        self.assertEqual(used - held, set())
        self.assertEqual(art_count, len(used))
        self.assertEqual(total, art_count + len(make_palette.BLUE_RAMP))

    def test_the_ramp_comes_after_the_art_colours(self):
        palette, _art, _total = make_palette.build_palette(self.pack)
        texts = [e["hex"] if isinstance(e, dict) else e for e in palette["colors"]]
        self.assertEqual(texts[-len(make_palette.BLUE_RAMP):],
                         [t for t, _ in make_palette.BLUE_RAMP])

    def test_the_cast_pictures_do_not_add_their_colours(self):
        palette, _art, _total = make_palette.build_palette(self.pack)
        texts = [e["hex"] if isinstance(e, dict) else e for e in palette["colors"]]
        self.assertNotIn("#010203", texts)
        self.assertNotIn("#FAF0E6", texts)

    def test_transparent_pixels_are_not_colours(self):
        path = self.root / "transparent.png"
        im = Image.new("RGBA", (4, 4), (12, 34, 56, 0))
        im.putpixel((0, 0), (12, 34, 56, 255))
        im.save(path)
        self.assertEqual(make_palette.picture_colours(path), {(12, 34, 56)})

    def test_is_blue_wants_blue_to_be_the_largest_channel(self):
        self.assertTrue(make_palette.is_blue((63, 126, 132)))
        self.assertFalse(make_palette.is_blue((140, 154, 43)))
        self.assertFalse(make_palette.is_blue((11, 185, 180)))

    def test_the_summary_line_names_the_counts(self):
        line = make_palette.summary_line("art/palette.json", 67, 77, 0, 110)
        self.assertEqual(
            line,
            "ok: 77 colours in art/palette.json - 67 from the shipped art, "
            "10 in the blue ramp, 0 off-palette in 110 pictures")


class CliTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.pack = synthetic_pack(self.root / "pack")
        self.out = self.root / "palette.json"

    def tearDown(self):
        self._tmp.cleanup()

    def test_write_then_check_passes(self):
        written = run_cli("--pack", str(self.pack), "--out", str(self.out))
        self.assertEqual(written.returncode, 0, written.stderr)
        self.assertIn("3 from the shipped art", written.stdout)
        self.assertIn("10 in the blue ramp", written.stdout)
        checked = run_cli("--pack", str(self.pack), "--out", str(self.out), "--check")
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertEqual(checked.stdout.strip(), written.stdout.strip())

    def test_a_hand_edited_palette_is_drift(self):
        run_cli("--pack", str(self.pack), "--out", str(self.out))
        data = json.loads(self.out.read_text())
        data["colors"].append("#123456")
        self.out.write_text(json.dumps(data))
        checked = run_cli("--pack", str(self.pack), "--out", str(self.out), "--check")
        self.assertEqual(checked.returncode, 1)
        self.assertIn("drift", checked.stdout)

    def test_report_prints_the_cast_and_painting_groups(self):
        run_cli("--pack", str(self.pack), "--out", str(self.out))
        reported = run_cli("--pack", str(self.pack), "--out", str(self.out),
                           "--check", "--report")
        self.assertEqual(reported.returncode, 0, reported.stderr)
        self.assertIn("cast (cut without the lock)", reported.stdout)
        self.assertIn("title painting", reported.stdout)

    def test_a_missing_picture_is_a_plain_failure(self):
        (self.pack / "props" / "pond.webp").write_text("not a picture")
        broken = run_cli("--pack", str(self.pack), "--out", str(self.out))
        self.assertEqual(broken.returncode, 1)
        self.assertNotIn("Traceback", broken.stderr)


@unittest.skipUnless(PALETTE_PATH.exists() and PACK.exists(),
                     "the committed palette and the pack are needed")
class CommittedPaletteTests(unittest.TestCase):
    """The palette file this repo ships, against the art it has to cover."""

    def setUp(self):
        with open(PALETTE_PATH, "r", encoding="utf-8") as fh:
            self.palette = json.load(fh)
        self.colours = set(make_palette.palette_colours(self.palette))

    def test_the_tool_built_this_file(self):
        built, _art, _total = make_palette.build_palette(PACK)
        self.assertEqual(built, self.palette)

    def test_every_colour_of_the_locked_art_is_in_the_palette(self):
        used = set()
        for path in make_palette.locked_pictures(PACK):
            used |= make_palette.picture_colours(path)
        self.assertEqual(used - self.colours, set())

    def test_the_palette_holds_a_blue_ramp(self):
        blues = [c for c in self.colours if make_palette.is_blue(c)]
        low, _high = make_palette.RAMP_SIZE
        self.assertTrue(len(blues) >= low,
                        "%d blue colours in the palette" % len(blues))
        ramp = set(make_palette.rgb_of(t) for t, _ in make_palette.BLUE_RAMP)
        self.assertTrue(ramp <= self.colours)
        self.assertIn(make_palette.rgb_of("#3F7E84"), ramp)

    def test_the_palette_is_what_the_downscale_tool_reads(self):
        held = pixel_downscale.load_palette(str(PALETTE_PATH))
        self.assertEqual(len(held), len(self.palette["colors"]))
        self.assertIn(make_palette.rgb_of("#3F7E84"), held)


if __name__ == "__main__":
    unittest.main()