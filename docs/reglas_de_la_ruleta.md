# Guía Completa y Reglas del Juego de la Ruleta

La **ruleta** es uno de los juegos de azar más populares y emblemáticos de los casinos. El objetivo del juego es predecir en qué casilla numerada y coloreada se detendrá una pequeña bola lanzada sobre un cilindro giratorio.

---

## 1. Componentes del Juego

* **El Cilindro (Ruleta):** Disco giratorio dividido en casillas numeradas del 0 al 36 (y el 00 en la versión americana). Los números están divididos en dos colores principales: rojo y negro, alternados, a excepción del 0 y 00, que son de color verde.
* **El Tapete (Paño):** Área donde los jugadores colocan sus fichas para realizar sus apuestas. Muestra la tabla numérica (0 al 36) y las secciones para las apuestas exteriores.
* **La Bola:** Pequeña esfera (tradicionalmente de marfil, hoy en día de resina o teflón) que el crupier lanza en dirección opuesta al giro del cilindro.
* **Las Fichas:** Representan la cantidad apostada. En casinos físicos, suelen ser fichas de colores específicos para cada jugador para evitar confusiones.

---

## 2. Diferencias Principales: Ruleta Europea vs. Ruleta Americana

| Característica | Ruleta Europea / Francesa | Ruleta Americana |
| :--- | :--- | :--- |
| **Casillas totales** | 37 (del 0 al 36) | 38 (del 0 al 36 + **00**) |
| **Casillas verdes** | 1 (el `0`) | 2 (el `0` y el `00`) |
| **Ventaja de la casa (Estándar)** | **2,70%** | **5,26%** |
| **Reglas especiales en 'Cero'** | *La Partage* / *En Prison* (reduce ventaja al 1,35%) | Ninguna (salvo variaciones locales) |
| **Disposición de números** | Secuencia aleatoria tradicional europea | Secuencia modificada para equilibrar 0 y 00 |

### Reglas Especiales de la Ruleta Europea / Francesa

Cuando la bola cae en la casilla del **0**, las apuestas sencillas (Rojo/Negro, Par/Impar, Falta/Pasa) suelen verse sujetas a una de estas dos reglas según el casino:

1. **La Partage:** El jugador pierde la mitad de su apuesta sencilla y recupera la otra mitad inmediatamente.
2. **En Prison (En Prisión):** La apuesta sencilla queda "bloqueada" para la siguiente ronda. Si en el siguiente giro la apuesta resulta ganadora, el jugador recupera el 100% de su dinero inicial (sin ganancias adicionales); si pierde, pierde toda la apuesta.

---

## 3. Tipos de Apuestas, Pagos y Probabilidades

Las apuestas se dividen principalmente en **Apuestas Interiores** (dentro de la cuadrícula numérica) y **Apuestas Exteriores** (fuera de la cuadrícula numérica).

> **Nota sobre el Pago:** La proporción se expresa como `X:1`, lo que significa que ganas `X` unidades por cada `1` unidad apostada, además de conservar tu ficha original.

### A. Apuestas Interiores

Tienen probabilidades de ganancia más bajas pero ofrecen los pagos más altos.

| Apuesta | Descripción | Cobertura | Pago | Probabilidad Europea | Probabilidad Americana |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Pleno (Straight Up)** | Apostar a un único número específico. | 1 número | **35:1** | 2,70% | 2,63% |
| **Pareja o Caballo (Split)** | Ficha en la línea que separa dos números adyacentes. | 2 números | **17:1** | 5,41% | 5,26% |
| **Talla o Calle (Street)** | Ficha al final de una fila horizontal de 3 números. | 3 números | **11:1** | 8,11% | 7,89% |
| **Cuadro o Esquina (Corner)** | Ficha en la intersección donde se cruzan 4 números. | 4 números | **8:1** | 10,81% | 10,53% |
| **Línea Superior (Basket)** | *(Solo en Americana)* Apuesta al 0, 00, 1, 2, y 3. | 5 números | **6:1** | N/A | 13,16% |
| **Seisena o Línea (Line)** | Ficha en la intersección de dos filas contiguas. | 6 números | **5:1** | 16,22% | 15,79% |

