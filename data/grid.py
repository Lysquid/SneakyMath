"""Grid class file"""

import random

import data.constants as c
from data.tiles import Number, Operation


class Grid:
    """Object that stores all the tiles in their respective position"""

    def __init__(self, grid=None):
        if grid is None:
            grid = [[None for y in range(c.NB_TILES_Y)] for x in range(c.NB_TILES_X)]
        self._grid = grid

    def __getitem__(self, index):
        return self._grid[index]

    def __setitem__(self, index, value):
        self._grid[index] = value

    def generate(self):
        """Generate tiles on the grid to have an initial layout"""
        # Set constants used for placement
        x_offset, y_offset = round(c.NB_TILES_X / 4), round(c.NB_TILES_Y / 4)
        # List of operations tiles with their positions
        ope_list = [
            ("+", (x_offset, y_offset)),
            ("+", (c.NB_TILES_X - x_offset - 1, c.NB_TILES_Y - y_offset - 1)),
            ("-", (x_offset, c.NB_TILES_Y - y_offset - 1)),
            ("-", (c.NB_TILES_X - x_offset - 1, y_offset)),
        ]
        # Place operations tiles
        for ope, pos in ope_list:
            Operation(self, ope, pos)
        # Place random number tiles
        for _ in range(10):
            x, y = (
                random.randint(0, c.NB_TILES_X - 1),
                random.randint(0, c.NB_TILES_Y - 1),
            )
            if self[x][y] is None:  # Check if tile is free
                Number(self, (x, y))

    @staticmethod
    def new_pos(direction, pos):
        """Return new position"""
        x, y = pos
        if direction == "up":
            y -= 1
        if direction == "down":
            y += 1
        if direction == "right":
            x += 1
        if direction == "left":
            x -= 1

        x %= c.NB_TILES_X
        y %= c.NB_TILES_Y

        return (x, y)
