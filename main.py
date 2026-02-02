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
        self.tablero = Tablero()
        self.generar_mapa_cuadrado()
        self.jugadores = [
            Jugador("DonLuis", 1, self.tablero.inicio),
            Jugador("Miguel", 2, self.tablero.inicio)
        ]
        self.minijuegos = Minijuegos()
        self.turno_actual = 0
        self.jugando = True  

    def generar_mapa_cuadrado(self):
        """Genera un tablero simétrico con 2 minijuegos por lado"""
        margen_x, margen_y = 100, 100
        ancho_util = ANCHO - (margen_x * 2)
        alto_util = ALTO - 250 # Espacio para la interfaz abajo
        
        # Definimos posiciones fijas para los minijuegos en cada lado (índices)
        pos_minijuegos = [2, 5, 9, 12, 16, 19, 23, 26] 
        contador = 0

        # Lado Superior
        for x in range(margen_x, ANCHO - margen_x + 1, ancho_util // 7):
            tipo = "Minijuego" if contador in pos_minijuegos else "Normal"
            self.tablero.anadir_casilla("C", tipo, x, margen_y)
            contador += 1
        
        # Lado Derecho
        for y in range(margen_y + (alto_util // 5), alto_util + margen_y, alto_util // 5):
            tipo = "Minijuego" if contador in pos_minijuegos else "Normal"
            self.tablero.anadir_casilla("C", tipo, ANCHO - margen_x, y)
            contador += 1
            
        # Lado Inferior
        for x in range(ANCHO - margen_x, margen_x - 1, -(ancho_util // 7)):
            tipo = "Minijuego" if contador in pos_minijuegos else "Normal"
            self.tablero.anadir_casilla("C", tipo, x, alto_util + margen_y)
            contador += 1
            
        # Lado Izquierdo
        for y in range(alto_util + margen_y - (alto_util // 5), margen_y, -(alto_util // 5)):
            tipo = "Minijuego" if contador in pos_minijuegos else "Normal"
            self.tablero.anadir_casilla("C", tipo, margen_x, y)
            contador += 1

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
            color = DORADO_CASILLA if actual.tipo == "Minijuego" else AZUL_CASILLA
            
            # Sombra/Borde para dar profundidad
            pygame.draw.circle(pantalla, (255, 255, 255), (actual.x, actual.y), 28) # Brillo exterior
            pygame.draw.circle(pantalla, color, (actual.x, actual.y), 25)           # Casilla
            pygame.draw.circle(pantalla, (0, 0, 0), (actual.x, actual.y), 25, 2)    # Contorno
            
            # ID de la casilla
            id_txt = fuente_pequena.render(str(actual.id), True, (255, 255, 255))
            pantalla.blit(id_txt, (actual.x - id_txt.get_width()//2, actual.y - id_txt.get_height()//2))
            actual = actual.siguiente

    def dibujar_jugadores(self):
        for i, jug in enumerate(self.jugadores):
            # i*10 para que no se tapen exactamente si están en la misma casilla
            pos_x = jug.casilla_actual.x + (i * 15 - 7) 
            pos_y = jug.casilla_actual.y - 30 
            
            color_ficha = (239, 68, 68) if i == 0 else (34, 197, 94) # Rojo y Verde vibrantes
            pygame.draw.circle(pantalla, color_ficha, (pos_x, pos_y), 12)
            pygame.draw.circle(pantalla, (0, 0, 0), (pos_x, pos_y), 12, 2)

    def dibujar_interfaz(self):
        # 1. TÍTULO SUPERIOR
        titulo_surf = fuente_titulo.render("MonoPOLI: La Aventura de Algoritmos", True, (40, 40, 40))
        # Lo ponemos a 10 píxeles del borde superior
        pantalla.blit(titulo_surf, (ANCHO // 2 - titulo_surf.get_width() // 2, 10))

        # 2. DADO VISUAL (Corregido para evitar números dobles)
        if hasattr(self, 'ultimo_valor_dado'):
            rect_dado = pygame.Rect(ANCHO // 2 - 50, ALTO // 2 - 50, 100, 100)
            
            # Sombra del dado
            pygame.draw.rect(pantalla, (200, 200, 200), rect_dado.move(4, 4), border_radius=15)
            # Cuerpo del dado
            pygame.draw.rect(pantalla, (255, 255, 255), rect_dado, border_radius=15)
            
            # Color del borde y número según el turno actual
            color_turno = (34, 197, 94) if self.turno_actual == 0 else (239, 68, 68) # Rojo o Verde
            pygame.draw.rect(pantalla, color_turno, rect_dado, 4, border_radius=15)
            
            # DIBUJAR EL NÚMERO (Solo una vez)
            val_txt = fuente_titulo.render(str(self.ultimo_valor_dado), True, color_turno)
            # Centramos perfectamente el número en el dado
            pos_x = ANCHO // 2 - val_txt.get_width() // 2
            pos_y = ALTO // 2 - val_txt.get_height() // 2
            pantalla.blit(val_txt, (pos_x, pos_y))
            
            # Texto pequeño que dice "DADO"
            txt_dado = fuente_pequena.render("DADO", True, (100, 100, 100))
            pantalla.blit(txt_dado, (ANCHO // 2 - txt_dado.get_width() // 2, ALTO // 2 + 55))

        # 3. PANEL INFERIOR (Tu código original de fondo blanco)
        pygame.draw.rect(pantalla, (255, 255, 255), (0, ALTO - 120, ANCHO, 120))
        pygame.draw.line(pantalla, (200, 200, 200), (0, ALTO - 120), (ANCHO, ALTO - 120), 2)

        # 4. ESTADO DEL JUGADOR (Izquierda)
        jugador_activo = self.jugadores[self.turno_actual]
        info_txt = f"Turno: {jugador_activo.nombre} | Puntaje: {jugador_activo.vida} / 70"
        txt_render = fuente_grande.render(info_txt, True, (33, 150, 243))
        pantalla.blit(txt_render, (50, ALTO - 75))

        # 5. CONTADOR DE VUELTAS (Arriba a la derecha)
        y_vueltas = 20
        for jug in self.jugadores:
            txt_v = fuente_pequena.render(f"Vueltas {jug.nombre}: {jug.vueltas}/15", True, (80, 80, 80))
            pantalla.blit(txt_v, (ANCHO - 180, y_vueltas))
            y_vueltas += 20

        # 6. INSTRUCCIONES (A la derecha en el panel inferior)
        x_inst = 600
        inst_lineas = [
            "Instrucciones:", 
                               "- [ESPACIO]: Lanzar dado.",
                               "- Casilla Dorada: Minijuego.",
                               "- Gana el primero con 70 pts."
        ]
        for i, linea in enumerate(inst_lineas):
            f = fuente_grande if i == 0 else fuente_pequena
            color = (0,0,0) if i == 0 else (100, 100, 100)
            texto = f.render(linea, True, color)
            pantalla.blit(texto, (x_inst, ALTO - 110 + (i * 22)))

    def mover_jugador(self):
        """Lógica de movimiento con comprobación de victoria inmediata"""
        import random
        import pygame
        import time # Necesario para la pausa de celebración
        
        # 1. LANZAMIENTO ÚNICO DE DADO
        valor_lanzado = random.randint(1, 4) 
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
        pygame.display.flip() # Crucial para ver el movimiento
        
        # 3. LÓGICA DE CASILLA ESPECIAL
        casilla_final = jugador.casilla_actual 
        
        # Limpiamos el texto por si hay espacios invisibles
        tipo_detectado = casilla_final.tipo.strip() 
        print(f"DEBUG: {jugador.nombre} en Casilla {casilla_final.id} ({tipo_detectado})")

        if tipo_detectado == "Minijuego":

            time.sleep(0.5) # Pequeña pausa antes de iniciar el minijuego

            print(f"✨ ¡MINIJUEGO ACTIVADO!")
            opcion = random.choice(["Trivia", "Dado"])
            if opcion == "Trivia":
                self.minijuegos.jugar_trivia(jugador)
            else:
                cambio = random.choice([-10, 5, 10, 15])
                jugador.modificar_vida(cambio)
        else:
            # SI ES AZUL (NORMAL), PASAMOS DIRECTO AL SIGUIENTE TURNO
            print(f"Casilla normal. Saltando lógica de minijuego.")

        self.dibujar_interfaz()
        pygame.display.flip()

        # 4. COMPROBACIÓN DE VICTORIA
        if jugador.vida >= 70:
            print("\n" + "🏆"*20)
            print(f"¡FELICIDADES {jugador.nombre.upper()}! HAS GANADO CON {jugador.vida} PUNTOS.")
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

        # 5. COMPROBACIÓN DE VUELTAS (EMPATE)
        if jugador.vueltas >= 15: 
            print("\n--- JUEGO TERMINADO POR LÍMITE DE VUELTAS (EMPATE) ---")
            self.jugando = False
            return

        # 6. CAMBIAR TURNO (Solo si nadie ha ganado aún)
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)

    def correr(self):
        """Bucle principal corregido para evitar que la ventana se cuelgue"""
        while self.jugando:
            # 1. PROCESAR EVENTOS (Esto evita el "No Responde")
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.jugando = False
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        self.mover_jugador() #

            # 2. DIBUJAR TODO
            pantalla.fill(COLOR_FONDO)
            self.dibujar_tablero()
            self.dibujar_jugadores()
            self.dibujar_interfaz()
            
            # 3. ACTUALIZAR PANTALLA
            pygame.display.flip()
            
            # 4. CONTROL DE VELOCIDAD (Opcional pero recomendado)
            pygame.time.Clock().tick(30) 

        pygame.quit()

if __name__ == "__main__":
    juego = JuegoGrafico()
    juego.correr()
