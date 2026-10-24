# CLAUDE.md — Instrucciones para Claude en este repositorio

Fork de [chiakibeats/CustomMaschineMK3](https://github.com/chiakibeats/CustomMaschineMK3) mantenido en `Caparrini/CustomMaschineMK3`.
Objetivo: adaptar el remote script de Ableton Live para la Maschine MK3 al directo de la banda y devolver al proyecto original, mediante pull requests, las mejoras de interés general.

Idioma de trabajo: castellano (España) en issues, commits, documentación y comentarios nuevos. Los PR al repositorio original se redactan en inglés.

## Documentos que hay que leer antes de tocar código

| Documento | Para qué |
| --- | --- |
| `docs/FLUJO_DE_TRABAJO.md` | Ciclo de vida de un issue, ramas, pruebas, definición de terminado |
| `docs/DECISIONES.md` | Decisiones de diseño vigentes (ADR). No contradecir una decisión aceptada sin abrir una nueva que la sustituya |
| `CHANGELOG.md` | Cambios por versión |

## Reglas obligatorias

1. **Ningún cambio sin issue.** Si la tarea no tiene issue, se crea primero con la plantilla correspondiente.
2. **Una rama por issue** desde `develop`: `feat/<n>-<nombre-corto>`, `fix/<n>-<nombre-corto>`, `docs/<n>-<nombre-corto>`.
3. **Commits** en imperativo y con referencia al issue: `Añade banco de parámetros de Serum (#3)`.
4. **Al terminar una sesión de trabajo**, añadir un comentario de registro en el issue (formato en `docs/FLUJO_DE_TRABAJO.md`): qué se ha hecho, qué falta, qué se ha probado y resultado.
5. **Toda decisión de diseño** que afecte a más de un archivo, a la interacción con el hardware o a la compatibilidad con el original se registra en `docs/DECISIONES.md` en el mismo PR.
6. **`CHANGELOG.md`** se actualiza en la sección «Sin publicar» en cada PR que cambie comportamiento.
7. **No modificar** `Template/` (plantillas de Controller Editor) sin un issue específico: cambiar asignaciones MIDI rompe la compatibilidad con la plantilla instalada en el hardware.
8. **Cabecera de licencia GPL-3.0** en todo archivo nuevo, siguiendo el formato de los existentes. No eliminar el copyright de chiaki.
9. **No afirmar que algo funciona** si no se ha probado en Live con el hardware. Claude solo puede hacer comprobaciones estáticas; el resultado funcional lo registra una persona.

## Contexto técnico verificado en el código

- **Framework:** API `ableton.v3` de remote scripts de Live (algún componente usa `ableton.v2`). La API no tiene documentación oficial; la referencia es el propio código del script y los scripts de Live.
- **Punto de entrada:** `CustomMaschineMK3/__init__.py` (`get_capabilities`, `create_instance`). Identifica MK3 (USB `0x17CC:0x1600`) y Maschine Plus (`0x17CC:0x1820`).
- **Clase principal:** `CustomMaschineMK3/CustomMaschineMK3.py`.
- **Elementos de hardware:** `ControlElements.py`. **Asignación de elementos a componentes y modos:** `Mappings.py`.
- **Configuración:** `Config.py` (`LOGGING`, `LOG_LEVEL`, `LCD_ENABLED`).
- **Logs:** con `LOGGING = True`, el script escribe `CustomMaschineMK3.log` en su propia carpeta. Los errores de Python no capturados aparecen en `Log.txt` de Live.
- **Pantalla:** texto por sysex con cabecera de protocolo Mackie Control, **4 líneas de 28 caracteres** (`DisplayDefinitions.py`: `LCD_LINES`, `LCD_LINE_LENGTH`). Sin gráficos.
- **Bancos de parámetros:** `CUSTOM_BANK_DEFINITIONS` en `CustomDeviceComponent.py`, indexado por `class_name` del dispositivo de Live (`OriginalSimpler`, `InstrumentVector`, `Eq8`, `Hybrid`...). Los decoradores (`*DeviceDecorator`) exponen parámetros especiales como parámetros normales.
- **Shift:** se recibe por sysex (`SysexShiftButton.py`).

## Comprobaciones que Claude puede hacer

- Sintaxis: `python3 -m py_compile CustomMaschineMK3/*.py`. Los módulos `ableton.*` y `Live` no existen fuera de Live, así que no se pueden importar ni ejecutar pruebas unitarias.
- Revisión de coherencia: nombres de elementos usados en `Mappings.py` que existan en `ControlElements.py`; claves de bancos que existan como `class_name`.
- Todo lo demás requiere prueba manual según `docs/FLUJO_DE_TRABAJO.md`.

## Contribución al original

- Las ramas para PR al original salen de `main` (espejo del original), nunca de `develop`.
- No incluyen `CLAUDE.md`, `docs/`, configuración específica de la banda ni cambios en `CHANGELOG.md` del fork.
- Antes de programar una contribución, se propone en un issue del repositorio original.
