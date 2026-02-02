class Jugador:
    def __init__(self, nombre, id, casilla_inicio):
        self.nombre = nombre
        self.id = id
        self.casilla_actual = casilla_inicio
        self.vida = 40
        self.vueltas = 0  # Atributo para el límite de 15 vueltas

    def mover(self, pasos):
        """Mueve al jugador y detecta si completa una vuelta al pasar por el ID 0"""
        for _ in range(pasos):
            self.casilla_actual = self.casilla_actual.siguiente
            if self.casilla_actual.id == 0:
                self.vueltas += 1
                print(f"{self.nombre} ha completado la vuelta {self.vueltas}/15!")

    def modificar_vida(self, cantidad):
        """Cambia el puntaje y avisa claramente en consola"""
        self.vida += cantidad
        simbolo = "☑" if cantidad > 0 else "☒"
        estado = "GANADO" if cantidad > 0 else "PERDIDO"
        print(f"{simbolo} [SISTEMA]: {self.nombre} ha {estado} {abs(cantidad)} puntos.")
        print(f"Nota actual de {self.nombre}: {self.vida} / 70")
    
