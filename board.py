DEFAULT_WIDTH = 10
DEFAULT_HEIGHT = 10
MIN_BOARD_SIDE = 3

width = DEFAULT_WIDTH
height = DEFAULT_HEIGHT


def configure(new_width, new_height):
    """Configure the playable area (the surrounding walls are not included)."""
    global width
    global height

    width = new_width
    height = new_height


def is_wall(row, col):
    return row == 0 or row == height + 1 or col == 0 or col == width + 1


def is_inside(row, col):
    return 1 <= row <= height and 1 <= col <= width
