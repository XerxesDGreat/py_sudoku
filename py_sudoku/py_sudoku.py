__author__ = 'josh'

import pygame
import sys
import gameboard
import os
import time


FPS = 60
NUMBER_KEY_TYPE = "number"
MOVEMENT_KEY_TYPE = "movement"
EDIT_KEY_TYPE = "edit"

def quit():
    """
    Quits the game, cleaning up anything if necessary
    """
    sys.exit()

def get_puzzle():
    """
    Gets a puzzle definition
    :return list:
    """
    import puzzles.easy
    return puzzles.easy.puzzles[0]

def get_key_pressed_value(key):
    """
    Gets the value of the key constant provided. If not between K_0 and K_9 or
    K_KP0 and K_KP9 (inclusive), returns None.
    """
    type = None
    value = None
    if key >= pygame.K_1 and key <= pygame.K_9:
        type = NUMBER_KEY_TYPE
        value = key - pygame.K_0
    if key >= pygame.K_KP1 and key <= pygame.K_KP9:
        type = NUMBER_KEY_TYPE
        value = key - pygame.K_KP0
    if key >= pygame.K_UP and key <= pygame.K_LEFT:
        type = MOVEMENT_KEY_TYPE
        value = key
    if key == pygame.K_DELETE or key == pygame.K_BACKSPACE:
        type = EDIT_KEY_TYPE
        value = key
    return type, value

def do_completion():
    print "holy crap you're done!"
    time.sleep(5)
    quit()

def main():
    """
    Main logic for the game
    """
    os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (1930,30)
    pygame.init()

    clock = pygame.time.Clock()
    playtime = 0

    screen = pygame.display.set_mode((1000,800))
    screen.fill((128,128,128))

    puzzle = get_puzzle()

    grid = gameboard.Grid()
    grid.create_grid(screen, puzzle)

    selected = None

    while 1:

        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
        playtime += seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT: quit()
            if event.type == pygame.KEYDOWN:
                # escape quits the game
                if event.key == pygame.K_ESCAPE:
                    quit()

                # don't have anything selected, can't do anything
                if selected is None:
                    continue

                # handle some key strokes
                key_type, key_val = get_key_pressed_value(event.key)

                # movements
                if key_type == MOVEMENT_KEY_TYPE:
                    selected.on_deselect()
                    selected = grid.move_sel_in_direction(selected, key_val)
                    selected.on_click()

                # if the selection can't be changed, can't do anything
                if selected.immutable:
                    continue

                # handle number key pressed
                if key_type == NUMBER_KEY_TYPE:
                    selected.set_value(key_val)
                elif key_type == EDIT_KEY_TYPE:
                    selected.on_edit(key_val)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if selected is not None:
                        selected.on_deselect()
                    selected = grid.get_tile_at_pos(pygame.mouse.get_pos())
                    print "tl: %s, br: %s" % (str(selected.rect.topleft), str(selected.rect.bottomright))
                    selected.on_click()

        pygame.display.set_caption("[FPS]: %.2f" % clock.get_fps())
        grid.tiles.update_all(grid)
        screen.blit(grid.background, (0,0))
        pygame.display.update()
        if grid.is_complete():
            do_completion()


if __name__ == "__main__":
    main()
