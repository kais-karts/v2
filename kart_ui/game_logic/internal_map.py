from typing import Tuple

current_item = None

item_locations = [] # List of item locations by index

def get_location_index(loc: Tuple) -> int:
    ''' Get the index of the location on the track

    Args:
        loc (Tuple(str, str)): The location data

    Returns:
        int: The index of the location on the track
    '''
    pass

def check_item_pickup(kart_location: Tuple) -> bool:
    ''' Check if the kart has passed an item location

    Args:
        kart_location (Tuple(str, str)): The location data

    Returns:
        bool: True if the kart has passed an item location, False otherwise
    '''
    pass