import numpy as np
import math

class SLAM:
    def __init__(self, initial_grid_width, initial_grid_height):
        self.grid = np.zeros((initial_grid_width, initial_grid_height))
        self.detection_count = np.zeros((initial_grid_width, initial_grid_height))  # Track how many times obstacles are detected
        self.width = initial_grid_width
        self.height = initial_grid_height

    def expand_grid(self, new_width, new_height):
        """Expands the SLAM grid when the robot explores beyond current bounds."""
        new_grid = np.zeros((new_width, new_height))
        detection_count_new = np.zeros((new_width, new_height))  # Expand detection count as well
        new_grid[:self.grid.shape[0], :self.grid.shape[1]] = self.grid  # Copy old grid into new one
        detection_count_new[:self.detection_count.shape[0], :self.detection_count.shape[1]] = self.detection_count  # Copy old detection counts
        self.grid = new_grid
        self.detection_count = detection_count_new
        self.width, self.height = new_width, new_height

    def update(self, position, angle, sensor_data, max_sensor_range=200):
        # Convert robot position to grid coordinates
        grid_x = int(position[0] // 10)
        grid_y = int(position[1] // 10)

        # Expand SLAM grid if necessary
        if grid_x >= self.width or grid_y >= self.height:
            self.expand_grid(max(grid_x + 10, self.width), max(grid_y + 10, self.height))

        # Mark robot's current position as explored
        self.grid[grid_x, grid_y] = 1

        # Simulate clear space and obstacles
        for distance in range(10, sensor_data, 10):
            clear_x = grid_x + int(distance * np.cos(np.radians(angle)) / 10)
            clear_y = grid_y + int(distance * np.sin(np.radians(angle)) / 10)

            # Expand if needed while marking clear space
            if clear_x >= self.width or clear_y >= self.height:
                self.expand_grid(max(clear_x + 10, self.width), max(clear_y + 10, self.height))

            self.grid[clear_x, clear_y] = 1  # Mark as clear space

        # If sensor detects an obstacle within range, mark it
        if sensor_data < max_sensor_range:
            obstacle_x = grid_x + int(sensor_data * np.cos(np.radians(angle)) / 10)
            obstacle_y = grid_y + int(sensor_data * np.sin(np.radians(angle)) / 10)
            
            # Increment detection count for the detected obstacle
            self.detection_count[obstacle_x, obstacle_y] += 1

            # First detection (yellow) -> Confirmed detection (green)
            if self.detection_count[obstacle_x, obstacle_y] == 1:
                self.grid[obstacle_x, obstacle_y] = 2  # First detection
            elif self.detection_count[obstacle_x, obstacle_y] >= 3:
                self.grid[obstacle_x, obstacle_y] = 3  # Confirmed obstacle

    def get_map(self):
        return self.grid
