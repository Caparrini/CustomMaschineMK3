# T-03 · [F1] Bancos de parámetros para los VST del directo

- **Estado:** En pruebas
- **Fase:** 1 · **Prioridad:** 1
- **Etiquetas:** tipo: mejora, upstream: candidata
- **Rama:** `feat/T-03-bancos-vst`
- **Issue de GitHub:** pendiente de migrar

## Estado de los criterios (2026-10-24)
- [x] `class_name` verificado en los scripts de Live: `PluginDevice` (VST) y `AuPluginDevice` (AU), registrado en ADR-005. No hace falta comprobarlo en Live.
- [x] Banco funcional para los VST del directo: ordenando los parámetros con Configure en Live, sin datos de la banda; con nombres de página, mediante `plugin_banks.json` (opcional).
- [x] Parámetro no expuesto: deja el encoder vacío sin error (cubierto por prueba automática).
- [x] Documentado cómo exponer parámetros: `docs/BANCOS_DE_PLUGINS.md`.

## Pasos manuales para la próxima prueba mínima
Ninguno aparte de P4 y P5. La forma recomendada de preparar un plug-in es ordenar sus parámetros con Configure en Live, sin archivos (`docs/BANCOS_DE_PLUGINS.md`); `plugin_banks.json` es opcional y solo se probará si la banda lo usa.

## Contexto
Los bancos personalizados solo existen para dispositivos nativos (Simpler, Wavetable, EQ Eight, Hybrid Reverb, Meld). Para los VST del directo los encoders siguen el orden de parámetros que expone Live, poco útil para tocar.

## Comportamiento esperado
Al seleccionar un VST con banco definido, los 8 encoders controlan los parámetros elegidos por página, con nombres legibles en pantalla. Las páginas se recorren con los botones de banco del modo dispositivo.

## Criterios de aceptación
- [ ] Verificado en Live el `class_name` de un VST2, un VST3 y un AU (si aplica) y registrado en ADR-005
- [ ] Banco funcional para al menos dos VST del directo (por confirmar: Serum, Massive X)
- [ ] Un parámetro no expuesto por Live no provoca error: la posición queda vacía en pantalla
- [ ] Documentado cómo exponer parámetros (modo Configure / `_PluginAutoPopulateThreshold`)

## Archivos previsiblemente afectados
`CustomDeviceComponent.py`, módulo de configuración de la banda (T-09)

## Decisiones de diseño relacionadas
ADR-005, ADR-004

## Candidata a contribución al original
Parcial: el mecanismo de bancos por plugin sí; los bancos concretos de la banda no

## Registro de trabajo

<!-- Una entrada por sesión, formato de docs/FLUJO_DE_TRABAJO.md, apartado 3 -->

### Registro 2026-10-24
- **Hecho:** `PluginBanks.py` (bancos por nombre de plug-in desde `plugin_banks.json` y volcado de parámetros), enganche en `CustomDeviceComponent._setup_bank` con fallo seguro, `Config.PLUGIN_PARAMETER_DUMP`, ejemplo `plugin_banks.example.json`, guía `docs/BANCOS_DE_PLUGINS.md`, ADR-004 y ADR-005 aceptadas.
- **Verificación:** cada método sobrescrito o usado (`BankingInfo`, `create_parameter_bank`, `DescribedDeviceParameterBank`, `DeviceComponent._setup_bank`, `DeviceBankNavigationComponent._banking_info`) contrastado con los scripts descompilados de Live 12.0. `class_name` de plug-ins (`PluginDevice`, `AuPluginDevice`) comprobado en `FaderfoxHelper` de Live.
- **Pruebas automáticas:** `tests/run_tests.sh` correcto, 17 pruebas contra el código de bancos de Live.
- **Pendiente:** pasos manuales en la próxima prueba mínima; `plugin_banks.json` de la banda cuando se tengan los nombres de parámetros.
- **Decisiones tomadas:** ADR-004, ADR-005
