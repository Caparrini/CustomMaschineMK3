#!/usr/bin/env bash
# Builds a test harness with Live's own banking code and runs the offline tests.
# Usage: tests/run_tests.sh <folder of the decompiled Live 12 MIDI Remote Scripts>
#   e.g. a clone of https://github.com/gluon/AbletonLive12_MIDIRemoteScripts
set -euo pipefail
REF="${1:?Path to the decompiled Live 12 MIDI Remote Scripts}"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
HARNESS="$(mktemp -d)"
trap 'rm -rf "$HARNESS"' EXIT

cp -r "$REPO/tests/stubs/." "$HARNESS/"
mkdir -p "$HARNESS/ableton/v2/base/collection" "$HARNESS/CustomMaschineMK3"
cp "$REF/ableton/v2/base/collection/indexed_dict.py" "$HARNESS/ableton/v2/base/collection/"
echo "from .indexed_dict import IndexedDict" > "$HARNESS/ableton/v2/base/collection/__init__.py"
cp "$REF/ableton/v2/control_surface/banking_util.py" "$REF/ableton/v2/control_surface/device_parameter_bank.py" "$HARNESS/ableton/v2/control_surface/"
cp "$REF/ableton/v3/control_surface/banking_util.py" "$HARNESS/ableton/v3/control_surface/"
# Decompiler artifacts: x[1[:None]] -> x[1:], x[None[:n]] -> x[:n], f)(a, ...) -> f)(*a, ...)
sed -i -E 's/\[([A-Za-z0-9_]+)\[:None\]\]/[\1:]/g; s/\[None\[:([^]]+)\]\]/[:\1]/g; s/__init__\)\(a, /__init__)(*a, /g' \
    "$HARNESS"/ableton/v2/control_surface/*.py "$HARNESS"/ableton/v3/control_surface/banking_util.py
for module in PluginBanks Config Logger SceneLaunchLogic SceneLaunchComponent; do
    cp "$REPO/CustomMaschineMK3/$module.py" "$HARNESS/CustomMaschineMK3/"
done
touch "$HARNESS/CustomMaschineMK3/__init__.py"

cd "$REPO"
python3 -m py_compile CustomMaschineMK3/*.py
HARNESS="$HARNESS" python3 -m unittest -v tests/test_plugin_banks.py tests/test_scene_launch.py tests/test_mappings.py
