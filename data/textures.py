"""Texture class file"""

import os

import pygame as pg

import data.constants as c
import data.textures_func as func
from data.functions import resource_path


class Textures:
    """Textures class, create and manage
    the textures of the game
    """

    def __init__(self):
        self.font = None
        self.color = None
        self.dflt = None
        self.text = None

    def create(self):
        """Create the textures and other attributes"""
        self.font = self.create_fonts()
        self.color = self.create_colors()
        self.dflt = self.create_dflts()
        self.text = self.create_texts

    @staticmethod
    def create_fonts():
        """Create font dict, which stores
        all the fonts of the game
        """
        fonts = {}
        font_path = os.path.join(c.FONTS_PATH, "JosefinSans-SemiBold.ttf")
        font_path = resource_path(font_path)

        font = func.get_font(font_path, 2)
        fonts["pause"] = font
        fonts["game_over"] = font

        font = func.get_font(font_path, 1.2)
        fonts["new_score"] = font
        fonts["best_score"] = font

        font = func.get_font(font_path, 0.9)
        fonts["menu"] = font

        font = func.get_font(font_path)
        fonts["number"] = font

        font = func.get_font(font_path, 1.8)
        fonts["operation"] = font

        font_path.replace("SemiBold", "Regular")
        font = func.get_font(font_path, 2.5)
        fonts["title"] = font

        font = func.get_font(font_path, 0.5)
        fonts["footnote"] = font

        font = func.get_font(font_path, 0.7)
        fonts["stat"] = font

        return fonts

    def create_colors(self):
        """Create the color dict, which stores
        all the colors of the game
        """
        colors = {}

        color = func.color_palette((50, 50, 50))
        colors["field"] = color

        colors["background"] = color[2]

        color = func.color_palette((120, 230, 120))
        colors["snake"] = color

        color = func.color_palette((250, 250, 100))
        colors["filled"] = color

        color = func.color_palette((230, 230, 230))
        colors["white"] = color

        color = func.color_palette((230, 230, 230), 0.95)
        colors["white_txt"] = color

        color = func.color_palette((80, 80, 80), 0.9)
        colors["black_txt"] = color

        color = func.color_palette(func.nbr_color(1), 0.9)
        colors["small_number"] = color

        color = func.color_palette(func.nbr_color(9), 0.9)
        colors["big_number"] = color

        return colors

    def create_dflts(self):
        """Create default textures dict, which stores
        all the default textures of the game
        """
        dflt = {}

        img = func.field_tile(self.color["field"])
        field_tile = img
        dflt["field_tile"] = img.convert()

        # ! self.screen.get_size()
        size = (c.FIELD_W + 2 * c.T_W, c.FIELD_H + 2 * c.T_H)
        img = pg.Surface(size)
        for col in range(c.NB_COLS):
            for row in range(c.NB_ROWS):
                coords = (c.T_W * col, c.T_H * row)
                img.blit(field_tile, coords)
        dflt["field"] = img.convert_alpha()

        size = (c.FIELD_W, c.T_H)
        color = self.color["background"]
        img = pg.Surface(size)
        img.fill(color)
        dflt["header"] = img.convert()

        color = self.color["snake"]
        img = func.tile(color)
        body_part = img
        dflt["snake_part"] = img.convert_alpha()

        size = list(c.T_SIZE)
        size[0] += 2 * c.BORDER
        size[1] += 2 * c.BORDER
        radius = c.RADIUS * 2
        color = self.color["filled"]
        img = func.tile(color)
        dflt["filled_snake_part"] = img.convert_alpha()

        color = self.color["snake"]
        img = func.tile(color, size=size, rounded=radius)
        dflt["snake_part_eating"] = img.convert_alpha()

        color = self.color["filled"]
        img = func.tile(color, size=size, rounded=radius)
        dflt["filled_snake_part_eating"] = img.convert_alpha()

        img = body_part.copy()
        size = (32, 32)
        img = pg.Surface(size, pg.SRCALPHA, 32)
        img.fill((255, 255, 255))  # For some reason SRCALPHA is black as an icon
        icon = pg.transform.smoothscale(body_part, size)
        img.blit(icon, (0, 0))
        dflt["icon"] = img.convert_alpha()
        icon.set_colorkey((255, 255, 255))

        font = self.font["operation"]
        color = self.color["black_txt"]
        text = func.relief_text("+", font, color)
        dflt["+"] = text.convert_alpha()

        text = func.relief_text("-", font, color)
        dflt["-"] = text.convert_alpha()

        img = func.tile(self.color["white"])
        dflt["operation"] = img.convert_alpha()

        font = self.font["number"]
        color = self.color["white_txt"]
        for nbr in range(1, 10):
            nbr_color = func.color_palette(func.nbr_color(nbr))
            img = func.tile(nbr_color)
            text = str(nbr)
            rendered = func.relief_text(text, font, color)
            rect = rendered.get_rect()
            rect.x = round((c.T_W - rect.w) / 2)
            rect.y = round((c.T_H - rect.h) / 2)
            img.blit(rendered, rect.topleft)
            dflt["number_" + text] = img.convert_alpha()

        return dflt

    def create_texts(self, view, font_name, text, color=None):
        """Render text on the screen
        in the given style
        """

        font = self.font[font_name]
        if font_name == "title":
            color = self.color["snake"]
            depth = c.S_W * 2
            rendered = func.relief_text(text, font, color, depth)
            coords = (c.SCREEN_W / 2, c.SCREEN_H / 4)

        if font_name == "pause":
            color = self.color["small_number"]
            rendered = func.relief_text(text, font, color)
            coords = (c.SCREEN_W / 2, c.SCREEN_H / 3)

        if font_name == "menu":
            color = self.color["white_txt"][0]
            rendered = font.render(text, True, color)
            coords = (c.SCREEN_W / 2, 3 * c.SCREEN_H / 5)

        if font_name == "game_over":
            color = self.color["big_number"]
            rendered = func.relief_text(text, font, color)
            coords = (c.SCREEN_W / 2, c.SCREEN_H / 3)

        if font_name == "new_score":
            color = self.color["white_txt"][0]
            rendered = font.render(text, True, color)
            coords = (c.SCREEN_W / 2, c.SCREEN_H / 2)

        if font_name == "best_score":
            color = self.color["white_txt"][0]
            rendered = font.render(text, True, color)
            coords = (c.SCREEN_W / 2, 6 * c.SCREEN_H / 10)

        if font_name == "footnote":
            color = self.color["white_txt"][2]
            rendered = font.render(text, True, color)
            coords = (c.SCREEN_W / 2, 19 * c.SCREEN_H / 20)

        rect = rendered.get_rect()
        x_coord, y_coord = round(coords[0]), round(coords[1])
        coords = (x_coord - rect.centerx, y_coord - rect.centery)
        view.screen.blit(rendered.convert_alpha(), coords)

    def render_header(self, snake, player):
        """Render the game header"""
        header = self.dflt["header"].copy()

        # Draw the size stat in a rectangle
        depth = round(c.DEPTH / 2)
        if player.goal_reached:
            color = self.color["snake"]
        else:
            color = self.color["white"]
        size = (round(c.T_W * 3.5), c.T_H)
        img = func.tile(color, size, depth)
        tile_img = img
        rect = img.get_rect()
        rect.x = round(c.HEADER_W / 3) - round(rect.w / 2)
        tile_rect = rect
        header.blit(img, rect.topleft)

        text = str(len(snake))
        font = self.font["number"]
        color = self.color["black_txt"]
        nb_y = tile_rect.y + round(2.1 * c.S_H)
        img = func.relief_text(text, font, color, depth)
        rect = img.get_rect()
        rect.y = nb_y
        rect.x = tile_rect.right - c.T_W - round(3.0 * c.S_W)
        rect.x += round((c.T_W - rect.w) / 2)
        header.blit(img, rect.topleft)

        text = "TAILLE"
        font = self.font["stat"]
        color = self.color["black_txt"]
        stat_y = tile_rect.y + round(2.8 * c.S_H)
        img = func.relief_text(text, font, color, depth)
        rect = img.get_rect()
        rect.y = stat_y
        rect.x = tile_rect.left + round(4.0 * c.S_W)
        header.blit(img, rect.topleft)

        # Increment
        font = self.font["number"]
        color = self.color["white_txt"]
        if snake.inc != 0:
            text = str(snake.inc)
            if snake.inc > 0:
                text = "+" + text
            img = func.relief_text(text, font, color, depth)
            rect = img.get_rect()
            rect.y = nb_y
            rect.x = tile_rect.right + round(2.0 * c.S_W)
            header.blit(img, rect.topleft)

        # Goal
        img = tile_img
        rect = tile_rect
        rect.x = round(2 / 3 * c.HEADER_W) - round(rect.w / 2)
        tile_rect = rect
        header.blit(img, rect.topleft)

        text = str(player.goal)
        color = self.color["black_txt"]
        img = func.relief_text(text, font, color, depth)
        rect = img.get_rect()
        rect.y = nb_y
        rect.x = tile_rect.right - c.T_W - round(3.0 * c.S_W)
        rect.x += round((c.T_W - rect.w) / 2)
        header.blit(img, rect.topleft)

        text = "OBJECTIF"
        font = self.font["stat"]
        img = func.relief_text(text, font, color, depth)
        rect = img.get_rect()
        rect.y = stat_y
        rect.x = tile_rect.x + round(4.0 * c.S_W)
        header.blit(img, rect.topleft)

        return header.convert()


TEXTURES = Textures()
