def get_state(snake, apples):

    head = snake[0]

    row = head[0]
    col = head[1]

    up = look_up(row, col, snake, apples)
    down = look_down(row, col, snake, apples)
    left = look_left(row, col, snake, apples)
    right = look_right(row, col, snake, apples)

    state = (
        tuple(up),
        tuple(down),
        tuple(left),
        tuple(right)
    )
    return state

def get_cell_content(row, col, snake, apples):

    for i in range(1, len(snake)):

        if ( row == snake[i][0] and col == snake[i][1] ):
            return "S"

    for i in range(len(apples)):
        apple_position = apples[i][0]
        apple_type = apples[i][1]

        if ( row == apple_position[0] and col == apple_position[1]):
            if apple_type == "green":
                return "G"
            elif apple_type == "red":
                return "R"

    if row == 0 or row == 11 or col == 0 or col == 11:
        return "W"
    return "0"

def look_up(row, col, snake, apples):
    up = row - 1
    look = []
    while (up >= 0):
        look.append(get_cell_content(up, col, snake, apples))
        up = up - 1
    return look

def look_down(row, col, snake, apples):
    down = row + 1
    look = []
    while (down <= 11):
        look.append(get_cell_content(down, col, snake, apples))
        down = down + 1
    return look

def look_left(row, col, snake, apples):
    left = col - 1
    look = []
    while (left >= 0):
        look.append(get_cell_content(row, left, snake, apples))
        left = left - 1
    return look


def look_right(row, col, snake, apples):
    right = col + 1
    look = []
    while (right <= 11):
        look.append(get_cell_content(row, right, snake, apples))
        right = right + 1
    return look