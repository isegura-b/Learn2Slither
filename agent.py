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

def choose_random_action():

    actions = [
        "Up",
        "Down",
        "Left",
        "Right"
    ]
    action = random.choice(actions)
    return action

def choose_best_action(state):
    q_values = get_q_values(state)
    best_value = max(q_values.values())
    best_actions = []

    for action in q_values:
        if q_values[action] == best_value:
            best_actions.append(action)
    action = random.choice(best_actions)
    return action

alpha = 0.1
gamma = 0.9

def update_q_value(state, action, reward, next_state):

    old_q = q_table[state][action]

    if next_state == None:
        best_next_q = 0
    else:
        next_q_values = get_q_values(next_state)
        best_next_q = max(next_q_values.values())

    new_q = old_q + alpha * ( reward + gamma * best_next_q - old_q)
    q_table[state][action] = new_q

def choose_action(state, epsilon):

    random_number = random.random()

    if random_number < epsilon:
        action = choose_random_action()
    else:
        action = choose_best_action(state)

    return action