from enum import Enum
from game_logic.item import Item
from p5 import *
from p5.core.image import PImage
from time import time
global width, height

IMAGE_SIZE=900

FLASH_PERIOD = 0.15

class WarningState(Enum):
    NO_WARNING = 0
    IMAGE_ON = 1
    IMAGE_OFF = 2

class Warning:
    def __init__(self, debugger):
        self.debugger = debugger
        self.state = WarningState.NO_WARNING
        self.warning_start = 0
        self.show_warning_duration = 0
        self.flash_start = 0 
        self.image = None

    def show(self, item: Item):
        print("show warning")
        self.warning_start = time()
        self.show_warning_duration = item.duration
        self.flash_start = time()
        self.image = loadImage(f"kart_ui/images/items/{item.file_name}.png")
        self.state = WarningState.IMAGE_ON
    
    def draw(self):
        global FLASH_PERIOD
        # print(self.state)
        if self.state == WarningState.IMAGE_ON:
            background(255, 0, 0)
            
            self.place_item(self.image)
            
            if time() - self.warning_start > self.show_warning_duration:
                self.state = WarningState.NO_WARNING
            elif time() - self.flash_start > FLASH_PERIOD:
                self.flash_start = time()
                self.state = WarningState.IMAGE_OFF
                
        elif self.state == WarningState.IMAGE_OFF:
            # background(255, 0, 0)
            
            if time() - self.warning_start > self.show_warning_duration:
                self.state = WarningState.NO_WARNING
            elif time() - self.flash_start > FLASH_PERIOD:
                self.flash_start = time()
                self.state = WarningState.IMAGE_ON
    
    def place_item(self, img):
        global width, height
        
        img_width = img.width()
        img_height = img.height()
        
        scale_size = min(IMAGE_SIZE / img_width, IMAGE_SIZE / img_height)
        push_matrix()
        scale(scale_size)
        scaled_width = width / scale_size
        scaled_height = height / scale_size

        img_x = scaled_width/2
        img_y = scaled_height/2
        

        image(img, img_x-img_width/2, img_y-img_height/2)
        self.debugger.show_image_outline(img_x, img_y, img_width, img_height)
        pop_matrix()
            
