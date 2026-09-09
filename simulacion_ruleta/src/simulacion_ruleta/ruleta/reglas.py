# Contenido del archivo: /simulacion_ruleta/simulacion_ruleta/src/simulacion_ruleta/ruleta/reglas.py

class ReglasRuleta:
    def __init__(self, variante):
        self.variante = variante
        self.pagos = self.definir_pagos()
        self.colores = self.definir_colores()

    def definir_pagos(self):
        if self.variante == 'europea':
            return {
                'pleno': 35,
                'seis': 5,
                'cuatro': 8,
                'tres': 11,
                'dos': 17,
                'uno': 1
            }
        elif self.variante == 'americana':
            return {
                'pleno': 35,
                'seis': 5,
                'cuatro': 8,
                'tres': 11,
                'dos': 17,
                'uno': 1
            }
        else:
            raise ValueError("Variante de ruleta no válida")

    def definir_colores(self):
        return {
            '0': 'verde',
            '00': 'verde',
            '1': 'rojo',
            '2': 'negro',
            '3': 'rojo',
            '4': 'negro',
            '5': 'rojo',
            '6': 'negro',
            '7': 'rojo',
            '8': 'negro',
            '9': 'rojo',
            '10': 'negro',
            '11': 'rojo',
            '12': 'negro',
            '13': 'rojo',
            '14': 'negro',
            '15': 'rojo',
            '16': 'negro',
            '17': 'rojo',
            '18': 'negro',
            '19': 'rojo',
            '20': 'negro',
            '21': 'rojo',
            '22': 'negro',
            '23': 'rojo',
            '24': 'negro',
            '25': 'rojo',
            '26': 'negro',
            '27': 'rojo',
            '28': 'negro',
            '29': 'rojo',
            '30': 'negro',
            '31': 'rojo',
            '32': 'negro',
            '33': 'rojo',
            '34': 'negro',
            '35': 'rojo',
            '36': 'negro'
        }

    def obtener_pago(self, tipo_apuesta):
        return self.pagos.get(tipo_apuesta, 0)

    def obtener_color(self, numero):
        return self.colores.get(str(numero), 'invalido')