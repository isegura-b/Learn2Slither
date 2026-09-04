import random

q_table = {}

def add_state(state):
    if state not in q_table:
        q_table[state] = {
            "Up": 0.0,
            "Down": 0.0,
            "Left": 0.0,
            "Right": 0.0
        }

def get_q_values(state):
    return q_table[state]

def choose_random_action(valid_actions):

    action = random.choice(valid_actions)
    return action

def choose_best_action(state, valid_actions):
    q_values = get_q_values(state)
    best_value = None
    best_actions = []

    for action in valid_actions:
        if best_value == None or q_values[action] > best_value:
            best_value = q_values[action]
            best_actions = [action]
        elif q_values[action] == best_value:
            best_actions.append(action)
    action = random.choice(best_actions)
    return action

alpha = 0.1
gamma = 0.9

def update_q_value(state, action, reward, next_state, next_valid_actions):

    old_q = q_table[state][action]

    if next_state == None:
        best_next_q = 0
    else:
        next_q_values = get_q_values(next_state)
        best_next_q = None

        for next_action in next_valid_actions:
            next_q = next_q_values[next_action]

            if best_next_q == None or next_q > best_next_q:
                best_next_q = next_q

    new_q = old_q + alpha * ( reward + gamma * best_next_q - old_q)
    q_table[state][action] = new_q

def choose_action(state, epsilon, valid_actions):

    random_number = random.random()

    if random_number < epsilon:
        action = choose_random_action(valid_actions)
    else:
        action = choose_best_action(state, valid_actions)

    return action
