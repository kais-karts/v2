from p5 import *

from kart_ui.go_kart import GoKart
from kart_ui.race import Race
from comms import PacketQueue, Packet
from constants import PORT, KART_ID, NUM_GO_KARTS
from items import ITEMS, ItemTarget
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
    # check for finshed lap
    packet_queue.send(location_packet)

    # Pickup item if I am near checkpoint
    race.local_pickup_item()
    # update local state
    # send attacks

    # Handle pending attack if one exists
    if race.owned_kart.pending_attack is not None:
        attack_packets = create_attack_packet(race.owned_kart.pending_attack)
        for attack_packet in attack_packets:
            packet_queue.send(attack_packet)
            print(f"Sent {ITEMS[attack_packet.data[1]]} to kart {attack_packet.data[0]}")
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