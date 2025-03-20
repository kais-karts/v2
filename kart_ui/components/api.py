from dataclasses import dataclass
from typing import List, Tuple


MapData = List[Tuple[int, float, float]]

class API:
    def __init__(self, shuffler, mini_map, warning):
        self.shuffler = shuffler
        self.mini_map = mini_map
        self.warning = warning
    
    def update_map(self, map_data: MapData):
        self.mini_map.update(map_data)
        
    def item_hit(self, item: str):
        self.warning.item_hit(item)
    
    def item_get(self, item: str):
        self.shuffler.shuffle(item)
    def item_use(self):
        self.shuffler.use_item()
    