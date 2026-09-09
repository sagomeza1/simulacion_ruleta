# Contenido del archivo: /simulacion_ruleta/simulacion_ruleta/src/simulacion_ruleta/ruleta/modelos.py

class Ruleta:
    def __init__(self, variante):
        self.variante = variante
        self.casillas = self.definir_casillas()

    def definir_casillas(self):
        if self.variante == 'Europea':
            return list(range(37))  # 0-36
        elif self.variante == 'Americana':
            return list(range(38))  # 0-36 y 00
        else:
            raise ValueError("Variante de ruleta no válida.")

class Casilla:
    def __init__(self, numero):
        self.numero = numero
        self.color = self.definir_color()

    def definir_color(self):
        if self.numero == 0:
            return 'Verde'
        elif self.numero in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]:
            return 'Rojo'
        else:
            return 'Negro'

class Apuesta:
    def __init__(self, monto, tipo, seleccion):
        self.monto = monto
        self.tipo = tipo
        self.seleccion = seleccion

    def validar(self):
        # Implementar lógica de validación de apuestas
        pass