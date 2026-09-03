from apple import apple_eaten

snake = [
    [5, 5],
    [5, 4],
    [5, 3]
]

direction = "Right"

def is_opposite_direction(new_direction):
    if direction == "Right" and new_direction == "Left":
        return True
    if direction == "Left" and new_direction == "Right":
        return True
    if direction == "Up" and new_direction == "Down":
        return True
    if direction == "Down" and new_direction == "Up":
        return True
    return False

def move_snake(new_direction, apples):

    global direction
    if len(snake) > 1 and is_opposite_direction(new_direction):
        return (True, 0)

    direction = new_direction
    head = snake[0]
    row = head[0]
    col = head[1]

    new_row = row
    new_col = col

    if direction == "Right":
        new_col = col + 1
    elif direction == "Left":
        new_col = col - 1
    elif direction == "Up":
        new_row = row - 1
    elif direction == "Down":
        new_row = row + 1
    new_head = [new_row, new_col]

    if (
        new_head[0] <= 0
        or new_head[1] <= 0
        or new_head[0] >= 11
        or new_head[1] >= 11
    ):
        print("Game Over: wall")
        return (False, 0)

    for i in range(1, len(snake)):

        if (
            new_head[0] == snake[i][0]
            and new_head[1] == snake[i][1]
        ):
            print("Game Over: body")
            return (False, 0)

    grow = apple_eaten(new_head, apples, snake)
    snake.insert(0, new_head)
    if grow == 0:
        snake.pop()
    elif grow == -1:
        snake.pop()
        if len(snake) > 0:
            snake.pop()
        if len(snake) == 0:
            print("Game Over: length 0")
            return (False, -1)
    elif grow == 1:
        pass

    return (True, grow)

def reset_snake():
    global direction

    snake.clear()

    snake.append([5, 5])
    snake.append([5, 4])
    snake.append([5, 3])
    snake.append([5, 2])

    direction = "Right"
