"""Parser y catálogo de apuestas de ruleta.

Codificación: <Monto><Abreviatura>[<Selección>]
Regex de validación: ^\\d+[A-Z]{2}(\\[[\\w,-]+\\])?$
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Set

from .wheel import RouletteType, color_of

BET_REGEX = re.compile(r"^(\d+)([A-Z]{2})(?:\[([\w,-]+)\])?$")

DOZEN_RANGES = {"1st": range(1, 13), "2nd": range(13, 25), "3rd": range(25, 37)}
COLUMN_SETS = {
    "1st": {1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34},
    "2nd": {2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35},
    "3rd": {3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36},
}

# Abreviatura -> (número de casillas cubiertas, pago "a 1")
PAYOUTS = {
    "SU": (1, 35),
    "SP": (2, 17),
    "ST": (3, 11),
    "CO": (4, 8),
    "FF": (4, 8),
    "BA": (5, 6),
    "LI": (6, 5),
    "DZ": (12, 2),
    "CL": (12, 2),
    "LO": (18, 1),
    "HI": (18, 1),
    "EV": (18, 1),
    "OD": (18, 1),
    "RE": (18, 1),
    "BL": (18, 1),
}


class InvalidBetError(ValueError):
    """Se lanza cuando una cadena de apuesta no cumple el formato o reglas del juego."""


@dataclass(frozen=True)
class Bet:
    """Representa una apuesta individual ya parseada y validada."""

    raw: str
    amount: int
    code: str
    selection: str | None
    covered: Set[str]

    def payout_ratio(self) -> int:
        return PAYOUTS[self.code][1]


def _parse_selection(code: str, selection: str | None) -> List[str]:
    if selection is None:
        return []
    return selection.split(",")


def _covered_pockets(code: str, selection: str | None, roulette_type: RouletteType) -> Set[str]:
    """Calcula el conjunto de casillas (como strings) que cubre una apuesta dada."""
    parts = _parse_selection(code, selection)

    if code == "SU":
        if len(parts) != 1:
            raise InvalidBetError(f"Pleno (SU) requiere exactamente un número: {selection}")
        pocket = parts[0]
        _validate_pocket(pocket, roulette_type)
        return {pocket}

    if code in ("SP", "ST", "CO"):
        if code == "SP" and len(parts) != 2:
            raise InvalidBetError(f"Split (SP) requiere 2 números: {selection}")
        if code == "ST" and len(parts) != 3:
            raise InvalidBetError(f"Street (ST) requiere 3 números: {selection}")
        if code == "CO" and len(parts) != 4:
            raise InvalidBetError(f"Corner (CO) requiere 4 números: {selection}")
        for p in parts:
            _validate_pocket(p, roulette_type, allow_zero_variants=True)
        return set(parts)

    if code == "LI":
        if len(parts) != 1 or "-" not in parts[0]:
            raise InvalidBetError(f"Línea (LI) requiere rango 'a-b': {selection}")
        lo, hi = parts[0].split("-")
        nums = [str(n) for n in range(int(lo), int(hi) + 1)]
        if len(nums) != 6:
            raise InvalidBetError(f"Línea (LI) debe cubrir 6 números: {selection}")
        return set(nums)

    if code == "FF":
        if roulette_type != "europea":
            raise InvalidBetError("Cuatro Primeros (FF) solo aplica a ruleta Europea")
        return {"0", "1", "2", "3"}

    if code == "BA":
        if roulette_type != "americana":
            raise InvalidBetError("Línea Superior (BA) solo aplica a ruleta Americana")
        return {"0", "00", "1", "2", "3"}

    if code == "DZ":
        if len(parts) != 1 or parts[0] not in DOZEN_RANGES:
            raise InvalidBetError(f"Docena (DZ) requiere selección 1st/2nd/3rd: {selection}")
        return {str(n) for n in DOZEN_RANGES[parts[0]]}

    if code == "CL":
        if len(parts) != 1 or parts[0] not in COLUMN_SETS:
            raise InvalidBetError(f"Columna (CL) requiere selección 1st/2nd/3rd: {selection}")
        return {str(n) for n in COLUMN_SETS[parts[0]]}

    if code == "LO":
        return {str(n) for n in range(1, 19)}

    if code == "HI":
        return {str(n) for n in range(19, 37)}

    if code == "EV":
        return {str(n) for n in range(1, 37) if n % 2 == 0}

    if code == "OD":
        return {str(n) for n in range(1, 37) if n % 2 == 1}

    if code == "RE":
        return {str(n) for n in range(1, 37) if color_of(n) == "Rojo"}

    if code == "BL":
        return {str(n) for n in range(1, 37) if color_of(n) == "Negro"}

    raise InvalidBetError(f"Abreviatura de apuesta desconocida: {code}")


def _validate_pocket(pocket: str, roulette_type: RouletteType, allow_zero_variants: bool = True) -> None:
    if pocket == "00":
        if roulette_type != "americana":
            raise InvalidBetError("La casilla '00' solo existe en ruleta Americana")
        return
    if pocket == "0":
        return
    try:
        n = int(pocket)
    except ValueError as exc:
        raise InvalidBetError(f"Número de casilla inválido: {pocket}") from exc
    if not (1 <= n <= 36):
        raise InvalidBetError(f"Número de casilla fuera de rango (0-36): {pocket}")


def parse_bet(raw: str, roulette_type: RouletteType) -> Bet:
    """Parsea y valida una única apuesta codificada (ej. '10SU[3]')."""
    raw = raw.strip()
    match = BET_REGEX.match(raw)
    if not match:
        raise InvalidBetError(
            f"Formato de apuesta inválido: '{raw}' (esperado <Monto><Abreviatura>[<Selección>])"
        )
    amount_str, code, selection = match.groups()
    amount = int(amount_str)
    if amount <= 0:
        raise InvalidBetError(f"El monto apostado debe ser mayor a 0: {raw}")
    if code not in PAYOUTS:
        raise InvalidBetError(f"Abreviatura de apuesta desconocida: {code}")

    covered = _covered_pockets(code, selection, roulette_type)
    return Bet(raw=raw, amount=amount, code=code, selection=selection, covered=covered)


def parse_bet_line(line: str, roulette_type: RouletteType) -> List[Bet]:
    """Parsea una línea con una o varias apuestas separadas por comas.

    Nota: las apuestas con selección de múltiples números (SP, ST, CO, LI) también
    usan comas dentro de los corchetes, por lo que se agrupan los segmentos hasta
    cerrar el corchete antes de separar por apuesta.
    """
    line = line.strip()
    if not line:
        return []

    tokens: List[str] = []
    depth = 0
    current = ""
    for ch in line:
        if ch == "[":
            depth += 1
            current += ch
        elif ch == "]":
            depth -= 1
            current += ch
        elif ch == "," and depth == 0:
            tokens.append(current.strip())
            current = ""
        else:
            current += ch
    if current.strip():
        tokens.append(current.strip())

    return [parse_bet(tok, roulette_type) for tok in tokens if tok]


def total_amount(bets: List[Bet]) -> int:
    return sum(b.amount for b in bets)


def resolve_bet(bet: Bet, winning_pocket: str) -> int:
    """Devuelve la ganancia bruta (incluye el monto original apostado si gana, 0 si pierde).

    Siguiendo la tabla de 'MontoFinal = MontoInicial - CantidadApostada + Ganancia',
    la 'Ganancia' registrada aquí es el monto bruto devuelto al jugador cuando acierta
    (apuesta original + premio neto), y 0 si no acierta.
    """
    if winning_pocket not in bet.covered:
        return 0
    ratio = bet.payout_ratio()
    return bet.amount + bet.amount * ratio


def resolve_bets(bets: List[Bet], winning_pocket: str) -> int:
    """Ganancia bruta total de un conjunto de apuestas de una misma jugada."""
    return sum(resolve_bet(b, winning_pocket) for b in bets)
