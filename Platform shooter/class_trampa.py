import pygame
from constantes import*
class Trampa(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TAMAÑO_BLOQUES // 2, y +
                            (TAMAÑO_BLOQUES - self.image.get_height()))
    def colision (self, player):
        if pygame.sprite.collide_rect(self, player):
                player.take_damage(1)

    def update(self, screen_scroll,player):
        self.colision(player)
        self.rect.x += screen_scroll
    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)