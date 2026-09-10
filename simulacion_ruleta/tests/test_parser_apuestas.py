import pytest

from src.simulacion_ruleta.apuestas.modelos import Apuesta
from src.simulacion_ruleta.apuestas.parser import ApuestaParser, parse_apuesta


def test_parsea_apuesta_individual_y_preserva_seleccion():
    apuesta = parse_apuesta("10SP[1,2]")

    assert isinstance(apuesta, Apuesta)
    assert apuesta.monto == 10
    assert apuesta.tipo == "SP"
    assert apuesta.seleccion == ["1", "2"]


def test_parsea_apuestas_multiples_y_espacios():
    apuestas = parse_apuesta("10RE, 5FF, 20DZ[1st]")

    assert [(apuesta.monto, apuesta.tipo, apuesta.seleccion) for apuesta in apuestas] == [
        (10, "RE", None),
        (5, "FF", None),
        (20, "DZ", ["1st"]),
    ]


@pytest.mark.parametrize("cadena", [
    "",
    "10RE,",
    ",10RE",
    "10-re",
    "10RE[1,2,3,4,5]",
    "RE10",
    "10SU",
    "10FF[0,1,2,3]",
    "10DZ[1]",
    "10DZ[4th]",
    "10RE[1]",
    "0RE",
    "-1RE",
    "10XX",
])
def test_rechaza_sintaxis_y_selecciones_invalidas(cadena):
    with pytest.raises(ValueError):
        parse_apuesta(cadena)


def test_parser_compatibilidad_delega_en_parse_apuesta():
    parser = ApuestaParser()

    assert parser.validar_apuesta("10RE")
    assert not parser.validar_apuesta("10XX")
    assert parser.procesar_apuestas("10RE, 5BL")[1].tipo == "BL"


@pytest.mark.parametrize("tipo", ["SU", "SP", "ST", "CO", "LI"])
def test_apuestas_numericas_rechazan_repetidos_o_fuera_de_rango(tipo):
    seleccion = {
        "SU": "1,1",
        "SP": "1,2,3",
        "ST": "0,1,2",
        "CO": "1,2,4,37",
        "LI": "1,2,3,4,5,7",
    }[tipo]

    with pytest.raises(ValueError):
        parse_apuesta(f"10{tipo}[{seleccion}]")
