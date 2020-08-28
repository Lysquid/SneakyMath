"""Grid class file"""

import random

import data.constants as c
from data.tiles import SnakePart, Number, Operation, Tile


class Grid:
    """Object that stores all the tiles
    in their respective position
    """

    def __init__(self):
        self._grid = [[None for y in range(c.NB_ROWS)] for x in range(c.NB_COLS)]

    def __getitem__(self, pos):
        return self._grid[pos[0]][pos[1]]

    def __setitem__(self, pos, tile):
        self._grid[pos[0]][pos[1]] = tile
        if isinstance(tile, Tile):
            tile.pos = pos

    def __repr__(self):
        string = ""
        for row in range(c.NB_ROWS):
            for col in range(c.NB_COLS):
                tile = self[(col, row)]
                if isinstance(tile, SnakePart):
                    string += "S"
                elif isinstance(tile, Number):
                    string += str(tile.value)
                elif isinstance(tile, Operation):
                    string += str(tile.ope)
                else:
                    string += "."
            string += "\n"
        return string

    def generate(self):
        """Generate tiles on the grid in an initial layout"""
        # Operation tiles
        col_offset, row_offset = round(c.NB_COLS / 4), round(c.NB_ROWS / 4)
        ope_list = (
            ("+", (col_offset, row_offset)),
            ("+", (c.NB_COLS - col_offset - 1, c.NB_ROWS - row_offset - 1)),
            ("-", (col_offset, c.NB_ROWS - row_offset - 1)),
            ("-", (c.NB_COLS - col_offset - 1, row_offset)),
        )
        for ope, pos in ope_list:
            self[pos] = Operation(ope)
        # Random number tiles
        for _ in range(10):
            nbr_pos = (
                random.randint(0, c.NB_COLS - 1),
                random.randint(0, c.NB_ROWS - 1),
            )
            if self[nbr_pos] is None:
                self[nbr_pos] = Number()
