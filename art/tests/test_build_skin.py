#!/usr/bin/env python3
"""Tests for build_skin.py, built from synthetic Pillow images only.

Every source picture and texture is made in memory with Image.new and
putpixel, saved into a TemporaryDirectory that cleans itself up; no picture
from art/source/ is ever read. The expected file names, sizes and skin.json
values are pinned here by hand, so a change to the tool's geometry table has
to fail a test first.
"""
import contextlib
import io
import json
import math
import os
import sys
import tempfile
import unittest

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
import build_skin as bs

MARGIN = (235, 228, 216)   # the flat background a raw picture stands on
BORDER = (60, 44, 30)      # its darker border ring
STUD = (200, 60, 40)       # one odd block in the bottom-right corner, on purpose

CREDIT = "Rylee and Claude; Codex proofs, training: not cleared"
INK = {"on_panel": "#2B2118", "on_panel_dim": "#5A4A38"}
TEXTURES = ("parchment.png", "wood.png", "brass.png")

# The backdrop row is optional: no backdrop source means no backdrop picture.
BACKDROP_SOURCE = "backdrop.jpg"
BACKDROP_OUT = "backdrop.webp"

# Every picture the build must write, and the size the plan fixes for it.
SIZES = {
    "panel.webp": (96, 96),
    "speech.webp": (192, 96),
    "tooltip.webp": (96, 64),
    "button.webp": (96, 40),
    "button-hover.webp": (96, 40),
    "button-pressed.webp": (96, 40),
    "button-disabled.webp": (96, 40),
    "tab.webp": (96, 40),
    "tab-selected.webp": (96, 40),
    "toggle-off.webp": (64, 32),
    "toggle-on.webp": (64, 32),
    "bar-frame.webp": (192, 32),
    "bar-fill.webp": (176, 20),
    "gold-plate.webp": (96, 32),
    "slot.webp": (64, 64),
    "divider.webp": (192, 16),
    "banner.webp": (192, 48),
    "corner.webp": (48, 48),
    "cursor.webp": (32, 32),
    "parchment.png": (288, 288),
    "wood.png": (288, 288),
    "brass.png": (288, 288),
}

EXPECTED_FILES = tuple(SIZES) + ("skin.json",)


def paint(img, box, colour):
    """Paint a rectangle into the picture."""
    for x in range(box[0], box[2]):
        for y in range(box[1], box[3]):
            img.putpixel((x, y), colour)


def base_colour(i):
    """A deterministic base colour for the i-th source picture."""
    return (60 + (i * 47) % 150, 60 + (i * 83) % 150, 60 + (i * 19) % 150)


