import pygame
from pygame.locals import*
from nivel import *

class Manejador_niveles:

    def __init__(self, pantalla) -> None:
        self._slave = pantalla # pantalla juego
        self.nivel = World()
        self.nivel = None
        self.nivel_uno = None  
       
    def get_nivel_1(self):
         #carga de rutas
        imagen_dict = {
        "image_dict_playe": {
            "idle": "img\player\Idle\{0}.png",
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

        nivel = 1
        self.nivel = World()
        self.nivel.process_data(imagen_dict, nivel)
        return self.nivel

    def get_nivel_2(self):
            #carga de rutas
        imagen_dict = {
        "image_dict_playe": {
            "idle": "img\player\Idle\{0}.png",
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
        

        
        nivel = 2
        self.nivel = World()
        self.nivel.process_data(imagen_dict, nivel)
        return self.nivel

    def get_nivel_3(self):
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
        nivel = 3
        self.nivel = World()
        self.nivel.process_data(imagen_dict, nivel)
        return self.nivel


