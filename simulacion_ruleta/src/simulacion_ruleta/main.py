import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.simulacion_ruleta.apuestas.parser import parse_apuesta
from src.simulacion_ruleta.consola.interfaz import InterfazConsola
from src.simulacion_ruleta.simulacion.gestor import Simulador


def _ejecutar_modo(modo: str):
    gestor = Simulador()

    if modo == "sencillo":
        gestor.configurar_juego(100, "Europea", 10)
        return gestor.ejecutar_ronda()

    if modo == "estatica":
        gestor.configurar_simulacion(
            "Europea",
            100,
            "10RE",
            5,
        )
        return gestor.ejecutar_simulacion(modo="Estatica")

    if modo == "dinamica":
        gestor.configurar_simulacion(
            "Americana",
            100,
            "10RE, 5BL",
            5,
        )
        return gestor.ejecutar_simulacion(modo="Dinamica")

    raise ValueError(f"Modo no soportado: {modo}")


def _modo_sencillo(interfaz: InterfazConsola):
    interfaz.mostrar_criterios_sencillo()
    while True:
        interfaz.mostrar_mensaje("\nOpciones del modo sencillo:")
        interfaz.mostrar_mensaje("    [A] Ejecutar otra ronda")
        interfaz.mostrar_mensaje("    [X] Volver al menú principal")
        seleccion = interfaz.obtener_opcion().strip().upper()
        if seleccion in {"X", "SALIR"}:
            return
        if seleccion != "A":
            interfaz.mostrar_mensaje("Selección inválida. Se volverá al menú principal.")
            return
        interfaz.mostrar_mensaje("Iniciando modo sencillo...")
        resultado = _ejecutar_modo("sencillo")
        interfaz.mostrar_mensaje(str(resultado))


def _modo_estatica(interfaz: InterfazConsola):
    configuracion = {
        "variante": "Americana",
        "monto_inicial": 500,
        "cantidad_juegos": 100,
        "apuesta_fija": "5SU[3], 10SU[00], 20RE",
    }

    interfaz.mostrar_criterios_estatica()
    while True:
        interfaz.mostrar_menu_estatica(configuracion)
        opcion = interfaz.obtener_opcion().strip().upper()

        if opcion == "A":
            interfaz.mostrar_mensaje("Iniciando simulación estática...")
            gestor = Simulador()
            try:
                gestor.configurar_simulacion(
                    configuracion["variante"],
                    configuracion["monto_inicial"],
                    configuracion["apuesta_fija"],
                    configuracion["cantidad_juegos"],
                )
            except ValueError as error:
                interfaz.mostrar_mensaje(f"Configuración inválida: {error}")
                return
            interfaz.mostrar_mensaje(str(gestor.ejecutar_simulacion(modo="Estatica")))
            return
        if opcion == "B":
            configuracion["variante"] = "Europea" if configuracion["variante"] == "Americana" else "Americana"
            interfaz.mostrar_mensaje(f"Tipo de ruleta actualizado: {configuracion['variante']}")
        elif opcion == "C":
            try:
                configuracion["monto_inicial"] = int(input("Ingrese el nuevo monto inicial: ").strip())
            except ValueError:
                interfaz.mostrar_mensaje("Monto inválido. Se conserva el valor actual.")
        elif opcion == "D":
            try:
                configuracion["cantidad_juegos"] = int(input("Ingrese la nueva cantidad de juegos: ").strip())
            except ValueError:
                interfaz.mostrar_mensaje("Cantidad inválida. Se conserva el valor actual.")
        elif opcion == "E":
            configuracion["apuesta_fija"] = input("Ingrese la nueva apuesta fija: ").strip()
        elif opcion in {"X", "SALIR"}:
            return
        else:
            interfaz.mostrar_mensaje("Opción inválida. Intente nuevamente.")


