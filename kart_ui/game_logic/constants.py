''' Constants for the kart_ui module. '''

PORT = ""
KART_ID = 0
BASE_MULTIPLIER = 0.5

# item name: (speed_multiplier, duration, buff?)
ITEMS = {'banana': (0, 3, False), 'bomb': (0, 10, False), 'redShroom': (1, 5, True), 'goldShroom': (1, 10, True), 'redShell': (0, 5, False), 'blueShell': (0, 7, False), 'lightning': (0.25, 5, False), 'bulletBill': (1, 10, True)}
CHARACTERS = {0: 'mario', 1: 'bowser', 2: 'toad', 3: 'wario', 4: 'luigi', 5: 'waluigi'}
MAP_METERS_PER_PIXEL = 2