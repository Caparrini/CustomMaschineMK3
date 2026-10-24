# T-05 · [F2] Texto en pantalla: dispositivo, página y parámetros

- **Estado:** Descartado
- **Fase:** 2 · **Prioridad:** 2
- **Etiquetas:** tipo: mejora, upstream: candidata
- **Rama:** —
- **Issue de GitHub:** pendiente de migrar

## Resolución
Cubierto por el original, sin cambios de código:
- Al cambiar de dispositivo y de banco, la pantalla muestra su nombre durante 1,5 s (`CustomDeviceNavigationComponent` notifica `Device.select`; `DeviceBankNavigationComponent` de Live notifica `Device.bank`).
- En modo dispositivo se ven nombres abreviados y valores de los 8 parámetros; al tocar un encoder, nombre completo y valor.
Mostrar el dispositivo de forma permanente exigiría quitar una línea de parámetros (ADR-006). Si la banda lo pide tras usarlo, se reabre con ese alcance.

## Contexto
La pantalla admite 4 líneas de 28 caracteres (ADR-006). Hay que aprovecharla para no mirar el ordenador.

## Hallazgo de T-01 (2026-10-24)
El modo dispositivo ya muestra en pantalla nombres abreviados y valores de los 8 parámetros, y el nombre completo y valor al tocar un encoder (`DisplayDefinitions.py`, `device_view` y `knob_control_view`). Lo que falta es identificar el dispositivo y el banco. El alcance de este issue se reduce a eso salvo que la banda pida otra cosa.

## Comportamiento esperado
En modo dispositivo: nombre del dispositivo y página, y nombres y valores de los 8 parámetros, abreviados de forma legible.

## Criterios de aceptación
- [ ] Diseño de las 4 líneas documentado en este issue antes de programar
- [ ] Lo mostrado coincide con Live tras cambiar de dispositivo, de página y de valor
- [ ] Sin parpadeos ni retrasos apreciables al girar un encoder

## Archivos previsiblemente afectados
`DisplayDefinitions.py`

## Decisiones de diseño relacionadas
ADR-006

## Candidata a contribución al original
Sí

## Registro de trabajo

<!-- Una entrada por sesión, formato de docs/FLUJO_DE_TRABAJO.md, apartado 3 -->
