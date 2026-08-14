from snake import move_snake
from snake import reset_snake

from display import window
from display import draw_board
from display import draw_snake
from display import draw_wall
from display import draw_rip_snake


alive = True


def key_pressed(event):

    global alive

    if event.keysym == "Escape":
        window.destroy()
        return
    if event.keysym == "r" or event.keysym == "R":
        reset_snake()
        alive = True
        draw_snake()
        return

    if alive == False:
        return

    if event.keysym == "Right":
        alive = move_snake("Right")
    elif event.keysym == "Left":
        alive = move_snake("Left")
    elif event.keysym == "Up":
        alive = move_snake("Up")
    elif event.keysym == "Down":
        alive = move_snake("Down")
    else:            #if any other key
        return

    if alive == False:
        draw_rip_snake()
        return

    print(event.keysym)
    draw_snake()


draw_wall()
draw_board()
draw_snake()

window.bind("<Key>", key_pressed)

window.mainloop()