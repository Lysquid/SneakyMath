"""Independant functions file"""

import pygame
import os
import sys


def blit_alpha(target, source, location, opacity=None):
    """Blit an image with tranparency
    at lower transparency
    (not supported by pygame by default)
    https://nerdparadise.com/programming/pygameblitopacity
    """
    if opacity is None:
        target.blit(source, location)
    else:
        x_coord = location[0]
        y_coord = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x_coord, -y_coord))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller
    source: stackoverflow
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
