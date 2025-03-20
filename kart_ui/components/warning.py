from enum import Enum
from game_logic.constants import ITEMS
from p5 import *
from p5.core.image import PImage
from time import time
global width, height

FLASH_PERIOD = 0.1

class Warning:
    def __init__(self):
        self.show_warning = False
        self.show_image = False
        self.show_warning_start = 0
        self.show_warning_duration = 0
        self.show_image_start = 0 

    def show(self, item: str):
        self.show_warning = True
        self.show_warning_start = time()
        self.show_warning_duration = ITEMS[item][1]
        self.show_image = True
        self.show_image_start = time()
    
    def draw(self):
        if self.show_warning:
            text(self.warning, width/2, height/2)
