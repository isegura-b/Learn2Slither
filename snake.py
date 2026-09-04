from apple import apple_eaten
import random

snake = []
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

def get_valid_actions():

    actions = [
        "Up",
        "Down",
        "Left",
        "Right"
    ]

    valid_actions = []

    for action in actions:
        if is_opposite_direction(action) == False:
            valid_actions.append(action)

    return valid_actions

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
        new_head[0] <= 0
        or new_head[1] <= 0
        or new_head[0] >= 11
        or new_head[1] >= 11
    ):
        print("Game Over: wall")
        return (False, 0)

    for i in range(1, len(snake) - 1):
        if ( new_head[0] == snake[i][0] and new_head[1] == snake[i][1] ):
            print("Game Over: body")
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
            print("Game Over: length 0")
            return (False, -1)
    elif grow == 1:
        pass

    return (True, grow)

def reset_snake():

    global direction
    snake.clear()
    while True:
        row = random.randint(1, 10)
        col = random.randint(1, 10)
        directions = [
            "Right",
            "Left",
            "Up",
            "Down"
        ]

        direction = random.choice(directions)
        if direction == "Right":
            head = [row, col]
            body1 = [row, col - 1]
            body2 = [row, col - 2]
        elif direction == "Left":
            head = [row, col]
            body1 = [row, col + 1]
            body2 = [row, col + 2]
        elif direction == "Up":
            head = [row, col]
            body1 = [row + 1, col]
            body2 = [row + 2, col]
        elif direction == "Down":
            head = [row, col]
            body1 = [row - 1, col]
            body2 = [row - 2, col]

        valid = True


        if ( body1[0] < 1 or body1[0] > 10 or body1[1] < 1 or body1[1] > 10 ):
            valid = False

        if ( body2[0] < 1 or body2[0] > 10 or body2[1] < 1 or body2[1] > 10 ):
            valid = False

        if valid == True:
            snake.append(head)
            snake.append(body1)
            snake.append(body2)

            break

reset_snake()
