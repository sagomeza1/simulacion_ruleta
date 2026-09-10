# Prompt de verificación de la Fase 1 y desarrollo de la Fase 2

Trabaja en el repositorio del simulador de ruleta ubicado en:

`/home/alejandro/Proyectos/simulacion_ruleta`

Tu objetivo es verificar rigurosamente la finalización de la Fase 1 y, únicamente si está completa, comenzar el desarrollo de la Fase 2.

## Reglas de trabajo

- Responde y comunica los avances en español.
- Antes de editar, revisa el estado real del repositorio y no asumas que los cambios anteriores están completos.
- No reviertas cambios existentes que no hayas realizado.
- Mantén los cambios limitados al alcance de la fase correspondiente.
- No avances a fases posteriores si la Fase 1 tiene incumplimientos.
- Ejecuta pruebas focalizadas después de cada cambio significativo.
- No hagas commits ni crees ramas.
- Usa Python 3.10 o superior.
- Ejecuta los comandos desde:

  ```bash
  cd /home/alejandro/Proyectos/simulacion_ruleta/simulacion_ruleta
  ```

## Paso 1: revisar el contrato del proyecto

Lee y contrasta estos documentos:

- `/home/alejandro/Proyectos/simulacion_ruleta/docs/especificaciones.md`
- `/home/alejandro/Proyectos/simulacion_ruleta/docs/objetivos.md`
- `/home/alejandro/Proyectos/simulacion_ruleta/docs/proyecto.md`
- `/home/alejandro/Proyectos/simulacion_ruleta/docs/reglas_de_la_ruleta.md`
- `/home/alejandro/Proyectos/simulacion_ruleta/.github/copilot-instructions.md`

También revisa cualquier documentación específica dentro de:

- `/home/alejandro/Proyectos/simulacion_ruleta/simulacion_ruleta/docs/`

Determina a partir de la documentación cuál es exactamente el alcance de la Fase 2. No inventes requisitos ni adelantes trabajo de fases posteriores.

## Paso 2: verificar la Fase 1

Revisa estos archivos:

- `src/simulacion_ruleta/apuestas/modelos.py`
- `src/simulacion_ruleta/apuestas/parser.py`
- `src/simulacion_ruleta/ruleta/modelos.py`
- `src/simulacion_ruleta/ruleta/reglas.py`
- `src/simulacion_ruleta/ruleta/resultados.py`
- `tests/test_parser_apuestas.py`
- `tests/test_reglas_ruleta.py`

Ejecuta primero:

```bash
pytest tests/test_parser_apuestas.py tests/test_reglas_ruleta.py
```

Si `pytest` no está disponible en el terminal, utiliza el intérprete Python configurado por el workspace o instala la dependencia mediante las herramientas de entorno disponibles. No declares la fase completa basándote únicamente en una revisión visual.

Verifica explícitamente que la Fase 1 cumple todos estos puntos:

### Modelo de apuestas

- Existe un único modelo coherente de `Apuesta`.
- Tiene `monto`, `tipo` y `seleccion`.
- Usa anotaciones de tipos explícitas compatibles con Python 3.10+.
- `seleccion` es una lista de strings o `None`.
- El modelo no realiza I/O.
- No existen modelos duplicados o incompatibles de `Apuesta`.

### Parser

- Existe la función pública `parse_apuesta(cadena)`.
- Acepta una apuesta individual.
- Acepta varias apuestas separadas por comas.
- Recorta espacios alrededor de cada token.
- Rechaza tokens vacíos.
- Valida estrictamente:

  `^\d+[A-Z]{2}(\[[\w,-]+\])?$`

- Extrae correctamente monto, tipo y selección.
- Conserva las selecciones como listas de strings.
- Usa excepciones específicas y mensajes claros.
- `ApuestaParser`, si existe, delega en la implementación principal y no duplica lógica.

### Códigos oficiales

Verifica que se soportan exactamente estos códigos:

- `SU`: pago 35:1
- `SP`: pago 17:1
- `ST`: pago 11:1
- `CO`: pago 8:1
- `FF`: cobertura fija `0, 1, 2, 3`, pago 8:1, solo Europea
- `BA`: cobertura fija `0, 00, 1, 2, 3`, pago 6:1, solo Americana
- `LI`: pago 5:1
- `DZ`: `1st`, `2nd` o `3rd`, pago 2:1
- `CL`: `1st`, `2nd` o `3rd`, pago 2:1
- `LO`: pago 1:1
- `HI`: pago 1:1
- `EV`: pago 1:1
- `OD`: pago 1:1
- `RE`: pago 1:1
- `BL`: pago 1:1

