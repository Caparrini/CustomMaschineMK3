# T-07 · [F3] Curva de velocidad configurable de los pads

- **Estado:** Descartado
- **Fase:** 3 · **Prioridad:** 2
- **Etiquetas:** tipo: mejora, upstream: candidata
- **Rama:** —
- **Issue de GitHub:** pendiente de migrar

## Resolución
No resoluble en el script. En los modos de teclado los pads se tocan en modo «playable»: Live recibe las notas directamente y el script no interviene en la velocidad (`MaschinePlayableComponent` solo traduce nota y canal). No se conoce en la API de remote scripts una forma de reescribir la velocidad de esas notas.

Alternativas sin desarrollo:
- Efecto MIDI **Velocity** de Live delante del instrumento, para subir el rango de salida.
- Velocidad fija: CHORDS (16 niveles) o FIXED VEL (acento a 127), ya disponibles.

Usuarios del foro de NI informan de que ni la sensibilidad máxima ni la curva «soft» resuelven el problema en modo MIDI; la única solución publicada usa la presión de los pads mediante scripting en FL Studio, no aplicable a Live.

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
