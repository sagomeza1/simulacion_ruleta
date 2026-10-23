"""Renderizado del tablero de apuestas (ASCII) para apoyar la selección de apuestas,
en especial identificar los 4 números válidos de una apuesta de Cuadro (Corner, 'CO').
"""
from __future__ import annotations

from typing import List

from .wheel import RouletteType, color_of

# El tapete real se organiza en 3 columnas x 12 filas (1..36), con el 0 (y 00 en
# Americana) a la izquierda, fuera de la cuadrícula principal.
COLUMNS = 3
ROWS = 12


def _cell(n: int, width: int = 4) -> str:
    mark = "R" if color_of(n) == "Rojo" else "N"
    return f"{n:>2}{mark}".center(width)


def render_board(roulette_type: RouletteType) -> str:
    """Devuelve el tablero como texto, con numeración y color (R/N) por casilla."""
    lines: List[str] = []

    if roulette_type == "americana":
        lines.append("   ┌──────┬──────┐")
        lines.append("   │  0 V │ 00 V │")
        lines.append("   ├──────┴──────┤")
    else:
        lines.append("   ┌─────────────┐")
        lines.append("   │     0 V     │")
        lines.append("   ├──────┬──────┤" if False else "   ├─────────────┤")

    sep = "   ├────┬────┬────┤"
    top = "   ┌────┬────┬────┐"
    bot = "   └────┴────┴────┘"

    lines.append(top)
    for row in range(ROWS, 0, -1):
        start = (row - 1) * COLUMNS + 1
        nums = [start, start + 1, start + 2]
        cells = [_cell(n) for n in nums]
        lines.append(f"   │{cells[0]}│{cells[1]}│{cells[2]}│")
        if row > 1:
            lines.append(sep)
    lines.append(bot)

    lines.append("")
    lines.append("   (V=Verde, R=Rojo, N=Negro)")
    lines.append("")
    lines.append("   Guía rápida para apuesta de Cuadro (CO, 4 números en cuadrado):")
    lines.append("   Toma 2 números contiguos de una fila y los 2 de la fila de abajo.")
    lines.append("   Ej. válidos: [1,2,4,5]  [2,3,5,6]  [4,5,7,8]  [8,9,11,12] ...")
    lines.append("   Ej. inválido: [1,2,3,4] (no forman un cuadrado 2x2 en el tapete)")
    if roulette_type == "europea":
        lines.append("   Caso especial europeo: 'Cuatro Primeros' (FF) cubre 0,1,2,3 (no usa CO).")
    else:
        lines.append("   Caso especial americano: 'Línea Superior' (BA) cubre 0,00,1,2,3 (no usa CO).")

    return "\n".join(lines)


def print_board(roulette_type: RouletteType) -> None:
    print(render_board(roulette_type))
