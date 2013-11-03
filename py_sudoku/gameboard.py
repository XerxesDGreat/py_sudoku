__author__ = 'josh'

import pygame
import colors
import itertools

class Grid(object):
    """
    Class which handles the grid
    """

    # constants for various settings
    GRID_X_BOX_COUNT = 3
    GRID_Y_BOX_COUNT = 3
    BOX_X_TILE_COUNT = 3
    BOX_Y_TILE_COUNT = 3
    BOX_BORDER_WIDTH = 3
    BOX_BORDER_COLOR = colors.BLACK

    def __init__(self):
        """
        Constructor
        """
        self.boxes = []
        self.columns = []
        self.rows = []
        self._init_group_list(self.boxes, Grid.GRID_X_BOX_COUNT * Grid.GRID_Y_BOX_COUNT)
        self._init_group_list(self.columns, Grid.GRID_Y_BOX_COUNT * Grid.BOX_Y_TILE_COUNT)
        self._init_group_list(self.rows, Grid.GRID_X_BOX_COUNT * Grid.BOX_X_TILE_COUNT)
        self.tiles = TileContainer()
         # background is gonna get resized anyway, so don't worry about the size
        self.background = pygame.Surface((1,1)).convert()
        self.background.fill(colors.BLACK)

    @property
    def width(self):
        return self.get_rect().width

    @property
    def height(self):
        return self.get_rect().height

    def get_rect(self):
        """
        Get the rectangle which contains the surface
        :return Rectangle:
        """
        return self.background.get_rect()

    def create_grid(self, screen, puzzle_definition):
        """
        Create the grid
        """
        # create all the tiles we need
        tile_x_count = self._get_num_columns()
        tile_y_count = self._get_num_rows()

        tile_position = (0,0)
        max_size = (0,0)
        for i in range(tile_x_count * tile_y_count):
            # get the indexes for column, row, and box
            c_index, r_index, b_index = self._get_col_row_box(i)

            # we need a tile before anything else
            t = self._create_tile(i, puzzle_definition[i])

            # pop it into the total group of tiles
            self.tiles.add(t)

            # add it to the defined column, row, and box groups
            self.columns[c_index].add(t)
            self.rows[r_index].add(t)
            self.boxes[b_index].add(t)

            # secure the backreferences in the tile
            t.set_tile_groups(self.boxes[b_index], self.rows[r_index],
                              self.columns[c_index])

            # make sure the tiles are in their correct locations
            self._update_position(t, tile_position)

        # reposition the boxes
        for i in range(len(self.boxes)):
            x_offset = Grid.BOX_BORDER_WIDTH * (1 + (i % Grid.GRID_X_BOX_COUNT))
            y_offset = Grid.BOX_BORDER_WIDTH * (1 + (i / Grid.GRID_Y_BOX_COUNT))
            self.boxes[i].move((x_offset, y_offset))

        # the last added tile will be the bottom-right corner; fetch that
        # so we can resize the background
        max_tile = self.tiles.get_by_index(len(self.tiles) - 1)
        max_x, max_y = max_tile.rect.bottomright
        max_x += Grid.BOX_BORDER_WIDTH
        max_y += Grid.BOX_BORDER_WIDTH
        self.background = pygame.transform.scale(self.background, (max_x, max_y))

        self.tiles.draw(self.background)
        screen.blit(self.background, (0,0))

    def move_sel_in_direction(self, tile, direction):
        """
        Gets the Tile which one unit in the given direction from the provided
        tile
        :param tile: Tile which is the starting point
        :param direction: which direction to move
        :return Tile:
        """
        new_tile = tile
        row = tile.id / self._get_num_rows()
        column = tile.id % self._get_num_columns()

        if direction == pygame.K_RIGHT:
            if column < self._get_num_columns() - 1:
                new_tile = self.tiles.get_by_index(tile.id + 1)
        elif direction == pygame.K_LEFT:
            if column > 0:
                new_tile = self.tiles.get_by_index(tile.id - 1)
        elif direction == pygame.K_UP:
            if row > 0:
                new_tile = self.tiles.get_by_index(tile.id - self._get_num_columns())
        elif direction == pygame.K_DOWN:
            if row < self._get_num_rows() - 1:
                new_tile = self.tiles.get_by_index(tile.id + self._get_num_columns())

        return new_tile

    def is_complete(self):
        """
        Checks to see whether the entire grid is is_complete
        :return Boolean:
        """
        for tile_group in itertools.chain(self.boxes, self.rows, self.columns):
            if not tile_group.is_complete():
                return False
        return True

    def get_tile_at_pos(self, position):
        """
        Gets the Tile which is at the given position (in real-world coordinates)
        :param position: tuple of real-world coordinates (x, y)
        :return Tile:
        """
        x_coord, y_coord = position
        column = x_coord / Tile.TILE_WIDTH
        row = y_coord / Tile.TILE_HEIGHT
        index = (row * self._get_num_rows()) + column
        return self.tiles.get_by_index(index)

    def _init_group_list(self, group_list, count):
        """
        Makes the given group list ready to receive tiles
        """
        for i in range(count):
            group_list.append(TileContainer())

    def _get_col_row_box(self, tile_index):
        """
        Returns the column, row, and box index for the given tile index
        :param tile_index: index for the tile
        :return int:
        """
        grid_width = Grid.BOX_X_TILE_COUNT * Grid.GRID_X_BOX_COUNT
        col = tile_index % grid_width
        row = tile_index / grid_width
        box_x = col / Grid.GRID_X_BOX_COUNT
        box_y = row / Grid.GRID_Y_BOX_COUNT
        box = box_x + (box_y * Grid.GRID_X_BOX_COUNT)

        return col, row, box

    def _update_position(self, tile, position):
        x, y = position
        x = tile.id % (Grid.BOX_X_TILE_COUNT * Grid.GRID_X_BOX_COUNT)
        y = tile.id / (Grid.BOX_Y_TILE_COUNT * Grid.GRID_Y_BOX_COUNT)
        tile.move_to((x, y))

    def _create_tile(self, id, puzzle_value):
        """
        Return an individual tile

        :param color: A tuple describing the color of the tile
        :return Surface:
        """
        t = Tile(id, puzzle_value)
        return t

    def _get_num_rows(self):
        return Grid.BOX_Y_TILE_COUNT * Grid.GRID_Y_BOX_COUNT

    def _get_num_columns(self):
        return Grid.BOX_X_TILE_COUNT * Grid.GRID_X_BOX_COUNT

    def _get_num_boxes(self):
        return Grid.GRID_X_BOX_COUNT * Grid.GRID_Y_BOX_COUNT


