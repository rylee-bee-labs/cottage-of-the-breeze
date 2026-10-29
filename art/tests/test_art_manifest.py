#!/usr/bin/env python3
"""Tests for art/tools/art_manifest.py, slots.json and the request briefs.

Stdlib only: no Pillow, no network. The audit runs against the real pack and
against a tiny made-up pack, so a missing picture is proven to fail, not only
assumed to.
"""
import json
import re
import shutil
import struct
import sys
import tempfile
import unittest
from pathlib import Path

ART_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ART_DIR / "tools"))

import art_manifest as am  # noqa: E402


def png(path, w, h):
    """A header-only PNG: enough for the size reader."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + struct.pack(">II", w, h) + b"\0" * 9)


class ImageSize(unittest.TestCase):
    def test_reads_shipped_webp_and_png(self):
        self.assertEqual(am.image_size(am.PACK / "tiles" / "cellar-wall.grid3x3.webp"), (96, 96))
        self.assertEqual(am.image_size(am.PACK / "sprites" / "hero-sheet.webp"), (768, 192))
        self.assertEqual(am.image_size(am.PACK / "sprites" / "cellar-king.png"), (256, 256))

    def test_unreadable_is_none(self):
        self.assertIsNone(am.image_size(am.PACK / "no-such-file.webp"))


class AuditRealPack(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = am.audit(am.PACK, am.load_slots())
        cls.slots = {r["slot"]: r for r in cls.report["slots"]}

    def test_no_missing_picture(self):
        self.assertEqual(self.report["missing"], [])

    def test_kinds_are_inferred(self):
        self.assertEqual(self.slots["sprite:hero"]["kind"], "person")
        self.assertEqual(self.slots["sprite:potion"]["kind"], "item")
        self.assertEqual(self.slots["sprite:rat"]["kind"], "mob")
        self.assertEqual(self.slots["sprite:cellar-king"]["kind"], "boss")
        self.assertEqual(self.slots["tile:cellar-wall"]["kind"], "tile")
        self.assertEqual(self.slots["decor:cobweb"]["kind"], "decor")
        self.assertEqual(self.slots["prop:hearth"]["kind"], "prop")

    def test_sheets_are_found_by_file_name(self):
        # The cat's key is hearth-cat but its file is cat.webp; its sheet is cat.sheet.json.
        sheet = self.slots["sprite:hearth-cat"].get("sheet")
        self.assertIsNotNone(sheet)
        self.assertEqual(sheet["frame"], [64, 64])
        self.assertLessEqual(sheet["frames_used"], sheet["frames_drawn"])

    def test_status_notes_apply(self):
        self.assertEqual(self.slots["tile:cellar-wall"]["status"], "redo")

    def test_ember_warden_wears_a_real_sprite(self):
        # It named 'hollow-shade', which no picture answered: the game drew a plain figure.
        families = json.loads((am.PACK / "blueprint.json").read_text())["families"]
        self.assertIn(families["ember-warden"]["defaults"]["sprite"],
                      json.loads((am.PACK / "world.json").read_text())["player"]["sprites"])


class AuditFails(unittest.TestCase):
    """A negative control: the audit must fail on a pack that names a picture it lacks."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        pack = self.tmp / "pack"
        (pack / "sections").mkdir(parents=True)
        (pack / "acts").mkdir()
        png(pack / "sprites" / "hero.png", 31, 48)
        world = {"player": {"sprites": {"hero": "sprites/hero.png", "ghost": "sprites/ghost.png"}},
                 "items": {"lamp": {"name": "a lamp", "sprite": "lamp"}}}
        (pack / "world.json").write_text(json.dumps(world))
        (pack / "blueprint.json").write_text(json.dumps({"families": {"ghost": {"defaults": {"sprite": "ghost"}}}}))
        self.pack = pack

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_missing_sprite_entry_and_missing_file_both_fail(self):
        report = am.audit(self.pack, {})
        text = "\n".join(report["missing"])
        self.assertIn("items.lamp: sprite 'lamp' is not in player.sprites", text)
        self.assertIn("sprites/ghost.png is missing", text)

    def test_cli_exits_one(self):
        self.assertEqual(am.main(["audit", "--pack", str(self.pack)]), 1)


