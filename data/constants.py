"""Global constants file"""

import pygame

pygame.init()

# Infos
GAME_NAME = "SneakyMath"
VERSION = "1.1"
FILES_PATH = "data/files"
FONTS_PATH = "data/fonts"


# Screen
infoObject = pygame.display.Info()
SCREEN_W = infoObject.current_w
SCREEN_H = infoObject.current_h
SCREEN_SIZE = (SCREEN_W, SCREEN_H)

NB_COLS = 20
NB_ROWS = 10

T_L = min(SCREEN_W // NB_COLS, SCREEN_H // (NB_ROWS + 1))
T_W = T_L
T_H = T_L
T_SIZE = (T_W, T_H)
S_W = round(T_W / 10)
S_H = round(T_H / 10)

FIELD_W = T_W * NB_COLS
FIELD_H = T_H * NB_ROWS

HEADER_H = SCREEN_H - FIELD_H
HEADER_W = SCREEN_W

FIELD_OFFSET_X = round((SCREEN_W - FIELD_W) / 2)
FIELD_OFFSET_Y = HEADER_H


# View
FPS = 60
NB_FRAMES = 13

# Gameplay
SCORE_INC = 3


# Style
RADIUS = 0.2
FONT_SIZE = round(11 / 20 * T_W)
DEPTH = S_H
BORDER = S_W
CONTRAST = 0.9
