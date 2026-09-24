import tkinter as tk

import board
from state import look_down
from state import look_left
from state import look_right
from state import look_up


MAX_VIEW_DISTANCE = max(board.width, board.height)
CELL_SIZE = max(1, min(38, 800 // (MAX_VIEW_DISTANCE * 2 + 5)))
GRID_SIZE = MAX_VIEW_DISTANCE * 2 + 5
CANVAS_SIZE = GRID_SIZE * CELL_SIZE
CENTER = GRID_SIZE // 2

snake_view_window = None
snake_view_canvas = None
info_text = None


def create_snake_view(parent):

    global snake_view_window
    global snake_view_canvas
    global info_text

    if snake_view_window is not None:
        return

    snake_view_window = tk.Toplevel(parent)
    snake_view_window.title("Snake Vision")

    snake_view_canvas = tk.Canvas(
        snake_view_window,
        width=CANVAS_SIZE,
        height=CANVAS_SIZE
    )

    snake_view_canvas.pack()

    info_text = tk.StringVar(master=snake_view_window)
    info_label = tk.Label(
        snake_view_window,
        textvariable=info_text,
        justify="left",
        anchor="w"
    )

    info_label.pack(fill="x", padx=10, pady=10)

    snake_view_window.protocol(
        "WM_DELETE_WINDOW",
        snake_view_window.withdraw
    )


def update_info(
    mode, episodes, snake_length, duration, learning,
    epsilon, action, reward, states_learned, paused
):

    if reward is None:
        reward = "-"

    info_text.set(
        f"Mode: {mode}\n"
        f"Episodes: {episodes} |  Length: {snake_length} | Duration: {duration}\n"
        f"Learning: {'ON' if learning else 'OFF'} | Epsilon: {epsilon:.3f}\n"
        f"Last action: {action or '-'} | Last reward: {reward}\n"
        f"States learned: {states_learned} | Paused: {'YES' if paused else 'NO'}\n\n"
        "1 Manual | 2 Auto | 3 Fast | 4 RealMode\n"
        "R Restart | Space Pause | Esc Exit"
    )


def draw_cell(grid_row, grid_col, content):

    if content == "0":
        color = "white"
    elif content == "W":
        color = "gray"
    elif content == "S":
        color = "royal blue"
    elif content == "G":
        color = "green"
    elif content == "R":
        color = "red"
    else:
        color = "deepskyblue"

    x1 = grid_col * CELL_SIZE
    y1 = grid_row * CELL_SIZE

    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE

    snake_view_canvas.create_rectangle(
        x1,
        y1,
        x2,
        y2,
        fill=color,
        outline="black"
    )

    snake_view_canvas.create_text(
        (x1 + x2) / 2,
        (y1 + y2) / 2,
        text=content,
        fill="black",
        font=("Arial", 12, "bold")
    )


def draw_ray(vision, row_step, col_step):

    for i in range(len(vision)):

        distance = i + 1
        content = vision[i]

        grid_row = CENTER + row_step * distance
        grid_col = CENTER + col_step * distance

        draw_cell(grid_row, grid_col, content)


def draw_direction_labels():

    padding = CELL_SIZE
    center_pixel = CENTER * CELL_SIZE + CELL_SIZE // 2

    snake_view_canvas.create_text(
        center_pixel,
        padding,
        text="UP",
        fill="white",
        font=("Arial", 11, "bold")
    )
    snake_view_canvas.create_text(
        center_pixel,
        CANVAS_SIZE - padding,
        text="DOWN",
        fill="white",
        font=("Arial", 11, "bold")
    )
    snake_view_canvas.create_text(
        10,
        center_pixel,
        text="LEFT",
        fill="white",
        font=("Arial", 11, "bold"),
        anchor="w"
    )
    snake_view_canvas.create_text(
        CANVAS_SIZE - 10,
        center_pixel,
        text="RIGHT",
        fill="white",
        font=("Arial", 11, "bold"),
        anchor="e"
    )


def update_snake_view(snake, apples):

    if snake_view_canvas is None:
        return

    if len(snake) == 0:
        return

    head_row = snake[0][0]
    head_col = snake[0][1]

    up = look_up(head_row, head_col, snake, apples)
    down = look_down(head_row, head_col, snake, apples)
    left = look_left(head_row, head_col, snake, apples)
    right = look_right(head_row, head_col, snake, apples)

    snake_view_canvas.delete("all")

    draw_direction_labels()
    draw_cell(CENTER, CENTER, "H")

    draw_ray(up, -1, 0)
    draw_ray(down, 1, 0)
    draw_ray(left, 0, -1)
    draw_ray(right, 0, 1)
