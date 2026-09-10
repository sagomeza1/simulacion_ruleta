from pathlib import Path

import pandas as pd

from src.simulacion_ruleta.persistencia.exportador_csv import ExportadorCSV


def test_exportar_simulacion_crea_tablas_contractuales(tmp_path: Path):
    exportador = ExportadorCSV(
        tmp_path / 'simulaciones', tmp_path / 'registros.csv'
    )
    directorio = exportador.exportar_simulacion(
        apuestas=[{
            'NoApuesta': 1,
            'Apuesta': '10RE',
            'MontoInicial': 100,
            'CantidadApostada': 10,
            'Ganancia': 10,
            'MontoFinal': 100,
        }],
        numeros=[{'NoPartida': 1, 'Numero': 3, 'Color': 'Rojo'}],
        frecuencias={3: 1},
        variante='Americana',
        resumen={
            'total_apostado': 10,
            'total_ganado': 10,
            'balance_final': 100,
            'causa_fin': 'JuegosCompletados',
        },
        nombre_simulacion='20240101_0101',
    )

    assert directorio.name == '20240101_0101'
    assert list(pd.read_csv(directorio / 'apuestas.csv').columns) == [
        'NoApuesta', 'Apuesta', 'MontoInicial', 'CantidadApostada',
        'Ganancia', 'MontoFinal',
    ]
    assert list(pd.read_csv(directorio / 'numeros.csv').columns) == [
        'NoPartida', 'Numero', 'Color',
    ]
    stats = pd.read_csv(directorio / 'stats.csv', dtype={'Numero': str})
    assert list(stats.columns) == ['Numero', 'Color', 'Cantidad']
    assert len(stats) == 38
    assert stats.loc[stats['Numero'] == '00', 'Cantidad'].item() == 0
    assert stats.loc[stats['Numero'] == '3', 'Cantidad'].item() == 1

    contenido = (directorio / 'apuestas.csv').read_text(encoding='utf-8')
    assert ',' in contenido


def test_exportar_simulacion_resuelve_colision_y_anexa_registros(tmp_path: Path):
    exportador = ExportadorCSV(
        tmp_path / 'simulaciones', tmp_path / 'registros.csv'
    )
    resumen = {
        'total_apostado': 5,
        'total_ganado': 0,
        'balance_final': 95,
        'causa_fin': 'Bancarrota',
    }
    argumentos = {
        'apuestas': [],
        'numeros': [],
        'frecuencias': {},
        'variante': 'Europea',
        'resumen': resumen,
        'nombre_simulacion': '20240101_0101',
    }

    primera = exportador.exportar_simulacion(**argumentos)
    segunda = exportador.exportar_simulacion(**argumentos)

    assert primera.name == '20240101_0101'
    assert segunda.name == '20240101_0101_01'
    registros = pd.read_csv(tmp_path / 'registros.csv')
    assert list(registros.columns) == [
        'Simulacion', 'Modo', 'Ruleta', 'TotalApostado',
        'TotalGanado', 'BalanceFinal', 'CausaFin',
    ]
    assert len(registros) == 2