No deben existir códigos inventados ni alias ambiguos.

### Validación semántica

Comprueba que se rechaza:

- monto cero;
- monto negativo;
- código desconocido;
- selección obligatoria ausente;
- selección sobrante;
- selección fuera de rango;
- números repetidos;
- selecciones mal formadas;
- `00` en ruleta Europea;
- `FF` en ruleta Americana;
- `BA` en ruleta Europea;
- estructuras inválidas de `SP`, `ST`, `CO` y `LI`;
- valores distintos de `1st`, `2nd` y `3rd` para `DZ` y `CL`;
- selecciones en `LO`, `HI`, `EV`, `OD`, `RE` y `BL`.

### Modelos de ruleta

- Ruleta Europea: exactamente `0, 1, ..., 36`.
- Ruleta Americana: exactamente `0, 00, 1, ..., 36`.
- `00` está representado como string.
- `0` y `00` son verdes.
- Los números rojos son exactamente:

  `1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36`

- Los números negros son exactamente:

  `2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35`

- No se asigna automáticamente negro a valores desconocidos.
- Las variantes se normalizan de forma coherente.
- Las variantes desconocidas se rechazan.

### Reglas y resultados

- La tabla de pagos está centralizada.
- Se puede obtener el pago por código.
- Se puede obtener el color de una casilla.
- Se puede determinar si una apuesta acierta.
- Se puede calcular la ganancia bruta.
- La ganancia es exactamente:

  `monto * pago`

- No se suma nuevamente el importe apostado.
- La lógica no usa `input()`, `print()` ni aleatoriedad.
- Funciona en ruleta Europea y Americana.
- Rechaza combinaciones incompatibles con la variante.
- Los modelos de resultados representan una tirada y su casilla/color.
- No se mezcla todavía la lógica con exportación CSV ni con el gestor de simulación.

## Paso 3: decidir qué hacer

Después de revisar código, pruebas y documentación, toma una de estas decisiones.

### Caso A: Fase 1 incompleta

Si falta cualquier requisito de la Fase 1:

1. Enumera brevemente los incumplimientos concretos.
2. Corrige únicamente lo necesario para completar la Fase 1.
3. Actualiza únicamente las pruebas relacionadas con parser, apuestas y reglas de ruleta.
4. Ejecuta:

   ```bash
   pytest tests/test_parser_apuestas.py tests/test_reglas_ruleta.py
   ```

5. Repite la corrección y las pruebas hasta que la Fase 1 quede completa.
6. No empieces la Fase 2 en esta sesión.

### Caso B: Fase 1 completa

Solo si todos los requisitos anteriores están satisfechos y las pruebas focalizadas pasan:

1. Informa que la Fase 1 está completa.
2. Explica brevemente qué evidencias lo confirman.
3. Identifica en la documentación el alcance exacto de la Fase 2.
4. Revisa las pruebas existentes relacionadas con la Fase 2.
5. Implementa la Fase 2 siguiendo la arquitectura del repositorio.
6. No modifiques todavía funcionalidades que pertenezcan a fases posteriores.
7. Añade o actualiza pruebas enfocadas para la Fase 2.
8. Ejecuta primero las pruebas de la Fase 2 y luego, si es posible, toda la suite:

   ```bash
   pytest tests/test_parser_apuestas.py tests/test_reglas_ruleta.py
   pytest
   ```

9. Si aparecen fallos no relacionados con tus cambios, no los ocultes ni los corrijas sin justificarlo. Indícalos claramente al final.

## Restricciones importantes

No avances a estos módulos salvo que la documentación confirme que forman parte de la Fase 2:

- `simulacion/gestor.py`
- `simulacion/modos.py`
- `persistencia/exportador_csv.py`
- `consola/interfaz.py`
- `consola/menus.py`
- `main.py`

No implementes persistencia, exportación CSV, interacción por consola, aleatoriedad ni coordinación de simulaciones si corresponden a una fase posterior.

## Informe final obligatorio

Al terminar, informa:

- Si la Fase 1 estaba completa al comenzar.
- Qué se corrigió, si fue necesario.
- Qué parte de la Fase 2 se implementó, si correspondía.
- Archivos modificados.
- Pruebas ejecutadas y resultado.
- Cualquier limitación, fallo preexistente o trabajo pendiente.
