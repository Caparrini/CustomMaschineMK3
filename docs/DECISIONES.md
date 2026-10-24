# Registro de decisiones de diseño

Formato ADR (Architecture Decision Record). Cada decisión tiene un número correlativo que no se reutiliza.
Una decisión aceptada no se edita: si cambia, se crea una nueva con estado «Aceptada» y la antigua pasa a «Sustituida por ADR-NNN».

Estados: **Propuesta** · **Aceptada** · **Rechazada** · **Sustituida por ADR-NNN**

## Índice

| ADR | Título | Estado | Fecha | Issue |
| --- | --- | --- | --- | --- |
| 001 | Base del desarrollo: CustomMaschineMK3 en modo MIDI | Aceptada | 2026-10-24 | — |
| 002 | Modelo de ramas | Aceptada | 2026-10-24 | — |
| 003 | Documentación del fork fuera de las contribuciones al original | Aceptada | 2026-10-24 | — |
| 004 | Configuración específica de la banda separada del código general | Aceptada | 2026-10-24 | T-09 |
| 005 | Bancos de parámetros para plugins de terceros | Aceptada | 2026-10-24 | T-03 |
| 006 | Pantalla limitada a texto Mackie Control de 4×28 | Aceptada | 2026-10-24 | — |
| 007 | Pruebas manuales mínimas y agrupadas | Aceptada | 2026-10-24 | T-11 |
| 008 | Control de escenas para el directo | Aceptada | 2026-10-24 | T-04 |
| 009 | Objetivo: flujo de trabajo y creatividad, además del directo | Aceptada | 2026-10-24 | T-12 |

---

## ADR-001 — Base del desarrollo: CustomMaschineMK3 en modo MIDI

- **Estado:** Aceptada · **Fecha:** 2026-10-24
- **Contexto:** se valoraron tres vías: (a) el script de pago de elton47, (b) CustomMaschineMK3 (GPL-3.0), (c) un puente HID propio con acceso a las pantallas gráficas. La vía (c) exige suspender los drivers de NI, un proceso externo en el directo y mantenimiento de ingeniería inversa.
- **Decisión:** partir de CustomMaschineMK3 y trabajar exclusivamente en modo MIDI, dentro de Ableton Live.
- **Consecuencias:** sin gráficos en pantalla, sin páginas NKS, sensibilidad de pads limitada por el modo MIDI. A cambio, ningún software externo en el directo y posibilidad de contribuir al original.

## ADR-002 — Modelo de ramas

- **Estado:** Aceptada · **Fecha:** 2026-10-24
- **Decisión:**
  - `main`: espejo del original. Solo recibe sincronizaciones desde `upstream/main`.
  - `develop`: integración del fork. Destino de todos los PR internos.
  - `live-stable`: versión aprobada para concierto. Solo recibe merges desde `develop` tras superar la prueba de ensayo. Se crea con la primera versión candidata.
  - Ramas de trabajo: `feat/`, `fix/`, `docs/` + número de issue, desde `develop`.
- **Consecuencias:** las contribuciones al original salen de `main` y no arrastran cambios propios.

## ADR-003 — Documentación del fork fuera de las contribuciones al original

- **Estado:** Aceptada · **Fecha:** 2026-10-24
- **Decisión:** `CLAUDE.md`, `docs/`, plantillas de `.github/` y `CHANGELOG.md` existen solo en `develop` y `live-stable`. Nunca se incluyen en ramas de PR al original.

## ADR-004 — Configuración específica de la banda separada del código general

- **Estado:** Aceptada · **Fecha:** 2026-10-24 · **Issue:** T-09
- **Contexto:** los bancos de plug-ins propios y los mapeos de canciones no interesan al original y mezclarlos con el código impediría aportarlo.
- **Decisión:** la configuración de la banda son archivos de datos JSON en la carpeta del script, leídos de forma opcional por código general. Si no existen, el script se comporta como el original. El primero es `plugin_banks.json` (ADR-005). El código incluye un ejemplo genérico (`plugin_banks.example.json`) que sí es aportable.
- **Alternativas descartadas:** módulo Python con la configuración (ejecuta código, más fácil de romper al editarlo a mano); ajustes en `settings.json` (lo gestiona el modo SETTINGS y no está versionado).
- **Consecuencias:** los cambios en los JSON requieren recargar la superficie de control. Un JSON inválido se ignora con un aviso en el log, sin afectar al resto.

