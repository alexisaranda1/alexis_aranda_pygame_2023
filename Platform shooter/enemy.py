import pygame 
import random
from constantes import *
from character import Character
from auxiliar import Auxiliar

class Enemy(Character):
    def __init__(self, x, y, velocidad, imagen_dict_ruta):
        super().__init__(x, y, velocidad)
        self.quieto_derecha = Auxiliar.getSurfaceFromSeparateFiles(imagen_dict_ruta["idle"], 1, 4, False)
        self.quieto_izquierda = Auxiliar.getSurfaceFromSeparateFiles(imagen_dict_ruta["idle"], 1, 4, True) 
        self.correr_derecha = Auxiliar.getSurfaceFromSeparateFiles(imagen_dict_ruta["run"], 1, 5)
        self.correr_izquierda = Auxiliar.getSurfaceFromSeparateFiles(imagen_dict_ruta["run"], 1, 5, True)
        self.saltar_derecha = Auxiliar.getSurfaceFromSeparateFiles(imagen_dict_ruta["jum"], 0, 1, False, 2)
        self.saltar_izquierda = Auxiliar.getSurfaceFromSeparateFiles(imagen_dict_ruta["jum"], 0, 1, True, 2)
        self.muerte_derecha = Auxiliar.getSurfaceFromSeparateFiles(imagen_dict_ruta["death"], 0, 1, False, 2)
        self.muerte_izquierda = Auxiliar.getSurfaceFromSeparateFiles(imagen_dict_ruta["death"], 0, 1, True, 2)
        self.indice_frame = 0
        self.animacion = self.quieto_derecha
        self.salud_maxima = self.salud
        self.image = self.animacion[self.indice_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.ancho = self.image.get_width()
        self.altura = self.image.get_height()
        self.direccion = 1
        self.accion = 0  
        self.municion = 5000
        self.municion_maxima = 5000
        self.contador_movimiento = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.inactivo = False
        self.contador_inactividad = 0


    def update(self,screen_scroll,player, bullet_group, shot_fx):
        super().update()  # Llama al método update() de la clase Character
        self.ai(player,bullet_group,shot_fx)  # inteligencia_artificial
        # desplazar
        self.rect.x += screen_scroll
            # Reducir el tiempo de espera para el próximo disparo
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    def move(self, movi_der, movi_izq):
        if movi_der:
            self.rect.x -= self.speed
        elif movi_izq:
            self.rect.x += self.speed

    def ai(self, player, grupo_balas, sonido_disparo):
        if self.alive and player.alive:
            if not self.inactivo and random.randint(1, 200) == 1:
                self.update_action(0)  # 0: idle
                self.inactivo = True
                self.contador_inactividad = 50

            # Comprueba si el enemigo está cerca del jugador
            if self.vision.colliderect(player.rect):
                # Detén el movimiento y enfrenta al jugador
                self.move(movi_der=False, movi_izq=False)  # Detén el movimiento (no muevas a izquierda ni derecha)
                self.update_action(0)  # 0: idle
                self.shoot(grupo_balas, sonido_disparo)
            else:
                if not self.inactivo:
                    ai_movimiento_derecha = self.direction == 1
                    ai_moving_left = not ai_movimiento_derecha
                    self.move(movi_der=ai_moving_left, movi_izq=ai_movimiento_derecha)
                    self.update_action(1)  # 1: run
                    self.contador_movimiento += 1
                    # Actualiza la visión del enemigo mientras se mueve
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.contador_movimiento > TILE_SIZE:
                        self.direction *= -1
                        self.contador_movimiento *= -1
                else:
                    self.contador_inactividad -= 1
                    if self.contador_inactividad <= 0:
                        self.inactivo = False
