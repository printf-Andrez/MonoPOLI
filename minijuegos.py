import pygame
import random
import sys
from constantes import *

# Requisito: Árboles
class NodoPregunta:
    def __init__(self, pregunta, respuesta_correcta):
        self.pregunta = pregunta
        self.respuesta_correcta = respuesta_correcta
        self.derecha = None  
        self.izquierda = None 

class Minijuegos:
    def __init__(self, img_evil_boris=None, img_good_boris=None, sonido_error=None):
        self.raiz_trivia = self._generar_arbol_trivia()
        self.archivo_log = ARCHIVO_LOG_MINIJUEGOS
        self.fuente = pygame.font.SysFont("Arial", 22, bold=True)
        self.img_evil_boris = img_evil_boris
        self.img_good_boris = img_good_boris
        self.sonido_error = sonido_error

    def _generar_arbol_trivia(self):
        """Genera árboles de decisión con preguntas técnicas de Estructuras de Datos"""
        
        # --- OPCIÓN A: Enfoque en ÁRBOLES BINARIOS ---
        raiz_a = NodoPregunta("¿Un árbol binario puede tener máximo 2 hijos?", "s")
        raiz_a.derecha = NodoPregunta("¿El nodo sin hijos se llama 'hoja'?", "s")
        raiz_a.izquierda = NodoPregunta("¿La 'raíz' es el nodo final del árbol?", "n")

        # --- OPCIÓN B: Enfoque en GRAFOS ---
        raiz_b = NodoPregunta("¿Los grafos pueden tener ciclos?", "s")
        raiz_b.derecha = NodoPregunta("¿Un grafo dirigido tiene flechas con sentido?", "s")
        raiz_b.izquierda = NodoPregunta("¿Un grafo solo puede tener 5 nodos?", "n")

        # --- OPCIÓN C: Recorridos y Propiedades ---
        raiz_c = NodoPregunta("¿El recorrido In-orden se usa en árboles?", "s")
        raiz_c.derecha = NodoPregunta("¿Un grafo no dirigido usa matrices de adyacencia?", "s")
        raiz_c.izquierda = NodoPregunta("¿En un árbol binario, el hijo izquierdo es mayor que el padre?", "n")

        # --- OPCIÓN D: Terminología Avanzada ---
        raiz_d = NodoPregunta("¿Un árbol es un tipo especial de grafo?", "s")
        raiz_d.derecha = NodoPregunta("¿Un grafo completo conecta todos sus nodos entre si?", "s")
        raiz_d.izquierda = NodoPregunta("¿El grado de un nodo es siempre cero?", "n")

        # Retornamos una de las cuatro opciones al azar
        return random.choice([raiz_a, raiz_b, raiz_c, raiz_d])
    
    def guardar_resultado(self, jugador, minijuego, resultado):
        """Guarda los datos del minijuego en un archivo de texto"""
        try:
            with open(self.archivo_log, "a") as f:
                f.write(f"Jugador: {jugador.nombre} | Juego: {minijuego} | Resultado: {resultado} | Nota: {jugador.vida}\n")
        except Exception as e:
            print(f"Error al guardar el historial: {e}")
    
    # MINIJUEGO 1 - LANZAR EL DADO 

    def lanzar_dado(self, jugador, pantalla):
        # Configuraciones de la ventana y botón
        rect_ventana = pygame.Rect(RECT_VENTANA_MODAL) 
        botón_rect = pygame.Rect(RECT_BOTON_DADO)
        esperando_clic = True
        
        while esperando_clic:
            # 1. CAPTURAR POSICIÓN DEL MOUSE PARA El BOTÓN
            mouse_pos = pygame.mouse.get_pos()
            color_boton = AZUL_HOVER if botón_rect.collidepoint(mouse_pos) else AZUL_BOTON

            # 2. DIBUJAR UNA SOLA VEZ 
            # Fondo oscuro semitransparente (solo una vez por frame)
            overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            overlay.fill(COLOR_OVERLAY)
            pantalla.blit(overlay, (0, 0))

            # Dibujar el cuadro grande de la ventana
            pygame.draw.rect(pantalla, BLANCO, rect_ventana, border_radius=20)
            pygame.draw.rect(pantalla, DORADO_CASILLA, rect_ventana, 6, border_radius=20)

            # Título y Mensaje
            titulo = self.fuente.render(" PRUEBA SORPRESA: EL DADO", True, COLOR_TEXTO)
            instruccion = self.fuente.render("Lanza el dado. Boris no tendrá piedad", True, GRIS_TEXTO_CLARO)
            
            pantalla.blit(titulo, (rect_ventana.centerx - titulo.get_width()//2, rect_ventana.y + 60))
            pantalla.blit(instruccion, (rect_ventana.centerx - instruccion.get_width()//2, rect_ventana.y + 150))

            # Dibujar el Botón con efecto Hover (Para que sea de otro color el botón si se pasa el ratón por ahí)
            pygame.draw.rect(pantalla, color_boton, botón_rect, border_radius=12)
            txt_boton = self.fuente.render("GIRAR DADO", True, BLANCO)
            pantalla.blit(txt_boton, (botón_rect.centerx - txt_boton.get_width()//2, botón_rect.centery - txt_boton.get_height()//2))

            pygame.display.flip()

            # 3. EVENTOS
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if botón_rect.collidepoint(evento.pos):
                        esperando_clic = False 

        # Acá es para que se vea una pequeña animación
        for i in range(15): # Más pasos de animación
            num_temp = random.randint(1, 8)
            # Reutilizamos el dibujo para que no parpadee
            pygame.draw.rect(pantalla, BLANCO, rect_ventana, border_radius=20)
            pygame.draw.rect(pantalla, DORADO_CASILLA, rect_ventana, 6, border_radius=20)
            
            # Texto de "Lanzando"
            txt_anim = self.fuente.render(f" Lanzando... {num_temp}", True, DORADO_CASILLA)
            pantalla.blit(txt_anim, (rect_ventana.centerx - txt_anim.get_width()//2, rect_ventana.centery - 20))
            
            pygame.display.flip()
            pygame.time.delay(120) # Aumentamos el tiempo a 120ms para que se vea mejor

        # Resultado
        dado_final = random.randint(1, 8)
        ganó = (dado_final % 2 == 0)
        puntos = 15 if ganó else -15
        jugador.modificar_vida(puntos)

        # Limpiar y mostrar resultado
        pygame.draw.rect(pantalla, BLANCO, rect_ventana, border_radius=20)
        pygame.draw.rect(pantalla, DORADO_CASILLA, rect_ventana, 6, border_radius=20)
        
        imagen_mostrar = None
        if ganó and self.img_good_boris:
            imagen_mostrar = self.img_good_boris
        elif not ganó and self.img_evil_boris:
            imagen_mostrar = self.img_evil_boris
            if self.sonido_error:
                self.sonido_error.play()

        if imagen_mostrar:
            img_x = rect_ventana.centerx - imagen_mostrar.get_width() // 2
            img_y = rect_ventana.centery - 175 
            pantalla.blit(imagen_mostrar, (img_x, img_y))
        
        res_txt = self.fuente.render(f"¡SALIÓ UN {dado_final}!", True, COLOR_TEXTO)
        sub_txt = self.fuente.render(f"{'¡APROBASTE!' if ganó else '¡REPROBASTE!'} ({puntos} pts)", True, VERDE_EXITO if ganó else ROJO_ERROR)
        
        pantalla.blit(res_txt, (rect_ventana.centerx - res_txt.get_width()//2, rect_ventana.centery + 20))
        pantalla.blit(sub_txt, (rect_ventana.centerx - sub_txt.get_width()//2, rect_ventana.centery + 60))
        
        pygame.display.flip()
        self.guardar_resultado(jugador, "Dado", "Gano" if ganó else "Perdio")
        pygame.time.delay(3000) # Tiempo extendido para leer el resultado

    # MINIJUEGO 2 - LA TRIVIA 

    def jugar_trivia(self, jugador, pantalla):

        self.raiz_trivia = self._generar_arbol_trivia()
        actual = self.raiz_trivia
        aciertos = 0

        rect_ventana = pygame.Rect(RECT_VENTANA_MODAL)

        while actual:
            # 1. DIBUJAR INTERFAZ DE PREGUNTA
            overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            overlay.fill(COLOR_OVERLAY)
            pantalla.blit(overlay, (0, 0))

            pygame.draw.rect(pantalla, BLANCO, rect_ventana, border_radius=20)
            pygame.draw.rect(pantalla, DORADO_CASILLA, rect_ventana, 6, border_radius=20)

            # Textos: Encabezado y Pregunta
            titulo = self.fuente.render(f"EXAMEN TEÓRICO (Aciertos: {aciertos})", True, DORADO_CASILLA)
            pregunta_txt = self.fuente.render(actual.pregunta, True, COLOR_TEXTO)
            
            pantalla.blit(titulo, (rect_ventana.centerx - titulo.get_width()//2, rect_ventana.y + 50))
            pantalla.blit(pregunta_txt, (rect_ventana.centerx - pregunta_txt.get_width()//2, rect_ventana.centery - 20))

            # Instrucciones 
            inst_s = self.fuente.render("[S] para SI", True, VERDE_EXITO)
            inst_n = self.fuente.render("[N] para NO", True, ROJO_ERROR)
            pantalla.blit(inst_s, (rect_ventana.centerx - 150, rect_ventana.y + 350))
            pantalla.blit(inst_n, (rect_ventana.centerx + 50, rect_ventana.y + 350))

            pygame.display.flip()

            # 2. ESPERAR RESPUESTA CON FEEDBACK
            esperando = True
            while esperando:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    if evento.type == pygame.KEYDOWN:
                        res_usuario = ""
                        if evento.key == pygame.K_s: res_usuario = "s"
                        if evento.key == pygame.K_n: res_usuario = "n"

                        if res_usuario != "":
                            # EFECTO VISUAL DE RESPUESTA
                            es_correcta = (res_usuario == actual.respuesta_correcta)
                            color_flash = VERDE_EXITO if es_correcta else ROJO_ERROR
                            texto_flash = "¡CORRECTO!" if es_correcta else "¡INCORRECTO!"
                            
                            # Dibujar pequeño flash de color
                            pygame.draw.rect(pantalla, color_flash, rect_ventana, 10, border_radius=20)
                            msg_flash = self.fuente.render(texto_flash, True, color_flash)
                            pantalla.blit(msg_flash, (rect_ventana.centerx - msg_flash.get_width()//2, rect_ventana.y + 100))
                            pygame.display.flip()
                            pygame.time.delay(600) # Pausa corta para ver si acertó

                            if es_correcta:
                                aciertos += 1
                                actual = actual.derecha
                            else:
                                actual = actual.izquierda
                            esperando = False

        # 3. RESULTADO FINAL DEL EXAMEN
        puntos = aciertos * 10
        jugador.modificar_vida(puntos)
        
        # Limpiar cuadro para el final
        pygame.draw.rect(pantalla, BLANCO, rect_ventana, border_radius=20)
        pygame.draw.rect(pantalla, DORADO_CASILLA, rect_ventana, 6, border_radius=20)
        
        imagen_mostrar = None
        if aciertos == 0 and self.img_evil_boris:
            imagen_mostrar = self.img_evil_boris
            if self.sonido_error:
                self.sonido_error.play()
        elif aciertos > 0 and self.img_good_boris:
            imagen_mostrar = self.img_good_boris
            
        if imagen_mostrar:
            img_x = rect_ventana.centerx - imagen_mostrar.get_width() // 2
            img_y = rect_ventana.centery - 175 
            pantalla.blit(imagen_mostrar, (img_x, img_y))

        fin_txt = self.fuente.render("EXAMEN FINALIZADO", True, COLOR_TEXTO)
        puntos_txt = self.fuente.render(f"Puntaje obtenido: +{puntos} de promedio", True, VERDE_EXITO)
        
        pantalla.blit(fin_txt, (rect_ventana.centerx - fin_txt.get_width()//2, rect_ventana.centery + 20))
        pantalla.blit(puntos_txt, (rect_ventana.centerx - puntos_txt.get_width()//2, rect_ventana.centery + 60))
        
        pygame.display.flip()
        self.guardar_resultado(jugador, "Trivia", f"{aciertos} aciertos")
        pygame.time.delay(3000)

    # MINIJUEGO 3 
        
    def reto_peligro(self, jugador, pantalla):
        """Reto de alta dificultad enfocado 100% en MST (Prim y Kruskal)"""
        # Esta línea DEBE tener 8 espacios (o 2 tabs) desde el borde izquierdo
        rect_ventana = pygame.Rect(RECT_VENTANA_MODAL)
        
        # BANCO DE PREGUNTAS TÉCNICAS
        retos = [
            ("¿El algoritmo de Prim comienza desde un nodo arbitrario?", "s"),
            ("¿Kruskal selecciona aristas de menor peso sin formar ciclos?", "s"),
            ("¿Prim es generalmente mejor que Kruskal en grafos densos?", "s"),
            ("¿Prim utiliza una estructura Union-Find para detectar ciclos?", "s"),
            ("¿El algoritmo Prim es mejor para grafos dispersos (pocas aristas)?.", "n")
        ]
        
        pregunta, respuesta_correcta = random.choice(retos)

        # 1. Pantalla de Advertencia
        self.dibujar_ventana_emergente(pantalla, " ¡RETO DE ALGORITMOS!", "Si fallas, pierdes 25 pts de promedio.")
        pygame.display.flip()
        pygame.time.delay(2000)

        # 2. Bucle de respuesta
        esperando = True
        while esperando:
            pygame.draw.rect(pantalla, BLANCO, rect_ventana, border_radius=20)
            pygame.draw.rect(pantalla, ROJO_PELIGRO, rect_ventana, 6, border_radius=20)
            
            txt_pregunta = self.fuente.render(pregunta, True, COLOR_TEXTO)
            pantalla.blit(txt_pregunta, (rect_ventana.centerx - txt_pregunta.get_width()//2, rect_ventana.centery - 20))
            
            instrucciones = self.fuente.render("[S] para VERDADERO | [N] para FALSO", True, GRIS_TEXTO_SECUNDARIO)
            pantalla.blit(instrucciones, (rect_ventana.centerx - instrucciones.get_width()//2, rect_ventana.y + 350))
            
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    import sys
                    sys.exit()
                
                if evento.type == pygame.KEYDOWN:
                    res_usuario = ""
                    if evento.key == pygame.K_s: res_usuario = "s"
                    if evento.key == pygame.K_n: res_usuario = "n"

                    if res_usuario != "":
                        if res_usuario == respuesta_correcta:
                            self.dibujar_ventana_emergente(pantalla, "Respuesta Correcta", "Boris te felicita", imagen=self.img_good_boris)
                        else:
                            jugador.modificar_vida(-25)
                            self.dibujar_ventana_emergente(pantalla, "Respuesta Incorrecta", "Boris te hace bailar: -25 pts.", imagen=self.img_evil_boris)
                            if self.sonido_error:
                                self.sonido_error.play()
                        
                        pygame.display.flip()
                        self.guardar_resultado(jugador, "Reto Peligro", "Aprobo" if res_usuario == respuesta_correcta else "Reprobo")
                        pygame.time.delay(2500)
                        esperando = False

    def dibujar_ventana_emergente(self, pantalla, titulo, subtitulo, imagen=None):
        # 1. Definir el área
        rect_ventana = pygame.Rect(RECT_VENTANA_MODAL)
        
        # 2. Dibujar fondo blanco y borde oscuro
        pygame.draw.rect(pantalla, BLANCO, rect_ventana, border_radius=20)
        pygame.draw.rect(pantalla, COLOR_TEXTO, rect_ventana, 6, border_radius=20)

        # 3. Renderizar y centrar el Título
        txt_titulo = self.fuente.render(titulo, True, COLOR_TEXTO)
        pantalla.blit(txt_titulo, (rect_ventana.centerx - txt_titulo.get_width()//2, rect_ventana.y + 80))

        if imagen:
             # La ponemos centrada, desplazada un poco hacia arriba del centro
            img_x = rect_ventana.centerx - imagen.get_width() // 2
            img_y = rect_ventana.centery - 120 
            pantalla.blit(imagen, (img_x, img_y))
            
            # Si hay imagen, bajamos un poco el subtítulo
            pos_y_sub = rect_ventana.centery + 80
        else:
            pos_y_sub = rect_ventana.centery

        # 4. Renderizar y centrar el Subtítulo (Pregunta o descripción)
        txt_sub = self.fuente.render(subtitulo, True, GRIS_TEXTO_INFO)
        pantalla.blit(txt_sub, (rect_ventana.centerx - txt_sub.get_width()//2, pos_y_sub))
        
        pygame.display.flip()