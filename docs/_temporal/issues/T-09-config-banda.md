# T-09 · [F1] Configuración específica de la banda separada del código general

- **Estado:** En pruebas
- **Fase:** 1 · **Prioridad:** 1
- **Etiquetas:** tipo: mejora, upstream: candidata
- **Rama:** `feat/T-03-bancos-vst` (junto con T-03)
- **Issue de GitHub:** pendiente de migrar

## Resolución (2026-10-24)
Formato y carga decididos en ADR-004 (aceptada): archivos JSON de datos en la carpeta del script, opcionales. Primer archivo: `plugin_banks.json`. Implementado junto con T-03 porque el mecanismo y su primer uso son el mismo cambio.
- [x] Formato y mecanismo de carga decididos y ADR-004 aceptada
- [x] Sin el archivo, el comportamiento es el original (cubierto por prueba automática); con un JSON inválido, se ignora con aviso (cubierto por prueba automática). La carga en Live se comprueba con P4 y P5 de la prueba mínima.

## Contexto
Bancos de plugins propios y mapeos de canciones no interesan al original y mezclarlos con el código general impide aportarlo.

## Comportamiento esperado
Configuración específica de la banda en un módulo separado, cargado de forma opcional. Sin él, el script se comporta como el original.

## Criterios de aceptación
- [ ] Formato y mecanismo de carga decididos y ADR-004 pasada a «Aceptada»
- [ ] El script carga sin errores con y sin el módulo de la banda

## Decisiones de diseño relacionadas
ADR-004

## Candidata a contribución al original
Sí, el mecanismo de carga opcional

## Registro de trabajo

<!-- Una entrada por sesión, formato de docs/FLUJO_DE_TRABAJO.md, apartado 3 -->

### Registro 2026-10-24
- **Hecho:** ver T-03.
- **Pruebas automáticas:** `tests/run_tests.sh` correcto.
- **Decisiones tomadas:** ADR-004
