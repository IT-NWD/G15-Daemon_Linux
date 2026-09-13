#!/usr/bin/env python3

import sys
import tempfile
import unittest
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE_ROOT / "gui"))

import g15_keyd
from g15_profile import ProfileSet


class ProfileSetTest(unittest.TestCase):
    def test_default_contains_all_54_bindings(self):
        rendered = g15_keyd.render(ProfileSet())
        self.assertEqual(54, sum(
            1 for line in rendered.splitlines()
            if line.startswith("g") and line.endswith(" = noop")
        ))

    def test_round_trip_preserves_bindings(self):
        model = ProfileSet()
        model.brightness = 1
        model.bindings["m1"][0] = "C-A-t"
        model.bindings["m2"][17] = "macro(Hello space World)"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "g15.conf"
            g15_keyd.save(model, path)
            loaded = g15_keyd.load(path)
        self.assertEqual("C-A-t", loaded.bindings["m1"][0])
        self.assertEqual("macro(Hello space World)", loaded.bindings["m2"][17])
        self.assertEqual(1, loaded.brightness)

    def test_rejects_invalid_device_and_actions(self):
        with self.assertRaises(ValueError):
            g15_keyd.render(ProfileSet(device_id="not-a-device"))
        model = ProfileSet()
        model.bindings["m3"][3] = "line one\nline two"
        with self.assertRaises(ValueError):
            g15_keyd.render(model)


if __name__ == "__main__":
    unittest.main()
