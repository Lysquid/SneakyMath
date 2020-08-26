"""Global constants file"""

# Infos
GAME_NAME = "SneakyMath"
FILES_PATH = "data/files"


# Screen
T_W = 70  # individual tile width and height
T_H = T_W
T_SIZE = (T_W, T_H)
S_W = round(T_W / 10)
S_H = round(T_H / 10)
NB_COLS = 17
NB_ROWS = 9

HEADER_H = T_H

SCREEN_W = T_W * NB_COLS
SCREEN_H = T_H * NB_ROWS + HEADER_H
SCREEN_SIZE = (SCREEN_W, SCREEN_H)

FIELD_W = T_W * NB_COLS
FIELD_H = T_H * NB_ROWS

HEADER_W = SCREEN_W

OFFSET_X = 0  # offset of the field in the screen
OFFSET_Y = T_H


# View
FPS = 40
NB_FRAMES = 9

# Gameplay
SCORE_INC = 3


# Style
RADIUS = 0.2
FONT_SIZE = round(11 / 20 * T_W)
DEPTH = S_H
BORDER = S_W
CONTRAST = 0.9
