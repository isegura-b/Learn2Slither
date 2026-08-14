snake = [
    [5, 5],
    [5, 4],
    [5, 3]
]

direction = "Right"
def move_snake(new_direction):

    global direction

    if direction == "Right" and new_direction == "Left":
        return
    if direction == "Left" and new_direction == "Right":
        return
    if direction == "Up" and new_direction == "Down":
        return
    if direction == "Down" and new_direction == "Up":
        return

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
    ) :
        print("GameOver")
        return (False)

    snake.insert(0, new_head)
    snake.pop()

def reset_snake():
    global direction

    snake.clear()

    snake.append([5, 5])
    snake.append([5, 4])
    snake.append([5, 3])

    direction = "Right"