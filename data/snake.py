"""Snake class file"""

import math
import random

import data.constants as c
from data.tiles import BodyPart, Number, Operation
from data.view import PygView


class Snake:
    """Snake class, containing a lot of information about the player
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
        self.head = BodyPart(view, (c.NB_TILES_X // 2, c.NB_TILES_Y // 2), self.ope)
        self.head_pos = (self.head.x, self.head.y)
        self.tail = self.head
        self.tail_pos = self.head_pos
        self.parts = [self.head]

    def move_body(self, direction):
        """Move body"""
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
        """Tail trail"""
        if self.tail_queue and self.inc == 0:
            block2place = self.tail_queue.pop(0)
            block2place.spawn(self.tail_pos)
        if self.inc > 0:
            self.tail = BodyPart(self.view, self.tail_pos)
            self.parts.append(self.tail)
            self.size += 1
            self.inc -= 1
        elif self.inc < 0:
            removed = self.parts.pop(-1)
            self.view.grid[removed.x][removed.y] = None
            self.tail_pos = (self.tail.x, self.tail.y)
            self.size -= 1
            if self.parts:
                self.tail = self.parts[-1]
                self.inc += 1

    def check_front(self):
        """Check front"""
        self.head_pos = PygView.new_pos(self.dir, self.head_pos)
        front_tile = self.view.grid[self.head_pos[0]][self.head_pos[1]]
        if front_tile is not None:
            if isinstance(front_tile, Number):
                if self.ope == "+":
                    self.inc += front_tile.value
                    nb_new = 2
                elif self.ope == "-":
                    self.inc -= front_tile.value
                    nb_new = 2
                self.added_score = 1
                for _ in range(nb_new):
                    self.tail_queue.append(Number(self.view))
            if isinstance(front_tile, Operation):
                if front_tile.ope == "+":
                    self.ope = "+"
                    self.tail_queue.append(Operation(self.view, "-"))
                elif front_tile.ope == "-":
                    self.ope = "-"
                    self.tail_queue.append(Operation(self.view, "+"))
                self.head.image = self.view.texture.BodyPart(self.ope)
            elif front_tile in self.parts:
                self.dead = True

    def move_head(self):
        """Move head"""
        self.head.move(self.dir, remove=False)

    def check_size(self):
        """Check size"""
        if self.size <= 0:
            self.dead = True
        if self.size == self.goal and self.inc == 0:

            self.goal = self.new_goal(self.score, self.goal)
            self.goal_reached = True
            self.added_score = 20
            n_nb = round(
                sum(isinstance(block, Number) for block in self.tail_queue) / 2
            )
            new_tail = []
            for block in self.tail_queue:
                if n_nb > 0 and isinstance(block, Number):
                    n_nb -= 1
                else:
                    new_tail.append(block)
            self.tail_queue = new_tail
            # !! Delete all numbers code:
            # self.tail_queue = [block for block in  if not isinstance(block, Number)]

    def new_goal(self, score, goal):
        """Generate new goal"""
        # 1st code
        # (int(str(score)[::-1]) - 1) % 50 + 1

        # 2nd code
        # return (goal + score - 1) % (35 + round(score / 15)) + 1

        # Natan's code
        bound = 8 + round(1.5 * math.sqrt(score))
        diff = min(40, 3 + score ** 1.2 // 70)
        prev_goal = goal
        while prev_goal < goal + diff and prev_goal > goal - diff:
            goal = random.randint(
                max(1, min(15, prev_goal - bound)),
                min(max(prev_goal + bound, 20), 35 + math.floor(math.sqrt(score))),
            )
        return goal

    def calc_score(self):
        """Calculate score"""
        self.score += self.added_score
        self.added_score = 0
        self.goal_reached = False
