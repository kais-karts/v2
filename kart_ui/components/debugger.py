from p5 import *
from game_logic.item import Item

global width, height

SHUFFLED_ITEMS = [item for item in Item]
TEST_KART_POSITIONS = [(),]
class Debugger:
    def __init__(self, kart_ui, on=False):
        self.on = on
        self.shuffler = None
        self.map = None
        self.warning = None
        self.kart_ui = kart_ui
        
        
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
            textSize(40)
            textAlign(CENTER, BOTTOM)
            text('bill get', width/4, 40)
            text('banana hit', width/4, height - 40)
            text('item use', 3*width/4, 40)
            text('random get', 3*width/4, height - 40)
    
    def mouse_pressed(self, mouse_x, mouse_y):
        if self.on:
            self.show_luigi_at(mouse_x, mouse_y)    
        if self.shuffler is not None:
            if 0 < mouse_x < width/2 and 0 < mouse_y < 200:
                self.kart_ui.on_picked_up_item(Item.BULLET_BILL)
                # self.shuffler.shuffle(Item.BULLET_BILL)
            elif 0 < mouse_x < width/2 and height - 200 < mouse_y < height:
                self.kart_ui.on_incoming_item(Item.BANANA)
                # self.warning.show(Item.BANANA)
            elif width/2 < mouse_x < width and 0 < mouse_y < 200:
                print("can use item", self.kart_ui.can_use_item())
                if self.kart_ui.can_use_item():
                    self.kart_ui.on_use_item()
                # self.shuffler.use_item()
            elif width/2 < mouse_x < 3*width/4 and height - 200 < mouse_y < height:
                item = SHUFFLED_ITEMS[int(random_uniform(0, len(SHUFFLED_ITEMS)))]
                self.kart_ui.on_picked_up_item(item)
                # self.shuffler.shuffle(item)
    
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
    
    def set_warning(self, warning):
        self.warning = warning
    
    def show_luigi_at(self, mouse_x, mouse_y):
        map_x = (mouse_x - self.map.origin_x) / self.map.scale_size
        map_y = (mouse_y - self.map.origin_y) / self.map.scale_size
        new_positions = self.map.kart_positions.copy()
        new_positions[4] = (map_x, map_y)
        # print(map_x, map_y)
        self.map.update(new_positions)
        
