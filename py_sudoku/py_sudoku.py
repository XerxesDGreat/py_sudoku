__author__ = 'josh'

import pygame
import sys
import gameboard

def main():
    pygame.init()

    grid_obj = gameboard.Grid()
    grid_rect = grid_obj.get_rect()

    screen = pygame.display.set_mode((grid_rect.width, grid_rect.height))
    screen.blit(grid_obj.grid, (0,0))
    pygame.display.flip()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

if __name__ == "__main__":
    main()
