import pygame
from auxiliar import Auxiliar
from bullet import Bullet
from character import Character

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
        super().update()  # Llama al método update() de la clase Character
        self.jum()
        self.move_left()
        self.move_right()

        # actualizar enfriamiento
        self.rect.y += self.vel_y
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
    def shoot(self,bullet_group, shot_fx):
        """
        La función de disparo comprueba si el jugador puede disparar, crea un objeto de bala, reduce la
        munición y reproduce un efecto de sonido.
        """
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery,
                            self.direction)
            bullet_group.add(bullet)
            # reducir munición
            self.ammo -= 1
            shot_fx.play()

    def jum(self):
        if self.jump  and not self.in_air:
            print("si salte")
            self.frame_index = 0
            self.animation = self.jum_reght
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        else:
            self.in_air = False

    def move_left(self):
        if self.moving_left:
            self.frame_index = 0
            self.animation = self.run_left
            self.direction = -1  
            self.rect.x -= self.speed
    def move_right(self):
        if self.moving_right:
            self.frame_index = 0
            self.animation = self.run_reght
            self.direction = 1 
            self.rect.x += self.speed
    def handle_key_events(self,event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print("left")
                self.moving_left = True
            elif event.key == pygame.K_d:
                print("right")
                self.moving_right = True
            elif event.key == pygame.K_SPACE:  
                #self.shoot = True
                pass
            elif event.key == pygame.K_q:
                self.grenade = True
            elif event.key == pygame.K_w and self.alive:
                print("salto")
                self.jump = True

        if event.type == pygame.KEYUP:
            self.animation = self.idle_reght
            if event.key == pygame.K_a:
                self.moving_left = False
            if event.key == pygame.K_d:
                self.moving_right = False
            if event.key == pygame.K_SPACE:
                #self.shoot = False
                pass
            if event.key == pygame.K_q:
                self.grenade = False
                self.grenade_thrown = False
                