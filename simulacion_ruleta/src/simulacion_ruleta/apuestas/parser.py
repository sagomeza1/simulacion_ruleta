# parser.py

import re
from typing import List, Tuple, Optional

class ApuestaParser:
    def __init__(self):
        # Expresión regular para validar la sintaxis de las apuestas
        self.regex = r'^\d+[A-Z]{2}(\[[\w,-]+\])?$'

    def validar_apuesta(self, apuesta: str) -> bool:
        """Valida la sintaxis de una apuesta."""
        return bool(re.match(self.regex, apuesta))

    def procesar_apuestas(self, apuestas: str) -> List[Tuple[str, int]]:
        """Procesa una cadena de apuestas y devuelve una lista de tuplas con el monto y la apuesta."""
        lista_apuestas = []
        for apuesta in apuestas.split(','):
            apuesta = apuesta.strip()
            if self.validar_apuesta(apuesta):
                monto = int(apuesta[:-2])  # Extrae el monto
                tipo_apuesta = apuesta[-2:]  # Extrae el tipo de apuesta
                lista_apuestas.append((tipo_apuesta, monto))
            else:
                raise ValueError(f"Apuesta inválida: {apuesta}")
        return lista_apuestas