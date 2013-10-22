__author__ = 'josh'

import pygame
import random

class Grid(object):
    """
    Class which handles the grid
    """

    # constants for various settings
    GRID_X_BOX_COUNT = 3
    GRID_Y_BOX_COUNT = 3
    BOX_X_TILE_COUNT = 3
    BOX_Y_TILE_COUNT = 3
    BOX_BORDER_WIDTH = 1
    BOX_BORDER_COLOR = (0,0,0)

    boxes = []
    columns = []
    rows = []
    grid = []
    tiles = []

    def __init__(self):
        """
        Constructor
        """
        self.boxes = []
        self.columns = []
        self.rows = []
        self.tiles = pygame.sprite.Group()

        self._create_grid()

    def get_rect(self):
        """
        Get the rectangle which contains the surface
        :return Rectangle:
        """
        return self.grid.get_rect()

    def _create_grid(self):
        """
        Create the grid
        """
        # create all the tiles we need
        tile_x_count = Grid.GRID_X_BOX_COUNT * Grid.BOX_X_TILE_COUNT
        tile_y_count = Grid.GRID_Y_BOX_COUNT * Grid.BOX_Y_TILE_COUNT

        for i in range(0, (tile_x_count * tile_y_count)):
            self.tiles.add(self._create_tile(i))

        # now, create each box
        b = None
        for i in range(0, (Grid.GRID_X_BOX_COUNT * Grid.GRID_Y_BOX_COUNT)):
            if b is None:
                b = TileContainer(BoxLayout)
                tmp_box = b
            else:
                tmp_box = b.copy()
            self.boxes.append(tmp_box)

        # attach the tiles to the boxes, columns, and rows
        box_count = Grid.GRID_X_BOX_COUNT * Grid.GRID_Y_BOX_COUNT
        i = 0
        for tile in iter(self.tiles):
            target_box = i / box_count # yay integer math!
            x_coord = (i % Grid.BOX_X_TILE_COUNT) * Tile.TILE_WIDTH + Grid.BOX_BORDER_WIDTH
            y_coord = ((i / Grid.BOX_X_TILE_COUNT) % Grid.BOX_Y_TILE_COUNT) * Tile.TILE_HEIGHT + Grid.BOX_BORDER_WIDTH
            self.boxes[target_box].update(tile, (x_coord, y_coord))

            tile_row_offset = (target_box / Grid.GRID_X_BOX_COUNT) * Grid.GRID_Y_BOX_COUNT
            base_row_index = i - (target_box * box_count) / Grid.GRID_X_BOX_COUNT
            row_index = base_row_index + tile_row_offset
            if row_index >= len(self.rows):
                self.rows.append(TileContainer(RowLayout))
            self.rows[row_index].add(tile)

            tile_column_offset = (target_box % Grid.GRID_Y_BOX_COUNT) * Grid.GRID_Y_BOX_COUNT
            base_column_index = i % Grid.GRID_Y_BOX_COUNT
            column_index = base_column_index + tile_column_offset
            if column_index >= len(self.columns):
                self.columns.append(TileContainer(ColumnLayout))
            self.columns[column_index].add(tile)

            i += 1

        # create the main grid container
        box_width = Tile.TILE_WIDTH * Grid.BOX_X_TILE_COUNT + 5
        box_height = Tile.TILE_HEIGHT * Grid.BOX_Y_TILE_COUNT + 5
        self.grid = pygame.Surface((box_width * Grid.GRID_X_BOX_COUNT, box_height * Grid.GRID_Y_BOX_COUNT))

        # attach the boxes
        for i in range(len(self.boxes)):
            x_coord = (i % Grid.GRID_X_BOX_COUNT) * box_width
            y_coord = ((i / Grid.GRID_X_BOX_COUNT) % Grid.GRID_Y_BOX_COUNT) * box_height
            self.boxes[i].draw(self.grid)


    def _create_tile(self, id, color=None):
        """
        Return an individual tile

        :param color: A tuple describing the color of the tile
        :return Surface:
        """
        t = Tile(id)
        t.set_text(t.id)
        return t


class Tile(pygame.sprite.DirtySprite):
    TILE_WIDTH = 40
    TILE_HEIGHT = 40

    DEFAULT_FONT = "monospace"

    def __init__(self, id, color = None, *args, **kwargs):
        """
        Constructor for this object; builds the Surface as well
        """
        super(Tile, self).__init__()
        self.id = id
        self.font = None
        self.background = pygame.Surface((Tile.TILE_WIDTH, Tile.TILE_HEIGHT))
        self.set_color(color)

    def set_color(self, color = None):
        """
        Sets the color for this tile and updates the rendered version

        :param color: tuple in the form (r, g, b)
        """
        if color is None:
            r = random.randrange(0, 255)
            g = random.randrange(0, 255)
            b = random.randrange(0, 255)
            color = (r, g, b)
        self.color = color
        self.background.fill(color)

    def set_text(self, string, coords=(1,1)):
        """
        Set the text for this tile. Refresh the display
        :param str:
        """
        print string
        label_font = pygame.font.SysFont(self.get_font(), 15)
        label = label_font.render(str(string), 1, self.get_text_color())
        self.background.blit(label, coords)


    def get_font(self):
        """
        Get the name of the font to use
        :return str:
        """
        if self.font is None:
            return Tile.DEFAULT_FONT
        return self.font

    def get_text_color(self):
        """
        Get the color for the font
        """
        return (0,0,0)


class TileContainer(pygame.sprite.LayeredUpdates):
    """
    Container for a list of tiles. Has a background which is rendered and
    a group which contains other sprites
    """
    def __init__(self, layout):
        super(TileContainer, self).__init__()
        self.tiles = pygame.sprite.Group()
        self.layout = layout

    def do_highlight(self):
        self.layout.do_highlight(self.tiles)



class BoxLayout():
    @staticmethod
    def do_highlight(self, tiles):
        print "box %d" % len(tiles)


class RowLayout():
    @staticmethod
    def do_highlight(self, tiles):
        print "row %d" % len(tiles)


class ColumnLayout():
    @staticmethod
    def do_highlight(self, tiles):
        print "column %d" % len(tiles)
