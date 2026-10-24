# Pruebas automáticas sin Live

Tres grupos de pruebas:

- `test_plugin_banks.py`: bancos de plug-ins ejecutados contra el código de bancos del propio Live (`ableton.v2` y `ableton.v3`, `banking_util` y `device_parameter_bank`), tomado de los scripts descompilados de Live 12.
- `test_scene_launch.py`: control de escenas (T-04) con objetos de Live simulados.
- `test_mappings.py`: análisis estático de que todo nombre de elemento usado en `Mappings.py` existe en `ControlElements.py` y todo componente está registrado. No necesita el entorno.

```bash
git clone --depth 1 https://github.com/gluon/AbletonLive12_MIDIRemoteScripts /ruta/ref
tests/run_tests.sh /ruta/ref
```

`run_tests.sh` monta un entorno temporal con:

- `tests/stubs/`: sustitutos mínimos de `ableton.v2.base`, de `Component`, `ButtonControl`, `InputControl` y `Renderable` de `ableton.v3`, y de los `__init__` de paquete, para no cargar el resto del framework ni el módulo `Live`.
- Los tres archivos del framework anteriores, con tres correcciones de artefactos del descompilador aplicadas con `sed`.
- Los módulos del script que se prueban.

Además compila todo `CustomMaschineMK3/*.py`.

Límites: los descompilados corresponden a Live 12.0 (marzo de 2024). Una prueba superada aquí no garantiza el comportamiento en la versión de Live instalada; para eso está la prueba mínima manual (`docs/pruebas/PRUEBA_MINIMA.md`).
