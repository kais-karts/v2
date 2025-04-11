from p5 import *
# from kart_ui.kart_ui import KartUi
global kart_ui
run(renderer="skia", sketch_draw=draw, sketch_setup=setup)
def setup():
    size(1024, 600)
    # global kart_ui
    # kart_ui = KartUi()
def draw():
    # kart_ui.draw()
    background(255)
