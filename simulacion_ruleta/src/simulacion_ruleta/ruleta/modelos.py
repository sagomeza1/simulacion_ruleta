from typing import List, Union

Numero = Union[int, str]
ROJOS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
NEGROS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}


def normalizar_variante(variante: str) -> str:
    variantes = {"europea": "Europea", "americana": "Americana"}
    try:
        return variantes[variante.strip().lower()]
    except (AttributeError, KeyError) as error:
        raise ValueError(f"Variante de ruleta no válida: {variante}") from error


class Ruleta:
    def __init__(self, variante: str):
        self.variante = normalizar_variante(variante)
        self.casillas: List[Numero] = self.definir_casillas()

    def definir_casillas(self):
        if self.variante == "Europea":
            return list(range(37))
        return [0, "00", *range(1, 37)]

class Casilla:
    def __init__(self, numero: Numero):
        self.numero = numero
        self.color = self.definir_color()

    def definir_color(self) -> str:
        if self.numero == 0 or self.numero == "00":
            return "Verde"
        if isinstance(self.numero, int) and self.numero in ROJOS:
            return "Rojo"
        if isinstance(self.numero, int) and self.numero in NEGROS:
            return "Negro"
        raise ValueError(f"Casilla no válida: {self.numero}")