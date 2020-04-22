"""
All classes used in the game
"""

# Modules
import random
import math
import pygame
from data.consts import *
from data.textures import *


class PygView():
    """
    General class which is the main storage for the game :
    contains the screen to show and the grid of tiles
    """

    def __init__(self):
        """ Constructor function """
        # Create the display
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        # Create the clock used to control the frame rate
        self.clock = pygame.time.Clock()

        self.texture = None

    def game_init(self):
        """ Initialize the basic objects needed for the game """
        # Create the grid, where are stored all tiles at their respective position
        self.grid = [[None for y in range(NB_TILES_Y)]
                     for x in range(NB_TILES_X)]
        self.prev_grid = []  # Make a slot for the previous grid, used to keep data
        self.snake = None  # Slot for snake once created

    def generate_grid(self):
        """ Generate tiles on the grid to have an initial layout """
        # Set constants used for placement
        x_offset, y_offset = round(NB_TILES_X / 4), round(NB_TILES_Y / 4)
        # List of operations tiles with their positions
        ope_list = [
            ("+", (x_offset, y_offset)),
            ("+", (NB_TILES_X - x_offset - 1, NB_TILES_Y - y_offset - 1)),
            ("-", (x_offset, NB_TILES_Y - y_offset - 1)),
            ("-", (NB_TILES_X - x_offset - 1, y_offset))]
        # Place operations tiles
        for ope, pos in ope_list:
            Operation(self, ope, pos)
        # Place random number tiles
        for i in range(10):
            x, y = random.randint(
                0, NB_TILES_X - 1), random.randint(0, NB_TILES_Y - 1)
            if self.grid[x][y] == None:  # Check if tile is free
                Number(self, (x, y))

    def draw_menu(self):
        """ Draw the menu screen """
        self.screen.fill(self.texture.colors["bg"])
        self.texture.render_text(self, "SNEAKYMATH", "title")
        self.texture.render_text(
            self, "Appuyer sur [Enter] pour commencer", "menu2")
        self.texture.render_text(
            self, "© Créé par Romain avec l'aide de Natan pour le prix Bernard Novelli des Trophées Tangente 2020", "footnote")

    def draw_pause(self):
        self.screen.fill(self.texture.colors["bg"])
        self.texture.render_text(
            self, "Pause", "menu1", color_palette(nb_color(1), 0.8))
        self.texture.render_text(
            self, "Appuyer sur [Entrer] pour reprendre", "menu2")

    def draw_game_over(self, best_score, new_best):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))
        self.texture.render_text(
            self, "Game Over", "menu1", color_palette(nb_color(9), 0.8))
        self.texture.render_text(
            self, "Score : " + str(self.snake.score), "menu2")
        if new_best:
            colors = self.texture.colors["snake"]
        else:
            colors = self.texture.colors["white_txt"]
        self.texture.render_text(
            self, "Meilleur score : " + str(best_score), "menu3", colors)

    def draw_field(self, progress):
        """ Draw everything from the grid onto the screen """
        # Create the field from the default field
        field = self.texture.dflt["field"].copy()
        # Draw the blocks from the grid onto the field
        for x in range(NB_TILES_X):
            for y in range(NB_TILES_Y):

                tile2draw = self.prev_grid[x][y]

                if isinstance(tile2draw, Block):  # Draw it only if it's not a snake part
                    field.blit(tile2draw.image, tile2draw.get_coords(progress))

        # Draw the snake parts (from the end) on the field
        for part in reversed(self.snake.parts):
            x, y = part.get_coords(progress, self.snake.dead)
            field.blit(part.image, (x, y))
            if x < 0:
                x += FIELD_W
            elif x + T_W > FIELD_W:
                x -= FIELD_W
            if y < 0:
                y += FIELD_H
            elif y + T_H > FIELD_H:
                y -= FIELD_H
            field.blit(part.image, (x, y))

        return field

    def draw_screen(self, header, field):
        self.screen.fill((0, 0, 0))
        self.screen.blit(field, (0, HEADER_H))

        self.screen.blit(header, (0, 0))

    def copy_grid(grid):
        """ Return a deep copy of a grid """
        return [[grid[x][y] for y in range(NB_TILES_Y)] for x in range(NB_TILES_X)]

    def new_pos(direction, pos):
        x, y = pos
        if direction == "up":
            y -= 1
        if direction == "down":
            y += 1
        if direction == "right":
            x += 1
        if direction == "left":
            x -= 1

        x %= NB_TILES_X
        y %= NB_TILES_Y

        return (x, y)