class TileContainer(object):
    def __init__(self, *sprites):
        """
        constructor
        :param *sprites: list, group, or single sprite
        """
        self.group = pygame.sprite.Group()
        self.tile_list = []
        self.complete = False
        self.complete_flags = [False for i in range(9)]
        for sprite in sprites:
            self.group.add(sprite)
            self.tile_list.append(sprite)

    def __getattr__(self, name):
        """
        Allows all methods, except for the ones specified here, to go through
        to the underlying group
        :param name: name of the attribute to get
        :return function:
        """
        return getattr(self.group, name)

    def __add__(self, other):
        """
        How to handle adding an instance of TileContainer to something else
        using the addition operator.
        :param other: the item which we're adding to this instance
        """
        if type(other) != TileContainer:
            raise TypeError("Cannot add object of type %s to object of type TileContainer" % type(other))

        both = []
        for list in [self.tile_list, other.tile_list]:
            for tile in list:
                both.append(tile)
        return TileContainer(both)

    def add(self, *sprites):
        """
        Adds a sprite, group of sprites, or list of sprites to this container
        and to the underlying group
        :param *sprites: list, group, or single sprite
        """
        self.group.add(sprites)
        for sprite in sprites:
            self.tile_list.append(sprite)

    def move(self, distance):
        """
        Moves all sprites in this group by distance
        :param distance: tuple of (width, height)
        """
        for tile in self.group:
            tile.move_relative(distance, False)

    def get_by_index(self, index):
        """
        Fetches a single sprite by its index in the list
        :param index: int the sprite's index
        :return Sprite:
        """
        return self.tile_list[index]

    def add_value(self, value):
        """
        Adds a value to the list of values which are represented in this group.
        Will not do any checking to see if this value is conflicted; therefore,
        perform that check before calling this function
        :param value: the new value (1-9) to add
        """
        self.complete_flags[value - 1] = True

    def remove_value(self, value):
        """
        Removes a value from the list of values which are represented in this
        group. Will not do any checking to see if this value is conflicted;
        therefore, perform that check before calling this function
        :param value: the new value (1-9) to remove
        """
        self.complete_flags[value - 1] = False

    def is_complete(self):
        """
        Determines whether this group is complete
        :return Boolean:
        """
        for flag in self.complete_flags:
            if not flag:
                return False

        return True

    def update_all(self, grid):
        """
        Updates all tiles in this group, checking for conflicts. Blits them onto
        the provided grid
        :param grid: Surface object
        """
        for tile in self.group:
            tile.update()
        self.group.draw(grid.background)

    def __iter__(self):
        return self.group.__iter__()

    def __len__(self):
        return len(self.tile_list)


