# Simulación de una ruleta

Simulador de ruleta (Europea y Americana) en Python, operado 100% desde consola (CLI). Permite ejecutar partidas manuales, simulaciones estáticas (apuesta fija repetida) y simulaciones dinámicas (pool de apuestas elegidas al azar), con el objetivo de analizar y comparar estrategias de apuestas y su efecto sobre el saldo del jugador.

La especificación completa de requisitos y arquitectura está en [`docs/proyecto.md`](docs/proyecto.md); las reglas del juego (pagos, probabilidades, tipos de apuesta) están en [`docs/reglas_de_la_ruleta.md`](docs/reglas_de_la_ruleta.md).

---

## 1. Requisitos

* **Python 3.10 o superior** (desarrollado y probado con Python 3.14).
* Librería externa: **`pandas`** (ver `requirements.txt`).

---

## 2. Instalación

Clona el repositorio y entra a la carpeta del proyecto:

```bash
git clone git@github.com:sagomeza1/simulacion_ruleta.git
cd simulacion_ruleta
```

### Instalar dependencias

Se recomienda usar un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate      # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

> **Nota (sistemas sin `pip` preinstalado, ej. Ubuntu/Debian recientes):** si `python3 -m venv` falla porque falta `ensurepip`, puedes instalar `pip` manualmente sin tocar el sistema:
> ```bash
> curl -fsSL https://bootstrap.pypa.io/pip/pip.pyz -o /tmp/pip.pyz
> python3 /tmp/pip.pyz install --user -r requirements.txt
> ```

---

## 3. Ejecución

El punto de entrada es `main.py`. Se ejecuta directamente con Python, sin argumentos (toda la configuración se hace de forma interactiva por consola):

```bash
python3 main.py
```

Al iniciar, se presenta el menú principal:

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

### Modo Sencillo `[A]`
Juego interactivo ronda por ronda: eliges tipo de ruleta y monto inicial, y en cada ronda ingresas tu apuesta (o `0` para pasar). Termina por decisión propia (`X`) o por bancarrota.

### Simulación Estática `[B]`
Define una **apuesta fija** que se repite automáticamente durante N partidas. Parámetros solicitados: tipo de ruleta, monto inicial, cantidad de partidas, apuesta fija. Se detiene al completar las partidas o por bancarrota.

### Simulación Dinámica `[C]`
Define un **pool de apuestas** candidatas; en cada ronda el sistema elige una al azar del pool y la ejecuta. Útil para comparar el comportamiento de distintas apuestas mezcladas a lo largo de muchas iteraciones.

### Simulación Mixta `[D]`
Combina lo mejor de los dos modos anteriores: defines una **apuesta fija** (parte Estática, se repite siempre) y un **pool de apuestas** (parte Dinámica, se elige una al azar en cada ronda). En cada jugada se apuestan **ambas simultáneamente** (apuesta fija + apuesta dinámica elegida), permitiendo analizar estrategias combinadas (ej. una cobertura base constante + exploración aleatoria adicional).

---

## 4. Codificación de apuestas

Toda apuesta se ingresa como texto con el formato:

```
<Monto><Abreviatura>[<Selección>]
```

Varias apuestas en la misma jugada (o en el pool dinámico) se separan por comas:

```
10SU[3], 5RE, 25DZ[1st]
```

| Apuesta | Abreviatura | Ejemplo |
| --- | --- | --- |
| Pleno (Straight Up) | `SU` | `10SU[3]` |
| Pareja (Split) | `SP` | `10SP[1,2]` |
| Calle (Street) | `ST` | `10ST[4,5,6]` |
| Cuadro (Corner) | `CO` | `10CO[4,5,7,8]` |
| Cuatro Primeros *(solo Europea)* | `FF` | `10FF` |
| Línea Superior / Basket *(solo Americana)* | `BA` | `10BA` |
| Seisena (Line) | `LI` | `10LI[1-6]` |
| Docena (Dozen) | `DZ` | `10DZ[1st]` |
| Columna (Column) | `CL` | `10CL[1st]` |
| Falta (Low 1-18) | `LO` | `10LO` |
| Pasa (High 19-36) | `HI` | `10HI` |
| Pares (Even) | `EV` | `10EV` |
| Impares (Odd) | `OD` | `10OD` |
| Rojos (Red) | `RE` | `10RE` |
| Negros (Black) | `BL` | `10BL` |

Tabla completa de pagos y probabilidades en [`docs/proyecto.md`](docs/proyecto.md#51-sintaxis-de-entrada) y [`docs/reglas_de_la_ruleta.md`](docs/reglas_de_la_ruleta.md).

---

## 5. Resultados y reportes generados

Cada simulación (Sencillo, Estática o Dinámica) genera una carpeta con marca de tiempo y exporta los resultados a CSV mediante `pandas`:

```text
/simulacion_ruleta
│
├── main.py
├── registros.csv                 # Global, acumulativo (resumen de cada simulación)
└── /simulaciones/
    └── YYYYMMDD_HHMM/
        ├── apuestas.csv           # Historial jugada a jugada
        ├── numeros.csv            # Secuencia de tiradas (número y color)
        └── stats.csv              # Frecuencia observada de cada casilla
```

* **`registros.csv`** (raíz del proyecto): se anexa (`mode='a'`) al finalizar cada simulación; no se sobrescribe entre ejecuciones.
* Las carpetas `/simulaciones/` y el archivo `registros.csv` **no se versionan en Git** (ver `.gitignore`): son datos generados localmente, no código fuente.

---

## 6. Estructura del proyecto

```text
simulacion_ruleta/
├── main.py                 # CLI interactiva (punto de entrada)
├── requirements.txt         # Dependencias (pandas)
├── roulette/
│   ├── wheel.py             # Rueda Europea/Americana, mapeo de colores
│   ├── bets.py              # Parser y validación de apuestas codificadas
│   ├── engine.py            # Motor de simulación (modos Estática/Dinámica)
│   └── storage.py           # Exportación de resultados a CSV (pandas)
├── docs/
│   ├── proyecto.md          # Especificación completa de requisitos y arquitectura
│   └── reglas_de_la_ruleta.md  # Reglas, pagos y probabilidades del juego
└── .vscode/                 # Configuración de editor (no afecta la ejecución)
```

---

## 7. Convenciones de desarrollo

* **Estilo de código:** PEP 8, con tipado estático explícito (`typing`) en firmas de funciones y clases.
* **Arquitectura:** Programación orientada a objetos modular — cada responsabilidad vive en su propio módulo dentro de `roulette/` (rueda, apuestas, motor, persistencia), desacoplado de la capa de interfaz (`main.py`).
* **Validación de apuestas:** toda cadena de apuesta se valida contra la expresión regular `^\d+[A-Z]{2}(\[[\w,-]+\])?$` y contra las reglas de negocio (p. ej. `FF` solo en ruleta Europea, `BA` solo en Americana) antes de ejecutarse; errores se señalizan mediante `InvalidBetError`.
* **Control de versiones:** commits de la colaboradora `Laira` (agente IA) se registran con autor propio (`Laira <laira@users.noreply.github.com>`) para distinguirse claramente de los commits de Alejandro en el historial de Git.
* **Datos generados vs. código fuente:** `registros.csv` y `/simulaciones/` son artefactos de ejecución y están excluidos de Git (`.gitignore`); solo el código y la documentación se versionan.

---

## Licencia

Este proyecto está bajo licencia MIT — ver [`LICENSE`](LICENSE).
