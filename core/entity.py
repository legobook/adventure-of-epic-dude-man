import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        # Initialize entity
        super().__init__(groups)

        # Entity setup
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        # Normalize the direction vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Move the hitbox
        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")

        # Update the rect based on the hitbox
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        # Check for collision with obstacles in the given direction
        if direction == "horizontal":
            # Check for collision with obstacles to the left or right
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            # Check for collision with obstacles above or below
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom