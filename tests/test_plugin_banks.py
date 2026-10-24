# ==================================================
#
# This file is part of CustomMaschineMK3.
# CustomMaschineMK3 is free software licensed under GPL-3.0.
# For more details, see "LICENSE" file.
#
# Copyright (C) 2026 Caparrini
#
# ==================================================

# Offline tests for CustomMaschineMK3/PluginBanks.py.
#
# They run the plug-in bank logic against Live's own banking code (ableton.v2 / ableton.v3
# banking_util and device_parameter_bank), loaded from a harness folder outside this
# repository. See tests/README.md for how to build the harness.
#
# Run: HARNESS=<harness folder> python3 -m unittest tests/test_plugin_banks.py

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

HARNESS = os.environ.get("HARNESS")
if not HARNESS:
    raise SystemExit("Set HARNESS to the harness folder (see tests/README.md)")
sys.path.insert(0, HARNESS)

from CustomMaschineMK3 import Config, PluginBanks as pb  # noqa: E402
from ableton.v3.control_surface import BankingInfo, create_parameter_bank  # noqa: E402
from ableton.v3.control_surface.banking_util import DescribedDeviceParameterBank  # noqa: E402


class FakeParameter:
    def __init__(self, name):
        self.name = name
        self.original_name = name


class FakeDevice:
    def __init__(self, name, class_name, parameter_names):
        self.name = name
        self.class_name = class_name
        self.parameters = [FakeParameter("Device On")] + [FakeParameter(n) for n in parameter_names]


SERUM_PARAMETERS = ["A Vol", "A Pan", "A Octave", "B Vol", "B Pan", "Fil Cutoff", "Fil Reso", "Env1 Atk", "Env1 Dec"]
BANKS_JSON = {
    "Serum": {
        "Oscillators": ["A Vol", "A Pan", "A Octave", "", "B Vol", "B Pan"],
        "Filter": ["Fil Cutoff", "Fil Reso", "Does Not Exist"],
    },
    "Serum FX": {"Main": ["Mix"]},
    "Broken": "not an object",
    "": {"X": ["A"]},
    "Too long": {"Bank": ["1", "2", "3", "4", "5", "6", "7", "8", "9"]},
}
NATIVE_DEFINITIONS = {"OriginalSimpler": pb.IndexedDict([("Main", {pb.BANK_PARAMETERS_KEY: ("Start",)})])}


def make_info():
    return pb.PluginAwareBankingInfo(NATIVE_DEFINITIONS, pb.parse_plugin_banks(BANKS_JSON), bank_size = 8)


def names(bank):
    return [parameter.name if parameter else None for parameter, _ in bank.parameters]


class ParseTests(unittest.TestCase):
    def test_invalid_entries_are_skipped(self):
        prefixes = [prefix for prefix, _ in pb.parse_plugin_banks(BANKS_JSON)]
        self.assertEqual(prefixes, ["serum fx", "too long", "serum"])

    def test_banks_are_padded_and_truncated_to_8(self):
        banks = dict(pb.parse_plugin_banks(BANKS_JSON))
        self.assertEqual(len(banks["serum"]["Filter"][pb.BANK_PARAMETERS_KEY]), 8)
        self.assertEqual(banks["too long"]["Bank"][pb.BANK_PARAMETERS_KEY], tuple("12345678"))

    def test_top_level_not_object(self):
        self.assertEqual(pb.parse_plugin_banks(["x"]), [])

    def test_missing_and_invalid_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder, "plugin_banks.json")
            self.assertEqual(pb.load_plugin_banks(path), [])
            path.write_text("{ not json", encoding = "utf-8")
            self.assertEqual(pb.load_plugin_banks(path), [])
            path.write_text(json.dumps(BANKS_JSON), encoding = "utf-8")
            self.assertEqual(len(pb.load_plugin_banks(path)), 3)


class MatchingTests(unittest.TestCase):
    def test_prefix_case_insensitive_longest_wins(self):
        banks = pb.parse_plugin_banks(BANKS_JSON)
        serum = pb.find_plugin_definition(FakeDevice("serum (2)", "PluginDevice", []), banks)
        serum_fx = pb.find_plugin_definition(FakeDevice("Serum FX", "PluginDevice", []), banks)
        self.assertEqual(list(serum.keys()), ["Oscillators", "Filter"])
        self.assertEqual(list(serum_fx.keys()), ["Main"])

    def test_au_plugins_match(self):
        banks = pb.parse_plugin_banks(BANKS_JSON)
        self.assertIsNotNone(pb.find_plugin_definition(FakeDevice("Serum", "AuPluginDevice", []), banks))

    def test_native_device_with_same_name_does_not_match(self):
        banks = pb.parse_plugin_banks(BANKS_JSON)
        self.assertIsNone(pb.find_plugin_definition(FakeDevice("Serum", "OriginalSimpler", []), banks))

    def test_unknown_plugin_and_none(self):
        banks = pb.parse_plugin_banks(BANKS_JSON)
        self.assertIsNone(pb.find_plugin_definition(FakeDevice("Massive X", "PluginDevice", []), banks))
        self.assertIsNone(pb.find_plugin_definition(None, banks))


