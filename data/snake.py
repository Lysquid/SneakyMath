"""Snake class file"""

import data.constants as c
from data.tiles import SnakePart, Number, Operation


class Snake:
    """Snake class
    """

    def __init__(self):
        self.dead = False
        self.inc = 4
        center_pos = (c.NB_COLS // 2, c.NB_ROWS // 2)
        self.parts = [SnakePart(center_pos)]
        self.behind_queue = []
        self.behind_pos = None
        self.ope = "change to +"

    def __len__(self):
        return len(self.parts)

    def _get_head(self):
        return self.parts[0]

    def _get_tail(self):
        return self.parts[-1]

    def _get_dir(self):
        if self.parts:
            return self.head.dir
        return None

    head = property(_get_head)
    tail = property(_get_tail)
    dir = property(_get_dir)

    def place_head(self, grid):
        """Place the head onto the screen
        and eventually change its texture
        """
        grid[self.head.pos] = self.head
        if self.ope.startswith("change"):
            self.ope = self.ope[-1]
            self.head.set_ope(self.ope)

    def move_body(self, grid, direction):
        """Move each body part one by one
        starting from the head
        """
        for part in self.parts:
            if part == self.tail:
                self.behind_pos = part.pos
            grid[part.pos] = None
            prev_dir = part.dir
            part.dir = direction
            part.move()
            if part is not self.head:
                grid[part.pos] = part
            direction = prev_dir

    def behind_trail(self, grid):
        """Handle what's behind the snake
        (new block, adding or removing a body part)
        """
        if self.behind_queue and not self.inc:
            grid[self.behind_pos] = self.behind_queue.pop(0)
        if self.inc > 0:
            self.parts.append(SnakePart())
            grid[(self.behind_pos)] = self.tail
            self.inc -= 1
        elif self.inc < 0:
            removed_part = self.parts.pop(-1)
            grid[removed_part.pos] = None
            self.behind_pos = removed_part.pos
            self.inc += 1
            if not self.parts:
                self.dead = True

    def check_front(self, grid, player):
        """Check the front tile and react
        depending of what's found
        """
        if not self.parts:
            return
        front_tile = grid[self.head.pos]
        if front_tile:
            # Face a number
            if isinstance(front_tile, Number):
                if "+" in self.ope:
                    self.inc += front_tile.value
                    nbr_new = 2
                elif "-" in self.ope:
                    self.inc -= front_tile.value
                    nbr_new = 2
                player.added_score += 1
                for _ in range(nbr_new):
                    self.behind_queue.append(Number())
            # Face an operation
            if isinstance(front_tile, Operation):
                self.ope = "change to " + front_tile.ope
                if front_tile.ope == "+":
                    self.behind_queue.append(Operation("-"))
                elif front_tile.ope == "-":
                    self.behind_queue.append(Operation("+"))
            # Face a body part
            elif front_tile in self.parts:
                self.dead = True

    def goal_reached(self, player):
        """Check if the goal is reached"""
        if len(self) == player.goal and not self.inc:
            player.goal_reached = True

            n_nbrs = sum(isinstance(block, Number) for block in self.behind_queue)
            new_n_nbrs = round(n_nbrs / 2)
            new_behind = []
            for block in self.behind_queue:
                if new_n_nbrs > 0 and isinstance(block, Number):
                    new_n_nbrs -= 1
                else:
                    new_behind.append(block)
            self.behind_queue = new_behind
