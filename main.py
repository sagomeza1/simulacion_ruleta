"""CLI interactiva del simulador de ruleta (ASCII UI según docs/proyecto.md)."""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roulette.bets import InvalidBetError, parse_bet_line, total_amount
from roulette.board import print_board
from roulette.engine import RouletteEngine, SimulationResult, StopCause
from roulette.storage import persist_simulation
from roulette.wheel import color_of

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HEADER = "=" * 50


def print_header(subtitle: str = "") -> None:
    print(HEADER)
    print("           --- SIMULACIÓN DE RULETA ---")
    if subtitle:
        print(f"              {subtitle}")
    print(HEADER)
    print()


def ask(prompt: str) -> str:
    return input(prompt).strip()


def ask_roulette_type() -> str:
    while True:
        print("Tipo de ruleta:")
        print("    [1] Europea")
        print("    [2] Americana")
        choice = ask("Indicar opción: ")
        if choice in ("1", "2"):
            roulette_type = "europea" if choice == "1" else "americana"
            print()
            print_board(roulette_type)
            print()
            return roulette_type
        print("Opción inválida.\n")


def ask_int(prompt: str, min_value: int = 0) -> int:
    while True:
        raw = ask(prompt)
        try:
            value = int(raw)
            if value < min_value:
                raise ValueError
            return value
        except ValueError:
            print(f"Debe ingresar un entero >= {min_value}.\n")


def ask_bet_line(prompt: str, roulette_type: str) -> str:
    while True:
        raw = ask(prompt)
        try:
            bets = parse_bet_line(raw, roulette_type)
            if not bets:
                print("Debe ingresar al menos una apuesta válida.\n")
                continue
            return raw
        except InvalidBetError as exc:
            print(f"Apuesta inválida: {exc}\n")


def print_result_summary(result: SimulationResult, folder: str) -> None:
    print()
    print(HEADER)
    print("Resumen de la simulación")
    print(HEADER)
    print(f"  Modo             : {result.modo}")
    print(f"  Ruleta           : {result.ruleta}")
    print(f"  Monto inicial    : ${result.monto_inicial}")
    print(f"  Total apostado   : ${result.total_apostado}")
    print(f"  Total ganado     : ${result.total_ganado}")
    print(f"  Balance final    : ${result.balance_final}")
    print(f"  Causa de fin     : {result.causa_fin.value}")
    print(f"  Jugadas jugadas  : {len(result.rounds)}")
    print(f"  Carpeta de datos : {folder}")
    print()


def modo_sencillo() -> None:
    print_header("Modo Sencillo")
    roulette_type = ask_roulette_type()
    balance = ask_int("Monto inicial en el bolsillo: $", min_value=1)

    engine = RouletteEngine(roulette_type)
    result = SimulationResult(
        modo="Sencillo",
        ruleta=roulette_type.capitalize(),
        monto_inicial=balance,
        balance_final=balance,
    )

    round_no = 0
    while True:
        round_no += 1
        print(f"\n-- Ronda {round_no} | Saldo actual: ${balance} --")
        raw = ask(
            "Ingrese su apuesta (ej. 10SU[3], 5RE) o '0' para pasar, 'X' para salir: "
        )
        if raw.upper() == "X":
            result.causa_fin = StopCause.TERMINADO_POR_USUARIO
            break
        if raw == "0":
            print("Ronda pasada, no se registró apuesta.")
            round_no -= 1
            continue
        try:
            bets = parse_bet_line(raw, roulette_type)
        except InvalidBetError as exc:
            print(f"Apuesta inválida: {exc}")
            round_no -= 1
            continue
        stake = total_amount(bets)
        if stake > balance:
            print(f"Fondos insuficientes: necesita ${stake}, tiene ${balance}.")
            round_no -= 1
            continue

        balance = engine.play_single_round(raw, balance, result, round_no)
        last_spin = result.spins[-1]
        last_round = result.rounds[-1]
        print(
            f"Resultado: {last_spin.numero} ({last_spin.color}) | "
            f"Ganancia: ${last_round.ganancia} | Saldo: ${balance}"
        )

        if balance <= 0:
            print("\n¡Bancarrota! Se queda sin fondos.")
            result.causa_fin = StopCause.BANCARROTA
            break

    result.balance_final = balance
    folder = persist_simulation(result, BASE_DIR, roulette_type)
    print_result_summary(result, folder)


def modo_estatica() -> None:
    print_header("Simulación Estática")
    roulette_type = ask_roulette_type()
    monto_inicial = ask_int("Monto inicial: $", min_value=1)
    num_games = ask_int("Cantidad de partidas a simular: ", min_value=1)
    apuesta_fija = ask_bet_line(
        "Apuesta fija (ej. 10SU[3], 20RE): ", roulette_type
    )

    engine = RouletteEngine(roulette_type)
    result = engine.run_static(monto_inicial, apuesta_fija, num_games)
    folder = persist_simulation(result, BASE_DIR, roulette_type)
    print_result_summary(result, folder)


def modo_dinamica() -> None:
    print_header("Simulación Dinámica")
    roulette_type = ask_roulette_type()
    monto_inicial = ask_int("Monto inicial: $", min_value=1)
    num_games = ask_int("Cantidad de partidas a simular: ", min_value=1)
    pool_raw = ask(
        "Pool de apuestas elegibles, separadas por ' | ' "
        "(ej. 10RE | 10BL | 5SU[7] | 15DZ[1st]): "
    )
    pool_lines = [p.strip() for p in pool_raw.split("|") if p.strip()]
    valid_pool = []
    for line in pool_lines:
        try:
            parse_bet_line(line, roulette_type)
            valid_pool.append(line)
        except InvalidBetError as exc:
            print(f"Apuesta del pool ignorada por ser inválida ('{line}'): {exc}")
    if not valid_pool:
        print("No hay apuestas válidas en el pool. Cancelando.")
        return

    engine = RouletteEngine(roulette_type)
    result = engine.run_dynamic(monto_inicial, valid_pool, num_games)
    folder = persist_simulation(result, BASE_DIR, roulette_type)
    print_result_summary(result, folder)


def main() -> None:
    while True:
        print_header()
        print("Seleccione el tipo de juego:\n")
        print("    [A] Modo Sencillo")
        print("    [B] Simulación Estática")
        print("    [C] Simulación Dinámica")
        print("    [X] Salir\n")
        choice = ask("Indicar opción: ").upper()
        print()

        if choice == "A":
            modo_sencillo()
        elif choice == "B":
            modo_estatica()
        elif choice == "C":
            modo_dinamica()
        elif choice == "X":
            print("¡Hasta pronto!")
            break
        else:
            print("Opción inválida.\n")


if __name__ == "__main__":
    main()
