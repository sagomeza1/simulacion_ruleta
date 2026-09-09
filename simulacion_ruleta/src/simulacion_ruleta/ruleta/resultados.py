# resultados.py

import pandas as pd
from typing import List, Dict

class Resultados:
    def __init__(self):
        self.resultados = []

    def agregar_resultado(self, numero: int, color: str, monto_inicial: float, cantidad_apostada: float, ganancia: float):
        resultado = {
            'Numero': numero,
            'Color': color,
            'MontoInicial': monto_inicial,
            'CantidadApostada': cantidad_apostada,
            'Ganancia': ganancia
        }
        self.resultados.append(resultado)

    def exportar_a_csv(self, ruta: str):
        df = pd.DataFrame(self.resultados)
        df.to_csv(ruta, index=False, encoding='utf-8')