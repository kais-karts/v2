from constants import KART_ID, BASE_MULTIPLIER
from items import ITEMS, ItemEffect, ItemTarget, Item
from map import Map

import numpy as np
import time


class GoKart():
    """
    Complete state of a single Go-Kart.

    Attributes:
        id (int): Unique identifier for this kart.
        game_map (Map): The Map object representing the map that this kart is currently on.
        position (tuple[float, float] | None): 2D location on the track, or `None` if not yet known.
        laps (int): Number of laps completed by this kart.
        speed_multiplier (float): Multiplier for the kart's speed (default BASE_MULTIPLIER).
        item_id (int | None): Identifier of the currently held item, or 'None' if no item.
        ongoing_effect (bool): Whether the kart is undergoing the effects of an item.
        effect_ends_at (float | None): Timestamp at which the ongoing_effect ends, or 'None' if no ongoing_effect.
        pending_attack (int | None): Identifier of the item to be sent off to other Karts
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
        self._pending_attack = None

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
    
    @property
    def pending_attack(self) -> int | None:
        """
        Identifier of the item to be sent as an attack, or None if no pending attack
        """
        return self._pending_attack
        
    @pending_attack.setter
    def pending_attack(self, val):
        self._pending_attack = val

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
        
        ITEM_WEIGHTS = [item.distribution for item in ITEMS]

        weights = np.array(ITEM_WEIGHTS)
        weights = weights / weights.sum(axis=0)

        item = np.random.choice(len(ITEMS), p=weights[:, place-1])

        self._item_id = item
        print(f"Picked up item: {ITEMS[item].name}")

    def use_held_item(self) -> None:
        """
        Uses the currently stored item and applies its effect if possible.
        """
        if self._item_id is None:
            print("No item to use.")
            return
        
        item = ITEMS[self._item_id]

        if item.effect == ItemEffect.BUFF and item.target == ItemTarget.SELF:
            if self.apply_item(self._item_id):
                self._item_id = None
        else:
            self._pending_attack = item
            self._item_id = None
            print(f"Ready to send {item.name} to {item.target.value} target")

    def apply_item(self, item_id) -> bool:
        """
        Applies effects of the given item if there is no ongoing effect

        Returns
            Whether effects could be applied
        """
        self.update_item_effect() # Updates current item effect before attempting to apply item

        if not self._ongoing_effect: #TODO: Do we want effects applied if there is an ongoing effect? Maybe debuff should negate a buff? Or for specific items?
            item: Item = ITEMS[item_id]
            if item.effect == ItemEffect.BUFF:
                print(f"Using {item.name} → multiplier: {item.speed_multiplier}, duration: {item.duration}s")
            else:
                print(f"Hit with {item.name} → multiplier: {item.speed_multiplier}, duration: {item.duration}s")

            self.apply_speed_effect(item.speed_multiplier, item.duration)
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
