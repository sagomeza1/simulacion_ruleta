## Plan: Primer Hito Técnico del Simulador

El primer hito debe convertir el esqueleto actual en un núcleo de dominio verificable: apuestas válidas, ruletas europea/americana, pagos y aciertos, una simulación estática determinista y persistencia CSV contractual. La consola completa, el modo dinámico y el modo sencillo quedarán preparados para reutilizar ese núcleo, pero no bloquearán su validación.

**Base verificada**
- Se revisaron `docs/especificaciones.md`, `docs/objetivos.md`, `docs/proyecto.md` y `docs/reglas_de_la_ruleta.md`.
- La estructura modular ya existe en `simulacion_ruleta/src/simulacion_ruleta/`, pero las clases principales contienen `pass` o contratos incompatibles.
- Las pruebas actuales importan APIs inexistentes y contienen expectativas contradictorias con la documentación; deben actualizarse como parte del hito.
- No se modificó código ni se ejecutó `pytest` durante el diseño.

**Decisiones de contrato**
- `Ganancia` será la ganancia bruta neta indicada por la tabla: por ejemplo, `35 * monto` para `SU`; el importe apostado no se suma otra vez.
- El saldo se actualizará como `saldo_final = saldo_inicial - cantidad_apostada + ganancia`.
- `FF` representa siempre `0,1,2,3` y solo es válida en Europea; `BA` representa `0,00,1,2,3` y solo es válida en Americana. Ninguna acepta selección entre corchetes.
- La ruleta americana usará el valor textual `00`, nunca el entero `37`.
- Las reglas opcionales `La Partage` y `En Prison` quedan fuera del primer contrato funcional, aunque se conservará una estructura que permita incorporarlas después.
- Las especificaciones y la tabla oficial prevalecen sobre las pruebas antiguas; no se mantendrán dos APIs ambiguas solo para ocultar esa discrepancia.

**Fases de implementación**

### Fase 1: Contrato de apuestas y dominio de ruleta
1. Unificar `Apuesta` y `ApuestaMultiple` en `apuestas/modelos.py` con tipos explícitos para `monto`, `tipo` y `seleccion`, representación estable y validación separada de la sintaxis.
2. Rehacer `apuestas/parser.py` para exponer una función pública `parse_apuesta(cadena)` y, si se conserva la clase, hacer que delegue en ella. Debe aceptar una apuesta o una lista separada por comas, recortar espacios, conservar la selección como lista de strings y rechazar tokens vacíos o sintaxis que no cumpla exactamente la regex contractual.
3. Añadir validación semántica por código: códigos admitidos `SU`, `SP`, `ST`, `CO`, `FF`, `BA`, `LI`, `DZ`, `CL`, `LO`, `HI`, `EV`, `OD`, `RE`, `BL`; cantidad y forma de selecciones; rango `0..36`/`00`; adyacencia y estructura de splits, calles, esquinas, líneas, docenas y columnas; y compatibilidad con la variante.
4. Reorganizar `ruleta/modelos.py` para que `Ruleta` produzca 37 casillas europeas o 38 americanas, usando `Casilla` con número textual y color. Centralizar las listas de rojos, negros y verdes para impedir que `00` termine como negro.
5. Extender `ruleta/reglas.py` con la tabla de pagos por código, `obtener_color`, comprobación de acierto y cálculo de ganancia bruta. La API final debe recibir una apuesta ya validada y un resultado de tirada, no depender de I/O ni de valores aleatorios.
6. Ajustar `ruleta/resultados.py` para representar una tirada y/o el acumulado de resultados que necesitará el simulador, sin mezclar todavía la exportación con las reglas.

### Fase 2: Motor de ronda y simulación estática
1. Definir en `simulacion/gestor.py` la configuración del simulador: variante, saldo inicial, apuesta fija y cantidad de partidas, además de un generador de resultados inyectable para pruebas deterministas.
2. Implementar una operación de ronda que compruebe antes de tirar si el saldo cubre el monto total de la apuesta fija; si no, termine con causa `Bancarrota` sin generar una tirada adicional.
3. Resolver todas las apuestas contra un mismo resultado, sumar `CantidadApostada` y `Ganancia`, y actualizar el saldo con la fórmula contractual. Acumular historial de apuestas, tiradas y frecuencias.
4. Implementar primero `ModoSimulacionEstatica.jugar()` o delegarlo explícitamente en el gestor, con parada por `JuegosCompletados` o `Bancarrota`. Las clases de modo sencillo y dinámico solo recibirán el contrato base necesario para una fase posterior, salvo que su implementación no introduzca duplicación.
5. Mantener una fachada compatible (`Simulador`) únicamente si las pruebas o el punto de entrada la necesitan, pero con una sola implementación interna del ciclo de ronda.