class BankingTests(unittest.TestCase):
    def test_plugin_gets_described_bank_with_names(self):
        info = make_info()
        device = FakeDevice("Serum", "PluginDevice", SERUM_PARAMETERS)
        bank = create_parameter_bank(device, info)
        self.assertIsInstance(bank, DescribedDeviceParameterBank)
        self.assertEqual(info.device_bank_count(device), 2)
        self.assertEqual(list(info.device_bank_names(device)), ["Oscillators", "Filter"])
        self.assertEqual(bank.name, "Oscillators")
        self.assertEqual(names(bank), ["A Vol", "A Pan", "A Octave", None, "B Vol", "B Pan", None, None])
        bank.index = 1
        self.assertEqual(bank.name, "Filter")
        self.assertEqual(names(bank), ["Fil Cutoff", "Fil Reso", None, None, None, None, None, None])

    def test_definitions_are_restored_after_each_call(self):
        info = make_info()
        info.device_bank_count(FakeDevice("Serum", "PluginDevice", SERUM_PARAMETERS))
        self.assertIs(info._bank_definitions, NATIVE_DEFINITIONS)

    def test_plugin_without_definition_keeps_live_behaviour(self):
        info = make_info()
        reference = BankingInfo(NATIVE_DEFINITIONS, bank_size = 8)
        device = FakeDevice("Massive X", "PluginDevice", SERUM_PARAMETERS)
        self.assertEqual(info.device_bank_count(device), reference.device_bank_count(device))
        self.assertEqual(list(info.device_bank_names(device)), list(reference.device_bank_names(device)))
        bank = create_parameter_bank(device, info)
        self.assertEqual(names(bank), SERUM_PARAMETERS[:8])

    def test_native_device_keeps_its_definition(self):
        info = make_info()
        device = FakeDevice("Simpler", "OriginalSimpler", ["Start", "End"])
        self.assertEqual(list(info.device_bank_names(device)), ["Main"])
        self.assertTrue(info.has_main_bank(device))

    def test_empty_plugin_banks_equal_live(self):
        info = pb.PluginAwareBankingInfo(NATIVE_DEFINITIONS, [], bank_size = 8)
        device = FakeDevice("Serum", "PluginDevice", SERUM_PARAMETERS)
        self.assertEqual(info.device_bank_count(device), 2)
        self.assertEqual(list(info.device_bank_names(device)), ["Bank 1", "Bank 2"])


class DumpTests(unittest.TestCase):
    def test_dump_writes_original_names_and_is_idempotent(self):
        device = FakeDevice("Serum: Lead/1", "PluginDevice", ["A Vol", "A Pan"])
        with tempfile.TemporaryDirectory() as folder:
            path = pb.dump_plugin_parameters(device, Path(folder))
            self.assertEqual(path.name, "Serum_ Lead_1.txt")
            lines = path.read_text(encoding = "utf-8").splitlines()
            self.assertEqual(lines[-2:], ["A Vol", "A Pan"])
            self.assertIn("# Parameters exposed by Live: 2", lines)
            mtime = path.stat().st_mtime_ns
            pb.dump_plugin_parameters(device, Path(folder))
            self.assertEqual(path.stat().st_mtime_ns, mtime)

    def test_dump_explains_unconfigured_plugin(self):
        device = FakeDevice("Massive X", "PluginDevice", [])
        with tempfile.TemporaryDirectory() as folder:
            text = pb.dump_plugin_parameters(device, Path(folder)).read_text(encoding = "utf-8")
            self.assertIn("Configure", text)

    def test_dump_ignores_native_devices_and_disabled_flag(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertIsNone(pb.dump_plugin_parameters(FakeDevice("Simpler", "OriginalSimpler", []), Path(folder)))
            Config.PLUGIN_PARAMETER_DUMP = False
            try:
                self.assertIsNone(pb.dump_plugin_parameters(FakeDevice("Serum", "PluginDevice", []), Path(folder)))
            finally:
                Config.PLUGIN_PARAMETER_DUMP = True

    def test_dump_never_raises(self):
        device = FakeDevice("Serum", "PluginDevice", [])
        self.assertIsNone(pb.dump_plugin_parameters(device, Path("/nonexistent/forbidden/folder")))


if __name__ == "__main__":
    unittest.main()
