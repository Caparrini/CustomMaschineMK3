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
| 004 | Configuración específica de la banda separada del código general | Propuesta | 2026-10-24 | ver issue de configuración |
| 005 | Bancos de parámetros para plugins de terceros | Propuesta | 2026-10-24 | ver issue de bancos VST |
| 006 | Pantalla limitada a texto Mackie Control de 4×28 | Aceptada | 2026-10-24 | — |

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

- **Estado:** Propuesta · **Fecha:** 2026-10-24
- **Contexto:** los bancos de plugins propios y los mapeos de canciones no interesan al original y dificultarían aportar el resto.
- **Propuesta:** un módulo propio (nombre por decidir) con los bancos y mapeos de la banda, cargado de forma opcional por el código general. Si no existe, el script se comporta como el original.
- **A decidir en el issue:** formato (módulo Python o JSON), ubicación y mecanismo de carga.

## ADR-005 — Bancos de parámetros para plugins de terceros

- **Estado:** Propuesta · **Fecha:** 2026-10-24
- **Contexto:** `CUSTOM_BANK_DEFINITIONS` indexa por `class_name`. Todos los plugins VST/AU comparten tipo de dispositivo en Live, por lo que la clave `class_name` no distingue Serum de Massive X. Pendiente de verificar en Live el valor exacto de `class_name` para VST2, VST3 y AU.
- **Propuesta:** para plugins, seleccionar el banco por nombre del dispositivo o del plugin, y nombrar los parámetros de cada banco por su nombre en Live.
- **Restricción conocida:** Live solo expone los parámetros de un plugin si su número no supera `_PluginAutoPopulateThreshold` (64 por defecto) o si se han añadido en modo Configure. Un banco que nombre un parámetro no expuesto debe degradar sin error.

## ADR-006 — Pantalla limitada a texto Mackie Control de 4×28

- **Estado:** Aceptada · **Fecha:** 2026-10-24
- **Contexto:** `DisplayDefinitions.py` envía texto por sysex con cabecera Mackie Control: 4 líneas de 28 caracteres.
- **Decisión:** todo diseño de pantalla se ajusta a 4×28. Cualquier propuesta que lo supere requiere un ADR nuevo.

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
