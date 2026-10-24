# T-03 · [F1] Bancos de parámetros para los VST del directo

- **Estado:** Backlog
- **Fase:** 1 · **Prioridad:** 1
- **Etiquetas:** tipo: mejora, upstream: candidata
- **Rama:** —
- **Issue de GitHub:** pendiente de migrar

## Contexto
Los bancos personalizados solo existen para dispositivos nativos (Simpler, Wavetable, EQ Eight, Hybrid Reverb, Meld). Para los VST del directo los encoders siguen el orden de parámetros que expone Live, poco útil para tocar.

## Comportamiento esperado
Al seleccionar un VST con banco definido, los 8 encoders controlan los parámetros elegidos por página, con nombres legibles en pantalla. Las páginas se recorren con los botones de banco del modo dispositivo.

## Criterios de aceptación
- [ ] Verificado en Live el `class_name` de un VST2, un VST3 y un AU (si aplica) y registrado en ADR-005
- [ ] Banco funcional para al menos dos VST del directo (por confirmar: Serum, Massive X)
- [ ] Un parámetro no expuesto por Live no provoca error: la posición queda vacía en pantalla
- [ ] Documentado cómo exponer parámetros (modo Configure / `_PluginAutoPopulateThreshold`)

## Archivos previsiblemente afectados
`CustomDeviceComponent.py`, módulo de configuración de la banda (T-09)

## Decisiones de diseño relacionadas
ADR-005, ADR-004

## Candidata a contribución al original
Parcial: el mecanismo de bancos por plugin sí; los bancos concretos de la banda no

## Registro de trabajo

<!-- Una entrada por sesión, formato de docs/FLUJO_DE_TRABAJO.md, apartado 3 -->
