import os
import tempfile
import unittest
from pathlib import Path
from src.simulacion_ruleta.simulacion.gestor import Simulador
from src.simulacion_ruleta.simulacion.modos import (
    ModoSimulacionEstatica,
    seleccionar_modo,
)
from src.simulacion_ruleta.persistencia.exportador_csv import ExportadorCSV

class TestSimulacion(unittest.TestCase):
    
    def setUp(self):
        self.simulador = Simulador()

    def test_inicializacion(self):
        self.assertIsNotNone(self.simulador)
        self.assertEqual(self.simulador.balance, 0)

    def test_ejecucion_partida(self):
        self.simulador.configurar_juego(100, 'Europea', 10)
        resultado = self.simulador.ejecutar_partida()
        self.assertIn(resultado['numero'], range(37))  # Verifica que el número esté en el rango de la ruleta europea
        self.assertIsInstance(resultado['ganancia'], (int, float))

    def test_bancarrota(self):
        self.simulador.configurar_juego(100, 'Americana', 150)  # Apuesta mayor que el balance
        resultado = self.simulador.ejecutar_partida()
        self.assertEqual(resultado['ganancia'], 0)  # No debería haber ganancia si no se puede apostar

    def test_exportar_datos(self):
        self.simulador.configurar_juego(100, 'Europea', 10)
        self.simulador.ejecutar_partida()
        self.simulador.exportar_datos()
        self.assertTrue(os.path.exists('simulaciones/'))  # Verifica que el directorio de simulaciones exista

    def test_simulacion_estatica_determinista_con_apuestas_multiples(self):
        resultados = iter([3, 2])
        simulador = Simulador()
        simulador.configurar_simulacion(
            'Europea',
            100,
            '10SU[3], 5RE',
            2,
            generador_resultados=lambda ruleta: next(resultados),
        )

        resumen = ModoSimulacionEstatica(simulador).jugar()

        self.assertEqual(resumen['partidas'], 2)
        self.assertEqual(resumen['causa_fin'], 'JuegosCompletados')
        self.assertEqual(resumen['total_apostado'], 30)
        self.assertEqual(resumen['total_ganado'], 355)
        self.assertEqual(resumen['balance_final'], 425)
        self.assertEqual(simulador.frecuencias[3], 1)
        self.assertEqual(simulador.frecuencias[2], 1)

    def test_bancarrota_no_genera_tirada_adicional(self):
        generador_llamado = False

        def generador(ruleta):
            nonlocal generador_llamado
            generador_llamado = True
            return 1

        simulador = Simulador()
        simulador.configurar_simulacion(
            'Europea', 10, '6RE, 5BL', 3, generador_resultados=generador
        )

        resumen = simulador.ejecutar_simulacion()

        self.assertEqual(resumen['partidas'], 0)
        self.assertEqual(resumen['causa_fin'], 'Bancarrota')
        self.assertFalse(generador_llamado)
        self.assertEqual(simulador.historial_tiradas, [])

    def test_seleccionar_modo_estatica_reutiliza_el_gestor(self):
        simulador = Simulador()
        simulador.configurar_simulacion('Europea', 10, '5RE', 0)

        modo = seleccionar_modo(' ESTATICA ', simulador)

        self.assertIs(modo.gestor, simulador)
        self.assertEqual(modo.jugar()['causa_fin'], 'JuegosCompletados')

    def test_simulacion_estatica_conecta_exportador(self):
        simulador = Simulador()
        simulador.configurar_simulacion(
            'Europea',
            20,
            '5RE',
            1,
            generador_resultados=lambda ruleta: 1,
        )
        with tempfile.TemporaryDirectory() as directorio_temporal:
            ruta_base = Path(directorio_temporal)
            exportador = ExportadorCSV(
                ruta_base / 'simulaciones', ruta_base / 'registros.csv'
            )

            resumen = simulador.ejecutar_simulacion(
                exportador=exportador,
                nombre_simulacion='20240101_0101',
            )

            directorio = resumen['directorio']
            self.assertTrue((directorio / 'apuestas.csv').exists())
            self.assertTrue((directorio / 'numeros.csv').exists())
            self.assertTrue((directorio / 'stats.csv').exists())
            self.assertTrue((ruta_base / 'registros.csv').exists())

if __name__ == '__main__':
    unittest.main()