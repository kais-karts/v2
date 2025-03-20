from enum import Enum
from game_logic.constants import ITEMS
from p5 import *
from p5.core.image import PImage
from time import time
global width, height
class ShuffleState(Enum):
    NO_ITEM = 0
    SHUFFLING = 1
    WAITING = 2
    COUNTDOWN = 3

SHUFFLE_PERIOD = .1 #how long each item is displayed during shuffling in seconds
SHUFFLE_DURATION = 2 #how long the shuffling lasts in seconds
IMAGE_SIZE = 1024 - 200

SHUFFLED_ITEMS = list(ITEMS.keys())
class Shuffler:
    def __init__(self, debugger):
        self.debugger = debugger
        # Load all item images
        self.images = {item: loadImage(f"kart_ui/images/items/{item}.png") for item in ITEMS}
        self.images['no-item'] = loadImage("kart_ui/images/items/no-item.png")

        self.state = ShuffleState.NO_ITEM
        self.available_item = 'no-item'
        self.displayed_item = 'no-item'
        # Shuffle
        self.shuffle_start = 0
        self.last_switch = 0
        self.shuffle_index = 0
        
        # Countdown
        self.countdown_start = 0
        self.countdown_duration = 0
        # image_mode('center')

    def draw(self):
        if self.state == ShuffleState.NO_ITEM:
            # print("no item")
            self.place_item(self.images['no-item'])
        elif self.state == ShuffleState.SHUFFLING:
            if time() - self.last_switch > SHUFFLE_PERIOD:
                self.displayed_item = SHUFFLED_ITEMS[self.shuffle_index]
                self.shuffle_index += 1
                if self.shuffle_index >= len(SHUFFLED_ITEMS):
                    self.shuffle_index = 0
                self.last_switch = time()
            self.place_item(self.images[self.displayed_item])
            
            if time() - self.shuffle_start > SHUFFLE_DURATION:
                self.place_item(self.images[self.available_item]) 
                self.state = ShuffleState.WAITING
                
        elif self.state == ShuffleState.WAITING:
            self.place_item(self.images[self.available_item])
        elif self.state == ShuffleState.COUNTDOWN:
            # print("countdown", self.countdown_duration)
            elapsed_time = time() - self.countdown_start
            # Draw countdown arc
            push_matrix()
            no_fill()
            stroke(102, 161, 255)  # Black outline
            stroke_weight(40)

            arc_progress = 3*PI/2 + 2*PI * (elapsed_time / self.countdown_duration)
            arc((3*width/4, height/2), 950, 950, arc_progress, 3*PI/2 + 2*PI)
            pop_matrix()
            self.place_item(self.images[self.available_item])
            
            if elapsed_time > self.countdown_duration:
                self.state = ShuffleState.NO_ITEM
            
    
    
    def shuffle(self, item: str):
        if item not in ITEMS:
            raise ValueError(f"Invalid item: {item}")
        
        self.shuffle_start = time()
        self.available_item = item       
        self.state = ShuffleState.SHUFFLING
    
    def place_item(self, img):
        global width, height
        
        img_width = img.width()
        img_height = img.height()
        
        scale_size = min(IMAGE_SIZE / img_width, IMAGE_SIZE / img_height)
        push_matrix()
        scale(scale_size)
        scaled_width = width / scale_size
        scaled_height = height / scale_size

        img_x = 3*scaled_width/4
        img_y = scaled_height/2
        

        image(img, img_x-img_width/2, img_y-img_height/2)
        self.debugger.show_image_outline(img_x, img_y, img_width, img_height)
        pop_matrix()
    
    def use_item(self):
        print("use item")
        if self.state == ShuffleState.WAITING:
            if ITEMS[self.available_item][2]: # buff item
                self.countdown_start = time()
                self.countdown_duration = ITEMS[self.available_item][1]
                self.state = ShuffleState.COUNTDOWN 
            else: # debuff item
                self.state = ShuffleState.NO_ITEM
    
        
        
        
