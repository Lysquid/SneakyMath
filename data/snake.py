"""Snake class file"""

import math
import random

import data.constants as c
from data.tiles import BodyPart, Number, Operation
from data.textures import TEXTURES as textures


class Snake:
    """Snake class, containing a lot of information about the player
    """

    def __init__(self):
        self.score = 0
        self.added_score = 0
        self.inc = 4
        self.goal = random.randint(10, 20)
        self.goal_reached = False
        self.dead = False
        self.behind_queue = []
        self.dir = None
        self.head = BodyPart((c.NB_COLS // 2, c.NB_ROWS // 2))
        self._ope = None
        self.ope = "+"  # This second col also change the image
        self.parts = [self.head]
        self.tail = self.parts[0]
        self.behind_pos = None

    def __len__(self):
        return len(self.parts)

    def _get_ope(self):
        return self._ope

    def _set_ope(self, ope):
        self._ope = ope
        if self.head:
            self.head.image = textures.body_part(ope)

    ope = property(_get_ope, _set_ope)

    def move_body(self, grid):
        """Move body"""
        for part in self.parts:
            if part == self.tail:
                self.behind_pos = part.pos

            grid[part.pos] = None
            part.move()
            prev_dir = part.dir
            if part is self.head:
                part.dir = self.dir
            else:
                part.dir = direction
                grid[part.pos] = part
            direction = prev_dir

    def behind_trail(self, grid):
        """Behind trail"""
        if self.behind_queue and not self.inc:
            grid[self.behind_pos] = self.behind_queue.pop(0)
        if self.inc > 0:
            self.tail = BodyPart(self.behind_pos)
            self.parts.append(self.tail)
            self.inc -= 1
        elif self.inc < 0:
            removed_part = self.parts.pop(-1)
            grid[removed_part.pos] = None
            self.behind_pos = removed_part.pos
            self.inc += 1
            if self.parts:
                self.tail = self.parts[-1]
            else:
                self.dead = True

    def check_front(self, grid):
        """Check front"""
        front_tile = grid[self.head.pos]
        if front_tile:
            # Face a number
            if isinstance(front_tile, Number):
                if self.ope == "+":
                    self.inc += front_tile.value
                    nbr_new = 2
                elif self.ope == "-":
                    self.inc -= front_tile.value
                    nbr_new = 2
                self.added_score = 1
                for _ in range(nbr_new):
                    self.behind_queue.append(Number())
            # Face an operation
            if isinstance(front_tile, Operation):
                self.ope = front_tile.ope
                if front_tile.ope == "+":
                    self.behind_queue.append(Operation("-"))
                elif front_tile.ope == "-":
                    self.behind_queue.append(Operation("+"))
            # Face a body part
            elif front_tile in self.parts:
                self.dead = True

    def place_head(self, grid):
        """Move head"""
        grid[self.head.pos] = self.head

    def check_size(self):
        """Check size"""
        if len(self) == self.goal and not self.inc:

            self.goal = self.new_goal(self.score, self.goal)
            self.goal_reached = True
            self.added_score = 20
            n_nbrs = sum(isinstance(block, Number) for block in self.behind_queue)
            new_n_nbrs = round(n_nbrs / 2)
            new_tail = []
            for block in self.behind_queue:
                if new_n_nbrs > 0 and isinstance(block, Number):
                    new_n_nbrs -= 1
                else:
                    new_tail.append(block)
            self.behind_queue = new_tail
            # !! Delete all numbers code:
            # self.behind_queue = [block for block in  if not isinstance(block, Number)]

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
