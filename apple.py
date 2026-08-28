import random

def create_apple(apple_type, snake, apples):

    while True:
        row = random.randint(1, 10)
        col = random.randint(1, 10)
        occupied = False

        for i in range(len(snake)):
            if ( row == snake[i][0] and col == snake[i][1] ):
                occupied = True

        for i in range(len(apples)):
            apple_position = apples[i][0]
            if ( row == apple_position[0] and col == apple_position[1] ):
                occupied = True
        if occupied == False:
            break

    apple = [[row, col], apple_type]
    return apple

def apple_eaten(head, apples, snake):

    for i in range(len(apples)):
        apple_position = apples[i][0]
        apple_type = apples[i][1]
        if (head[0] == apple_position[0] and head[1] == apple_position[1]):

            apples.pop(i)
            apples.append(create_apple(apple_type, snake, apples))

            if apple_type == "green":
                return 1

            if apple_type == "red":
                return -1

    return 0