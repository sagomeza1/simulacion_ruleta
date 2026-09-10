# Contrato de interfaces para la fase 4

Este documento deja fijado el contrato mínimo que consumirán los modos de juego, la consola y la persistencia antes de continuar con la siguiente fase del desarrollo.

## 1. Simulador base

La clase `Simulador` es la fachada del núcleo de dominio. Debe ofrecer estas operaciones:

- `configurar_simulacion(variante, saldo_inicial, apuesta_fija, cantidad_partidas, generador_resultados=None)`
  - Normaliza la variante (`Europea` o `Americana`).
  - Valida la apuesta fija mediante `parse_apuesta` y `ReglasRuleta.validar_apuesta`.
  - Reinicia el estado financiero y estadístico de la simulación.

- `ejecutar_ronda()`
  - Comprueba si hay saldo suficiente para cubrir la apuesta total.
  - Si no hay saldo, devuelve `causa_fin = "Bancarrota"` sin generar una tirada adicional.
  - Genera una tirada, resuelve las apuestas, actualiza `balance`, `total_apostado` y `total_ganado`, y registra la frecuencia del número obtenido.

- `ejecutar_simulacion(exportador=None, modo="Estatica", nombre_simulacion=None)`
  - Ejecuta rondas hasta completar `cantidad_partidas` o hasta que el saldo imposibilite la siguiente apuesta.
  - Finaliza con `causa_fin` en `"JuegosCompletados"` o `"Bancarrota"`.
  - Devuelve un resumen con: `partidas`, `causa_fin`, `total_apostado`, `total_ganado` y `balance_final`.
  - Si se proporciona un `ExportadorCSV`, genera los CSV de la simulación y anexa su registro global.

## 2. Modos reutilizables

Los modos solo encapsulan la selección del flujo y reutilizan el mismo `Simulador`:

- `ModoSencillo.gestor` -> instancia del `Simulador`.
- `ModoSimulacionEstatica.gestor` -> instancia del mismo `Simulador` ya configurado.
- `ModoSimulacionDinamica.gestor` -> se reutiliza la misma infraestructura del gestor y no debe duplicar reglas ni serialización.

Todos los modos deben exponer `jugar()` y devolver un diccionario de resumen con al menos:

- `partidas`
- `causa_fin`
- `total_apostado`
- `total_ganado`
- `balance_final`

## 3. Interfaz de consola

La consola no debe mezclar I/O con lógica de ruleta ni de pago. Debe delegar en el gestor y en el parser:

- `InterfazConsola` debe exponer los componentes de entrada/salida para presentar menús y mensajes.
- `Menu` debe encapsular la navegación entre modos.
- `main.py` debe construir la interfaz y llamar a `seleccionar_modo(...)` para iniciar la ejecución sin tocar la lógica financiera.

## 4. Persistencia

`ExportadorCSV` debe aceptar:

- `directorio_base` para la carpeta de simulaciones.
- `ruta_registros` para el archivo acumulativo.

Debe exportar exactamente estas tablas:

- `apuestas.csv`: columnas `NoApuesta`, `Apuesta`, `MontoInicial`, `CantidadApostada`, `Ganancia`, `MontoFinal`.
- `numeros.csv`: columnas `NoPartida`, `Numero`, `Color`.
- `stats.csv`: columnas `Numero`, `Color`, `Cantidad`, incluyendo todas las casillas de la variante con frecuencia cero.
- `registros.csv`: columnas `Simulacion`, `Modo`, `Ruleta`, `TotalApostado`, `TotalGanado`, `BalanceFinal`, `CausaFin`.

La API pública final de persistencia se usa así:

```python
exportador = ExportadorCSV("simulaciones", "registros.csv")
resumen = simulador.ejecutar_simulacion(
    exportador=exportador,
    modo="Estatica",
    nombre_simulacion="20240101_0101",
)
```

## 5. Contrato de validación

Las apuestas deben validarse en dos etapas:

1. Sintaxis: regex `^\d+[A-Z]{2}(\[[\w,-]+\])?$` aplicada a cada token individual.
2. Semántica: verificación de códigos oficiales, rangos, exclusividad de variantes y geometría de selecciones.

En particular:

- `FF` solo está permitida en Europea.
- `BA` solo está permitida en Americana.
- `00` solo se admite en la ruleta americana y solo como valor válido de la casilla/selección apropiada.
- La selección parcial de `DZ` y `CL` usa valores `1st`, `2nd` o `3rd` según la documentación oficial.

Estas reglas son la base que seguirá la siguiente fase de desarrollo de consola y modos dinámicos.
