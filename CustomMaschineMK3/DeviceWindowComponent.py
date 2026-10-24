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

# SHIFT + PLUG-IN opens or closes the window of the selected plug-in (VST/AU).
# For Live's own devices, which have no separate window, it shows the device chain view.
#
# PluginDevice.is_editor_open is documented in the Live Object Model for Live 12.4 and is
# not used by the Live 12.0 scripts, so it may be missing in older versions; then the
# device chain view is shown instead and the display says so.

from ableton.v3.control_surface.component import Component
from ableton.v3.control_surface.controls import ButtonControl
from ableton.v3.control_surface.display import Renderable
from ableton.v3.live import liveobj_valid

from .Logger import logger


def toggle_editor(device):
    # Returns "open", "closed" or None when the device has no window Live can control.
    if not liveobj_valid(device) or not hasattr(device, "is_editor_open"):
        return None
    device.is_editor_open = not device.is_editor_open
    return "open" if device.is_editor_open else "closed"


class DeviceWindowComponent(Component, Renderable):
    toggle_button = ButtonControl(color = None)

    def __init__(self, name = "Device_Window", *a, **k):
        super().__init__(name, *a, **k)

    @toggle_button.pressed
    def _on_toggle_button_pressed(self, button):
        try:
            device = self.song.appointed_device
            if not liveobj_valid(device):
                self.notify(self.notifications.DeviceWindow.no_device)
                return
            state = toggle_editor(device)
            if state is None:
                view = self.application.view
                view.show_view("Detail")
                view.show_view("Detail/DeviceChain")
                self.notify(self.notifications.DeviceWindow.chain, device.name)
            else:
                self.notify(self.notifications.DeviceWindow.window, device.name, state)
        except Exception as error:
            logger.warning(f"Device window toggle failed: {error}")
