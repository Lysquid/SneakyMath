"""
Texture ganeration
"""

import os
import pygame
from pygame import gfxdraw
from data.consts import *


def color_palette(color, multiplier=0.9):
    colors = [color]
    colors.append(tuple([round(value * multiplier) for value in colors[0]]))
    colors.append(tuple([round(value * multiplier) for value in colors[1]]))
    return colors


def nb_color(value):
    return (150 + value*10, 120, 100 + (10-value)*10)


def draw_rounded_rec(image, color, rect, radius):
    temp = pygame.Surface(rect.size, pygame.SRCALPHA, 32)

    circle_centers = [(radius, radius),
                      (rect.w - radius, radius),
                      (radius, rect.h - radius),
                      (rect.w - radius, rect.h - radius)]
    for circle_center in circle_centers:
        pygame.gfxdraw.aacircle(
            temp, circle_center[0], circle_center[1], radius, color)
        pygame.gfxdraw.filled_circle(
            temp, circle_center[0], circle_center[1], radius, color)

    rec_rects = [pygame.Rect(radius, 0, rect.w - 2*radius, rect.h),
                 pygame.Rect(0, radius, rect.w, rect.h - 2*radius)]
    for rec_rect in rec_rects:
        pygame.draw.rect(temp, color, rec_rect)

    image.blit(temp, rect.topleft)
    return image.convert_alpha()


def make_tile(colors, size=(T_W, T_H), depth=S_H, border=S_W, rounded=RADIUS):
    image = pygame.Surface(size, pygame.SRCALPHA, 32)

    rec_offset = (round(T_W / 10), round(T_H / 10))
    rec_size = (round(size[0] - 2*rec_offset[0]),
                round(size[1] - 2*rec_offset[1]))
    rects = [pygame.Rect(rec_offset, rec_size)]
    rects.append(pygame.Rect((rects[0].x, rects[0].y - depth), rects[0].size))
    rects.append(pygame.Rect(rects[1].x + border, rects[1].y +
                             border, rects[1].w - 2*border, rects[1].h - 2*border))
    rects.append(pygame.Rect(
        rects[2].x, rects[2].y + depth, rects[2].w, rects[2].h - depth))

    for rect_id, col_id in enumerate((1, 0, 1, 2)):
        radius = round(min(rects[rect_id].size) * RADIUS)
        draw_rounded_rec(image, colors[col_id], rects[rect_id], radius)

    return image.convert_alpha()


def make_field_tile(colors, size=(T_W, T_H), depth=S_H, rounded=RADIUS):
    image = pygame.Surface(size)

    rec_offset = (round(T_W / 10), round(T_H / 10))
    rec_size = (round(size[0] - 2*rec_offset[0]),
                round(size[1] - 2*rec_offset[1]))
    rects = [pygame.Rect(rec_offset, rec_size)]
    rects.append(pygame.Rect(
        rects[0].x, rects[0].y + depth, rects[0].w, rects[0].h - depth))

    image.fill(colors[0])
    for rect_id, col_id in enumerate((1, 2)):
        radius = round(rects[rect_id].w * RADIUS)
        draw_rounded_rec(image, colors[col_id], rects[rect_id], radius)

    return image.convert()


def relief_text(text, font, colors, depth=S_H):
    text = str(text)

    rendered = font.render(text, True, colors[2])
    rect = rendered.get_rect()
    image = pygame.Surface((rect.w, rect.h + depth), pygame.SRCALPHA, 32)
    for y in range(depth):
        image.blit(rendered, (0, y+1))

    rendered = font.render(text, True, colors[0])
    image.blit(rendered, (0, 0))

    return image.convert_alpha()


