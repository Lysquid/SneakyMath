"""PygView class file"""

import random

import pygame

import data.constants as c
import data.textures as textures
from data.tiles import Block, Number, Operation


class PygView:
    """
    General class which is the main storage for the game :
    contains the screen to show and the grid of tiles
    """

    def __init__(self):
        # Create the display
        self.screen = pygame.display.set_mode((c.SCREEN_W, c.SCREEN_H))
        # Create the clock used to control the frame rate
        self.clock = pygame.time.Clock()

        self.texture = None
        self.grid = None
        self.prev_grid = None
        self.snake = None

    def game_init(self):
        """Initialize the basic objects needed for the game"""
        # Create the grid, where are stored all tiles at their respective position
        self.grid = [[None for y in range(c.NB_TILES_Y)] for x in range(c.NB_TILES_X)]
        self.prev_grid = []  # Make a slot for the previous grid, used to keep data
        self.snake = None  # Slot for snake once created

    def generate_grid(self):
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
            if self.grid[x][y] == None:  # Check if tile is free
                Number(self, (x, y))

    def draw_menu(self):
        """Draw the menu screen"""
        self.screen.fill(self.texture.colors["bg"])
        self.texture.render_text(self, "SNEAKYMATH", "title")
        self.texture.render_text(self, "Appuyer sur [Enter] pour commencer", "menu2")
        self.texture.render_text(
            self,
            """© Créé par Romain avec l'aide de Natan
            pour le prix Bernard Novelli des Trophées Tangente 2020""",
            "footnote",
        )

    def draw_pause(self):
        """Draw pause screen"""
        self.screen.fill(self.texture.colors["bg"])
        self.texture.render_text(
            self, "Pause", "menu1", textures.color_palette(textures.nb_color(1), 0.8)
        )
        self.texture.render_text(self, "Appuyer sur [Entrer] pour reprendre", "menu2")

    def draw_game_over(self, best_score, new_best):
        """Draw game over screen"""
        overlay = pygame.Surface((c.SCREEN_W, c.SCREEN_H))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))
        self.texture.render_text(
            self,
            "Game Over",
            "menu1",
            textures.color_palette(textures.nb_color(9), 0.8),
        )
        self.texture.render_text(self, "Score : " + str(self.snake.score), "menu2")
        if new_best:
            colors = self.texture.colors["snake"]
        else:
            colors = self.texture.colors["white_txt"]
        self.texture.render_text(
            self, "Meilleur score : " + str(best_score), "menu3", colors
        )

    def draw_field(self, progress):
        """Draw everything from the grid onto the screen"""
        # Create the field from the default field
        field = self.texture.dflt["field"].copy()
        # Draw the blocks from the grid onto the field
        for x in range(c.NB_TILES_X):
            for y in range(c.NB_TILES_Y):

                tile2draw = self.prev_grid[x][y]

                if isinstance(
                    tile2draw, Block
                ):  # Draw it only if it's not a snake part
                    field.blit(tile2draw.image, tile2draw.get_coords(progress))

        # Draw the snake parts (from the end) on the field
        for part in reversed(self.snake.parts):
            x, y = part.get_coords(progress, self.snake.dead)
            field.blit(part.image, (x, y))
            if x < 0:
                x += c.FIELD_W
            elif x + c.T_W > c.FIELD_W:
                x -= c.FIELD_W
            if y < 0:
                y += c.FIELD_H
            elif y + c.T_H > c.FIELD_H:
                y -= c.FIELD_H
            field.blit(part.image, (x, y))

        return field

    def draw_screen(self, header, field):
        """Draw screen"""
        self.screen.fill((0, 0, 0))
        self.screen.blit(field, (0, c.HEADER_H))

        self.screen.blit(header, (0, 0))

    @staticmethod
    def copy_grid(grid):
        """Return a deep copy of a grid"""
        return [[grid[x][y] for y in range(c.NB_TILES_Y)] for x in range(c.NB_TILES_X)]

    @staticmethod
    def new_pos(direction, pos):
        """New pos"""
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
