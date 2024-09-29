import pygame

class World:
    def __init__(self):
        self.obstacles = [
            pygame.Rect(200, 200, 50, 50),
            pygame.Rect(500, 400, 50, 50)
        ]

    def draw(self, screen):
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, (255, 0, 0), obstacle)
