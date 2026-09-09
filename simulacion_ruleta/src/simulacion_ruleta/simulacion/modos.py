# Contenido del archivo: /simulacion_ruleta/simulacion_ruleta/src/simulacion_ruleta/simulacion/modos.py

class ModoSencillo:
    def jugar(self):
        # Lógica para el modo sencillo
        pass

class ModoSimulacionEstatica:
    def jugar(self):
        # Lógica para el modo de simulación estática
        pass

class ModoSimulacionDinamica:
    def jugar(self):
        # Lógica para el modo de simulación dinámica
        pass

def seleccionar_modo(modo):
    if modo == 'sencillo':
        return ModoSencillo()
    elif modo == 'estatica':
        return ModoSimulacionEstatica()
    elif modo == 'dinamica':
        return ModoSimulacionDinamica()
    else:
        raise ValueError("Modo de juego no válido")