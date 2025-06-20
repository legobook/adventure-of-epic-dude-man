from csv import reader
import os
import pygame

# Game setup
WIDTH    = 1280	
HEIGTH   = 720
FPS      = 60
TILESIZE = 64

def get_image_path(name):
    # Get image path
    return os.path.join("assets", "images", f"{name}.png")

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
