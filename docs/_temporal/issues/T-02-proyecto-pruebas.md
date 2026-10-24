# T-02 · [F0] Proyecto de Live de pruebas reproducible

- **Estado:** Descartado
- **Fase:** 0 · **Prioridad:** 1
- **Etiquetas:** tipo: prueba
- **Rama:** —
- **Issue de GitHub:** pendiente de migrar

## Resolución
Descartado por ADR-007: la prueba mínima usa un proyecto real de la banda. Montar y mantener un proyecto de pruebas cuesta más tiempo de prueba del que ahorra.

## Contexto
Para que las pruebas sean reproducibles todas deben hacerse sobre el mismo proyecto de Live.

## Comportamiento esperado
Proyecto de Live con: pistas MIDI con Simpler (clásico y Slicing), Drum Rack, Wavetable, Meld, EQ Eight, Hybrid Reverb, los VST del directo, al menos 8 escenas y retornos.

## Criterios de aceptación
- [ ] Proyecto guardado en `docs/pruebas/proyecto-pruebas/` sin samples pesados (samples de Core Library o recogidos con «Collect All and Save» si son pequeños)
- [ ] Documentado en `docs/pruebas/README.md` qué contiene cada pista y para qué prueba sirve

## Candidata a contribución al original
No

## Registro de trabajo

<!-- Una entrada por sesión, formato de docs/FLUJO_DE_TRABAJO.md, apartado 3 -->
