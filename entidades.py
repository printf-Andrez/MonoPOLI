class Jugador:
    def __init__(self, nombre, id_jugador, nodo_inicial):
        self.nombre = nombre
        self.id_jugador = id_jugador
        self.vida = 40
        self.vida_max = 40
        self.casilla_actual = nodo_inicial
        self.ganador = False
    def mover (self, num_casillas):
        for cont in range(num_casillas):
            self.casilla_actual = self.casilla_actual.siguiente
    def modificar_vida (self, cantidad_vida):
        self.vida += cantidad_vida
        if self.vida > self.vida_max:
            self.vida = self.vida_max
        if self.vida < 0:
            self.vida = 0
    def __str__(self):
        return f"{self.nombre} (Nota: {self.vida}) en casilla: {self.casilla_actual.nombre}"
    