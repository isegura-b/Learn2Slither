import random
import board


def create_apple(apple_type, snake, apples):
    occupied = {tuple(segment) for segment in snake}
    occupied.update(tuple(apple[0]) for apple in apples)
    free_cells = [
        [row, col]
        for row in range(1, board.height + 1)
        for col in range(1, board.width + 1)
        if (row, col) not in occupied
    ]

    if len(free_cells) == 0:
        return None

    return [random.choice(free_cells), apple_type]

def apple_eaten(head, apples, snake):

    for i in range(len(apples)):
        apple_position = apples[i][0]
        apple_type = apples[i][1]
        if (head[0] == apple_position[0] and head[1] == apple_position[1]):

            apples.pop(i)
            replacement = create_apple(apple_type, snake, apples)
            if replacement is not None:
                apples.append(replacement)

            if apple_type == "green":
                return 1

            if apple_type == "red":
                return -1

    return 0
