import pygame

class World:
    def __init__(self):
        self.width = 1000  # Define the world width
        self.height = 1000  # Define the world height

        # World boundaries (obstacles)
        self.obstacles = [
            pygame.Rect(0, 0, self.width, 10),  # Top boundary
            pygame.Rect(0, 0, 10, self.height),  # Left boundary
            pygame.Rect(0, self.height - 10, self.width, 10),  # Bottom boundary
            pygame.Rect(self.width - 10, 0, 10, self.height),  # Right boundary
            pygame.Rect(200, 200, 50, 50),  #Object 1
            pygame.Rect(500, 400, 50, 50)  #Object 2
        ]

    def draw(self, screen):
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, (255, 0, 0), obstacle)  # Draw the world boundary obstacles in red