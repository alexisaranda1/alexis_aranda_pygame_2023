import pygame
from auxiliar import Auxiliar
from character import Character
from constantes import *
class Player(Character): # jugador
    def __init__(self, x, y, speed, ammo, grenades,imge_dict):
        super().__init__(x, y, speed)

        self.idle_reght= Auxiliar.getSurfaceFromSeparateFiles(imge_dict["idle"], 1, 4,False)
        self.idle_left = Auxiliar.getSurfaceFromSeparateFiles(imge_dict["idle"], 1, 4,True) 
        self.run_reght= Auxiliar.getSurfaceFromSeparateFiles(imge_dict["run"], 1, 5)
        self.run_left = Auxiliar.getSurfaceFromSeparateFiles(imge_dict["run"], 1, 5, True)
        self.jum_reght = Auxiliar.getSurfaceFromSeparateFiles(imge_dict["jum"], 0, 1,False ,2)
        self.jum_left = Auxiliar.getSurfaceFromSeparateFiles(imge_dict["jum"], 0, 1, True,2)
        
        self.frame_index = 0
        self.animation = self.idle_reght
        self.image = self.animation[self.frame_index]
        self.rect = self.image.get_rect()  # rectangulo
        self.rect.center = (x, y)  # centro_rectangulo
        self.width = self.image.get_width()  # ancho
        self.height = self.image.get_height()  # alto
        self.ammo = ammo  # municion
        self.start_ammo = ammo  # municion_inicial
        self.shoot_cooldown = 0  # enfriamiento_disparo
        self.action = 0
        self.grenades = grenades  # granadas
        self.moving_left = False
        self.moving_right = False
        self.direction = 1  # direccion

        self.jump = False  # saltar
        self.in_air = False  # en_aire
        self.flip = False  # voltear
    def update(self):
        super().update()

        self.vel_x = 0  # Reiniciar la velocidad horizontal

        if self.moving_left:
            self.move_left()
        elif self.moving_right:
            self.move_right()

        self.jum()
        # actualizar enfriamiento
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
    def jum(self):
        if self.jump  and not self.in_air:
            print("si salte")
            self.frame_index = 0
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        else:
            self.in_air = False


    def move_left(self):
        if self.moving_left:
            self.frame_index = 0
            self.direction = -1
            self.rect.x -= self.speed
            self.rect.y = self.y  # Actualizar la coordenada y del rectángulo

    def move_right(self):
        new_position_x = self.rect.x + self.speed
        right_limit = SCREEN_WIDTH * 3/4

        if self.moving_right:
            if new_position_x + self.rect.width <= right_limit:
                self.frame_index = 0
                self.direction = 1
                self.rect.x = new_position_x
                self.rect.y = self.y  # Actualizar la coordenada y del rectángulo
            else:
                self.rect.x = right_limit - self.rect.width
        else:
            self.rect.x = right_limit - self.rect.width

    def handle_key_events(self, event,bullet_group,shot_fx):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print("left")
                self.moving_left = True
                self.update_action(3)  # Actualizar la acción a "Correr hacia la izquierda"
            elif event.key == pygame.K_d:
                print("right")
                self.moving_right = True
                self.update_action(2)  # Actualizar la acción a "Correr hacia la derecha"
            elif event.key == pygame.K_SPACE:
                print("dispa")
                self.shoot(bullet_group, shot_fx) 
            elif event.key == pygame.K_q:
                self.grenade = True
            elif event.key == pygame.K_w and self.alive:
                print("salto")
                self.jump = True
                self.update_action(4)  # Actualizar la acción a "Saltar"

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.moving_left = False
                if not self.moving_right:
                    self.update_action(0)  # Actualizar la acción a "Quieto"
            elif event.key == pygame.K_d:
                self.moving_right = False
                if not self.moving_left:
                    self.update_action(0)  # Actualizar la acción a "Quieto"
            elif event.key == pygame.K_SPACE:
                #self.shoot = False
                pass
            elif event.key == pygame.K_q:
                self.grenade = False
                self.grenade_thrown = False
            elif event.key == pygame.K_w and self.alive:
                self.jump = False
                self.update_action(0)  # Actualizar la acción a "Quieto"
        self.update_velocity()

    def update_velocity(self):
        if self.moving_left:
            self.vel_x = -self.speed
        elif self.moving_right:
            self.vel_x = self.speed
        else:
            self.vel_x = 0