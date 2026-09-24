import tkinter as tk

import board
from snake import snake


BOARD_WIDTH = board.width + 2
BOARD_HEIGHT = board.height + 2
LARGEST_BOARD_SIDE = max(BOARD_WIDTH, BOARD_HEIGHT)
CELL_SIZE = 800 // LARGEST_BOARD_SIDE
if CELL_SIZE < 1:
    CELL_SIZE = 1
elif CELL_SIZE > 100:
    CELL_SIZE = 100

WINDOW_WIDTH = BOARD_WIDTH * CELL_SIZE
WINDOW_HEIGHT = BOARD_HEIGHT * CELL_SIZE

window = tk.Tk()

window.title("Learn2Slither")


canvas = tk.Canvas(
    window,
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT
)

canvas.pack()

snake_length_text = tk.StringVar()
snake_length_label = tk.Label(
    window,
    textvariable=snake_length_text,
    font=("Arial", 18, "bold"),
    pady=10
)
snake_length_label.pack()


def update_snake_length():
    snake_length_text.set("Snake length: " + str(len(snake)))


def draw_board():

    for i in range(BOARD_WIDTH + 1):

        position = i * CELL_SIZE

        canvas.create_line(
            position,
            0,
            position,
            WINDOW_HEIGHT
        )

    for i in range(BOARD_HEIGHT + 1):

        position = i * CELL_SIZE

        canvas.create_line(
            0,
            position,
            WINDOW_WIDTH,
            position
        )


def draw_wall():
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if (
                row == 0
                or row == BOARD_HEIGHT - 1
                or col == 0
                or col == BOARD_WIDTH - 1
            ):

                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE

                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill="gray",
                    tags="wall"
                )


def draw_snake():

    canvas.delete("snake")
    update_snake_length()

    for i in range(len(snake)):

        row = snake[i][0]
        col = snake[i][1]

        x1 = col * CELL_SIZE
        y1 = row * CELL_SIZE

        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE

        if i == 0:
            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill="deepskyblue",
                tags="snake"
            )
            canvas.create_rectangle(
                x1 + CELL_SIZE * 0.3,
                y1 + CELL_SIZE * 0.3,
                x1 + CELL_SIZE * 0.7,
                y1 + CELL_SIZE * 0.7,
                fill="white",
                tags="snake"
            )
            canvas.create_rectangle(
                x1 + CELL_SIZE * 0.4,
                y1 + CELL_SIZE * 0.4,
                x1 + CELL_SIZE * 0.6,
                y1 + CELL_SIZE * 0.6,
                fill="black",
                tags="snake"
            )
        else:
            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill="royal blue",
                tags="snake"
            )


def draw_rip_snake():
    canvas.delete("snake")
    update_snake_length()

    for i in range(len(snake)):

        row = snake[i][0]
        col = snake[i][1]

        x1 = col * CELL_SIZE
        y1 = row * CELL_SIZE

        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE

        if i == 0:
            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill="deepskyblue",
                tags="snake"
            )
            canvas.create_rectangle(
                x1 + CELL_SIZE * 0.3,
                y1 + CELL_SIZE * 0.3,
                x1 + CELL_SIZE * 0.7,
                y1 + CELL_SIZE * 0.7,
                fill="white",
                tags="snake"
            )
            canvas.create_text(
                x1 + CELL_SIZE * 0.5,
                y1 + CELL_SIZE * 0.5,
                text="X",
                fill="black",
                font=("Arial", 18, "bold"),
                tags="snake"
            )
        else:
            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill="royal blue",
                tags="snake"
            )


def draw_apple(apple, rgb):

    row = apple[0]
    col = apple[1]

    x1 = col * CELL_SIZE
    y1 = row * CELL_SIZE

    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE

    if (rgb == "red"):
        canvas.create_oval(
            x1 + CELL_SIZE * 0.2,
            y1 + CELL_SIZE * 0.2,
            x2 - CELL_SIZE * 0.2,
            y2 - CELL_SIZE * 0.2,
            fill="red",
            tags="apple"
        )
    else:
        canvas.create_oval(
            x1 + CELL_SIZE * 0.2,
            y1 + CELL_SIZE * 0.2,
            x2 - CELL_SIZE * 0.2,
            y2 - CELL_SIZE * 0.2,
            fill="green",
            tags="apple"
        )


def draw_apples(apples):

    canvas.delete("apple")

    for apple in apples:
        draw_apple(apple[0], apple[1])
