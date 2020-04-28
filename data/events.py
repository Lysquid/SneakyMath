"""Events"""

import pygame as pg


class Events:
    """Events class"""

    def __init__(self):
        self.actions_keys = {
            pg.K_ESCAPE: ("excape", "unpause"),
            pg.K_RETURN: ("enter", "menu", "unpause"),
            pg.K_F4: ("f4",),
            pg.K_UP: ("up",),
            pg.K_DOWN: ("down",),
            pg.K_RIGHT: ("right",),
            pg.K_LEFT: ("left",),
        }
        self.dir_keys = {
            pg.K_UP: "up",
            pg.K_DOWN: "down",
            pg.K_RIGHT: "right",
            pg.K_LEFT: "left",
        }
        self.opposite_dir = {
            "up": "down",
            "down": "up",
            "right": "left",
            "left": "right",
            None: None,
        }
        self.dir_list = []

    def get(self):
        """Handle pgame events to return corresponding game events"""
        keys_down = pg.key.get_pressed()
        actions = []
        for event in pg.event.get():
            if event.type == pg.QUIT:
                actions.append("quit")
                continue
            if event.type == pg.KEYDOWN:
                if event.key in self.actions_keys:
                    actions.extend(self.actions_keys[event.key])
            if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                if event.key in self.dir_keys:
                    self.track_dir(event)
        if keys_down[pg.K_LALT] and "f4" in actions:
            actions.append("quit")

        return actions

    def track_dir(self, event):
        """Keeps track of directional key presses"""
        direction = self.dir_keys[event.key]
        if event.type == pg.KEYDOWN:
            self.dir_list.append(direction)
        if event.type == pg.KEYUP:
            if direction in self.dir_list:
                self.dir_list.remove(direction)

    def calc_dir(self, snake_dir, prev_dir):
        """Return the direction based on the """
        for potential_dir in self.dir_list:
            if potential_dir != self.opposite_dir[snake_dir]:
                return potential_dir
        return prev_dir

    @staticmethod
    def get_dir(actions, prev_dir):
        """Handle mouvements events to return corresponding direction"""
        direction = prev_dir

        keys_down = pg.key.get_pressed()
        if keys_down[pg.K_UP] and prev_dir != "down":
            direction = "up"
        if keys_down[pg.K_DOWN] and prev_dir != "up":
            direction = "down"
        if keys_down[pg.K_RIGHT] and prev_dir != "left":
            direction = "right"
        if keys_down[pg.K_LEFT] and prev_dir != "right":
            direction = "left"
        print(actions)
        if "up" in actions and prev_dir != "down":
            direction = "up"
        if "down" in actions and prev_dir != "up":
            direction = "down"
        if "right" in actions and prev_dir != "left":
            direction = "right"
        if "left" in actions and prev_dir != "right":
            direction = "left"

        return direction


EVENTS = Events()
