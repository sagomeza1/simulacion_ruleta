from typing import List
import pandas as pd

class ExportadorCSV:
    def __init__(self, directorio: str):
        self.directorio = directorio

    def exportar_apuestas(self, datos: List[dict], nombre_archivo: str = "apuestas.csv"):
        df = pd.DataFrame(datos)
        df.to_csv(f"{self.directorio}/{nombre_archivo}", index=False, encoding='utf-8')

    def exportar_numeros(self, datos: List[dict], nombre_archivo: str = "numeros.csv"):
        df = pd.DataFrame(datos)
        df.to_csv(f"{self.directorio}/{nombre_archivo}", index=False, encoding='utf-8')

    def exportar_stats(self, datos: List[dict], nombre_archivo: str = "stats.csv"):
        df = pd.DataFrame(datos)
        df.to_csv(f"{self.directorio}/{nombre_archivo}", index=False, encoding='utf-8')

    def exportar_registros(self, datos: List[dict], nombre_archivo: str = "registros.csv"):
        df = pd.DataFrame(datos)
        df.to_csv(nombre_archivo, mode='a', index=False, header=False, encoding='utf-8')