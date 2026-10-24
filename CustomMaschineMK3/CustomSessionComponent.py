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

from ableton.v3.control_surface.components import SessionComponent


class CustomSessionComponent(SessionComponent):
    # DUPLICATE is mapped to copy_button, which only reaches clip slots. This sends it to
    # the scene launch buttons as well, so DUPLICATE + SCENE + pad 4, 8, 12 or 16 duplicates
    # that scene (SceneComponent handles the action). Clip copy is unchanged.

    def set_scene_duplicate_button(self, button):
        for index in range(self._session_ring.num_scenes):
            self.scene(index).duplicate_button.set_control_element(button)
