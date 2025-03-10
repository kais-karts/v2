from p5 import *
from localization import current_location
from speed_ctrl import set_speed_multiplier
from comms import PacketQueue


# Intellisense can't find these on its own for some reason
global mouse_is_pressed, mouse_x, mouse_y


def start():
    """
    Start the UI. This function takes over the main thread (never returns)!
    """
    run(renderer="skia", sketch_draw=draw, sketch_setup=setup)


def setup():
    size(800, 600)
    background(200)


def draw():
    if mouse_is_pressed:
        fill(random_uniform(255), random_uniform(127), random_uniform(51), 127)
    else:
        fill(255, 15)

    circle_size = random_uniform(low=10, high=80)

    circle((mouse_x, mouse_y), circle_size)