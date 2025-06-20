import pygame 
from core.settings import *
from core.tile import Tile
from core.player import Player

class Level:
	def __init__(self):
		# Level setup
		self.display_surface = pygame.display.get_surface()

		# Sprite groups
		self.visible_sprites = Camera()
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
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()

class Camera(pygame.sprite.Group):
	def __init__(self):
		# Initialize camera 
		super().__init__()
		
        # Camera setup
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

	def custom_draw(self, player):
		# Calculate offset
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		# Draw sprites with offset
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)