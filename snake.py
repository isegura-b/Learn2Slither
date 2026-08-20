from apple import apple_eaten

snake = [
    [5, 5],
    [5, 4],
    [5, 3]
]

direction = "Right"
def move_snake(new_direction, apples):

    global direction
    if direction == "Right" and new_direction == "Left":
        return True
    if direction == "Left" and new_direction == "Right":
        return True
    if direction == "Up" and new_direction == "Down":
        return True
    if direction == "Down" and new_direction == "Up":
        return True

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
        return False

    for i in range(1, len(snake)):

        if (
            new_head[0] == snake[i][0]
            and new_head[1] == snake[i][1]
        ):
            print("Game Over: body")
            return False

    grow = apple_eaten(new_head, apples)
    snake.insert(0, new_head)
    if grow == 0:
        snake.pop()
    elif grow == -1:
        snake.pop()
        if len(snake) > 0:
            snake.pop()
        if len(snake) == 0:
            print("Game Over: length 0")
            return False
    elif grow == 1:
        pass

    return True

def reset_snake():
    global direction

    snake.clear()

    snake.append([5, 5])
    snake.append([5, 4])
    snake.append([5, 3])
    snake.append([5, 2])

    direction = "Right"