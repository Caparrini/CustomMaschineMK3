# Seguimiento temporal (sustituye a GitHub Issues y Projects)

Carpeta provisional mientras los issues y el tablero de GitHub no estén activos en el fork. Se elimina al migrar.

## Uso

- Cada archivo de `issues/` equivale a un issue: `T-NN-<slug>.md`.
- El estado se cambia en la línea **Estado** del archivo y en `TABLERO.md`, en el mismo commit.
- Estados válidos: Backlog · Preparado · En curso · En pruebas · Hecho · Enviado upstream.
- Ramas: `feat/T-NN-<slug>`, `fix/T-NN-<slug>`, `docs/T-NN-<slug>`.
- Commits: referencia `(T-NN)` en lugar de `(#n)`.
- El registro de cada sesión de trabajo se añade al final del archivo del issue, en «Registro de trabajo».
- Los PR internos a `develop` se abren igualmente en GitHub (no dependen de que los issues estén activos) y citan `T-NN` en la descripción.

## Migración a GitHub

1. Activar Issues en el fork y crear el Project con auto-añadido (`is:issue`).
2. Crear los issues en orden T-01 … T-10 para que el número de GitHub coincida (`T-03` → `#3`), con etiquetas e hito de fase.
3. Copiar el registro de trabajo de cada archivo como primer comentario del issue.
4. Sustituir referencias `T-NN` por `#NN` en documentación y plantillas.
5. Eliminar esta carpeta y la sección provisional de `CLAUDE.md` en un único commit.
