__author__ = 'josh'

import pygame
import sys
import gameboard

def main():
    pygame.init()

    screen = pygame.display.set_mode((800,800))
    screen.fill((128,128,128))

    puzzle = get_puzzle()

    grid = gameboard.Grid()
    grid.create_grid(screen, puzzle)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    tile = grid.get_tile_at_pos(pygame.mouse.get_pos())
                    print "tl: %s, br: %s" % (str(tile.rect.topleft), str(tile.rect.bottomright))
                    tile.on_click()
        grid.tiles.update_all(grid)
        screen.blit(grid.background, (0,0))
        pygame.display.update()

def quit():
    sys.exit()

def get_puzzle():
    import puzzles.easy
    return puzzles.easy.puzzles[0]

if __name__ == "__main__":
    main()
