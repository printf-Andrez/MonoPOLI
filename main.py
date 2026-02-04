import pygame
import sys
from estructuras import Tablero
from entidades import Jugador
from minijuegos import Minijuegos

# --- CONFIGURACIÓN INICIAL ---
ANCHO, ALTO = 1000, 800 
MARGEN_TABLERO = 120      # Espacio para que el título quepa arriba
COLOR_FONDO = (240, 244, 248) # Gris azulado muy claro (estilo aplicación)
AZUL_CASILLA = (59, 130, 246)    # Azul vibrante (estilo Tailwind)
DORADO_CASILLA = (245, 158, 11)  # Naranja/Dorado elegante
COLOR_LINEA = (100, 100, 100)
BORDE_TABLERO = (203, 213, 225)  # Gris para las líneas de conexión
COLOR_TEXTO = (30, 41, 59)       # Azul oscuro casi negro para legibilidad
COLOR_JUGADOR_1 = (200, 50, 50) # Rojo
COLOR_JUGADOR_2 = (50, 200, 50) # Verde

# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("MonoPOLI - Bori's Version")
fuente = pygame.font.SysFont("Arial", 16)
fuente_grande = pygame.font.SysFont("Arial", 24, bold=True)
fuente_titulo = pygame.font.SysFont("Arial", 36, bold=True)
fuente_pequena = pygame.font.SysFont("Arial", 14)

