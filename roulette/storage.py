"""Persistencia: generación de archivos CSV (registros.csv y los internos por simulación)."""
from __future__ import annotations

import os
from datetime import datetime
from typing import List

import pandas as pd

from .engine import SimulationResult, StopCause
from .wheel import Wheel


def new_simulation_folder(base_dir: str) -> str:
    """Crea (si no existe) y devuelve la carpeta /simulaciones/YYYYMMDD_HHMM/."""
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    folder = os.path.join(base_dir, "simulaciones", stamp)
    os.makedirs(folder, exist_ok=True)
    return folder


def save_apuestas_csv(result: SimulationResult, folder: str) -> str:
    path = os.path.join(folder, "apuestas.csv")
    rows = [
        {
            "NoApuesta": r.no_apuesta,
            "Apuesta": r.apuesta,
            "MontoInicial": r.monto_inicial,
            "CantidadApostada": r.cantidad_apostada,
            "Ganancia": r.ganancia,
            "MontoFinal": r.monto_final,
        }
        for r in result.rounds
    ]
    df = pd.DataFrame(rows, columns=[
        "NoApuesta", "Apuesta", "MontoInicial", "CantidadApostada", "Ganancia", "MontoFinal",
    ])
    df.to_csv(path, index=False, sep=",", encoding="utf-8")
    return path


def save_numeros_csv(result: SimulationResult, folder: str) -> str:
    path = os.path.join(folder, "numeros.csv")
    rows = [
        {"NoPartida": s.no_partida, "Numero": s.numero, "Color": s.color}
        for s in result.spins
    ]
    df = pd.DataFrame(rows, columns=["NoPartida", "Numero", "Color"])
    df.to_csv(path, index=False, sep=",", encoding="utf-8")
    return path


def save_stats_csv(result: SimulationResult, folder: str, roulette_type: str) -> str:
    wheel = Wheel(roulette_type)  # type: ignore[arg-type]
    counts = {pocket: 0 for pocket in wheel.all_pockets_ordered()}
    for s in result.spins:
        counts[s.numero] = counts.get(s.numero, 0) + 1

    from .wheel import color_of

    rows = [
        {"Numero": pocket, "Color": color_of(pocket), "Cantidad": count}
        for pocket, count in counts.items()
    ]
    path = os.path.join(folder, "stats.csv")
    df = pd.DataFrame(rows, columns=["Numero", "Color", "Cantidad"])
    df.to_csv(path, index=False, sep=",", encoding="utf-8")
    return path


def append_registro_global(result: SimulationResult, folder: str, base_dir: str) -> str:
    """Anexa el resumen consolidado de la simulación a registros.csv (en la raíz)."""
    path = os.path.join(base_dir, "registros.csv")
    sim_name = os.path.basename(folder)
    row = {
        "Simulacion": sim_name,
        "Modo": result.modo,
        "Ruleta": result.ruleta,
        "TotalApostado": result.total_apostado,
        "TotalGanado": result.total_ganado,
        "BalanceFinal": result.balance_final,
        "CausaFin": result.causa_fin.value if isinstance(result.causa_fin, StopCause) else result.causa_fin,
    }
    df = pd.DataFrame([row], columns=[
        "Simulacion", "Modo", "Ruleta", "TotalApostado", "TotalGanado", "BalanceFinal", "CausaFin",
    ])
    write_header = not os.path.exists(path)
    df.to_csv(path, index=False, sep=",", encoding="utf-8", mode="a", header=write_header)
    return path


def persist_simulation(result: SimulationResult, base_dir: str, roulette_type: str) -> str:
    """Genera la carpeta de simulación completa + anexa el registro global. Devuelve la carpeta."""
    folder = new_simulation_folder(base_dir)
    save_apuestas_csv(result, folder)
    save_numeros_csv(result, folder)
    save_stats_csv(result, folder, roulette_type)
    append_registro_global(result, folder, base_dir)
    return folder
