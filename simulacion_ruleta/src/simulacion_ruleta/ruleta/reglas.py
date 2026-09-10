# Contenido del archivo: /simulacion_ruleta/simulacion_ruleta/src/simulacion_ruleta/ruleta/reglas.py

from typing import Union

from ..apuestas.modelos import Apuesta
from .modelos import Casilla, Numero, Ruleta, normalizar_variante


PAGOS = {"SU": 35, "SP": 17, "ST": 11, "CO": 8, "FF": 8, "BA": 6,
         "LI": 5, "DZ": 2, "CL": 2, "LO": 1, "HI": 1, "EV": 1,
         "OD": 1, "RE": 1, "BL": 1}


class ReglasRuleta:
    def __init__(self, variante: str):
        self.ruleta = Ruleta(variante)
        self.variante = self.ruleta.variante
        self.pagos = PAGOS.copy()

    def obtener_pago(self, tipo: str) -> int:
        try:
            return self.pagos[tipo]
        except KeyError as error:
            raise ValueError(f"Código de apuesta desconocido: {tipo}") from error

    def obtener_color(self, numero: Numero) -> str:
        if numero not in self.ruleta.casillas:
            raise ValueError(f"Resultado no válido para ruleta {self.variante}: {numero}")
        return Casilla(numero).color

    def validar_apuesta(self, apuesta: Apuesta) -> None:
        seleccion = apuesta.seleccion or []
        if apuesta.tipo == "FF" and self.variante != "Europea":
            raise ValueError("FF solo está disponible en ruleta Europea")
        if apuesta.tipo == "BA" and self.variante != "Americana":
            raise ValueError("BA solo está disponible en ruleta Americana")
        if apuesta.tipo in {"SU", "SP", "ST", "CO", "LI"}:
            if "00" in seleccion and self.variante != "Americana":
                raise ValueError("00 solo está disponible en ruleta Americana")
            if any(token not in {str(casilla) for casilla in self.ruleta.casillas} for token in seleccion):
                raise ValueError("La selección no pertenece a la ruleta elegida")

    def acierta(self, apuesta: Apuesta, resultado: Union[int, str]) -> bool:
        self.validar_apuesta(apuesta)
        if resultado not in self.ruleta.casillas:
            raise ValueError(f"Resultado no válido para ruleta {self.variante}: {resultado}")
        numero = str(resultado)
        seleccion = apuesta.seleccion or []
        if apuesta.tipo in {"SU", "SP", "ST", "CO", "LI"}:
            return numero in seleccion
        if apuesta.tipo == "FF":
            return numero in {"0", "1", "2", "3"}
        if apuesta.tipo == "BA":
            return numero in {"0", "00", "1", "2", "3"}
        if apuesta.tipo == "DZ":
            inicio = {"1st": 1, "2nd": 13, "3rd": 25}[seleccion[0]]
            return inicio <= int(numero) <= inicio + 11 if numero.isdigit() else False
        if apuesta.tipo == "CL":
            columna = {"1st": 0, "2nd": 1, "3rd": 2}[seleccion[0]]
            return numero.isdigit() and int(numero) > 0 and (int(numero) - 1) % 3 == columna
        if not numero.isdigit() or int(numero) == 0:
            return False
        numero_entero = int(numero)
        return {"LO": 1 <= numero_entero <= 18, "HI": 19 <= numero_entero <= 36,
                "EV": numero_entero % 2 == 0, "OD": numero_entero % 2 == 1,
                "RE": self.obtener_color(resultado) == "Rojo",
                "BL": self.obtener_color(resultado) == "Negro"}[apuesta.tipo]

    def calcular_ganancia(self, apuesta: Apuesta, resultado: Union[int, str]) -> float:
        return apuesta.monto * self.obtener_pago(apuesta.tipo) if self.acierta(apuesta, resultado) else 0