class Slots(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.slots = am.load_slots()

    def test_slots_json_is_sound(self):
        self.assertEqual(am.check_slots(self.slots), [])

    def test_between_ten_and_sixty_wanted(self):
        self.assertGreaterEqual(len(self.slots["wanted"]), 10)
        self.assertLessEqual(len(self.slots["wanted"]), 60)

    def test_every_wanted_slot_is_in_one_batch(self):
        counted = {}
        for batch in self.slots["batches"]:
            for sid in batch["slots"]:
                counted[sid] = counted.get(sid, 0) + 1
        for slot in self.slots["wanted"]:
            self.assertEqual(counted.get(slot["id"]), 1, slot["id"])

    def test_loops_name_a_loop_in_loops_md(self):
        loops = (am.REPO / "docs" / "plans" / "release-1-0" / "LOOPS.md").read_text(encoding="utf-8")
        numbers = set(re.findall(r"^### (\d+)\.", loops, re.M))
        for slot in self.slots["wanted"]:
            self.assertIn(str(slot["loop"]), numbers, slot["id"])

    def test_wanted_ids_do_not_collide_with_shipped_sprites(self):
        sprites = json.loads((am.PACK / "world.json").read_text())["player"]["sprites"]
        for slot in self.slots["wanted"]:
            self.assertNotIn(slot["id"], sprites)

    def test_check_slots_catches_bad_input(self):
        bad = {"wanted": [{"id": "x", "kind": "nope", "loop": 1, "native": [1, 1], "subject": "s"},
                          {"id": "x", "kind": "item", "loop": 1, "native": "big", "subject": "s"}],
               "batches": [{"id": "b", "slots": ["x", "y"]}]}
        problems = "\n".join(am.check_slots(bad))
        self.assertIn("unknown kind 'nope'", problems)
        self.assertIn("missing or repeated id", problems)
        self.assertIn("native must be [w, h]", problems)
        self.assertIn("names unknown slot 'y'", problems)


class Briefs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.slots = am.load_slots()
        cls.by_id = {s["id"]: s for s in cls.slots["wanted"]}

    def test_every_batch_renders_completely(self):
        for batch in self.slots["batches"]:
            text, plan = am.render_brief(batch, self.slots)
            self.assertNotRegex(text, r"\{\{\w+\}\}", batch["id"])
            for sid in batch["slots"]:
                self.assertIn(f"`{sid}`", text)
                self.assertIn(self.by_id[sid]["subject"], text)
            self.assertIn("#00FF00", text)
            self.assertIn("never pure black", text)
            for ref in re.findall(r"^\d+\. `([^`]+)`", text, re.M):
                self.assertTrue((am.REPO / ref).is_file(), f"{batch['id']}: reference {ref} is not on disk")
            json.loads(am.dump(plan))

    def test_kit_plans_match_process_kit(self):
        batch = next(b for b in self.slots["batches"] if b["id"] == "items-gear-1")
        _, plan = am.render_brief(batch, self.slots)
        sheet = plan["sheets"][0]
        cols, rows = (int(n) for n in sheet["grid"].split("x"))
        self.assertEqual(len(sheet["props"]), cols * rows)
        self.assertEqual(plan["tile"], 32)
        self.assertEqual(sheet["props"][0], {"name": "gear-hand-1", "size": [24, 24]})

    def test_written_requests_are_current(self):
        """art/requests/ is generated: it must match what slots.json renders today."""
        out = am.REPO / "art" / "requests"
        for batch in self.slots["batches"]:
            text, plan = am.render_brief(batch, self.slots)
            self.assertEqual((out / f"{batch['id']}.md").read_text(encoding="utf-8"), text,
                             f"{batch['id']}.md is stale: run `python3 art/tools/art_manifest.py brief --all`")
            self.assertEqual((out / f"{batch['id']}.plan.json").read_text(encoding="utf-8"), am.dump(plan) + "\n")


if __name__ == "__main__":
    unittest.main()
