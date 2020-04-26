"""Tile classes file"""

import random

import pygame

import data.constants as c


class Tile:
    """Tile class"""

    def __init__(self, view, pos):
        self.view = view
        self.rect = pygame.Rect(0, 0, c.T_W, c.T_H)
        self.x = None
        self.y = None
        if pos is not None:
            self.spawn(pos)

    def spawn(self, pos):
        """Spawn tile"""
        self.x, self.y = pos
        self.view.grid[self.x][self.y] = self


class BodyPart(Tile):
    """Body Part of the snake class"""

    def __init__(self, view, pos, ope=None):

        super().__init__(view, pos)

        self.image = view.texture.body_part(ope)

        self.prev_x, self.prev_y = self.x, self.y
        self.dir = None

    def move(self, direction, remove=True):
        """Move"""
        self.prev_x, self.prev_y = self.x, self.y

        self.dir = direction

        self.x, self.y = self.view.new_pos(self.dir, (self.x, self.y))

        self.view.grid[self.x][self.y] = self

    def get_coords(self, progress, dead=False):
        """Get the coordinates"""
        if not dead:
            offset = round(progress * c.T_W)
        else:
            offset = round(0.5 * (-((progress * 2 - 1) ** 2) + 1) * c.T_W)
        self.rect.x = (
            self.prev_x * c.T_W
            + ((self.dir == "right") - (self.dir == "left")) * offset
        )
        self.rect.y = (
            self.prev_y * c.T_H + ((self.dir == "down") - (self.dir == "up")) * offset
        )

        return self.rect.topleft


class Block(Tile):
    """Block"""

    def __init__(self, view, pos):
        super().__init__(view, pos)

    def get_coords(self, progress=None):
        """Get the coordinates"""
        self.rect.x = self.x * c.T_W
        self.rect.y = self.y * c.T_H
        return self.rect.topleft


class Number(Block):
    """Number"""

    def __init__(self, view, pos=None, value=None):
        super().__init__(view, pos)

        if value is None:
            self.value = random.randint(1, 9)
        else:
            self.value = value

        self.image = view.texture.number(self.value)


class Operation(Block):
    """Operation"""

    def __init__(self, view, ope, pos=None):
        super().__init__(view, pos)

        self.ope = ope

        self.image = view.texture.operation(self.ope)
