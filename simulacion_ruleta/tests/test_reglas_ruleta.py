import pytest

from src.simulacion_ruleta.apuestas.parser import parse_apuesta
from src.simulacion_ruleta.ruleta.modelos import Casilla, Ruleta
from src.simulacion_ruleta.ruleta.reglas import ReglasRuleta


ROJOS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
NEGROS = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
PAGOS = {
    "SU": 35, "SP": 17, "ST": 11, "CO": 8, "FF": 8, "BA": 6,
    "LI": 5, "DZ": 2, "CL": 2, "LO": 1, "HI": 1, "EV": 1,
    "OD": 1, "RE": 1, "BL": 1,
}


def apuesta(cadena):
    return parse_apuesta(cadena)


def test_casillas_exactas_y_variantes():
    assert Ruleta("Europea").casillas == list(range(37))
    assert Ruleta("americana").casillas == [0, "00", *range(1, 37)]
    with pytest.raises(ValueError):
        Ruleta("inexistente")


def test_colores_oficiales_incluyen_ceros_verdes():
    assert Casilla(0).color == "Verde"
    assert Casilla("00").color == "Verde"
    assert all(Casilla(numero).color == "Rojo" for numero in ROJOS)
    assert all(Casilla(numero).color == "Negro" for numero in NEGROS)


def test_pagos_de_los_15_codigos_oficiales():
    reglas = ReglasRuleta("Europea")
    assert {tipo: reglas.obtener_pago(tipo) for tipo in PAGOS} == PAGOS


@pytest.mark.parametrize("cadena,resultado", [
    ("10SU[3]", 3),
    ("10SP[1,2]", 2),
    ("10ST[4,5,6]", 5),
    ("10CO[4,5,7,8]", 8),
    ("10LI[1,2,3,4,5,6]", 6),
    ("10DZ[1st]", 12),
    ("10CL[2nd]", 5),
    ("10LO", 18),
    ("10HI", 19),
    ("10EV", 2),
    ("10OD", 3),
    ("10RE", 3),
    ("10BL", 2),
    ("10FF", 0),
])
def test_apuestas_aciertan_y_calculan_ganancia_bruta(cadena, resultado):
    reglas = ReglasRuleta("Europea")
    apuesta_actual = apuesta(cadena)

    assert reglas.acierta(apuesta_actual, resultado)
    assert reglas.calcular_ganancia(apuesta_actual, resultado) == apuesta_actual.monto * reglas.obtener_pago(apuesta_actual.tipo)


def test_basket_00_y_pleno_americano():
    reglas = ReglasRuleta("Americana")

    assert reglas.acierta(apuesta("10BA"), "00")
    assert reglas.calcular_ganancia(apuesta("10SU[00]"), "00") == 350


def test_fallos_y_exclusion_de_ceros_en_pares_impares():
    reglas = ReglasRuleta("Americana")
    assert not reglas.acierta(apuesta("10SU[3]"), 4)
    assert not reglas.acierta(apuesta("10EV"), 0)
    assert not reglas.acierta(apuesta("10OD"), "00")


def test_apuestas_exclusivas_de_variante():
    with pytest.raises(ValueError):
        ReglasRuleta("Europea").acierta(apuesta("10BA"), 0)
    with pytest.raises(ValueError):
        ReglasRuleta("Americana").acierta(apuesta("10FF"), 0)
    with pytest.raises(ValueError):
        ReglasRuleta("Europea").acierta(apuesta("10SU[00]"), 0)


@pytest.mark.parametrize("cadena", [
    "10SP[1,3]",
    "10ST[1,2,4]",
    "10CO[1,2,3,4]",
    "10LI[1,2,3,4,5,7]",
])
def test_rechaza_estructuras_geometricas_invalidas(cadena):
    with pytest.raises(ValueError):
        apuesta(cadena)
