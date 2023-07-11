from constantes import *
from player import Player
from enemy import Enemy
from bullet import *
import pygame
import csv
from plataforma import Platform
from botin import ItemBox
from background import Background
from banderas import *
from class_chronometer import Chronometer
from class_trampa import Trampa
from class_decoration import Decoration
from class_healthBar import HealthBar
import json

class World():
    def __init__(self):
        self.platform_group = pygame.sprite.Group()
        self.font =  pygame.font.SysFont('Futura', 30)
        self.fondo =  Background( "img/background/fondo_0.png")
        self.sonido_disparo = pygame.mixer.Sound('audio/shot.wav')
        self.desplazamiento_pantalla  = 0
        self.datos_nivel = []
        self.amagen_list = []
        self.nivel_len = 0
        self.bandera_nivel = 0
        self.player = None
        self.barra_salud = None
        self.cronometro = Chronometer(tiempo_inicial=150)
        self.item_box_group = pygame.sprite.Group()
        self.trampa_group = pygame.sprite.Group()
        self.grupo_decoracion = pygame.sprite.Group()
        self.grupo_granada = pygame.sprite.Group()
        self.grupo_player = pygame.sprite.Group()
        self.grupo_enemigos = pygame.sprite.Group()
        self.grupo_balas = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()
        self.dic_data = {}
        for x in range(CANTIDAD_BLOQUES):
            image = pygame.image.load(f'img/tile/{x}.png')
            image = pygame.transform.scale(image, (TAMAÑO_BLOQUES, TAMAÑO_BLOQUES))
            self.amagen_list.append(image)

    def load_level_data(self, nivel):
        # Create empty tile list
        self.bandera_nivel = nivel
        self.datos_nivel = []
        for fila in range(FILAS):
            r = [-1] * COLUMNAS
            self.datos_nivel.append(r)
        # Load level data and create world
        with open(f'level{nivel}_data.csv', newline='') as archivo:
            lector = csv.reader(archivo, delimiter=',')
            for x, fila in enumerate(lector):
                for y, elemento in enumerate(fila):
                    self.datos_nivel[x][y] = int(elemento)

    def process_data(self, image_dict,nivel):
        self.load_level_data(nivel)
        self.nivel_len = len(self.datos_nivel[0])
        for y, fila in enumerate(self.datos_nivel):
            for x, elemento in enumerate(fila):
                if elemento >= 0:
                    image = self.amagen_list[elemento]
                if elemento >= 0 and elemento <= 8:
                    self.platform_group.add(Platform(x * TAMAÑO_BLOQUES, y * TAMAÑO_BLOQUES, image))
                elif elemento >= 9 and elemento <= 10:
                    trampa = Trampa(image, x * TAMAÑO_BLOQUES, y * TAMAÑO_BLOQUES)
                    self.trampa_group.add(trampa)
                elif elemento >= 11 and elemento <= 14:
                    decoration = Decoration(image, x * TAMAÑO_BLOQUES, y * TAMAÑO_BLOQUES)
                    self.grupo_decoracion.add(decoration)
                elif elemento == 15:
                    player = Player(x * TAMAÑO_BLOQUES, y * TAMAÑO_BLOQUES, velocidad=5, municion=10, granadas=4, imagen_dict_ruta=image_dict["image_dict_playe"])
                    self.grupo_player.add(player)
                    self.player = self.grupo_player .sprites()[0]
                    self.barra_salud = HealthBar(10, 10, self.player.salud, self.player.salud_maxima)
                elif elemento == 16:
                    self.grupo_enemigos.add(Enemy(x * TAMAÑO_BLOQUES, y * TAMAÑO_BLOQUES, velocidad=3, imagen_dict_ruta=image_dict["image_dict_enemi"]))

                elif elemento == 17:
                    item_box = ItemBox('Ammo', x * TAMAÑO_BLOQUES, y * TAMAÑO_BLOQUES)
                    self.item_box_group.add(item_box)
                elif elemento == 19:
                    item_box = ItemBox('Health', x * TAMAÑO_BLOQUES, y * TAMAÑO_BLOQUES)
                    self.item_box_group.add(item_box)
                elif elemento == 20:
                    item_box = ItemBox('Exit', x * TAMAÑO_BLOQUES, y * TAMAÑO_BLOQUES,nivel)
                    self.item_box_group.add(item_box)

    def update(self,lista_evento):
        self.player.update_position(self.desplazamiento_pantalla)
        self.player.handle_key_events(lista_evento,self.grupo_balas,self.sonido_disparo)
        self.player.update()
        self.desplazamiento_pantalla = self.fondo.update_scroll(self)
        self.check_collision(self.grupo_player)
        self.check_collision(self.grupo_enemigos)



        self.trampa_group.update(self.desplazamiento_pantalla, self.player)
        self.grupo_decoracion.update(self.desplazamiento_pantalla)
        self.item_box_group.update(self.desplazamiento_pantalla,self.player)
        self.grupo_balas.update(self, self.player, self.grupo_enemigos, self.grupo_balas)
        self.grupo_enemigos.update(self.desplazamiento_pantalla , self.player,self.grupo_balas,self.sonido_disparo)
        self.cronometro.actualizar()

    def draw(self, pantalla):

        bandera = leer_bandera(f"bandera_{self.bandera_nivel}")
        if not self.player.vivo or self.cronometro.tiempo_desendente <= 0 :
            imagen = pygame.image.load(r'menu_1\game_over.jpg')
            imagen_escalada = pygame.transform.scale(imagen, (1000, 600))
            pantalla.blit(imagen_escalada, (0, 0))

        elif bandera[0] == "true":
            self.guardar_partida()
            imagen = pygame.image.load(r'menu_1\win.jpg')
            imagen_escalada = pygame.transform.scale(imagen, (1000, 600))
            pantalla.blit(imagen_escalada, (0, 0))

        else:
            self.fondo.draw(pantalla,self.desplazamiento_pantalla)
            self.trampa_group.draw(pantalla)
            self.grupo_decoracion.draw(pantalla)
            self.item_box_group.draw(pantalla)  
            self.grupo_balas.draw(pantalla) 
            self.grupo_enemigos.draw(pantalla) 
            self.barra_salud.draw(self.player.salud,pantalla)
            self.draw_ammo(self.player,pantalla)
            self.platform_group.update(pantalla,self.desplazamiento_pantalla)
            self.player.draw(pantalla)
            self.cronometro.mostrar_tiempo(pantalla)



    def draw_ammo(self, player,pantalla):
        imagen_balas = pygame.image.load('img/tile/17.png')
        imagen_balas = pygame.transform.scale(imagen_balas, (TAMAÑO_IMAGEN_BALAS, TAMAÑO_IMAGEN_BALAS))
        for x in range(player.municion):
            pantalla.blit(imagen_balas, (10 + (x * 10), 40))

    def check_collision(self, character_group):
        limite_colision = 0  # Valor para evitar errores de colisión falsos

        for character in character_group:
            next_x = character.rect.x + character.vel_x
            next_y = character.rect.y + character.vel_y

            self.handle_horizontal_collision(character, next_x, limite_colision)
            self.handle_vertical_collision(character, next_y, limite_colision)

    def handle_horizontal_collision(self, character, next_x, limite_colision):
        character.rect.x = next_x
        collision_list = pygame.sprite.spritecollide(character, self.platform_group, False)
        for platform in collision_list:
            if character.vel_x > 0:
                character.rect.right = platform.rect.left - limite_colision
            elif character.vel_x < 0:
                character.rect.left = platform.rect.right + limite_colision

        if collision_list:
            character.vel_x = 0  # Detener el movimiento horizontal si hubo colisión
        character.x = character.rect.x  # Actualizar la posición x del personaje

    def handle_vertical_collision(self, character, next_y, limite_colision):
        character.rect.y = next_y
        collision_list = pygame.sprite.spritecollide(character, self.platform_group, False)
        for platform in collision_list:
            if character.vel_y > 0:
                character.rect.bottom = platform.rect.top - limite_colision
                character.in_air = False
                character.en_suelo = True
            elif character.vel_y < 0:
                character.rect.top = platform.rect.bottom + limite_colision
                character.vel_y = 0
            if character.rect.colliderect(platform.rect):
                if character.rect.centerx < platform.rect.centerx:
                    character.rect.right = platform.rect.left - limite_colision
                else:
                    character.rect.left = platform.rect.right + limite_colision
        if collision_list:
            character.vel_y = 0  # Detener el movimiento vertical si hubo colisión
        character.y = character.rect.y  # Actualizar la posición y del personaje

        # GUARDAR EN TXT
    def guardar_partida(self):
        '''
        Brief: Guarda en un archivio la ultima puntucion del jugado

        Parameters:
            self -> Instancia de la clase   
        '''
        with open("score.txt","w") as archivo:
            archivo.write(str(self.player.scoree))

            
