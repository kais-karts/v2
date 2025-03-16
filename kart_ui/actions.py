''' This module contains functions that update the rankings and apply items to the kart. '''

from localization import current_location
from speed_ctrl import set_speed_multiplier
from internal_map import get_location_index
from constants import ITEMS, BASE_MULTIPLIER

import threading
import time

positions = {} # Dict of kart_id: index/position
ranking = [] # List of kart_id in order of position (index 0 is first place)
affect_lock = threading.Lock()

def update_ranking(data):
    """Update the rankings based on the location data

    Args:
        data (str): The location data
    """

    print(f"Updating ranking with location data: {data}")

    kart_to_update = data.kart_id
    kart_location = data.position
    prev_rank = ranking.index(kart_to_update) 

    # update kart position
    kart_index = get_location_index(kart_location)
    positions[kart_to_update] = kart_index

    # update ranking
    ranking.remove(kart_to_update)
    for i in range(len(ranking)):
        if kart_index > ranking[i]:
            ranking.insert(i, kart_to_update)
            break
    
    # for debugging
    new_rank = ranking.index(kart_to_update)
    if new_rank < prev_rank:
        print(f"Kart {kart_to_update} moved up in the rankings!")
    elif new_rank > prev_rank:
        print(f"Kart {kart_to_update} moved down in the rankings!")
    else:
        print(f"Kart {kart_to_update} did not move in the rankings.")

def apply_item(item: int):
    """Apply an item to the kart

    Args:
        item (int): The item to apply (index of the item in the ITEMS dict)
    """
    if item < 0 or item >= len(ITEMS):
        print("Invalid item index.")
        return
    t = threading.Thread(target=apply_effect, args=(item))
    t.start()
    print(f"Applying item: {ITEMS[ITEMS.keys()[item]]}")

def apply_effect(item: int):
    """Apply the item after a delay"""
    if affect_lock.acquire(blocking=False):
        item_data = ITEMS[ITEMS.keys()[item]]
        print("<Item Applied>")
        set_speed_multiplier(item_data[0])
        time.sleep(item_data[1])
        print("!Speed Restored!")
        set_speed_multiplier(BASE_MULTIPLIER)
        affect_lock.release()
    else:
        print("Affect lock already held, item not applied.")