from p5 import *
# import RPi.GPIO as GPIO

from comms import PacketQueue

from constants import PORT, BUTTON_IN, BUTTON_OUT, ITEM_CHECKPOINTS, START_LINE, TRACK_PATH
from kart_ui.game_logic.map import Map
from kart_ui.game_logic.race import Race
from kart_ui.game_logic.game_controller import GameController, last_button_state

from kart_ui.components.shuffler import Shuffler
from kart_ui.components.debugger import Debugger
from kart_ui.components.map_ui import MapUI
from kart_ui.components.warning import Warning
from kart_ui.components.api import API

# Intellisense can't find these on its own for some reason
global mouse_is_pressed, mouse_x, mouse_y, key_is_pressed, key
global shuffler, debugger, mini_map, warning, ui_api
global width, height

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
    global shuffler, debugger, img, img_width, img_height, mini_map, warning, ui_api, packet_queue, game_controller, race
    
    debugger = Debugger(on=True)
    shuffler = Shuffler(debugger)
    mini_map = MapUI(debugger)
    warning = Warning(debugger)
    ui_api = API(shuffler, mini_map, warning)

    packet_queue = PacketQueue(PORT)
    map = Map(START_LINE, ITEM_CHECKPOINTS, TRACK_PATH, ui_api)
    race = Race(map, ui_api)
    game_controller = GameController(map, race, ui_api, packet_queue)

    debugger.set_shuffler(shuffler)
    debugger.set_map(mini_map)  
    debugger.set_warning(warning)
    
    setup_button()

def setup_button():
    """
    Sets up button input for Raspberry Pi GPIO.
    """
    try:
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(BUTTON_IN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # GPIO.setup(BUTTON_OUT, GPIO.OUT)
        # GPIO.output(BUTTON_OUT, GPIO.LOW)
        
        # Initialize last button state
        global last_button_state
        # last_button_state = GPIO.input(BUTTON_IN)
        
        print("GPIO button setup complete")
    except (ImportError, RuntimeError) as e:
        print(f"GPIO button setup failed: {e}")
        print("Running in development mode without GPIO")

def draw():
    """
    This method is called by p5 each frame
    """
    update()

    # Now draw stuff to the screen
    background(255)
    shuffler.draw()
    debugger.draw()
    mini_map.draw()
    warning.draw()

def mouse_pressed():
    debugger.mouse_pressed(mouse_x, mouse_y)

def update():
    """
    Update the game logic each frame
    """
    game_controller.update()

def start():
    """
    Start the UI. This function takes over the main thread (never returns)!
    """
    run(renderer="skia", sketch_draw=draw, sketch_setup=setup)
    
if __name__ == "__main__":
    start()


    # the stuff above is useless, but here's something more concrete:
    for go_kart in race:
        # Now, we're iterating the go karts in the ranking order, could be useful for e.g.
        # displaying the ranking UI
        # go_kart.
        pass