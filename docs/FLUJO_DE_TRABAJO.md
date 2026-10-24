# Flujo de trabajo

Proceso obligatorio para que todo cambio sea trazable: issue → rama → commits → registro de pruebas → PR → merge.

## 1. Ciclo de vida de un issue

| Estado en el tablero | Entra cuando | Sale cuando |
| --- | --- | --- |
| Backlog | Se crea el issue con plantilla | Cumple la definición de preparado |
| Preparado | Tiene criterios de aceptación comprobables | Alguien lo asigna y crea la rama |
| En curso | Existe rama y primer commit | Se abre PR a `develop` |
| En pruebas | PR abierto | Pruebas registradas y superadas |
| Hecho | PR fusionado en `develop` | — |
| Enviado upstream | PR abierto en el original | El original lo fusiona o lo rechaza |

### Definición de preparado

- Contexto: qué problema del directo resuelve.
- Comportamiento esperado concreto: qué control hace qué y qué muestra la pantalla (4 líneas × 28 caracteres).
- Criterios de aceptación comprobables a mano.
- Fase y prioridad asignadas.

### Definición de terminado

- Criterios de aceptación superados y registrados en el issue.
- Checklist de regresión ejecutada sin fallos.
- `python3 -m py_compile CustomMaschineMK3/*.py` sin errores.
- `CHANGELOG.md` actualizado si cambia el comportamiento.
- `docs/DECISIONES.md` actualizado si hubo decisión de diseño.
- PR revisado y fusionado; issue cerrado por el PR.

## 2. Ramas y commits

- Rama desde `develop` actualizado: `feat/<n>-<nombre>`, `fix/<n>-<nombre>`, `docs/<n>-<nombre>`.
- Commits pequeños, en imperativo, con `(#n)` al final.
- PR a `develop` con la plantilla; el texto incluye `Closes #n`.
- Fusión con «Squash and merge» para que cada issue sea un commit en `develop`.

## 3. Registro de trabajo en el issue

Un comentario por sesión de trabajo:

```markdown
### Registro AAAA-MM-DD
- **Hecho:** …
- **Pendiente:** …
- **Commit probado:** <hash corto>
- **Entorno:** SO …, Live 12.x.x, firmware/driver NI …
- **Pruebas:**
  - [x] Caso 1 — correcto
  - [ ] Caso 2 — fallo: <descripción> (extracto del log abajo)
- **Decisiones tomadas:** ninguna / ADR-NNN
```

## 4. Pruebas

No hay pruebas automáticas: las librerías de Live solo existen dentro de Live.

1. **Carga:** copiar `CustomMaschineMK3/` a `User Library/Remote Scripts/`, abrir Live, seleccionar la superficie de control. Revisar `Log.txt` de Live y, con `Config.LOGGING = True`, `CustomMaschineMK3.log`.
2. **Funcional:** criterios de aceptación del issue sobre el proyecto de pruebas del repositorio.
3. **Regresión:** checklist completa de funciones existentes (se crea en el issue de línea base y se guarda en `docs/pruebas/`).
4. **Estrés:** 30 minutos de uso continuo cambiando modos, dispositivos y escenas sin reiniciar Live.
5. **Ensayo:** solo para pasar a `live-stable`; una sesión real con la banda.

## 5. Versiones

- `develop` no se etiqueta.
- Cada merge a `live-stable` se etiqueta `live-AAAA.MM.DD` y se mueve la sección «Sin publicar» de `CHANGELOG.md` a esa versión.

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
3. Llevar solo el código general (sin `docs/`, `CLAUDE.md`, `CHANGELOG.md` ni configuración de la banda).
4. PR en inglés con descripción y pruebas.
5. El issue del fork pasa a «Enviado upstream» con enlace al PR.

## 8. Etiquetas

| Etiqueta | Uso |
| --- | --- |
| `tipo: mejora` / `tipo: fallo` / `tipo: documentación` / `tipo: prueba` | Naturaleza del issue |
| `prioridad: 1` / `prioridad: 2` / `prioridad: 3` | 1 = necesaria para el directo |
| `fase: 0` … `fase: 4` | Fase del plan |
| `upstream: candidata` | Mejora aportable al original |
| `bloqueado` | Depende de otro issue o de información externa |
