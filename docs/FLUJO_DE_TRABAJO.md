# Flujo de trabajo

Proceso obligatorio para que todo cambio sea trazable: issue → rama → commits → registro de pruebas → PR → merge.

## 1. Ciclo de vida de un issue

| Estado en el tablero | Entra cuando | Sale cuando |
| --- | --- | --- |
| Backlog | Se crea el issue con plantilla | Cumple la definición de preparado |
| Preparado | Tiene criterios de aceptación comprobables | Alguien lo asigna y crea la rama |
| En curso | Existe rama y primer commit | El PR se fusiona en `develop` tras pruebas automáticas y revisión |
| En pruebas | PR fusionado; falta la prueba mínima de la versión candidata | Prueba mínima superada con los pasos específicos del PR |
| Hecho | Prueba mínima superada, o cambio solo de documentación fusionado | — |
| Descartado | Ya resuelto en el original, no viable o sustituido; el motivo queda en el issue | — |
| Enviado upstream | PR abierto en el original | El original lo fusiona o lo rechaza |

### Definición de preparado

- Contexto: qué problema del flujo de trabajo o del directo resuelve.
- Comportamiento esperado concreto: qué control hace qué y qué muestra la pantalla (4 líneas × 28 caracteres).
- Criterios de aceptación comprobables, automáticamente siempre que sea posible.
- Fase y prioridad asignadas.

### Definición de terminado

- Criterios de aceptación cubiertos: por pruebas automáticas (`tests/`) siempre que se pueda, y por pasos manuales solo cuando dependen de Live o del hardware.
- `tests/run_tests.sh` sin errores (incluye `py_compile` de todo el script).
- Pasos manuales del cambio (como mucho 3) escritos en el PR y añadidos a `docs/pruebas/VERSION_CANDIDATA.md`.
- `CHANGELOG.md` actualizado si cambia el comportamiento.
- `docs/DECISIONES.md` actualizado si hubo decisión de diseño.
- `docs/FUNCIONES.md` actualizado si cambia o se añade una función.
- PR fusionado en `develop`. El issue pasa a «En pruebas» si tiene pasos manuales, o a «Hecho» si no los tiene.

## 2. Ramas y commits

- Rama desde `develop` actualizado: `feat/<n>-<nombre>`, `fix/<n>-<nombre>`, `docs/<n>-<nombre>`.
- Commits pequeños, en imperativo, con `(#n)` al final.
- PR a `develop` con la plantilla; el texto incluye `Closes #n`.
- Revisión antes de fusionar: pruebas automáticas y relectura completa del diff contra los scripts de Live 12, en un paso separado de la escritura. No requiere tiempo de la persona que prueba.
- Fusión con «Squash and merge» para que cada issue sea un commit en `develop`.

## 3. Registro de trabajo en el issue

Un comentario por sesión de trabajo:

```markdown
### Registro AAAA-MM-DD
- **Hecho:** …
- **Pendiente:** …
- **Commit probado:** <hash corto>
- **Entorno:** SO …, Live 12.x.x (solo si hubo prueba manual)
- **Pruebas automáticas:** `tests/run_tests.sh` correcto / fallo
- **Prueba manual:** no aplica / P1–P6 correctos / `P4 fallo: …` (con `Log.txt` adjunto)
- **Decisiones tomadas:** ninguna / ADR-NNN
```

## 4. Pruebas

Principio (ADR-007): el tiempo de quien prueba con el hardware es el recurso más caro del proyecto. Todo lo verificable sin Live se verifica antes; la prueba manual se reduce al mínimo y se agrupa.

1. **Automáticas (Claude, en cada PR):** `tests/run_tests.sh <scripts de Live descompilados>`. Compila todo el script y ejecuta la lógica contra el código de bancos de Live. Ver `tests/README.md`.
2. **Revisión estática (Claude, en cada PR):** cada llamada nueva al framework se contrasta con los scripts descompilados de Live 12; el código que toca el framework falla de forma segura (registra el error y conserva el comportamiento original).
3. **Prueba mínima (manual, una vez por versión candidata):** `docs/pruebas/PRUEBA_MINIMA.md`, menos de 5 minutos, más los pasos específicos de los PR acumulados. Solo se anotan los fallos.
4. **Ensayo:** el uso normal en un ensayo de la banda valida la versión antes de pasar a `live-stable`. No requiere pasos adicionales.

Cambios solo de documentación: no necesitan prueba manual y se fusionan directamente.

`docs/FUNCIONES.md` es el inventario de funciones con IDs `R-xxx`; no se ejecuta completo.

## 5. Versiones

- `develop` no se etiqueta.
- Versión candidata: el commit de `develop` que se instala para la prueba mínima. Se anota en el registro de los issues «En pruebas».
- Cada merge a `live-stable` se etiqueta `live-AAAA.MM.DD`, se mueve la sección «Sin publicar» de `CHANGELOG.md` a esa versión y se vacía `docs/pruebas/VERSION_CANDIDATA.md`.

## 6. Sincronización con el original

```bash
git remote add upstream https://github.com/chiakibeats/CustomMaschineMK3.git   # una vez
git fetch upstream
git checkout main && git merge --ff-only upstream/main && git push origin main
git checkout develop && git merge main   # resolver conflictos en una rama sync/<fecha> si los hay
```

Frecuencia mínima: mensual, y siempre antes de preparar un PR al original.

## 7. Contribución al original

1. Proponer la mejora en un issue del original.
2. Rama desde `main` sincronizado: `upstream/<nombre>`.
3. Llevar solo el código general (sin `docs/`, `CLAUDE.md`, `CHANGELOG.md`, `tests/` ni `plugin_banks.json` de la banda).
4. PR en inglés con descripción y pruebas.
5. El issue del fork pasa a «Enviado upstream» con enlace al PR.

## 8. Etiquetas

| Etiqueta | Uso |
| --- | --- |
| `tipo: mejora` / `tipo: fallo` / `tipo: documentación` / `tipo: prueba` | Naturaleza del issue |
| `prioridad: 1` / `prioridad: 2` / `prioridad: 3` | 1 = imprescindible para el uso diario (producción o directo) |
| `fase: 0` … `fase: 4` | Fase del plan |
| `upstream: candidata` | Mejora aportable al original |
| `bloqueado` | Depende de otro issue o de información externa |
