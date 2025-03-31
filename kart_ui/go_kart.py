from constants import KART_ID, BASE_MULTIPLIER, ITEMS, ITEM_NAMES, ITEM_WEIGHTS
from kart_ui.map import Map

import numpy as np
import time


class GoKart():
    """
    Complete state of a single Go-Kart.

    Attributes:
        id (int): Unique identifier for this kart.
        position (tuple[float, float] | None): 2D location on the track, or `None` if not yet known.
        laps (int): Number of laps completed by this kart.
        speed_multiplier (float): Multiplier for the kart's speed (default BASE_MULTIPLIER).
        item_id (int | None): Identifier of the currently held item, or 'None' if no item.
        ongoing_effect (bool): Whether the kart is undergoing the effects of an item.
        effect_ends_at (float | None): Timestamp at which the ongoing_effect ends, or 'None' if no ongoing_effect.
    """
    def __init__(self, id: int, game_map: Map):
        self._id = id
        self._game_map = game_map
        self._position = None
        self._laps = 0
        self.speed_multiplier = BASE_MULTIPLIER
        self._item_id = None
        self._ongoing_effect = False
        self._effect_ends_at = None

    @property
    def id(self) -> int:
        """
        Unique identifier for this kart (0..=7)
        """
        return self._id
    
    @property
    def is_owned(self) -> bool:
        """
        Does this Go-Kart object refer to the go-kart running this code rn?
        """
        return self._id == KART_ID
    
    @property
    def position(self) -> tuple[float, float] | None:
        """
        2D location on the track, or `None` is not yet known
        """
        return self._position
    
    @position.setter
    def position(self, val):
        self._position = val

    @property
    def laps(self) -> int:
        """
        Number of laps completed by this kart
        """
        return self._laps

    def __gt__(self, other) -> bool:
        """
        Check if this kart is ahead of another kart
        """
        if not isinstance(other, GoKart):
            return NotImplemented
        return (self._laps > other.laps) or (self._laps == other.laps and self._position > other.position)
    
    def update_position(self, new_pos) -> None:
        """
        Updates kart position, checking for valid movement and lap completion.
        """
        if self._game_map.is_valid_movement(self._position, new_pos):
            if self._game_map.crossed_finish_line(self._position, new_pos):
                self._laps += 1
        self._position = new_pos

    def pickup_item(self, place: int) -> None:
        """
        Picks up item based on kart's rank if within item checkpoint.
        """
        if not self._game_map.is_within_item_checkpoint(self._position):
            return
        
        weights = np.array(ITEM_WEIGHTS)
        weights = weights / weights.sum(axis=0)

        item = np.random.choice(ITEM_NAMES, p=weights[:, place-1])
        self._item_id = ITEM_NAMES.index(item)
        print(f"Picked up item: {item}")

    def use_held_item(self) -> None:
        """
        Uses the currently stored item and applies its effect if possible.
        """
        if self._item_id is None:
            print("No item to use.")
            return

        if self.apply_item(self._item_id):
            self._item_id = None

    def apply_item(self, item_id) -> bool:
        """
        Applies effects of the given item if there is no ongoing effect

        Returns
            Whether effects could be applied
        """
        self.update_item_effect()
        if not self._ongoing_effect: #TODO: DO WE WANT THIS?
            item_name = list(ITEMS.keys())[item_id]
            multiplier, duration = ITEMS[item_name]
            print(f"Using {item_name} → multiplier: {multiplier}, duration: {duration}s")

            self.apply_speed_effect(multiplier, duration)
            return True
        return False

    def apply_speed_effect(self, multiplier: float, duration: float):
        """
        Temporarily changes the kart's speed multiplier.
        """
        self.speed_multiplier = multiplier
        self._ongoing_effect = True
        self._effect_ends_at = time.time() + duration

    def update_item_effect(self) -> None:
        """
        Checks whether item effect duration has been reached and adjusts state.
        """
        if self._ongoing_effect:
            if time.time() >= self._effect_ends_at:
                self.speed_multiplier = BASE_MULTIPLIER
                self._effect_ends_at = None
                self._ongoing_effect = False
                print("Speed effect ended, reset to base.")

    def update_local_state(self):
        self.update_item_effect()
        self.check_button_pressed()
        # check for button pressed