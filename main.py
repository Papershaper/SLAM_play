import pygame
import math
from robot import Robot
from map import World
from slam import SLAM

# Initialize pygame
pygame.init()

# Set up the display for a vertical aspect ratio (YouTube short format)
SCREEN_WIDTH, SCREEN_HEIGHT = 720, 1280
UI_HEIGHT = 150  # Height reserved for the UI telemetry at the top
MAP_HEIGHT = SCREEN_HEIGHT - UI_HEIGHT  # The remaining height for the simulated map

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('SLAM Simulator')

# Font for telemetry data
font = pygame.font.SysFont("Arial", 24)

# Create robot and world objects
robot = Robot([SCREEN_WIDTH // 2, UI_HEIGHT + MAP_HEIGHT // 2], 0)  # Start robot in the center of the map area
world = World()  # Define the world bounds
slam = SLAM(80, 60)  # Start with 80x60 grid for the map

# Colors
BACKGROUND_COLOR = (0, 0, 0)  # Black for map background
UI_BACKGROUND_COLOR = (50, 50, 50)  # Darker grey for UI section
TEXT_COLOR = (255, 255, 255)  # White text for telemetry
CLEAR_SPACE_COLOR = (128, 128, 128)  # Grey for clear space
OBSTACLE_FIRST_DETECTED_COLOR = (255, 255, 0)  # Yellow for first detection of obstacle
OBSTACLE_CONFIRMED_COLOR = (0, 255, 0)  # Green for confirmed obstacles
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

    # Draw the UI section at the top
    pygame.draw.rect(screen, UI_BACKGROUND_COLOR, pygame.Rect(0, 0, SCREEN_WIDTH, UI_HEIGHT))
    
    # Add description about the ultrasonic sensor
    sensor_text = font.render("Robot: 1 forward ultrasonic sensor", True, TEXT_COLOR)
    screen.blit(sensor_text, (10, 10))
    
    # Display telemetry data in the UI section
    telemetry_text = font.render(f"Angle: {robot.angle:.2f}° | Position: ({int(robot.position[0])}, {int(robot.position[1])})", True, TEXT_COLOR)
    screen.blit(telemetry_text, (10, 50))

    # Track robot's path (append to the path array)
    path_points.append((robot.position[0], robot.position[1]))

    # Centering: Keep the robot centered in the map area
    robot_screen_x = SCREEN_WIDTH // 2
    robot_screen_y = UI_HEIGHT + MAP_HEIGHT // 2

    # Calculate offset based on robot's position relative to the grid
    offset_x = SCREEN_WIDTH // 2 - robot.position[0]
    offset_y = UI_HEIGHT + MAP_HEIGHT // 2 - robot.position[1]

    # Draw the SLAM map (only what the robot has detected)
    slam_map = slam.get_map()
    for x in range(slam_map.shape[0]):
        for y in range(slam_map.shape[1]):
            rect_x = x * 10 + offset_x
            rect_y = y * 10 + offset_y

            if rect_y > UI_HEIGHT:  # Ensure map is drawn below the UI section
                if slam_map[x, y] == 1:  # Clear space (grey)
                    pygame.draw.rect(screen, CLEAR_SPACE_COLOR, pygame.Rect(rect_x, rect_y, 10, 10), 1)
                elif slam_map[x, y] == 2:  # First detected obstacle (yellow)
                    pygame.draw.rect(screen, OBSTACLE_FIRST_DETECTED_COLOR, pygame.Rect(rect_x, rect_y, 10, 10))
                elif slam_map[x, y] == 3:  # Confirmed obstacle (green)
                    pygame.draw.rect(screen, OBSTACLE_CONFIRMED_COLOR, pygame.Rect(rect_x, rect_y, 10, 10))

    # Draw robot's path using the real-world positions
    if len(path_points) > 1:
        transformed_path = [(x - robot.position[0] + robot_screen_x, y - robot.position[1] + robot_screen_y) for (x, y) in path_points]
        pygame.draw.lines(screen, PATH_COLOR, False, transformed_path, 2)

    # Draw the robot at the center of the map area
    pygame.draw.circle(screen, ROBOT_COLOR, (robot_screen_x, robot_screen_y), robot.radius)
    line_length = robot.radius + 10
    direction_x = robot_screen_x + line_length * math.cos(math.radians(robot.angle))
    direction_y = robot_screen_y + line_length * math.sin(math.radians(robot.angle))
    pygame.draw.line(screen, (255, 255, 255), (robot_screen_x, robot_screen_y), (direction_x, direction_y), 2)

    # Update the display
    pygame.display.flip()

    # Small delay to control the frame rate
    pygame.time.delay(30)

pygame.quit()