class JuegoGrafico:
    def __init__(self):
        pygame.init() #Aseguramos que se inicie
        self.pantalla = pygame.display.set_mode((1000, 800))

        self.tablero = Tablero()
        self.generar_mapa_cuadrado()
        self.jugadores = [
            Jugador("DonLuis", 1, self.tablero.inicio),
            Jugador("Miguel", 2, self.tablero.inicio)
        ]

        self.tumbas = []
        self.turno_actual = 0
        self.corriendo = True
        
        # DEFINIR EL ARCHIVO DE LOG
        self.archivo_log = "historial_partida.txt"

        # Forzamos la vida inicial a 40 para el semestre
        for j in self.jugadores:
            j.vida = 40
            
        self.minijuegos = Minijuegos()
        self.turno_actual = 0
        self.jugando = True  

    def mostrar_pantalla_inicio(self):
        try:
            fondo = pygame.image.load('Portada (1).png').convert()
            fondo = pygame.transform.scale(fondo, (1000, 800)) # tamaño de la pantalla
        except pygame.error as e:
            print(f"Error al cargar la imagen de fondo: {e}")
            fondo = pygame.Surface((1000, 800))
            fondo.fill((40, 40, 40)) 
        
        # Fuente para el botón y el título
        fuente_titulo = pygame.font.SysFont("Arial", 70, bold=True)
        fuente_boton = pygame.font.SysFont("Arial", 40, bold=True)
        
        # Colores
        COLOR_BOTON = (0, 150, 0) # Verde
        COLOR_TEXTO_BOTON = (255, 255, 255) # Blanco
        
        # Rectángulo para el botón "Jugar"
        rect_boton = pygame.Rect(400, 600, 200, 70) # x, y, ancho, alto

        esperando_inicio = True
        while esperando_inicio:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    import sys
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if rect_boton.collidepoint(evento.pos):
                        esperando_inicio = False # El juego puede empezar

            # Dibujar el fondo
            self.pantalla.blit(fondo, (0, 0))

            # Dibujar el botón
            pygame.draw.rect(self.pantalla, COLOR_BOTON, rect_boton, border_radius=15)
            txt_jugar = fuente_boton.render("Jugar", True, COLOR_TEXTO_BOTON)
            self.pantalla.blit(txt_jugar, (rect_boton.centerx - txt_jugar.get_width()//2, rect_boton.centery - txt_jugar.get_height()//2))

            pygame.display.flip()

    def generar_mapa_cuadrado(self):
        margen_x, margen_y = 150, 150
        ancho_util = ANCHO - (margen_x * 2)
        alto_util = ALTO - 350
        
        # Posiciones de los "Exámenes" (Minijuegos) en las casillas 
        pos_minijuegos = [2, 5, 10]

        # Posiciones para preguntas Bonus 
        pos_peligro = [3, 7, 9]
        
        # Lista de coordenadas para las 12 casillas (ID 0 al 11)
        puntos = []
        
        for i in range(4):
            puntos.append((margen_x + i * (ancho_util // 3), margen_y))
        
        # Derecha (2 casillas: 4, 5)
        for i in range(1, 3):
            puntos.append((ANCHO - margen_x, margen_y + i * (alto_util // 3)))
            
        # Inferior (4 casillas: 6, 7, 8, 9) en reversa
        for i in range(4):
            puntos.append((ANCHO - margen_x - i * (ancho_util // 3), margen_y + alto_util))
            
        # Izquierda (2 casillas: 10, 11) en reversa
        for i in range(1, 3):
            puntos.append((margen_x, margen_y + alto_util - i * (alto_util // 3)))

        # Crear las casillas físicamente en el tablero
        for i, (px, py) in enumerate(puntos):
            if i in pos_minijuegos:
                tipo = "Minijuego"
                nombre = "Examen"
            elif i in pos_peligro:
                tipo = "Peligro" 
                nombre = "¡FALLA!"
            else:
                tipo = "Normal"
                nombre = "Semana"
            
            self.tablero.anadir_casilla(nombre, tipo, px, py)

    def dibujar_tablero(self):
        # Dibujar líneas de conexión primero
        actual = self.tablero.inicio
        for _ in range(self.tablero.tamano):
            sig = actual.siguiente
            pygame.draw.line(pantalla, BORDE_TABLERO, (actual.x, actual.y), (sig.x, sig.y), 4)
            actual = sig

        # Dibujar círculos con borde
        actual = self.tablero.inicio
        for _ in range(self.tablero.tamano):
            # Color según el tipo
            if actual.tipo == "Minijuego":
                color = (245, 158, 11) # Dorado
            elif actual.tipo == "Peligro":
                color = (220, 38, 38)  # Rojo 
            else:
                color = (59, 130, 246) # Azul
            
            # Sombra/Borde para dar profundidad
            pygame.draw.circle(pantalla, (255, 255, 255), (actual.x, actual.y), 28) # Brillo exterior
            pygame.draw.circle(pantalla, color, (actual.x, actual.y), 25)           # Casilla
            pygame.draw.circle(pantalla, (0, 0, 0), (actual.x, actual.y), 25, 2)    # Contorno
            
            # ID de la casilla
            id_txt = fuente_pequena.render(str(actual.id), True, (255, 255, 255))
            pantalla.blit(id_txt, (actual.x - id_txt.get_width()//2, actual.y - id_txt.get_height()//2))
            actual = actual.siguiente

        # DIBUJAR TUMBAS DE REPROBADOS
        for tx, ty in self.tumbas:
            pygame.draw.circle(self.pantalla, (50, 50, 50), (tx, ty), 15)
            
            fuente_tumba = pygame.font.SysFont("Arial", 20, bold=True)
            txt_x = fuente_tumba.render("X", True, (200, 200, 200))
            self.pantalla.blit(txt_x, (tx - txt_x.get_width()//2, ty - txt_x.get_height()//2))

    def dibujar_jugadores(self):
        for i, jug in enumerate(self.jugadores):
            # i*10 para que no se tapen exactamente si están en la misma casilla
            pos_x = jug.casilla_actual.x + (i * 15 - 7) 
            pos_y = jug.casilla_actual.y - 30 
            
            color_ficha = (239, 68, 68) if i == 0 else (34, 197, 94) # Rojo y Verde vibrantes
            pygame.draw.circle(pantalla, color_ficha, (pos_x, pos_y), 12)
            pygame.draw.circle(pantalla, (0, 0, 0), (pos_x, pos_y), 12, 2)

    def dibujar_interfaz(self):
        # 1. Título
        titulo_surf = fuente_titulo.render("MonoPOLI: La Aventura de Algoritmos", True, (40, 40, 40))
        # Lo ponemos a 10 píxeles del borde superior
        pantalla.blit(titulo_surf, (ANCHO // 2 - titulo_surf.get_width() // 2, 10))

        # 2. Dado
        if hasattr(self, 'ultimo_valor_dado'):
            rect_dado = pygame.Rect(ANCHO // 2 - 50, ALTO // 2 - 50, 100, 100)
            
            # Sombra del dado
            pygame.draw.rect(pantalla, (200, 200, 200), rect_dado.move(4, 4), border_radius=15)
            # Cuerpo del dado
            pygame.draw.rect(pantalla, (255, 255, 255), rect_dado, border_radius=15)
            
            # Color del borde y número según el turno actual
            color_turno = (34, 197, 94) if self.turno_actual == 0 else (239, 68, 68) # Rojo o Verde
            pygame.draw.rect(pantalla, color_turno, rect_dado, 4, border_radius=15)
            
            # Dibujar el número
            val_txt = fuente_titulo.render(str(self.ultimo_valor_dado), True, color_turno)
            pos_x = ANCHO // 2 - val_txt.get_width() // 2
            pos_y = ALTO // 2 - val_txt.get_height() // 2
            pantalla.blit(val_txt, (pos_x, pos_y))
            
            # Texto pequeño que dice "DADO"
            txt_dado = fuente_pequena.render("DADO", True, (100, 100, 100))
            pantalla.blit(txt_dado, (ANCHO // 2 - txt_dado.get_width() // 2, ALTO // 2 + 55))

        # 3. PANEL INFERIOR 
        pygame.draw.rect(pantalla, (255, 255, 255), (0, ALTO - 120, ANCHO, 120))
        pygame.draw.line(pantalla, (200, 200, 200), (0, ALTO - 120), (ANCHO, ALTO - 120), 2)

        # 4. ESTADO DEL JUGADOR (Izquierda)
        jugador_activo = self.jugadores[self.turno_actual]
        info_txt = f"Turno de: {jugador_activo.nombre} | Nota: {jugador_activo.vida}"
        txt_render = fuente_grande.render(info_txt, True, (33, 150, 243))
        pantalla.blit(txt_render, (50, ALTO - 75))

        # 5. CONTADOR DE VUELTAS (Arriba a la derecha)
        for i, jug in enumerate(self.jugadores):
            txt_v = fuente_pequena.render(f"Meta {jug.nombre}: {jug.vueltas}/1 Vuelta", True, (80, 80, 80))
            pantalla.blit(txt_v, (ANCHO - 180, 20 + i*20))

        # 6. INSTRUCCIONES (A la derecha en el panel inferior)
        x_inst = 600
        inst_lineas = [
            "Instrucciones:", 
                               "- [ESPACIO]: Lanzar dado.",
                               "- Casilla Dorada: Minijuego.",
                               "- Casiila Roda: Pregunta Bonus."
                               "- Gana en dar primero una vuelta."
                               
        ]
        for i, linea in enumerate(inst_lineas):
            f = fuente_grande if i == 0 else fuente_pequena
            color = (0,0,0) if i == 0 else (100, 100, 100)
            texto = f.render(linea, True, color)
            pantalla.blit(texto, (x_inst, ALTO - 110 + (i * 22)))

    def mover_jugador(self):
        import random
        import pygame
        import time # Necesario para la pausa de celebración
        
        # 1. LANZAMIENTO ÚNICO DE DADO
        valor_lanzado = random.randint(1, 2) 
        self.ultimo_valor_dado = valor_lanzado
        jugador = self.jugadores[self.turno_actual]

        print(f"\n" + "-"*30)
        print(f"TURNO DE: {jugador.nombre}")
        print(f"El dado marca: {valor_lanzado}")
        
        # 2. MOVER AL JUGADOR
        jugador.mover(valor_lanzado)

        # ANTES de que el input() de la trivia detenga el programa.
        pantalla.fill(COLOR_FONDO)
        self.dibujar_tablero()
        self.dibujar_jugadores()
        self.dibujar_interfaz()
        pygame.display.flip() # 
        
        # 3. LÓGICA DE CASILLA ESPECIAL
        casilla_final = jugador.casilla_actual 
        tipo_detectado = casilla_final.tipo.strip() 
        print(f"DEBUG: {jugador.nombre} en Casilla {casilla_final.id} ({tipo_detectado})")

        if tipo_detectado == "Minijuego":
            time.sleep(0.5) 
            print(f" ¡MINIJUEGO ACTIVADO!")
            opcion = random.choice(["Trivia", "Dado"])
            
            if opcion == "Trivia":
                self.minijuegos.jugar_trivia(jugador, pantalla) 
            else:
                self.minijuegos.lanzar_dado(jugador, pantalla)

        elif tipo_detectado == "Peligro": 
            time.sleep(0.5)
            print(f" ¡CASILLA DE PELIGRO ACTIVADA!")
            self.minijuegos.reto_peligro(jugador, pantalla)
            
        else:
            print(f"Casilla normal. Saltando lógica de minijuego.")

        # 4. LÓGICA DE ELIMINACIÓN 
        if jugador.vida <= 0:
            nombre_reprobado = jugador.nombre
            
            #Para que quede su posición de donde reprobó.
            pos_tumba = (jugador.casilla_actual.x, jugador.casilla_actual.y)
            self.tumbas.append(pos_tumba)

            # 1. Efecto de parpadeo y espera activa
            for i in range(6):  # Parpadeará 3 veces (rojo/oscuro)
                # Alternar colores entre rojo oscuro y casi negro
                color = (150, 0, 0) if i % 2 == 0 else (30, 0, 0)
                pantalla.fill(color)
                
                fuente_derrota = pygame.font.SysFont("Arial", 50, bold=True)
                txt = fuente_derrota.render(f"¡{nombre_reprobado} REPROBÓ!", True, (255, 255, 255))
                sub_txt = fuente_derrota.render("Saliendo del sistema...", True, (200, 200, 200))
                
                # Dibujar textos
                pantalla.blit(txt, (pantalla.get_width()//2 - txt.get_width()//2, pantalla.get_height()//2 - 60))
                pantalla.blit(sub_txt, (pantalla.get_width()//2 - sub_txt.get_width()//2, pantalla.get_height()//2 + 20))
                
                pygame.display.flip()
                
                # Pequeña pausa para el parpadeo 
                tiempo_espera = pygame.time.get_ticks() + 500
                while pygame.time.get_ticks() < tiempo_espera:
                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            pygame.quit()
                            return
                
            # 2. Quitar al jugador de la lista
            self.jugadores.pop(self.turno_actual)

            # 3. Verificar si no quedan jugadores
            if len(self.jugadores) == 0:
                print("Todos han reprobado. Fin del semestre.")
                self.corriendo = False
                return

            # 4. Ajustar el turno para el siguiente sobreviviente
            self.turno_actual %= len(self.jugadores)
            print(f"DEBUG: {nombre_reprobado} eliminado. El semestre continúa.")
            return
    
        # 5. COMPROBACIÓN DE VICTORIA
        if jugador.vueltas >= 1:
            print(f"¡FELICIDADES {jugador.nombre.upper()}! HAS PASADO EL SEMESTRE.")
            print("🏆"*20)
            
            # Dibujar pantalla de victoria
            pantalla.fill((255, 255, 255))
            fuente_vic = pygame.font.SysFont("Arial", 50, bold=True)
            txt = fuente_vic.render(f"¡GANADOR: {jugador.nombre}!", True, (0, 150, 0))
            pantalla.blit(txt, (ANCHO//2 - txt.get_width()//2, ALTO//2 - 50))
            pygame.display.flip()
            
            time.sleep(5) # Pausa para ver el resultado
            self.jugando = False # Detiene el bucle principal
            return 

        # 5. CAMBIAR TURNO (Solo si nadie ha ganado aún)
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)

    def correr(self):
        self.mostrar_pantalla_inicio()

        while self.jugando:
            # 1. PROCESAR EVENTOS
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.jugando = False
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        self.mover_jugador() 

            # 2. DIBUJAR TODO
            self.pantalla.fill(COLOR_FONDO) 
            self.dibujar_tablero()
            self.dibujar_jugadores()
            self.dibujar_interfaz()
            
            # 3. ACTUALIZAR PANTALLA
            pygame.display.flip()
            
            # 4. CONTROL DE VELOCIDAD
            pygame.time.Clock().tick(30) 

        pygame.quit()

if __name__ == "__main__":
    juego = JuegoGrafico()
    juego.correr()
