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

# Parameter banks for third-party plug-ins (VST2, VST3, AU).
#
# Live's bank lookup is keyed by device.class_name, and every plug-in shares the same
# class name ("PluginDevice" or "AuPluginDevice"). This module selects a bank definition
# by the plug-in's device name instead.
#
# Bank definitions are read from "plugin_banks.json" in the script folder:
#
#   {
#       "Serum": {
#           "Oscillators": ["A Vol", "A Pan", "A Octave", "", "B Vol", "B Pan", "B Octave", ""],
#           "Filter": ["Fil Cutoff", "Fil Reso"]
#       }
#   }
#
# - Top-level keys are matched against the start of the device name, ignoring case.
#   The longest matching key wins, so "Serum" matches "Serum" and "Serum (2)".
# - Each bank holds up to 8 parameter names. Missing entries and "" leave the knob empty.
# - Parameter names are the plug-in's original parameter names (see "plugin_parameters").
#   A name Live does not expose leaves that knob empty; it never raises an error.
#
# When PLUGIN_PARAMETER_DUMP is enabled in Config.py, selecting a plug-in writes the list
# of parameters Live exposes for it to "plugin_parameters/<device name>.txt".

import json
import re
from pathlib import Path

from ableton.v2.base.collection import IndexedDict
from ableton.v3.control_surface import BankingInfo
from ableton.v3.control_surface.default_bank_definitions import BANK_PARAMETERS_KEY
from ableton.v3.live import liveobj_valid

from . import Config
from .Logger import logger

PLUGIN_CLASS_NAMES = ("PluginDevice", "AuPluginDevice")
PLUGIN_BANKS_FILE_NAME = "plugin_banks.json"
PLUGIN_PARAMETERS_FOLDER_NAME = "plugin_parameters"
BANK_SIZE = 8

SCRIPT_FOLDER = Path(__file__).absolute().parent


def is_plugin_device(device):
    return liveobj_valid(device) and getattr(device, "class_name", None) in PLUGIN_CLASS_NAMES


def parse_plugin_banks(data):
    # Returns a list of (lower-case name prefix, IndexedDict of banks), longest prefix first.
    # Invalid entries are skipped and logged; this function never raises.
    result = []
    if not isinstance(data, dict):
        logger.warning(f"{PLUGIN_BANKS_FILE_NAME}: top level must be an object, ignored")
        return result

    for plugin_name, banks in data.items():
        if not isinstance(plugin_name, str) or plugin_name.strip() == "":
            logger.warning(f"{PLUGIN_BANKS_FILE_NAME}: empty plug-in name ignored")
            continue
        if not isinstance(banks, dict):
            logger.warning(f"{PLUGIN_BANKS_FILE_NAME}: banks of '{plugin_name}' must be an object, ignored")
            continue

        definition = IndexedDict()
        for bank_name, parameter_names in banks.items():
            if not isinstance(bank_name, str) or not isinstance(parameter_names, list):
                logger.warning(f"{PLUGIN_BANKS_FILE_NAME}: bank '{bank_name}' of '{plugin_name}' ignored")
                continue
            if len(parameter_names) > BANK_SIZE:
                logger.warning(f"{PLUGIN_BANKS_FILE_NAME}: bank '{bank_name}' of '{plugin_name}' has more than {BANK_SIZE} parameters, extra ones ignored")
            slots = [name if isinstance(name, str) else "" for name in parameter_names[:BANK_SIZE]]
            slots += [""] * (BANK_SIZE - len(slots))
            definition[bank_name] = {BANK_PARAMETERS_KEY: tuple(slots)}

        if len(definition) == 0:
            logger.warning(f"{PLUGIN_BANKS_FILE_NAME}: '{plugin_name}' has no valid banks, ignored")
            continue

        result.append((plugin_name.strip().lower(), definition))

    result.sort(key = lambda entry: len(entry[0]), reverse = True)
    return result


def load_plugin_banks(file_path = None):
    file_path = file_path or SCRIPT_FOLDER.joinpath(PLUGIN_BANKS_FILE_NAME)
    if not file_path.exists():
        return []
    try:
        data = json.loads(file_path.read_text(encoding = "utf-8"))
    except Exception as error:
        logger.warning(f"{PLUGIN_BANKS_FILE_NAME} could not be read, plug-in banks disabled: {error}")
        return []
    banks = parse_plugin_banks(data)
    logger.info(f"Plug-in banks loaded for: {', '.join(prefix for prefix, _ in banks) or 'none'}")
    return banks


def find_plugin_definition(device, plugin_banks):
    if not plugin_banks or not is_plugin_device(device):
        return None
    name = (getattr(device, "name", "") or "").lower()
    for prefix, definition in plugin_banks:
        if name.startswith(prefix):
            return definition
    return None


class PluginAwareBankingInfo(BankingInfo):
    # Same as BankingInfo, but a plug-in with a definition in plugin_banks.json is treated
    # as if its class name had that definition. Every lookup in the framework goes through
    # one of the five methods below, and all of them read self._bank_definitions.

    def __init__(self, bank_definitions, plugin_banks, *a, **k):
        super().__init__(bank_definitions, *a, **k)
        self._plugin_banks = plugin_banks

    def _call_with_plugin_definitions(self, device, method, *a, **k):
        definition = find_plugin_definition(device, self._plugin_banks)
        if definition is None:
            return method(device, *a, **k)
        original_definitions = self._bank_definitions
        self._bank_definitions = {device.class_name: definition}
        try:
            return method(device, *a, **k)
        finally:
            self._bank_definitions = original_definitions

    def has_main_bank(self, device):
        return self._call_with_plugin_definitions(device, super().has_main_bank)

    def has_bank_names(self, device):
        return self._call_with_plugin_definitions(device, super().has_bank_names)

    def device_bank_count(self, device, **k):
        return self._call_with_plugin_definitions(device, super().device_bank_count, **k)

    def device_bank_definition(self, device):
        return self._call_with_plugin_definitions(device, super().device_bank_definition)

    def device_bank_names(self, device, **k):
        return self._call_with_plugin_definitions(device, super().device_bank_names, **k)


def safe_file_name(name):
    cleaned = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", name).strip(" .")
    return cleaned or "plugin"


def format_parameter_list(device):
    parameters = list(device.parameters)[1:]  # The first parameter is always "Device On"
    lines = [
        f"# {device.name}",
        f"# Parameters exposed by Live: {len(parameters)}",
        "# Copy the names below into plugin_banks.json (up to 8 per bank).",
    ]
    if len(parameters) == 0:
        lines.append("# Live exposes no parameters for this plug-in.")
        lines.append("# Add them with the plug-in's Configure button in Live, then select the plug-in again.")
    lines += [parameter.original_name for parameter in parameters]
    return "\n".join(lines) + "\n"


def dump_plugin_parameters(device, folder = None):
    # Never raises: a failure here must not affect the controller.
    if not Config.PLUGIN_PARAMETER_DUMP or not is_plugin_device(device):
        return None
    try:
        folder = folder or SCRIPT_FOLDER.joinpath(PLUGIN_PARAMETERS_FOLDER_NAME)
        folder.mkdir(exist_ok = True)
        file_path = folder.joinpath(safe_file_name(device.name) + ".txt")
        content = format_parameter_list(device)
        if not file_path.exists() or file_path.read_text(encoding = "utf-8") != content:
            file_path.write_text(content, encoding = "utf-8")
            logger.info(f"Plug-in parameters written to {file_path}")
        return file_path
    except Exception as error:
        logger.warning(f"Plug-in parameters of '{getattr(device, 'name', '?')}' could not be written: {error}")
        return None
