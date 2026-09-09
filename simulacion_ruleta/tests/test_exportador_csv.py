import pytest
import pandas as pd
from src.simulacion_ruleta.persistencia.exportador_csv import ExportadorCSV

def test_exportar_datos():
    # Datos de prueba
    datos = {
        'NoApuesta': [1, 2],
        'Apuesta': ['10RE', '5BA'],
        'MontoInicial': [100, 50],
        'CantidadApostada': [10, 5],
        'Ganancia': [0, 0],
        'MontoFinal': [90, 45]
    }
    
    # Crear un DataFrame de pandas
    df = pd.DataFrame(datos)
    
    # Ruta de prueba para exportar
    ruta_prueba = 'tests/simulaciones/test_exportacion.csv'
    
    # Instanciar el exportador y exportar los datos
    exportador = ExportadorCSV()
    exportador.exportar(df, ruta_prueba)
    
    # Leer el archivo exportado para verificar su contenido
    df_exportado = pd.read_csv(ruta_prueba)
    
    # Comprobar que los datos exportados son correctos
    pd.testing.assert_frame_equal(df, df_exportado)

    # Limpiar el archivo de prueba después de la verificación
    import os
    os.remove(ruta_prueba)