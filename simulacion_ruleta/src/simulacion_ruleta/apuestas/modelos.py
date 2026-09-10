from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Apuesta:
    """Una apuesta validada, independiente de cualquier entrada/salida."""

    monto: float
    tipo: str
    seleccion: Optional[List[str]] = None