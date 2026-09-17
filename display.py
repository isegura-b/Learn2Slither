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
