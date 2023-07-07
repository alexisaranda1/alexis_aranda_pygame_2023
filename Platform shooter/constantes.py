SCREEN_WIDTH =600 # ancho
SCREEN_HEIGHT =400 # alto

WIDTH = 64  # Ancho del personaje
HEIGHT = 64  # Alto del personaje

SPEED_FACTOR = 0.000
FPS = 60
#define game variables
GRAVITY = 0.75 # Gravedad

ROWS = 16 # Filas
COLS = 150 # Columnas
TILE_SIZE = SCREEN_HEIGHT // ROWS # Tamaño de los bloques
TILE_TYPES = 21 # Tipos de bloques
MAX_LEVELS = 3 # Número máximo de niveles
DEBUF = False
#define colours
BG = (144, 201, 120) # Fondo (verde claro)
RED = (255, 0, 0) # Rojo
WHITE = (255, 255, 255) # Blanco
GREEN = (0, 255, 0) # Verde
BLACK = (0, 0, 0) # Negro
PINK = (235, 65, 54) # Rosa



SCROLL_THRESH = 200 # desplazamiento
# Las variables `screen_scroll` y `bg_scroll` se utilizan para realizar un seguimiento de la posición
# de desplazamiento de la pantalla y el fondo del juego.
screen_scroll = 0
bg_scroll = 0