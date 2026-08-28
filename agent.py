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

