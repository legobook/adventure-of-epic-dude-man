import pygame
from core.settings import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        # Initialize tile sprite
        super().__init__(groups)
        direction = player.status.split("_")[0]

        # Weapon setup
        self.image = pygame.image.load(get_image_path(f"weapons/{player.weapon}/{direction}")).convert_alpha()
        print(get_image_path(f"weapons/{player.weapon}/{direction}"))
        
        # Placements
        if direction == "right":
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
        elif direction == "left": 
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
        elif direction == "down":
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0))
        else:
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0))