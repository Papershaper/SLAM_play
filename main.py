import pygame
from robot import Robot
from map import World
from slam import SLAM

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('SLAM Simulator')

# Create robot and world objects
robot = Robot([400, 300], 0)
world = World()
slam = SLAM(80, 60)  # 80x60 grid for the map

# Colors
BACKGROUND_COLOR = (0, 0, 0)  # Black
CLEAR_SPACE_COLOR = (128, 128, 128)  # Grey for clear space
OBSTACLE_COLOR = (0, 255, 0)  # Green for obstacles
FRONTIER_COLOR = (64, 64, 64)  # Dark grey for frontier
ROBOT_COLOR = (0, 0, 255)  # Blue for robot

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Exit on pressing the Escape key or 'Q'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False

    # Handle robot movement via keyboard input
    robot.handle_input()

    # Get sensor data and update SLAM map
    sensor_data = robot.simulate_ultrasonic(world.obstacles)
    slam.update(robot.position, robot.angle, sensor_data)

    # Clear the screen with background color
    screen.fill(BACKGROUND_COLOR)

    # Draw the world (obstacles)
    world.draw(screen)

    # Draw the robot
    robot.draw(screen)

    # Draw the SLAM map
    slam_map = slam.get_map()
    for x in range(slam_map.shape[0]):
        for y in range(slam_map.shape[1]):
            if slam_map[x, y] == 1:  # Clear space (grey)
                pygame.draw.rect(screen, CLEAR_SPACE_COLOR, pygame.Rect(x * 10, y * 10, 10, 10), 1)
            elif slam_map[x, y] == 2:  # Obstacle (green dot)
                pygame.draw.rect(screen, OBSTACLE_COLOR, pygame.Rect(x * 10, y * 10, 10, 10))
            elif slam_map[x, y] == 3:  # Frontier (dark grey)
                pygame.draw.rect(screen, FRONTIER_COLOR, pygame.Rect(x * 10, y * 10, 10, 10), 1)

    # Update the display
    pygame.display.flip()

    # Small delay to control the frame rate
    pygame.time.delay(30)

pygame.quit()
