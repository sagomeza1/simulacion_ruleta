from typing import Optional

from .gestor import Simulador


class ModoSencillo:
    def __init__(self, gestor: Optional[Simulador] = None) -> None:
        self.gestor = gestor or Simulador()

    def jugar(self):
        return self.gestor.ejecutar_ronda()


class ModoSimulacionEstatica:
    def __init__(self, gestor: Optional[Simulador] = None) -> None:
        self.gestor = gestor or Simulador()

    def jugar(self):
        return self.gestor.ejecutar_simulacion()


class ModoSimulacionDinamica:
    def __init__(self, gestor: Optional[Simulador] = None) -> None:
        self.gestor = gestor or Simulador()

    def jugar(self):
        return self.gestor.ejecutar_ronda()


def seleccionar_modo(modo: str, gestor: Optional[Simulador] = None):
    modos = {
        "sencillo": ModoSencillo,
        "estatica": ModoSimulacionEstatica,
        "dinamica": ModoSimulacionDinamica,
    }
    try:
        return modos[modo.strip().lower()](gestor)
    except (AttributeError, KeyError) as error:
        raise ValueError("Modo de juego no válido") from error
