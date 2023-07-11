import pygame
from auxiliar import Auxiliar
from character import *
from constantes import *
class Player(Character): # jugador
    def __init__(self, x, y, velocidad, municion, granadas,imagen_dict_ruta):
        super().__init__(x, y, velocidad)
        
        self.quieto_derecha= Auxiliar.getSurfaceFromSeparateFiles(imagen_dict_ruta["idle"], 1, 4,False)
        self.quieto_izquierda = Auxiliar.getSurfaceFromSeparateFiles(imagen_dict_ruta["idle"], 1, 4,True) 
        self.correr_derecha= Auxiliar.getSurfaceFromSeparateFiles(imagen_dict_ruta["run"], 1, 5)
        self.correr_izquierda = Auxiliar.getSurfaceFromSeparateFiles(imagen_dict_ruta["run"], 1, 5, True)
        self.saltar_derecha = Auxiliar.getSurfaceFromSeparateFiles(imagen_dict_ruta["jum"], 0, 1,True ,2)
        self.saltar_izquierda = Auxiliar.getSurfaceFromSeparateFiles(imagen_dict_ruta["jum"], 0, 1, True,2)
        self.muerte_derecha = Auxiliar.getSurfaceFromSeparateFiles(imagen_dict_ruta["death"], 0, 1, False, 2)
        self.muerte_izquierda = Auxiliar.getSurfaceFromSeparateFiles(imagen_dict_ruta["death"], 0, 1, True, 2)
        self.indice_frame = 0
        self.bandera = True
        self.posicion_inicial_x = x
        self.posicion_inicial_y = y
        self.animacion = self.quieto_derecha
        self.image = self.animacion[self.indice_frame]
        self.rect = self.image.get_rect()  
        self.rect.center = (x, y)
        self.rect.width -= 5 
        self.ancho = self.image.get_width()  
        self.alto = self.image.get_height()  
        self.municion = municion  
        self.municion_inicial = municion 
        self.enfriamiento_disparo = 0  
        self.granadas = granadas  # granadas
        self.movimiento_izquierdo = False
        self.movimiento_derecha = False
        self.diparar = False
        self.en_suelo = False
        self.player = True
        self.saltar = False
        self.en_aire = False 
        self.scoree = 0
        
    def jum(self):
        if self.saltar  and self.en_suelo:
            self.indice_frame = 0
            self.vel_y = -12
            self.saltar = False
            self.en_aire = True
            self.en_suelo = False
        else:
            self.en_aire = False

    def move_left(self):
        if self.movimiento_izquierdo :
            self.vel_x = -self.velocidad
            self.indice_frame = 0
            self.direccion = -1
    def move_right(self):
        if self.movimiento_derecha:
            self.vel_x = self.velocidad
            self.indice_frame = 0
            self.direccion = 1
    def handle_key_events(self, lista_event,grupo_balas,sonido_disparo):
      
        for event in lista_event:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.movimiento_izquierdo = True
                elif event.key == pygame.K_d:
                    self.movimiento_derecha = True
                elif event.key == pygame.K_SPACE:
                    print(self.scoree)
                    self.shoot(grupo_balas, sonido_disparo)
                elif event.key == pygame.K_w and self.vivo:
                    self.saltar = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.movimiento_izquierdo = False   
                elif event.key == pygame.K_d:
                    self.movimiento_derecha = False
                elif event.key == pygame.K_w and self.vivo:
                    self.saltar = False
         
   
                       
    def update_position(self, desplazamiento_pantalla):
        self.rect.x += desplazamiento_pantalla
        self.x += desplazamiento_pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > ANCHO_PANTALLA:
            self.rect.right = ANCHO_PANTALLA
        elif self.rect.y > ALTO_PANTALLA:
            self.salud = 0
            
    def update(self):
        super().update()
        if not self.movimiento_izquierdo and not self.movimiento_derecha:
            self.vel_x = 0
        self.jum()
        self.move_left()
        self.move_right()
        self.check_alive()
       
        self.update_animation_player()
       
    def update_animation_player(self):
        tiempo_enfriamiento = 100

        if not self.en_suelo:
            if self.direccion == 1:
                self.animacion = self.quieto_derecha
            else:
                self.animacion = self.quieto_izquierda

        elif self.movimiento_izquierdo or self.movimiento_derecha:
            if self.direccion == 1:
                self.animacion = self.correr_derecha
            else:
                self.animacion = self.correr_izquierda
        elif  not self.vivo:
            if self.direccion == 1:
                self.animacion = self.muerte_derecha
            else:
                self.animacion = self.muerte_izquierda
        else:
            if self.direccion == 1:
                self.animacion = self.quieto_derecha
            else:
                self.animacion = self.quieto_izquierda

        if pygame.time.get_ticks() - self.tiempo_actualizacion > tiempo_enfriamiento:
            self.tiempo_actualizacion = pygame.time.get_ticks()
            self.indice_frame += 1

        if self.indice_frame >= len(self.animacion):
            self.indice_frame = 0

    def take_damage(self, cantidad):
        self.salud -= cantidad
        if self.salud <= 0:
            self.salud = 0

    def shooting(self, grupo_balas, shot_fx):
            bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direccion), self.rect.centery, self.direccion, bullet_img)
            grupo_balas.add(bullet)
            print("esta disparando")
            self.municion -= 1
            shot_fx.play()

