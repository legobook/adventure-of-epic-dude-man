import os
import pygame
from csv import reader
from core.settings import *

def get_image_path(name):
    # Get image path
    return os.path.join("assets", "images", f"{name}.png")

def get_sound_path(name):
    # Get sound path
    return os.path.join("assets", "audio", f"{name}.wav")

def get_map_path(name):
    # Get map path
    return os.path.join("assets", "map", f"{name}.csv")

def import_csv_layout(path):
    # Initialize an empty list to store the terrain map
    terrain_map = []
    # Open the CSV file at the given path
    with open(path) as level_map:
        # Read the CSV file with comma as delimiter
        layout = reader(level_map, delimiter=",")
        # Iterate over each row in the CSV
        for row in layout:
            # Convert the row to a list and append to terrain_map
            terrain_map.append(list(row))
        # Return the completed terrain map
        return terrain_map

def import_folder(name):
    path = os.path.join("assets", "images", name)
    surface_list = []  # List to store loaded images

    # Walk through the directory to get image files
    for _, _, img_files in os.walk(path):
        for image in img_files:
            full_path = path + "/" + image  # Construct full file path
            image_surf = pygame.image.load(full_path).convert_alpha()  # Load image with transparency
            surface_list.append(image_surf)  # Add image surface to list

    return surface_list  # Return list of loaded images


# Game setup
WIDTH    = 1280	
HEIGTH   = 720
FPS      = 60
TILESIZE = 64

# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = os.path.join("assets", "font.ttf")
UI_FONT_SIZE = 18

# General colors
WATER_COLOR = "#71ddee"
UI_BG_COLOR = "#222222"
UI_BORDER_COLOR = "#111111"
TEXT_COLOR = "#EEEEEE"

# UI colors
HEALTH_COLOR = "red"
ENERGY_COLOR = "blue"
UI_BORDER_COLOR_ACTIVE = "gold"

# Weapon data
weapon_data = {
    "sword": {"cooldown": 100, "damage": 15, "graphic": get_image_path("weapons/sword/full")},
    "lance": {"cooldown": 400, "damage": 30, "graphic": get_image_path("weapons/lance/full")},
    "axe": {"cooldown": 300, "damage": 20, "graphic": get_image_path("weapons/axe/full")},
    "rapier": {"cooldown": 50, "damage": 8, "graphic": get_image_path("weapons/rapier/full")},
    "sai": {"cooldown": 80, "damage": 10, "graphic": get_image_path("weapons/sai/full")}
}

# Magic data
magic_data = {
    "flame": {"strength": 5, "cost": 20, "graphic": get_image_path("particles/flame/fire")},
    "heal" : {"strength": 20, "cost": 10, "graphic": get_image_path("particles/heal/heal")}
}

# Enemy data
monster_data = {
    "squid": {"health": 100, "exp": 100, "damage": 20, "attack_type": "slash", "attack_sound": get_sound_path("slash"), "speed": 3, "resistance": 3, "attack_radius": 80, "notice_radius": 360},
    "raccoon": {"health": 300, "exp": 250, "damage": 40, "attack_type": "claw", "attack_sound": get_sound_path("claw"), "speed": 2, "resistance": 3, "attack_radius": 120, "notice_radius": 400},
    "spirit": {"health": 100, "exp": 110, "damage": 8, "attack_type": "thunder", "attack_sound": get_sound_path("fireball"), "speed": 4, "resistance": 3, "attack_radius": 60, "notice_radius": 350},
    "bamboo": {"health": 70, "exp": 120, "damage": 6, "attack_type": "leaf_attack", "attack_sound": get_sound_path("slash"), "speed": 3, "resistance": 3, "attack_radius": 50, "notice_radius": 300}
}