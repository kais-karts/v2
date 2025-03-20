from p5 import *
from game_logic.constants import CHARACTERS
MAP_WIDTH = 1024
MAP_VERTICAL_OFFSET = 100
global mouse_x, mouse_y
class Map:
    def __init__(self, debugger):
        self.debugger = debugger
        self.map_image = loadImage("kart_ui/images/map.png")
        self.kart_positions = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
        self.kart_images = {id: loadImage(f"kart_ui/images/heads/{CHARACTERS[id]}.png") for id in CHARACTERS}
        
        self.map_width = self.map_image.width()
        self.map_height = self.map_image.height()
        self.scale_size = MAP_WIDTH/self.map_width
        self.origin_x = None
        self.origin_y = None
        
    def draw(self):
        global width, height
        img_width = self.map_width
        img_height = self.map_height
        scale_size = MAP_WIDTH/img_width
        push_matrix()
        scale(self.scale_size)
        scaled_width = width / self.scale_size
        scaled_height = height / self.scale_size
        
        img_x = scaled_width/4
        img_y = scaled_height/2 - MAP_VERTICAL_OFFSET
        image(self.map_image, img_x-img_width/2, img_y-img_height/2)
        pop_matrix()
        
        push_matrix()
        translate(width/4, height/2 - MAP_VERTICAL_OFFSET)
        for kart_id, position in self.kart_positions.items():
            x, y = position
            img = self.kart_images[kart_id]
            image(img, x-img.width()/2, y-img.height()/2)
        pop_matrix()
    def update(self, kart_positions: dict):
        self.kart_positions = kart_positions
    
        
        
        
    
    
        
        
    
    # def set_position(self, x, y):
