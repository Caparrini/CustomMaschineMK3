# Versión candidata

Pasos específicos acumulados desde la última versión estable. Se hacen en la misma sesión que la prueba mínima (paso P7) y se vacían al crear la siguiente etiqueta `live-…`.

Commit de `develop` a instalar: el último en el momento de la prueba.

| Paso | Origen | Acción | Resultado esperado |
| --- | --- | --- | --- |
| V1 | T-12 | Seleccionar un plug-in VST/AU y pulsar SHIFT + PLUG-IN dos veces | Su ventana se abre y se cierra; la pantalla dice «window open» / «window closed». Si dice «shown in device view», la versión de Live no permite controlar la ventana: anotarlo, no es un fallo |
| V2 | T-12 | En PAD MODE, DUPLICATE + SCENE + pad 16 | La primera escena del recuadro (fila superior de pads) se duplica justo debajo |
| V3 | T-12 | BROWSER y girar el encoder 2 | Cambia el tempo de 1 en 1 BPM y la pantalla lo muestra |

Opcional, solo si se va a usar: pedal con «Pedal Function» = «Next Scene» (`docs/DIRECTO.md`).
