from snake import move_snake
from snake import reset_snake
from snake import snake

from apple import create_apple
from apple import apple_eaten

from display import window
from display import draw_board
from display import draw_snake
from display import draw_wall
from display import draw_rip_snake
from display import draw_apples

from state import get_state

from agent import q_table
from agent import add_state

alive = True

apples = []
apples.append(create_apple("green", snake, apples))
apples.append(create_apple("green", snake, apples))
apples.append(create_apple("red", snake, apples))


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
        apples.append(create_apple("green", snake, apples))
        apples.append(create_apple("green", snake, apples))
        apples.append(create_apple("red", snake, apples))
        draw_snake()
        draw_apples(apples)
        return

    if alive == False:
        return

    if event.keysym == "Right":
        alive = move_snake("Right", apples)
        print("Right")
    elif event.keysym == "Left":
        alive = move_snake("Left", apples)
        print("Left")
    elif event.keysym == "Up":
        alive = move_snake("Up", apples)
        print("Up")
    elif event.keysym == "Down":
        alive = move_snake("Down", apples)
        print("Down")
    else:            #if any other key
        return

    if alive == False:
        draw_rip_snake()
        return

    draw_snake()
    draw_apples(apples)

    state = get_state(snake, apples)
    add_state(state)
    print("States learned:", len(q_table))
    print(state)


draw_wall()
draw_board()
draw_snake()
draw_apples(apples)

window.bind("<Key>", key_pressed)

window.mainloop()