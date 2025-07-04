import pygame
from core.settings import *
from core.entity import Entity

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player):
        # Initialize enemy
        super().__init__(groups)
        self.sprite_type = "enemy"

        # Enemy setup
        self.import_graphics(monster_name)
        self.status = "idle"
        self.image = self.animations[self.status][self.frame_index]

        # Movement setup
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # Stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info["health"]
        self.exp = monster_info["exp"]
        self.speed = monster_info["speed"]
        self.attack_damage = monster_info["damage"]
        self.attack_type = monster_info["attack_type"]
        self.resistance = monster_info["resistance"]
        self.attack_radius = monster_info["attack_radius"]
        self.notice_radius = monster_info["notice_radius"]

        # Player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player

        # Invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

    def import_graphics(self, name):
        self.animations = {"idle": [], "move": [], "attack": []}
        
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(f"monsters/{name}/{animation}")

    def get_player_distance_direction(self, player):
        # Find the distance and direction to the player
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        # Determine the status of the enemy
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != "attack":
                self.frame_index = 0
            self.status = "attack"
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"

    def actions(self, player):
        # Perform an action based on the status
        if self.status == "attack":
            self.attack_time = pygame.time.get_ticks()
            print(self.health)
        elif self.status == "move":
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        # Animate the enemy
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == "attack":
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def cooldowns(self):
        # Handle cooldown for attacks
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
    
    def get_damage(self, player, attack_type):
        # Take damage from the player
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == "weapon":
                self.health -= player.get_full_weapon_damage()
            # Magic damage 
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        # Check if the enemy is dead
        if self.health <= 0:
            self.kill()

    def hit_reaction(self):
        # Enemy is hit and should react
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        # Update the enemy
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player):
        # Update the enemy
        self.get_status(player)
        self.actions(player)