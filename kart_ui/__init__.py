from p5 import *
from components.shuffler import Shuffler
from components.debugger import Debugger
from components.map import Map
from game_logic.constants import ITEMS
# Intellisense can't find these on its own for some reason
global mouse_is_pressed, mouse_x, mouse_y
global shuffler, debugger, mini_map
global width, height

SHUFFLED_ITEMS = list(ITEMS.keys())
img = None
img_width = None
img_height = None

def start():
    """
    Start the UI. This function takes over the main thread (never returns)!
    """
    run(renderer="skia", sketch_draw=draw, sketch_setup=setup)


def setup():
    size(1024, 600) #touchscreen size
    background(200)
    global shuffler, debugger, img, img_width, img_height, mini_map
    debugger = Debugger(on=True)
    shuffler = Shuffler(debugger)
    mini_map = Map(debugger)
    debugger.set_shuffler(shuffler)
    debugger.set_map(mini_map)  
    # img = loadImage("kart_ui/images/no-item.png")
    # print("original size", img.width(), img.height())
    # img_width = int(img.width()/2)
    # img_height = int(img.height()/2)
    # img.resize(img_width, img_height)
    # no_tint()


    


def draw():
    background(255)
    shuffler.draw()
    debugger.draw()
    mini_map.draw()

def mouse_pressed():
    # debugger.mouse_pressed(mouse_x, mouse_y)
    # print(f"({int(mouse_x)}, {int(mouse_y)})")
    debugger.show_character_at(mouse_x, mouse_y)
if __name__ == "__main__":
    start()
