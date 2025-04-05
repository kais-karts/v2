from typing import Dict, List

from comms import Packet

from constants import KART_ID
from map import Map
from go_kart import GoKart

from components.api import API

class Race():
    """
    Complete state of a race.

    Attributes:
        me (GoKart): The GoKart object representing the go-kart running this code
        game_map (Map): The Map object that this race is played on.
        go_karts (dict[int, GoKart]): Mapping of go-kart IDs to their respective GoKart objects
        rankings (list[int]): List of go-kart IDs in order of their current ranking
        ui_api (API): API for the local kart UI
    """
    def __init__(self, game_map: Map, ui_api: API):
        self._me: GoKart = GoKart(KART_ID, game_map, ui_api)
        self._game_map: Map = game_map
        self._go_karts: Dict[int, GoKart] = {KART_ID: self._me}
        self.rankings: List[int] = [KART_ID]
        self.ui: API = ui_api

    def _add_go_kart(self, go_kart: GoKart):
        """
        Add a go-kart to the race

        Args:
            go_kart (GoKart): Go-Kart to add
        """
        self._go_karts[go_kart.id] = go_kart
        self.rankings.append(go_kart.id) # Not necessarily last place, but assumes rankings will be sorted

    def update_ranking(self, packet: Packet):
        """
        Update the location of a GoKart, and thereby the ranking of the race

        Args:
            packet (Packet): Packet describing the new location of one of the go karts
        """
        if packet.tag != Packet.LOCATION:
            return

        kart_id, kart_position = packet.kart_id, packet.location

        # Adds the go-kart to the race if it has not been seen before
        if kart_id not in self._go_karts:
            self._add_go_kart(GoKart(kart_id, self._game_map))
        
        # Update kart position
        kart = self._go_karts[kart_id]
        kart.update_position(kart_position)
        
        self.rankings.remove(kart_id)
        new_rank = len(self.rankings)  # Default to last position

        # Check where the kart should be ranked
        for ix, other_kart_id in enumerate(self.rankings):
            if kart > self._go_karts[other_kart_id]:
                new_rank = ix
                break

        # Insert kart at new position
        self.rankings.insert(new_rank, kart_id)

        self.ui.update_map([(kart_id, *kart.position) for kart_id, kart in self._go_karts.items()])
            
    def apply_attack(self, packet: Packet):
        """
        Applies an attack (debuff item) to the local Go Kart in the race if it is the target
            else does nothing

        Args:
            packet (Packet): Packet describing the item being applied
        """
        if packet.tag != Packet.ATTACK:
            return

        victim_id, item_id = packet.data

        if victim_id == KART_ID:
            self._me.apply_item(item_id)
        
            

    def local_pickup_item(self):
        """
        Picks up an item locally if item checkpoint is reached 
        """
        place = self.rankings.index(KART_ID) + 1
        self._me.pickup_item(place)

    def __iter__(self):
        """
        Iterate through the go-karts in this race, in order of their ranking
        """
        for ranking in self.rankings:
            yield self._go_karts[ranking]
    
    @property
    def owned_kart(self) -> GoKart:
        """
        Get the state of the "me" Go-Kart, i.e. the one running this code
        """
        return self._me