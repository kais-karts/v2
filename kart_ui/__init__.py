from p5 import *

from kart_ui.go_kart import GoKart
from kart_ui.race import Race
from comms import PacketQueue, Packet
from constants import PORT, KART_ID, NUM_GO_KARTS
from localization import current_location
from speed_ctrl import set_speed_multiplier

# Intellisense can't find these on its own for some reason
global mouse_is_pressed, mouse_x, mouse_y

packet_queue = PacketQueue(PORT)
race = Race(NUM_GO_KARTS)

def setup():
    """
    This method is called by p5 once at the beginning
    """
    size(800, 600)
    background(200)


def draw():
    """
    This method is called by p5 each frame
    """
    update()

    # Now draw stuff to the screen
    if mouse_is_pressed:
        fill(random_uniform(255), random_uniform(127), random_uniform(51), 127)
    else:
        fill(255, 15)

    circle_size = random_uniform(low=10, high=80)

    circle((mouse_x, mouse_y), circle_size)

    # the stuff above is useless, but here's something more concrete:
    for go_kart in race:
        # Now, we're iterating the go karts in the ranking order, could be useful for e.g.
        # displaying the ranking UI
        # go_kart.
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

    # Pickup item if I am near checkpoint
    race.local_pickup_item()

    # Update the speed control for this go kart
    set_speed_multiplier(race.owned_kart.speed_multiplier)

def start():
    """
    Start the UI. This function takes over the main thread (never returns)!
    """
    run(renderer="skia", sketch_draw=draw, sketch_setup=setup)