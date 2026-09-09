# Contenido del archivo: /simulacion_ruleta/simulacion_ruleta/src/simulacion_ruleta/consola/menus.py

class Menu:
    def mostrar_menu_principal(self):
        print("Bienvenido al Simulador de Ruleta")
        print("Seleccione un modo de juego:")
        print("1. Modo Sencillo")
        print("2. Modo Simulación Estática")
        print("3. Modo Simulación Dinámica")
        print("4. Salir")

    def seleccionar_modo(self):
        opcion = input("Ingrese el número de la opción deseada: ")
        return opcion

    def mostrar_menu_configuracion(self):
        print("Configuración de Parámetros")
        print("1. Seleccionar Variante de Ruleta")
        print("2. Establecer Monto Inicial")
        print("3. Establecer Cantidad de Juegos")
        print("4. Establecer Apuesta Fija")
        print("5. Volver al Menú Principal")

    def seleccionar_configuracion(self):
        opcion = input("Ingrese el número de la opción deseada: ")
        return opcion

    def mostrar_mensaje_error(self, mensaje):
        print(f"Error: {mensaje}")