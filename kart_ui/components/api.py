from typing import List, Tuple
from game_logic.item import Item
from p5 import *
from kart_ui.components.shuffler import Shuffler
from kart_ui.components.debugger import Debugger
from kart_ui.components.map_ui import MapUI
from kart_ui.components.warning import Warning


MapData = List[Tuple[int, float, float]]

class KartUi:
    def __init__(self, debug=False):
        self.debugger = Debugger(on=True)
        self.shuffler = Shuffler(self.debugger)
        self.mini_map = MapUI(self.debugger)
        self.warning = Warning(self.debugger)  
        self.debugger.set_shuffler(self.shuffler)
        self.debugger.set_map(self.mini_map)  
        self.debugger.set_warning(self.warning)   
    
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
    
    def draw(self):
        background(255)
        self.shuffler.draw()
        self.debugger.draw()
        self.mini_map.draw()
        self.warning.draw()
    
    def on_mouse_pressed(self, mouse_x, mouse_y):
        self.debugger.mouse_pressed(mouse_x, mouse_y)