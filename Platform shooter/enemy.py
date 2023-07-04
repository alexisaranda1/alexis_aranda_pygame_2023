import pygame 
import random
from constantes import *
from character import Character
from auxiliar import Auxiliar

class Enemy(Character):
    def __init__(self, x, y, speed, imge_dict):
        super().__init__(x, y, speed)

        self.idle_reght= Auxiliar.getSurfaceFromSeparateFiles(imge_dict["idle"], 1, 4,False)
        self.idle_left = Auxiliar.getSurfaceFromSeparateFiles(imge_dict["idle"], 1, 4,True) 
        self.run_reght= Auxiliar.getSurfaceFromSeparateFiles(imge_dict["run"], 1, 5)
        self.run_left = Auxiliar.getSurfaceFromSeparateFiles(imge_dict["run"], 1, 5, True)
        self.jum_reght = Auxiliar.getSurfaceFromSeparateFiles(imge_dict["jum"], 0, 1,False ,2)
        self.jum_left = Auxiliar.getSurfaceFromSeparateFiles(imge_dict["jum"], 0, 1, True,2)
        self.death_reght = Auxiliar.getSurfaceFromSeparateFiles(imge_dict["death"], 0, 1,False ,2)
        self.death_left = Auxiliar.getSurfaceFromSeparateFiles(imge_dict["death"], 0, 1, True,2)
        self.frame_index = 0
        self.animation = self.idle_reght
        self.max_health = self.health  # salud_maxima
        self.image = self.animation[self.frame_index]
        self.rect = self.image.get_rect()  # rectangulo
        self.rect.center = (x, y)  # centro_rectangulo
        self.width = self.image.get_width()  # ancho
        self.height = self.image.get_height()  # alto
        self.direction = 1  # O cualquier otro valor inicial que desees
        self.action = 0  # 0: idle, 1: run



        self.move_counter = 0  # contador_movimiento
        self.vision = pygame.Rect(0, 0, 150, 20)  # vision
        self.idling = False  # inactividad
        self.idling_counter = 0  # contador_inactividad


    def update(self,screen_scroll,player):
        super().update()  # Llama al método update() de la clase Character
        #self.ai(player)  # inteligencia_artificial
        # desplazar
        self.rect.x += screen_scroll

    def ai(self, player):
        if self.alive and player.alive:
            if not self.idling and random.randint(1, 200) == 1:
                self.update_action(0)  # 0: idle
                self.idling = True
                self.idling_counter = 50
            # Verificar si la IA está cerca del jugador
            if self.vision.colliderect(player.rect):
                # Detenerse y mirar al jugador
                self.update_action(0)  # 0: idle
                # Disparar
                self.shoot()
            else:
                if not self.idling:
                    direction = "right" if self.direction == 1 else "left"
                    self.move(direction)
                    self.update_action(1)  # 1: run
                    self.move_counter += 1
                    # Actualizar visión de la IA mientras el enemigo se mueve
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False



