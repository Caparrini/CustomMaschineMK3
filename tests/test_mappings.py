# ==================================================
#
# This file is part of CustomMaschineMK3.
# CustomMaschineMK3 is free software licensed under GPL-3.0.
# For more details, see "LICENSE" file.
#
# Copyright (C) 2026 Caparrini
#
# ==================================================

# Static consistency check between Mappings.py and ControlElements.py: every element name
# used in a mapping must be created in ControlElements.py, and every component named in
# Mappings.py must exist in the component map. A typo here would only show up in Live.

import ast
import re
import unittest
from pathlib import Path

SCRIPT = Path(__file__).absolute().parent.parent / "CustomMaschineMK3"
NON_ELEMENT_KEYS = {"component", "modes", "default_behaviour", "behaviour"}
FRAMEWORK_COMPONENTS = {
    # Created by ableton.v3 ControlSurface itself, not listed in Specification.component_map.
    "Transport", "View_Based_Recording", "Session", "Session_Navigation", "Session_Overview",
    "Mixer", "Device", "Drum_Group", "Step_Sequence", "View_Toggle", "Undo_Redo", "Clip_Actions",
    "Accent", "Target_Track", "Note_Repeat", "Sliced_Simpler", "Session_Ring",
}


def element_names():
    source = (SCRIPT / "ControlElements.py").read_text()
    names = set()
    for match in re.finditer(r'add_(?:modifier_)?(?:button|encoder)\(\s*\d+\s*,\s*"([^"]+)"', source):
        names.add(match.group(1))
    for match in re.finditer(r'add_(?:button_matrix|encoder_matrix|matrix)\(\s*[^"]*?"([^"]+)"', source):
        names.add(match.group(1))
    for match in re.finditer(r'add_element\(\s*"([^"]+)"', source):
        names.add(match.group(1))
    for match in re.finditer(r'add_submatrix\([^,]+,\s*"([^"]+)"', source):
        names.add(match.group(1))
    names.add("original_order_pads")
    names = {name.lower().replace(" ", "_") for name in names}
    for match in re.finditer(r'add_modified_control\(self\.(\w+),\s*self\.(\w+)\)', source):
        names.add(f"{match.group(1)}_with_{match.group(2)}")
    return names


def mapped_values():
    # (key, element name) for every string assigned to a control in Mappings.py
    tree = ast.parse((SCRIPT / "Mappings.py").read_text())
    pairs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "dict":
            for keyword in node.keywords:
                if keyword.arg in NON_ELEMENT_KEYS or keyword.arg is None:
                    continue
                if isinstance(keyword.value, ast.Constant) and isinstance(keyword.value.value, str):
                    pairs.append((keyword.arg, keyword.value.value))
                elif isinstance(keyword.value, ast.IfExp):
                    for branch in (keyword.value.body, keyword.value.orelse):
                        if isinstance(branch, ast.Constant) and isinstance(branch.value, str):
                            pairs.append((keyword.arg, branch.value))
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Subscript):
            target = node.targets[0]
            if isinstance(target.value, ast.Subscript) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                pairs.append((ast.unparse(target.slice).strip("'\""), node.value.value))
    return pairs


def base_element(name):
    name = re.sub(r"\[\d+\]$", "", name)
    return name[:-len("_raw")] if name.endswith("_raw") else name


class MappingTests(unittest.TestCase):
    def test_every_mapped_element_exists(self):
        names = element_names()
        missing = sorted({value for _, value in mapped_values() if base_element(value) not in names})
        self.assertEqual(missing, [])

    def test_mapped_components_exist(self):
        mappings_source = re.sub(r"#[^\n]*", "", (SCRIPT / "Mappings.py").read_text())
        surface_source = (SCRIPT / "CustomMaschineMK3.py").read_text()
        component_map = set(re.findall(r'^\s*"(\w+)":', surface_source, re.MULTILINE))
        component_map |= set(re.findall(r'component_map\["(\w+)"\]', surface_source))
        used = set(re.findall(r'component = "(\w+)"', mappings_source))
        used |= {name for name in re.findall(r'mappings\["(\w+)"\] = dict', mappings_source) if not name.endswith("_Modes")}
        unknown = sorted(used - component_map - FRAMEWORK_COMPONENTS)
        self.assertEqual(unknown, [])

    def test_scene_launch_controls_are_mapped(self):
        values = dict(mapped_values())
        self.assertEqual(values["next_scene_button"], "right_with_scene")
        self.assertEqual(values["prev_scene_button"], "left_with_scene")
        self.assertEqual(values["pedal_input"], "pedaltip")


if __name__ == "__main__":
    unittest.main()