class Textures():

    def __init__(self, view):

        view.texture = self
        self.fonts = self.create_font()
        self.colors = {}
        for name in COLORS.keys():
            self.colors[name] = color_palette(COLORS[name][0], COLORS[name][1])
            self.colors["bg"] = self.colors["field"][2]
        self.dflt = {}
        for name in ["field_tile", "field", "header", "Body_part", "Number", "Operation"]:
            self.dflt[name] = self.create_dflt(name)

    def set_icon(self, view):
        icon = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        icon.fill((255, 255, 255))
        image = pygame.transform.smoothscale(
            self.dflt["Body_part"].copy(), (32, 32)).convert_alpha()
        icon.blit(image, (0, 0))
        #icon.set_colorkey((255, 255, 255))
        pygame.display.set_icon(icon.convert_alpha())

    def create_font(self):
        fonts = {}
        font_path = os.path.join("data/fonts", "JosefinSans-SemiBold.ttf")
        font_size = round(11 * T_W / 20)
        fonts["menu1"] = pygame.font.Font(font_path, round(font_size * 1.5))
        fonts["menu2"] = pygame.font.Font(font_path, round(font_size * 0.9))
        fonts["menu3"] = pygame.font.Font(font_path, round(font_size * 0.9))
        fonts["nb"] = pygame.font.Font(font_path, font_size)
        fonts["ope"] = pygame.font.Font(font_path, round(font_size * 1.8))
        font_path.replace("SemiBold", "Regular")
        fonts["title"] = pygame.font.Font(font_path, round(font_size * 2.5))
        fonts["footnote"] = pygame.font.Font(font_path, round(font_size * 0.5))
        fonts["stat"] = pygame.font.Font(font_path, round(font_size * 0.7))
        return fonts

    def create_dflt(self, name):
        # Background tile texture
        if name == "field_tile":

            image = make_field_tile(self.colors["field"])
            is_alpha = False

        # Default field image
        if name == "field":
            # ! self.screen.get_size()
            image = pygame.Surface((FIELD_W + 2 * T_W, FIELD_H + 2 * T_H))
            field_tile = self.dflt["field_tile"]
            for x in range(NB_TILES_X):
                for y in range(NB_TILES_Y):
                    coords = (T_W * x, T_H * y)
                    image.blit(field_tile, coords)
            is_alpha = False

        if name == "header":
            image = pygame.Surface([FIELD_W, T_H])
            image.fill(self.colors["bg"])
            is_alpha = False

        # Default body part
        if name == "Body_part":
            image = make_tile(self.colors["snake"])
            is_alpha = True

        if name == "Number":
            image = pygame.Surface([T_W, T_H], pygame.SRCALPHA, 32)
            is_alpha = True

        if name == "Operation":
            image = make_tile(self.colors["white"])
            is_alpha = True

        if is_alpha:
            return image.convert_alpha()
        else:
            return image.convert()

    def render_text(self, view, text, font_name, colors=None):
        """ Draw a message on the middle of the screen """
        font = self.fonts[font_name]
        if font_name == "title":
            coords = (round(SCREEN_W / 2), round(SCREEN_H / 4))
            rendered = relief_text(text, font, self.colors["snake"], S_W*2)
        if font_name == "menu1":
            coords = (round(SCREEN_W / 2), round(SCREEN_H / 3))
            rendered = relief_text(text, font, colors)
        if font_name == "menu2":
            coords = (round(SCREEN_W / 2), round(SCREEN_H / 2))
            rendered = font.render(text, True, self.colors["white_txt"][0])
        if font_name == "menu3":
            coords = (round(SCREEN_W / 2), round(6 * SCREEN_H / 10))
            rendered = font.render(text, True, colors[0])
        if font_name == "footnote":
            coords = (round(SCREEN_W / 2), round(19 * SCREEN_H / 20))
            rendered = font.render(text, True, self.colors["white_txt"][2])
        rect = rendered.get_rect()
        coords = (coords[0] - rect.centerx, coords[1] - rect.centery)
        view.screen.blit(rendered.convert_alpha(), coords)

    def render_ope(self, image, ope):
        font = self.fonts["ope"]
        colors = self.colors["black_txt"]
        ope_img = relief_text(ope, font, colors)
        rect = ope_img.get_rect()
        offset = (round((T_W - rect.w) / 2), round((T_H - rect.h - S_H) / 2))
        image.blit(ope_img, offset)
        return image

    def header(self, snake):

        header = self.dflt["header"].copy()

        nb_font = self.fonts["nb"]
        stat_font = self.fonts["stat"]
        depth = round(S_H / 2)

        # Draw the size stat in a rectangle
        if snake.goal_reached:
            rec_color = self.colors["snake"]
        else:
            rec_color = self.colors["white"]
        rec = make_tile(rec_color, (round(T_W * 3.5), T_H), depth)
        rec_rect = rec.get_rect()
        rec_rect.x = round(HEADER_W / 3) - round(rec_rect.w / 2)
        header.blit(rec, rec_rect.topleft)

        nb_y = rec_rect.y + round((T_H - relief_text(
            "123", self.fonts["nb"], self.colors["black_txt"]).get_rect().h) / 2) + round(S_H / 3)
        stat_y = rec_rect.y + \
            round((T_H - relief_text("ABC",
                                     self.fonts["nb"], self.colors["black_txt"]).get_rect().h) / 2) + S_H

        size = str(snake.size)
        size_img = relief_text(
            size, self.fonts["nb"], self.colors["black_txt"], depth)
        size_rect = size_img.get_rect()
        size_rect.topleft = (rec_rect.right - T_W - 3 *
                             S_W + round((T_W - size_rect.w) / 2), nb_y)
        header.blit(size_img, size_rect.topleft)

        size_stat_img = relief_text(
            "TAILLE", self.fonts["stat"], self.colors["black_txt"], depth)
        size_stat_rect = size_img.get_rect()
        size_stat_rect.topleft = (rec_rect.left + 4*S_W, stat_y)
        header.blit(size_stat_img, size_stat_rect.topleft)

        # Increment
        if snake.inc != 0:
            inc = str(snake.inc)
            if snake.inc > 0:
                inc = "+" + inc
            inc_img = relief_text(
                inc, self.fonts["nb"], self.colors["white_txt"], depth)
            inc_rect = inc_img.get_rect()
            inc_rect.topleft = (rec_rect.right + 2*S_W, nb_y)
            header.blit(inc_img, inc_rect.topleft)

        # Goal
        rec_rect.x = round(2*HEADER_W / 3) - round(rec_rect.w / 2)
        header.blit(rec, rec_rect.topleft)

        goal = str(snake.goal)
        goal_img = relief_text(
            goal, self.fonts["nb"], self.colors["black_txt"], depth)
        goal_rect = goal_img.get_rect()
        goal_rect.topleft = (rec_rect.right - T_W - 3 *
                             S_W + round((T_W - goal_rect.w) / 2), nb_y)
        header.blit(goal_img, goal_rect.topleft)

        goal_stat_img = relief_text(
            "OBJECTIF", self.fonts["stat"], self.colors["black_txt"], depth)
        goal_stat_rect = goal_stat_img.get_rect()
        goal_stat_rect.topleft = (rec_rect.left + 4*S_W, stat_y)
        header.blit(goal_stat_img, goal_stat_rect.topleft)

        # Score
        score = str(snake.score)
        score_img = relief_text(
            score, self.fonts["nb"], self.colors["white_txt"], depth)
        score_rect = score_img.get_rect()
        score_rect.topleft = (
            HEADER_W - round(score_rect.w / 2) - (T_W + 5*S_W), nb_y)
        header.blit(score_img, score_rect.topleft)

        score_stat = "SCORE"
        score_stat_img = relief_text(
            score_stat, self.fonts["stat"], self.colors["white_txt"], depth)
        score_stat_rect = score_stat_img.get_rect()
        score_stat_rect.topleft = (HEADER_W - round(T_W * 3.5), stat_y)
        header.blit(score_stat_img, score_stat_rect.topleft)

        # Added score
        if snake.added_score != 0:
            added = "+" + str(snake.added_score)
            added_img = relief_text(
                added, self.fonts["nb"], self.colors["white_txt"], depth)
            added_rect = added_img.get_rect()
            added_rect.topleft = (score_rect.right + 2*S_W, nb_y)
            header.blit(added_img, added_rect.topleft)

        game_name_img = relief_text(
            "SNEAKYMATH", self.fonts["stat"], self.colors["white_txt"], depth)
        game_name_rect = game_name_img.get_rect()
        game_name_rect.topleft = (3*S_W, stat_y)
        header.blit(game_name_img, game_name_rect.topleft)

        return header.convert()

    def body_part(self, ope):

        image = self.dflt["Body_part"].copy()

        if ope != None:
            self.render_ope(image, ope)

        return image.convert_alpha()

    def number(self, value):

        image = make_tile(color_palette(nb_color(value)))

        font = self.fonts["nb"]
        nb = str(value)
        nb_img = relief_text(nb, font, self.colors["white_txt"])
        rect = nb_img.get_rect()
        offset = (round((T_W - rect.w) / 2), round((T_H - rect.h) / 2))
        image.blit(nb_img, offset)

        return image.convert_alpha()

    def operation(self, ope):

        image = self.dflt["Operation"].copy()
        self.render_ope(image, ope)

        return image.convert_alpha()
