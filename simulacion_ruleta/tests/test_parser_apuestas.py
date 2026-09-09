import pytest
from src.simulacion_ruleta.apuestas.parser import parse_apuesta

def test_parse_apuesta_valida():
    assert parse_apuesta("10RE") == {"monto": 10, "tipo": "RE", "seleccion": None}
    assert parse_apuesta("5FF[1,2]") == {"monto": 5, "tipo": "FF", "seleccion": ["1", "2"]}
    assert parse_apuesta("20DZ[1st]") == {"monto": 20, "tipo": "DZ", "seleccion": ["1st"]}

def test_parse_apuesta_invalida():
    with pytest.raises(ValueError):
        parse_apuesta("10INVALIDO")
    with pytest.raises(ValueError):
        parse_apuesta("5RE[1,2,3,4,5]")  # Selección inválida para tipo de apuesta
    with pytest.raises(ValueError):
        parse_apuesta("RE10")  # Formato incorrecto

def test_parse_apuesta_multiple():
    apuestas = parse_apuesta("10RE, 5FF[1,2], 20DZ[1st]")
    assert len(apuestas) == 3
    assert apuestas[0] == {"monto": 10, "tipo": "RE", "seleccion": None}
    assert apuestas[1] == {"monto": 5, "tipo": "FF", "seleccion": ["1", "2"]}
    assert apuestas[2] == {"monto": 20, "tipo": "DZ", "seleccion": ["1st"]}