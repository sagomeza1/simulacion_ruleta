import os
import random
from typing import Callable, Dict, List, Optional, Union

from ..apuestas.modelos import Apuesta
from ..apuestas.parser import parse_apuesta
from ..persistencia.exportador_csv import ExportadorCSV
from ..ruleta.modelos import Numero, Ruleta
from ..ruleta.reglas import ReglasRuleta
from ..ruleta.resultados import Resultados

GeneradorResultado = Callable[[Ruleta], Numero]
ApuestaEntrada = Union[str, Apuesta, List[Apuesta]]


class Simulador:
    """Ejecuta rondas y simulaciones estaticas sin ocuparse de la persistencia."""

    def __init__(self, generador_resultados: Optional[GeneradorResultado] = None) -> None:
        self.balance: float = 0
        self.ruleta: Optional[Ruleta] = None
        self.reglas: Optional[ReglasRuleta] = None
        self.apuestas: List[Apuesta] = []
        self.cantidad_partidas: int = 0
        self.generador_resultados: GeneradorResultado = (
            generador_resultados or (lambda ruleta: random.choice(ruleta.casillas))
        )
        self.resultados = Resultados()
        self.historial_apuestas: List[Dict[str, object]] = []
        self.historial_tiradas: List[Dict[str, object]] = []
        self.frecuencias: Dict[Numero, int] = {}
        self.causa_fin: Optional[str] = None
        self.total_apostado: float = 0
        self.total_ganado: float = 0

    def configurar_simulacion(
        self,
        variante: str,
        saldo_inicial: float,
        apuesta_fija: ApuestaEntrada,
        cantidad_partidas: int,
        generador_resultados: Optional[GeneradorResultado] = None,
    ) -> None:
        if saldo_inicial < 0:
            raise ValueError("El monto inicial no puede ser negativo")
        if cantidad_partidas < 0:
            raise ValueError("La cantidad de partidas no puede ser negativa")

        ruleta = Ruleta(variante)
        reglas = ReglasRuleta(variante)
        apuestas = self._normalizar_apuestas(apuesta_fija)
        for apuesta in apuestas:
            reglas.validar_apuesta(apuesta)

        self.ruleta = ruleta
        self.reglas = reglas
        self.balance = saldo_inicial
        self.apuestas = apuestas
        self.cantidad_partidas = cantidad_partidas
        self.generador_resultados = generador_resultados or (
            lambda ruleta: random.choice(ruleta.casillas)
        )
        self.resultados = Resultados()
        self.historial_apuestas = []
        self.historial_tiradas = []
        self.frecuencias = {casilla: 0 for casilla in ruleta.casillas}
        self.causa_fin = None
        self.total_apostado = 0
        self.total_ganado = 0

    def configurar_juego(
        self, monto_inicial: float, variante: str, monto_apuesta: float
    ) -> None:
        """Conserva la interfaz anterior para ejecutar una ronda individual."""
        if monto_apuesta <= 0:
            raise ValueError("El monto de la apuesta debe ser positivo")
        self.configurar_simulacion(
            variante,
            monto_inicial,
            Apuesta(monto_apuesta, "SU", ["0"]),
            1,
        )

    @staticmethod
    def _normalizar_apuestas(apuesta_fija: ApuestaEntrada) -> List[Apuesta]:
        if isinstance(apuesta_fija, str):
            resultado = parse_apuesta(apuesta_fija)
            return resultado if isinstance(resultado, list) else [resultado]
        if isinstance(apuesta_fija, Apuesta):
            return [apuesta_fija]
        if isinstance(apuesta_fija, list) and apuesta_fija and all(
            isinstance(apuesta, Apuesta) for apuesta in apuesta_fija
        ):
            return list(apuesta_fija)
        raise ValueError("La apuesta fija debe ser una apuesta valida o una lista no vacia")

    def _verificar_configuracion(self) -> None:
        if self.ruleta is None or self.reglas is None or not self.apuestas:
            raise ValueError("La simulacion debe configurarse antes de ejecutar una ronda")

    def _cantidad_apostada(self) -> float:
        return sum(apuesta.monto for apuesta in self.apuestas)

    def _representar_apuestas(self) -> str:
        representaciones = []
        for apuesta in self.apuestas:
            seleccion = (
                f"[{','.join(apuesta.seleccion)}]"
                if apuesta.seleccion is not None
                else ""
            )
            representaciones.append(f"{apuesta.monto:g}{apuesta.tipo}{seleccion}")
        return ", ".join(representaciones)

    def ejecutar_ronda(self) -> Dict[str, object]:
        self._verificar_configuracion()
        assert self.ruleta is not None
        assert self.reglas is not None

        cantidad_apostada = self._cantidad_apostada()
        if self.balance < cantidad_apostada:
            self.causa_fin = "Bancarrota"
            return {
                "numero": None,
                "color": None,
                "cantidad_apostada": 0,
                "ganancia": 0,
                "balance": self.balance,
                "causa_fin": self.causa_fin,
            }

        monto_inicial = self.balance
        numero = self.generador_resultados(self.ruleta)
        color = self.reglas.obtener_color(numero)
        ganancia = sum(
            self.reglas.calcular_ganancia(apuesta, numero)
            for apuesta in self.apuestas
        )
        self.balance = monto_inicial - cantidad_apostada + ganancia
        self.total_apostado += cantidad_apostada
        self.total_ganado += ganancia

        numero_partida = len(self.historial_tiradas) + 1
        self.historial_apuestas.append(
            {
                "NoApuesta": numero_partida,
                "Apuesta": self._representar_apuestas(),
                "MontoInicial": monto_inicial,
                "CantidadApostada": cantidad_apostada,
                "Ganancia": ganancia,
                "MontoFinal": self.balance,
            }
        )
        self.historial_tiradas.append(
            {
                "NoPartida": numero_partida,
                "Numero": numero,
                "Color": color,
            }
        )
        self.frecuencias[numero] += 1
        self.resultados.agregar_resultado(numero, color)

        if self.balance < cantidad_apostada:
            self.causa_fin = "Bancarrota"

        return {
            "numero": numero,
            "color": color,
            "cantidad_apostada": cantidad_apostada,
            "ganancia": ganancia,
            "balance": self.balance,
            "causa_fin": self.causa_fin,
        }

    def ejecutar_partida(self) -> Dict[str, object]:
        """Alias de compatibilidad para ejecutar una unica ronda."""
        return self.ejecutar_ronda()

    def ejecutar_simulacion(
        self,
        exportador: Optional[ExportadorCSV] = None,
        modo: str = "Estatica",
        nombre_simulacion: Optional[str] = None,
    ) -> Dict[str, object]:
        self._verificar_configuracion()
        while len(self.historial_tiradas) < self.cantidad_partidas:
            if self.causa_fin == "Bancarrota":
                break
            self.ejecutar_ronda()

        if self.causa_fin is None:
            self.causa_fin = "JuegosCompletados"
        resumen: Dict[str, object] = {
            "partidas": len(self.historial_tiradas),
            "causa_fin": self.causa_fin,
            "total_apostado": self.total_apostado,
            "total_ganado": self.total_ganado,
            "balance_final": self.balance,
        }
        if exportador is not None:
            resumen["directorio"] = exportador.exportar_simulacion(
                self.historial_apuestas,
                self.historial_tiradas,
                self.frecuencias,
                self.ruleta.variante if self.ruleta else "",
                resumen,
                modo=modo,
                nombre_simulacion=nombre_simulacion,
            )
        return resumen

    def exportar_datos(self) -> None:
        """Prepara la ruta de salida; la exportacion CSV pertenece a Fase 3."""
        if not os.path.exists("simulaciones"):
            os.makedirs("simulaciones")


GestorSimulacion = Simulador
