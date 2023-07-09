from constantes import *
from player import Player
from enemy import Enemy
from bullet import *
import pygame
import csv
from plataforma import Platform
from botin import ItemBox
from background import Background

# La clase Agua es un sprite que representa el agua en un juego y se puede
#  actualizar para moverse con
# el desplazamiento de la pantalla.
class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TAMAÑO_BLOQUES // 2, y +
                            (TAMAÑO_BLOQUES - self.image.get_height()))

    def update(self, screen_scroll):
        self.rect.x += screen_scroll
    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)
# La clase `Decoration` es una subclase de `pygame.sprite.Sprite` que representa un objeto de
# decoración con una imagen, una posición y un método de actualización.

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TAMAÑO_BLOQUES // 2, y + (TAMAÑO_BLOQUES - self.image.get_height()))

    def update(self, screen_scroll):
        self.rect.x += int(screen_scroll)

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)

# La clase ItemBox es una subclase de pygame.sprite.Sprite que representa
# una caja que contiene un
# elemento en un juego, con atributos para el tipo de elemento, la imagen y la posición.
# La clase HealthBar se usa para crear y dibujar una barra de salud en la pantalla.

class HealthBar():
    def __init__(self, x, y, salud, salud_maxima):
        self.x = x
        self.y = y
        self.salud = salud
        self.salud_maxima = salud_maxima

    def draw(self, salud, pantalla):
        self.salud = salud
        proporcion_salud = self.salud / self.salud_maxima
        pygame.draw.rect(pantalla, NEGRO, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(pantalla, ROJO, (self.x, self.y, 150, 20))
        pygame.draw.rect(pantalla, VERDE, (self.x, self.y, 150 * proporcion_salud, 20))

# La clase `World` procesa datos de nivel y dibuja el mundo del juego en la pantalla.



































class World():
    def __init__(self):
        self.platform_group = pygame.sprite.Group()
        self.font =  pygame.font.SysFont('Futura', 30)
        self.fondo =  Background( "img/background/fondo_0.png")
        self.pantalla =self.fondo.get_screen()
        self.sonido_disparo = pygame.mixer.Sound('audio/shot.wav')
        self.desplazamiento_pantalla  = 0
        self.datos_nivel = []
        self.amagen_list = []
        self.nivel_len = 0
        self.player = None
        self.barra_salud = None
        self.item_box_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.grupo_decoracion = pygame.sprite.Group()
        self.grupo_granada = pygame.sprite.Group()
        self.grupo_player = pygame.sprite.Group()
        self.grupo_enemigos = pygame.sprite.Group()
        self.grupo_balas = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()
        for x in range(CANTIDAD_BLOQUES):
            image = pygame.image.load(f'img/tile/{x}.png')
            image = pygame.transform.scale(image, (TAMAÑO_BLOQUES, TAMAÑO_BLOQUES))
            self.amagen_list.append(image)

    def load_level_data(self, nivel):
        # Create empty tile list
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
                    water = Water(image, x * TAMAÑO_BLOQUES, y * TAMAÑO_BLOQUES)
                    self.water_group.add(water)
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
                    item_box = ItemBox('Exit', x * TAMAÑO_BLOQUES, y * TAMAÑO_BLOQUES)
                    self.item_box_group.add(item_box)
  
    def update(self,lista_evento):

        self.player.handle_key_events(lista_evento,self.grupo_balas,self.sonido_disparo)
        self.player.update()
        self.check_collision(self.grupo_player)
        self.check_collision(self.grupo_enemigos)
        self.player.update_position(self.desplazamiento_pantalla)
        self.desplazamiento_pantalla = self.fondo.update_scroll(self)
        self.water_group.update(self.desplazamiento_pantalla)
        self.grupo_decoracion.update(self.desplazamiento_pantalla)
        self.item_box_group.update(self.desplazamiento_pantalla,self.player)
        self.grupo_balas.update(self, self.player, self.grupo_enemigos, self.grupo_balas)
        self.grupo_enemigos.update(self.desplazamiento_pantalla , self.player,self.grupo_balas,self.sonido_disparo)
    
    def draw(self, pantalla):
        self.fondo.draw(self.desplazamiento_pantalla)
        self.water_group.draw(pantalla)
        self.grupo_decoracion.draw(pantalla)
        self.item_box_group.draw(pantalla)  
        self.grupo_balas.draw(pantalla) 
        self.grupo_enemigos.draw(pantalla) 
        self.barra_salud.draw(self.player.salud,pantalla)
        self.draw_ammo(self.player,pantalla)
        self.platform_group.update(pantalla,self.desplazamiento_pantalla)
        self.player.draw(pantalla)

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



