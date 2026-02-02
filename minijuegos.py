import random

# REQUISITO: ÁRBOLES
class NodoPregunta:
    def __init__(self, pregunta, respuesta_correcta):
        self.pregunta = pregunta
        self.respuesta_correcta = respuesta_correcta
        self.derecha = None  
        self.izquierda = None 

class Minijuegos:
    def __init__(self):
        self.raiz_trivia = self._generar_arbol_trivia()
        self.archivo_log = "historial_minijuegos.txt"

    def _generar_arbol_trivia(self):
        """Crea la estructura del árbol para la trivia"""
        raiz = NodoPregunta("¿Python es interpretado? (si/no)", "si")
        raiz.derecha = NodoPregunta("¿Los nodos de un arbol tienen un solo padre? (si/no)", "si")
        raiz.izquierda = NodoPregunta("¿Un arbol puede tener ciclos? (si/no)", "no")
        return raiz

    def guardar_resultado(self, jugador, minijuego, resultado):
        """Guarda datos en archivo de texto"""
        with open(self.archivo_log, "a") as f:
            # Usa atributos de la clase Jugador
            f.write(f"Jugador: {jugador.nombre} | Juego: {minijuego} | Resultado: {resultado} | Nota: {jugador.vida}\n")

    # MINIJUEGO 1: TRIVIA (Usa Árboles)
    def jugar_trivia(self, jugador):
        print(f"\n--- TRIVIA: RESPONDE EN LA TERMINAL ABAJO ---")
        actual = self.raiz_trivia
        aciertos = 0
        while actual:
            print(f"Pregunta: {actual.pregunta}")
            resp = input("Tu respuesta: ").strip().lower()
            if resp == actual.respuesta_correcta:
                print("¡Correcto!")
                aciertos += 1
                actual = actual.derecha
            else:
                print("Incorrecto.")
                actual = actual.izquierda
        
        # Cálculo y aviso de puntos
        puntos = aciertos * 5
        jugador.modificar_vida(puntos) # Llama al método con print que hicimos arriba
        
        print("\n" + "="*40)
        print(f"RESUMEN PARA {jugador.nombre.upper()}:")
        print(f"Aciertos: {aciertos} | Puntaje: +{puntos}")
        print("="*40)
        
        self.guardar_resultado(jugador, "Trivia", f"{aciertos} aciertos")

    # MINIJUEGO 2: DADO
    def lanzar_dado(self, jugador):
        dado = random.randint(1, 6)
        print(f"\n--- MINIJUEGO DADO: Salió {dado} ---")
        ganó = (dado % 2 == 0)
        if ganó:
            jugador.modificar_vida(10)
            res = "Gano (Par)"
        else:
            jugador.modificar_vida(-10)
            res = "Perdio (Impar)"
        
        self.guardar_resultado(jugador, "Dado", res)
        return dado, ganó

    # MINIJUEGO 4: SALTO DE GRAFO 
    def salto_de_grafo(self, jugador):
        print(f"\n--- DESAFÍO DE GRAFO ---")
        # Accede al atributo siguiente de la casilla actual
        print(f"La siguiente casilla es: {jugador.casilla_actual.siguiente.nombre}")
        opcion = input("¿Quieres saltar directamente a ella? (si/no): ").lower()
        if opcion == "si":
            jugador.mover(1) # Usa método mover de entidades.py
            print(f"Movido a: {jugador.casilla_actual.nombre}")
            self.guardar_resultado(jugador, "Grafo", "Salto realizado")
        else:
            print("Decidiste no saltar.")
