# CLAUDE.md — Instrucciones para Claude en este repositorio

Fork de [chiakibeats/CustomMaschineMK3](https://github.com/chiakibeats/CustomMaschineMK3) mantenido en `Caparrini/CustomMaschineMK3`.
Objetivo: mejorar el flujo de trabajo y la creatividad con la Maschine MK3 en Ableton Live, en producción y en el directo de la banda (ADR-009), y devolver al proyecto original, mediante pull requests, las mejoras de interés general.

Idioma de trabajo: castellano (España) en issues, commits, documentación y comentarios nuevos. Los PR al repositorio original se redactan en inglés.

## Documentos que hay que leer antes de tocar código

| Documento | Para qué |
| --- | --- |
| `docs/FLUJO_DE_TRABAJO.md` | Ciclo de vida de un issue, ramas, pruebas, definición de terminado |
| `docs/DECISIONES.md` | Decisiones de diseño vigentes (ADR). No contradecir una decisión aceptada sin abrir una nueva que la sustituya |
| `CHANGELOG.md` | Cambios por versión |
| `docs/FUNCIONES.md` | Qué hace cada control, con IDs `R-xxx` para citar funciones |
| `docs/pruebas/PRUEBA_MINIMA.md` | Única prueba manual, por versión candidata |
| `docs/pruebas/VERSION_CANDIDATA.md` | Pasos manuales específicos acumulados para la próxima prueba |

## Provisional: seguimiento sin GitHub Issues

Mientras los issues no estén activos en el fork, los issues son los archivos de `docs/_temporal/issues/` (`T-NN`) y el tablero es `docs/_temporal/TABLERO.md`. En las reglas siguientes, «issue» equivale a `T-NN`, `#n` a `T-NN` y «comentario de registro» a una entrada en la sección «Registro de trabajo» del archivo. Detalle en `docs/_temporal/README.md`. Esta sección se elimina al migrar.

## Reglas obligatorias

1. **Ningún cambio sin issue.** Si la tarea no tiene issue, se crea primero con la plantilla correspondiente.
2. **Una rama por issue** desde `develop`: `feat/<n>-<nombre-corto>`, `fix/<n>-<nombre-corto>`, `docs/<n>-<nombre-corto>`.
3. **Commits** en imperativo y con referencia al issue: `Añade banco de parámetros de Serum (#3)`.
4. **Al terminar una sesión de trabajo**, añadir un comentario de registro en el issue (formato en `docs/FLUJO_DE_TRABAJO.md`): qué se ha hecho, qué falta, qué se ha probado y resultado.
5. **Toda decisión de diseño** que afecte a más de un archivo, a la interacción con el hardware o a la compatibilidad con el original se registra en `docs/DECISIONES.md` en el mismo PR.
6. **`CHANGELOG.md`** se actualiza en la sección «Sin publicar» en cada PR que cambie comportamiento.
7. **No modificar** `Template/` (plantillas de Controller Editor) sin un issue específico: cambiar asignaciones MIDI rompe la compatibilidad con la plantilla instalada en el hardware.
8. **Cabecera de licencia GPL-3.0** en todo archivo nuevo, siguiendo el formato de los existentes. No eliminar el copyright de chiaki.
9. **No afirmar que algo funciona** si no se ha probado en Live con el hardware. Claude solo puede hacer comprobaciones estáticas y pruebas sin Live; el resultado funcional lo registra una persona.
10. **El tiempo de prueba manual es el recurso más caro** (ADR-007). Antes de pedir una prueba: verificar todo lo posible sin Live, contrastar cada llamada al framework con los scripts de Live 12, hacer que todo código nuevo que toque el framework falle de forma segura y dejar como mucho 3 pasos manuales por PR, agrupados en la prueba mínima de la siguiente versión candidata.

## Contexto técnico verificado en el código

- **Framework:** API `ableton.v3` de remote scripts de Live (algún componente usa `ableton.v2`). La API no tiene documentación oficial; la referencia es el propio código del script y los scripts de Live.
- **Punto de entrada:** `CustomMaschineMK3/__init__.py` (`get_capabilities`, `create_instance`). Identifica MK3 (USB `0x17CC:0x1600`) y Maschine Plus (`0x17CC:0x1820`).
- **Clase principal:** `CustomMaschineMK3/CustomMaschineMK3.py`.
- **Elementos de hardware:** `ControlElements.py`. **Asignación de elementos a componentes y modos:** `Mappings.py`.
- **Configuración:** `Config.py` (`LOGGING`, `LOG_LEVEL`, `LCD_ENABLED`, `PLUGIN_PARAMETER_DUMP`).
- **Logs:** con `LOGGING = True`, el script escribe `CustomMaschineMK3.log` en su propia carpeta. Los errores de Python no capturados aparecen en `Log.txt` de Live.
- **Pantalla:** texto por sysex con cabecera de protocolo Mackie Control, **4 líneas de 28 caracteres** (`DisplayDefinitions.py`: `LCD_LINES`, `LCD_LINE_LENGTH`). Sin gráficos.
- **Bancos de parámetros:** `CUSTOM_BANK_DEFINITIONS` en `CustomDeviceComponent.py`, indexado por `class_name` del dispositivo de Live (`OriginalSimpler`, `InstrumentVector`, `Eq8`, `Hybrid`...). Los decoradores (`*DeviceDecorator`) exponen parámetros especiales como parámetros normales.
- **Bancos de plug-ins:** `PluginBanks.py` (ADR-005); datos de la banda en `CustomMaschineMK3/plugin_banks.json` (ADR-004), ejemplo en `plugin_banks.example.json`; guía en `docs/BANCOS_DE_PLUGINS.md`.
- **Escenas:** `SceneLaunchComponent.py` (componente) y `SceneLaunchLogic.py` (lógica sin framework, probada en `tests/`); ADR-008; guía en `docs/DIRECTO.md`.
- **Ventana de dispositivo:** `DeviceWindowComponent.py` (SHIFT + PLUG-IN). **Duplicar escena:** `CustomSessionComponent.py`.
- **Shift:** se recibe por sysex (`SysexShiftButton.py`).
- **Ajustes de usuario:** `settings.json` en la carpeta del script (`SettingsComponent.py`), no versionado.
- **Notificaciones:** mensajes temporales de 1,5 s en pantalla (`DisplayDefinitions.py`, `Notifications`); el cambio de dispositivo y de banco ya se notifica.

## Comprobaciones que Claude puede hacer

- `tests/run_tests.sh <scripts de Live 12 descompilados>`: compila todo el script y ejecuta las pruebas sin Live contra el código de bancos de Live (ver `tests/README.md`). Los scripts descompilados están en https://github.com/gluon/AbletonLive12_MIDIRemoteScripts (corresponden a Live 12.0; el script exige 12.1.10 o posterior, así que pueden diferir).
- Contrastar cada clase o método del framework que se use o se sobrescriba con esos scripts descompilados.
- Revisión de coherencia: nombres de elementos usados en `Mappings.py` que existan en `ControlElements.py`; claves de bancos que existan como `class_name`.
- Lo que dependa de Live o del hardware se deja como paso manual en el PR (regla 10).

## Contribución al original

- Las ramas para PR al original salen de `main` (espejo del original), nunca de `develop`.
- No incluyen `CLAUDE.md`, `docs/`, `tests/`, configuración específica de la banda ni cambios en `CHANGELOG.md` del fork.
- Antes de programar una contribución, se propone en un issue del repositorio original.
