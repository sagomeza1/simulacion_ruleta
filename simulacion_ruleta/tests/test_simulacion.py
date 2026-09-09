import unittest
from src.simulacion_ruleta.simulacion.gestor import Simulador

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

if __name__ == '__main__':
    unittest.main()