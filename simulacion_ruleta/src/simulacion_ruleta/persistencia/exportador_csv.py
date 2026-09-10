from datetime import datetime
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Union

import pandas as pd

from ..ruleta.modelos import Numero, Ruleta
from ..ruleta.reglas import ReglasRuleta

Ruta = Union[str, Path]

COLUMNAS_APUESTAS = [
    "NoApuesta",
    "Apuesta",
    "MontoInicial",
    "CantidadApostada",
    "Ganancia",
    "MontoFinal",
]
COLUMNAS_NUMEROS = ["NoPartida", "Numero", "Color"]
COLUMNAS_STATS = ["Numero", "Color", "Cantidad"]
COLUMNAS_REGISTROS = [
    "Simulacion",
    "Modo",
    "Ruleta",
    "TotalApostado",
    "TotalGanado",
    "BalanceFinal",
    "CausaFin",
]


class ExportadorCSV:
    """Escribe las tablas contractuales de una simulacion en CSV."""

    def __init__(
        self,
        directorio_base: Ruta = "simulaciones",
        ruta_registros: Optional[Ruta] = None,
    ) -> None:
        self.directorio_base = Path(directorio_base)
        self.ruta_registros = Path(ruta_registros) if ruta_registros else (
            self.directorio_base.parent / "registros.csv"
        )

    def crear_directorio_simulacion(
        self, nombre: Optional[str] = None
    ) -> Path:
        self.directorio_base.mkdir(parents=True, exist_ok=True)
        nombre_base = nombre or datetime.now().strftime("%Y%m%d_%H%M")
        directorio = self.directorio_base / nombre_base
        sufijo = 1
        while directorio.exists():
            directorio = self.directorio_base / f"{nombre_base}_{sufijo:02d}"
            sufijo += 1
        directorio.mkdir()
        return directorio

    @staticmethod
    def _escribir(data_frame: pd.DataFrame, ruta: Path) -> Path:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        data_frame.to_csv(ruta, sep=",", encoding="utf-8", index=False)
        return ruta

    def exportar(self, datos: object, ruta: Ruta) -> Path:
        """Mantiene la API simple para exportar un DataFrame arbitrario."""
        data_frame = datos if isinstance(datos, pd.DataFrame) else pd.DataFrame(datos)
        return self._escribir(data_frame, Path(ruta))

    def exportar_apuestas(
        self, datos: List[Mapping[str, object]], directorio: Ruta
    ) -> Path:
        data_frame = pd.DataFrame(datos, columns=COLUMNAS_APUESTAS)
        return self._escribir(data_frame, Path(directorio) / "apuestas.csv")

    def exportar_numeros(
        self, datos: List[Mapping[str, object]], directorio: Ruta
    ) -> Path:
        data_frame = pd.DataFrame(datos, columns=COLUMNAS_NUMEROS)
        return self._escribir(data_frame, Path(directorio) / "numeros.csv")

    def exportar_stats(
        self,
        frecuencias: Mapping[Numero, int],
        variante: str,
        directorio: Ruta,
    ) -> Path:
        ruleta = Ruleta(variante)
        reglas = ReglasRuleta(variante)
        filas = [
            {
                "Numero": casilla,
                "Color": reglas.obtener_color(casilla),
                "Cantidad": frecuencias.get(casilla, 0),
            }
            for casilla in ruleta.casillas
        ]
        data_frame = pd.DataFrame(filas, columns=COLUMNAS_STATS)
        return self._escribir(data_frame, Path(directorio) / "stats.csv")

    def exportar_registros(
        self, datos: List[Mapping[str, object]], ruta: Optional[Ruta] = None
    ) -> Path:
        destino = Path(ruta) if ruta else self.ruta_registros
        data_frame = pd.DataFrame(datos, columns=COLUMNAS_REGISTROS)
        destino.parent.mkdir(parents=True, exist_ok=True)
        necesita_cabecera = not destino.exists() or destino.stat().st_size == 0
        data_frame.to_csv(
            destino,
            sep=",",
            encoding="utf-8",
            index=False,
            mode="a",
            header=necesita_cabecera,
        )
        return destino

    def exportar_simulacion(
        self,
        apuestas: List[Mapping[str, object]],
        numeros: List[Mapping[str, object]],
        frecuencias: Mapping[Numero, int],
        variante: str,
        resumen: Mapping[str, object],
        modo: str = "Estatica",
        nombre_simulacion: Optional[str] = None,
    ) -> Path:
        directorio = self.crear_directorio_simulacion(nombre_simulacion)
        self.exportar_apuestas(apuestas, directorio)
        self.exportar_numeros(numeros, directorio)
        self.exportar_stats(frecuencias, variante, directorio)
        self.exportar_registros(
            [
                {
                    "Simulacion": directorio.name,
                    "Modo": modo,
                    "Ruleta": variante,
                    "TotalApostado": resumen["total_apostado"],
                    "TotalGanado": resumen["total_ganado"],
                    "BalanceFinal": resumen["balance_final"],
                    "CausaFin": resumen["causa_fin"],
                }
            ]
        )
        return directorio
