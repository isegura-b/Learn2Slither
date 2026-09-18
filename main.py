import sys

from arguments import build_parser

from snake import move_snake
from snake import reset_snake
from snake import snake
from snake import get_valid_actions

from apple import create_apple

from state import get_state

from agent import add_state
from agent import choose_action
from agent import choose_random_action
from agent import q_table
from agent import alpha as ALPHA
from agent import gamma as GAMMA

from reward import get_reward

from model import load_model
from model import save_model

from training import decay_training_epsilon
from training import epsilon_by_length
from training import fast_training
from training import get_training_epsilon
from training import print_epsilons_by_length
from training import print_step_info
from training import run_sessions
from training import training_transition


alive = True
auto_mode = False
real_mode = False
paused = False

RED_TEXT = "\033[91m"
RESET_TEXT = "\033[0m"

episodes = 0

window = None
draw_board = None
draw_snake = None
draw_wall = None
draw_rip_snake = None
draw_apples = None
create_snake_view = None
update_snake_view = None

apples = []
apples.append(create_apple("green", snake, apples))
apples.append(create_apple("green", snake, apples))
apples.append(create_apple("red", snake, apples))


def print_game_over(message="GAME OVER"):
    print(RED_TEXT + message + RESET_TEXT)


def load_training_model(model_path):
    global episodes

    metadata = load_model(model_path, q_table, epsilon_by_length)
    episodes = metadata["episodes"]
    return metadata


def initialize_display():
    global window
    global draw_board
    global draw_snake
    global draw_wall
    global draw_rip_snake
    global draw_apples
    global create_snake_view
    global update_snake_view

    import display
    import display_snake_view

    window = display.window
    draw_board = display.draw_board
    draw_snake = display.draw_snake
    draw_wall = display.draw_wall
    draw_rip_snake = display.draw_rip_snake
    draw_apples = display.draw_apples
    create_snake_view = display_snake_view.create_snake_view
    update_snake_view = display_snake_view.update_snake_view


def reset_game_state():
    global alive
    global apples

    reset_snake()
    alive = True
    apples = []
    apples.append(create_apple("green", snake, apples))
    apples.append(create_apple("green", snake, apples))
    apples.append(create_apple("red", snake, apples))
    return alive, apples


def restart_game():
    reset_game_state()

    draw_snake()
    draw_apples(apples)
    update_snake_view(snake, apples)


# -------------------------
# MANUAL - 1
# -------------------------

def key_pressed(event):

    global alive
    global auto_mode
    global real_mode
    global paused
    global episodes

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
        alive, episodes = fast_training(
            alive,
            apples,
            episodes,
            reset_game_state
        )
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
            #REAL mode always uses epsilon 0
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
        alive, reward = training_transition(state, action, apples)
        decay_training_epsilon(training_length)

    if real_mode == True:
        print_step_info("Real", state, action, reward)
    else:
        print_step_info("Training", state, action, reward)

    # Draw
    draw_snake()
    draw_apples(apples)
    update_snake_view(snake, apples)

    if alive == False:
        print_game_over()
        draw_rip_snake()

    window.after(100, training_step)


def initialize_board():
    draw_wall()
    draw_board()
    draw_snake()
    draw_apples(apples)
    create_snake_view(window)
    update_snake_view(snake, apples)


def draw_current_state(dead=False):
    draw_snake()
    draw_apples(apples)
    update_snake_view(snake, apples)
    if dead:
        draw_rip_snake()
    window.update_idletasks()
    window.update()


def wait_for_visual_step(step_by_step):
    if step_by_step:
        import tkinter as tk

        step_requested = tk.BooleanVar(master=window, value=False)
        window.bind_all("<space>", lambda event: step_requested.set(True))
        window.bind_all("<Return>", lambda event: step_requested.set(True))
        window.wait_variable(step_requested)
    else:
        window.after(1)


def run_interactive():
    initialize_display()
    initialize_board()
    window.bind("<Key>", key_pressed)
    training_step()
    window.mainloop()


def run_cli(args, parser):
    global alive
    global episodes

    visual = args.visual == "on"

    if args.step_by_step and not visual:
        parser.error("-step-by-step requires -visual on")

    if args.load:
        metadata = load_training_model(args.load)
        print("Load trained model from", metadata["path"])

    if visual:
        initialize_display()
        initialize_board()
        if args.step_by_step:
            print("Press Space or Enter for each move")
    metrics, episodes, alive = run_sessions(
        args.sessions,
        episodes,
        reset_game_state,
        learn=not args.dontlearn,
        visual=visual,
        step_by_step=args.step_by_step,
        draw_current_state=draw_current_state,
        wait_for_visual_step=wait_for_visual_step
    )
    print(
        "Game over, max length = "
        + str(metrics["max_length"])
        + ", max duration = "
        + str(metrics["max_duration"])
    )

    if args.save:
        model_path = save_model(
            q_table,
            epsilon_by_length,
            episodes,
            ALPHA,
            GAMMA,
            args.save
        )
        print("Save learning state in", model_path)

    if visual:
        window.destroy()


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:] #quita el primer elemento
    if len(argv) == 0:
        run_interactive()
        return

    parser = build_parser()
    args = parser.parse_args(argv)
    run_cli(args, parser)


if __name__ == "__main__":
    main()
