"""Events"""

import pygame


class Events:
    """Events class"""

    @staticmethod
    def get():
        """Handle pygameame events to return corresponding game events"""
        keys_down = pygame.key.get_pressed()
        pressed_keys = set()
        actions = set()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                actions.add("quit")
            elif event.type == pygame.KEYDOWN:
                pressed_keys.add(event.key)
        if pygame.K_ESCAPE in pressed_keys:
            actions.add("escape")
        if pygame.K_RETURN in pressed_keys:
            actions.add("enter")
        if keys_down[pygame.K_LALT] and pygame.K_F4 in pressed_keys:
            actions.add("quit")

        return actions

    @staticmethod
    def get_direction():
        """Handle mouvements events to return corresponding direction"""


EVENTS = Events()
