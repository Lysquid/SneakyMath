"""Tile classes file"""

import random

import pygame

import data.constants as c
from data.textures import TEXTURES as textures


class Tile:
    """Tile class, parent class of all types of tiles,
    handles the positional attributes and their syncronisation
    """

    def __init__(self, pos=None):
        self.rect = pygame.Rect(0, 0, c.T_W, c.T_H)
        if pos:
            self._pos = list(pos)
            self._col = pos[0]
            self._row = pos[1]

    def _get_pos(self):
        return tuple(self._pos)

    def _set_pos(self, pos):
        self._pos = list(pos)
        self._col = pos[0]
        self._row = pos[1]

    def _get_col(self):
        return self._col

    def _set_col(self, col):
        self._col = col
        self._pos[0] = col

    def _get_row(self):
        return self._row

    def _set_row(self, row):
        self._row = row
        self._pos[1] = row

    pos = property(_get_pos, _set_pos)
    row = property(_get_row, _set_row)
    col = property(_get_col, _set_col)


class SnakePart(Tile):
    """Snake part of the snake class
    """

    def __init__(self, pos=None):

        super().__init__(pos)
        self.image = textures.dflt["snake_part"].copy()
        self.dir = None

    def move(self):
        """Move according to the direction"""
        if self.dir == "up":
            self.row -= 1
        if self.dir == "down":
            self.row += 1
        if self.dir == "right":
            self.col += 1
        if self.dir == "left":
            self.col -= 1

        self.col %= c.NB_COLS
        self.row %= c.NB_ROWS

    def calc_rect(self, progress, snake):
        """Calculate the coordinates on the screen
        from the position in the grid
        """
        if snake.dead:
            offset = -0.5 * (1 + (2 * progress - 1) ** 2)
            # 0.5(1+(2x-1)²)
        else:
            offset = progress - 1
        # if self is snake.tail and snake.inc < 0:
        #     if self is not snake.head:
        #         offset = -1
        #     next_part = snake.parts[-2]
        #     if self.dir == next_part.dir:
        #         offset = 1 + offset * 2

        oriented_offset = ((self.dir == "right") - (self.dir == "left")) * offset
        self.rect.x = round((self.col + oriented_offset) * c.T_W)
        oriented_offset = ((self.dir == "down") - (self.dir == "up")) * offset
        self.rect.y = round((self.row + oriented_offset) * c.T_H)
        return self.rect

    def set_ope(self, ope):
        """Change the texture to a given operation"""
        self.image = textures.dflt["head_" + ope]


class Block(Tile):
    """Block class, parent class
    of the Number and Operation classes
    """

    def __init__(self, pos):
        super().__init__(pos)

    def calc_rect(self):
        """Calculate the coordinates on the screen
        from the position in the grid
        """
        self.rect.x = self.col * c.T_W
        self.rect.y = self.row * c.T_H
        return self.rect


class Number(Block):
    """Number block class
    """

    def __init__(self, pos=None, value=None):
        super().__init__(pos)
        if value is None:
            value = random.randint(1, 9)
        self.value = value
        self.image = textures.dflt["number_" + str(value)]


class Operation(Block):
    """Operation block class"""

    def __init__(self, ope, pos=None):
        super().__init__(pos)
        self.ope = ope
        self.image = textures.dflt["operation_" + ope]
