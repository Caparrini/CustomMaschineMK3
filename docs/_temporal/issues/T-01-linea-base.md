# T-01 · [F0] Línea base: inventario de funciones y checklist de regresión

- **Estado:** En pruebas
- **Fase:** 0 · **Prioridad:** 1
- **Etiquetas:** tipo: prueba
- **Rama:** `docs/T-01-linea-base`
- **Issue de GitHub:** pendiente de migrar

## Contexto
Antes de modificar nada hace falta saber qué hace hoy el script y poder detectar regresiones.

## Comportamiento esperado
Inventario de todas las funciones del script (a partir de la [documentación del original](https://chiakibeats.github.io/CustomMaschineDocs/docs/all-operations) y del código) convertido en checklist ejecutable a mano.

## Criterios de aceptación
- [x] `docs/pruebas/regresion.md` con una línea por función: modo, control, acción, resultado esperado
- [ ] Checklist ejecutada completa sobre `main` sin modificar, resultado registrado en este issue
- [x] Anotado qué hace hoy el script con: bancos de plugins de terceros, texto en pantalla por modo, velocidad de pads

## Archivos previsiblemente afectados
`docs/pruebas/regresion.md`

## Candidata a contribución al original
No

## Registro de trabajo

<!-- Una entrada por sesión, formato de docs/FLUJO_DE_TRABAJO.md, apartado 3 -->

### Registro 2026-10-24
- **Hecho:** `docs/pruebas/regresion.md` con 162 casos (3 requisitos previos y 159 en 16 secciones), extraídos de `Mappings.py`, `ControlElements.py`, `DisplayDefinitions.py` y `SettingsComponent.py`, contrastados con la documentación del original. Cada caso indica si está verificado en el código (M) o solo en la documentación (D).
- **Pendiente:** ejecución manual completa en Live con la MK3 (necesita el proyecto de pruebas de T-02).
- **Commit probado:** ninguno en hardware. Comprobación estática: `python3 -m py_compile CustomMaschineMK3/*.py` sin errores.
- **Entorno:** análisis de código, sin Live.
- **Hallazgos para otros issues:**
  - **Bancos de plugins de terceros (T-03):** `CUSTOM_BANK_DEFINITIONS` solo define Simpler, Wavetable, EQ Eight, Hybrid Reverb y Meld sobre las definiciones por defecto de Live. Un VST usa el orden de parámetros que expone Live, en bancos de 8.
  - **Texto en pantalla (T-05):** el modo dispositivo ya muestra nombres (6 caracteres) y valores de los 8 parámetros del banco, y al tocar un encoder muestra nombre completo y valor. Falta el nombre del dispositivo y del banco. T-05 debe reducirse a eso.
  - **Velocidad (T-07):** el script no transforma la velocidad de los pads; solo ofrece 16 niveles fijos (CHORDS) y acento a 127 (FIXED VEL). La velocidad llega tal cual desde la plantilla de Controller Editor.
  - **Pantalla:** se activa con `Config.LCD_ENABLED`; con ella desactivada los encoders usan otros CC (70–77 en lugar de 16–23).
  - **Ajustes:** se guardan en `settings.json` dentro de la carpeta del script; `sequencer_style` y `mixer_mode` requieren recargar.
- **Decisiones tomadas:** ninguna
