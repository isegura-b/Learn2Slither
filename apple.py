import random

def create_apple(apple_type):

    row = random.randint(1, 10)
    col = random.randint(1, 10)

    apple = [[row, col], apple_type]

    return apple

def apple_eaten(head, apples):

    for i in range(len(apples)):
        apple_position = apples[i][0]
        apple_type = apples[i][1]
        if (head[0] == apple_position[0] and head[1] == apple_position[1]):

            apples.pop(i)
            apples.append(create_apple(apple_type))

            if apple_type == "green":
                return 1

            if apple_type == "red":
                return -1

    return 0