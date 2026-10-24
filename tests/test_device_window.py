# ==================================================
#
# This file is part of CustomMaschineMK3.
# CustomMaschineMK3 is free software licensed under GPL-3.0.
# For more details, see "LICENSE" file.
#
# Copyright (C) 2026 Caparrini
#
# ==================================================

# Offline tests for DeviceWindowComponent.py (T-12). Run through tests/run_tests.sh.

import os
import sys
import unittest

HARNESS = os.environ.get("HARNESS")
if not HARNESS:
    raise SystemExit("Set HARNESS to the harness folder (see tests/README.md)")
sys.path.insert(0, HARNESS)

from CustomMaschineMK3.DeviceWindowComponent import DeviceWindowComponent, toggle_editor  # noqa: E402


class FakePlugin:
    def __init__(self, name = "Serum"):
        self.name = name
        self.is_editor_open = False


class FakeNativeDevice:
    def __init__(self, name = "Simpler"):
        self.name = name


class FakeView:
    def __init__(self):
        self.shown = []

    def show_view(self, name):
        self.shown.append(name)


class FakeApplication:
    def __init__(self):
        self.view = FakeView()


class FakeSong:
    appointed_device = None


class FakeNotifications:
    class DeviceWindow:
        window = staticmethod(lambda name, state: f"{name}\nwindow {state}")
        chain = staticmethod(lambda name: f"{name}\nshown in device view")
        no_device = "No device selected"


def make(device):
    song = FakeSong()
    song.appointed_device = device
    application = FakeApplication()
    component = DeviceWindowComponent(song = song, application = application)
    component.notifications = FakeNotifications
    return component, application


class DeviceWindowTests(unittest.TestCase):
    def test_toggle_editor(self):
        plugin = FakePlugin()
        self.assertEqual(toggle_editor(plugin), "open")
        self.assertEqual(toggle_editor(plugin), "closed")
        self.assertIsNone(toggle_editor(FakeNativeDevice()))
        self.assertIsNone(toggle_editor(None))

    def test_plugin_window_opens_and_closes(self):
        plugin = FakePlugin()
        component, application = make(plugin)
        component._on_toggle_button_pressed(None)
        self.assertTrue(plugin.is_editor_open)
        self.assertEqual(component.notified[-1], "Serum\nwindow open")
        component._on_toggle_button_pressed(None)
        self.assertFalse(plugin.is_editor_open)
        self.assertEqual(application.view.shown, [])

    def test_native_device_shows_device_chain(self):
        component, application = make(FakeNativeDevice())
        component._on_toggle_button_pressed(None)
        self.assertEqual(application.view.shown, ["Detail", "Detail/DeviceChain"])
        self.assertEqual(component.notified[-1], "Simpler\nshown in device view")

    def test_no_device(self):
        component, _ = make(None)
        component._on_toggle_button_pressed(None)
        self.assertEqual(component.notified[-1], "No device selected")

    def test_errors_never_escape(self):
        class Broken:
            name = "Broken"

            @property
            def is_editor_open(self):
                raise RuntimeError("Live error")

        component, _ = make(Broken())
        component._on_toggle_button_pressed(None)


if __name__ == "__main__":
    unittest.main()
