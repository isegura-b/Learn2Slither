import tkinter as tk

from snake import snake


BOARD_SIZE = 12
CELL_SIZE = 100
WINDOW_SIZE = BOARD_SIZE * CELL_SIZE

window = tk.Tk()

window.title("Learn2Slither")


canvas = tk.Canvas(
    window,
    width=WINDOW_SIZE,
    height=WINDOW_SIZE
)

canvas.pack()


def draw_board():

    for i in range(BOARD_SIZE + 1):

        position = i * CELL_SIZE

        canvas.create_line(
            position,
            0,
            position,
            WINDOW_SIZE
        )

        canvas.create_line(
            0,
            position,
            WINDOW_SIZE,
            position
        )


def draw_wall():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if (
                row == 0
                or row == BOARD_SIZE - 1
                or col == 0
                or col == BOARD_SIZE - 1
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

    for i in range(len(snake)):

        row = snake[i][0]
        col = snake[i][1]

        x1 = col * CELL_SIZE
        y1 = row * CELL_SIZE

        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE

        canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill="green",
            tags="snake"
        )

        if i == 0:

            canvas.create_rectangle(
                x1 + 30,
                y1 + 30,
                x1 + 70,
                y1 + 70,
                fill="white",
                tags="snake"
            )

            canvas.create_rectangle(
                x1 + 40,
                y1 + 40,
                x1 + 60,
                y1 + 60,
                fill="black",
                tags="snake"
            )

def draw_rip_snake():
    canvas.delete("snake")

    for i in range(len(snake)):

        row = snake[i][0]
        col = snake[i][1]

        x1 = col * CELL_SIZE
        y1 = row * CELL_SIZE

        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE

        canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill="green",
            tags="snake"
        )

        if i == 0:

            canvas.create_rectangle(
                x1 + 30,
                y1 + 30,
                x1 + 70,
                y1 + 70,
                fill="white",
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
            x1 + 20,
            y1 + 20,
            x2 - 20,
            y2 - 20,
            fill="red",
            tags="apple"
        )
    else:
        canvas.create_oval(
            x1 + 20,
            y1 + 20,
            x2 - 20,
            y2 - 20,
            fill="green",
            tags="apple"
        )


def draw_apples(apples):

    canvas.delete("apple")

    for apple in apples:
        draw_apple(apple[0], apple[1])