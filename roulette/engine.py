"""Motor de simulación: ejecuta rondas de ruleta y lleva el registro de resultados."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from .bets import Bet, parse_bet_line, resolve_bets, total_amount
from .wheel import Wheel, color_of


class StopCause(str, Enum):
    BANCARROTA = "Bancarrota"
    JUEGOS_COMPLETADOS = "JuegosCompletados"
    TERMINADO_POR_USUARIO = "TerminadoPorUsuario"


@dataclass
class RoundRecord:
    """Una fila del historial de apuestas (apuestas.csv)."""

    no_apuesta: int
    apuesta: str
    monto_inicial: int
    cantidad_apostada: int
    ganancia: int
    monto_final: int


@dataclass
class SpinRecord:
    """Una fila del historial de tiradas (numeros.csv)."""

    no_partida: int
    numero: str
    color: str


@dataclass
class SimulationResult:
    """Resultado consolidado de una simulación completa."""

    modo: str
    ruleta: str
    monto_inicial: int
    balance_final: int
    total_apostado: int = 0
    total_ganado: int = 0
    causa_fin: StopCause = StopCause.JUEGOS_COMPLETADOS
    rounds: List[RoundRecord] = field(default_factory=list)
    spins: List[SpinRecord] = field(default_factory=list)


class RouletteEngine:
    """Ejecuta simulaciones estáticas y dinámicas sobre una rueda configurada."""

    def __init__(self, roulette_type: str, rng: Optional[random.Random] = None) -> None:
        self.wheel = Wheel(roulette_type)  # type: ignore[arg-type]
        self.roulette_type = roulette_type
        self.rng = rng or random.Random()

    def _play_round(
        self,
        round_no: int,
        bet_line: str,
        balance: int,
        result: SimulationResult,
    ) -> int:
        """Ejecuta una jugada: valida fondos, gira la rueda, resuelve apuestas.

        Devuelve el nuevo balance. Puede lanzar InvalidBetError si la línea no es válida.
        """
        bets: List[Bet] = parse_bet_line(bet_line, self.roulette_type)  # type: ignore[arg-type]
        stake = total_amount(bets)

        winning_pocket = self.wheel.spin(self.rng)
        result.spins.append(
            SpinRecord(no_partida=round_no, numero=winning_pocket, color=color_of(winning_pocket))
        )

        ganancia = resolve_bets(bets, winning_pocket) if stake > 0 else 0
        monto_final = balance - stake + ganancia

        result.rounds.append(
            RoundRecord(
                no_apuesta=round_no,
                apuesta=bet_line if bet_line else "(sin apuesta)",
                monto_inicial=balance,
                cantidad_apostada=stake,
                ganancia=ganancia,
                monto_final=monto_final,
            )
        )
        result.total_apostado += stake
        result.total_ganado += ganancia
        return monto_final

    def run_static(self, initial_amount: int, fixed_bet_line: str, num_games: int) -> SimulationResult:
        """Modo Simulación Estática: misma apuesta fija repetida N veces."""
        result = SimulationResult(
            modo="Estatica",
            ruleta=self.roulette_type.capitalize(),
            monto_inicial=initial_amount,
            balance_final=initial_amount,
        )
        balance = initial_amount
        stake = total_amount(parse_bet_line(fixed_bet_line, self.roulette_type))  # type: ignore[arg-type]

        for i in range(1, num_games + 1):
            if balance <= 0 or balance < stake:
                result.causa_fin = StopCause.BANCARROTA
                break
            balance = self._play_round(i, fixed_bet_line, balance, result)
        else:
            result.causa_fin = StopCause.JUEGOS_COMPLETADOS

        result.balance_final = balance
        return result

    def run_dynamic(
        self,
        initial_amount: int,
        bet_pool_lines: List[str],
        num_games: int,
    ) -> SimulationResult:
        """Modo Simulación Dinámica: en cada ronda se elige al azar una apuesta del pool."""
        result = SimulationResult(
            modo="Dinamica",
            ruleta=self.roulette_type.capitalize(),
            monto_inicial=initial_amount,
            balance_final=initial_amount,
        )
        balance = initial_amount

        for i in range(1, num_games + 1):
            chosen_line = self.rng.choice(bet_pool_lines)
            stake = total_amount(parse_bet_line(chosen_line, self.roulette_type))  # type: ignore[arg-type]
            if balance <= 0 or balance < stake:
                result.causa_fin = StopCause.BANCARROTA
                break
            balance = self._play_round(i, chosen_line, balance, result)
        else:
            result.causa_fin = StopCause.JUEGOS_COMPLETADOS

        result.balance_final = balance
        return result

    def run_mixed(
        self,
        initial_amount: int,
        fixed_bet_line: str,
        bet_pool_lines: List[str],
        num_games: int,
    ) -> SimulationResult:
        """Modo Simulación Mixta: combina una apuesta fija (Estática) con una apuesta
        elegida al azar del pool (Dinámica) en cada ronda, jugadas simultáneamente.

        La 'Apuesta fija' se repite siempre; además, en cada ronda se suma al tapete
        una apuesta tomada al azar del pool dinámico. El monto apostado y la ganancia
        de la ronda se calculan sobre la unión de ambas.
        """
        result = SimulationResult(
            modo="Mixta",
            ruleta=self.roulette_type.capitalize(),
            monto_inicial=initial_amount,
            balance_final=initial_amount,
        )
        balance = initial_amount

        for i in range(1, num_games + 1):
            dynamic_line = self.rng.choice(bet_pool_lines)
            combined_line = f"{fixed_bet_line}, {dynamic_line}" if fixed_bet_line else dynamic_line
            stake = total_amount(parse_bet_line(combined_line, self.roulette_type))  # type: ignore[arg-type]
            if balance <= 0 or balance < stake:
                result.causa_fin = StopCause.BANCARROTA
                break
            balance = self._play_round(i, combined_line, balance, result)
        else:
            result.causa_fin = StopCause.JUEGOS_COMPLETADOS

        result.balance_final = balance
        return result

    def play_single_round(self, bet_line: str, balance: int, result: SimulationResult, round_no: int) -> int:
        """Ejecuta una única ronda interactiva (usada por el Modo Sencillo) y devuelve el balance."""
        return self._play_round(round_no, bet_line, balance, result)
