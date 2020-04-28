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
                    snake = Snake()
                    snake.place_head(grid)
                    grid.generate()
                    direction = None
                    active_game = True
                prev_state = state

            header = textures.header(snake)

            for i_refresh in range(c.NB_REFRESH):

                progress = i_refresh / c.NB_REFRESH
                field = view.draw_field(grid, snake, progress)
                view.draw_game(header, field)
                view.update()

                view.tick()
                actions = events.get()
                if "quit" in actions:
                    main_loop = False
                    break
                if "escape" in actions:
                    state = "pause"
                    break

                direction = events.calc_dir(snake.dir, direction)

            if snake.dead:
                header = textures.header(snake)
                state = "game over"
                if snake.score > best_score:
                    best_score = snake.score
                    new_best = True
                break

            if snake.dir:
                snake.calc_score()
                snake.move_body(grid)
                snake.behind_trail(grid)
                snake.check_front(grid)
                snake.place_head(grid)
                snake.check_size()
            snake.dir = direction

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
            if "unpause" in actions:
                state = "game"

        # Game over
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
