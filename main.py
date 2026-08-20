from snake import move_snake
from snake import reset_snake

from apple import create_apple
from apple import apple_eaten

from display import window
from display import draw_board
from display import draw_snake
from display import draw_wall
from display import draw_rip_snake
from display import draw_apples

alive = True

apples = []
apples.append(create_apple("green"))
apples.append(create_apple("green"))
apples.append(create_apple("red"))


def key_pressed(event):

    global alive
    global apples

    if event.keysym == "Escape":
        window.destroy()
        return
    if event.keysym == "r" or event.keysym == "R":
        reset_snake()
        alive = True
        apples = []
        apples.append(create_apple("green"))
        apples.append(create_apple("green"))
        apples.append(create_apple("red"))
        draw_snake()
        draw_apples(apples)
        return

    if alive == False:
        return

    if event.keysym == "Right":
        alive = move_snake("Right", apples)
    elif event.keysym == "Left":
        alive = move_snake("Left", apples)
    elif event.keysym == "Up":
        alive = move_snake("Up", apples)
    elif event.keysym == "Down":
        alive = move_snake("Down", apples)
    else:            #if any other key
        return

    if alive == False:
        draw_rip_snake()
        return

    draw_snake()
    draw_apples(apples)


draw_wall()
draw_board()
draw_snake()
draw_apples(apples)

window.bind("<Key>", key_pressed)

window.mainloop()