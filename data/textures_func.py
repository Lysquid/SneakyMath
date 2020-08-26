"""Texture functions file"""

import pygame as pg
from pygame import gfxdraw

import data.constants as c


def rounded_rec(image, color, rect, radius):
    """Draw a rounded rectangle"""
    temp = pg.Surface(rect.size, pg.SRCALPHA, 32)

    circle_centers = (
        (radius, radius),
        (rect.w - radius, radius),
        (radius, rect.h - radius),
        (rect.w - radius, rect.h - radius),
    )
    for circle_center in circle_centers:
        x_coord, y_coord = circle_center
        gfxdraw.aacircle(temp, x_coord, y_coord, radius, color)
        gfxdraw.filled_circle(temp, x_coord, y_coord, radius, color)

    rec_rects = (
        pg.Rect(radius, 0, rect.w - 2 * radius, rect.h),
        pg.Rect(0, radius, rect.w, rect.h - 2 * radius),
    )
    for rec_rect in rec_rects:
        pg.draw.rect(temp, color, rec_rect)

    image.blit(temp, rect.topleft)
    return image.convert_alpha()


def tile(colors, size=c.T_SIZE, depth=c.DEPTH, border=c.BORDER, rounded=c.RADIUS):
    """Draw a tile with relief"""
    img = pg.Surface(size, pg.SRCALPHA, 32)
    rects = []

    rect = img.get_rect()
    rect.x += border
    rect.y += border
    rect.w -= 2 * rect.x
    rect.h -= 2 * rect.y
    rects.append(rect)

    rect = rect.copy()
    rect.y -= depth
    rects.append(rect)

    rect = rect.copy()
    rect.x += border
    rect.y += border
    rect.w -= 2 * border
    rect.h -= 2 * border
    rects.append(rect)

    rect = rect.copy()
    rect.y += depth
    rect.h -= depth
    rects.append(rect)

    for rect_id, color_id in enumerate((1, 0, 1, 2)):
        color = colors[color_id]
        rect = rects[rect_id]
        radius = round(min(rects[rect_id].size) * rounded)
        rounded_rec(img, color, rect, radius)

    return img.convert_alpha()


def field_tile(colors, size=c.T_SIZE, depth=c.DEPTH, rounded=c.RADIUS):
    """Draw a background tile, the one blitted on the screen"""
    img = pg.Surface(size)
    rects = []

    rect = img.get_rect()
    rect.topleft = (c.S_W, c.S_H)
    rect.w -= 2 * rect.x
    rect.h -= 2 * rect.y
    rects.append(rect)

    rect = rect.copy()
    rect.y += depth
    rect.h -= depth
    rects.append(rect)

    img.fill(colors[0])
    for rect_id, color_id in enumerate((1, 2)):
        color = colors[color_id]
        rect = rects[rect_id]
        radius = round(rects[rect_id].w * rounded)
        rounded_rec(img, color, rect, radius)

    return img.convert()


def relief_text(text, font, colors, depth=c.DEPTH):
    """Draw the text in relief"""
    text = str(text)

    color = colors[2]
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    rect.h += depth
    image = pg.Surface(rect.size, pg.SRCALPHA, 32)

    for y_inc in range(depth):
        coords = (0, y_inc + 1)
        image.blit(rendered, coords)

    color = colors[0]
    rendered = font.render(text, True, color)
    image.blit(rendered, (0, 0))

    return image.convert_alpha()


def color_palette(color, multiplier=1):
    """Generate a color palette from one color"""
    colors = [color]
    contrast = multiplier * c.CONTRAST
    for i in range(2):
        color = [round(value * contrast) for value in colors[i]]
        colors.append(tuple(color))
    return colors


def nbr_color(value):
    """Generate the color of a number block
    depending to its value
    """
    return (150 + value * 10, 120, 100 + (10 - value) * 10)


def get_font(font_path, multiplier=1):
    """Get font from fonts folder"""
    font_size = round(c.FONT_SIZE * multiplier)
    return pg.font.Font(font_path, font_size)
