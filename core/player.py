import pygame 
from core.settings import *

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, obstacle_sprites):
		# Initialize player
		super().__init__(groups)
		
        # Player setup
		self.image = pygame.image.load(get_image_path("player")).convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-26)

        # Movement setup
		self.direction = pygame.math.Vector2()
		self.speed = 5

        # Collision setup
		self.obstacle_sprites = obstacle_sprites

	def input(self):
		# Get keysdown
		keys = pygame.key.get_pressed()

        # Check vertical movement
		if keys[pygame.K_UP]:
			self.direction.y = -1
		elif keys[pygame.K_DOWN]:
			self.direction.y = 1
		else:
			self.direction.y = 0

        # Check horizontal movement
		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
		else:
			self.direction.x = 0

	def move(self,speed):
		# Normalize vector for smooth movement
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

        # Move player
		self.rect.x += self.direction.x * speed
		self.collision("horizontal")
		self.rect.y += self.direction.y * speed
		self.collision("vertical")

	def collision(self,direction):
		# Check for horizontal collision
		if direction == "horizontal":
			for sprite in self.obstacle_sprites:
				if sprite.rect.colliderect(self.rect):
					if self.direction.x > 0:
						self.rect.right = sprite.rect.left
					if self.direction.x < 0:
						self.rect.left = sprite.rect.right

        # Check for vertical collision
		if direction == "vertical":
			for sprite in self.obstacle_sprites:
				if sprite.rect.colliderect(self.rect):
					if self.direction.y > 0:
						self.rect.bottom = sprite.rect.top
					if self.direction.y < 0:
						self.rect.top = sprite.rect.bottom

	def update(self):
		# Update player
		self.input()
		self.move(self.speed)