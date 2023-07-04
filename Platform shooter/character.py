import pygame
from constantes import *

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

    def update_animation(self):
        # actualizar animación
        ANIMATION_COOLDOWN = 100
        # actualizar imagen según el fotograma actual
        self.image = self.animation
        # comprobar si ha pasado suficiente tiempo desde la última actualización
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # si la animación se ha terminado, volver al inicio
        if self.frame_index >= len(self.animation):
            if self.action == 3:
                self.frame_index = len(self.animation) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # comprobar si la nueva acción es diferente a la anterior
        if new_action != self.action:
            self.action = new_action
            # actualizar la configuración de la animación
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    def update(self):
        self.update_animation()  # actualizar_animacion
        self.check_alive()  # verificar_vivo
        self.apply_gravity()
        self.rect.y += self.vel_y  # actualizar posición vertical

    def draw(self,screen):
        self.image = self.animation[self.frame_index]
        screen.blit(self.image, self.rect)
        if DEBUF:
            player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(screen, RED, player_rect)

    def apply_gravity(self):
        if self.vel_y < 10:
            self.vel_y += GRAVITY

    def move(self, direction):
        if direction == "left":
            self.x -= self.speed
        elif direction == "right":
            self.x += self.speed
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
