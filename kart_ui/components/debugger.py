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
            
            fill(255, 0, 0)
            circle(self.map.origin_x, self.map.origin_y, 50)
    
    def mouse_pressed(self, mouse_x, mouse_y):
        if self.on:
            self.show_luigi_at(mouse_x, mouse_y)    
        if self.shuffler is not None:
            if mouse_x < width/2:
                item = SHUFFLED_ITEMS[int(random_uniform(0, len(SHUFFLED_ITEMS)))]
                # item = 'banana'
                self.shuffler.shuffle(item)
            else:
                self.shuffler.use_item()
    def show_image_outline(self, x, y, width, height, loc='center'):
        if self.on:
            stroke(255, 0, 0)  # Red border
            stroke_weight(2)  # Border thickness
            no_fill()
            if loc == 'center':
                rect(x-width/2, y-height/2, width, height)
            elif loc == 'top_left':
                rect(x, y, width, height)
            elif loc == 'top_right':
                rect(x-width, y, width, height)
                

    def set_shuffler(self, shuffler):
        self.shuffler = shuffler
    
    def set_map(self, map):
        self.map = map
    
    def show_luigi_at(self, mouse_x, mouse_y):
        map_x = (mouse_x - self.map.origin_x) / self.map.scale_size
        map_y = (mouse_y - self.map.origin_y) / self.map.scale_size
        new_positions = self.map.kart_positions.copy()
        new_positions[4] = (map_x, map_y)
        print(map_x, map_y)
        self.map.update(new_positions)
        
