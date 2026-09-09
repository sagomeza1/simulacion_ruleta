import unittest
from src.simulacion_ruleta.ruleta.reglas import ReglasRuleta

class TestReglasRuleta(unittest.TestCase):

    def setUp(self):
        self.reglas = ReglasRuleta()

    def test_pago_ruleta_europea(self):
        # Test de pagos para la ruleta europea
        self.assertEqual(self.reglas.calcular_pago('pleno', 10), 350)
        self.assertEqual(self.reglas.calcular_pago('color', 10, 'rojo'), 20)

    def test_pago_ruleta_americana(self):
        # Test de pagos para la ruleta americana
        self.reglas.set_variantes('americana')
        self.assertEqual(self.reglas.calcular_pago('pleno', 10), 360)
        self.assertEqual(self.reglas.calcular_pago('color', 10, 'negro'), 20)

    def test_mapeo_colores(self):
        # Test de mapeo de colores
        self.assertEqual(self.reglas.mapeo_color(0), 'verde')
        self.assertEqual(self.reglas.mapeo_color(1), 'rojo')
        self.assertEqual(self.reglas.mapeo_color(2), 'negro')

if __name__ == '__main__':
    unittest.main()