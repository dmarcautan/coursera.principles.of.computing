"""
Clone of 2048 game.

@author: Dmitry Marcautsan
"""

import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    merged = line[:]
    iterations = len(merged) - 1
    iteration = 0
    
    while iteration < iterations:
        next_index = iteration + 1
        while next_index < len(merged) - 1 and merged[next_index] == 0:
            next_index += 1
            
        if merged[iteration] == 0:
            merged[iteration] = merged[next_index]
            merged[next_index] = 0
            if next_index == iterations:
                break
        elif merged[iteration] == merged[next_index]:
            merged[iteration] = 2 * merged[next_index]
            merged[next_index] = 0
            iteration += 1
        else:
            iteration += 1
            
        
        
    return merged

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_width = grid_width
        self._grid_height = grid_height
        self._initials = {UP: [(0, y) for y in range(grid_width)],
                          DOWN: [(grid_height - 1, y) for y in range(grid_width)],
                          LEFT: [(x, 0) for x in range(grid_height)],
                          RIGHT: [(x, grid_width - 1) for x in range(grid_height)]}
        self.reset()
        
    def reset(self):
        """
        Reset the game so the _grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for _ in range(self._grid_width)] for _ in range(self._grid_height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the _grid for debugging.
        """
        return "\n".join([str(x) for x in self._grid])

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        moved = False
        start_indices = self._initials[direction]
        for index in start_indices:
            current_index = index
            line = []
            
            while 0 <= current_index[0] < self._grid_height and 0 <= current_index[1] < self._grid_width:
                line.append(self._grid[current_index[0]][current_index[1]])
                current_index = (current_index[0] + OFFSETS[direction][0], current_index[1] + OFFSETS[direction][1])
                
            merged_line = merge(line)
            current_index = index
            merged_index = 0
            
            while 0 <= current_index[0] < self._grid_height and 0 <= current_index[1] < self._grid_width:
                if self._grid[current_index[0]][current_index[1]] != merged_line[merged_index]:
                    moved = True
                    
                self._grid[current_index[0]][current_index[1]] = merged_line[merged_index]
                merged_index += 1
                current_index = (current_index[0] + OFFSETS[direction][0], current_index[1] + OFFSETS[direction][1])
                
        if moved:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        tile_value = random.choice([2] * 9 + [4])
        tile_index = random.choice(self.get_empty_cells())
        self.set_tile(tile_index[0], tile_index[1], tile_value)
        
    def get_empty_cells(self):
        """
        Returns a list of empty cells indices
        """
        return [(x, y) for y in range(self._grid_width) for x in range(self._grid_height) if self._grid[x][y] == 0]

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]