## ADR-005 — Bancos de parámetros para plugins de terceros

- **Estado:** Aceptada · **Fecha:** 2026-10-24 · **Issue:** T-03
- **Contexto:** Live busca los bancos por `class_name`, y todos los plug-ins comparten `PluginDevice` (VST) o `AuPluginDevice` (AU), así que no se distingue Serum de Massive X. Valores comprobados en los scripts de Live 12 (`FaderfoxHelper`); los scripts de Live para Komplete Kontrol identifican plug-ins por el principio del nombre del dispositivo.
- **Decisión:**
  - `PluginBanks.py` elige el banco de un plug-in por el principio de su nombre de dispositivo, sin distinguir mayúsculas; gana el prefijo más largo.
  - Se envuelve el `BankingInfo` de Live (`PluginAwareBankingInfo`): para un plug-in con definición, las cinco consultas de bancos ven esa definición como si fuera la de su `class_name`; para todo lo demás no cambia nada.
  - Se instala en `CustomDeviceComponent._setup_bank`, antes del primer banco. Si falla, se registra y se mantiene el comportamiento original.
  - Los parámetros se nombran por su nombre original en el plug-in. Para obtenerlos, al seleccionar un plug-in se escribe `plugin_parameters/<nombre>.txt` (`Config.PLUGIN_PARAMETER_DUMP`).
- **Restricción conocida:** Live solo expone los parámetros de un plug-in si su número no supera `_PluginAutoPopulateThreshold` (64 por defecto) o si se han añadido en modo Configure. Un nombre no expuesto deja vacío ese encoder, sin error.
- **Consecuencias:** cambiar el nombre del dispositivo en Live puede hacer que deje de coincidir. Cambios en `plugin_banks.json` requieren recargar la superficie de control.

## ADR-006 — Pantalla limitada a texto Mackie Control de 4×28

- **Estado:** Aceptada · **Fecha:** 2026-10-24
- **Contexto:** `DisplayDefinitions.py` envía texto por sysex con cabecera Mackie Control: 4 líneas de 28 caracteres.
- **Decisión:** todo diseño de pantalla se ajusta a 4×28. Cualquier propuesta que lo supere requiere un ADR nuevo.

## ADR-007 — Pruebas manuales mínimas y agrupadas

- **Estado:** Aceptada · **Fecha:** 2026-10-24 · **Issue:** T-11
- **Contexto:** la única forma de comprobar el script en Live es con la MK3 conectada, y el tiempo de quien prueba es el recurso más caro del proyecto. Una checklist de regresión de 162 casos o un proyecto de pruebas dedicado no son asumibles.
- **Decisión:**
  - Todo lo verificable sin Live se verifica con pruebas automáticas (`tests/`) contra el código de bancos de Live 12.
  - Todo código nuevo que toque el framework falla de forma segura: registra el error y conserva el comportamiento original.
  - La prueba manual es una sola: `docs/pruebas/PRUEBA_MINIMA.md`, menos de 5 minutos, una vez por versión candidata, con como mucho 3 pasos específicos por PR acumulado. Solo se anotan los fallos.
  - Se usa un proyecto real de la banda; no hay proyecto de pruebas.
  - Los cambios solo de documentación no requieren prueba manual.
  - `docs/FUNCIONES.md` es inventario de referencia, no checklist.
- **Alternativas descartadas:** checklist completa por PR (horas por versión); proyecto de Live de pruebas versionado (mantenimiento y tiempo de montaje).
- **Consecuencias:** una regresión en una función no cubierta por la prueba mínima puede llegar al ensayo; por eso `live-stable` solo avanza tras un ensayo, y la versión anterior se recupera copiando su carpeta.

## ADR-008 — Control de escenas para el directo

