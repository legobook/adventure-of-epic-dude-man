import pygame
import random
from core.settings import *
from core.tile import Tile
from core.player import Player
from core.weapon import Weapon
from core.ui import UI

class Level:
    def __init__(self):
        # Level setup
        self.display_surface = pygame.display.get_surface()

        # Sprite groups
        self.visible_sprites = Camera()
        self.obstacle_sprites = pygame.sprite.Group()

        # Current attack
        self.current_attack = None

        # Map setup
        self.create_map()

        # User interface
        self.ui = UI()

    def create_map(self):
        # Load map layouts
        layouts = {
            "boundary": import_csv_layout(get_map_path("floor")),
            "grass": import_csv_layout(get_map_path("grass")),
            "object": import_csv_layout(get_map_path("objects")),
        }

        # Load graphics for grass and objects
        graphics = {
            "grass": import_folder("grass"),
            "objects": import_folder("objects")
        }

        # Iterate through each layout type
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            # Create invisible boundary tile
                            Tile((x, y), [self.obstacle_sprites], "invisible")
                        if style == "grass":
                            # Create grass tile with random image
                            random_grass_image = random.choice(graphics["grass"])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], "grass", random_grass_image)
                        if style == "object":
                            # Create object tile with corresponding image
                            surf = graphics["objects"][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], "object", surf)
        
        # Create player
        self.player = Player((2000, 1430), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack, self.create_magic)
    
    def create_attack(self):
        # Create a weapon attack and add it to visible sprites
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self):
        # Remove the current weapon attack if it exists
        if self.current_attack:
            self.current_attack.kill()

        self.current_attack = None
    
    def create_magic(self, style, strength, cost):
        # Create a magic attack and add it to visible sprites
        print(style)
        print(strength)
        print(cost)

    def run(self):
        # Update and render game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)

class Camera(pygame.sprite.Group):
    def __init__(self):
        # Initialize camera 
        super().__init__()
        
        # Camera setup
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Floor setup
        self.floor_surf = pygame.image.load(get_image_path("ground")).convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))

    def custom_draw(self, player):
        # Calculate offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Draw floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        # Draw sprites with offset
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)