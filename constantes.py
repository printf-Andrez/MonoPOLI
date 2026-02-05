import pygame

# --- CONFIGURACIÓN DE PANTALLA ---
ANCHO = 1280
ALTO = 720
TITULO_VENTANA = "MonoPOLI Bori's Version"
FPS = 30

# --- MÁRGENES Y DISEÑO ---
MARGEN_TABLERO = 120   # Espacio superior
MARGEN_X = 150         # Margen lateral para el cuadrado del mapa
MARGEN_Y = 150         # Margen vertical para el cuadrado del mapa
RADIO_NODO = 25        # Radio de las casillas del tablero
RADIO_FICHA = 12       # Radio de las fichas de los jugadores

# --- COLORES GENERALES (Estilo Tailwind/Moderno) ---
COLOR_FONDO = (240, 244, 248)       # Gris azulado muy claro
COLOR_TEXTO = (30, 41, 59)          # Azul oscuro casi negro
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# --- COLORES DEL TABLERO ---
AZUL_CASILLA = (59, 130, 246)       # Azul vibrante (Casilla Normal)
DORADO_CASILLA = (245, 158, 11)     # Dorado (Minijuegos)
ROJO_PELIGRO = (220, 38, 38)        # Rojo (Casilla Peligro/Tumbas)
BORDE_TABLERO = (203, 213, 225)     # Gris para las líneas de conexión
COLOR_BRILLO = (255, 255, 255)      # Brillo exterior de casillas
CELESTE_CLARO = (0, 180, 255)

# --- COLORES DE JUGADORES ---
COLOR_JUGADOR_1 = (200, 50, 50)     # Rojo
COLOR_JUGADOR_2 = (50, 200, 50)     # Verde

# --- COLORES DE INTERFAZ / MINIJUEGOS ---
VERDE_EXITO = (16, 185, 129)
AZUL_BOTON = (59, 130, 246)
AZUL_HOVER = (37, 99, 235)
GRIS_TEXTO_SECUNDARIO = (100, 100, 100)
COLOR_BOTON_JUGAR = CELESTE_CLARO

# --- RUTAS DE ARCHIVOS ---

RUTA_PORTADA = 'ElementosGraficos/BorisPortada.png'
RUTA_FICHA_J1 = "ElementosGraficos/ficha1.png"  
RUTA_FICHA_J2 = "ElementosGraficos/ficha2.png"
ARCHIVO_LOG = "historial_partida.txt"
RUTA_FONDO_JUEGO = "ElementosGraficos/fondo_juego.jpg"
RUTA_EVIL_BORIS = "ElementosGraficos/evilBoris.png"
RUTA_GOOD_BORIS = "ElementosGraficos/goodBoris.png"
RUTA_MUSICA = "EfectosDeSonido/soundtrack.mp3"
RUTA_SONIDO_ERROR = "EfectosDeSonido/error.mp3"
RUTA_FONDO_VICTORIA = "ElementosGraficos/victoria_fondo.jpg"

# --- CONSTANTES DE MINIJUEGOS  ---
ARCHIVO_LOG_MINIJUEGOS = "historial_minijuegos.txt"
COLOR_OVERLAY = (0, 0, 0, 180)      # Negro semitransparente para el fondo
ROJO_ERROR = (239, 68, 68)          # Rojo para textos de error (un poco más claro que el de peligro)
GRIS_TEXTO_CLARO = (71, 85, 105)    # Gris pizarra para instrucciones
GRIS_TEXTO_INFO = (70, 70, 70)      # Gris para subtítulos

# Dimensiones (x, y, ancho, alto)
ANCHO_MODAL = 700
ALTO_MODAL = 500
X_MODAL = (ANCHO - ANCHO_MODAL) // 2
Y_MODAL = (ALTO - ALTO_MODAL) // 2
RECT_VENTANA_MODAL = (X_MODAL, Y_MODAL, ANCHO_MODAL, ALTO_MODAL)
ANCHO_BOTON = 200
ALTO_BOTON = 60
X_BOTON = (ANCHO - ANCHO_BOTON) // 2
Y_BOTON = Y_MODAL + 300
RECT_BOTON_DADO = (X_BOTON, Y_BOTON, ANCHO_BOTON, ALTO_BOTON)    # El botón para girar dado
TAMANO_FICHA = 80
VOLUMEN_MUSICA = 0.3