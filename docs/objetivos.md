# Objetivos del Proyecto: Simulador de Ruleta en Python

## 1. Visión General del Proyecto
El proyecto consiste en una aplicación interactiva en Python que ejecuta simulaciones de juego de ruleta (Americana y Europea) a través de una interfaz de consola (ASCII UI). Su propósito es evaluar, analizar y comparar la efectividad de distintas estrategias financieras y de apuestas, procesando las entradas del usuario y generando reportes estructurados en archivos CSV que consolidan los datos estadísticos y financieros de cada ejecución.

## 2. Objetivos Principales (Core Objectives)
*   **Objetivo General:** Desarrollar un simulador interactivo de ruleta en Python que permita ejecutar partidas en modos sencillo, estático y dinámico, registrando detalladamente el comportamiento financiero y estadístico de cada sesión en archivos CSV.
*   **Objetivos Específicos:**
    *   Implementar las reglas de negocio, pagos y mapeos de casillas/colores para las variantes de Ruleta Europea (37 casillas) y Ruleta Americana (38 casillas).
    *   Desarrollar un parser de apuestas basado en expresiones regulares para validar la codificación estándar y sintaxis de apuestas en consola.
    *   Proveer tres modos de juego y simulación: Modo Sencillo (interactivo ronda a ronda), Modo Simulación Estática (apuesta fija por $N$ partidas) y Modo Simulación Dinámica (apuesta fija más selección aleatoria desde un pool de apuestas).
    *   Gestionar la persistencia de datos mediante la librería `pandas`, generando archivos CSV tanto globales (`registros.csv`) como por simulación (`apuestas.csv`, `numeros.csv`, `stats.csv`).

## 3. Alcance del Proyecto (Scope)
### 3.1. Características Incluidas (In-Scope)
*   **Gestión de Ruletas:** Soporte completo para Ruleta Europea y Ruleta Americana, incluyendo apuestas exclusivas (Cuatro Primeros `FF` en Europea, Línea Superior/Basket `BA` en Americana).
*   **Codificación Estándar de Apuestas:** Formato `<Monto><Abreviatura>[<Selección>]` validado mediante Regex (`^\d+[A-Z]{2}(\[[\w,-]+\])?$`), admitiendo apuestas múltiples separadas por comas.
*   **Modos de Ejecución:**
    *   *Modo Sencillo:* Control manual ronda a ronda, detención por bancarrota o retiro voluntario.
    *   *Modo Simulación Estática:* Configuración previa de parámetros y ejecución de $N$ partidas con apuesta fija.
    *   *Modo Simulación Dinámica:* Configuración de apuesta fija y pool de apuestas dinámicas elegibles al azar en cada jugada.
*   **Reglas de Parada Automatizadas:** Finalización inmediata por cumplimiento de partidas ($N$) o por bancarrota (saldo $0$ o insuficiente para la apuesta).
*   **Interfaz de Usuario (ASCII UI):** Menús navegables interactivos por consola para la selección de modos y edición de parámetros.
*   **Persistencia y Estructura de Salida:**
    *   Creación de la carpeta `/simulaciones/YYYYMMDD_HHMM/` para cada ejecución.
    *   Generación de `apuestas.csv`, `numeros.csv` y `stats.csv` por simulación.
    *   Actualización incremental (`mode='a'`) del archivo consolidado `registros.csv` en la raíz del proyecto.

### 3.2. Fuera de Alcance (Out-of-Scope)
*   Interfaz gráfica de usuario (GUI) o aplicaciones web.
*   Conexión a bases de datos relacionales o NoSQL.
*   Uso de frameworks de API REST (FastAPI, Flask, etc.).
*   Estrategias de apuestas automatizadas complejas distintas a las especificadas (ej. Martingala programada dinámicamente según resultados previos).
*   Análisis gráfico o visualizaciones integradas (Matplotlib, Seaborn, etc.).

## 4. Criterios de Aceptación y Éxito
*   **Compatibilidad y Estilo:** Ejecución limpia en Python 3.10+, cumplimiento estricto de la guía de estilo PEP 8 y anotaciones de tipado explícitas (`typing`).
*   **Precisión Financiera y Matemática:** Cálculo correcto de ganancias y retornos según la tabla oficial de pagos (desde 35 a 1 en Pleno hasta 1 a 1 en apuestas simples) y actualización precisa del saldo en bolsillo.
*   **Validación de Entradas:** Rechazo correcto de apuestas que no cumplan con la sintaxis Regex o que incluyan tipos de apuesta incompatibles con la ruleta seleccionada.
*   **Integridad de Persistencia:**
    *   Generación exitosa de la estructura de directorios `/simulaciones/YYYYMMDD_HHMM/`.
    *   Listado completo de todas las casillas disponibles en `stats.csv`, incluyendo aquellas con $0$ apariciones.
    *   Registro acumulativo en `registros.csv` sin sobrescribir las ejecuciones previas.