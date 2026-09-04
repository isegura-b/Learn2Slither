def get_state(snake, apples):

    head = snake[0]

    row = head[0]
    col = head[1]

    up = look_up(row, col, snake, apples)
    down = look_down(row, col, snake, apples)
    left = look_left(row, col, snake, apples)
    right = look_right(row, col, snake, apples)

    state = (
        compact_direction(up),
        compact_direction(down),
        compact_direction(left),
        compact_direction(right)
    )
    return state


def categorize_distance(distance):

    # 0 
    if distance == 0:
        return 0

    # Next
    if distance == 1:
        return 1

    # Close
    if distance <= 3:
        return 2

    # Far
    return 3


def compact_direction(vision):


    green_distance = 0
    red_distance = 0
    body_distance = 0
    wall_distance = 0

    for i in range(len(vision)):
        content = vision[i]
        distance = i + 1

        if content == "G" and green_distance == 0:
            green_distance = distance
        elif content == "R" and red_distance == 0:
            red_distance = distance
        elif content == "S" and body_distance == 0:
            body_distance = distance
        elif content == "W" and wall_distance == 0:
            wall_distance = distance

    immediate_danger = False
    if len(vision) > 0:
        if vision[0] == "W" or vision[0] == "S":
            immediate_danger = True

    compact_vision = (
        immediate_danger,
        categorize_distance(green_distance),
        categorize_distance(red_distance),
        categorize_distance(body_distance),
        categorize_distance(wall_distance)
    )
    return compact_vision

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
