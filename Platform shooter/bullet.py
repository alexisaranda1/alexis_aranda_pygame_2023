import pygame
from constantes import *
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, direcion, imagen_bala):
		pygame.sprite.Sprite.__init__(self)
		self.velocidad = 10
		self.image = imagen_bala
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direccion = direcion

	def update(self, world, player, grupo_enemigos, grupo_balas):
	
		self.rect.x += (self.direccion * self.velocidad) 
	
		if self.rect.right < 0 or self.rect.left > ANCHO_PANTALLA:
			self.kill()

		collision_list = pygame.sprite.spritecollide(self, world.platform_group, False)
		for obstacle in collision_list:
			self.kill()

		if pygame.sprite.spritecollide(player, grupo_balas, False):
			if player.vivo:
				player.salud -= 5
				self.kill()

		for enemigo in grupo_enemigos:
			if pygame.sprite.spritecollide(enemigo, grupo_balas, False):
				if enemigo.vivo:
					enemigo.salud -= 25
					self.kill()
	def draw(self, pantalla):
		pantalla.blit(self.image, self.rect)
	