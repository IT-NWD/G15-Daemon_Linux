#!/usr/bin/env python3

import sys
import tempfile
import unittest
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE_ROOT / "gui"))

import g15_keyd
import g15_platform
from g15_profile import ActionKind, BindingAction, ProfileSet, WINDOWS_DEFAULT_BINDINGS


class ProfileSetTest(unittest.TestCase):
    def test_default_contains_all_54_bindings(self):
        rendered = g15_keyd.render(ProfileSet())
        self.assertEqual(54, sum(
            1 for line in rendered.splitlines()
            if line.startswith("g") and line.endswith(" = noop")
        ))

    def test_round_trip_preserves_bindings(self):
        model = ProfileSet()
        model.name = "Produktivität"
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
        self.assertEqual("Produktivität", loaded.name)

    def test_rejects_invalid_device_and_actions(self):
        with self.assertRaises(ValueError):
            g15_keyd.render(ProfileSet(device_id="not-a-device"))
        model = ProfileSet()
        model.bindings["m3"][3] = "line one\nline two"
        with self.assertRaises(ValueError):
            g15_keyd.render(model)

    def test_understands_editor_action_types(self):
        self.assertEqual(ActionKind.DISABLED, BindingAction.parse("noop").kind)
        self.assertEqual(ActionKind.KEYSTROKE, BindingAction.parse("C-A-t").kind)
        self.assertEqual("macro(Hello space World)",
                         BindingAction(ActionKind.MACRO, "Hello space World").render())
        repeated = BindingAction(ActionKind.REPEATING_MACRO, "C-c", 500, 75)
        self.assertEqual(repeated, BindingAction.parse(repeated.render()))
        self.assertEqual(ActionKind.ADVANCED,
                         BindingAction.parse("overload(control, esc)").kind)

    def test_can_copy_and_reset_memory_banks(self):
        model = ProfileSet()
        model.bindings["m1"][0] = "C-c"
        model.copy_bank("m1", "m2")
        self.assertEqual("C-c", model.bindings["m2"][0])
        model.bindings["m1"][0] = "C-v"
        self.assertEqual("C-c", model.bindings["m2"][0])
        model.reset_bank("m3", use_windows_defaults=True)
        self.assertEqual(list(WINDOWS_DEFAULT_BINDINGS), model.bindings["m3"])

    def test_rejects_invalid_profile_name_and_repeat_delays(self):
        with self.assertRaises(ValueError):
            ProfileSet(name="").validate()
        with self.assertRaises(ValueError):
            BindingAction(ActionKind.REPEATING_MACRO, "a", 0, 50).render()
        with self.assertRaises(ValueError):
            BindingAction(ActionKind.ADVANCED, "command(id)").render()

    def test_creates_portable_export_filename(self):
        self.assertEqual("Meine-Spiele.conf",
                         g15_platform.safe_profile_filename("Meine Spiele"))
        self.assertEqual("g15-profile.conf", g15_platform.safe_profile_filename("..."))


if __name__ == "__main__":
    unittest.main()
