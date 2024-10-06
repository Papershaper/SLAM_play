import numpy as np
import math

class SLAM:
    def __init__(self, initial_grid_width, initial_grid_height):
        # Start with an initial grid and keep track of boundaries
        self.grid = np.zeros((initial_grid_width, initial_grid_height))
        self.min_x, self.max_x = 0, initial_grid_width - 1
        self.min_y, self.max_y = 0, initial_grid_height - 1

    def expand_grid(self, new_min_x, new_max_x, new_min_y, new_max_y):
        """Expands the grid when the robot explores beyond the current boundaries."""
        # Calculate new grid dimensions
        new_width = new_max_x - new_min_x + 1
        new_height = new_max_y - new_min_y + 1

        # Create a new grid with the new dimensions and fill it with unexplored space (0)
        new_grid = np.zeros((new_width, new_height))

        # Copy the old grid into the new one, with adjusted coordinates
        old_width, old_height = self.grid.shape
        new_grid[(self.min_x - new_min_x):(self.min_x - new_min_x + old_width),
                 (self.min_y - new_min_y):(self.min_y - new_min_y + old_height)] = self.grid

        # Update grid and boundaries
        self.grid = new_grid
        self.min_x, self.max_x = new_min_x, new_max_x
        self.min_y, self.max_y = new_min_y, new_max_y

    def update(self, position, angle, sensor_data, max_sensor_range=200):
        # Convert position to grid indices
        grid_x = int(position[0] // 10)
        grid_y = int(position[1] // 10)

        # Check if we need to expand the grid
        if grid_x < self.min_x or grid_x > self.max_x or grid_y < self.min_y or grid_y > self.max_y:
            new_min_x = min(self.min_x, grid_x - 1)
            new_max_x = max(self.max_x, grid_x + 1)
            new_min_y = min(self.min_y, grid_y - 1)
            new_max_y = max(self.max_y, grid_y + 1)
            self.expand_grid(new_min_x, new_max_x, new_min_y, new_max_y)

        # Adjust coordinates after expansion
        grid_x = grid_x - self.min_x
        grid_y = grid_y - self.min_y

        # Mark the robot's current position as explored
        self.grid[grid_x, grid_y] = 1

        # Simulate clear space (grey line)
        for distance in range(10, sensor_data, 10):
            clear_x = grid_x + int(distance * np.cos(np.radians(angle)) / 10)
            clear_y = grid_y + int(distance * np.sin(np.radians(angle)) / 10)

            clear_x = max(0, min(clear_x, self.grid.shape[0] - 1))
            clear_y = max(0, min(clear_y, self.grid.shape[1] - 1))

            self.grid[clear_x, clear_y] = 1  # Mark clear space

        # If the sensor detects something within range, mark the obstacle
        if sensor_data < max_sensor_range:
            obstacle_x = grid_x + int(sensor_data * np.cos(np.radians(angle)) / 10)
            obstacle_y = grid_y + int(sensor_data * np.sin(np.radians(angle)) / 10)

            obstacle_x = max(0, min(obstacle_x, self.grid.shape[0] - 1))
            obstacle_y = max(0, min(obstacle_y, self.grid.shape[1] - 1))

            self.grid[obstacle_x, obstacle_y] = 2  # Mark as obstacle
        else:
            # If no obstacle is detected, mark the frontier (dark grey) if not already explored
            frontier_x = grid_x + int(max_sensor_range * np.cos(np.radians(angle)) / 10)
            frontier_y = grid_y + int(max_sensor_range * np.sin(np.radians(angle)) / 10)

            frontier_x = max(0, min(frontier_x, self.grid.shape[0] - 1))
            frontier_y = max(0, min(frontier_y, self.grid.shape[1] - 1))

            # Only mark as frontier if the space hasn't been marked as clear or obstacle
            if self.grid[frontier_x, frontier_y] == 0:  # Unexplored space
                self.grid[frontier_x, frontier_y] = 3  # Mark as frontier

    def get_map(self):
        return self.grid
