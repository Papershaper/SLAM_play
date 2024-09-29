import numpy as np
import math

class SLAM:
    def __init__(self, grid_width, grid_height):
        self.grid = np.zeros((grid_width, grid_height))

    def update(self, position, angle, sensor_data, max_sensor_range=200):
        grid_x = int(position[0] // 10)
        grid_y = int(position[1] // 10)

        # Ensure grid_x and grid_y are within bounds
        grid_x = max(0, min(grid_x, self.grid.shape[0] - 1))
        grid_y = max(0, min(grid_y, self.grid.shape[1] - 1))

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
