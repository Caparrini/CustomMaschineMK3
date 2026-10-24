# T-06 · [F2] Modo sampler ampliado sobre Simpler

- **Estado:** Descartado
- **Fase:** 2 · **Prioridad:** 2
- **Etiquetas:** tipo: mejora, upstream: candidata
- **Rama:** —
- **Issue de GitHub:** pendiente de migrar

## Resolución
Cubierto por el original, sin cambios de código. El banco de Simpler de `CustomDeviceComponent.py` ya incluye:
- «Main»: modo, inicio, fin y parámetros según el modo (Classic, One-Shot, Slicing).
- «Amplitude», «Filter Envelope», «Pitch Modifiers»: envolventes.
- «Sample & Warp»: ganancia, inicio, fin, warp, modo de warp y sus parámetros.
- Slices: modo Simpler en Slicing desde KEYBOARD (R-531 a R-534 en `docs/FUNCIONES.md`).
Si en el uso real falta algo concreto, se reabre con ese parámetro.

## Contexto
Objetivo: un flujo de sampler parecido al de Maschine sobre Simpler.

## Comportamiento esperado
Ampliar el banco de Simpler y su texto en pantalla: inicio, fin, envolvente, warp y slices, accesibles por páginas.

## Criterios de aceptación
- [ ] Edición completa de un sample sin mirar la pantalla del ordenador
- [ ] Funciona en modos Classic, One-Shot y Slicing

## Archivos previsiblemente afectados
`CustomDeviceComponent.py`, `CustomSlicedSimplerComponent.py`, `DisplayDefinitions.py`

## Candidata a contribución al original
Sí

## Registro de trabajo

<!-- Una entrada por sesión, formato de docs/FLUJO_DE_TRABAJO.md, apartado 3 -->
