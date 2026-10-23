"""Definición de la rueda de ruleta (Europea / Americana) y sus casillas."""
from __future__ import annotations

import random
from typing import List, Literal, Optional, Union

RouletteType = Literal["europea", "americana"]

RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
BLACK_NUMBERS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}


def color_of(pocket: Union[str, int]) -> str:
    """Devuelve el color ('Verde', 'Rojo', 'Negro') de una casilla."""
    pocket_str = str(pocket)
    if pocket_str in ("0", "00"):
        return "Verde"
    n = int(pocket_str)
    if n in RED_NUMBERS:
        return "Rojo"
    if n in BLACK_NUMBERS:
        return "Negro"
    raise ValueError(f"Número de casilla inválido: {pocket}")


class Wheel:
    """Representa una rueda de ruleta Europea (37 casillas) o Americana (38 casillas)."""

    def __init__(self, roulette_type: RouletteType) -> None:
        if roulette_type not in ("europea", "americana"):
            raise ValueError("Tipo de ruleta debe ser 'europea' o 'americana'")
        self.roulette_type: RouletteType = roulette_type
        pockets: List[str] = [str(n) for n in range(0, 37)]
        if roulette_type == "americana":
            pockets.append("00")
        self.pockets: List[str] = pockets

    def spin(self, rng: Optional[random.Random] = None) -> str:
        """Gira la ruleta y devuelve la casilla ganadora como texto ('0', '00', '1'..'36')."""
        chooser = rng or random
        return chooser.choice(self.pockets)

    def all_pockets_ordered(self) -> List[str]:
        """Lista ordenada de todas las casillas posibles, para reportes de frecuencia."""
        ordered = ["0"]
        if "00" in self.pockets:
            ordered.append("00")
        ordered.extend(str(n) for n in range(1, 37))
        return ordered
