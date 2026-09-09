# Especificaciones Técnicas: Simulador de Ruleta en Python

## 1. Stack Tecnológico y Entorno
*   **Lenguaje de Programación:** Python 3.10 o superior.
*   **Frameworks / Librerías Principales:**
    *   *Librería Estándar:* `os`, `sys`, `random`, `datetime`, `re`, `typing`.
    *   *Librerías Externas:* `pandas` (para manipulación, consolidación y exportación de DataFrames a CSV).
*   **Gestión de Entornos / Contenedores:** [PENDIENTE: Especificar por el usuario]
*   **Base de Datos / Almacenamiento:** Archivos planos CSV gestionados a través de `pandas`.

## 2. Arquitectura y Estructura del Código
### 2.1. Patrón de Diseño / Arquitectura
*   **Programación Orientada a Objetos (POO) Modular:**
    *   Diseño basado en clases con responsabilidades bien delimitadas (ej. lógica del juego de ruleta, parser de apuestas, gestor de simulaciones, interfaz de consola y exportador de datos).
    *   Uso de tipado estático explícito mediante el módulo estándar `typing` (`Union`, `List`, `Dict`, `Optional`, etc.).

### 2.2. Guías de Estilo y Calidad de Código
*   Cumplimiento estricto del estándar **PEP 8** (nombres de variables, funciones, clases, sangría e importaciones).
*   Manejo estructurado de excepciones durante el consumo de entradas del usuario y procesamiento de datos.

## 3. Requerimientos Funcionales y Técnicos Detallados
### 3.1. Flujo de Datos / Lógica de Negocio
1.  **Inicio e Interacción:**
    *   Presentación del menú interactivo en consola (ASCII UI).
    *   Selección del modo de juego (`Sencillo`, `Simulación Estática`, `Simulación Dinámica`).
2.  **Configuración de Parámetros:**
    *   Definición de Variante (`Europea` o `Americana`).
    *   Definición de Monto Inicial, Cantidad de Juegos (para simulaciones), Apuesta Fija y Pool de Apuestas Dinámicas.
3.  **Procesamiento de Apuestas:**
    *   Validación de la cadena de apuesta mediante la expresión regular: `^\d+[A-Z]{2}(\[[\w,-]+\])?$`
    *   Descomposición de la apuesta múltiple (separada por comas) y verificación de compatibilidad según el tipo de ruleta (`FF` solo para Europea, `BA` solo para Americana).
4.  **Ejecución de la Tirada:**
    *   Generación pseudoaleatoria del resultado de la casilla (`0` a `36` en Europea; `0`, `00`, `1` a `36` en Americana) y mapeo del color (`Verde`, `Rojo`, `Negro`).
    *   Evaluación de aciertos y cálculo de ganancias brutas.
    *   Actualización del saldo en bolsillo: $\text{MontoFinal} = \text{MontoInicial} - \text{CantidadApostada} + \text{Ganancia}$.
5.  **Criterios de Parada:**
    *   Finalización al alcanzar la cantidad de juegos programada.
    *   Finalización por bancarrota si $\text{MontoFinal} = 0$ o si el saldo disponible es menor al monto requerido para la siguiente apuesta.
    *   Finalización manual decidida por el usuario en Modo Sencillo.
6.  **Persistencia y Exportación (Pandas):**
    *   Creación del directorio `/simulaciones/YYYYMMDD_HHMM/`.
    *   Exportación de DataFrames a `apuestas.csv`, `numeros.csv` y `stats.csv` (con codificación `utf-8` y separador `,`).
    *   Anexo incremental (`mode='a'`) en el archivo raíz `registros.csv`.

### 3.2. Especificaciones de Datos e Interfaces
*   **Entradas:**
    *   Comandos y selecciones a través de la consola interactiva (I/O).
    *   Cadenas de texto para apuestas en formato estandarizado (ej. `10SU[3], 5RE, 25DZ[1st]`).
*   **Salidas (Archivos CSV con separador `,` y codificación `utf-8`):**
    *   `registros.csv` (Raíz):
        *   Columnas: `Simulacion`, `Modo`, `Ruleta`, `TotalApostado`, `TotalGanado`, `BalanceFinal`, `CausaFin`.
    *   `apuestas.csv` (`/simulaciones/YYYYMMDD_HHMM/`):
        *   Columnas: `NoApuesta`, `Apuesta`, `MontoInicial`, `CantidadApostada`, `Ganancia`, `MontoFinal`.
    *   `numeros.csv` (`/simulaciones/YYYYMMDD_HHMM/`):
        *   Columnas: `NoPartida`, `Numero`, `Color`.
    *   `stats.csv` (`/simulaciones/YYYYMMDD_HHMM/`):
        *   Columnas: `Numero`, `Color`, `Cantidad` (incluye casillas con $0$ frecuencias).

## 4. Instrucciones de Contexto para GitHub Copilot
> **Nota para el Agente de Copilot:** Al desarrollar código para este repositorio, prioriza la optimización de código en Python, el manejo estructurado de excepciones y modularidad. Asegúrate de verificar este archivo de especificaciones antes de proponer cambios estructurales.