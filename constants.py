''' Constants for the kart_ui module. '''

PORT = "/dev/tty.usbmodem101"
KART_ID = 0
BASE_MULTIPLIER = 0.5
NUM_GO_KARTS = 6

# item name: (speed_multiplier, duration)
ITEMS = {
    "banana": (0.3),
    "bomb": (0, 10),
    "redShroom": (1, 5),
    "goldShroom": (1, 10),
    "redShell": (0, 5),
    "blueShell": (0, 7),
    "lightning": (0.25, 5),
    "bulletBill": (1, 10),
}

ITEM_NAMES = list(ITEMS.keys())

ITEM_WEIGHTS = [
    [30, 20, 20, 0, 0, 0],    # Banana
    [0, 0, 10, 15, 15, 0],    # Bomb
    [30, 25, 50, 30, 10, 0],  # redShroom
    [0, 0, 0, 10, 50, 50],    # goldShroom
    [0, 30, 30, 20, 10, 0],   # redShell
    [0, 0, 10, 20, 10, 0],    # blueShell
    [0, 0, 0, 5, 10, 10],     # lightning
    [0, 0, 0, 0, 0, 50],      # bulletBill
]