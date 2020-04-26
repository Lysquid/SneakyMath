"""Global constants"""


# Screen
T_W = 70  # individual tile width and height
T_H = T_W
S_W = round(T_W / 10)
S_H = round(T_H / 10)
NB_TILES_X = 17  # number of tiles in a row
NB_TILES_Y = 9  # number of tiles in a clomun

HEADER_H = T_H

SCREEN_W = T_W * NB_TILES_X  # screen/window width and height
SCREEN_H = T_H * NB_TILES_Y + HEADER_H

FIELD_W = T_W * NB_TILES_X  # field : visual grid of playground
FIELD_H = T_H * NB_TILES_Y

HEADER_W = SCREEN_W

OFFSET_X = 0  # offset of the field in the screen
OFFSET_Y = T_H

# Display
FPS = 40  # frames per second
NB_REFRESH = 9
# number of refresh of the screen per cycle of the game (odd number only)

# Style

RADIUS = 0.2
COLORS = {
    "field": [(50, 50, 50), 0.9],
    "snake": [(120, 230, 120), 0.9],
    "white": [(230, 230, 230), 0.9],
    "white_txt": [(230, 230, 230), 0.85],
    "black_txt": [(80, 80, 80), 0.8],
}
