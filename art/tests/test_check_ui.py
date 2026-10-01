#!/usr/bin/env python3
"""Tests for check_ui.py, built from synthetic Pillow images only."""
import contextlib
import copy
import io
import json
import os
import sys
import tempfile
import unittest

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
import check_ui as cu

BORDER = (90, 64, 40)      # the panel's flat border ring
INSIDE = (200, 170, 130)   # the panel's inside: passes both contrast checks
NORMAL = (150, 120, 90)    # the four button states, each visibly
HOVER = (170, 140, 110)    # different from the other three
PRESSED = (120, 90, 60)
DISABLED = (135, 135, 130)

GOOD_PARTS = {
    "panel": {"file": "panel.webp", "slice": 8, "fill": "parchment"},
    "button": {"file": "button.webp", "slice": 12, "hover": "button-hover.webp",
               "pressed": "button-pressed.webp", "disabled": "button-disabled.webp"},
    "divider": {"file": "divider.webp"},
    "cursor": {"file": "cursor.png", "hotspot": [4, 4]},
}
GOOD_INK = {"on_panel": "#2B2118", "on_panel_dim": "#5A4A38"}


def gray(value):
    """A flat grey colour."""
    return (value, value, value)


def paint(img, box, colour):
    """Paint a rectangle into the picture."""
    for x in range(box[0], box[2]):
        for y in range(box[1], box[3]):
            img.putpixel((x, y), colour)


def panel_picture(width=64, height=64, slice_n=8, inside=INSIDE):
    """A symmetric nine-slice panel: a flat border ring around a flat inside."""
    img = Image.new("RGB", (width, height), BORDER)
    paint(img, (slice_n, slice_n, width - slice_n, height - slice_n), inside)
    return img


def ramp_panel(width=64, height=64, slice_n=8):
    """A panel with a symmetric ring and a left-to-right ramp inside, like a tiled texture."""
    img = Image.new("RGB", (width, height), BORDER)
    inner = width - 2 * slice_n
    for y in range(slice_n, height - slice_n):
        for x in range(slice_n, width - slice_n):
            t = (x - slice_n) / max(1, inner - 1)
            img.putpixel((x, y), (round(170 + 60 * t), round(140 + 60 * t),
                                  round(100 + 60 * t)))
    return img


def state_picture(colour, width=48, height=48):
    """A flat button-state picture."""
    return Image.new("RGB", (width, height), colour)


def noisy_picture(width, height, seed=7):
    """A deterministic noisy picture that PNG compresses badly."""
    data = bytearray(width * height)
    state = seed
    for i in range(len(data)):
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        data[i] = (state >> 16) & 0xFF
    return Image.frombytes("L", (width, height), bytes(data))


