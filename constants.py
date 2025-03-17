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