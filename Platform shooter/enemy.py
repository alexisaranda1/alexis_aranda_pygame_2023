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
        self.muerte_derecha = Auxiliar.getSurfaceFromSeparateFiles(imagen_dict_ruta["death"], 0, 7, False, 2)
        self.muerte_izquierda = Auxiliar.getSurfaceFromSeparateFiles(imagen_dict_ruta["death"], 0, 7, True, 2)
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
        self.finalizar_animacion_muerte = False


    def update(self, desplazamiento_pantalla, player, grupos_balas, sonido_disparo):
        super().update()  # Llama al método update() de la clase Character

        self.ai(player, grupos_balas, sonido_disparo)  # inteligencia_artificial
        self.update_animation_enemi()
        # desplazar
        self.rect.x += desplazamiento_pantalla
        # Reducir el tiempo de espera para el próximo disparo
        if self.enfriamiento_disparo > 0:
            self.enfriamiento_disparo -= 1
    
    def move(self, direccion=0):
        if direccion == 1:  # derecha
            self.rect.x += self.velocidad
        elif direccion == 2:  # izquierda
            self.rect.x -= self.velocidad


    def ai(self, player, grupo_balas, sonido_disparo):
        if self.vivo and player.vivo:
            if not self.inactivo and random.randint(1, 200) == 1:
                self.update_action(0)  # 0: idle
                self.inactivo = True
                self.contador_inactividad = 50

            # Comprueba si el enemigo está cerca del jugador
            if self.vision.colliderect(player.rect):
                # Detén el movimiento y enfrenta al jugador
                self.move()  # Detén el movimiento (no muevas a izquierda ni derecha)
                self.update_action(0)  # 0: idle
                self.shoot(grupo_balas, sonido_disparo)
            else:
                if not self.inactivo:
                    ai_movimiento_derecha = self.direccion == 1
                    if ai_movimiento_derecha:
                        self.move(1)  # Mover a la derecha
                    else:
                        self.move(2)  # Mover a la izquierda

                    self.update_action(1)  # 1: run
                    self.contador_movimiento += 1
                    # Actualiza la visión del enemigo mientras se mueve
                    self.vision.center = (self.rect.centerx + 75 * self.direccion, self.rect.centery)

                    if self.contador_movimiento > TAMAÑO_BLOQUES:
                        self.direccion *= -1
                        self.contador_movimiento *= -1
                else:
                    self.contador_inactividad -= 1
                    if self.contador_inactividad <= 0:
                        self.inactivo = False

    def update_animation_enemi(self):
        tiempo_enfriamiento = 100
        if self.accion == 0:  # Idle
            if self.direccion == 1:
                self.animacion = self.quieto_derecha
            else:
                self.animacion = self.quieto_izquierda
        elif self.accion == 1:  # Run
            if self.direccion == 1:
                self.animacion = self.correr_derecha
            else:
                self.animacion = self.correr_izquierda
        elif self.accion == 2:  # Jump
            if self.direccion == 1:
                self.animacion = self.saltar_derecha
            else:
                self.animacion = self.saltar_izquierda
        elif self.accion == 3:  # Death
            if self.direccion == 1:
                self.animacion = self.muerte_derecha
            else:
                self.animacion = self.muerte_izquierda

        self.image = self.animacion[self.indice_frame]
        if pygame.time.get_ticks() - self.tiempo_actualizacion > tiempo_enfriamiento:
            self.tiempo_actualizacion = pygame.time.get_ticks()
            if self.indice_frame < len(self.animacion) - 1:
                self.indice_frame += 1
        if self.indice_frame >= len(self.animacion)-1:
            self.indice_frame = 0
        if self.accion == 3 and self.indice_frame == 0: 
                    self.kill()

