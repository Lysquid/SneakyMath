"""Tile classes file"""

import random

import pygame

import data.constants as c

from data.textures import TEXTURES as textures


class Tile:
    """Tile class"""

    def __init__(self, pos=None):
        self.rect = pygame.Rect(0, 0, c.T_W, c.T_H)
        if pos:
            self._pos = list(pos)
            self._col = pos[0]
            self._row = pos[1]

    def _get_pos(self):
        return self._pos

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


class BodyPart(Tile):
    """Body Part of the snake class"""

    def __init__(self, pos):

        super().__init__(pos)
        self.image = textures.body_part()
        self.dir = None

    def move(self):
        """Move"""
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

    def calc_coords(self, progress, dead):
        """Get the coordinates"""
        if dead:
            offset = round(0.5 * (-(1 + (2 * progress - 1) ** 2)) * c.T_W)
            # -0.5(1+(2x-1)²)
        else:
            offset = round(progress * c.T_W)

        oriented_offset = ((self.dir == "right") - (self.dir == "left")) * offset
        self.rect.x = self.col * c.T_W + oriented_offset
        oriented_offset = ((self.dir == "down") - (self.dir == "up")) * offset
        self.rect.y = self.row * c.T_H + oriented_offset

        return self.rect.topleft


class Block(Tile):
    """Block"""

    def __init__(self, pos):
        super().__init__(pos)

    def calc_coords(self):
        """Get the coordinates"""
        self.rect.x = self.col * c.T_W
        self.rect.y = self.row * c.T_H
        return self.rect.topleft


class Number(Block):
    """Number"""

    def __init__(self, pos=None, value=None):
        super().__init__(pos)

        if value is None:
            self.value = random.randint(1, 9)
        else:
            self.value = value

        self.image = textures.number(self.value)


class Operation(Block):
    """Operation"""

    def __init__(self, ope, pos=None):
        super().__init__(pos)

        self.ope = ope

        self.image = textures.operation(self.ope)
