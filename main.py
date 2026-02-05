import pygame
import sys
from estructuras import Tablero
from entidades import Jugador
from minijuegos import Minijuegos
from constantes import *

class JuegoGrafico:
    def __init__(self):
        pygame.init() #Aseguramos que se inicie
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(TITULO_VENTANA)

        try:
            icono = pygame.image.load(RUTA_FICHA_J1)
            pygame.display.set_icon(icono)
        except Exception as e:
            print(f"No se pudo cargar el icono: {e}")
        
        self.reloj = pygame.time.Clock()

        self.fuente = pygame.font.SysFont("Arial", 16)
        self.fuente_grande = pygame.font.SysFont("Arial", 24, bold=True)
        self.fuente_titulo = pygame.font.SysFont("Arial", 36, bold=True)
        self.fuente_pequena = pygame.font.SysFont("Arial", 14)
        self.fuente_gigante = pygame.font.SysFont("Arial", 70, bold=True)
        self.img_evil_boris = None
        self.img_good_boris = None
        
        self.fondo_victoria = None 
        try:
            print("Cargando fondo de victoria...")
            # Usamos .convert() porque los fondos usualmente no necesitan transparencia
            img_temp = pygame.image.load(RUTA_FONDO_VICTORIA).convert()
            # Escalamos la imagen para que cubra exactamente toda la pantalla (ANCHO y ALTO están en constantes)
            self.fondo_victoria = pygame.transform.scale(img_temp, (ANCHO, ALTO))
        except Exception as e:
            print(f"ADVERTENCIA: No se pudo cargar la imagen de victoria. Se usará color sólido. Error: {e}")
        
        try:
            print("Cargando música de fondo...")
            pygame.mixer.music.load(RUTA_MUSICA)       # 1. Cargar el archivo
            pygame.mixer.music.set_volume(VOLUMEN_MUSICA) # 2. Ajustar volumen
            pygame.mixer.music.play(-1)                # 3. Reproducir en bucle infinito (-1)
        except Exception as e:
            print(f"ADVERTENCIA: No se pudo cargar la música '{RUTA_MUSICA}'. Error: {e}")

        self.sonido_error = None
        try:
            self.sonido_error = pygame.mixer.Sound(RUTA_SONIDO_ERROR)
            self.sonido_error.set_volume(0.4) 
        except Exception as e:
            print(f"No se pudo cargar el sonido de error: {e}")

        try:
            img_temp = pygame.image.load(RUTA_GOOD_BORIS).convert_alpha()
            # Escalamos igual que la otra (ej. 180x180)
            self.img_good_boris = pygame.transform.scale(img_temp, (180, 180))
        except Exception as e:
            print(f"ADVERTENCIA: No se pudo cargar {RUTA_GOOD_BORIS}. Error: {e}")

        try:
            # Convert alpha es importante si el PNG tiene transparencia
            img_temp = pygame.image.load(RUTA_EVIL_BORIS).convert_alpha()
            # Escalamos la imagen a un tamaño que quepa bien en la ventana modal (ej. 180x180)
            self.img_evil_boris = pygame.transform.scale(img_temp, (180, 180))
        except Exception as e:
            print(f"ADVERTENCIA: No se pudo cargar {RUTA_EVIL_BORIS}. El juego continuará sin ella. Error: {e}")

        try:
            print("Cargando imagen de fondo del tablero...")
            # 1. Cargar la imagen. .convert() es crucial para la velocidad en fondos sin transparencia
            img_temp = pygame.image.load(RUTA_FONDO_JUEGO).convert()
            # 2. Escalarla al tamaño exacto de la ventana (ANCHO, ALTO están en constantes)
            self.fondo_tablero = pygame.transform.scale(img_temp, (ANCHO, ALTO))
            # 3. Marcamos que la carga fue exitosa
            self.usar_imagen_fondo = True
        except Exception as e:
            print(f"ADVERTENCIA: No se pudo cargar '{RUTA_FONDO_JUEGO}'. Usando color sólido. Error: {e}")
            # Si falla, marcamos como falso y el juego usará COLOR_FONDO
            self.usar_imagen_fondo = False

        self.tablero = Tablero()
        self.generar_mapa_cuadrado()
        self.jugadores = [
            Jugador("Jugador1", 1, self.tablero.inicio, RUTA_FICHA_J1),
            Jugador("Jugador2", 2, self.tablero.inicio, RUTA_FICHA_J2)
        ]

        self.tumbas = []
        self.turno_actual = 0
        self.corriendo = True
        # DEFINIR EL ARCHIVO DE LOG
        self.archivo_log = ARCHIVO_LOG

        # Forzamos la vida inicial a 40 para el semestre
        for j in self.jugadores:
            j.vida = 40
            
        self.minijuegos = Minijuegos(self.img_evil_boris, self.img_good_boris, self.sonido_error)
        self.jugando = True  

    def mostrar_pantalla_inicio(self):
        try:
            fondo = pygame.image.load(RUTA_PORTADA).convert()
            fondo = pygame.transform.scale(fondo, (ANCHO, ALTO)) # tamaño de la pantalla
        except pygame.error as e:
            print(f"Error al cargar la imagen de fondo: {e}")
            fondo = pygame.Surface((ANCHO, ALTO))
            fondo.fill((40, 40, 40)) 
        
        # Fuente para el botón y el título
        fuente_titulo = pygame.font.SysFont("Arial", 70, bold=True)
        fuente_boton = pygame.font.SysFont("Arial", 40, bold=True)
        
        # Colores
        COLOR_BOTON = COLOR_BOTON_JUGAR
        COLOR_TEXTO_BOTON = BLANCO 
        
        # Rectángulo para el botón "Jugar"
        rect_boton = pygame.Rect(ANCHO //2 - 100, 600, 200, 70) # x, y, ancho, alto

        esperando_inicio = True
        while esperando_inicio:
            #Controlar FPS
            self.reloj.tick(FPS)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
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
        ancho_util = ANCHO - (MARGEN_X * 2)
        alto_util = ALTO - 350
        
        # Posiciones de los "Exámenes" (Minijuegos) en las casillas 
        pos_minijuegos = [2, 5, 10]

        # Posiciones para preguntas Bonus 
        pos_peligro = [3, 7, 9]
        
        # Lista de coordenadas para las 12 casillas (ID 0 al 11)
        puntos = []
        
        for i in range(4):
            puntos.append((MARGEN_X + i * (ancho_util // 3), MARGEN_Y))
        
        # Derecha (2 casillas: 4, 5)
        for i in range(1, 3):
            puntos.append((ANCHO - MARGEN_X, MARGEN_Y + i * (alto_util // 3)))
            
        # Inferior (4 casillas: 6, 7, 8, 9) en reversa
        for i in range(4):
            puntos.append((ANCHO - MARGEN_X - i * (ancho_util // 3), MARGEN_Y + alto_util))
            
        # Izquierda (2 casillas: 10, 11) en reversa
        for i in range(1, 3):
            puntos.append((MARGEN_X, MARGEN_Y + alto_util - i * (alto_util // 3)))

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
            pygame.draw.line(self.pantalla, BORDE_TABLERO, (actual.x, actual.y), (sig.x, sig.y), 4)
            actual = sig

        # Dibujar círculos con borde
        actual = self.tablero.inicio
        for _ in range(self.tablero.tamano):
            # Color según el tipo
            if actual.tipo == "Minijuego":
                color = DORADO_CASILLA # Dorado
            elif actual.tipo == "Peligro":
                color = ROJO_PELIGRO  # Rojo 
            else:
                color = AZUL_CASILLA # Azul
            
            # Sombra/Borde para dar profundidad
            pygame.draw.circle(self.pantalla, COLOR_BRILLO, (actual.x, actual.y), RADIO_NODO + 3) # Brillo exterior
            pygame.draw.circle(self.pantalla, color, (actual.x, actual.y), RADIO_NODO)           # Casilla
            pygame.draw.circle(self.pantalla, NEGRO, (actual.x, actual.y), RADIO_NODO, 2)    # Contorno
            
            # ID de la casilla
            id_txt = self.fuente_pequena.render(str(actual.id), True, BLANCO)
            self.pantalla.blit(id_txt, (actual.x - id_txt.get_width()//2, actual.y - id_txt.get_height()//2))
            actual = actual.siguiente

        # DIBUJAR TUMBAS DE REPROBADOS
        for tx, ty in self.tumbas:
            pygame.draw.circle(self.pantalla, COLOR_TEXTO, (tx, ty), 15)
            #miau acá abajo
            fuente_tumba = pygame.font.SysFont("Arial", 20, bold=True)
            txt_x = fuente_tumba.render("X", True, (200, 200, 200))
            self.pantalla.blit(txt_x, (tx - txt_x.get_width()//2, ty - txt_x.get_height()//2))

    def dibujar_jugadores(self):
        for i, jug in enumerate(self.jugadores):
            # i*10 para que no se tapen exactamente si están en la misma casilla
            pos_x = jug.casilla_actual.x + (i * 15 - 7) 
            pos_y = jug.casilla_actual.y - 30 
            
            x_img = pos_x - (TAMANO_FICHA // 2)
            y_img = pos_y - (TAMANO_FICHA // 2)

            if hasattr(jug, 'imagen'):
                self.pantalla.blit(jug.imagen, (x_img, y_img))
            else:
                color_ficha = COLOR_JUGADOR_1 if i == 0 else COLOR_JUGADOR_2
                pygame.draw.circle(self.pantalla, color_ficha, (pos_x, pos_y), RADIO_FICHA)
                pygame.draw.circle(self.pantalla, (0, 0, 0), (pos_x, pos_y), RADIO_FICHA, 2)

    def dibujar_interfaz(self):
        
        if hasattr(self, 'ultimo_valor_dado'):
            rect_dado = pygame.Rect(ANCHO // 2 - 50, ALTO // 2 - 50, 100, 100)
            
            # Sombra del dado
            pygame.draw.rect(self.pantalla, BORDE_TABLERO, rect_dado.move(4, 4), border_radius=15) #OJO 200 200 200
            # Cuerpo del dado
            pygame.draw.rect(self.pantalla, BLANCO, rect_dado, border_radius=15)
            
            # Color del borde y número según el turno actual
            color_turno = COLOR_JUGADOR_1 if self.turno_actual == 0 else COLOR_JUGADOR_2 # Rojo o Verde
            pygame.draw.rect(self.pantalla, color_turno, rect_dado, 4, border_radius=15)
            
            # Dibujar el número
            val_txt = self.fuente_titulo.render(str(self.ultimo_valor_dado), True, color_turno)
            pos_x = ANCHO // 2 - val_txt.get_width() // 2
            pos_y = ALTO // 2 - val_txt.get_height() // 2
            self.pantalla.blit(val_txt, (pos_x, pos_y))
            
            # Texto pequeño que dice "DADO"
            txt_dado = self.fuente_pequena.render("DADO", True, GRIS_TEXTO_SECUNDARIO) #pilas es 100 100 100
            self.pantalla.blit(txt_dado, (ANCHO // 2 - txt_dado.get_width() // 2, ALTO // 2 + 55))

        # 3. PANEL INFERIOR 
        pygame.draw.rect(self.pantalla, BLANCO, (0, ALTO - 120, ANCHO, 120))
        pygame.draw.line(self.pantalla, BORDE_TABLERO, (0, ALTO - 120), (ANCHO, ALTO - 120), 2) #pilas es 200 200 200

        # 4. ESTADO DEL JUGADOR (Izquierda)
        if self.jugadores:
            jugador_activo = self.jugadores[self.turno_actual]
            info_txt = f"Turno de: {jugador_activo.nombre} | Nota: {jugador_activo.vida}"
            txt_render = self.fuente_grande.render(info_txt, True, AZUL_CASILLA)
            self.pantalla.blit(txt_render, (50, ALTO - 75))
        else:
            txt_fin = self.fuente_grande.render("¡SEMESTRE TERMINADO!", True, ROJO_PELIGRO)
            self.pantalla.blit(txt_fin, (50, ALTO - 75))

        # 6. INSTRUCCIONES (A la derecha en el panel inferior)
        x_inst = 800
        inst_lineas = [
            "Instrucciones:", 
                               "- [ESPACIO]: Lanzar dado.",
                               "- Casilla Dorada: Minijuego.",
                               "- Casiila Roja: Pregunta Bonus."
                               "- Gana en dar primero una vuelta."
                               
        ]
        for i, linea in enumerate(inst_lineas):
            f = self.fuente_grande if i == 0 else self.fuente_pequena
            color = NEGRO if i == 0 else GRIS_TEXTO_SECUNDARIO
            texto = f.render(linea, True, color)
            self.pantalla.blit(texto, (x_inst, ALTO - 110 + (i * 22)))
    def actualizar_pantalla_completa(self):
        """Método auxiliar para dibujar todo el escenario (Fondo + Tablero + Jugadores + Interfaz)"""
        # 1. DIBUJAR FONDO (Imagen o Color)
        if self.usar_imagen_fondo:
            self.pantalla.blit(self.fondo_tablero, (0, 0))
        else:
            self.pantalla.fill(COLOR_FONDO)
            
        # 2. DIBUJAR ELEMENTOS DEL JUEGO
        self.dibujar_tablero()
        self.dibujar_jugadores()
        self.dibujar_interfaz()
        
        # 3. MOSTRAR CAMBIOS
        pygame.display.flip()

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
        self.actualizar_pantalla_completa()
        
        # 3. LÓGICA DE CASILLA ESPECIAL
        casilla_final = jugador.casilla_actual 
        tipo_detectado = casilla_final.tipo.strip() 
        print(f"DEBUG: {jugador.nombre} en Casilla {casilla_final.id} ({tipo_detectado})")

        if tipo_detectado == "Minijuego":
            time.sleep(0.5) 
            print(f" Minijuego Iniciado")
            opcion = random.choice(["Trivia", "Dado"])
            
            if opcion == "Trivia":
                self.minijuegos.jugar_trivia(jugador, self.pantalla) 
            else:
                self.minijuegos.lanzar_dado(jugador, self.pantalla)

        elif tipo_detectado == "Peligro": 
            time.sleep(0.5)
            print(f" Casilla de Peligro Activada")
            self.minijuegos.reto_peligro(jugador, self.pantalla)
            
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
                color = ROJO_PELIGRO if i % 2 == 0 else NEGRO
                self.pantalla.fill(color)
                
                # PILAS fuente_derrota = pygame.font.SysFont("Arial", 50, bold=True)

                txt = self.fuente_gigante.render(f"¡{nombre_reprobado} fue reprobado por BORIS", True, BLANCO)
                sub_txt = self.fuente_grande.render("Dirigiéndolo a segunda..", True, GRIS_TEXTO_SECUNDARIO)
                
                # Dibujar textos
                self.pantalla.blit(txt, (ANCHO//2 - txt.get_width()//2, ALTO//2 - 60)) #self.pantalla.get_width()//2 - txt.get_width()//2
                self.pantalla.blit(sub_txt, (ANCHO//2 - sub_txt.get_width()//2, ALTO//2 + 20))
                
                pygame.display.flip()
                
                # Pequeña pausa para el parpadeo 
                tiempo_espera = pygame.time.get_ticks() + 500
                while pygame.time.get_ticks() < tiempo_espera:
                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit() #PILAS
                            return
                
            # 2. Quitar al jugador de la lista
            self.jugadores.pop(self.turno_actual)

            # 3. Verificar si no quedan jugadores
            if len(self.jugadores) == 0:
                print("Nadie escapó de BORIS. El semestre termina sin ganadores.")
                self.jugando = False #self.corriendo = False
                return

            # 4. Ajustar el turno para el siguiente sobreviviente
            self.turno_actual %= len(self.jugadores)
            print(f"DEBUG: {nombre_reprobado} eliminado por BORIS.")
            return
    
        # 5. COMPROBACIÓN DE VICTORIA
        if jugador.vueltas >= 1:
            print(f"{jugador.nombre.upper()} ¡SOBREVIVISTE A BORIS Y PASASTE EDA!")
            
            if self.fondo_victoria:
                # Si la imagen cargó correctamente, la dibujamos en (0,0)
                self.pantalla.blit(self.fondo_victoria, (0, 0))
            else:
                #Si falló la carga de la imagen, usamos el fondo blanco clásico
                self.pantalla.fill(BLANCO)
            
            txt = self.fuente_gigante.render(f"¡GANADOR: {jugador.nombre}!", True, BLANCO)
            self.pantalla.blit(txt, (ANCHO//2 - txt.get_width()//2, ALTO//2 - 50))
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

            self.actualizar_pantalla_completa()
            
            # 4. CONTROL DE VELOCIDAD
            self.reloj.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    juego = JuegoGrafico()
    juego.correr()