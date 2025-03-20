from kart_ui import GoKart
from comms import Packet
from constants import KART_ID

class Race():
    """
    Complete state of a race.

    Attributes:
        go_karts (dict[int, GoKart]): Mapping of go-kart IDs to their respective GoKart objects
        rankings (list[int]): List of go-kart IDs in order of their current ranking
        me (GoKart): The GoKart object representing the go-kart running this code
    """
    def __init__(self, num_go_karts: int = 0):
        self._go_karts = { i: GoKart(i) for i in range(num_go_karts) }
        self._rankings = list(range(num_go_karts))
        self._me = self._go_karts[KART_ID]

    def _add_go_kart(self, go_kart: GoKart):
        """
        Add a go-kart to the race

        Args:
            go_kart (GoKart): Go-Kart to add
        """
        self._go_karts[go_kart.id] = go_kart
        self._rankings.append(go_kart.id) # Not necessarily last place, but assumes rankings will be sorted

    def update_ranking(self, packet: Packet):
        """
        Update the location of a GoKart, and thereby the ranking of the race

        Args:
            packet (Packet): Packet describing the new location of one of the go karts
        """
        assert packet.tag == Packet.LOCATION

        kart_id, kart_position = packet.kart_id, packet.location

        # Adds the go-kart to the race if it has not been seen before
        if kart_id not in self._go_karts:
            self._add_go_kart(GoKart(kart_id))
        
        # Update kart position
        kart = self._go_karts[kart_id]
        kart.position = kart_position
        
        self._rankings.remove(kart_id)
        new_rank = len(self._rankings)  # Default to last position

        # Check where the kart should be ranked
        for ix, other_kart_id in enumerate(self._rankings):
            if kart > self._go_karts[other_kart_id]:
                new_rank = ix
                break

        # Insert kart at new position
        self._rankings.insert(new_rank, kart_id)
            
    def apply_item(self, packet: Packet):
        """
        Apply an item to a Go-Kart in this race

        Args:
            packet (Packet): Packet describing the item being applied
        """
        assert packet.tag == Packet.ATTACK

        # TODO(bruke): the logic u had before. I've pasted it below
        # if item < 0 or item >= len(ITEMS):
        #     print("Invalid item index.")
        #     return
        # t = threading.Thread(target=apply_effect, args=(item))
        # t.start()
        # print(f"Applying item: {ITEMS[ITEMS.keys()[item]]}")

    def __iter__(self):
        """
        Iterate through the go-karts in this race, in order of their ranking
        """
        for ranking in self._rankings:
            yield self._go_karts[ranking]
    
    @property
    def owned_kart(self) -> GoKart:
        """
        Get the state of the "me" Go-Kart, i.e. the one running this code
        """
        return self._me