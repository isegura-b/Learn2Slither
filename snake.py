from apple import apple_eaten
import random

import board

snake = []
direction = "Right"

ACTIONS = [
    "Up",
    "Down",
    "Left",
    "Right"
]

def get_valid_actions():
    return ACTIONS.copy()

def move_snake(new_direction, apples):

    global direction

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
        not board.is_inside(new_head[0], new_head[1])
    ):
        #print("Game Over: wall")
        return (False, 0)

    # Moving into the last tail cell is safe only when that cell is going to
    # disappear during this tick. A green apple prevents the tail from moving.
    tail_will_move = True
    for apple in apples:
        apple_position = apple[0]
        apple_type = apple[1]
        if new_head == apple_position and apple_type == "green":
            tail_will_move = False

    body_end = len(snake)
    if tail_will_move == True:
        body_end = len(snake) - 1

    for i in range(1, body_end):
        if ( new_head[0] == snake[i][0] and new_head[1] == snake[i][1] ):
            #print("Game Over: body")
            return (False, 0)

    snake.insert(0, new_head)
    grow = apple_eaten(new_head, apples, snake)
    if grow == 0:
        snake.pop()
    elif grow == -1:
        snake.pop()
        if len(snake) > 0:
            snake.pop()
        if len(snake) == 0:
            #print("Game Over: length 0")
            return (False, -1)
    elif grow == 1:
        pass

    return (True, grow)

def reset_snake():

    global direction
    snake.clear()

    initial_length = min(3, max(board.width, board.height))
    while True:
        row = random.randint(1, board.height)
        col = random.randint(1, board.width)
        directions = [
            "Right",
            "Left",
            "Up",
            "Down"
        ]

        direction = random.choice(directions)
        if direction == "Right":
            head = [row, col]
            body = [[row, col - offset] for offset in range(1, initial_length)]
        elif direction == "Left":
            head = [row, col]
            body = [[row, col + offset] for offset in range(1, initial_length)]
        elif direction == "Up":
            head = [row, col]
            body = [[row + offset, col] for offset in range(1, initial_length)]
        elif direction == "Down":
            head = [row, col]
            body = [[row - offset, col] for offset in range(1, initial_length)]

        valid = all(board.is_inside(segment[0], segment[1]) for segment in body)

        if valid == True:
            snake.append(head)
            snake.extend(body)

            break

reset_snake()
