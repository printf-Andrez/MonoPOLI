import pygame
from constantes import TAMANO_FICHA

class Jugador:
    def __init__(self, nombre, id, casilla_inicio, ruta_imagen = None):
        self.nombre = nombre
        self.id = id
        self.casilla_actual = casilla_inicio
        self.vida = 40
        self.vueltas = 0  # Atributo para el límite de 12 vueltas
        self.imagen = None
        if ruta_imagen:
            try:
                # convert_alpha() es importante para que se vea la transparencia del PNG
                img_temp = pygame.image.load(ruta_imagen).convert_alpha()
                # Redimensionamos la imagen al tamaño definido en constantes
                self.imagen = pygame.transform.scale(img_temp, (TAMANO_FICHA, TAMANO_FICHA))
            except Exception as e:
                print(f"Error al cargar imagen de {nombre}: {e}")
                self.imagen = None # Si falla, se queda en None y main.py dibujará un círculo

    def mover(self, pasos):
        """Mueve al jugador y detecta si completa una vuelta al pasar por el ID 0"""
        for _ in range(pasos):
            self.casilla_actual = self.casilla_actual.siguiente
            if self.casilla_actual.id == 0:
                self.vueltas += 1
                print(f"{self.nombre} ha completado la vuelta {self.vueltas}/12!")

    def modificar_vida(self, cantidad):
        """Cambia el puntaje y avisa claramente en consola"""
        self.vida += cantidad
        if self.vida > 40:
            self.vida = 40
        simbolo = "☑" if cantidad > 0 else "☒"
        estado = "GANADO" if cantidad > 0 else "PERDIDO"
        print(f"{simbolo} [SISTEMA]: {self.nombre} ha {estado} {abs(cantidad)} puntos.")
        print(f"Nota actual de {self.nombre}: {self.vida} / 40")