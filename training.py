from snake import move_snake
from snake import snake
from snake import get_valid_actions

from state import get_state

from agent import add_state
from agent import choose_action
from agent import choose_random_action
from agent import update_q_value
from agent import q_table

from reward import get_reward


MIN_EPSILON = 0.05
NEW_LENGTH_EPSILON = 1
EPSILON_DECAY = 0.9999
epsilon_by_length = {}


def get_training_epsilon(snake_length):
    #new lengths start with higher exploration
    if snake_length not in epsilon_by_length:
        epsilon_by_length[snake_length] = NEW_LENGTH_EPSILON

    return epsilon_by_length[snake_length]


def decay_training_epsilon(snake_length):
    epsilon_by_length[snake_length] = max(
        MIN_EPSILON,
        epsilon_by_length[snake_length] * EPSILON_DECAY
    )


def print_epsilons_by_length():
    for snake_length in sorted(epsilon_by_length):
        epsilon = epsilon_by_length[snake_length]
        print("Length:", snake_length, "| epsilon:", format(epsilon, ".3f"))


def print_step_info(agent_name, state, action, reward):
    print(agent_name + " agent:", action)
    print("State:", state)
    if state in q_table:
        print("Q values:", q_table[state])
    else:
        print("Q values: STATE NOT LEARNED")
    print("Action:", action)
    print("Reward:", reward)
    print("States learned:", len(q_table))
    print()


def training_transition(state, action, apples):
    alive, grow = move_snake(action, apples)
    reward = get_reward(alive, grow)

    if alive == False:
        update_q_value(state, action, reward, None, None)
    else:
        next_state = get_state(snake, apples)
        next_valid_actions = get_valid_actions()
        add_state(next_state)
        update_q_value(
            state,
            action,
            reward,
            next_state,
            next_valid_actions
        )

    return alive, reward


def fast_training(alive, apples, episodes, reset_game_state):
    episode_steps = 0
    max_steps = 1000

    while episodes < 100000:
        truncated = episode_steps >= max_steps

        if alive == False:# or truncated == True:
            episodes = episodes + 1
            episode_steps = 0

            alive, apples = reset_game_state()

            if episodes % 100 == 0:
                print("Episodes:", episodes)
                print_epsilons_by_length()
                print("States learned:", len(q_table))
                print()
            continue

        state = get_state(snake, apples)
        valid_actions = get_valid_actions()
        add_state(state)

        training_length = len(snake)
        epsilon = get_training_epsilon(training_length)
        action = choose_action(state, epsilon, valid_actions)

        alive, reward = training_transition(state, action, apples)
        decay_training_epsilon(training_length)
        episode_steps = episode_steps + 1

    return alive, episodes


def run_sessions(
    session_count,
    episodes,
    reset_game_state,
    learn=True,
    visual=False,
    step_by_step=False,
    draw_current_state=None,
    wait_for_visual_step=None
):
    max_length = 0
    max_duration = 0

    for _ in range(session_count):
        alive, apples = reset_game_state()
        session_duration = 0
        session_max_length = len(snake)

        if visual:
            draw_current_state()

        while alive:
            if visual:
                wait_for_visual_step(step_by_step)

            state = get_state(snake, apples)
            valid_actions = get_valid_actions()

            if learn:
                add_state(state)
                training_length = len(snake)
                epsilon = get_training_epsilon(training_length)
                action = choose_action(state, epsilon, valid_actions)
                alive, reward = training_transition(state, action, apples)
                decay_training_epsilon(training_length)
            else:
                if state in q_table:
                    action = choose_action(state, 0.0, valid_actions)
                else:
                    action = choose_random_action(valid_actions)
                alive, grow = move_snake(action, apples)
                reward = get_reward(alive, grow)

            if visual:
                if learn:
                    agent_name = "Training"
                else:
                    agent_name = "Real"
                print_step_info(agent_name, state, action, reward)

            session_duration = session_duration + 1
            session_max_length = max(session_max_length, len(snake))

            if visual:
                draw_current_state(dead=not alive)

        if learn:
            episodes = episodes + 1

        max_length = max(max_length, session_max_length)
        max_duration = max(max_duration, session_duration)

    metrics = {
        "max_length": max_length,
        "max_duration": max_duration
    }
    return metrics, episodes, alive
