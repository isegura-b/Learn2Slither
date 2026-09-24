import board


def get_vision(snake, apples):
    head = snake[0]
    row = head[0]
    col = head[1]

    return (
        look_up(row, col, snake, apples),
        look_down(row, col, snake, apples),
        look_left(row, col, snake, apples),
        look_right(row, col, snake, apples)
    )


def format_vision(vision):
    up, down, left, right = vision
    head_indent = "  " * len(left)
    rows = []

    for content in reversed(up):
        rows.append(head_indent + content)

    horizontal_ray = list(reversed(left)) + ["H"] + right
    rows.append(" ".join(horizontal_ray))

    for content in down:
        rows.append(head_indent + content)

    return "\n".join(rows)


def get_state(snake, apples):
    up, down, left, right = get_vision(snake, apples)

    up_distances = get_direction_distances(up)
    down_distances = get_direction_distances(down)
    left_distances = get_direction_distances(left)
    right_distances = get_direction_distances(right)

    state = (
        categorize_direction(up_distances),
        categorize_direction(down_distances),
        categorize_direction(left_distances),
        categorize_direction(right_distances)
    )
    return state


def categorize_distance(distance):

    # 0 not visible, 1 adjacent, 2 near, 3 far
    if distance == 0:
        return 0
    if distance == 1:
        return 1
    if distance <= 3:
        return 2
    return 3


def categorize_direction(distances):

    return (
        categorize_distance(distances[0]),
        categorize_distance(distances[1]),
        categorize_distance(distances[2]),
        categorize_distance(distances[3])
    )


def get_direction_distances(vision):

    # 0 means object not visible in this ray
    green_distance = 0
    red_distance = 0
    body_distance = 0
    wall_distance = 0

    for i in range(len(vision)):
        content = vision[i]
        # exact distance from head
        distance = i + 1

        if content == "G" and green_distance == 0:
            green_distance = distance
        elif content == "R" and red_distance == 0:
            red_distance = distance
        elif content == "S" and body_distance == 0:
            body_distance = distance
        elif content == "W" and wall_distance == 0:
            wall_distance = distance

    direction_distances = (
        green_distance,
        red_distance,
        body_distance,
        wall_distance
    )
    return direction_distances


def get_cell_content(row, col, snake, apples):

    for i in range(1, len(snake)):

        if row == snake[i][0] and col == snake[i][1]:
            return "S"

    for i in range(len(apples)):
        apple_position = apples[i][0]
        apple_type = apples[i][1]

        if row == apple_position[0] and col == apple_position[1]:
            if apple_type == "green":
                return "G"
            elif apple_type == "red":
                return "R"

    if board.is_wall(row, col):
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
    while (down <= board.height + 1):
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
    while (right <= board.width + 1):
        look.append(get_cell_content(row, right, snake, apples))
        right = right + 1
    return look
