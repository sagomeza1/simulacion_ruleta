# Especificación de Requisitos y Arquitectura: Simulador de Ruleta en Python

Documento completo y estandarizado para la implementación por parte de agentes de desarrollo e Inteligencia Artificial.

---

# 1. Propósito del Proyecto

Desarrollar una aplicación interactiva en Python que ejecute simulaciones de juego de ruleta (Americana y Europea) para evaluar, analizar y comparar la efectividad de distintas estrategias financieras y de apuestas. El sistema procesará las entradas del usuario a través de una interfaz de consola y generará reportes estructurados mediante archivos CSV que consolidan los datos estadísticos y financieros de cada ejecución.

---

# 2. Requisitos Generales del Sistema

* **Lenguaje y Versión:** Python 3.10 o superior.
* **Estilo de Código:** Cumplimiento estricto de las directrices de estilo PEP 8.
* **Arquitectura de Software:** Programación Orientada a Objetos (POO) modular con tipado estático explícito (`typing`).
* **Librerías Permitidas:**
* **Librería estándar:** `os`, `sys`, `random`, `datetime`, `re`, `typing`.
* **Librerías externas:** `pandas` (para la manipulación, consolidación y exportación de datos a CSV).


* **Interfaz de Usuario:** Exclusivamente por consola interactiva (Input/Output).

---

# 3. Reglas de Negocio del Juego de Ruleta

## 3.1. Tipos de Ruleta Elegibles

El sistema debe permitir al usuario seleccionar el tipo de ruleta al iniciar la configuración del juego o simulación:

1. **Ruleta Europea:**
* Total de casillas: 37 ($0, 1 \dots 36$).
* Apuestas exclusivas: **Cuatro Primeros (FF)**.


2. **Ruleta Americana:**
* Total de casillas: 38 ($0, 00, 1 \dots 36$).
* Apuestas exclusivas: **Línea Superior / Basket (BA)**.



## 3.2. Mapeo de Números y Colores

* **Verde:** `0` (y `00` en ruleta americana).
* **Rojo (18 números):** 1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36.
* **Negro (18 números):** 2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35.

---

# 4. Modos de Simulación y Reglas de Parada

1. **Modo Sencillo:**
* El usuario ingresa un monto inicial de dinero en su bolsillo.
* Se ejecuta ronda por ronda. En cada partida, el usuario ingresa la apuesta que desea realizar (se permite apostar $0 para pasar de ronda).
* La sesión finaliza cuando el usuario decide salir o por bancarrota (saldo igual a 0).


2. **Modo Simulación Estática:**
* Requiere los siguientes parámetros de entrada:
* Tipo de ruleta.
* Monto inicial.
* Apuesta fija (cadena con una o varias apuestas combinadas en la misma ronda).
* Cantidad total de partidas a simular.


* Criterio de detención: Se detiene inmediatamente si se completa el número de partidas programadas o si ocurre bancarrota (el saldo en bolsillo es $0$ o resulta inferior al monto total requerido para la apuesta fija de la siguiente ronda).


3. **Modo Simulación Dinámica:**
* Requiere los siguientes parámetros de entrada:
* Tipo de ruleta.
* Monto inicial.
* Apuesta fija (cadena con una o varias apuestas combinadas en la misma ronda).
* Lista de apuestas dinámicas ingresadas en una sola línea separadas por comas (pool de apuestas elegibles).
* Cantidad total de partidas a simular.


* Lógica de ejecución: En cada jugada, el sistema selecciona de manera aleatoria una apuesta del pool configurado y la ejecuta.
* Criterio de detención: Completa las iteraciones configuradas o se detiene por bancarrota si el saldo en el bolsillo es $0$ o insuficiente para cubrir la apuesta seleccionada al azar.



---

# 5. Codificación Estándar de Apuestas

## 5.1. Sintaxis de Entrada

Toda apuesta ingresada por la consola (sea individual o en lote) debe cumplir con la siguiente estructura de representación:

