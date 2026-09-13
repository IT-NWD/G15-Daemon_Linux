#!/usr/bin/env python3

import importlib.machinery
import importlib.util
import unittest
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parents[1]
HELPER_PATH = SOURCE_ROOT / "gui/g15-profile-install"
loader = importlib.machinery.SourceFileLoader("g15_profile_install", str(HELPER_PATH))
spec = importlib.util.spec_from_loader(loader.name, loader)
helper = importlib.util.module_from_spec(spec)
loader.exec_module(helper)


class InstallHelperTest(unittest.TestCase):
    def test_finds_device_id(self):
        profile = "# comment\n[ids]\n0000:0000:95e990cb\n\n[main]\n"
        self.assertEqual("0000:0000:95e990cb", helper.find_device_id(profile))

    def test_updates_existing_brightness(self):
        original = "[Global]\nUse MR as Cycle Key: Off\nKeyboard Backlight Level: 1\n\n[Next]\nx: y\n"
        updated = helper.update_brightness(original, 2)
        self.assertIn("Keyboard Backlight Level: 2", updated)
        self.assertNotIn("Keyboard Backlight Level: 1", updated)
        self.assertEqual(1, updated.count("Keyboard Backlight Level"))

    def test_adds_global_section_when_missing(self):
        updated = helper.update_brightness("[PLUGIN_LOAD_ORDER]\n0: plugin.so\n", 2)
        self.assertTrue(updated.endswith("[Global]\nKeyboard Backlight Level: 2\n"))


if __name__ == "__main__":
    unittest.main()
