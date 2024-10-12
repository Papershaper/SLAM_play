import pygame
import math

class Robot:
    def __init__(self, position, angle):
        self.position = position
        self.angle = angle
        self.speed = 2  # Movement speed (adjust as needed)
        self.rotation_speed = 2  # Rotation speed (adjust as needed)
        self.radius = 20  # Robot size (visual purposes)

    def handle_input(self):
        """Handles the robot's movement based on keyboard input."""
        keys = pygame.key.get_pressed()

        # Move forward
        if keys[pygame.K_UP]:
            self.position[0] += self.speed * math.cos(math.radians(self.angle))
            self.position[1] += self.speed * math.sin(math.radians(self.angle))

        # Move backward
        if keys[pygame.K_DOWN]:
            self.position[0] -= self.speed * math.cos(math.radians(self.angle))
            self.position[1] -= self.speed * math.sin(math.radians(self.angle))

        # Rotate left
        if keys[pygame.K_LEFT]:
            self.angle -= self.rotation_speed
            if self.angle < 0:
                self.angle += 360

        # Rotate right
        if keys[pygame.K_RIGHT]:
            self.angle += self.rotation_speed
            if self.angle >= 360:
                self.angle -= 360

    def simulate_ultrasonic(self, obstacles):
        """Simulates an ultrasonic sensor by detecting obstacles in the robot's direction."""
        max_distance = 200  # Maximum range of the ultrasonic sensor
        step_size = 5  # Step size for sensor simulation

        # Scan forward in steps to check for obstacles
        for distance in range(0, max_distance, step_size):
            x = self.position[0] + distance * math.cos(math.radians(self.angle))
            y = self.position[1] + distance * math.sin(math.radians(self.angle))

            # Check for collision with any obstacle
            for obstacle in obstacles:
                if obstacle.collidepoint(x, y):
                    return distance  # Return distance to the obstacle

        return max_distance  # No obstacle detected within max range
