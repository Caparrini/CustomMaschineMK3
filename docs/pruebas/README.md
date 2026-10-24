# Pruebas

| Qué | Dónde | Quién | Cuándo |
| --- | --- | --- | --- |
| Pruebas automáticas sin Live | `tests/` (`tests/run_tests.sh`) | Claude | En cada PR |
| Prueba mínima con Live y la MK3 | `PRUEBA_MINIMA.md` | Persona con el hardware | Una vez por versión candidata, menos de 5 minutos |
| Pasos específicos de los cambios pendientes de probar | `VERSION_CANDIDATA.md` | Persona con el hardware | En la misma sesión que la prueba mínima |
| Inventario de funciones | `docs/FUNCIONES.md` | Consulta | No se ejecuta completo |

No hay proyecto de Live de pruebas: la prueba mínima usa un proyecto real (ADR-007).

Los resultados no se guardan aquí: se registran en el issue o PR correspondiente (formato en `docs/FLUJO_DE_TRABAJO.md`, apartado 3).
