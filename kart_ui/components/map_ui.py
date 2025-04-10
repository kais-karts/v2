from p5 import *
from kart_ui.characters import CHARACTERS
from kart_ui.mystery_boxes import MYSTERY_BOXES

MAP_WIDTH = 1024
MAP_VERTICAL_OFFSET = 100
KART_WIDTH = 100
MYSTERY_BOX_WIDTH = 50

global mouse_x, mouse_y
class MapUI:
    def __init__(self, debugger):
        self.debugger = debugger
        self.map_image = loadImage("kart_ui/images/map.png")
        self.kart_positions = {0: (0, 0), 1: (1080, 0), 2: (1080, 834), 3: (0, 834)}
        self.kart_images = {id: loadImage(f"kart_ui/images/heads/{CHARACTERS[id]}.png") for id in CHARACTERS}
        
        self.map_width = self.map_image.width()
        self.map_height = self.map_image.height()
        self.scale_size = MAP_WIDTH/self.map_width
        self.origin_x = width / 4 - (self.map_width/2 * self.scale_size) 
        self.origin_y = height / 2 - (MAP_VERTICAL_OFFSET * self.scale_size) - (self.map_height/2 * self.scale_size) 
        
        self.mystery_box_image = loadImage("kart_ui/images/mystery_box.webp")
        
    def draw(self):
        global width, height
        # draw map
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
        self.debugger.show_image_outline(img_x, img_y, img_width, img_height, 'center')
        pop_matrix()
        
        # draw karts
        for kart_id, position in self.kart_positions.items():
            img = self.kart_images[kart_id]
            map_x, map_y = position
            self.place_on_map(img, map_x, map_y, KART_WIDTH)
        # draw mystery boxes
        for box in MYSTERY_BOXES:
            self.place_on_map(self.mystery_box_image, box[0], box[1], MYSTERY_BOX_WIDTH)
        
    def update(self, kart_positions: dict):
        self.kart_positions = kart_positions
    
    def place_on_map(self, img, map_x, map_y, target_width):
        image_scale_size = target_width/img.width()
        push_matrix()
        scale(image_scale_size)
        
        if map_x > self.map_width:
            map_x = self.map_width
        if map_y > self.map_height:
            map_y = self.map_height
        if map_x < 0:
            map_x = 0
        if map_y < 0:
            map_y = 0
            
        x = self.origin_x + (map_x * self.scale_size) # get global x
        y = self.origin_y + (map_y * self.scale_size) # get global y
        
        x = x / image_scale_size # get matrix x
        y = y / image_scale_size # get matrix y
        image(img, x-img.width()/2, y-img.height()/2)
        self.debugger.show_image_outline(x, y, img.width(), img.height(), 'center')
        pop_matrix()
        
    
        
        
        
    
    
        
        
    
    # def set_position(self, x, y):
