from snake import move_snake
from snake import reset_snake
from snake import snake

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
from agent import update_q_value
from agent import q_table

from reward import get_reward


alive = True
auto_mode = False

epsilon = 1.0
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
# MANUAL
# -------------------------

def key_pressed(event):

    global alive
    global auto_mode

    if event.keysym == "Escape":
        window.destroy()
        return

    if event.keysym == "space":
        if auto_mode == False:
            auto_mode = True
            print("AUTO MODE")
        else:
            auto_mode = False
            print("MANUAL MODE")
        return

    if event.keysym == "f" or event.keysym == "F":
        print("FAST TRAINING")
        fast_training()
        print("FAST TRAINING FINISHED")
        return

    if event.keysym == "r" or event.keysym == "R":
        restart_game()
        return

    # State BEFORE movement
    state = get_state(snake, apples)
    add_state(state)

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
    reward = get_reward(alive, grow, len(snake))

    # Next state
    next_state = get_state(snake, apples)
    add_state(next_state)

    # Bellman
    update_q_value(state, action, reward, next_state)

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
# AUTO
# -------------------------

def training_step():

    global alive
    global apples
    global auto_mode
    global epsilon
    global episodes


    if auto_mode == False:
        window.after(100, training_step)
        return

    if alive == False:
        episodes = episodes + 1
        restart_game()
        window.after(100, training_step)
        return

    # State BEFORE movement
    state = get_state(snake, apples)
    add_state(state)

    # Agent chooses action
    action = choose_action(state, epsilon)

    # Move
    alive, grow = move_snake(action, apples)

    # Reward
    reward = get_reward(alive, grow, len(snake))

    # Next state
    next_state = get_state(snake, apples)
    add_state(next_state)

    # Bellman
    update_q_value(state, action, reward, next_state)

    print("Agent:", action)
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
# FAST TRAIN
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
            episode_steps = 0
            reset_snake()

            alive = True

            apples = []
            apples.append(create_apple("green", snake, apples))
            apples.append(create_apple("green", snake, apples))
            apples.append(create_apple("red", snake, apples))

            if episodes % 100 == 0:
                epsilon = epsilon - 0.1
                if epsilon < 0:
                    epsilon = 0
                print("Episodes:", episodes)
                print("Epsilon:", epsilon)
                print("States learned:", len(q_table))
                print()
            continue

        # State BEFORE movement
        state = get_state(snake, apples)
        add_state(state)

        # Agent chooses action
        action = choose_action(state, epsilon)

        # Move
        alive, grow = move_snake(action, apples)
        episode_steps = episode_steps + 1

        # Reward
        reward = get_reward(alive, grow, len(snake))

        # Next state
        if alive == False:
            update_q_value(state, action, reward, None)
        else:
            next_state = get_state(snake, apples)
            add_state(next_state)

            # Bellman
            update_q_value(state, action, reward, next_state)

draw_wall()
draw_board()
draw_snake()
draw_apples(apples)


window.bind("<Key>", key_pressed)
training_step()

window.mainloop()