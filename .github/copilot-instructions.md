# Instrucciones para agentes

## Contexto del repositorio

- El proyecto Python está dentro de `simulacion_ruleta/`. Ejecuta desde ese directorio los comandos de instalación, pruebas y la aplicación.
- La fuente está en `simulacion_ruleta/src/simulacion_ruleta/` y las pruebas en `simulacion_ruleta/tests/`.
- Consulta [`docs/objetivos.md`](../docs/objetivos.md), [`docs/especificaciones.md`](../docs/especificaciones.md), [`docs/proyecto.md`](../docs/proyecto.md) y [`docs/reglas_de_la_ruleta.md`](../docs/reglas_de_la_ruleta.md) antes de cambiar reglas, arquitectura o formatos de salida.
- Usa Python 3.10 o superior. La dependencia externa obligatoria es `pandas`; respeta también las dependencias declaradas en [`simulacion_ruleta/pyproject.toml`](../simulacion_ruleta/pyproject.toml) y [`simulacion_ruleta/requirements.txt`](../simulacion_ruleta/requirements.txt).

## Comandos de referencia

Desde `simulacion_ruleta/`:

```bash
pip install -r requirements.txt
pytest
python src/simulacion_ruleta/main.py
```

Mantén las pruebas enfocadas en la modificación. Añade o actualiza pruebas para reglas de pagos, validación de apuestas, condiciones de bancarrota y exportación cuando cambie alguno de esos contratos.

## Arquitectura obligatoria

- Mantén una POO modular con responsabilidades únicas y tipado explícito mediante `typing`.
- `apuestas/` valida y transforma entradas; `ruleta/` contiene casillas, colores, pagos y compatibilidad de apuestas; `simulacion/` coordina partidas, modos y saldo; `consola/` gestiona únicamente interacción I/O; `persistencia/` serializa resultados.
- No mezcles `input()`/`print()` con reglas financieras, aleatoriedad, parsing o acceso a CSV.
- Conserva las interfaces públicas existentes salvo que el cambio sea necesario y actualiza sus pruebas y documentación.
- Usa la biblioteca estándar indicada por la especificación (`os`, `sys`, `random`, `datetime`, `re`, `typing`) y `pandas` para DataFrames y CSV. No introduzcas bases de datos, frameworks web, GUI, Matplotlib ni nuevas dependencias sin justificarlo.
- Sigue PEP 8, nombres descriptivos, imports limpios, docstrings útiles y anotaciones de tipos completas. Usa excepciones específicas y mensajes claros para entradas inválidas y errores de persistencia.

## Reglas de negocio que no deben cambiarse accidentalmente

- Ruleta europea: 37 casillas (`0` a `36`) y apuesta exclusiva `FF`.
- Ruleta americana: 38 casillas (`0`, `00` y `1` a `36`) y apuesta exclusiva `BA`.
- `0` y `00` son verdes. Los números rojos son `1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36`; los restantes números válidos son negros.
- La sintaxis de cada apuesta debe validar `^\d+[A-Z]{2}(\[[\w,-]+\])?$`. Las apuestas múltiples se reciben en una línea separada por comas, se recortan y se validan individualmente.
- Respeta las abreviaturas, coberturas y pagos oficiales definidos en [`docs/proyecto.md`](../docs/proyecto.md). No inventes tipos ni aceptes selecciones incompatibles con la apuesta o la variante.
- El saldo se calcula como `MontoFinal = MontoInicial - CantidadApostada + Ganancia`. La ganancia es bruta según la tabla oficial; no confundas pago con retorno total.
- El modo sencillo permite detenerse manualmente. Los modos estático y dinámico terminan al completar `N` partidas o cuando el saldo es cero o insuficiente para cubrir la próxima apuesta.

## Datos, volumen y persistencia

- Genera cada simulación en `simulaciones/YYYYMMDD_HHMM/` con `apuestas.csv`, `numeros.csv` y `stats.csv`.
- Escribe todos los CSV con separador `,`, codificación `utf-8` y columnas contractuales. `stats.csv` debe incluir todas las casillas de la variante, incluso con frecuencia cero.
- `registros.csv` es acumulativo: anexa una fila con las columnas `Simulacion`, `Modo`, `Ruleta`, `TotalApostado`, `TotalGanado`, `BalanceFinal` y `CausaFin` sin sobrescribir ejecuciones anteriores.
- Para simulaciones grandes, evita concatenaciones repetidas de DataFrames y escrituras por ronda; acumula registros estructurados y exporta de forma controlada al finalizar o en lotes claramente justificados. No cargues todo el histórico de `registros.csv` para añadir una fila.
- Usa rutas construidas con APIs de rutas y crea directorios antes de escribir. Evita colisiones de nombres de simulación y no mezcles archivos de pruebas con `simulaciones/` de producción.
- No alteres nombres, tipos, orden de columnas, separadores o codificación sin actualizar la especificación y las pruebas afectadas.

## Criterio de cambios

Antes de editar, identifica el módulo que posee la decisión y verifica el contrato en la documentación y en una prueba cercana. Prefiere el cambio mínimo; no corrijas problemas no relacionados. Después ejecuta las pruebas enfocadas y, si es posible, `pytest` completo desde `simulacion_ruleta/`.