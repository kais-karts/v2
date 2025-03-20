from p5 import *
global width, height
from game_logic.constants import ITEMS, MAP_METERS_PER_PIXEL
SHUFFLED_ITEMS = list(ITEMS.keys())
TEST_KART_POSITIONS = [(),]
class Debugger:
    def __init__(self, on=False):
        self.on = on
        self.shuffler = None
        self.map = None
        
        
    def draw(self):
        if self.on:
            # Draw center lines
            stroke(0)  # Black lines
            strokeWeight(1)
            
            # Vertical center line
            line(width/2, 0, width/2, height)
            
            # Horizontal center line  
            line(0, height/2, width, height/2)
    
    def mouse_pressed(self, mouse_x, mouse_y):
        if self.on and self.shuffler is not None:
            if mouse_x < width/2:
                item = SHUFFLED_ITEMS[int(random_uniform(0, len(SHUFFLED_ITEMS)))]
                # item = 'banana'
                self.shuffler.shuffle(item)
            else:
                self.shuffler.use_item()
    def show_image_outline(self, x, y, width, height):
        if self.on:
            stroke(255, 0, 0)  # Red border
            stroke_weight(2)  # Border thickness
            no_fill()
            rect(x-width/2, y-height/2, width, height)

    def set_shuffler(self, shuffler):
        self.shuffler = shuffler
    
    def set_map(self, map):
        self.map = map
    
    def show_character_at(self, mouse_x, mouse_y):
        rel_x, rel_y = float((mouse_x-self.map.map_x)), float((mouse_y-self.map.map_y))
        print(f"({int(rel_x)}, {int(rel_y)})")
        self.map.update({0: (rel_x, rel_y)})
        
