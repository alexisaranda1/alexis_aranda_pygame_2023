
import pygame
from player import Player
from enemy import Enemy
from nivel import *
from constantes import *
from background import Background
pygame.init()
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption('Shooter')

clock = pygame.time.Clock()

#carga de rutas
imagen_dict = {
    "image_dict_playe": {
        "idle": "img/player/Idle/{0}.png",
        "run": "img/player/Run/{0}.png",
        "jum": "img/player/Jump/{0}.png",
         "death": "img/player/Death/{0}.png"
    },
    "image_dict_enemi": {
        "idle": "img/enemy/Idle/{0}.png",
        "run": "img/enemy/Run/{0}.png",
        "jum": "img/enemy/Jump/{0}.png",
        "death": "img/enemy/Death/{0}.png"
    }
}


level = 1
nivel_actual = World()

nivel_actual.process_data(imagen_dict,level)

run = True

while run: 
    lista_eventos = pygame.event.get()
    for event in lista_eventos:
        # Quit game
        if event.type == pygame.QUIT:
            run = False
    nivel_actual.update(lista_eventos)
    nivel_actual.draw(pantalla)
    pygame.display.flip()
    clock.tick(30)

