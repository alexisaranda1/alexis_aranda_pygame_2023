
import pygame
from constantes import *
from banderas import *
class ItemBox(pygame.sprite.Sprite):
    item_boxes = {
        'Health': pygame.image.load('img/tile/19.png'),
        'Ammo': pygame.image.load('img/tile/17.png'),
        'Exit': pygame.image.load('img/tile/20.png')
    }
    def __init__(self, item_type, x, y,nivel= False):
        pygame.sprite.Sprite.__init__(self)
        self.nivel = nivel
        self.terminar_nivel = False
        self.item_type = item_type
        self.image = ItemBox.item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TAMAÑO_BLOQUES // 2, y + (TAMAÑO_BLOQUES - self.image.get_height()))

    def update(self, screen_scroll, player):
        self.rect.x += screen_scroll
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Health':
                if player.salud < 100:
                    player.salud += 10  
            elif self.item_type == 'Ammo':
                if player.municion < 10:
                    player.municion = 10 
            elif self.item_type == 'Exit':
                crear_bandera(f"bandera_{self.nivel}","true") 
                self.terminar_nivel = True
            self.kill()
            
    def draw(self, pantalla):
        print(self.terminar_nivel)
        if self.terminar_nivel:
            print(self.terminar_nivel)
            imagen = pygame.image.load(r'menu_1\win.jpg')
            pantalla.blit(imagen, (0, 0))
        else:
            pantalla.blit(self.image,(self.rect))
          


