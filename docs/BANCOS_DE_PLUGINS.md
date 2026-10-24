# Bancos de parámetros para plug-ins

Permite que los 8 encoders del modo PLUG-IN controlen, en el orden elegido y por páginas con nombre, los parámetros de un plug-in VST o AU. Sin configurar nada, un plug-in se controla como en Live: sus parámetros en orden, de 8 en 8.

## Cómo se prepara un plug-in

1. **Que Live exponga los parámetros.** Live solo los expone automáticamente si el plug-in tiene pocos (el límite por defecto es 64); si tiene más, hay que añadir los que interesen con el botón Configure del dispositivo en Live. Para no repetirlo en cada proyecto: clic derecho en la barra de título del plug-in → «Save as Default Configuration» ([Ableton](https://help.ableton.com/hc/en-us/articles/209073089)).
2. **Obtener sus nombres.** Con la MK3 en modo PLUG-IN, seleccionar el plug-in. El script escribe `plugin_parameters/<nombre del dispositivo>.txt` dentro de su carpeta en `User Library/Remote Scripts/CustomMaschineMK3/`, con un nombre de parámetro por línea. Si el archivo dice que no hay parámetros, falta el paso 1.
3. **Definir los bancos** en `CustomMaschineMK3/plugin_banks.json` del repositorio (o pasar los `.txt` a Claude para que lo haga):

```json
{
    "Serum": {
        "Osciladores": ["A Vol", "A Pan", "A Octave", "", "B Vol", "B Pan", "B Octave", ""],
        "Filtro": ["Fil Cutoff", "Fil Reso"]
    }
}
```

- La clave (`"Serum"`) se compara con el principio del nombre del dispositivo en Live, sin distinguir mayúsculas. Si dos claves coinciden, gana la más larga.
- Cada banco tiene hasta 8 nombres, copiados tal cual del `.txt`. `""` o un nombre que Live no expone dejan ese encoder vacío.
- El orden de los bancos en el archivo es el orden en la MK3: ◀ / ▶ los recorren y MACRO + botón 1–8 salta a cada uno.

4. **Instalar y recargar:** copiar la carpeta del script como en `docs/pruebas/PRUEBA_MINIMA.md` y volver a seleccionar la superficie de control en las preferencias de Live (o reiniciar Live). El archivo solo se lee al cargar el script.

Un JSON con errores no rompe nada: se ignora y queda un aviso en el log.

Detalles de diseño: ADR-004 y ADR-005 en `docs/DECISIONES.md`.