def _modo_dinamica(interfaz: InterfazConsola):
    configuracion = {
        "variante": "Europea",
        "monto_inicial": 1000,
        "cantidad_juegos": 500,
        "apuesta_fija": "5SU[3], 10RE, 20RE",
        "pool_apuestas": "10RE, 10BL, 5SU[7], 15DZ[1st], 20LO",
    }

    interfaz.mostrar_criterios_dinamica()
    while True:
        interfaz.mostrar_menu_dinamica(configuracion)
        opcion = interfaz.obtener_opcion().strip().upper()

        if opcion == "A":
            interfaz.mostrar_mensaje("Iniciando simulación dinámica...")
            gestor = Simulador()
            try:
                gestor.configurar_simulacion(
                    configuracion["variante"],
                    configuracion["monto_inicial"],
                    configuracion["apuesta_fija"],
                    configuracion["cantidad_juegos"],
                )
                pool = parse_apuesta(configuracion["pool_apuestas"])
            except ValueError as error:
                interfaz.mostrar_mensaje(f"Configuración inválida: {error}")
                return

            opciones = pool if isinstance(pool, list) else [pool]
            resumen = {
                "partidas": 0,
                "causa_fin": "JuegosCompletados",
                "total_apostado": 0,
                "total_ganado": 0,
                "balance_final": gestor.balance,
            }

            for _ in range(configuracion["cantidad_juegos"]):
                if not opciones:
                    break
                apuesta_elegida = random.choice(opciones)
                gestor.apuestas = [apuesta_elegida]
                resultado = gestor.ejecutar_ronda()
                resumen["partidas"] += 1
                resumen["total_apostado"] = gestor.total_apostado
                resumen["total_ganado"] = gestor.total_ganado
                resumen["balance_final"] = gestor.balance
                if resultado.get("causa_fin") == "Bancarrota":
                    resumen["causa_fin"] = "Bancarrota"
                    break
                if gestor.balance <= 0:
                    resumen["causa_fin"] = "Bancarrota"
                    break

            interfaz.mostrar_mensaje(str(resumen))
            return
        if opcion == "B":
            configuracion["variante"] = "Europea" if configuracion["variante"] == "Americana" else "Americana"
            if configuracion["variante"] == "Europea":
                configuracion["apuesta_fija"] = "5SU[3], 10RE, 20RE"
                configuracion["pool_apuestas"] = "10RE, 10BL, 5SU[7], 15DZ[1st], 20LO"
            else:
                configuracion["apuesta_fija"] = "5SU[3], 10SU[00], 20RE"
                configuracion["pool_apuestas"] = "10RE, 10BL, 5SU[7], 15DZ[1st], 20LO, 10BA"
            interfaz.mostrar_mensaje(f"Tipo de ruleta actualizado: {configuracion['variante']}")
        elif opcion == "C":
            try:
                configuracion["monto_inicial"] = int(input("Ingrese el nuevo monto inicial: ").strip())
            except ValueError:
                interfaz.mostrar_mensaje("Monto inválido. Se conserva el valor actual.")
        elif opcion == "D":
            try:
                configuracion["cantidad_juegos"] = int(input("Ingrese la nueva cantidad de juegos: ").strip())
            except ValueError:
                interfaz.mostrar_mensaje("Cantidad inválida. Se conserva el valor actual.")
        elif opcion == "E":
            configuracion["apuesta_fija"] = input("Ingrese la nueva apuesta fija: ").strip()
        elif opcion == "F":
            configuracion["pool_apuestas"] = input("Ingrese el nuevo pool de apuestas: ").strip()
        elif opcion in {"X", "SALIR"}:
            return
        else:
            interfaz.mostrar_mensaje("Opción inválida. Intente nuevamente.")


def main():
    interfaz = InterfazConsola()

    while True:
        interfaz.mostrar_menu()
        opcion = interfaz.obtener_opcion().strip().upper()

        if opcion == "A":
            _modo_sencillo(interfaz)
        elif opcion == "B":
            _modo_estatica(interfaz)
        elif opcion == "C":
            _modo_dinamica(interfaz)
        elif opcion in {"X", "SALIR"}:
            interfaz.despedida()
            break
        else:
            interfaz.mostrar_mensaje("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()