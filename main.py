import pygame
import math
from robot import Robot
from map import World
from slam import SLAM

# Initialize pygame
pygame.init()

# Set up the display
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('SLAM Simulator')

# Font for telemetry data
font = pygame.font.SysFont("Arial", 18)

# Create robot and world objects
robot = Robot([SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], 0)  # Start robot centered
world = World()  # For obstacle simulation, but not drawing obstacles directly
slam = SLAM(80, 60)  # Start with 80x60 grid for the map

# Colors
BACKGROUND_COLOR = (0, 0, 0)  # Black
CLEAR_SPACE_COLOR = (128, 128, 128)  # Grey for clear space
OBSTACLE_COLOR = (0, 255, 0)  # Green for obstacles
FRONTIER_COLOR = (64, 64, 64)  # Dark grey for frontier
ROBOT_COLOR = (0, 0, 255)  # Blue for robot
PATH_COLOR = (255, 255, 255)  # White for path

# Track robot path (real-world coordinates)
path_points = []

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

    # Centering: Keep the robot centered on the screen
    robot_screen_x = SCREEN_WIDTH // 2
    robot_screen_y = SCREEN_HEIGHT // 2

    # Calculate offset based on robot's position relative to the grid
    grid_min_x, grid_min_y = slam.min_x, slam.min_y  # Get current grid boundaries

    # Adjust the map offset based on robot's position relative to map boundaries
    offset_x = robot_screen_x - (robot.position[0] - grid_min_x * 10)
    offset_y = robot_screen_y - (robot.position[1] - grid_min_y * 10)

    # Store robot's current real-world position for the path
    path_points.append((robot.position[0], robot.position[1]))

    # Draw the SLAM map (only what the robot has detected)
    slam_map = slam.get_map()
    for x in range(slam_map.shape[0]):
        for y in range(slam_map.shape[1]):
            rect_x = x * 10 + offset_x
            rect_y = y * 10 + offset_y

            if slam_map[x, y] == 1:  # Clear space (grey)
                pygame.draw.rect(screen, CLEAR_SPACE_COLOR, pygame.Rect(rect_x, rect_y, 10, 10), 1)
            elif slam_map[x, y] == 2:  # Obstacle (green)
                pygame.draw.rect(screen, OBSTACLE_COLOR, pygame.Rect(rect_x, rect_y, 10, 10))
            elif slam_map[x, y] == 3:  # Frontier (dark grey)
                pygame.draw.rect(screen, FRONTIER_COLOR, pygame.Rect(rect_x, rect_y, 10, 10), 1)

    # Draw the robot's path using the real-world positions, but offset to keep it centered
    if len(path_points) > 1:
        transformed_path = [(x - grid_min_x * 10 + offset_x, y - grid_min_y * 10 + offset_y) for (x, y) in path_points]
        pygame.draw.lines(screen, PATH_COLOR, False, transformed_path, 2)  # Draw robot's path

    # Draw the robot at the center of the screen
    pygame.draw.circle(screen, ROBOT_COLOR, (robot_screen_x, robot_screen_y), robot.radius)
    line_length = robot.radius + 10
    direction_x = robot_screen_x + line_length * math.cos(math.radians(robot.angle))
    direction_y = robot_screen_y + line_length * math.sin(math.radians(robot.angle))
    pygame.draw.line(screen, (255, 255, 255), (robot_screen_x, robot_screen_y), (direction_x, direction_y), 2)

    # Display telemetry data (angle, position)
    telemetry_text = font.render(f"Angle: {robot.angle:.2f}°  |  Position: ({int(robot.position[0])}, {int(robot.position[1])})", True, (255, 255, 255))
    screen.blit(telemetry_text, (10, 10))  # Display the text on screen at position (10,10)

    # Update the display
    pygame.display.flip()

    # Small delay to control the frame rate
    pygame.time.delay(30)

pygame.quit()
