# Simulador de Ruleta en Python

Este proyecto es un simulador interactivo de ruleta que permite ejecutar partidas en diferentes modos, registrando el comportamiento financiero y estadístico de cada sesión. El simulador está diseñado para evaluar y comparar distintas estrategias de apuestas en las variantes de ruleta Americana y Europea.

## Contenido del Proyecto

- **src/simulacion_ruleta/**: Contiene el código fuente del simulador.
  - **main.py**: Punto de entrada de la aplicación.
  - **apuestas/**: Módulo que maneja las apuestas.
    - **modelos.py**: Definición de tipos de apuestas y estructuras de datos.
    - **parser.py**: Valida y procesa las entradas de apuestas.
  - **ruleta/**: Módulo que implementa la lógica del juego de ruleta.
    - **modelos.py**: Clases y estructuras de datos relacionadas con la ruleta.
    - **reglas.py**: Implementación de las reglas del juego.
    - **resultados.py**: Manejo de resultados de las tiradas.
  - **simulacion/**: Módulo que gestiona la lógica de simulación.
    - **gestor.py**: Ejecuta partidas y evalúa resultados.
    - **modos.py**: Define los diferentes modos de juego.
  - **consola/**: Módulo que gestiona la interfaz de usuario en consola.
    - **menus.py**: Implementa los menús interactivos.
    - **interfaz.py**: Maneja la entrada y salida de datos.
  - **persistencia/**: Módulo que maneja la exportación de datos.
    - **exportador_csv.py**: Exporta datos a archivos CSV.

- **tests/**: Contiene pruebas unitarias para el código del simulador.
  - **test_parser_apuestas.py**: Pruebas para el parser de apuestas.
  - **test_reglas_ruleta.py**: Pruebas para las reglas del juego.
  - **test_simulacion.py**: Pruebas para la lógica de simulación.
  - **test_exportador_csv.py**: Pruebas para la funcionalidad de exportación a CSV.

- **docs/**: Documentación del proyecto.
  - **objetivos.md**: Objetivos del proyecto.
  - **especificaciones.md**: Especificaciones técnicas del proyecto.

- **simulaciones/**: Directorio para almacenar las simulaciones generadas.

- **registros.csv**: Archivo que almacena el registro acumulativo de las simulaciones.

- **requirements.txt**: Lista de dependencias del proyecto.

- **pyproject.toml**: Configuración del proyecto y dependencias necesarias.

- **.gitignore**: Archivos y directorios que deben ser ignorados por Git.

## Instalación

1. Clona el repositorio:
   ```
   git clone <URL_DEL_REPOSITORIO>
   ```
2. Navega al directorio del proyecto:
   ```
   cd simulacion_ruleta
   ```
3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso

Ejecuta el simulador utilizando el siguiente comando:
```
python src/simulacion_ruleta/main.py
```

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT.