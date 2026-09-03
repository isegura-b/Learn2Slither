GREEN_REWARD = 100
RED_REWARD = -10
MOVE_REWARD = -1
DEATH_REWARD = -100


def get_reward(alive, grow, snake_length):

    if alive == False:
        return -100
    if snake_length < 10:
        if grow == 1:
            return 100
        if grow == -1:
            return -50
    else:
        if grow == 1:
            return -10
        if grow == -1:
            return 30

    return -1