# Funciones del script

Inventario de las funciones de CustomMaschineMK3 versión 1.4 (commit `6b8cdb5` del original), elaborado a partir de `Mappings.py`, `ControlElements.py`, `DisplayDefinitions.py` y `SettingsComponent.py`, contrastado con la [documentación de operaciones del original](https://chiakibeats.github.io/CustomMaschineDocs/docs/all-operations).

Es documentación de referencia, no una lista de pruebas: no se ejecuta completa (ADR-007). Sirve para:

- Saber qué control hace qué sin abrir el código.
- Citar una función por su ID (`R-xxx`) en issues, PR y fallos.
- Elegir, en cada PR, los pocos casos afectados por el cambio que hay que probar a mano.

Columna **Fuente**: `M` = verificado en el código (`Mappings.py` y componentes); `D` = solo en la documentación del original.

## Convenciones

- `A + B`: mantener A y pulsar B.
- **Pads 1–16**: numeración de Maschine, 1 abajo a la izquierda y 16 arriba a la derecha.
- **Botones 1–8**: los 8 botones sobre las pantallas. **Encoders 1–8**: los 8 encoders bajo las pantallas.
- **Encoder**: el encoder principal 4D. «Inclinar» = empujarlo arriba, abajo, izquierda o derecha.
- **Grupos A–H**: los 8 botones de grupo.

## Instalación

| ID | Comprobación | Resultado esperado |
| --- | --- | --- |
| R-000 | MK3 en modo MIDI (SHIFT + botón MASCHINE) con la plantilla `Template/CustomMaschineMK3.ncm3` cargada | La pantalla deja de mostrar el software Maschine |
| R-001 | Seleccionar `CustomMaschineMK3` como superficie de control en Live | Sin errores en `Log.txt` de Live; los LED de la MK3 se encienden |
| R-002 | Abrir un proyecto de Live | La pantalla muestra el modo mezclador (sección 9) |

## 1. Transporte

| ID | Control | Resultado esperado | Fuente |
| --- | --- | --- | --- |
| R-101 | PLAY | Inicia la reproducción | M |
| R-102 | SHIFT + PLAY | Reproduce desde la posición actual / pausa | M |
| R-103 | STOP | Detiene la reproducción | M |
| R-104 | RESTART | Activa / desactiva el bucle del arreglo | M |
| R-105 | TAP | Tap tempo | M |
| R-106 | SHIFT + TAP | Activa / desactiva el metrónomo | M |
| R-107 | FOLLOW | Activa / desactiva la cuantización de grabación | M |
| R-108 | AUTO | Activa / desactiva la grabación de automatización | M |
| R-109 | SHIFT + AUTO | Reactiva la automatización | M |
| R-110 | SHIFT + pad 7 / SHIFT + pad 8 | Nudge de tempo abajo / arriba | M |
| R-111 | SHIFT + STOP | Detiene los clips de todas las pistas | M |

## 2. Grabación

| ID | Control | Resultado esperado | Fuente |
| --- | --- | --- | --- |
| R-201 | REC | Lanza la grabación según la vista | M |
| R-202 | SHIFT + REC | Capture MIDI | M |
| R-203 | SHIFT + ERASE | Activa / desactiva el overdub de clip | M |
| R-204 | PATTERN + grupos A–H | Selecciona la longitud de grabación fija | M |
| R-205 | PATTERN + REC | Lanza grabación de longitud fija | D |

## 3. Pistas y edición general

| ID | Control | Resultado esperado | Fuente |
| --- | --- | --- | --- |
| R-301 | FILE | Crea pista de audio (o de retorno, según contexto) | M |
| R-302 | SHIFT + FILE | Crea pista MIDI | M |
| R-303 | DUPLICATE + FILE | Duplica la pista seleccionada | M |
| R-304 | ERASE + FILE | Borra la pista seleccionada | M |
| R-305 | Girar el encoder (modo de encoder por defecto) | Selecciona pista anterior / siguiente | M |
| R-306 | Pulsar el encoder | Arma la pista seleccionada (exclusivo) | M |
| R-307 | SHIFT + pulsar el encoder | Arma la pista sin desarmar las demás | M |
| R-308 | LOCK | Bloquea / desbloquea la pista objetivo | M |
| R-309 | SHIFT + pad 1 / SHIFT + pad 2 | Deshacer / rehacer | M |
| R-310 | SHIFT + pad 5 / SHIFT + pad 6 | Cuantiza las notas del clip al 100 % / 50 % | M |
| R-311 | SHIFT + DUPLICATE | Duplica la longitud y el contenido del clip seleccionado | M |
| R-312 | ARRANGER | Alterna vista Session / Arrangement | M |
| R-313 | SHIFT + BROWSER | Muestra / oculta el panel del navegador de Live | M |
| R-314 | Pedal en entradas de pedal (si hay pedal) | Punta y anillo envían control | M |

## 4. Vista Session (PAD MODE)

| ID | Control | Resultado esperado | Fuente |
| --- | --- | --- | --- |
| R-401 | PAD MODE | Modo Session; pads con el color de los clips; recuadro 4×4 visible en Live | M |
| R-402 | Pads 1–16 | Lanza el clip slot | M |
| R-403 | SELECT + pad | Selecciona el clip slot sin lanzarlo | M |
| R-404 | ERASE + pad | Borra el clip | M |
| R-405 | DUPLICATE + pad, luego pad destino | Copia y pega el clip | M |
| R-406 | SCENE + pad 4, 8, 12 o 16 | Lanza la escena de esa fila | M |
| R-407 | MUTE + pad 1–4 | Detiene los clips de esa pista | M |
| R-408 | Inclinar el encoder | Mueve el recuadro de sesión una pista o escena | M |
| R-409 | SHIFT + inclinar el encoder | Mueve el recuadro una página (4 pistas o escenas) | M |
| R-410 | Grupos A–H | Mueve el recuadro dentro de la matriz 16×8 (vista general de sesión) | M |

## 5. Modos de teclado (KEYBOARD)

La selección del submodo es automática según el dispositivo de la pista.

| ID | Control | Resultado esperado | Fuente |
| --- | --- | --- | --- |
| R-501 | KEYBOARD en pista con instrumento | Modo teclado MIDI integrado con la escala de Live | D |
| R-502 | KEYBOARD en pista con Drum Rack | Modo Drum Rack; colores de pad iguales a los de las cadenas | D |
| R-503 | KEYBOARD en pista con Simpler en Slicing | Modo slices | D |

### 5.1 Teclado MIDI

| ID | Control | Resultado esperado | Fuente |
| --- | --- | --- | --- |
| R-511 | Pads 1–16 | Tocan notas; fijan la nota objetivo del secuenciador y de velocidad fija | M |
| R-512 | Grupos A–H | Seleccionan octava | M |
| R-513 | SHIFT + pad 13 / 14 | Baja / sube una nota | M |
| R-514 | SHIFT + pad 15 / 16 | Baja / sube una octava | M |
| R-515 | Notas raíz | Pads de nota raíz más brillantes, color del clip o de la pista | D |

### 5.2 Drum Rack

| ID | Control | Resultado esperado | Fuente |
| --- | --- | --- | --- |
| R-521 | Pads 1–16 | Disparan los pads del Drum Rack | M |
| R-522 | Grupos A–H | Seleccionan página de pads | M |
| R-523 | SHIFT + pad 13 / 14 / 15 / 16 | Fila abajo / arriba, página abajo / arriba | M |
| R-524 | MUTE + pad / SOLO + pad | Mute / solo del pad | M |
| R-525 | ERASE + MUTE / ERASE + SOLO | Quita todos los mutes / solos | M |
| R-526 | ERASE + pad | Borra el pad | M |
| R-527 | DUPLICATE + pad, luego pad destino | Copia y pega el pad | M |

### 5.3 Simpler en Slicing

| ID | Control | Resultado esperado | Fuente |
| --- | --- | --- | --- |
| R-531 | Pads 1–16 | Disparan slices | M |
| R-532 | Grupos A–D | Seleccionan página de slices | M |
| R-533 | SHIFT + pad 13 / 14 / 15 / 16 | Fila abajo / arriba, página abajo / arriba | M |
| R-534 | ERASE + pad | Borra el slice | M |

### 5.4 Común a los modos de teclado

| ID | Control | Resultado esperado | Fuente |
| --- | --- | --- | --- |
| R-541 | SELECT + pad | Cambia la nota objetivo sin dispararla | M |
| R-542 | EVENTS + pad | Selecciona en el clip las notas de esa nota, pad o slice | M |
| R-543 | EVENTS dos veces | Deselecciona todas las notas del clip | D |
| R-544 | ERASE + EVENTS | Borra las notas seleccionadas | M |
| R-545 | NOTE REPEAT (mantener) | Repetición de notas mientras se mantiene | M |
| R-546 | NOTE REPEAT + LOCK | Deja la repetición activa | M |
| R-547 | NOTES | Muestra / oculta el selector de velocidad de repetición en los grupos | M |
| R-548 | Grupos A–H con el selector visible | Seleccionan la velocidad de repetición (por defecto 1/4, 1/8, 1/16, 1/32, 1/4T, 1/8T, 1/16T, 1/32T) | M |
| R-549 | FIXED VEL | Acento: velocidad fija al máximo | M |

## 6. Velocidad fija (CHORDS)

| ID | Control | Resultado esperado | Fuente |
| --- | --- | --- | --- |
| R-601 | CHORDS | Modo de 16 niveles de velocidad para la nota objetivo | M |
| R-602 | Pads 1–16 | Disparan la nota objetivo con 16 velocidades distintas | M |
| R-603 | SELECT + pad | Selecciona el nivel de velocidad sin disparar | M |

## 7. Secuenciador por pasos (STEP)

| ID | Control | Resultado esperado | Fuente |
| --- | --- | --- | --- |
| R-701 | STEP | Modo secuenciador sobre el clip seleccionado | M |
| R-702 | Pads 1–16 | Añaden / borran pasos | M |
| R-703 | PATTERN + grupos A–E | Seleccionan la resolución del paso | M |
| R-704 | Grupos A–H | Seleccionan compás; dos grupos a la vez fijan la región de bucle | M |
| R-705 | SHIFT + pad 15 / 16 | Compás anterior / siguiente | M |
| R-706 | ERASE + grupo | Borra las notas de ese compás | M |
| R-707 | DUPLICATE + grupo, luego grupo destino | Copia y pega compás | M |
| R-708 | SELECT + pad | Selecciona las notas de ese paso | M |
| R-709 | Mantener paso + encoders 5–8 (modo editor de clip) | Posición, longitud, longitud fina y velocidad de la nota | D |
| R-710 | Ajuste `sequencer_style` en «Push» | Orden de pads estilo Push tras recargar | M |

## 8. Modos del encoder principal

| ID | Control | Resultado esperado | Fuente |
| --- | --- | --- | --- |
| R-801 | VOLUME + girar el encoder | Volumen máster | M |
| R-802 | VOLUME + pulsar el encoder | Volumen máster a 0,0 dB | M |
| R-803 | SWING + girar / SHIFT + girar | Groove en pasos de 5 % / 1 % | M |
| R-804 | SHIFT + SWING + girar / SHIFT + girar | Posición del arreglo / inicio del bucle | M |
| R-805 | SHIFT + SWING + pulsar el encoder | Añade / borra punto de referencia (cue) | M |
| R-806 | SHIFT + SWING + inclinar arriba / abajo | Cue anterior / siguiente | M |
| R-807 | SHIFT + SWING + inclinar izquierda / derecha | Rebobinar / avanzar | M |
| R-808 | TEMPO + girar / SHIFT + girar | Tempo en pasos de 1,0 / 0,1 | M |
| R-809 | SHIFT + TEMPO + girar | Cambia el tipo de escala | M |
| R-810 | SHIFT + TEMPO + pulsar el encoder | Activa / desactiva el modo escala | M |
| R-811 | SHIFT + TEMPO + inclinar | Cambia nota raíz u opciones de escala (dirección exacta por confirmar) | M |
| R-812 | Pulsar de nuevo el botón del modo activo | Vuelve al modo de encoder por defecto | M |

## 9. Mezclador (MIXER), modo de 8 pistas por defecto

| ID | Control | Resultado esperado | Fuente |
| --- | --- | --- | --- |
| R-901 | MIXER | Modo mezclador | M |
| R-902 | Encoders 1–8 | Parámetro seleccionado (volumen, pan o envío) de 8 pistas; MACRO mantenido = ajuste fino | M |
| R-903 | MACRO + botones 1–8 | Selecciona parámetro: volumen, pan, envíos A–F | M |
| R-904 | MACRO + ◀ / ▶ | Parámetro anterior / siguiente | M |
| R-905 | ◀ / ▶ | Página de pistas anterior / siguiente | M |
| R-906 | Botones 1–8 | Seleccionan pista | M |
| R-907 | SELECT + botón | Arma / desarma pista | M |
| R-908 | MUTE + botón / SOLO + botón | Mute / solo de pista | M |
| R-909 | ERASE + doble toque en encoder 1–8 | Restablece el valor por defecto | M |
| R-910 | PERFORM + grupos A–H | Cambia la asignación del crossfader | M |
| R-911 | Ajuste `mixer_mode` en «4Track» | Mezclador de 4 pistas: encoders 1–4 pan/envío, 5–8 volumen, botones 1–4 armado, 5–8 selección, PERFORM + A–D crossfader | M |

## 10. Control de dispositivos (PLUG-IN)

| ID | Control | Resultado esperado | Fuente |
| --- | --- | --- | --- |
| R-1001 | PLUG-IN | Modo dispositivo | M |
| R-1002 | Encoders 1–8 | Parámetros del banco actual; MACRO mantenido = ajuste fino | M |
| R-1003 | ◀ / ▶ | Banco de parámetros anterior / siguiente | M |
| R-1004 | MACRO + botones 1–8 | Salta al banco 1–8 | M |
| R-1005 | Botones 1–8 | Seleccionan dispositivo en la cadena de la pista | M |
| R-1006 | MUTE + botón | Activa / desactiva el dispositivo | M |
| R-1007 | ERASE + botón | Borra el dispositivo | M |
| R-1008 | PLUG-IN + ◀ / ▶ | Página de dispositivos anterior / siguiente | M |
| R-1009 | PLUG-IN + girar el encoder | Recorre la selección de dispositivos | M |
| R-1010 | Inclinar el encoder izquierda / derecha | Dispositivo anterior / siguiente | M |
| R-1011 | PLUG-IN + LOCK | Bloquea el dispositivo objetivo | M |
| R-1012 | VARIATION / DUPLICATE + VARIATION | Alterna ranura A/B / copia parámetros a la otra ranura | M |
| R-1013 | Bancos propios en Simpler, Wavetable, EQ Eight, Hybrid Reverb, Meld | Bancos personalizados del script en lugar de los de Live | M |
| R-1014 | Plug-in VST/AU | Parámetros en el orden que expone Live, en bancos de 8 | M |
| R-1015 | ERASE + doble toque en encoder 1–8 | Restablece el parámetro a su valor por defecto (solo continuos) | M |
| R-1016 | Cambiar de dispositivo o de banco | Notificación de 1,5 s con el nombre del dispositivo o del banco | M |

## 11. Tira táctil

| ID | Control | Resultado esperado | Fuente |
| --- | --- | --- | --- |
| R-1101 | PITCH + deslizar | Pitch bend; vuelve al centro al soltar | M |
| R-1102 | MOD + botones 1–8 | Asigna a la tira el parámetro del encoder correspondiente (en modo mezclador o dispositivo) | M |
| R-1103 | MOD + deslizar | Modifica el parámetro asignado | M |
| R-1104 | ERASE + MOD | Restablece el parámetro asignado | M |
| R-1105 | PERFORM + deslizar | Crossfader | M |

## 12. Editor de clip (SAMPLING)

| ID | Control | Resultado esperado | Fuente |
| --- | --- | --- | --- |
| R-1201 | SAMPLING | Modo editor de clip | M |
| R-1202 | Botones 1 / 2 / 3 | Mute de clip / bucle / recortar | M |
| R-1203 | Botones 5 / 6 / 7 | Modo de lanzamiento / cuantización de lanzamiento / legato | M |
| R-1204 | Botón 8 (clip de audio) | Activa / desactiva warp | M |
| R-1205 | Encoders 1–3, bucle activado | Inicio de bucle / longitud / inicio de reproducción | M |
| R-1206 | Encoders 1–2, bucle desactivado | Inicio / fin del clip | M |
| R-1207 | Encoders 5–7 (audio) | Ganancia / transposición / modo de warp | M |
| R-1208 | Encoders 5–8 (MIDI) | Posición / longitud en pasos / longitud fina / velocidad de las notas seleccionadas | M |
| R-1209 | MACRO mantenido | Ajuste fino | M |

## 13. Navegador (BROWSER)

| ID | Control | Resultado esperado | Fuente |
| --- | --- | --- | --- |
| R-1301 | BROWSER | Modo navegador; BROWSER de nuevo sale | M |
| R-1302 | Girar el encoder | Recorre elementos | M |
| R-1303 | Pulsar el encoder | Carga el elemento | M |
| R-1304 | Inclinar derecha / izquierda | Entra en la carpeta / sube a la carpeta superior | M |
| R-1305 | Inclinar abajo / arriba | Salto adelante / atrás en la lista | M |
| R-1306 | Botones 1–8 | Colecciones roja, naranja, amarilla, verde, azul, morada, gris y raíz del navegador | D |
| R-1307 | MACRO + botón 1 / encoder 1 | Activa la previsualización / volumen de previsualización | M |
| R-1308 | VARIATION | Hot-swap del dispositivo seleccionado | M |
| R-1309 | SELECT + VARIATION | Hot-swap del sample o pad (Simpler o Drum Rack seleccionado) | M |

## 14. Mapeo MIDI personalizado (CHANNEL)

| ID | Control | Resultado esperado | Fuente |
| --- | --- | --- | --- |
| R-1401 | CHANNEL | Modo de mapeo personalizado | M |
| R-1402 | MACRO | Modo aprendizaje para encoders | M |
| R-1403 | Encoders 1–8 y botones 1–8 | Controlan lo mapeado con MIDI Map de Live | M |
| R-1404 | ◀ / ▶ | Página anterior / siguiente | M |
| R-1405 | Volver al modo teclado tras usar este modo | Sin LED residuales en notas C-2 a G-2 (fallo conocido del original, T-08) | M |

## 15. Ajustes (SETTINGS)

| ID | Control | Resultado esperado | Fuente |
| --- | --- | --- | --- |
| R-1501 | SETTINGS | Modo ajustes; SETTINGS de nuevo sale | M |
| R-1502 | Girar el encoder | Recorre las opciones | M |
| R-1503 | Encoder 1 | Cambia el valor de la opción | M |
| R-1504 | Cerrar y reabrir Live | Los ajustes persisten (`settings.json` en la carpeta del script) | M |

Opciones y valores por defecto: selección automática de velocidad de repetición (desactivada), velocidades de repetición A–H (1/4, 1/8, 1/16, 1/32, 1/4T, 1/8T, 1/16T, 1/32T), estilo de secuenciador (Maschine, requiere recarga), modo de mezclador (8Track, requiere recarga), versión (1.4).

## 16. Pantalla

| ID | Modo | Contenido esperado (4 líneas × 28 caracteres) | Fuente |
| --- | --- | --- | --- |
| R-1601 | Mezclador | L1 parámetro seleccionado; L2 `Track:` o `Lock:` + pista; L3 y L4 valores de 4 encoders cada una | M |
| R-1602 | Dispositivo | L1 y L2 nombres de 4 parámetros cada una (6 caracteres); L3 y L4 sus valores. Sin dispositivo: «No device selected» | M |
| R-1603 | Dispositivo, tocar un encoder | Nombre completo y valor de ese parámetro | M |
| R-1604 | Mezclador, tocar un encoder | Pista y parámetro:valor | M |
| R-1605 | Editor de clip | Nombre, marcadores, modo de lanzamiento, cuantización; ganancia, tono y warp en audio. Sin clip: «No clip selected» | M |
| R-1606 | Navegador | `In:` carpeta y elemento seleccionado | M |
| R-1607 | Ajustes | Descripción y valor de la opción | M |
| R-1608 | Mapeo personalizado | Página y números de control | M |
