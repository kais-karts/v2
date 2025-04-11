from typing import List, Tuple
from game_logic.item import Item


MapData = List[Tuple[int, float, float]]

class KartUi:
    def __init__(self, debug=False):
        raise NotImplementedError()
    
        self.shuffler = shuffler
        self.mini_map = mini_map
        self.warning = warning
    
    def update_map(self, map_data: MapData):
        self.mini_map.update(map_data)
        
    def on_incoming_item(self, item: Item):
        """
        Called the frame that someone has hit this kart with an item
        """
        self.warning.item_hit(item)
    
    def on_picked_up_item(self, item: Item):
        """
        Called the frame that this kart has picked up an item
        """
        self.shuffler.shuffle(item)
        
    def on_use_item(self):
        """
        Called the frame that this kart is using an item
        """
        self.shuffler.use_item()

    def can_use_item(self) -> bool:
        """
        When shuffling through items, returns `True` if the animation is done
        """
        raise NotImplementedError()
    