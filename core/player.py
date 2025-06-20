import pygame
from core.settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        # Initialize player
        super().__init__(groups)

        # Player setup
        self.image = pygame.image.load(get_image_path("player/down_idle/idle_down")).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # Animation setup
        self.import_player_assets()
        self.status = "down"
        self.frame_index = 0
        self.animation_speed = 0.15

        # Movement setup
        self.direction = pygame.math.Vector2()
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        # Weapon setup
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # Magic setup
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # Collision setup
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.stats = {"health": 100, "energy": 60, "attack": 10, "magic": 4, "speed": 5}
        self.health = self.stats["health"] * 0.5
        self.energy = self.stats["energy"] * 0.8
        self.exp = 123
        self.speed = self.stats["speed"]

    def import_player_assets(self):
        # Initialize a dictionary to hold animation frames for each player state
        self.animations = {
            "up": [], "down": [], "left": [], "right": [],
            "right_idle": [], "left_idle": [], "up_idle": [], "down_idle": [],
            "right_attack": [], "left_attack": [], "up_attack": [], "down_attack": []
        }

        # Load animation frames for each state using import_folder
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(f"player/{animation}")

    def input(self):
        if not self.attacking:
            # Get keysdown
            keys = pygame.key.get_pressed()

            # Check vertical movement
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            # Check horizontal movement
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = "right"
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0
            
            # Attack
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            # Magic
            if keys[pygame.K_LCTRL]:
                # Set player to attacking mode
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()

                # Get magic style, strength, and cost
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']

                # Create the magic
                self.create_magic(style, strength, cost)
            
            # Weapon switch
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                
                # Cycle to the next weapon
                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                    
                # Update which weapon the player is using
                self.weapon = list(weapon_data.keys())[self.weapon_index]
            
            # Magic switch
            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                
                # Cycle to next magic
                self.magic_index = (self.magic_index + 1) % len(list(magic_data.keys()))
                self.magic = list(magic_data.keys())[self.magic_index]
    
    def get_status(self):
        # If not moving, set to idle if not already idle or attacking
        if self.direction.x == 0 and self.direction.y == 0:
            if "idle" not in self.status and "attack" not in self.status:
                self.status = self.status + "_idle"

        # If attacking, stop movement and set attack status
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if "attack" not in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            # If attack finished, revert to non-attack status
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Move hitbox instead of rect
        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        # Check for horizontal collision
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        # Check for vertical collision
        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
    
    def cooldowns(self):
        # Get the current time
        current_time = pygame.time.get_ticks()

        # Check if attack cooldown has passed
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()
        
        # Check if weapon switch cooldown has passed
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True
        
        # Check if magic switch cooldown has passed
        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

    def animate(self):
        # Get the current animation frames for the player"s status
        animation = self.animations[self.status]

        # Increment the frame index for animation speed
        self.frame_index += self.animation_speed
        # Loop the animation if at the end
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Update the player"s image to the current animation frame
        self.image = animation[int(self.frame_index)]
        # Update the rect to keep the player centered
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        # Update player
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)