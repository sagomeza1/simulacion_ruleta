class Apuesta:
    def __init__(self, monto: float, tipo: str):
        self.monto = monto
        self.tipo = tipo

    def __str__(self):
        return f"Apuesta(monto={self.monto}, tipo='{self.tipo}')"


class ApuestaMultiple:
    def __init__(self, apuestas: list):
        self.apuestas = apuestas

    def agregar_apuesta(self, apuesta: Apuesta):
        self.apuestas.append(apuesta)

    def __str__(self):
        return f"ApuestaMultiple(apuestas={self.apuestas})"