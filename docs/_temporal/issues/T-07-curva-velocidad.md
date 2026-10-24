# T-07 · [F3] Curva de velocidad configurable de los pads

- **Estado:** Backlog
- **Fase:** 3 · **Prioridad:** 2
- **Etiquetas:** tipo: mejora, upstream: candidata
- **Rama:** —
- **Issue de GitHub:** pendiente de migrar

## Contexto
En modo MIDI la respuesta de los pads es peor que con el software Maschine.

## Hallazgo de T-01 (2026-10-24)
El script no transforma la velocidad de los pads: llega tal cual desde la plantilla de Controller Editor. Antes de programar, comprobar si la plantilla (`Template/CustomMaschineMK3.ncm3`) permite ajustar la curva sin tocar el script; si es así, la solución puede ser solo de plantilla (requiere issue propio por la regla sobre `Template/`).

## Comportamiento esperado
Curva de velocidad seleccionable (al menos lineal, suave y dura) desde la configuración del script.

## Criterios de aceptación
- [ ] Verificado primero dónde entra la velocidad de los pads en el código y si es posible transformarla en el script
- [ ] Al menos 3 curvas seleccionables
- [ ] Golpe suave registrado de forma fiable con la curva suave

## Candidata a contribución al original
Sí

## Registro de trabajo

<!-- Una entrada por sesión, formato de docs/FLUJO_DE_TRABAJO.md, apartado 3 -->
