"""Main program"""

import pygame

import data.constants as c
from data.snake import Snake
from data.view import VIEW
from data.textures import TEXTURES
from data.events import EVENTS
from data.grid import Grid


def main():
    """Main program"""

    view = VIEW
    textures = TEXTURES
    events = EVENTS

    # Window settings
    view.customize_window()
    view.update()

    # Booleans
    main_loop = True
    state = "menu"
    prev_state = None
    active_game = False
    best_score = 0
    new_best = False

    # Main loop
    while main_loop:

        # Menu
        while main_loop and state == "menu":

            if prev_state != state:
                view.draw_menu()
                pygame.display.flip()
                active_game = False
                prev_state = state
            else:
                view.tick()

            actions = events.get()
            if "quit" in actions:
                main_loop = False
            if "enter" in actions:
                state = "game"

        # Game
        while main_loop and state == "game":

            if prev_state != state:
                if not active_game:
                    grid = Grid()
                    snake = Snake(grid)
                    direction = None
                    active_game = True
                prev_state = state

            header = textures.header(snake)

            prev_dir = direction
            for i_refresh in range(c.NB_REFRESH):

                progress = i_refresh / c.NB_REFRESH
                field = view.draw_field(grid, snake, progress)
                view.draw_screen(header, field)
                view.update()

                view.tick()
                actions = events.get()
                if "quit" in actions:
                    main_loop = False
                    break
                if "escape" in actions:
                    state = "pause"
                    break

                key = pygame.key.get_pressed()

                if key[pygame.K_UP] and snake.dir != "down" and prev_dir != "up":
                    direction = "up"
                if key[pygame.K_DOWN] and snake.dir != "up" and prev_dir != "down":
                    direction = "down"
                if key[pygame.K_RIGHT] and snake.dir != "left" and prev_dir != "right":
                    direction = "right"
                if key[pygame.K_LEFT] and snake.dir != "right" and prev_dir != "left":
                    direction = "left"

            if snake.dead:
                header = textures.header(snake)
                state = "game over"
                if snake.score > best_score:
                    best_score = snake.score
                    new_best = True
                break

            if prev_dir:
                snake.calc_score()
                snake.move_body()
                snake.tail_trail()
                snake.check_front()
                snake.move_head()
                snake.check_size()
            if direction:
                snake.orient(direction)

        # Pause
        while main_loop and state == "pause":

            if prev_state != state:
                view.draw_pause()
                view.update()
                prev_state = state
            else:
                view.tick()

            actions = events.get()
            if "quit" in actions:
                main_loop = False
            if "escape" in actions:
                state = "menu"
            if "enter" in actions:
                state = "game"

        while main_loop and state == "game over":

            if prev_state != state:
                view.draw_game_over(snake.score, best_score, new_best)
                view.update()
                new_best = False
                prev_state = state
            else:
                view.tick()

            actions = events.get()
            if "quit" in actions:
                main_loop = False
            if "escape" in actions:
                state = "menu"
            if "enter" in actions:
                state = "menu"

    pygame.quit()
