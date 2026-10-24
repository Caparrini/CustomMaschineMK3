# Prueba mínima

Única prueba manual obligatoria antes de dar por buena una versión. Objetivo: menos de 5 minutos. Se hace una vez por versión candidata, no por cada cambio: una sesión valida todos los PR acumulados.

Solo hay que anotar lo que falle. Si todo va bien, basta con escribir «Prueba mínima correcta» y el commit en el issue o PR.

## Preparación (una vez por versión)

1. Cerrar Live.
2. Copiar la carpeta `CustomMaschineMK3` del repositorio encima de la instalada en `User Library/Remote Scripts/`, fusionando. Si se sustituye la carpeta entera, se pierden los ajustes del modo SETTINGS (`settings.json`).
3. MK3 en modo MIDI (SHIFT + botón MASCHINE).
4. Abrir Live con un proyecto real que tenga al menos un Simpler o un instrumento, un plug-in VST/AU y varias escenas.

## Pasos

| Paso | Acción | Resultado esperado |
| --- | --- | --- |
| P1 | Preferencias → Link, Tempo & MIDI: superficie de control `CustomMaschineMK3`, entrada y salida de la MK3 | Los LED de la MK3 se encienden y la pantalla muestra el mezclador |
| P2 | PAD MODE y pulsar un pad con clip | El clip se lanza |
| P3 | Seleccionar una pista con instrumento, KEYBOARD y tocar pads | Suena el instrumento |
| P4 | PLUG-IN y girar un encoder | El parámetro cambia en Live y en la pantalla |
| P5 | ▶ en modo PLUG-IN | Cambia el banco y la pantalla muestra su nombre 1,5 s |
| P6 | SCENE + ▶ dos veces | Se lanzan las dos escenas siguientes a la seleccionada y la pantalla muestra «Scene N» y su nombre |
| P7 | Pasos de `docs/pruebas/VERSION_CANDIDATA.md`, si los hay | Los que indique |

## Si algo falla

- Anotar el paso (`P4 fallo: …`) en el issue o PR.
- Adjuntar `Log.txt` de Live (Windows: `%AppData%\Ableton\Live <versión>\Preferences\`; macOS: `~/Library/Preferences/Ableton/Live <versión>/`). No hace falta buscar el error dentro.
- Para volver a la versión anterior: copiar la carpeta de la etiqueta `live-…` anterior y reiniciar Live.
