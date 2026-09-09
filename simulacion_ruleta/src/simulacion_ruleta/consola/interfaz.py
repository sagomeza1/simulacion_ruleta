# Contenido del archivo: /simulacion_ruleta/simulacion_ruleta/src/simulacion_ruleta/consola/interfaz.py

class InterfazConsola:
    def __init__(self):
        self.bienvenida()

    def bienvenida(self):
        print("Bienvenido al Simulador de Ruleta")
        print("Seleccione una opción del menú para comenzar.")

    def mostrar_menu(self):
        print("\nMenú de Opciones:")
        print("1. Modo Sencillo")
        print("2. Simulación Estática")
        print("3. Simulación Dinámica")
        print("4. Salir")

    def obtener_opcion(self):
        opcion = input("Ingrese su opción: ")
        return opcion

    def mostrar_mensaje(self, mensaje):
        print(mensaje)

    def mostrar_resultados(self, resultados):
        print("\nResultados de la Simulación:")
        for resultado in resultados:
            print(resultado)

    def despedida(self):
        print("Gracias por jugar. ¡Hasta la próxima!")