"""Main program"""

import pygame

import data.constants as c
from data.snake import Snake
from data.textures import Textures
from data.view import PygView


def main():
    """Main program"""

    # Pygame initialization
    pygame.init()
    view = PygView()
    texture = Textures(view)

    # Window settings
    pygame.display.set_caption("SneakyMath")
    view.texture.set_icon()

    # Booleans
    main_loop = True
    state = "menu"
    active_game = False
    best_score = 0
    new_best = False

    # Main loop
    while main_loop:

        if main_loop and state == "menu":

            active_game = False
            view.draw_menu()

            pygame.display.flip()

            while main_loop and state == "menu":

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        main_loop = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            main_loop = False
                        if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                            state = "game"

                view.clock.tick(c.FPS)

        if main_loop and state == "game":

            if not active_game:
                view.game_init()
                snake = Snake(view)
                view.generate_grid()

                direction = None
                active_game = True

            while main_loop and state == "game":

                view.prev_grid = PygView.copy_grid(view.grid)

                header = texture.header(snake)

                if direction is not None:
                    snake.calc_score()
                    snake.move_body(direction)
                    snake.tail_trail()
                    snake.check_front()
                    snake.move_head()
                    snake.check_size()

                for i_refresh in range(c.NB_REFRESH):

                    progress = i_refresh / c.NB_REFRESH
                    field = view.draw_field(progress)
                    view.draw_screen(header, field)
                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            main_loop = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                state = "pause"

                    if state == "pause":
                        break

                    key = pygame.key.get_pressed()
                    prev_dir = direction
                    if key[pygame.K_UP] and snake.dir != "down" and prev_dir != "up":
                        direction = "up"
                    if key[pygame.K_DOWN] and snake.dir != "up" and prev_dir != "down":
                        direction = "down"
                    if (
                        key[pygame.K_RIGHT]
                        and snake.dir != "left"
                        and prev_dir != "right"
                    ):
                        direction = "right"
                    if (
                        key[pygame.K_LEFT]
                        and snake.dir != "right"
                        and prev_dir != "left"
                    ):
                        direction = "left"

                    view.clock.tick(c.FPS)

                if snake.dead:
                    header = texture.header(snake)
                    view.grid = PygView.copy_grid(view.prev_grid)
                    state = "game over"
                    if snake.score > best_score:
                        best_score = snake.score
                        new_best = True

        if main_loop and state == "pause":

            view.draw_pause()
            pygame.display.flip()

            while main_loop and state == "pause":

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        main_loop = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            state = "menu"
                        if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                            state = "game"

        if main_loop and state == "game over":

            view.draw_game_over(best_score, new_best)
            new_best = False
            pygame.display.flip()

            while main_loop and state == "game over":

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        main_loop = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            state = "menu"
                        if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                            state = "menu"

                view.clock.tick(c.FPS)

    pygame.quit()
