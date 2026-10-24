# T-05 · [F2] Texto en pantalla: dispositivo, página y parámetros

- **Estado:** Backlog
- **Fase:** 2 · **Prioridad:** 2
- **Etiquetas:** tipo: mejora, upstream: candidata
- **Rama:** —
- **Issue de GitHub:** pendiente de migrar

## Contexto
La pantalla admite 4 líneas de 28 caracteres (ADR-006). Hay que aprovecharla para no mirar el ordenador.

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
