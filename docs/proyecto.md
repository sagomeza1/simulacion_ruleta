# ¿Cuál es el propósito del proyecto?

Realizar una simulación de una ruleta para generar una estrategia que permita generar ganancias.

# ¿Qué debe requerir el proyecto?

Una simulación de la ruleta que permita experimentar con las diferentes formas de apuestas.

# ¿Qué debe contener la interfaz?

Se esta pensando una interfaz CLI, con un programa que se base en Input/Output, donde por medio de un menu se pueda configurar diferentes parámetros para realizar una simulación. Una primera configuración deseada en indicar cierto tipo de apuesta y repetir la misma cierta cantidad de veces de acuerdo a cierto número indicado con anterioridad, realizando la siguiente apuesta con el monto resultante de la apuesta que le precede.

# Valor de las fichas

Para realizar las apuestas se tomara los siguientes valores:

- $1 (Blanco/Gris)
- $5 (Rojo)
- $10 (Azul)
- $25 (Verde)
- $100 (Negro)
- $500 (Morado/Violeta)
- $1000 (Naranja/Amarillo)

# Ejemplo de la interfaz.

```text
--- SIMULACIÓN DE RULETA ---

Monto para iniciar: 50
Cantidad de apuestas: 5

[] Cambiar monto inicial
[] Cambiar cantidad de apuestas
[] Indicar las apuestas
[] Empezar simulación
```

# Resultado esperado

Cuando finalice la simulación de las apuesetas, se debe generar una tabla que despues será exportada en un archivo csv que va contener la siguiente información:

