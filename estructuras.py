class Casilla:
    def __init__ (self, id_casilla, nombre, tipo, x, y):
        self.id = id_casilla #Número de casilla
        self.nombre = nombre
        self.tipo = tipo  #Puede contener minijuego o no
        self.x = x  # X y Y coordenadas
        self.y = y
        self.siguiente = None #La casilla que le sigue
    def __str__ (self):
        return f"[{self.id} de tipo {self.tipo}]"
    
class Tablero:
    def __init__(self):
        self.inicio = None
        self.fin = None
        self.tamano = 0
    def anadir_casilla(self, nombre, tipo, x, y):
        nueva_casilla = Casilla(self.tamano, nombre, tipo, x, y)
        if self.inicio is None:
            self.inicio = nueva_casilla
            self.fin = nueva_casilla
            self.fin.siguiente = nueva_casilla
        else:
            self.fin.siguiente = nueva_casilla
            self.fin = nueva_casilla
            self.fin.siguiente = self.inicio
        self.tamano += 1