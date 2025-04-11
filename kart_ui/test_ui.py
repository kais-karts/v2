from p5 import *
# from p5 import Sketch
from kart_ui.kart_ui import KartUi
global kart_ui
global mouse_is_pressed, mouse_x, mouse_y, key_is_pressed, key, mouuse_pressed
def setup():
    global kart_ui
    kart_ui = KartUi(debugMode=True)
def draw():
    kart_ui.draw()
    # print(mouse_x, mouse_y)

def mouse_pressed():
    kart_ui.on_mouse_pressed(mouse_x, mouse_y)
    
def start():
    run(renderer="skia", sketch_draw=draw, sketch_setup=setup)
    
if __name__ == "__main__":
    start()
