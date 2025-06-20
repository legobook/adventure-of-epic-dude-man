import pygame 
from core.settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
		# Initialize tile sprite
		super().__init__(groups)
		
        # Tile stup
		self.sprite_type = sprite_type
		self.image = surface
		
		if sprite_type == "object":
			self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - TILESIZE))
		else:
			self.rect = self.image.get_rect(topleft = pos)
			
		self.hitbox = self.rect.inflate(0, -10)