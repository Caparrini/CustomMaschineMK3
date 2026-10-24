# T-04 · [F1] Mapeo de botones para el directo

- **Estado:** Backlog
- **Fase:** 1 · **Prioridad:** 1
- **Etiquetas:** tipo: mejora, bloqueado
- **Rama:** —
- **Issue de GitHub:** pendiente de migrar

## Propuesta para decidir (solo lectura, sin prueba)
Lo que ya existe para el directo (ver `docs/FUNCIONES.md`):
- SCENE + pad 4, 8, 12 o 16: lanza una de las 4 escenas visibles en el recuadro de sesión (R-406).
- Encoder: mueve el recuadro de sesión; SHIFT + inclinar, de 4 en 4 (R-408, R-409).
- MUTE + pad 1–4: detiene los clips de una pista; SHIFT + STOP: detiene todo (R-407, R-111).

Opciones de mejora, de menor a mayor cambio:
1. **Escena siguiente y anterior:** dos botones (p. ej. SCENE + ▶ / ◀) que lanzan la escena siguiente o la anterior a la que suena y mueven el recuadro con ella. Una canción se toca solo con «siguiente».
2. **16 escenas con SCENE:** SCENE + pad 1–16 lanza 16 escenas seguidas desde el recuadro, en lugar de 4.
3. **Modo directo dedicado:** grupos A–H = canciones (primera escena de cada una), pads = partes de la canción actual.

Para elegir hace falta saber: cuántas escenas tiene una canción típica, si cada canción empieza en una escena fija y si el click y los fondos van en clips de esas mismas escenas.

## Contexto
En el directo hay que lanzar escenas, bloques de canción y sonidos de fondo sin tocar el ratón.

## Comportamiento esperado
Por definir en este issue antes de programar: tabla de botones y pads con su función en un modo «directo», basada en la estructura real de los proyectos de la banda (escenas por canción, pistas de click y fondos).

## Criterios de aceptación
- [ ] Tabla de asignaciones acordada por la banda y añadida a este issue
- [ ] Una canción completa se toca desde la MK3 sin usar el ratón
- [ ] LED coherentes con el estado de escenas y pistas

## Archivos previsiblemente afectados
`Mappings.py`, posiblemente componente nuevo

## Candidata a contribución al original
Parcial

## Registro de trabajo

<!-- Una entrada por sesión, formato de docs/FLUJO_DE_TRABAJO.md, apartado 3 -->
