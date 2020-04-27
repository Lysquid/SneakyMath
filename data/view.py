"""view class file"""


import pygame

import data.constants as c
from data.tiles import Block
from data.textures import TEXTURES as textures


class View:
    """
    General class which is the main storage for the game :
    contains the screen to show and the grid of tiles
    """

    def __init__(self):
        self.screen = pygame.display.set_mode((c.SCREEN_W, c.SCREEN_H))
        self.clock = pygame.time.Clock()

    def customize_window(self):
        """Customize window"""
        pygame.display.set_caption(c.GAME_NAME)
        pygame.display.set_icon(textures.icon())
        self.screen.fill(textures.colors["bg"])

    def tick(self):
        """Sleep accordingly to FPS"""
        self.clock.tick(c.FPS)

    @staticmethod
    def update():
        """Update screen"""
        pygame.display.flip()

    def draw_menu(self):
        """Draw the menu screen"""
        self.screen.fill(textures.colors["bg"])
        textures.render_text(self, c.GAME_NAME.upper(), "title")
        textures.render_text(self, "Appuyer sur [Enter] pour commencer", "menu2")
        textures.render_text(
            self,
            "© Créé par Romain avec l'aide de Natan "
            + "pour le prix Bernard Novelli des Trophées Tangente 2020",
            "footnote",
        )

    def draw_pause(self):
        """Draw pause screen"""
        self.screen.fill(textures.colors["bg"])
        textures.render_text(
            self, "Pause", "menu1", textures.color_palette(textures.nb_color(1), 0.8)
        )
        textures.render_text(self, "Appuyer sur [Entrer] pour reprendre", "menu2")

    def draw_game_over(self, score, best_score, new_best):
        """Draw game over screen"""
        overlay = pygame.Surface((c.SCREEN_W, c.SCREEN_H))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))
        textures.render_text(
            self,
            "Game Over",
            "menu1",
            textures.color_palette(textures.nb_color(9), 0.8),
        )
        textures.render_text(self, "Score : " + str(score), "menu2")
        if new_best:
            colors = textures.colors["snake"]
        else:
            colors = textures.colors["white_txt"]
        textures.render_text(
            self, "Meilleur score : " + str(best_score), "menu3", colors
        )

    def draw_field(self, grid, snake, progress):
        """Draw everything from the grid onto the screen"""
        # Create the field from the default field
        field = textures.dflt["field"].copy()
        # Draw the blocks from the grid onto the field
        for x in range(c.NB_TILES_X):
            for y in range(c.NB_TILES_Y):
                tile2draw = grid[x][y]
                if isinstance(tile2draw, Block):
                    field.blit(tile2draw.image, tile2draw.get_coords(progress))

        # Draw the snake parts (from the end) on the field
        for part in reversed(snake.parts):
            x, y = part.get_coords(progress, snake.dead)
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

VIEW = View()