class CheckUiTest(unittest.TestCase):
    """Every check, run against a synthetic skin in a temporary folder."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = self._tmp.name
        self.save(panel_picture(), "panel.webp")
        self.save(state_picture(NORMAL), "button.webp")
        self.save(state_picture(HOVER), "button-hover.webp")
        self.save(state_picture(PRESSED), "button-pressed.webp")
        self.save(state_picture(DISABLED), "button-disabled.webp")
        self.save(Image.new("RGB", (32, 8), (60, 45, 30)), "divider.webp")
        cursor = Image.new("RGB", (32, 32), (250, 245, 235))
        paint(cursor, (4, 4, 12, 12), (20, 20, 20))
        self.save(cursor, "cursor.png")
        self.save(Image.new("RGB", (16, 16), (230, 215, 190)), "parchment.png")
        self.write_skin()

    def tearDown(self):
        self._tmp.cleanup()

    def save(self, img, name):
        """Save a synthetic picture into the skin folder, keeping webp pictures exact."""
        path = os.path.join(self.dir, name)
        if name.lower().endswith(".webp"):
            img.save(path, lossless=True)
        else:
            img.save(path)
        return path

    def write_skin(self, parts=None, ink=GOOD_INK):
        """Write skin.json over the folder; None parts means a fresh copy of the good ones."""
        skin = {"name": "test-skin", "credit": "synthetic tests",
                "parts": copy.deepcopy(GOOD_PARTS) if parts is None else parts}
        if ink is not None:
            skin["ink"] = ink
        with open(os.path.join(self.dir, "skin.json"), "w", encoding="utf-8") as fh:
            json.dump(skin, fh, indent=2)

    def run_args(self, args):
        """Run check_ui.main on raw arguments, returning (exit code, stdout, stderr)."""
        out, err = io.StringIO(), io.StringIO()
        code = None
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = cu.main(args)
        except SystemExit as exc:
            code = exc.code if exc.code is not None else 0
        return code, out.getvalue(), err.getvalue()

    def check(self, *extra):
        """Run the check on the skin folder, returning (exit code, stdout)."""
        code, out, _ = self.run_args([self.dir] + list(extra))
        return code, out

    def assert_fails(self, code, out, *words):
        """The skin failed: exit 1, no ok lines, and every word is in the output."""
        self.assertEqual(code, 1, out)
        lines = out.splitlines()
        self.assertFalse(any(line.startswith("ok ") for line in lines),
                         "ok lines mixed with problems:\n" + out)
        for word in words:
            self.assertIn(word, out)

    def test_good_skin_exits_zero_with_one_ok_line_per_part(self):
        code, out = self.check()
        self.assertEqual(code, 0, out)
        self.assertEqual(out.splitlines(),
                         ["ok panel", "ok button", "ok divider", "ok cursor"])

    def test_a_named_file_that_does_not_exist(self):
        os.remove(os.path.join(self.dir, "button-hover.webp"))
        code, out = self.check()
        self.assert_fails(code, out, "button-hover.webp: not found")

    def test_a_named_file_that_is_not_a_webp_or_png(self):
        parts = copy.deepcopy(GOOD_PARTS)
        parts["divider"]["file"] = "divider.gif"
        self.save(Image.new("RGB", (32, 8), (60, 45, 30)), "divider.gif")
        self.write_skin(parts)
        code, out = self.check()
        self.assert_fails(code, out, "divider.gif: not a .webp or .png picture")

    def test_a_piece_over_the_128_kb_cap(self):
        parts = copy.deepcopy(GOOD_PARTS)
        parts["ornament"] = {"file": "noisy.png"}
        path = self.save(noisy_picture(512, 512), "noisy.png")
        self.assertGreater(os.path.getsize(path), 128 * 1024)
        self.write_skin(parts)
        code, out = self.check()
        self.assert_fails(code, out, "noisy.png", "over the 128 KB cap for a piece")

    def test_a_texture_over_the_256_kb_cap(self):
        path = self.save(noisy_picture(900, 900), "parchment.png")
        self.assertGreater(os.path.getsize(path), 256 * 1024)
        code, out = self.check()
        self.assert_fails(code, out, "parchment.png",
                          "over the 256 KB cap for a texture")

    def test_a_texture_that_resolves_to_no_file(self):
        parts = copy.deepcopy(GOOD_PARTS)
        parts["panel"]["fill"] = "vellum"
        self.write_skin(parts)
        code, out = self.check()
        self.assert_fails(code, out, "vellum", "texture")

    def test_a_slice_that_does_not_fit_the_picture(self):
        parts = copy.deepcopy(GOOD_PARTS)
        parts["panel"]["slice"] = 40  # 2 * 40 is not under 64
        self.write_skin(parts)
        code, out = self.check()
        self.assert_fails(code, out, "panel.webp: slice 40 does not fit a 64x64 picture")

    def test_a_slice_that_is_not_a_whole_number(self):
        parts = copy.deepcopy(GOOD_PARTS)
        parts["panel"]["slice"] = 8.5
        self.write_skin(parts)
        code, out = self.check()
        self.assert_fails(code, out, "slice 8.5 is not a whole number")

    def test_button_states_where_one_is_a_copy_of_another(self):
        self.save(state_picture(NORMAL), "button-pressed.webp")
        code, out = self.check()
        self.assert_fails(code, out,
                          "button.webp and button-pressed.webp are too alike",
                          "mean difference 0.0")

    def test_button_states_of_different_sizes(self):
        self.save(state_picture(DISABLED, 32, 32), "button-disabled.webp")
        code, out = self.check()
        self.assert_fails(code, out, "not all the same size", "disabled 32x32")

    def test_a_part_naming_only_some_button_states_is_not_checked(self):
        parts = copy.deepcopy(GOOD_PARTS)
        parts["button"] = {"file": "button.webp", "slice": 12,
                           "hover": "button-hover.webp"}
        self.save(state_picture(NORMAL), "button-hover.webp")  # a copy of the normal state
        self.write_skin(parts)
        code, out = self.check()
        self.assertEqual(code, 0, out)

    def test_a_panel_border_ring_that_is_not_symmetric(self):
        panel = panel_picture()
        paint(panel, (56, 0, 64, 64), (200, 40, 40))  # the right band differs from the left
        self.save(panel, "panel.webp")
        code, out = self.check()
        self.assert_fails(code, out, "border ring is not symmetric", "left-right")

    def test_a_symmetric_ring_with_an_asymmetric_inside_passes(self):
        self.save(ramp_panel(), "panel.webp")
        code, out = self.check()
        self.assertEqual(code, 0, out)
        self.assertIn("ok panel", out)

    def test_a_picture_that_cannot_be_read(self):
        with open(os.path.join(self.dir, "panel.webp"), "wb") as fh:
            fh.write(b"not a picture")
        code, out = self.check()
        self.assert_fails(code, out, "panel.webp: cannot read")

    def test_an_ink_that_is_too_light_for_the_panel(self):
        self.write_skin(ink={"on_panel": "#C0C0C0", "on_panel_dim": "#C0C0C0"})
        code, out = self.check()
        self.assert_fails(code, out, "ink.on_panel #C0C0C0 is 1.21:1",
                          "needs 4.5:1", "needs 3:1")

    def test_a_dark_ink_passes_both_contrast_checks(self):
        self.write_skin(ink={"on_panel": "#101010", "on_panel_dim": "#30251C"})
        code, out = self.check()
        self.assertEqual(code, 0, out)

    def test_on_panel_contrast_at_the_4_5_boundary(self):
        self.write_skin(ink={"on_panel": "#2B2118", "on_panel_dim": "#2B2118"})
        # Grey 136 inside gives 4.44:1, just under the 4.5:1 this ink needs.
        self.save(panel_picture(inside=gray(136)), "panel.webp")
        code, out = self.check()
        self.assert_fails(code, out, "ink.on_panel #2B2118 is 4.44:1", "needs 4.5:1")
        # Grey 137 gives 4.50:1, just over: the skin passes.
        self.save(panel_picture(inside=gray(137)), "panel.webp")
        code, out = self.check()
        self.assertEqual(code, 0, out)

    def test_on_panel_dim_contrast_at_the_3_boundary(self):
        self.write_skin(ink={"on_panel": "#2B2118", "on_panel_dim": "#5A4A38"})
        # Grey 153 inside gives 2.98:1, just under the 3:1 the dim ink needs.
        self.save(panel_picture(inside=gray(153)), "panel.webp")
        code, out = self.check()
        self.assert_fails(code, out, "ink.on_panel_dim #5A4A38 is 2.98:1", "needs 3:1")
        # Grey 154 gives 3.02:1, just over: the skin passes.
        self.save(panel_picture(inside=gray(154)), "panel.webp")
        code, out = self.check()
        self.assertEqual(code, 0, out)

    def test_missing_ink_makes_contrast_uncheckable(self):
        self.write_skin(ink=None)
        code, out = self.check()
        self.assert_fails(code, out, "ink.on_panel", "contrast cannot be checked")
        code, out = self.check("--ink-on-panel", "#2B2118",
                               "--ink-on-panel-dim", "#5A4A38")
        self.assertEqual(code, 0, out)

    def test_the_ink_flags_override_the_declared_ink(self):
        self.write_skin(ink={"on_panel": "#C0C0C0", "on_panel_dim": "#C0C0C0"})
        code, _ = self.check()
        self.assertEqual(code, 1)  # the declared ink is too light for the panel
        code, out = self.check("--ink-on-panel", "#2B2118",
                               "--ink-on-panel-dim", "#5A4A38")
        self.assertEqual(code, 0, out)

    def test_a_bad_ink_flag_exits_two(self):
        code, _, err = self.run_args([self.dir, "--ink-on-panel", "parchment"])
        self.assertEqual(code, 2)
        self.assertIn("--ink-on-panel", err)

    def test_a_hotspot_outside_the_picture(self):
        parts = copy.deepcopy(GOOD_PARTS)
        parts["cursor"]["hotspot"] = [32, 4]  # x sits on the 32-wide edge
        self.write_skin(parts)
        code, out = self.check()
        self.assert_fails(code, out, "hotspot [32, 4] is outside the 32x32 picture")

    def test_a_hotspot_inside_the_picture(self):
        parts = copy.deepcopy(GOOD_PARTS)
        parts["cursor"]["hotspot"] = [31, 31]  # the last pixel that is still inside
        self.write_skin(parts)
        code, out = self.check()
        self.assertEqual(code, 0, out)
        self.assertIn("ok cursor", out)

    def test_a_cursor_without_a_hotspot(self):
        parts = copy.deepcopy(GOOD_PARTS)
        del parts["cursor"]["hotspot"]
        self.write_skin(parts)
        code, out = self.check()
        self.assert_fails(code, out, "cursor: no hotspot declared")

    def test_a_hotspot_that_is_not_two_whole_numbers(self):
        parts = copy.deepcopy(GOOD_PARTS)
        parts["cursor"]["hotspot"] = [4, 4.5]
        self.write_skin(parts)
        code, out = self.check()
        self.assert_fails(code, out, "not a list of two whole numbers")

    def test_a_missing_skin_json(self):
        os.remove(os.path.join(self.dir, "skin.json"))
        code, out = self.check()
        self.assert_fails(code, out, "skin.json: not found")

    def test_malformed_json(self):
        with open(os.path.join(self.dir, "skin.json"), "w", encoding="utf-8") as fh:
            fh.write("{not json")
        code, out = self.check()
        self.assert_fails(code, out, "skin.json: not valid JSON")

    def test_a_skin_json_without_parts(self):
        with open(os.path.join(self.dir, "skin.json"), "w", encoding="utf-8") as fh:
            json.dump({"name": "no-parts"}, fh)
        code, out = self.check()
        self.assert_fails(code, out, "parts")

    def test_a_directory_that_does_not_exist_exits_two(self):
        code, _, err = self.run_args([os.path.join(self.dir, "nope")])
        self.assertEqual(code, 2)
        self.assertIn("no such directory", err)

    def test_no_arguments_exits_two(self):
        code, _, _ = self.run_args([])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
