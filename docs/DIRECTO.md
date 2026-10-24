# Uso en directo

Cómo preparar un proyecto de Live para tocarlo desde la MK3 con SCENE + ▶ o con el pedal (ADR-008).

## Estructura del proyecto

- **Escenas en el orden en que se tocan:** cada parte de cada canción es una escena, de arriba abajo. Una canción puede ser una sola escena o varias.
- **Click y fondos dentro de las escenas:** los clips de click y de sonidos de fondo van en la escena de la parte a la que pertenecen, para que entren con ella.
- **Cuantización de lanzamiento global de 1 compás** (o la que use la banda): las escenas entran a tiempo aunque se pulse un poco antes.
- **Follow Actions de escena (opcional):** si una parte debe pasar sola a la siguiente, se configura en la escena. La MK3 sigue contando desde la última escena lanzada, así que SCENE + ▶ después de una Follow Action lanza la correcta.

## Controles

| Acción | Control |
| --- | --- |
| Siguiente parte | SCENE + ▶, o el pedal si está configurado |
| Repetir o volver a la parte anterior | SCENE + ◀ |
| Parar todo | SHIFT + STOP |
| Saltar a otra canción | Ratón, o encoder para mover el recuadro y SCENE + pad 4, 8, 12 o 16 |

La pantalla muestra «Scene N» y el nombre de la escena durante 1,5 s en cada lanzamiento. Conviene nombrar las escenas con canción y parte, por ejemplo «Friends · Estribillo».

## Pedal para pasar de parte

1. Conectar un pedal de sustain a la entrada PEDAL de la MK3.
2. En la MK3: SETTINGS, girar el encoder hasta «Pedal Function (Reload required)» y cambiar el valor con el encoder 1 a «Next Scene».
3. Recargar el script: volver a seleccionar `CustomMaschineMK3` en las preferencias de Live, o reiniciar Live.

Con «Next Scene», el pedal deja de funcionar como sustain. Si el pedal es de polaridad inversa, la escena se lanza al soltarlo en lugar de al pisarlo; sigue siendo una escena por pisada.
