# ==================================================
#
# This file is part of CustomMaschineMK3.
# CustomMaschineMK3 is free software licensed under GPL-3.0.
# For more details, see "LICENSE" file.
#
# Copyright (C) 2024-2025 chiaki
# Copyright (C) 2026 Caparrini
#
# ==================================================

# Framework-independent logic of SceneLaunchComponent, kept apart so it can be tested
# without Live (tests/test_scene_launch.py).

from time import monotonic

PEDAL_THRESHOLD = 64
# Two pedal launches closer than this are treated as one (contact bounce, double step).
PEDAL_MIN_INTERVAL = 0.3


def target_scene_index(reference_index, scene_count, step):
    # Index of the scene to launch, or None when there is none in that direction.
    if scene_count <= 0:
        return None
    if reference_index is None or reference_index < 0 or reference_index >= scene_count:
        return 0 if step > 0 else None
    index = reference_index + step
    if 0 <= index < scene_count:
        return index
    return None


def ring_scene_offset(current_offset, ring_size, scene_index):
    # Smallest move of the session ring that makes scene_index visible.
    if scene_index < current_offset:
        return scene_index
    if scene_index >= current_offset + ring_size:
        return scene_index - ring_size + 1
    return current_offset


class PedalEdgeDetector:
    # Turns a CC footswitch into single presses: one press each time the value rises
    # across the threshold, ignoring repeats closer than min_interval seconds.

    def __init__(self, threshold = PEDAL_THRESHOLD, min_interval = PEDAL_MIN_INTERVAL, clock = monotonic):
        self._threshold = threshold
        self._min_interval = min_interval
        self._clock = clock
        self._is_down = False
        self._last_press = None

    def feed(self, value):
        is_down = value >= self._threshold
        was_down = self._is_down
        self._is_down = is_down
        if not is_down or was_down:
            return False
        now = self._clock()
        if self._last_press is not None and now - self._last_press < self._min_interval:
            return False
        self._last_press = now
        return True
