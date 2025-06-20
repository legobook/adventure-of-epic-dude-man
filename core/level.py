import pygame 
from core.settings import *
from core.tile import Tile
from core.player import Player

class Level:
	def __init__(self):
		# Level setup
		self.display_surface = pygame.display.get_surface()

		# Sprite groups
		self.visible_sprites = pygame.sprite.Group()
		self.obstacle_sprites = pygame.sprite.Group()

		# Map setup
		self.create_map()

	def create_map(self):
		for row_index,row in enumerate(WORLD_MAP):
			for col_index, col in enumerate(row):
				# Get tile position
				x = col_index * TILESIZE
				y = row_index * TILESIZE
				
				if col == "x":
					# Create tile
					Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
				if col == "p":
					# Create player
					self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites)

	def run(self):
		# Update and render game
		self.visible_sprites.draw(self.display_surface)
		self.visible_sprites.update()