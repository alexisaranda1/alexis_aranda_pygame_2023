import pygame
from constantes import *
from bullet import *

import pygame
from constantes import *
from bullet import *


class Character(pygame.sprite.Sprite): # personaje
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True  # vivo
        self.x = x
        self.y = y
        self.vel_y = 0  
        self.vel_x = 0
        self.speed = speed
        self.update_time = pygame.time.get_ticks()
        self.health = 100  # salud
        self.max_health = self.health  # salud_maxima
        self.shoot_cooldown = 0
        #self.width = TILE_SIZE ajusta segun el tamaño de los bloques
        #self.height = TILE_SIZE
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.frame_index = 0
        self.animation = []  # Debes definir las animaciones específicas en las subclases
        self.direction = 1  # O cualquier otro valor inicial que desees
        self.action = 0  # 0: idle, 1: run, 2: jump, etc.

    def update_animation(self):
        ANIMATION_COOLDOWN = 100

        if self.action == 0:  # Idle
            if self.direction == 1:
                self.animation = self.idle_reght
            else:
                self.animation = self.idle_left
        elif self.action == 1:  # Run
            if self.direction == 1:
                self.animation = self.run_reght
            else:
                self.animation = self.run_left
        elif self.action == 2:  # Jump
            if self.direction == 1:
                self.animation = self.jum_reght
            else:
                self.animation = self.jum_left

        self.image = self.animation[self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update(self):
        self.update_animation()
        self.check_alive()
        self.apply_gravity()

    def draw(self, screen):
        self.image = self.animation[self.frame_index]
        screen.blit(self.image, self.rect)
        if DEBUF:
            player_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
            pygame.draw.rect(screen, RED, player_rect)

    def apply_gravity(self):
        if self.vel_y < 10:
            self.vel_y += GRAVITY
            
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
    def shoot(self, bullet_group, shot_fx):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction, bullet_img)
            bullet_group.add(bullet)
            self.ammo -= 1
            shot_fx.play()


    # def shoot(self, bullet_group, shot_fx):

    #     if self.shoot_cooldown == 0 and self.ammo > 0:
    #         print("diparo el enemigo")
    #         self.shoot_cooldown = 20
    #         bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
    #         bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction, bullet_img)
    #         bullet_group.add(bullet)
    #         self.ammo -= 1
    #         shot_fx.play()
