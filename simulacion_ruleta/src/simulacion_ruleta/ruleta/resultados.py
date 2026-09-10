# resultados.py

from dataclasses import dataclass
from typing import List, Union

from .modelos import Numero


@dataclass
class ResultadoTirada:
    numero: Numero
    color: str

class Resultados:
    def __init__(self):
        self.resultados: List[ResultadoTirada] = []

    def agregar_resultado(self, numero: Numero, color: str) -> None:
        self.resultados.append(ResultadoTirada(numero, color))