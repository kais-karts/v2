"""
This file imports p5 for drawings things and to help debug localization without involving
every other sub-system (namely kart_ui)
"""
from p5 import *


def setup():
    size(800, 600)
    background(200)


def draw():
    background(random_uniform(255), random_uniform(127), random_uniform(51), 127)


if __name__ == "__main__":
    run(renderer="skia", sketch_draw=draw, sketch_setup=setup)