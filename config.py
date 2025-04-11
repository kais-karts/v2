"""
Game configuration and constants (shared across all sub-systems)
"""

# == KART CONFIG ==
# Identifier (0..=7) for this Go-Kart. MUST be different on each physical kart!
KART_ID = 0
# Number of Go-Karts in the game
NUM_GO_KARTS = 6

assert 0 <= KART_ID < NUM_GO_KARTS


# == GPIO ASSIGNMENT ==
BUTTON_IN, BUTTON_OUT = 17, 27


# == SPEED CONTROL ==
BASE_MULTIPLIER = 0.5

ITEM_CHECKPOINTS = []
TRACK_PATH = []
START_LINE = ()