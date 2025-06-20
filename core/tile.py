import pygame 
from core.settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups):
		# Initialize tile sprite
		super().__init__(groups)
		
        # Tile stup
		self.image = pygame.image.load(get_image_path("rock")).convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)