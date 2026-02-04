import pygame
import random
import sys

# Mantenemos tu Nodo de Árbol (Requisito: Árboles)
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
        self.fuente = pygame.font.SysFont("Arial", 22, bold=True)

    def _generar_arbol_trivia(self):
        """Genera árboles de decisión con preguntas técnicas de Estructuras de Datos"""
        
        # --- OPCIÓN A: Enfoque en ÁRBOLES BINARIOS ---
        raiz_a = NodoPregunta("¿Un arbol binario puede tener maximo 2 hijos?", "s")
        raiz_a.derecha = NodoPregunta("¿El nodo sin hijos se llama 'hoja'?", "s")
        raiz_a.izquierda = NodoPregunta("¿La 'raiz' es el nodo final del arbol?", "n")

        # --- OPCIÓN B: Enfoque en GRAFOS ---
        raiz_b = NodoPregunta("¿Los grafos pueden tener ciclos?", "s")
        raiz_b.derecha = NodoPregunta("¿Un grafo dirigido tiene flechas con sentido?", "s")
        raiz_b.izquierda = NodoPregunta("¿Un grafo solo puede tener 5 nodos?", "n")

        # --- OPCIÓN C: Recorridos y Propiedades ---
        raiz_c = NodoPregunta("¿El recorrido In-orden se usa en arboles?", "s")
        raiz_c.derecha = NodoPregunta("¿Un grafo no dirigido usa matrices de adyacencia?", "s")
        raiz_c.izquierda = NodoPregunta("¿En un arbol binario, el hijo izquierdo es mayor que el padre?", "n")

        # --- OPCIÓN D: Terminología Avanzada ---
        raiz_d = NodoPregunta("¿Un arbol es un tipo especial de grafo?", "s")
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
        rect_ventana = pygame.Rect(150, 150, 700, 500) 
        botón_rect = pygame.Rect(400, 450, 200, 60)
        esperando_clic = True
        
        # Colores
        AZUL_NORMAL = (59, 130, 246)
        AZUL_HOVER = (37, 99, 235) # Un azul más oscuro para el hover
        DORADO = (245, 158, 11)

        while esperando_clic:
            # 1. CAPTURAR POSICIÓN DEL MOUSE PARA El BOTÓN
            mouse_pos = pygame.mouse.get_pos()
            color_boton = AZUL_HOVER if botón_rect.collidepoint(mouse_pos) else AZUL_NORMAL

            # 2. DIBUJAR UNA SOLA VEZ 
            # Fondo oscuro semitransparente (solo una vez por frame)
            overlay = pygame.Surface((1000, 800), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            pantalla.blit(overlay, (0, 0))

            # Dibujar el cuadro grande de la ventana
            pygame.draw.rect(pantalla, (255, 255, 255), rect_ventana, border_radius=20)
            pygame.draw.rect(pantalla, DORADO, rect_ventana, 6, border_radius=20)

            # Título y Mensaje
            titulo = self.fuente.render(" EXAMEN DE SUERTE: EL DADO", True, (30, 41, 59))
            instruccion = self.fuente.render("¡Presiona el botón para lanzar tu destino!", True, (71, 85, 105))
            
            pantalla.blit(titulo, (rect_ventana.centerx - titulo.get_width()//2, rect_ventana.y + 60))
            pantalla.blit(instruccion, (rect_ventana.centerx - instruccion.get_width()//2, rect_ventana.y + 150))

            # Dibujar el Botón con efecto Hover (Para que sea de otro color el botón si se pasa el ratón por ahí)
            pygame.draw.rect(pantalla, color_boton, botón_rect, border_radius=12)
            txt_boton = self.fuente.render("GIRAR DADO", True, (255, 255, 255))
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
            pygame.draw.rect(pantalla, (255, 255, 255), rect_ventana, border_radius=20)
            pygame.draw.rect(pantalla, DORADO, rect_ventana, 6, border_radius=20)
            
            # Texto de "Lanzando"
            txt_anim = self.fuente.render(f" Lanzando... {num_temp}", True, DORADO)
            pantalla.blit(txt_anim, (rect_ventana.centerx - txt_anim.get_width()//2, rect_ventana.centery - 20))
            
            pygame.display.flip()
            pygame.time.delay(120) # Aumentamos el tiempo a 120ms para que se vea mejor

        # Resultado
        dado_final = random.randint(1, 8)
        ganó = (dado_final % 2 == 0)
        puntos = 15 if ganó else -15
        jugador.modificar_vida(puntos)

        # Limpiar y mostrar resultado
        pygame.draw.rect(pantalla, (255, 255, 255), rect_ventana, border_radius=20)
        pygame.draw.rect(pantalla, DORADO, rect_ventana, 6, border_radius=20)
        
        res_txt = self.fuente.render(f"¡SALIÓ UN {dado_final}!", True, (30, 41, 59))
        sub_txt = self.fuente.render(f"{'¡APROBASTE!' if ganó else '¡REPROBASTE!'} ({puntos} pts)", True, (16, 185, 129) if ganó else (239, 68, 68))
        
        pantalla.blit(res_txt, (rect_ventana.centerx - res_txt.get_width()//2, rect_ventana.centery - 40))
        pantalla.blit(sub_txt, (rect_ventana.centerx - sub_txt.get_width()//2, rect_ventana.centery + 30))
        
        pygame.display.flip()
        self.guardar_resultado(jugador, "Dado", "Gano" if ganó else "Perdio")
        pygame.time.delay(3000) # Tiempo extendido para leer el resultado

    # MINIJUEGO 2 - LA TRIVIA 

    def jugar_trivia(self, jugador, pantalla):

        self.raiz_trivia = self._generar_arbol_trivia()
        actual = self.raiz_trivia
        aciertos = 0

        rect_ventana = pygame.Rect(150, 150, 700, 500)
        
        # Colores temáticos
        GRIS_OSCURO = (30, 41, 59)
        VERDE_EXITO = (16, 185, 129)
        ROJO_ERROR = (239, 68, 68)
        DORADO = (245, 158, 11)

        while actual:
            # 1. DIBUJAR INTERFAZ DE PREGUNTA
            overlay = pygame.Surface((1000, 800), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            pantalla.blit(overlay, (0, 0))

            pygame.draw.rect(pantalla, (255, 255, 255), rect_ventana, border_radius=20)
            pygame.draw.rect(pantalla, DORADO, rect_ventana, 6, border_radius=20)

            # Textos: Encabezado y Pregunta
            titulo = self.fuente.render(f"EXAMEN TEÓRICO (Aciertos: {aciertos})", True, DORADO)
            pregunta_txt = self.fuente.render(actual.pregunta, True, GRIS_OSCURO)
            
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
        pygame.draw.rect(pantalla, (255, 255, 255), rect_ventana, border_radius=20)
        pygame.draw.rect(pantalla, DORADO, rect_ventana, 6, border_radius=20)
        
        fin_txt = self.fuente.render("EXAMEN FINALIZADO", True, GRIS_OSCURO)
        puntos_txt = self.fuente.render(f"Puntaje obtenido: +{puntos} de promedio", True, VERDE_EXITO)
        
        pantalla.blit(fin_txt, (rect_ventana.centerx - fin_txt.get_width()//2, rect_ventana.centery - 40))
        pantalla.blit(puntos_txt, (rect_ventana.centerx - puntos_txt.get_width()//2, rect_ventana.centery + 20))
        
        pygame.display.flip()
        self.guardar_resultado(jugador, "Trivia", f"{aciertos} aciertos")
        pygame.time.delay(3000)

    # MINIJUEGO 3 
        
    def reto_peligro(self, jugador, pantalla):
        """Reto de alta dificultad enfocado 100% en MST (Prim y Kruskal)"""
        # Esta línea DEBE tener 8 espacios (o 2 tabs) desde el borde izquierdo
        rect_ventana = pygame.Rect(150, 150, 700, 500)
        
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
            pygame.draw.rect(pantalla, (255, 255, 255), rect_ventana, border_radius=20)
            pygame.draw.rect(pantalla, (220, 38, 38), rect_ventana, 6, border_radius=20)
            
            txt_pregunta = self.fuente.render(pregunta, True, (30, 41, 59))
            pantalla.blit(txt_pregunta, (rect_ventana.centerx - txt_pregunta.get_width()//2, rect_ventana.centery - 20))
            
            instrucciones = self.fuente.render("[S] para VERDADERO | [N] para FALSO", True, (100, 100, 100))
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
                            self.dibujar_ventana_emergente(pantalla, "¡EXPERTO EN GRAFOS!", "Has dominado el algoritmo.")
                        else:
                            jugador.modificar_vida(-25)
                            self.dibujar_ventana_emergente(pantalla, "¡FALLASTE", "Te confundiste de algoritmo: -25 pts.")
                        
                        pygame.display.flip()
                        self.guardar_resultado(jugador, "Reto Peligro", "Aprobo" if res_usuario == respuesta_correcta else "Reprobo")
                        pygame.time.delay(2500)
                        esperando = False

    def dibujar_ventana_emergente(self, pantalla, titulo, subtitulo):
        # 1. Definir el área
        rect_ventana = pygame.Rect(150, 150, 700, 500)
        
        # 2. Dibujar fondo blanco y borde oscuro
        pygame.draw.rect(pantalla, (255, 255, 255), rect_ventana, border_radius=20)
        pygame.draw.rect(pantalla, (30, 41, 59), rect_ventana, 6, border_radius=20)

        # 3. Renderizar y centrar el Título
        txt_titulo = self.fuente.render(titulo, True, (30, 41, 59))
        pantalla.blit(txt_titulo, (rect_ventana.centerx - txt_titulo.get_width()//2, rect_ventana.y + 80))

        # 4. Renderizar y centrar el Subtítulo (Pregunta o descripción)
        txt_sub = self.fuente.render(subtitulo, True, (70, 70, 70))
        pantalla.blit(txt_sub, (rect_ventana.centerx - txt_sub.get_width()//2, rect_ventana.centery))
        
        pygame.display.flip()