class Tile(pygame.sprite.DirtySprite):
    TILE_WIDTH = 80
    TILE_HEIGHT = 80
    TILE_SIZE = TILE_WIDTH, TILE_HEIGHT

    background = None
    yellow_tint = None
    light_grey_tint = None

    DEFAULT_FONT = "Courier New Regular"
    BOLD_FONT = "Courier New Bold"

    def __init__(self, id, init_value = None, *args, **kwargs):
        """
        Constructor for this object; builds the Surface as well
        """
        super(Tile, self).__init__()
        self.id = id
        self.box = None
        self.row = None
        self.column = None

        self.group_completed = False
        self.selected = False
        self.group_selected = False

        self._divisions = None
        self.value = init_value
        self.immutable = False
        self._conflicted = False
        self.dirty = 1
        self.tint_surface = None

        self._set_up_prototypes()
        img = Tile.background.subsurface(Tile.background.get_rect())
        self.image = img.convert()
        self.rect = self.image.get_rect()

        if self.value is not None:
            self.immutable = True


    def set_tile_groups(self, box, row, column):
        """
        adds the various groups this tile is in
        :param box: TileContainer
        :param row: TileContainer
        :param column: TileContainer
        """
        self.box = box
        self.row = row
        self.column = column

        if self.value is not None:
            self.row.add_value(self.value)
            self.box.add_value(self.value)
            self.column.add_value(self.value)

    @property
    def divisions(self):
        if self._divisions is None:
            self._divisions = self.box + self.row + self.column
        return self._divisions

    @property
    def conflicted(self):
        return self._conflicted

    @conflicted.setter
    def conflicted(self, flag):
        if flag != self._conflicted:
            self.dirty = True
        self._conflicted = flag

    def move_relative(self, distance, use_tile_coords = True):
        """
        Moves this tile to another location relative to the current location.
        As an example, if this tile is at (2,2) and position is (1,1), the tile
        will end up at (3,3). Tile is anchored on the top-left corner of the rect
        :param distance: how far to move the tile
        :param use_tile_coords: if set to true, moves by number of tiles, not pixels
        """
        x, y = distance
        if use_tile_coords:
            x *= Tile.TILE_WIDTH
            y *= Tile.TILE_HEIGHT
        self.rect.left += x
        self.rect.top += y

    def move_to(self, position, use_tile_coords = True):
        """
        Moves this tile to another location. Tile is anchored on the topleft
        corner of the rect
        :param position: new location for the tile
        :param use_tile_coords: if set to true, moves by number of tiles, not pixels
        """
        x, y = position
        if use_tile_coords:
            x *= Tile.TILE_WIDTH
            y *= Tile.TILE_HEIGHT
        self.rect.left = x
        self.rect.top = y

    def set_value(self, value):
        """
        Set the value for this tile.
        """
        if self.immutable:
            return

        if self.value is not None:
            self.box.remove_value(self.value)
            self.column.remove_value(self.value)
            self.row.remove_value(self.value)

        self.value = value
        self.dirty = 1

        self._update_conflicts()

        if not self.conflicted and self.value is not None:
            self.box.add_value(self.value)
            self.column.add_value(self.value)
            self.row.add_value(self.value)

    def _update_conflicts(self):
        """
        Checks all other tiles in this tile's groups for conflicting values.
        Will perform resetting conflicted state of all tiles, suppressing the
        setting again of a conflict state if the value is None
        """
        has_conflicts = False
        for tile in self.divisions:
            if tile is self:
                continue
            if self.value is not None and tile.value == self.value:
                has_conflicts = True
                tile.conflicted = True
            else:
                tile.conflicted = False

        self.conflicted = has_conflicts


    def get_font(self, bold = False):
        """
        Get the name of the font to use
        :param bold: Whether the font should be bold
        :return str:
        """
        return Tile.BOLD_FONT if bold else Tile.DEFAULT_FONT

    def get_text_color(self):
        """
        Get the color for the font
        """
        return colors.BLACK

    def on_click(self):
        """
        Handler for mouse clicks on this tile
        """
        self.on_select()

    def on_select(self):
        """
        How to handle this tile being selected
        """
        self.selected = True
        for tile in self.divisions:
            if tile is not self:
                tile.group_selected = True

    def on_deselect(self):
        """
        How to handle this tile being deselected
        """
        for tile in self.divisions:
            tile.group_selected = False
            tile.selected = False

    def on_edit(self, key):
        """
        Performs some edit operation on this tile
        :param key: pygame constant for the value of the key
        """
        if key == pygame.K_BACKSPACE or key == pygame.K_DELETE:
            self.set_value(None)


    def _set_up_prototypes(self):
        if Tile.background is None:
            img = pygame.image.load("assets/tile.png").convert()
            Tile.background = pygame.transform.scale(img, Tile.TILE_SIZE)


    #
    #
    # Visual update methods
    #
    #
    def update(self):
        """
        Updates the display for this tile
        """
        if self.dirty < 1:
            # let's just try updating all of them
            pass
            #return
        self._update_background()
        self._update_text()
        self.dirty = 2 if self.dirty == 2 else 0

    def _update_background(self):
        """
        Updates the background imagery based on the tile's current state
        """
        self.image.blit(self.background, (0,0))

        alpha = 64
        color = None
        if self.conflicted:
            color = colors.RED
        elif self.selected:
            color = colors.YELLOW
            alpha = 128
        elif self.group_selected:
            color = colors.BLUE
        elif self.group_completed:
            color = colors.GREEN

        if color is not None:
            tint = pygame.Surface(Tile.TILE_SIZE)
            tint.set_alpha(alpha)
            tint.fill(color)
            self.image.blit(tint, (0,0))

    def _update_text(self, *args):
        """
        Updates the text display for this tile
        """
        if self.value is None:
            return
        bold = self.immutable or self.conflicted
        color = colors.MEDIUM_GREY if not self.immutable else colors.BLACK
        color = color if not self.conflicted else colors.RED
        label_font = pygame.font.SysFont(self.get_font(bold), 32)
        label = label_font.render(str(self.value), 1, color)

        label_rect = label.get_rect()
        label_rect.centerx = Tile.TILE_WIDTH / 2
        label_rect.centery = Tile.TILE_HEIGHT / 2
        self.image.blit(label, label_rect)