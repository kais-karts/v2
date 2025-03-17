from kart_ui import GoKart
from comms import Packet
from constants import KART_ID

class Race():
    """
    Complete state of a race
    """
    def __init__(self, num_go_karts: int):
        self._go_karts = { i: GoKart(i) for i in range(num_go_karts) }
        self._rankings = list(range(num_go_karts))
        self._me = self._go_karts[KART_ID]

    def update_ranking(self, packet: Packet):
        """
        Update the location of a GoKart, and thereby the ranking of the race

        Args:
            packet (Packet): Packet describing the new location of one of the go karts
        """
        assert packet.tag == Packet.LOCATION

        # TODO(bruke): the logic u had before. I've pasted it below
        # print(f"Updating ranking with location data: {kart_id=} {position=}")

        # kart_to_update = kart_id
        # kart_location = position
        # prev_rank = ranking.index(kart_to_update) 

        # # update kart position
        # kart_index = get_location_index(kart_location)
        # positions[kart_to_update] = kart_index

        # # update ranking
        # ranking.remove(kart_to_update)
        # for i in range(len(ranking)):
        #     if kart_index > ranking[i]:
        #         ranking.insert(i, kart_to_update)
        #         break
        
        # # for debugging
        # new_rank = ranking.index(kart_to_update)
        # if new_rank < prev_rank:
        #     print(f"Kart {kart_to_update} moved up in the rankings!")
        # elif new_rank > prev_rank:
        #     print(f"Kart {kart_to_update} moved down in the rankings!")
        # else:
        #     print(f"Kart {kart_to_update} did not move in the rankings.")

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