def raw_picture(width, height, inside):
    """A margin, a border ring with a stud, and a flat inside: a raw drawn box."""
    img = Image.new("RGB", (width, height), MARGIN)
    m = max(4, min(width, height) // 12)
    paint(img, (m, m, width - m, height - m), BORDER)
    t = max(2, m - 2)
    paint(img, (m + t, m + t, width - m - t, height - m - t), inside)
    paint(img, (width - m - t, height - m - t, width - m, height - m), STUD)
    return img


def photographic(size=256, alpha=False):
    """An opaque drawn texture: smooth grain that a lossy save throws away.

    A flat margin and a border ring would compress to almost nothing, so the
    whole frame carries slow waves instead; that is what makes the lossy file
    unmistakably smaller than the lossless one.
    """
    img = Image.new("RGBA", (size, size))
    px = img.load()
    for y in range(size):
        for x in range(size):
            px[x, y] = (
                int(128 + 100 * math.sin(x / 23.0) * math.cos(y / 17.0)) % 256,
                int(120 + 90 * math.sin((x + y) / 31.0)) % 256,
                int(110 + 80 * math.cos(x / 13.0 + y / 29.0)) % 256,
                0 if alpha and x < 8 and y < 8 else 255)
    return img


def grain(size):
    """Opaque photographic noise at a size no quality-80 save can squeeze
    under the engine's cap: the picture that must be refused."""
    return Image.effect_noise((size, size), 120).convert("RGB")


class BuildSkinTest(unittest.TestCase):
    """One synthetic source folder, then every check the brief asks for."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = self._tmp.name
        self.src = os.path.join(self.dir, "skin-source")
        self.out = os.path.join(self.dir, "skin")
        os.makedirs(self.src)
        for i, (name, (width, height)) in enumerate(SIZES.items()):
            if name in TEXTURES:
                img = Image.new("RGB", (width, height), base_colour(i))
            else:
                img = raw_picture(width, height, base_colour(i))
            img.save(os.path.join(self.src, name))

    def tearDown(self):
        self._tmp.cleanup()

    def write_backdrop(self, alpha=False, size=None):
        """Drop the optional backdrop source into the source folder.

        The alpha case is written as PNG under the backdrop's name: the name
        is what the table asks for, and the rule is about the pixels, not the
        suffix. A real JPEG cannot carry alpha at all.
        """
        path = os.path.join(self.src, BACKDROP_SOURCE)
        if alpha:
            photographic(alpha=True).save(path, format="PNG")
        elif size:
            grain(size).save(path, quality=90)
        else:
            photographic().convert("RGB").save(path, quality=90)
        return path

    def run_build(self, src=None, out=None, name="test-skin", extra=()):
        """Run the build with both streams captured, returning (code, stdout, stderr)."""
        out_buf, err_buf = io.StringIO(), io.StringIO()
        code = None
        try:
            with contextlib.redirect_stdout(out_buf), contextlib.redirect_stderr(err_buf):
                code = bs.main([src if src is not None else self.src,
                                out if out is not None else self.out,
                                "--name", name, *extra])
        except SystemExit as exc:
            code = exc.code
        return code, out_buf.getvalue(), err_buf.getvalue()

    def build(self):
        """Run the build on the full source folder and assert it succeeded."""
        code, _, err = self.run_build()
        self.assertEqual(code, 0, err)
        return os.listdir(self.out)

    def read_folder(self, folder):
        """Every file in a folder as a {name: bytes} dictionary."""
        contents = {}
        for name in sorted(os.listdir(folder)):
            with open(os.path.join(folder, name), "rb") as fh:
                contents[name] = fh.read()
        return contents

    def read_skin(self, out=None):
        """skin.json's exact text as the build wrote it."""
        with open(os.path.join(out if out is not None else self.out, "skin.json"),
                  "r", encoding="utf-8") as fh:
            return fh.read()

    def test_the_build_writes_every_expected_file(self):
        self.build()
        self.assertEqual(sorted(os.listdir(self.out)), sorted(EXPECTED_FILES))

    def test_one_wrote_line_per_file_and_nothing_else(self):
        code, out, err = self.run_build()
        self.assertEqual(code, 0, err)
        lines = out.splitlines()
        self.assertEqual(len(lines), len(EXPECTED_FILES))
        for line in lines:
            self.assertTrue(line.startswith("wrote "), f"unexpected output: {line!r}")
        written = [line[len("wrote "):] for line in lines]
        self.assertEqual(sorted(os.path.basename(p) for p in written),
                         sorted(EXPECTED_FILES))
        self.assertEqual(written[-1], os.path.join(self.out, "skin.json"))

    def test_every_picture_is_exactly_the_size_the_plan_fixes(self):
        self.build()
        for name, size in SIZES.items():
            with self.subTest(name=name):
                with Image.open(os.path.join(self.out, name)) as img:
                    self.assertEqual(img.size, size)

    def test_skin_json_carries_the_required_values(self):
        self.build()
        with open(os.path.join(self.out, "skin.json"), "r", encoding="utf-8") as fh:
            text = fh.read()
        skin = json.loads(text)
        self.assertTrue(text.endswith("\n"))
        self.assertIn('\n  "credit": ', text)          # 2-space indent
        self.assertEqual(list(skin), ["name", "credit", "parts", "ink"])
        self.assertEqual(skin["name"], "test-skin")
        self.assertEqual(skin["credit"], CREDIT)
        self.assertEqual(skin["ink"], INK)
        self.assertEqual(skin["parts"]["panel"]["slice"], 32)
        self.assertEqual(skin["parts"]["button"]["slice"], 14)

    def test_two_runs_into_the_same_folder_are_byte_identical(self):
        self.write_backdrop()
        self.build()
        first = self.read_folder(self.out)
        self.assertEqual(sorted(first), sorted(EXPECTED_FILES + (BACKDROP_OUT,)))
        self.build()
        second = self.read_folder(self.out)
        for name in sorted(first):
            with self.subTest(name=name):
                self.assertEqual(first[name], second[name])

    def test_a_fresh_folder_gets_the_same_bytes_as_the_first(self):
        self.build()
        other = os.path.join(self.dir, "skin-again")
        code, _, err = self.run_build(out=other)
        self.assertEqual(code, 0, err)
        self.assertEqual(self.read_folder(self.out), self.read_folder(other))

    def test_the_three_textures_are_copied_byte_for_byte(self):
        self.build()
        for name in TEXTURES:
            with self.subTest(name=name):
                with open(os.path.join(self.src, name), "rb") as fh:
                    source_bytes = fh.read()
                with open(os.path.join(self.out, name), "rb") as fh:
                    self.assertEqual(fh.read(), source_bytes)

    def test_the_panel_is_symmetric_like_process_ui_makes_it(self):
        self.build()
        with Image.open(os.path.join(self.src, "panel.webp")) as img:
            source = img.convert("RGBA")
        self.assertNotEqual(source.tobytes(),
                            source.transpose(Image.FLIP_LEFT_RIGHT).tobytes(),
                            "the raw panel source is already symmetric, so this "
                            "test would prove nothing")
        with Image.open(os.path.join(self.out, "panel.webp")) as img:
            panel = img.convert("RGBA")
        raw = panel.tobytes()
        self.assertEqual(raw, panel.transpose(Image.FLIP_LEFT_RIGHT).tobytes())
        self.assertEqual(raw, panel.transpose(Image.FLIP_TOP_BOTTOM).tobytes())

    def test_backdrop_saves_lossy_and_under_the_cap(self):
        self.write_backdrop()
        code, _, err = self.run_build()
        self.assertEqual(code, 0, err)
        path = os.path.join(self.out, BACKDROP_OUT)
        with Image.open(path) as img:
            self.assertEqual(img.format, "WEBP")
        size = os.path.getsize(path)
        with Image.open(os.path.join(self.src, BACKDROP_SOURCE)) as src:
            lossless = io.BytesIO()
            src.save(lossless, "WEBP", lossless=True)
        self.assertLess(size, len(lossless.getvalue()))
        self.assertLessEqual(size, bs.BACKDROP_MAX_BYTES)

    def test_backdrop_with_alpha_is_refused(self):
        self.write_backdrop(alpha=True)
        code, out, err = self.run_build()
        self.assertEqual(code, 2)
        self.assertNotIn("Traceback", err)
        self.assertEqual(err.count("\n"), 1)           # one plain line
        self.assertIn("backdrop", err)
        self.assertNotIn(BACKDROP_OUT, out)            # nothing was written for it
        self.assertFalse(os.path.exists(os.path.join(self.out, BACKDROP_OUT)))

    def test_backdrop_over_the_engine_cap_is_refused(self):
        self.write_backdrop(size=1100)     # 761718 bytes at quality 80
        code, _, err = self.run_build()
        self.assertEqual(code, 2)
        self.assertNotIn("Traceback", err)
        self.assertEqual(err.count("\n"), 1)
        self.assertIn(str(bs.BACKDROP_MAX_BYTES), err)
        self.assertFalse(os.path.exists(os.path.join(self.out, BACKDROP_OUT)))

    def test_a_missing_source_picture_exits_2_with_a_plain_message(self):
        os.remove(os.path.join(self.src, "button-pressed.webp"))
        code, out, err = self.run_build()
        self.assertEqual(code, 2)
        self.assertEqual(out, "")                      # nothing was written
        self.assertFalse(os.path.exists(self.out))
        self.assertNotIn("Traceback", err)
        self.assertEqual(err.count("\n"), 1)           # one plain line
        self.assertIn("button-pressed.webp", err)

    def test_a_missing_source_directory_exits_2_with_a_plain_message(self):
        code, out, err = self.run_build(src=os.path.join(self.dir, "nope"))
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertFalse(os.path.exists(self.out))
        self.assertNotIn("Traceback", err)
        self.assertEqual(err.count("\n"), 1)
        self.assertIn("no such directory", err)

    def test_no_new_flags_leaves_the_new_keys_out(self):
        self.build()
        skin = json.loads(self.read_skin())
        self.assertEqual(list(skin), ["name", "credit", "parts", "ink"])
        self.assertEqual(skin["credit"], CREDIT)
        self.assertNotIn("backdrop", skin)
        self.assertNotIn("fonts", skin)

    def test_the_credit_flag_writes_its_own_credit_line(self):
        code, _, err = self.run_build(extra=["--credit", "Soft Wood Studio; drawn here"])
        self.assertEqual(code, 0, err)
        skin = json.loads(self.read_skin())
        self.assertEqual(skin["credit"], "Soft Wood Studio; drawn here")
        self.assertEqual(list(skin), ["name", "credit", "parts", "ink"])

    def test_the_backdrop_flag_adds_one_key_and_no_flag_leaves_it_out(self):
        self.build()
        self.assertNotIn("backdrop", json.loads(self.read_skin()))
        code, _, err = self.run_build(extra=["--backdrop", "wood"])
        self.assertEqual(code, 0, err)
        skin = json.loads(self.read_skin())
        self.assertEqual(skin["backdrop"], "wood")
        self.assertEqual(list(skin), ["name", "credit", "backdrop", "parts", "ink"])

    def test_font_flags_fill_one_fonts_object_in_flag_order(self):
        code, _, err = self.run_build(extra=["--font", "display=Crimson Pro",
                                             "--font", "body=Crimson Pro"])
        self.assertEqual(code, 0, err)
        skin = json.loads(self.read_skin())
        self.assertEqual(skin["fonts"], {"display": "Crimson Pro",
                                         "body": "Crimson Pro"})
        self.assertEqual(list(skin), ["name", "credit", "fonts", "parts", "ink"])

    def test_all_three_flags_keep_one_key_order_and_stay_byte_identical(self):
        extra = ["--credit", "Rylee; drawn here", "--backdrop", "wood",
                 "--font", "display=Crimson Pro", "--font", "body=Crimson Pro"]
        code, _, err = self.run_build(extra=extra)
        self.assertEqual(code, 0, err)
        skin = json.loads(self.read_skin())
        self.assertEqual(list(skin), ["name", "credit", "backdrop", "fonts",
                                      "parts", "ink"])
        self.assertEqual(skin["credit"], "Rylee; drawn here")
        self.assertEqual(skin["backdrop"], "wood")
        self.assertEqual(list(skin["fonts"]), ["display", "body"])
        self.assertTrue(self.read_skin().endswith("\n"))
        first = self.read_folder(self.out)
        code, _, err = self.run_build(extra=extra)
        self.assertEqual(code, 0, err)
        self.assertEqual(first, self.read_folder(self.out))

    def test_two_font_flags_for_one_role_exit_2_with_one_plain_line(self):
        code, out, err = self.run_build(extra=["--font", "body=Crimson Pro",
                                               "--font", "body=Ledger"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertEqual(err.count("\n"), 1)           # one plain line
        self.assertNotIn("Traceback", err)
        self.assertIn("--font", err)
        self.assertFalse(os.path.exists(self.out))

    def test_a_font_flag_that_is_not_role_family_exits_2_with_one_plain_line(self):
        for spec in ("display", "display=", "=Crimson Pro", "", "display=Crimson=Pro"):
            with self.subTest(spec=spec):
                code, out, err = self.run_build(extra=["--font", spec])
                self.assertEqual(code, 2)
                self.assertEqual(out, "")
                self.assertEqual(err.count("\n"), 1)
                self.assertNotIn("Traceback", err)
                self.assertIn("--font", err)
                self.assertFalse(os.path.exists(self.out))


if __name__ == "__main__":
    unittest.main()
