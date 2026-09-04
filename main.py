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

epsilon = 1.0
MIN_EPSILON = 0.05
EPSILON_DECAY = 0.995
episodes = 0


apples = []
apples.append(create_apple("green", snake, apples))
apples.append(create_apple("green", snake, apples))
apples.append(create_apple("red", snake, apples))


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


# -------------------------
# MANUAL - 1
# -------------------------

def key_pressed(event):

    global alive
    global auto_mode
    global real_mode

    if event.keysym == "Escape":
        window.destroy()
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
        print("MODE 4: REAL EVALUATION (epsilon = 0, learning disabled)")
        return

    if event.keysym == "r" or event.keysym == "R":
        restart_game()
        return

    if alive == False:
        print("GAME OVER: press R to restart or select another mode")
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

    valid_actions = get_valid_actions()
    if action not in valid_actions:
        print("Invalid action: opposite direction ignored")
        return

    # State BEFORE movement
    state = get_state(snake, apples)
    add_state(state)

    alive, grow = move_snake(action, apples)

    # Reward
    reward = get_reward(alive, grow, len(snake))

    # Next state and Bellman update
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

    print("Keyboard:", action)
    print("Reward:", reward)
    print("States learned:", len(q_table))
    print()

    # Draw
    draw_snake()
    draw_apples(apples)

    if alive == False:
        draw_rip_snake()


# -------------------------
# AUTO - 2      RealMode - 4
# -------------------------

def training_step():

    global alive
    global apples
    global auto_mode
    global real_mode
    global epsilon
    global episodes


    if auto_mode == False:
        window.after(100, training_step)
        return

    if alive == False:
        if real_mode == False:
            episodes = episodes + 1
            epsilon = max(MIN_EPSILON, epsilon * EPSILON_DECAY)
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
            action = choose_action(state, 0.0, valid_actions)
        else:
            action = choose_random_action(valid_actions)
    else:
        action = choose_action(state, epsilon, valid_actions)

    # Move
    alive, grow = move_snake(action, apples)

    # Reward
    reward = get_reward(alive, grow, len(snake))

    # Bellman update only while training
    if real_mode == False:
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

    if alive == False:
        draw_rip_snake()

    window.after(100, training_step)


# -------------------------
# FAST TRAIN - 3
# -------------------------

def fast_training():

    global alive
    global apples
    global epsilon

    episodes = 0
    episode_steps = 0
    max_steps = 1000

    while episodes < 100000:

        if alive == False or episode_steps >= max_steps:
            episodes = episodes + 1
            epsilon = max(MIN_EPSILON, epsilon * EPSILON_DECAY)
            episode_steps = 0
            reset_snake()

            alive = True

            apples = []
            apples.append(create_apple("green", snake, apples))
            apples.append(create_apple("green", snake, apples))
            apples.append(create_apple("red", snake, apples))

            if episodes % 100 == 0:
                print("Episodes:", episodes)
                print("Epsilon:", epsilon)
                print("States learned:", len(q_table))
                print()
            continue

        # State BEFORE movement
        state = get_state(snake, apples)
        valid_actions = get_valid_actions()
        add_state(state)

        # Agent chooses action
        action = choose_action(state, epsilon, valid_actions)

        # Move
        alive, grow = move_snake(action, apples)
        episode_steps = episode_steps + 1

        # Reward
        reward = get_reward(alive, grow, len(snake))

        # Next state
        if alive == False:
            update_q_value(state, action, reward, None, None)
        else:
            next_state = get_state(snake, apples)
            next_valid_actions = get_valid_actions()
            add_state(next_state)

            # Bellman
            update_q_value(
                state,
                action,
                reward,
                next_state,
                next_valid_actions
            )

draw_wall()
draw_board()
draw_snake()
draw_apples(apples)


window.bind("<Key>", key_pressed)
training_step()

window.mainloop()
