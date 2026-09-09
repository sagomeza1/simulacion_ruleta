# ¿Cuál es el propósito del proyecto?

Realizar una simulación de una ruleta para generar una estrategia que permita generar ganancias.

# ¿Qué debe requerir el proyecto?

Una simulación de la ruleta que permita experimentar con las diferentes formas de apuestas.

# ¿Qué debe contener la interfaz?

Se esta pensando una interfaz CLI, con un programa que se base en Input/Output, donde por medio de un menu se pueda configurar diferentes parámetros para realizar una simulación. Una primera configuración deseada en indicar cierto tipo de apuesta y repetir la misma cierta cantidad de veces de acuerdo a cierto número indicado con anterioridad, realizando la siguiente apuesta con el monto resultante de la apuesta que le precede.

# Valor de las fichas

Para realizar las apuestas se tomara los siguientes valores:

|Denominación|Color|
|--|--|
| $1 | Blanco/Gris |
| $5 | Rojo |
| $10 | Azul |
| $25 | Verde |
| $100 | Negro |
| $500 | Morado/Violeta |
| $1000 | Naranja/Amarillo |

# Ejemplo de la interfaz.

```text
    --- SIMULACIÓN DE RULETA ---

Monto para iniciar: 50
Cantidad de apuestas: 5

Selecione una opción:

    [A] Cambiar monto inicial
    [B] Cambiar cantidad de apuestas
    [C] Indicar las apuestas
    [D] Empezar simulación

Indicar opción:
```

# Resultado esperado

En el desarrollo de la simulación, se debe ir generando un registro de la información que se va produciendo para que una vez finalice la simulación de las apuestas, se consolide esta información en tablas que despues serán exportadas en archivos csv y almacenados en una carpeta que corresponde a la simulación ejecutada.

El nombre de la carpeta que almacene las tablas producto de la simulación debera ir con el siguiente formato `yyyymmdd_hhmm` indicando la fecha de la simulación.

Se debe llevar una tabla en un archivo csv con el nombre `registros.csv` de los resultados generales de las simulaciones realizadas.

## Registros de las simulaciones

Ejemplo de la tabla `registros.csv`:

|Simulación| Total apostado | Total Ganado |
|:---------|:---------------|:-------------|
|20261001_1628|$150000 | $450000 |
|20261001_1454|$150000 | $70000 |

## Simulaciones

En la carpeta `yyyymmdd_hhmm` se debera guardar las tablas `apuestas.csv`, `numeros.csv` y `stats.csv`.

La tabla `apuestas.csv` debera registrar la siguiente información

|Columna|Descripción|
|:------------------|:----|
|No apuesta         |Cantidad de apuestas registradas|
|Apuesta            |La apuesta realizada sobre la mesa|
|Monto              |Cantidad de dinero en el bolsillo (No se cuenta el que se encuentra en la mesa)|
|Cantidad apostada  |Cantidad de dinero sobre la mesa en la apuesta realizada|
|Ganancia           |Cantidad de dinero ganado con la apuesta realizada|
|Monto final        |Cantidad de dinero en el bolsillo más la ganancia obtenida|

# PDTES

- Indicar formato de tablas para que se exporte.
  - Registros de números obtenidos.
  - Registro de la partida simulada.
- Indicar el nombre de la caprte que almacenara las tablas.
- Generar un registro de las simulaciones ejecutadas almacenando los resultados generales.