class Snake():
    """
    Snake class, containing a lot of information about the player
    """

    def __init__(self, view):

        view.snake = self
        self.view = view
        self.score = 0
        self.added_score = 0
        self.size = 1
        self.inc = 4
        self.goal = random.randint(10, 20)
        self.goal_reached = False
        self.dead = False
        self.tail_queue = []
        self.dir = None
        self.dir_hist = []
        self.ope = "+"
        self.head = Body_part(
            view, (NB_TILES_X // 2, NB_TILES_Y // 2), self.ope)
        self.head_pos = (self.head.x, self.head.y)
        self.tail = self.head
        self.tail_pos = self.head_pos
        self.parts = [self.head]

    def move_body(self, direction):
        self.dir = direction
        self.dir_hist.insert(0, self.dir)
        for i, part in enumerate(self.parts):
            if part == self.tail:
                self.tail_pos = (part.x, part.y)
            if part == self.head:
                continue
            part.move(self.dir_hist[i])
        self.view.grid[self.tail_pos[0]][self.tail_pos[1]] = None

    def tail_trail(self):
        if len(self.tail_queue) and self.inc == 0:
            block2place = self.tail_queue.pop(0)
            block2place.spawn(self.tail_pos)
        if self.inc > 0:
            self.tail = Body_part(self.view, self.tail_pos)
            self.parts.append(self.tail)
            self.size += 1
            self.inc -= 1
        elif self.inc < 0:
            removed = self.parts.pop(-1)
            self.view.grid[removed.x][removed.y] = None
            self.tail_pos = (self.tail.x, self.tail.y)
            self.size -= 1
            if len(self.parts) > 0:
                self.tail = self.parts[-1]
                self.inc += 1

    def check_front(self):
        self.head_pos = PygView.new_pos(self.dir, self.head_pos)
        front_tile = self.view.grid[self.head_pos[0]][self.head_pos[1]]
        if front_tile != None:
            if isinstance(front_tile, Number):
                if self.ope == "+":
                    self.inc += front_tile.value
                    nb_new = 2
                elif self.ope == "-":
                    self.inc -= front_tile.value
                    nb_new = 2
                self.added_score = 1
                for i in range(nb_new):
                    self.tail_queue.append(Number(self.view))
            if isinstance(front_tile, Operation):
                if front_tile.ope == "+":
                    self.ope = "+"
                    self.tail_queue.append(Operation(self.view, "-"))
                elif front_tile.ope == "-":
                    self.ope = "-"
                    self.tail_queue.append(Operation(self.view, "+"))
                self.head.image = self.view.texture.body_part(self.ope)
            elif front_tile in self.parts:
                self.dead = True

    def move_head(self):
        self.head.move(self.dir, remove=False)

    def check_size(self):
        if self.size <= 0:
            self.dead = True
        if self.size == self.goal and self.inc == 0:

            self.goal = self.new_goal(self.score, self.goal)
            self.goal_reached = True
            self.added_score = 20
            n_nb = round(sum(isinstance(block, Number)
                             for block in self.tail_queue) / 2)
            new_tail = []
            for block in self.tail_queue:
                if n_nb > 0 and isinstance(block, Number):
                    n_nb -= 1
                else:
                    new_tail.append(block)
            self.tail_queue = new_tail
            # !! Delete all numbers code: self.tail_queue = [block for block in  if not isinstance(block, Number)]

    def new_goal(self, score, goal):
        """ # 1st code
        (int(str(score)[::-1]) - 1) % 50 + 1
        """
        """ # 2nd code
        return (goal + score - 1) % (35 + round(score / 15)) + 1

        """
        # Natan's code
        bound = 8 + round(1.5 * math.sqrt(score))
        diff = min(40, 3 + score ** 1.2 // 70)
        prev_goal = goal
        while prev_goal < goal + diff and prev_goal > goal - diff:
            goal = random.randint(max(1, min(15, prev_goal - bound)),
                                  min(max(prev_goal + bound, 20), 35 + math.floor(math.sqrt(score))))
        return goal

    def calc_score(self):
        self.score += self.added_score
        self.added_score = 0
        self.goal_reached = False


class Tile():

    def __init__(self, view, pos):
        self.view = view
        self.rect = pygame.Rect(0, 0, T_W, T_H)
        if pos != None:
            self.spawn(pos)

    def spawn(self, pos):
        self.x, self.y = pos
        self.view.grid[self.x][self.y] = self

    def get_coords(self, progress):
        self.rect.x = self.x * T_W
        self.rect.y = self.y * T_H
        return self.rect.topleft


class Body_part(Tile):

    def __init__(self, view, pos, ope=None):

        super().__init__(view, pos)

        self.image = view.texture.body_part(ope)

        self.prev_x, self.prev_y = self.x, self.y
        self.dir = None

    def move(self, direction, remove=True):

        self.prev_x, self.prev_y = self.x, self.y

        self.dir = direction

        self.x, self.y = PygView.new_pos(self.dir, (self.x, self.y))

        self.view.grid[self.x][self.y] = self

    def get_coords(self, progress, dead=False):
        if not dead:
            offset = round(progress * T_W)
        else:
            offset = round(0.5 * (-(progress * 2 - 1) ** 2 + 1) * T_W)
        self.rect.x = self.prev_x * T_W + \
            ((self.dir == "right") - (self.dir == "left")) * offset
        self.rect.y = self.prev_y * T_H + \
            ((self.dir == "down") - (self.dir == "up")) * offset

        return self.rect.topleft


class Block(Tile):

    def __init__(self, view, pos):
        super().__init__(view, pos)


class Number(Block):

    def __init__(self, view, pos=None, value=None):
        super().__init__(view, pos)

        if value == None:
            self.value = random.randint(1, 9)
        else:
            self.value = value

        self.image = view.texture.number(self.value)


class Operation(Block):

    def __init__(self, view, ope, pos=None):
        super().__init__(view, pos)

        self.ope = ope

        self.image = view.texture.operation(self.ope)