$$\text{Formato: } \langle\text{Monto}\rangle\langle\text{Abreviatura}\rangle[\langle\text{Selección}\rangle]$$

* **Expresión Regular de Validación (Regex):** `^\d+[A-Z]{2}(\[[\w,-]+\])?$`
* **Ingreso Múltiple:** Cuando el usuario realice varias apuestas dentro de una misma jugada o defina un pool dinámico, las apuestas deberán ingresarse en **una sola línea separadas por comas**.
* *Ejemplo:* `10SU[3], 5RE, 25DZ[1st]`



## 5.2. Tabla Oficial de Apuestas, Pagos y Codificación

| Apuesta | Descripción | Cobertura | Pago (Ganancia) | Abreviatura | Ejemplo |
| --- | --- | --- | --- | --- | --- |
| **Pleno (Straight Up)** | Un único número específico ($0..36$ o $00$) | 1 | 35 a 1 | `SU` | `10SU[3]` |
| **Pareja / Caballo (Split)** | Dos números adyacentes | 2 | 17 a 1 | `SP` | `10SP[1,2]` |
| **Talla / Calle (Street)** | Fila horizontal de 3 números | 3 | 11 a 1 | `ST` | `10ST[4,5,6]` |
| **Cuadro / Esquina (Corner)** | Intersección de 4 números | 4 | 8 a 1 | `CO` | `10CO[4,5,7,8]` |
| **Cuatro Primeros (First Four)** | *(Solo Europea)* Números 0, 1, 2, 3 | 4 | 8 a 1 | `FF` | `10FF` |
| **Línea Superior (Top Line / Basket)** | *(Solo Americana)* Números 0, 00, 1, 2, 3 | 5 | 6 a 1 | `BA` | `10BA` |
| **Seisena / Línea (Line)** | Seis números (2 calles contiguas) | 6 | 5 a 1 | `LI` | `10LI[1-6]` |
| **Docena (Dozen)** | Bloque de 12 (`1st`: 1-12, `2nd`: 13-24, `3rd`: 25-36) | 12 | 2 a 1 | `DZ` | `10DZ[1st]` |
| **Columna (Column)** | Línea vertical (`1st`, `2nd`, `3rd`) | 12 | 2 a 1 | `CL` | `10CL[1st]` |
| **Falta / Menores (Low)** | Números del 1 al 18 | 18 | 1 a 1 | `LO` | `10LO` |
| **Pasa / Mayores (High)** | Números del 19 al 36 | 18 | 1 a 1 | `HI` | `10HI` |
| **Pares (Even)** | Números pares (excluye 0 y 00) | 18 | 1 a 1 | `EV` | `10EV` |
| **Impares (Odd)** | Números impares | 18 | 1 a 1 | `OD` | `10OD` |
| **Rojos (Red)** | Color rojo | 18 | 1 a 1 | `RE` | `10RE` |
| **Negros (Black)** | Color negro | 18 | 1 a 1 | `BL` | `10BL` |

---

# 6. Especificación de la Interfaz de Consola (ASCII UI)

```text
==================================================
           --- SIMULACIÓN DE RULETA ---
==================================================

Seleccione el tipo de juego:

    [A] Modo Sencillo
    [B] Simulación Estática
    [C] Simulación Dinámica
    [X] Salir

Indicar opción: 

```

```text
==================================================
           --- SIMULACIÓN DE RULETA ---
              Modo Simulación Estática
==================================================

Parámetros actuales:
  - Tipo de Ruleta   : Americana
  - Monto inicial    : $500
  - Cantidad juegos  : 100
  - Apuesta fija     : 5SU[3], 10SU[00], 20RE

Seleccione una opción:

    [A] Iniciar simulación
    [B] Modificar tipo de ruleta
    [C] Modificar monto inicial
    [D] Modificar cantidad de juegos
    [E] Modificar apuesta fija (separada por comas)
    [X] Atrás

Indicar opción: 

```