### Fase 3: Persistencia contractual
1. Rediseñar `persistencia/exportador_csv.py` con rutas construidas mediante APIs de rutas, creación de directorios y métodos para exportar las tres tablas de una simulación.
2. Garantizar exactamente las columnas y orden de `apuestas.csv`, `numeros.csv` y `stats.csv`, separador coma y codificación UTF-8. `stats.csv` debe generar todas las casillas de la variante, incluidas frecuencias cero.
3. Generar carpetas bajo `simulaciones/YYYYMMDD_HHMM/` y resolver colisiones de nombres sin sobrescribir otra ejecución.
4. Implementar el append de `registros.csv` con las siete columnas contractuales, escribiendo cabecera solo cuando el archivo no exista o esté vacío y sin cargar todo el histórico.
5. Conectar el final de la simulación estática con el exportador, incluyendo `CausaFin`, totales y balance final.

### Fase 4: Pruebas y contrato para fases posteriores
1. Reemplazar las pruebas desalineadas por pruebas de dominio para parser, selecciones, variantes, `00`, colores, pagos y aciertos.
2. Añadir pruebas deterministas del saldo, suma de apuestas múltiples, bancarrota antes de la siguiente ronda, límite de partidas y causas de fin.
3. Añadir pruebas de exportación con directorio temporal: columnas, orden, encoding, separador, estadísticas con ceros, cabecera inicial y append posterior.
4. Dejar documentada la interfaz que consumirán `ModoSencillo`, `ModoSimulacionDinamica`, `consola/interfaz.py`, `consola/menus.py` y `main.py` en el hito siguiente.

**Archivos relevantes**
- `simulacion_ruleta/src/simulacion_ruleta/apuestas/modelos.py`: modelo único de apuesta y colección de apuestas.
- `simulacion_ruleta/src/simulacion_ruleta/apuestas/parser.py`: `parse_apuesta`, separación de múltiples apuestas y validaciones sintáctica/semántica.
- `simulacion_ruleta/src/simulacion_ruleta/ruleta/modelos.py`: casillas, números válidos y colores por variante.
- `simulacion_ruleta/src/simulacion_ruleta/ruleta/reglas.py`: pagos, coberturas, aciertos y ganancias.
- `simulacion_ruleta/src/simulacion_ruleta/ruleta/resultados.py`: resultado de tirada y acumulados de frecuencia.
- `simulacion_ruleta/src/simulacion_ruleta/simulacion/gestor.py`: configuración, ciclo de ronda, saldo, causas de fin y fachada `Simulador` si procede.
- `simulacion_ruleta/src/simulacion_ruleta/simulacion/modos.py`: integración de la simulación estática con el gestor; contratos base para los otros modos.
- `simulacion_ruleta/src/simulacion_ruleta/persistencia/exportador_csv.py`: generación de archivos internos y registro global.
- `simulacion_ruleta/tests/test_parser_apuestas.py`: contrato de parser y validación de selecciones.
- `simulacion_ruleta/tests/test_reglas_ruleta.py`: variantes, colores, coberturas, pagos y resolución.
- `simulacion_ruleta/tests/test_simulacion.py`: rondas, saldo, parada y resultados controlados.
- `simulacion_ruleta/tests/test_exportador_csv.py`: persistencia aislada en directorio temporal.

**Dependencias y paralelismo**
- Las fases 1 y el diseño de columnas de la fase 3 pueden planificarse en paralelo, pero la implementación del exportador depende de los nombres y tipos finales de los registros del gestor.
- La fase 2 depende de los modelos y reglas de la fase 1.
- La conexión completa de la fase 3 depende de la forma final de los acumulados de la fase 2.
- La fase 4 debe acompañar cada fase: no se pospone toda la validación hasta el final.

**Verificación**
1. Desde `simulacion_ruleta/`, ejecutar las pruebas enfocadas de parser, reglas, simulación y exportación; después ejecutar `pytest` completo.
2. Comprobar que Europea contiene exactamente `0..36` y Americana `0`, `00`, `1..36`, con `0`/`00` verdes y las listas oficiales de rojos y negros.
3. Probar los 15 códigos, sus pagos oficiales, selecciones válidas e inválidas, y exclusividad de `FF`/`BA`.
4. Ejecutar una simulación pequeña con resultados inyectados y verificar manualmente la fórmula de saldo, la ganancia bruta, el conteo de tiradas y la parada antes de apostar sin saldo suficiente.
5. Leer los cuatro CSV generados y verificar nombres, columnas, orden, separador, UTF-8, ceros en `stats.csv`, cabecera de `registros.csv` y append de una segunda ejecución.
6. Ejecutar diagnóstico estático/errores del editor y revisar que no se introduzcan dependencias fuera de Python estándar y `pandas`.

**Alcance excluido**
- Menús ASCII completos, lectura interactiva y edición de parámetros.
- Implementación final de modo sencillo y modo dinámico; solo se define el contrato reutilizable.
- `La Partage`, `En Prison`, bases de datos, GUI, web, visualizaciones, estrategias avanzadas y nuevas dependencias.
