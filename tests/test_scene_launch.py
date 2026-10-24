# ==================================================
#
# This file is part of CustomMaschineMK3.
# CustomMaschineMK3 is free software licensed under GPL-3.0.
# For more details, see "LICENSE" file.
#
# Copyright (C) 2026 Caparrini
#
# ==================================================

# Offline tests for SceneLaunchLogic.py and SceneLaunchComponent.py (T-04).
# Run through tests/run_tests.sh.

import os
import sys
import unittest

HARNESS = os.environ.get("HARNESS")
if not HARNESS:
    raise SystemExit("Set HARNESS to the harness folder (see tests/README.md)")
sys.path.insert(0, HARNESS)

from CustomMaschineMK3.SceneLaunchLogic import PedalEdgeDetector, ring_scene_offset, target_scene_index  # noqa: E402
from CustomMaschineMK3.SceneLaunchComponent import SceneLaunchComponent  # noqa: E402


class FakeScene:
    def __init__(self, name):
        self.name = name
        self.is_triggered = False
        self.fired = 0

    def fire(self):
        self.fired += 1
        self.is_triggered = True


class FakeView:
    selected_scene = None


class FakeSong:
    def __init__(self, count):
        self.scenes = [FakeScene(f"S{i + 1}") for i in range(count)]
        self.view = FakeView()
        self.view.selected_scene = self.scenes[0] if self.scenes else None


class FakeRing:
    def __init__(self, num_scenes = 4):
        self.num_scenes = num_scenes
        self.track_offset = 2
        self.scene_offset = 0

    def set_offsets(self, track_offset, scene_offset):
        self.track_offset = track_offset
        self.scene_offset = scene_offset


class FakeNotifications:
    class SceneLaunch:
        launch = staticmethod(lambda number, name: f"Scene {number}\n{name}")
        no_scene = staticmethod("No {} scene".format)


def make_component(count = 8, ring = None):
    song = FakeSong(count)
    component = SceneLaunchComponent(song = song, session_ring = ring if ring is not None else FakeRing())
    component.notifications = FakeNotifications
    return component, song


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


class LogicTests(unittest.TestCase):
    def test_target_index(self):
        self.assertEqual(target_scene_index(2, 8, 1), 3)
        self.assertEqual(target_scene_index(2, 8, -1), 1)
        self.assertIsNone(target_scene_index(7, 8, 1))
        self.assertIsNone(target_scene_index(0, 8, -1))
        self.assertEqual(target_scene_index(None, 8, 1), 0)
        self.assertIsNone(target_scene_index(None, 8, -1))
        self.assertEqual(target_scene_index(20, 8, 1), 0)
        self.assertIsNone(target_scene_index(0, 0, 1))

    def test_ring_offset_minimal_travel(self):
        self.assertEqual(ring_scene_offset(0, 4, 2), 0)
        self.assertEqual(ring_scene_offset(0, 4, 4), 1)
        self.assertEqual(ring_scene_offset(4, 4, 2), 2)
        self.assertEqual(ring_scene_offset(4, 4, 7), 4)

    def test_pedal_one_press_per_step(self):
        clock = Clock()
        pedal = PedalEdgeDetector(clock = clock)
        self.assertTrue(pedal.feed(127))
        self.assertFalse(pedal.feed(127))
        self.assertFalse(pedal.feed(0))
        clock.now = 1.0
        self.assertTrue(pedal.feed(127))

    def test_pedal_ignores_bounce(self):
        clock = Clock()
        pedal = PedalEdgeDetector(clock = clock)
        self.assertTrue(pedal.feed(127))
        pedal.feed(0)
        clock.now = 0.1
        self.assertFalse(pedal.feed(127))
        pedal.feed(0)
        clock.now = 0.5
        self.assertTrue(pedal.feed(127))

    def test_pedal_inverted_polarity_still_one_press_per_cycle(self):
        clock = Clock()
        pedal = PedalEdgeDetector(clock = clock)
        presses = 0
        for step, value in enumerate([127, 0, 127, 0, 127]):
            clock.now = step * 1.0
            presses += pedal.feed(value)
        self.assertEqual(presses, 3)


class ComponentTests(unittest.TestCase):
    def test_next_from_selected_scene_when_nothing_launched(self):
        component, song = make_component()
        song.view.selected_scene = song.scenes[2]
        component._on_next_scene_button_pressed(None)
        self.assertEqual(song.scenes[3].fired, 1)
        self.assertIs(song.view.selected_scene, song.scenes[3])
        self.assertEqual(component.notified[-1], "Scene 4\nS4")

    def test_next_follows_last_triggered_not_selection(self):
        component, song = make_component()
        song.scenes[5].is_triggered = True
        component._on_scene_triggered(song.scenes[5])
        song.view.selected_scene = song.scenes[0]
        component._on_next_scene_button_pressed(None)
        self.assertEqual(song.scenes[6].fired, 1)

    def test_two_fast_presses_advance_two_scenes(self):
        component, song = make_component()
        component._on_next_scene_button_pressed(None)
        component._on_next_scene_button_pressed(None)
        self.assertEqual([scene.fired for scene in song.scenes[:4]], [0, 1, 1, 0])

    def test_previous_and_limits(self):
        component, song = make_component(count = 2)
        component._on_prev_scene_button_pressed(None)
        self.assertEqual(component.notified[-1], "No previous scene")
        component._on_next_scene_button_pressed(None)
        component._on_next_scene_button_pressed(None)
        self.assertEqual(component.notified[-1], "No next scene")
        self.assertEqual(song.scenes[1].fired, 1)

    def test_ring_follows_launched_scene(self):
        ring = FakeRing()
        component, song = make_component(ring = ring)
        song.view.selected_scene = song.scenes[3]
        component._on_next_scene_button_pressed(None)
        self.assertEqual((ring.track_offset, ring.scene_offset), (2, 1))

    def test_pedal_launches_next_scene(self):
        component, song = make_component()
        component._on_pedal_value(127, None)
        component._on_pedal_value(0, None)
        self.assertEqual(song.scenes[1].fired, 1)

    def test_scene_list_change_resets_stale_reference(self):
        component, song = make_component()
        song.scenes[7].is_triggered = True
        component._on_scene_triggered(song.scenes[7])
        song.scenes = song.scenes[:3]
        component._on_scenes_changed()
        self.assertEqual(len(component._on_scene_triggered.subjects), 3)
        song.view.selected_scene = song.scenes[0]
        component._on_next_scene_button_pressed(None)
        self.assertEqual(song.scenes[1].fired, 1)

    def test_errors_never_escape(self):
        component, song = make_component()

        def broken_fire():
            raise RuntimeError("Live error")

        song.scenes[1].fire = broken_fire
        component._on_next_scene_button_pressed(None)
        self.assertEqual(song.scenes[0].fired, 0)

    def test_reference_survives_inserted_scenes(self):
        component, song = make_component()
        song.scenes[2].is_triggered = True
        component._on_scene_triggered(song.scenes[2])
        song.scenes.insert(0, FakeScene("New"))
        component._on_scenes_changed()
        component._on_next_scene_button_pressed(None)
        self.assertEqual(song.scenes[4].fired, 1)
        self.assertEqual(song.scenes[4].name, "S4")

    def test_empty_set(self):
        component, song = make_component(count = 0)
        component._on_next_scene_button_pressed(None)
        self.assertEqual(component.notified[-1], "No next scene")


if __name__ == "__main__":
    unittest.main()
