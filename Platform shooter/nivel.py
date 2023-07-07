from constantes import *
from player import Player
from enemy import Enemy
from bullet import *
import pygame
import csv
from plataforma import Platform

# La clase `ScreenFade` representa un efecto de desvanecimiento de la pantalla en un juego,
#  lo que
# permite un desvanecimiento de entrada o salida en diferentes direcciones y velocidades.

class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self, screen):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:  # whole screen fade
            pygame.draw.rect(
                screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH //
                             2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (0, 0 -
                             self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.colour, (0, SCREEN_HEIGHT //
                             2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.direction == 2:  # vertical screen fade down
            pygame.draw.rect(screen, self.colour,
                             (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True

        return fade_complete


# La clase Exit es una subclase de pygame.sprite.Sprite que
# representa un objeto de salida con una
# imagen y una posición.
class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def update(self, screen_scroll, player):
        # scroll
        self.rect.x += screen_scroll
        # check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            # check what kind of box it was
            if self.item_type == 'Health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 15
            elif self.item_type == 'Grenade':
                player.grenades += 3
            # delete the item box
            self.kill()


# La clase HealthBar se usa para crear y dibujar una barra de salud en la pantalla.
class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health, screen):
        # update with new health
        self.health = health
        # calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


# La clase ItemBox es una subclase de pygame.sprite.Sprite que representa
# una caja que contiene un
# elemento en un juego, con atributos para el tipo de elemento, la imagen y la posición.
class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y, item_boxes):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))


# La clase Agua es un sprite que representa el agua en un juego y se puede
#  actualizar para moverse con
# el desplazamiento de la pantalla.
class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def update(self, screen_scroll):
        self.rect.x += screen_scroll

# La clase `Decoration` es una subclase de `pygame.sprite.Sprite` que representa un objeto de
# decoración con una imagen, una posición y un método de actualización.


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def update(self, screen_scroll):
        self.rect.x += screen_scroll

# La clase `World` procesa datos de nivel y dibuja el mundo del juego en la pantalla.


class World():
    def __init__(self):
        self.obstacle_list = []
        self.world_data = []
        self.img_list = []
        self.level_length = 0
        for x in range(TILE_TYPES):
            img = pygame.image.load(f'img/tile/{x}.png')
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            self.img_list.append(img)

    def load_level_data(self, level):
        # Create empty tile list
        self.world_data = []
        for row in range(ROWS):
            r = [-1] * COLS
            self.world_data.append(r)
        # Load level data and create world
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.world_data[x][y] = int(tile)

    def process_data(self, image_dict):
        self.level_length = len(self.world_data[0])
        player = None
        health_bar = None

        for y, row in enumerate(self.world_data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    if tile >= 0 and tile <= 8:
                        img = self.img_list[tile]
                        self.obstacle_list.append(Platform(x * TILE_SIZE, y * TILE_SIZE, img))
                    # elif tile >= 9 and tile <= 10:
                    #     water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                    #     water_group.add(water)
                    # elif tile >= 11 and tile <= 14:
                    #     decoration = Decoration(
                    #         img, x * TILE_SIZE, y * TILE_SIZE)
                    #     decoration_group.add(decoration)

                    elif tile == 15:
                       player = Player( x * TILE_SIZE, y * TILE_SIZE, speed=5, ammo=100, grenades=4, imge_dict=image_dict["image_dict_playe"])

                        # health_bar = HealthBar(10, 10, player.health, player.health, animation_list)
                    elif tile == 16:
                        enemy = Enemy( x * TILE_SIZE, y * TILE_SIZE, velocidad=5,
                                      imagen_dict_ruta=image_dict["image_dict_enemi"])
                        
                    # elif tile == 17:
                        #     item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE, item_boxes)
                        #     item_box_group.add(item_box)

                    # elif tile == 18:
                        #     item_box = Grenade('Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        #     item_box_group.add(item_box)
                    # elif tile == 19:
                        #     item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE, item_boxes)
                        #     item_box_group.add(item_box)
                    # elif tile == 20:
                        #     exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        #     exit_group.add(exit)

        # return player, health_bar
        return player, enemy
    
    def check_collision(self, character):
        collision_threshold = 0  # Umbral de colisión para evitar errores de colisión falsos

        character.rect.x += character.vel_x
        for platform in self.obstacle_list:
            if platform.rect.colliderect(character.rect):
                if character.vel_x > 0:
                    character.rect.right = platform.rect.left - collision_threshold
                elif character.vel_x < 0:
                    character.rect.left = platform.rect.right + collision_threshold

        character.rect.y += character.vel_y
        for platform in self.obstacle_list:
            if platform.rect.colliderect(character.rect):
                if character.vel_y > 0:
                    character.rect.bottom = platform.rect.top - collision_threshold
                    character.in_air = False
                elif character.vel_y < 0:
                    character.rect.top = platform.rect.bottom + collision_threshold
                    character.vel_y = 0

        character.rect.x = round(character.rect.x)
        character.rect.y = round(character.rect.y)



    def draw(self, screen,screen_scroll):
        for platform in self.obstacle_list:
            platform.update(screen,screen_scroll)













''' 
class Level:
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, image_dict):
        self.level_length = len(self.world_data[0])
        player = None
        enemy = None

        for y, row in enumerate(self.world_data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = self.img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(Platform(x * TILE_SIZE, y * TILE_SIZE, img))
                    elif tile == 15:
                        player = Player(x * TILE_SIZE, y * TILE_SIZE, speed=5, ammo=100, grenades=4,
                                        image_dict=image_dict["image_dict_player"])
                    elif tile == 16:
                        enemy = Enemy(x * TILE_SIZE, y * TILE_SIZE, speed=5, image_dict=image_dict["image_dict_enemy"])

        return player, enemy

    def check_collision(self, character):
        collision_threshold = 0  # Umbral de colisión para evitar errores de colisión falsos

        character.rect.x += character.vel_x
        for platform in self.obstacle_list:
            if platform.rect.colliderect(character.rect):
                if character.vel_x > 0:
                    character.rect.right = platform.rect.left - collision_threshold
                elif character.vel_x < 0:
                    character.rect.left = platform.rect.right + collision_threshold

        character.rect.y += character.vel_y
        for platform in self.obstacle_list:
            if platform.rect.colliderect(character.rect):
                if character.vel_y > 0:
                    character.rect.bottom = platform.rect.top - collision_threshold
                    character.in_air = False
                elif character.vel_y < 0:
                    character.rect.top = platform.rect.bottom + collision_threshold
                    character.vel_y = 0

        character.rect.x = round(character.rect.x)
        character.rect.y = round(character.rect.y)

    def draw(self, screen):
        for platform in self.obstacle_list:
            platform.draw(screen)
'''