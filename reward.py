GREEN_REWARD = 1000
RED_REWARD = -200
MOVE_REWARD = -10
DEATH_REWARD = -500

def get_reward(alive, grow):

    if alive == False:
        return DEATH_REWARD

    if grow == 1:
        return GREEN_REWARD

    if grow == -1:
        return RED_REWARD

    return MOVE_REWARD
