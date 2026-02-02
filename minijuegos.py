import random
import time

#  Lógica del Minijuego:
class NodoPregunta:
    def __init__(self, pregunta, respuesta_correcta):
        self.pregunta = pregunta
        self.respuesta_correcta = respuesta_correcta
        self.derecha = None  # Camino si acierta
        self.izquierda = None # Camino si falla

class Minijuegos:
    def __init__(self):
        # Se genera el árbol de trivia al iniciar
        self.raiz_trivia = self._generar_arbol_trivia()
        self.archivo_log = "historial_minijuegos.txt"

    def _generar_arbol_trivia(self):
        # Construcción del árbol binario
        raiz = NodoPregunta("¿Python es un lenguaje de programación? (si/no)", "si")
        # Nivel 1
        raiz.derecha = NodoPregunta("¿Los Grafos pueden tener ciclos? (si/no)", "si")
        raiz.izquierda = NodoPregunta("¿Los Árboles son Grafos? (si/no)", "si")
        return raiz

    # Para almacenar datos 
    def guardar_resultado(self, jugador, minijuego, resultado):
        with open(self.archivo_log, "a") as f:
            f.write(f"Jugador: {jugador.nombre} | Juego: {minijuego} | Resultado: {resultado} | Nota: {jugador.vida}\n")

    # MINIJUEGO 1: TRIVIA 
    def jugar_trivia(self, jugador):
        print(f"\n--- TRIVIA: {jugador.nombre} ---")
        actual = self.raiz_trivia
        aciertos = 0
        
        while actual:
            print(actual.pregunta)
            resp = input("Respuesta: ").strip().lower()
            if resp == actual.respuesta_correcta:
                aciertos += 1
                actual = actual.derecha # Sube dificultad
            else:
                actual = actual.izquierda # Baja dificultad o termina
        
        bono = aciertos * 5
        jugador.modificar_vida(bono) 
        self.guardar_resultado(jugador, "Trivia", f"{aciertos} aciertos")

    # MINIJUEGO 2: DADO 
    def lanzar_dado(self, jugador):
        dado = random.randint(1, 6)
        print(f"\n{jugador.nombre} lanzó el dado y salió: {dado}")
        
        if dado % 2 == 0:
            jugador.modificar_vida(10) #
            res = "Ganó (Par)"
        else:
            jugador.modificar_vida(-10) #
            res = "Perdió (Impar)"
        
        self.guardar_resultado(jugador, "Dado", res)

    # MINIJUEGO 3: SPEED CLICKER
    def jugar_clicker(self, jugador, clics):
     
        if clics >= 15:
            jugador.modificar_vida(5)
            self.guardar_resultado(jugador, "Clicker", "Ganó")
        else:
            self.guardar_resultado(jugador, "Clicker", "Perdió")

    # MINIJUEGO 4: SALTO DE NODO 
    def salto_de_grafo(self, jugador):
        """Aprovecha que la casilla es un nodo de un grafo/lista enlazada"""
        print(f"\n--- {jugador.nombre}, ¿quieres saltar al siguiente nodo? ---")
        print(f"Estás en: {jugador.casilla_actual.nombre}")
        print(f"El siguiente nodo es: {jugador.casilla_actual.siguiente.nombre}")
        
        opcion = input("¿Saltar? (si/no): ").lower()
        if opcion == "si":
            # Usamos la estructura de Andrés: casilla_actual.siguiente
            jugador.casilla_actual = jugador.casilla_actual.siguiente
            print(f"Ahora estás en: {jugador.casilla_actual.nombre}")
            self.guardar_resultado(jugador, "Grafo", "Salto realizado")
        else:
            print("Te quedas donde estás.")
