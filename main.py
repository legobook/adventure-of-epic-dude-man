import pygame, sys
from core.settings import *
from core.level import Level

class Game:
    def __init__(self):
        # Game setup
        pygame.init()
        
        # Screen setup
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption("Adventure of Epic Dude Man")
        
        # Clock setup
        self.clock = pygame.time.Clock()

        # Level setup
        self.level = Level()
    
    def run(self):
        while True:
            # Handle quit game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Reset screen
            self.screen.fill("black")
            
            # Run level
            self.level.run()
            
            # Update display
            pygame.display.update()
            
            # Tick tock
            self.clock.tick(FPS)

if __name__ == "__main__":
    # Run game
    Game().run()