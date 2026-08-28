q_table = {}

def add_state(state):
    if state not in q_table:
        q_table[state] = {
            "Up": 0.0,
            "Down": 0.0,
            "Left": 0.0,
            "Right": 0.0
        }