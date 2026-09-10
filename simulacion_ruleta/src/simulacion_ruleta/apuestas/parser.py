import re
from typing import List, Union

from .modelos import Apuesta


PATRON_APUESTA = re.compile(r"^\d+[A-Z]{2}(\[[\w,-]+\])?$")
CODIGOS_CON_SELECCION = {"SU", "SP", "ST", "CO", "LI", "DZ", "CL"}
CODIGOS_SIN_SELECCION = {"FF", "BA", "LO", "HI", "EV", "OD", "RE", "BL"}
CODIGOS_OFICIALES = CODIGOS_CON_SELECCION | CODIGOS_SIN_SELECCION


def _numeros(seleccion: List[str], tipo: str) -> List[int]:
    if any(not token.isdigit() or token not in {"00", *[str(numero) for numero in range(37)]} for token in seleccion):
        raise ValueError(f"La selección de {tipo} debe contener números del 0 al 36")
    numeros = [int(token) for token in seleccion if token != "00"]
    if "00" in seleccion and tipo != "SU":
        raise ValueError(f"{tipo} no puede cubrir la casilla 00")
    if any(numero > 36 for numero in numeros):
        raise ValueError(f"La selección de {tipo} contiene un número fuera de rango")
    if len(set(numeros)) != len(numeros):
        raise ValueError(f"La selección de {tipo} no puede repetir números")
    return numeros


def _validar_geometria(tipo: str, seleccion: List[str]) -> None:
    cantidades = {"SU": 1, "SP": 2, "ST": 3, "CO": 4, "LI": 6}
    if len(seleccion) != cantidades[tipo]:
        raise ValueError(f"{tipo} requiere {cantidades[tipo]} número(s)")
    numeros = _numeros(seleccion, tipo)
    if tipo == "SU":
        return
    if tipo == "ST":
        if numeros != list(range(min(numeros), min(numeros) + 3)) or (min(numeros) - 1) % 3 != 0:
            raise ValueError("ST debe cubrir una fila de tres números")
        return
    filas = {(numero - 1) // 3 for numero in numeros}
    columnas = {(numero - 1) % 3 for numero in numeros}
    if tipo == "SP":
        adyacentes = len(filas) == 1 and len(columnas) == 2 or len(filas) == 2 and len(columnas) == 1
        if not adyacentes or max(numeros) - min(numeros) not in (1, 3):
            raise ValueError("SP debe cubrir dos números adyacentes")
    elif tipo == "CO":
        if len(filas) != 2 or len(columnas) != 2 or max(filas) - min(filas) != 1 or max(columnas) - min(columnas) != 1:
            raise ValueError("CO debe cubrir una esquina válida")
    elif tipo == "LI":
        if len(filas) != 2 or any(sum(fila == fila_actual for fila in filas) != 1 for fila_actual in filas):
            raise ValueError("LI debe cubrir dos calles contiguas")
        calles = sorted({min(numero for numero in numeros if (numero - 1) // 3 == fila) for fila in filas})
        if calles[1] - calles[0] != 3:
            raise ValueError("LI debe cubrir dos calles contiguas")


def _parsear_individual(cadena: str) -> Apuesta:
    if not PATRON_APUESTA.fullmatch(cadena):
        raise ValueError(f"Apuesta inválida: {cadena}")
    coincidencia = re.fullmatch(r"(\d+)([A-Z]{2})(?:\[([\w,-]+)\])?", cadena)
    assert coincidencia is not None
    monto = int(coincidencia.group(1))
    tipo = coincidencia.group(2)
    contenido = coincidencia.group(3)
    if monto <= 0:
        raise ValueError("El monto de la apuesta debe ser positivo")
    if tipo not in CODIGOS_OFICIALES:
        raise ValueError(f"Código de apuesta desconocido: {tipo}")
    seleccion = contenido.split(",") if contenido is not None else None
    if tipo in CODIGOS_CON_SELECCION and seleccion is None:
        raise ValueError(f"La apuesta {tipo} requiere una selección")
    if tipo in CODIGOS_SIN_SELECCION and seleccion is not None:
        raise ValueError(f"La apuesta {tipo} no admite selección")
    if tipo in {"DZ", "CL"} and seleccion != ["1st"] and seleccion != ["2nd"] and seleccion != ["3rd"]:
        raise ValueError(f"La apuesta {tipo} requiere 1st, 2nd o 3rd")
    if tipo in {"SU", "SP", "ST", "CO", "LI"}:
        _validar_geometria(tipo, seleccion or [])
    return Apuesta(monto=monto, tipo=tipo, seleccion=seleccion)


def parse_apuesta(cadena: str) -> Union[Apuesta, List[Apuesta]]:
    """Parsea una apuesta individual o una lista separada por comas."""
    if not isinstance(cadena, str) or not cadena.strip():
        raise ValueError("La apuesta no puede estar vacía")
    tokens = []
    inicio = 0
    profundidad = 0
    for indice, caracter in enumerate(cadena):
        if caracter == "[":
            profundidad += 1
        elif caracter == "]":
            profundidad -= 1
        elif caracter == "," and profundidad == 0:
            tokens.append(cadena[inicio:indice])
            inicio = indice + 1
    tokens.append(cadena[inicio:])
    if any(not token.strip() for token in tokens):
        raise ValueError("No se permiten apuestas vacías")
    apuestas = [_parsear_individual(token.strip()) for token in tokens]
    return apuestas[0] if len(apuestas) == 1 else apuestas


class ApuestaParser:
    def validar_apuesta(self, apuesta: str) -> bool:
        try:
            parse_apuesta(apuesta)
        except ValueError:
            return False
        return True

    def procesar_apuestas(self, apuestas: str) -> List[Apuesta]:
        resultado = parse_apuesta(apuestas)
        return resultado if isinstance(resultado, list) else [resultado]