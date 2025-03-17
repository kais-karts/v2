from p5 import *
from comms import PacketQueue, Packet
from kart_ui.game_logic.actions import update_ranking, apply_item
from constants import PORT, KART_ID
from localization import current_location

# Intellisense can't find these on its own for some reason
global mouse_is_pressed, mouse_x, mouse_y

packet_queue = PacketQueue(PORT)

def setup():
    size(800, 600)
    background(200)


def draw():
    # Update game state from received packets
    for packet in packet_queue:
        match packet.tag:
            case Packet.PING: pass
            case Packet.LOCATION: update_ranking(packet.kart_id, packet.position)
            case Packet.ATTACK:
                if packet.victim_id == KART_ID:
                    apply_item(packet.item_id)
            # etc...

    # Update game state based on location update
    # TODO: i've commented this out for now, I'm assuming the function isn't done? it's crashing atm
    # update_ranking(KART_ID, current_location())

    # Now draw stuff to the screen
    if mouse_is_pressed:
        fill(random_uniform(255), random_uniform(127), random_uniform(51), 127)
    else:
        fill(255, 15)

    circle_size = random_uniform(low=10, high=80)

    circle((mouse_x, mouse_y), circle_size)


def start():
    """
    Start the UI. This function takes over the main thread (never returns)!
    """
    run(renderer="skia", sketch_draw=draw, sketch_setup=setup)