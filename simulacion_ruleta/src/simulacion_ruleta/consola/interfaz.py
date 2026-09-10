class InterfazConsola:
    def __init__(self):
        self.bienvenida()

    def bienvenida(self):
        self.mostrar_menu()

    def mostrar_menu(self):
        print("==================================================")
        print("           --- SIMULACIÓN DE RULETA ---")
        print("==================================================")
        print("Seleccione el tipo de juego:")
        print()
        print("    [A] Modo Sencillo")
        print("    [B] Simulación Estática")
        print("    [C] Simulación Dinámica")
        print("    [X] Salir")
        print()
        print("Indicar opción: ")

    def mostrar_criterios_sencillo(self):
        print("\nCriterios del Modo Sencillo:")
        print("- El usuario ingresa un monto inicial en su bolsillo.")
        print("- Se ejecuta ronda por ronda.")
        print("- Cada partida acepta una apuesta por tirada.")
        print("- Se permite apostar 0 para pasar la ronda.")
        print("- La sesión finaliza al salir o por bancarrota.")

    def mostrar_criterios_estatica(self):
        print("\nCriterios del Modo Simulación Estática:")
        print("- Requiere: tipo de ruleta, monto inicial, apuesta fija y cantidad total de partidas.")
        print("- El sistema realiza N partidas con la misma apuesta fija.")
        print("- Se detiene al completar las partidas o por bancarrota.")

    def mostrar_criterios_dinamica(self):
        print("\nCriterios del Modo Simulación Dinámica:")
        print("- Requiere: tipo de ruleta, monto inicial, apuesta fija, pool de apuestas y cantidad total de partidas.")
        print("- En cada jugada se elige aleatoriamente una apuesta del pool configurado.")
        print("- Se detiene al completar las partidas o por bancarrota.")

    def mostrar_menu_estatica(self, configuracion=None):
        config = configuracion or {
            "variante": "Americana",
            "monto_inicial": 500,
            "cantidad_juegos": 100,
            "apuesta_fija": "5SU[3], 10SU[00], 20RE",
        }
        print("==================================================")
        print("           --- SIMULACIÓN DE RULETA ---")
        print("              Modo Simulación Estática")
        print("==================================================")
        print("Parámetros actuales:")
        print(f"  - Tipo de Ruleta   : {config['variante']}")
        print(f"  - Monto inicial    : ${config['monto_inicial']}")
        print(f"  - Cantidad juegos  : {config['cantidad_juegos']}")
        print(f"  - Apuesta fija     : {config['apuesta_fija']}")
        print()
        print("Seleccione una opción:")
        print()
        print("    [A] Iniciar simulación")
        print("    [B] Modificar tipo de ruleta")
        print("    [C] Modificar monto inicial")
        print("    [D] Modificar cantidad de juegos")
        print("    [E] Modificar apuesta fija (separada por comas)")
        print("    [X] Atrás")
        print()
        print("Indicar opción: ")

    def mostrar_menu_dinamica(self, configuracion=None):
        config = configuracion or {
            "variante": "Europea",
            "monto_inicial": 1000,
            "cantidad_juegos": 500,
            "apuesta_fija": "5SU[3], 10SU[00], 20RE",
            "pool_apuestas": "10RE, 10BL, 5SU[7], 15DZ[1st], 20LO",
        }
        print("==================================================")
        print("           --- SIMULACIÓN DE RULETA ---")
        print("              Modo Simulación Dinámica")
        print("==================================================")
        print("Parámetros actuales:")
        print(f"  - Tipo de Ruleta   : {config['variante']}")
        print(f"  - Monto inicial    : ${config['monto_inicial']}")
        print(f"  - Cantidad juegos  : {config['cantidad_juegos']}")
        print(f"  - Apuesta fija     : {config['apuesta_fija']}")
        print(f"  - Pool de apuestas : {config['pool_apuestas']}")
        print()
        print("Seleccione una opción:")
        print()
        print("    [A] Iniciar simulación")
        print("    [B] Modificar tipo de ruleta")
        print("    [C] Modificar monto inicial")
        print("    [D] Modificar cantidad de juegos")
        print("    [E] Modificar apuesta fija (separada por comas)")
        print("    [F] Configurar lista de apuestas (separada por comas)")
        print("    [X] Atrás")
        print()
        print("Indicar opción: ")

    def obtener_opcion(self):
        return input().strip()

    def mostrar_mensaje(self, mensaje):
        print(mensaje)

    def mostrar_resultados(self, resultados):
        print("\nResultados de la Simulación:")
        for resultado in resultados:
            print(resultado)

    def despedida(self):
        print("Gracias por jugar. ¡Hasta la próxima!")