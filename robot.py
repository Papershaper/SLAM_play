import pygame
import math

class Robot:
    def __init__(self, position, angle):
        self.position = position
        self.angle = angle
        self.speed = 2
        self.rotation_speed = 2
        self.radius = 20

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.position[0] += self.speed * math.cos(math.radians(self.angle))
            self.position[1] += self.speed * math.sin(math.radians(self.angle))
        if keys[pygame.K_DOWN]:
            self.position[0] -= self.speed * math.cos(math.radians(self.angle))
            self.position[1] -= self.speed * math.sin(math.radians(self.angle))
        if keys[pygame.K_LEFT]:
            self.angle -= self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.angle += self.rotation_speed

    def simulate_ultrasonic(self, obstacles):
        max_distance = 200
        step_size = 5

        for distance in range(0, max_distance, step_size):
            x = self.position[0] + distance * math.cos(math.radians(self.angle))
            y = self.position[1] + distance * math.sin(math.radians(self.angle))

            for obstacle in obstacles:
                if obstacle.collidepoint(x, y):
                    return distance
        return max_distance

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), (int(self.position[0]), int(self.position[1])), self.radius)
        line_length = self.radius + 10
        direction_x = self.position[0] + math.cos(math.radians(self.angle)) * line_length
        direction_y = self.position[1] + math.sin(math.radians(self.angle)) * line_length
        pygame.draw.line(screen, (255, 255, 255), self.position, (direction_x, direction_y), 2)