```text
==================================================
           --- SIMULACIÓN DE RULETA ---
              Modo Simulación Dinámica
==================================================

Parámetros actuales:
  - Tipo de Ruleta   : Europea
  - Monto inicial    : $1000
  - Cantidad juegos  : 500
  - Apuesta fija     : 5SU[3], 10SU[00], 20RE
  - Pool de apuestas : 10RE, 10BL, 5SU[7], 15DZ[1st], 20LO

Seleccione una opción:

    [A] Iniciar simulación
    [B] Modificar tipo de ruleta
    [C] Modificar monto inicial
    [D] Modificar cantidad de juegos
    [E] Modificar apuesta fija (separada por comas)
    [F] Configurar lista de apuestas (separada por comas)
    [X] Atrás

Indicar opción: 

```

---

# 7. Persistencia de Datos y Archivos CSV

La manipulación de los DataFrames y la exportación de archivos debe ser gestionada mediante la librería `pandas`.

## 7.1. Estructura de Directorios

```text
/proyecto_ruleta
│
├── main.py
├── registros.csv (Global, acumulativo)
└── /simulaciones/
    └── YYYYMMDD_HHMM/
        ├── apuestas.csv
        ├── numeros.csv
        └── stats.csv

```

## 7.2. Especificación de Archivos Generados

* **Separador de campos:** Coma (`,`).
* **Codificación:** `utf-8`.

### 1. Archivo Global: `registros.csv`

Ubicado en la raíz del proyecto. Permite anexar (`mode='a'`) el resumen consolidado de cada simulación terminada.

* **Columnas:**

| Columna | Descripción |
| --- | --- |
| `Simulacion` | Nombre de la carpeta de la simulación (`YYYYMMDD_HHMM`). |
| `Modo` | Tipo de modo ejecutado (`Sencillo`, `Estatica`, `Dinamica`). |
| `Ruleta` | Variante utilizada (`Europea` o `Americana`). |
| `TotalApostado` | Suma acumulada de todo el dinero puesto en mesa durante las jugadas. |
| `TotalGanado` | Suma acumulada del dinero devuelto por ganancias. |
| `BalanceFinal` | Saldo final disponible en el bolsillo al concluir la simulación. |
| `CausaFin` | Motivo de finalización (`Bancarrota`, `JuegosCompletados`, `TerminadoPorUsuario`). |

### 2. Archivos Internos por Simulación (`/simulaciones/YYYYMMDD_HHMM/`):

#### A. `apuestas.csv`

Registra el historial de las jugadas realizadas corrida a corrida.

| Columna | Descripción |
| --- | --- |
| `NoApuesta` | Número secuencial de la jugada ($1, 2, 3 \dots$). |
| `Apuesta` | Cadena representativa de la apuesta realizada (ej. `10SU[3], 20RE`). |
| `MontoInicial` | Dinero en el bolsillo antes de realizar la apuesta de la ronda. |
| `CantidadApostada` | Dinero total colocado sobre la mesa en esa partida. |
| `Ganancia` | Monto bruto obtenido como ganancia en la jugada ($0$ si no acertó). |
| `MontoFinal` | Dinero restante en bolsillo tras resolver la apuesta (`MontoInicial - CantidadApostada + Ganancia`). |

#### B. `numeros.csv`

Registra la secuencia cronológica de tiradas de la ruleta.

| Columna | Descripción |
| --- | --- |
| `NoPartida` | Número secuencial de la tirada. |
| `Numero` | Número donde cayó la bola (`0`, `00`, `1` al `36`). |
| `Color` | Color asignado al número (`Verde`, `Rojo`, `Negro`). |

#### C. `stats.csv`

Frecuencia observada de cada casilla disponible en la rueda. Debe listar la totalidad de casillas posibles de la ruleta seleccionada, incluso aquellas con $0$ apariciones.

| Columna | Descripción |
| --- | --- |
| `Numero` | Número de la casilla (`0`, `00` si es Americana, `1` al `36`). |
| `Color` | Color de la casilla (`Verde`, `Rojo`, `Negro`). |
| `Cantidad` | Total de veces que la ruleta se detuvo en dicho número durante la simulación. |