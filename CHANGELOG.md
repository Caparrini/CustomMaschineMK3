# Registro de cambios del fork

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/). Solo recoge cambios del fork; los del original se consultan en su repositorio.

## [Sin publicar]

### Añadido
- Bancos de parámetros por plug-in VST/AU definidos en `plugin_banks.json`, elegidos por el nombre del dispositivo (T-03, T-09, ADR-004, ADR-005).
- Volcado automático de los parámetros de cada plug-in seleccionado en `plugin_parameters/` para preparar esos bancos (T-03).
- Pruebas automáticas sin Live (`tests/`).
- Documentación de proceso: `CLAUDE.md`, `docs/DECISIONES.md`, `docs/FLUJO_DE_TRABAJO.md`, plantillas de issue y de PR.
- Inventario de funciones `docs/FUNCIONES.md` de la versión 1.4 del original (T-01).
- Prueba mínima manual por versión `docs/pruebas/PRUEBA_MINIMA.md` y estrategia de pruebas (ADR-007, T-11).
