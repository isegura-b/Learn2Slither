from snake import move_snake
from snake import reset_snake
from snake import snake
from snake import get_valid_actions

from apple import create_apple

from display import window
from display import draw_board
from display import draw_snake
from display import draw_wall
from display import draw_rip_snake
from display import draw_apples

from display_snake_view import create_snake_view
from display_snake_view import update_snake_view

from state import get_state

from agent import add_state
from agent import choose_action
from agent import choose_random_action
from agent import update_q_value
from agent import q_table

from reward import get_reward


alive = True
auto_mode = False
real_mode = False
paused = False

MIN_EPSILON = 0.05
NEW_LENGTH_EPSILON = 1
EPSILON_DECAY = 0.9999
epsilon_by_length = {}

RED_TEXT = "\033[91m"
RESET_TEXT = "\033[0m"

episodes = 0

apples = []
apples.append(create_apple("green", snake, apples))
apples.append(create_apple("green", snake, apples))
apples.append(create_apple("red", snake, apples))


def get_training_epsilon(snake_length):
    #new lengths start with higher exploration
    if snake_length not in epsilon_by_length:
        epsilon_by_length[snake_length] = NEW_LENGTH_EPSILON

    return epsilon_by_length[snake_length]


def decay_training_epsilon(snake_length):
    epsilon_by_length[snake_length] = max( MIN_EPSILON, epsilon_by_length[snake_length] * EPSILON_DECAY )


def print_epsilons_by_length():

    for snake_length in sorted(epsilon_by_length):
        epsilon = epsilon_by_length[snake_length]
        print("Length:", snake_length, "| epsilon:", format(epsilon, ".3f"))


def print_game_over(message="GAME OVER"):
    print(RED_TEXT + message + RESET_TEXT)


def restart_game():

    global alive
    global apples

    reset_snake()
    alive = True
    apples = []

    apples.append(create_apple("green", snake, apples))
    apples.append(create_apple("green", snake, apples))
    apples.append(create_apple("red", snake, apples))

    draw_snake()
    draw_apples(apples)
    update_snake_view(snake, apples)


def training_transition(state, action):

    global alive

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

    return reward


# -------------------------
# MANUAL - 1
# -------------------------

def key_pressed(event):

    global alive
    global auto_mode
    global real_mode
    global paused

    if event.keysym == "Escape":
        window.destroy()
        return

    if event.keysym == "space":
        paused = not paused
        if paused == True:
            print("PAUSED")
        else:
            print("PLAYING")
        return

    if event.keysym == "1":
        auto_mode = False
        real_mode = False
        print("MODE 1: MANUAL")
        return

    if event.keysym == "2":
        auto_mode = True
        real_mode = False
        print("MODE 2: AUTO TRAINING")
        return

    if event.keysym == "3":
        auto_mode = False
        real_mode = False
        print("MODE 3: FAST TRAINING")
        fast_training()
        print("FAST TRAINING FINISHED")
        return

    if event.keysym == "4":
        auto_mode = True
        real_mode = True
        restart_game()
        print("MODE 4: REAL EVALUATION (epsilon = 0, learning disabled)")
        return

    if event.keysym == "r" or event.keysym == "R":
        restart_game()
        return

    if paused == True:
        return

    if alive == False:
        print_game_over("GAME OVER: press R to restart or select another mode")
        return

    # Action
    if event.keysym == "Right":
        action = "Right"
    elif event.keysym == "Left":
        action = "Left"
    elif event.keysym == "Up":
        action = "Up"
    elif event.keysym == "Down":
        action = "Down"
    else:
        return

    alive, grow = move_snake(action, apples)

    # Reward
    reward = get_reward(alive, grow)

    print("Keyboard:", action)
    print("Reward:", reward)
    print("States learned:", len(q_table))
    print()

    # Draw
    draw_snake()
    draw_apples(apples)
    update_snake_view(snake, apples)

    if alive == False:
        print_game_over()
        draw_rip_snake()


# -------------------------
# AUTO - 2      RealMode - 4
# -------------------------

def training_step():

    global alive
    global apples
    global auto_mode
    global real_mode
    global episodes

    if paused == True:
        window.after(100, training_step)
        return

    if auto_mode == False:
        window.after(100, training_step)
        return

    if alive == False:
        if real_mode == False:
            episodes = episodes + 1
            if episodes % 100 == 0:
                print_epsilons_by_length()
        restart_game()
        window.after(100, training_step)
        return

    # State BEFORE movement
    state = get_state(snake, apples)
    valid_actions = get_valid_actions()
    if real_mode == False:
        add_state(state)

    # Agent chooses action
    if real_mode == True:
        if state in q_table:
            # NEW: REAL mode always uses epsilon 0
            action = choose_action(state, 0.0, valid_actions)
        else:
            action = choose_random_action(valid_actions)
    else:
        training_length = len(snake)
        epsilon = get_training_epsilon(training_length)
        action = choose_action(state, epsilon, valid_actions)

    if real_mode == True:
        alive, grow = move_snake(action, apples)
        reward = get_reward(alive, grow)
    else:
        reward = training_transition(state, action)
        decay_training_epsilon(training_length)

    if real_mode == True:
        print("Real agent:", action)
        print("State:", state)
        if state in q_table:
            print("Q values:", q_table[state])
        else:
            print("Q values: STATE NOT LEARNED")
        print("Action:", action)
    else:
        print("Training agent:", action)
    print("Reward:", reward)
    print("States learned:", len(q_table))
    print()

    # Draw
    draw_snake()
    draw_apples(apples)
    update_snake_view(snake, apples)

    if alive == False:
        print_game_over()
        draw_rip_snake()

    window.after(100, training_step)


# -------------------------
# FAST TRAIN - 3
# -------------------------

def fast_training():

    global alive
    global apples

    episodes = 0
    episode_steps = 0
    max_steps = 1000

    while episodes < 100000:
        truncated = episode_steps >= max_steps

        if alive == False:# or truncated == True:
            episodes = episodes + 1

            episode_steps = 0

            reset_snake()
            alive = True

            apples = []
            apples.append(create_apple("green", snake, apples))
            apples.append(create_apple("green", snake, apples))
            apples.append(create_apple("red", snake, apples))

            if episodes % 100 == 0:
                print("Episodes:", episodes)
                print_epsilons_by_length()
                print("States learned:", len(q_table))
                print()
            continue

        # State BEFORE movement
        state = get_state(snake, apples)
        valid_actions = get_valid_actions()
        add_state(state)

        # Agent chooses action
        training_length = len(snake)
        epsilon = get_training_epsilon(training_length)
        action = choose_action(state, epsilon, valid_actions)

        training_transition(state, action)
        decay_training_epsilon(training_length)
        episode_steps = episode_steps + 1

draw_wall()
draw_board()
draw_snake()
draw_apples(apples)
create_snake_view(window)
update_snake_view(snake, apples)


window.bind("<Key>", key_pressed)
training_step()

window.mainloop()
