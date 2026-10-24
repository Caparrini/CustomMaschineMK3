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

# Scene launching for live performance.
#
# - SCENE + RIGHT launches the scene after the last launched one, SCENE + LEFT the one before.
# - Optionally, a footswitch on the PEDAL input launches the next scene
#   (setting "Pedal Function" = "Next Scene", reload required).
#
# "Last launched" is the last scene that became triggered by any means (this controller,
# the mouse, another controller or a scene Follow Action). Live's selected scene is not
# moved by Follow Actions, so using it as the reference would launch the wrong scene after
# a Follow Action. The selected scene is used only until a scene has been launched.

from ableton.v3.base import depends, listens, listens_group
from ableton.v3.control_surface.component import Component
from ableton.v3.control_surface.controls import ButtonControl, InputControl
from ableton.v3.control_surface.display import Renderable
from ableton.v3.live import liveobj_valid

from .Logger import logger
from .SceneLaunchLogic import PedalEdgeDetector, ring_scene_offset, target_scene_index


class SceneLaunchComponent(Component, Renderable):
    next_scene_button = ButtonControl(color = None)
    prev_scene_button = ButtonControl(color = None)
    pedal_input = InputControl()

    @depends(session_ring = None)
    def __init__(self, name = "Scene_Launch", session_ring = None, *a, **k):
        super().__init__(name, *a, **k)
        self._session_ring = session_ring
        self._last_triggered_index = None
        self._pedal = PedalEdgeDetector()
        self._on_scenes_changed.subject = self.song
        self._on_scenes_changed()

    @next_scene_button.pressed
    def _on_next_scene_button_pressed(self, button):
        self._launch_relative(1)

    @prev_scene_button.pressed
    def _on_prev_scene_button_pressed(self, button):
        self._launch_relative(-1)

    @pedal_input.value
    def _on_pedal_value(self, value, control):
        if self._pedal.feed(value):
            self._launch_relative(1)

    def _reference_index(self):
        if self._last_triggered_index is not None:
            return self._last_triggered_index
        scenes = list(self.song.scenes)
        selected = self.song.view.selected_scene
        for index, scene in enumerate(scenes):
            if scene == selected:
                return index
        return None

    def _launch_relative(self, step):
        try:
            scenes = list(self.song.scenes)
            index = target_scene_index(self._reference_index(), len(scenes), step)
            if index is None:
                self.notify(self.notifications.SceneLaunch.no_scene, "next" if step > 0 else "previous")
                return
            scene = scenes[index]
            scene.fire()
            # Fired scenes become triggered, which also updates _last_triggered_index; set it
            # here as well so two fast presses advance two scenes.
            self._last_triggered_index = index
            self.song.view.selected_scene = scene
            self._show_scene_in_ring(index)
            self.notify(self.notifications.SceneLaunch.launch, index + 1, scene.name)
        except Exception as error:
            logger.warning(f"Scene launch failed: {error}")

    def _show_scene_in_ring(self, index):
        ring = self._session_ring
        if ring is None:
            return
        new_offset = ring_scene_offset(ring.scene_offset, ring.num_scenes, index)
        if new_offset != ring.scene_offset:
            ring.set_offsets(ring.track_offset, new_offset)

    @listens("scenes")
    def _on_scenes_changed(self):
        self._on_scene_triggered.replace_subjects(list(self.song.scenes))
        if self._last_triggered_index is not None and self._last_triggered_index >= len(self.song.scenes):
            self._last_triggered_index = None

    @listens_group("is_triggered")
    def _on_scene_triggered(self, scene):
        if liveobj_valid(scene) and scene.is_triggered:
            for index, candidate in enumerate(self.song.scenes):
                if candidate == scene:
                    self._last_triggered_index = index
                    break
