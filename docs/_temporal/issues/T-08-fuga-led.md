# T-08 · [F3] Corregir fuga de LED del modo de mapeo MIDI al modo teclado

- **Estado:** Backlog
- **Fase:** 3 · **Prioridad:** 3
- **Etiquetas:** tipo: fallo, upstream: candidata
- **Rama:** —
- **Issue de GitHub:** pendiente de migrar

## Análisis desde el código (2026-10-24)
- El modo CHANNEL traduce los 8 botones sobre las pantallas (notas 0–7) a los canales 2 y 3 según la página (`PageableBackgroundComponent`). Las notas C-2 a G-2 son las notas MIDI 0–7.
- El modo teclado traduce los pads al canal 9 (y 10 para notas fuera de rango) (`MaschinePlayableComponent`).
- Con esos datos no hay solapamiento evidente de canal y nota; la causa no se puede determinar sin reproducirlo. El autor del original lo tiene en investigación.
- Prioridad 3: no se pedirá prueba manual específica. Si aparece en un ensayo, anotar la secuencia exacta (modo anterior, mapeo usado en CHANNEL, nota tocada).

## Contexto
Incidencia conocida del original: el feedback de LED del modo de mapeo MIDI personalizado aparece en el modo teclado en las notas C-2 a G-2.

## Criterios de aceptación
- [ ] Reproducido y documentado en este issue
- [ ] Sin LED erróneos en ese rango tras la corrección
- [ ] Antes de programar, comprobado en el original si ya está corregido o en curso

## Candidata a contribución al original
Sí

## Registro de trabajo

<!-- Una entrada por sesión, formato de docs/FLUJO_DE_TRABAJO.md, apartado 3 -->
