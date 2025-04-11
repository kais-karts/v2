from p5 import *
def setup():
    size(1024, 600)
def draw():
    background(255)
run(renderer="skia", sketch_draw=draw, sketch_setup=setup)