---

### B. Apuestas Exteriores

Tienen mayores probabilidades de éxito pero ofrecen pagos más bajos.

| Apuesta | Descripción | Cobertura | Pago | Probabilidad Europea | Probabilidad Americana |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Rojo / Negro** | Color del número ganador. | 18 números | **1:1** | 48,65% | 47,37% |
| **Par / Impar** | Si el número es par o impar (excluye 0 y 00). | 18 números | **1:1** | 48,65% | 47,37% |
| **Falta (1-18) / Pasa (19-36)** | Si el número está en la mitad inferior o superior. | 18 números | **1:1** | 48,65% | 47,37% |
| **Docenas (1ª, 2ª, 3ª)** | Bloques de 12 números: (1-12), (13-24) o (25-36). | 12 números | **2:1** | 32,43% | 31,58% |
| **Columnas (1ª, 2ª, 3ª)** | Apuesta a una de las tres filas verticales completas. | 12 números | **2:1** | 32,43% | 31,58% |

---

## 4. Flujo Paso a Paso para Replicar/Implementar el Juego

Para programar o coordinar una partida de ruleta, el ciclo de una ronda sigue este procedimiento estandarizado:

```
[1. Apertura de Apuestas] -> [2. Cierre de Apuestas] -> [3. Giro & Resultado] -> [4. Resolución & Pagos]
```

### Paso 1: Apertura de Apuestas (*"Hagan sus apuestas"*)
* El crupier/sistema anuncia el inicio de la ronda.
* Los jugadores colocan sus fichas en las posiciones del tapete correspondientes a las apuestas elegidas.
* Cada mesa fija un límite mínimo y máximo de apuesta por posición.

### Paso 2: Lanzamiento y Cierre (*"No va más"*)
* El crupier hace girar el cilindro en una dirección y lanza la bola en la dirección opuesta a lo largo del riel exterior del cilindro.
* Cuando la bola empieza a perder velocidad y está a punto de caer a las casillas, se anuncia *"No va más"* (o *No more bets*). A partir de este momento no se permite colocar ni modificar apuestas.

### Paso 3: Determinación del Resultado
* La bola cae en una de las casillas numeradas y se detiene.
* Se anuncia públicamente el número y color ganador (ejemplo: *"21, Negro, Impar y Pasa"*).
* En el casino físico, se coloca un marcador físico llamado *Dolly* sobre el número ganador en el tapete.

### Paso 4: Liquidación y Pagos
1. **Retiro:** El casino retira todas las fichas perdedoras del paño.
2. **Pago:** Se efectúa el pago a las apuestas ganadoras según las proporciones estipuladas.
3. **Liberación:** Se retira el *Dolly* del tapete y el tablero queda listo para la siguiente ronda.

---

## 5. Fórmulas de Matemáticas del Juego (Para Desarrolladores)

Si deseas implementar la lógica matemática en software:

1. **Retorno al Jugador (RTP):**
   $$\text{RTP (Europea)} = \left( \frac{36}{37} \right) \times 100 \approx 97,3\%$$
   $$\text{RTP (Americana)} = \left( \frac{36}{38} \right) \times 100 \approx 94,74\%$$

2. **Cálculo del Pago Neto:**
   $$\text{Ganancia Neta} = \text{Monto Apostado} \times \left( \frac{36 - N}{N} \right)$$
   *Donde $N$ es la cantidad de números cubiertos en la apuesta.*

   * *Ejemplo (Cuadro / 4 números):*
     $$\text{Ganancia} = 10 \times \left( \frac{36 - 4}{4} \right) = 10 \times 8 = 80 \text{ unidades}$$