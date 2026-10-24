# Seguimiento temporal (sustituye a GitHub Issues y Projects)

Carpeta provisional mientras los issues y el tablero de GitHub no estén activos en el fork. Se elimina al migrar.

## Uso

- Cada archivo de `issues/` equivale a un issue: `T-NN-<slug>.md`.
- El estado se cambia en la línea **Estado** del archivo y en `TABLERO.md`, en el mismo commit.
- Estados válidos: Backlog · Preparado · En curso · En pruebas · Hecho · Descartado · Enviado upstream (definiciones en `docs/FLUJO_DE_TRABAJO.md`, apartado 1).
- Ramas: `feat/T-NN-<slug>`, `fix/T-NN-<slug>`, `docs/T-NN-<slug>`.
- Commits: referencia `(T-NN)` en lugar de `(#n)`.
- El registro de cada sesión de trabajo se añade al final del archivo del issue, en «Registro de trabajo».
- Los PR internos a `develop` se abren igualmente en GitHub (no dependen de que los issues estén activos) y citan `T-NN` en la descripción.

## Migración a GitHub

1. Activar Issues en el fork y crear el Project con auto-añadido (`is:issue`).
2. Crear los issues en orden T-01 … T-NN; los «Hecho» y «Descartado» se crean y se cierran, con etiquetas e hito de fase. Los números de GitHub no coincidirán con `T-NN`, porque issues y PR comparten numeración y ya existen PR; anotar la correspondencia en una tabla en este README antes de borrarlo.
3. Copiar el registro de trabajo de cada archivo como primer comentario del issue.
4. Sustituir cada referencia `T-NN` por su `#n` según esa tabla en documentación y plantillas.
5. Eliminar esta carpeta y la sección provisional de `CLAUDE.md` en un único commit.
