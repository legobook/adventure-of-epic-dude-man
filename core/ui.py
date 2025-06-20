import pygame
from core.settings import *

class UI:
    def __init__(self):
        # Get the main display surface for drawing UI
        self.display_surface = pygame.display.get_surface()
        # Set the font for UI text
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Setup rectangles for health and energy bars
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # Load weapon graphics into a list
        self.weapon_graphics = []
        self.magic_graphics = []
        
        for weapon in weapon_data.values():
            path = weapon["graphic"]
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)
        
        for magic in magic_data.values():
            magic = pygame.image.load(magic["graphic"]).convert_alpha()
            self.magic_graphics.append(magic)

    def show_bar(self, current, max_amount, bg_rect, color):
        # Draw background bar
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # Convert stat to pixel width for current value
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # Draw the filled bar and border
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        # Render experience points as text
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20  # Right margin
        y = self.display_surface.get_size()[1] - 20  # Bottom margin
        text_rect = text_surf.get_rect(bottomright=(x, y))

        # Draw background for exp, then text, then border
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def selection_box(self, left, top, has_switched):
        # Draw a selectable item box at the given position
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        # Draw a box around the weapon in the corner of the screen
        bg_rect = self.selection_box(10, 630, has_switched)
        # Load the weapon sprite from the list
        weapon_surf = self.weapon_graphics[weapon_index]
        # Center the weapon sprite in the box
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        # Draw the weapon sprite
        self.display_surface.blit(weapon_surf, weapon_rect)
    
    def magic_overlay(self, magic_index, has_switched):
        # Draw a box around the magic in the bottom right corner of the screen
        bg_rect = self.selection_box(80, 635, has_switched)
        # Load the magic sprite from the list
        magic_surf = self.magic_graphics[magic_index]
        # Center the magic sprite in the box
        magic_rect = magic_surf.get_rect(center=bg_rect.center)

        # Draw the magic sprite
        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        # Draw the health bar
        self.show_bar(player.health, player.stats["health"], self.health_bar_rect, HEALTH_COLOR)
        # Draw the energy bar
        self.show_bar(player.energy, player.stats["energy"], self.energy_bar_rect, ENERGY_COLOR)

        # Draw experience points
        self.show_exp(player.exp)

        # Add the weapon overlay in the bottom left corner of the screen
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.magic_overlay(player.magic_index,not player.can_switch_magic)