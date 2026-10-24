# T-12 · [F2] Funciones de flujo de trabajo y creatividad

- **Estado:** En pruebas
- **Fase:** 2 · **Prioridad:** 2
- **Etiquetas:** tipo: mejora, upstream: candidata
- **Rama:** `feat/T-12-produccion`
- **Issue de GitHub:** pendiente de migrar

## Contexto
El objetivo principal del fork es el flujo de trabajo y la creatividad en producción, no solo el directo (ADR-009). Revisión de funciones que faltan respecto al script de elton47 y a las peticiones de usuarios en el foro del original.

## Comportamiento esperado
- SHIFT + PLUG-IN abre o cierra la ventana del plug-in seleccionado; con dispositivos de Live, muestra la vista de dispositivos.
- DUPLICATE + SCENE + pad 4, 8, 12 o 16 duplica la escena.
- En BROWSER, encoder 2 cambia el tempo de 1 en 1 BPM y encoder 3 de 0,1 en 0,1, mostrando el valor al tocarlos.

## Criterios de aceptación
- [x] Pruebas automáticas de la ventana de dispositivo y del mapeo
- [ ] V1–V3 de `docs/pruebas/VERSION_CANDIDATA.md`

## Descartado, con motivo (ADR-009)
- Medidores de volumen en los pads: tráfico MIDI continuo con la espera de 0,5 ms por mensaje del original.
- Color de pads de Drum Rack por nombre: el original ya muestra el color de cada cadena, elegido en Live.
- Navegador integrado con el de Live: limitación reconocida por el autor, sin soporte conocido en la API.
- Más controles mapeables: el modo CHANNEL ya ofrece 16.

## Candidata a contribución al original
Sí: las tres funciones son generales.

## Registro de trabajo

### Registro 2026-10-24
- **Hecho:** `DeviceWindowComponent.py`, `CustomSessionComponent.py`, combinación SHIFT + PLUG-IN, mapeos, notificaciones y texto de pantalla del tempo en el navegador; ADR-009; R-415 a R-417, R-1019, R-1310.
- **Verificación:** `SessionComponent.set_modifier_button` y `SceneComponent` (duplicar con `duplicate_button`), modos con `behaviour` y `modes` (`control_surface_mapping`), `EnablingAddLayerMode` (no desactiva Transport al salir del navegador porque tiene otras capas), `StepEncoderControl` de tempo, `show_view`, `appointed_device` y `ComboElement` contrastados con los scripts de Live 12. `PluginDevice.is_editor_open` figura en la referencia del LOM para Live 12.4.5 pero no en los scripts de 12.0: si no existe, se muestra la vista de dispositivos.
- **Pruebas automáticas:** `tests/run_tests.sh` correcto, 40 pruebas.
- **Pendiente:** V1–V3 en la próxima prueba.
- **Decisiones tomadas:** ADR-009