- **Estado:** Aceptada · **Fecha:** 2026-10-24 · **Issue:** T-04
- **Contexto:** la banda toca en Session View con escenas que llevan click y fondos. El original solo lanza las 4 escenas visibles (SCENE + pad 4, 8, 12, 16), lo que obliga a mover el recuadro durante la canción. En Live, las Follow Actions de escena no mueven la escena seleccionada, de modo que un «lanzar la seleccionada y avanzar» manual se desincroniza tras una Follow Action; para resolverlo se venden dispositivos de Max for Live específicos ([guía de Ableton Drummer](https://blog.abletondrummer.com/how-to-play-next-scene-automatically/)).
- **Criterios:**
  1. Una sola acción por cambio de parte, sin mirar la pantalla y sin cambiar de modo.
  2. Correcto aunque la escena se haya lanzado con el ratón o con Follow Actions.
  3. No quitar ninguna función existente.
  4. Sin conocer la estructura de cada canción: válido tanto para una escena por canción como para varias.
  5. Fallo seguro (ADR-007).
- **Decisión:**
  - SCENE + ▶ / ◀: lanzar la escena siguiente / anterior a la última que se lanzó por cualquier vía (se sigue `is_triggered` de todas las escenas); antes del primer lanzamiento, relativo a la escena seleccionada. Selecciona la escena, mueve el recuadro lo mínimo y muestra su nombre.
  - Pedal: ajuste opcional «Pedal Function» = «Next Scene» (por defecto «Sustain», como el original). Con él, cada pisada equivale a SCENE + ▶, con 0,3 s de antirrebote.
  - SCENE + ◀ / ▶ estaban libres: SCENE solo se usaba con los pads 4, 8, 12 y 16.
- **Alternativas descartadas:**
  - SCENE + pads 1–16 para 16 escenas: sigue dependiendo de la posición del recuadro y exige mirar los pads.
  - Modo directo dedicado con canciones en los grupos A–H: requiere una convención de nombres de escena por canción y sustituye la vista de sesión de los grupos.
  - Activar `link_session_ring_to_scene_selection` del framework: cambia el comportamiento del original en todos los modos.
- **Consecuencias:** saltar a otra canción sigue haciéndose con el ratón o con el encoder y los pads. Si la banda lo necesita, se añade como opción nueva.

## ADR-009 — Objetivo: flujo de trabajo y creatividad, además del directo

- **Estado:** Aceptada · **Fecha:** 2026-10-24 · **Issue:** T-12
- **Contexto:** el proyecto se planteó para el directo de la banda, pero su objetivo principal es mejorar el flujo de trabajo y la creatividad con la MK3 en Live, más cerca del uso nativo de Maschine.
- **Decisión:**
  - Las mejoras se priorizan por cuánto evitan el ratón y la pantalla del ordenador mientras se produce, y por su riesgo para la respuesta del controlador.
  - `live-stable` (ADR-002) es la versión estable de uso diario, no solo de concierto. Pasa a ella tras la prueba mínima y una sesión de uso real.
  - Criterios para incorporar una función: (1) evita una acción con ratón frecuente al producir; (2) no quita funciones del original; (3) no añade tráfico MIDI continuo (el original espera 0,5 ms tras cada mensaje a la MK3, `_do_send_midi`); (4) cabe en la pantalla de 4×28.
- **Aplicación (T-12):**
  - Incorporadas: abrir y cerrar la ventana del plug-in (SHIFT + PLUG-IN), duplicar escena (DUPLICATE + SCENE + pad), tempo en el navegador (encoders 2 y 3).
  - Descartadas: medidores en los pads (criterio 3: mensajes continuos a los pads); color de pads de Drum Rack por nombre (el original ya muestra el color de cada cadena, que se elige en Live); navegador integrado con la vista del navegador de Live (el autor del original lo deja como limitación y no se conoce soporte en la API de scripts); más controles mapeables (el modo CHANNEL ya ofrece 16).

---

## Plantilla

```markdown
## ADR-NNN — Título

- **Estado:** Propuesta · **Fecha:** AAAA-MM-DD · **Issue:** #N
- **Contexto:** problema y restricciones.
- **Decisión:** qué se hace.
- **Alternativas descartadas:** cuáles y por qué.
- **Consecuencias:** qué se gana, qué se pierde, qué hay que vigilar.
```
