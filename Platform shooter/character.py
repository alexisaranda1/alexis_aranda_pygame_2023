import pygame
from constantes import *
from bullet import *
import pygame
from constantes import *
from bullet import *
class Character(pygame.sprite.Sprite): # personaje
    def __init__(self, x, y, velocidad):
        pygame.sprite.Sprite.__init__(self)
        self.vivo = True  
        self.x = x
        self.y = y
        self.vel_y = 0  
        self.vel_x = 0
        self.velocidad = velocidad
        self.tiempo_actualizacion = pygame.time.get_ticks()
        self.salud = 100 
        self.salud_maxima = self.salud
        self.enfriamiento_disparo = 0
        self.rect = pygame.Rect(x, y, ANCHO, ALTO)
        self.image = pygame.Surface((ANCHO, ALTO))
        self.indice_frame = 0
        self.animacion = [] 
        self.direccion = 1
        self.accion = 0

    def update_action(self, nueva_accion):
        if nueva_accion != self.accion:
            self.accion = nueva_accion
            self.indice_frame = 0
            self.tiempo_actualizacion = pygame.time.get_ticks()
    def update(self):
        self.check_alive()
        self.apply_gravity()
    def draw(self, screen):
        self.image = self.animacion[self.indice_frame]
        screen.blit(self.image, self.rect)
        if self.scoree is not None:
            fuente = pygame.font.Font(None, 50)
            score_texto = fuente.render(f"score: {self.scoree}", False, BLANCO)
            screen.blit(score_texto, (600, 6))
        if DEBUG:
            player_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
            pygame.draw.rect(screen, ROJO, player_rect)
    def apply_gravity(self):
        if self.vel_y < 10:
            self.vel_y += GRAVEDAD
    def check_alive(self):
        if self.salud <= 0:
            self.salud = 0
            self.velocidad = 0
            self.vivo = False
            self.update_action(3)    
    def shoot(self, grupo_balas, shot_fx):
        
        if  self.municion > 0:
            self.enfriamiento_disparo = 20
            bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direccion), self.rect.centery, self.direccion, bullet_img)
            grupo_balas.add(bullet)
            print("esta disparando")
            self.municion -= 1
            shot_fx.play()



