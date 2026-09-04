GREEN_REWARD = 100
RED_REWARD = -50
MOVE_REWARD = -1
DEATH_REWARD = -100


def get_reward(alive, grow, len):

    if alive == False:
        return DEATH_REWARD

    if grow == 1:
        return GREEN_REWARD

    if grow == -1:
        return RED_REWARD

    return MOVE_REWARD