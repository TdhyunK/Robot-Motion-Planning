from cs1lib import *

def draw():
    global x, vx
    clear()

    set_clear_color(.8, .4, .4)
    clear()

    set_fill_color(.2, .5, .9)
    set_stroke_color(1, 1, 0)
    draw_rectangle(100, 100, 200, 200)

    set_stroke_color(0, 0, 0)
    set_fill_color(1, 1, 1)
    draw_circle(200, 200, 100)

start_graphics(draw)