import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SKIN_DIR = REPO_ROOT / "worlds/cottage-of-the-breeze/skins/parchment-and-wood"


class SkinContractTests(unittest.TestCase):
    def setUp(self):
        self.skin = json.loads((SKIN_DIR / "skin.json").read_text(encoding="utf-8"))

    def test_skin_opts_into_the_themed_interface(self):
        self.assertEqual(self.skin["fonts"]["display"], "Crimson Pro")
        self.assertEqual(self.skin["fonts"]["body"], "Crimson Pro")
        backdrop = self.skin["backdrop"]
        self.assertIsInstance(backdrop, str)
        self.assertTrue(backdrop.strip())
        self.assertTrue((SKIN_DIR / backdrop).is_file())

    def test_skin_backdrop_is_a_legal_picture(self):
        backdrop = Path(self.skin["backdrop"])
        candidate = SKIN_DIR / backdrop
        # vefr.maplab._skin_picture_errors requires the resolved picture to stay in the skin folder.
        self.assertTrue(candidate.resolve().is_relative_to(SKIN_DIR.resolve()))
        # vefr.cli._ART_TYPES accepts png, webp, jpg and gif, within its 8 MiB limit.
        self.assertIn(backdrop.suffix.lower(), {".png", ".webp", ".jpg", ".gif"})
        self.assertLessEqual(candidate.stat().st_size, 8 * 1024 * 1024)


if __name__ == "__main__":
    unittest.main()
