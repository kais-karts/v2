from p5 import *
import RPi.GPIO as GPIO

from kart_ui.map import Map
from kart_ui.race import Race
from comms import PacketQueue, Packet
from constants import PORT, KART_ID, BUTTON_IN, BUTTON_OUT, ITEM_CHECKPOINTS, START_LINE, TRACK_PATH
from items import ITEMS, ItemTarget
from localization import current_location
from speed_ctrl import set_speed_multiplierfrom components.shuffler import Shuffler
from components.debugger import Debugger
from components.map import Map
from game_logic.constants import ITEMS
# Intellisense can't find these on its own for some reason
global mouse_is_pressed, mouse_x, mouse_y, key_is_pressed, key

packet_queue = PacketQueue(PORT)
map = Map(START_LINE, ITEM_CHECKPOINTS, TRACK_PATH)
race = Race(map)

# Global variables to track button state
button_pressed = False
last_button_state = None

def setup():
    """
    This method is called by p5 once at the beginning
    """
    size(800, 600)
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


    

    setup_button()

def setup_button():
    """
    Sets up button input for Raspberry Pi GPIO.
    """
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_IN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_OUT, GPIO.OUT)
        GPIO.output(BUTTON_OUT, GPIO.LOW)
        
        # Initialize last button state
        global last_button_state
        last_button_state = GPIO.input(BUTTON_IN)
        
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

def mouse_pressed():
    debugger.mouse_pressed(mouse_x, mouse_y)
    # print(f"({int(mouse_x)}, {int(mouse_y)})")
if __name__ == "__main__":
    start()


    # the stuff above is useless, but here's something more concrete:
    for go_kart in race:
        # Now, we're iterating the go karts in the ranking order, could be useful for e.g.
        # displaying the ranking UI
        # go_kart.
        pass

def check_button_press():
    """
    Check if the item button has been pressed.
    GPIO in production and keyboard in development.
    """
    global button_pressed, last_button_state
    
    # Try to use GPIO if available
    try:
        current_button_state = GPIO.input(BUTTON_IN)
        
        # Check for falling edge (1 -> 0, button press)
        if last_button_state == 1 and current_button_state == 0:
            button_pressed = True
            print("Button pressed (GPIO)")
        
        last_button_state = current_button_state
        
    except (NameError, RuntimeError):
        # Fall back to keyboard for development
        try:
            # Check for space key (common standard for 'use item')
            if key_is_pressed and key == ' ':
                if not button_pressed:  # Avoid multiple triggers while held
                    button_pressed = True
                    print("Button pressed (Keyboard)")
        except NameError:
            # If even p5 key detection isn't available, we can't detect input
            pass

def update():
    """
    Update the game logic each frame
    """
    # Update game state from packets received from other go-karts
    for packet in packet_queue:
        match packet.tag:
            case Packet.PING: pass
            case Packet.LOCATION: race.update_ranking(packet)
            case Packet.ATTACK: race.apply_item(packet)
    
    # Update my location and broadcast to everyone else
    location_packet = Packet(Packet.LOCATION, kart_id=KART_ID, location=current_location())
    
    race.update_ranking(location_packet)
    packet_queue.send(location_packet)

    # Pickup item if kart near checkpoint
    race.local_pickup_item()
    
    # Update local kart state (effects)
    race.owned_kart.update_item_effect()
    
    # Check for button press
    check_button_press()
    
    # Use item if button was pressed
    if button_pressed:
        if race.owned_kart._item_id is not None:
            race.owned_kart.use_held_item()
        button_pressed = False  # Reset after handling

    # Handle pending attack if one exists
    if race.owned_kart.pending_attack is not None:
        attack_packets = create_attack_packet(race.owned_kart.pending_attack)
        for attack_packet in attack_packets:
            packet_queue.send(attack_packet)
            print(f"Sent {ITEMS[attack_packet.data[1]].name} to kart {attack_packet.data[0]}")
        race.owned_kart.pending_attack = None

    # Update the speed control for this go kart
    set_speed_multiplier(race.owned_kart.speed_multiplier)

def create_attack_packet(item_id):
    """
    Creates attack packets based on the item type and its targeting rules.
    
    Args:
        item_id (int): The identifier of the item being used for the attack
        
    Returns:
        list[Packet]: A list of attack packets ready to be sent through the packet queue.
    """
    item = ITEMS[item_id]
    target_type = item.target
    
    # Handle different targeting types
    target_kart_ids = []
    
    if target_type == ItemTarget.FRONT:
        # Find the kart directly in front of us
        my_rank = race.rankings.index(KART_ID)
        if my_rank > 0:  # Not in first place
            target_kart_ids = [race.rankings[my_rank - 1]]
    
    elif target_type == ItemTarget.BEHIND:
        # Find the kart directly behind us
        my_rank = race.rankings.index(KART_ID)
        if my_rank < len(race.rankings) - 1:  # Not in last place
            target_kart_ids = [race.rankings[my_rank + 1]]
    
    elif target_type == ItemTarget.ALL_OTHERS:
        # Target all karts except self
        target_kart_ids = [kart_id for kart_id in race.rankings if kart_id != KART_ID]
    
    elif target_type == ItemTarget.LEADER:
        # Target the leader (first place)
        if len(race.rankings) > 0 and race.rankings[0] != KART_ID:
            target_kart_ids = [race.rankings[0]]
    
    attack_packets = []
    # Create attack packets for all targets
    for target_id in target_kart_ids:
        attack_packet = Packet(Packet.ATTACK, data=(target_id, item_id))
        attack_packets.append(attack_packet)
    
    return attack_packets

def start():
    """
    Start the UI. This function takes over the main thread (never returns)!
    """
    run(renderer="skia", sketch_draw=draw, sketch_setup=setup)