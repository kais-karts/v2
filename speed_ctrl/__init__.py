import RPi.GPIO as GPIO
import time


# CONSTANTS

# pins
INC_PIN = 27
UD_PIN  = 22

# other
MINSLEEP = .001
NUMTAPS = 100
INITIALIZED = False
CURRENT_TAP = 0

def set_speed_multiplier(val: float, reset: bool = False) -> float:
    """
    Set the speed multiplier, e.g. how much of the pedal is applied to the actual motor speed controller.
    Speed should change with minimal jitter.
    Returns the attempted multiplier and raises exception if val out of bounds or not initalized
    Args:
        val (float): Value from 0.0 to 1.0, which multiplies the voltage of the pedal.
        reset (bool): Optional, defaults to False. Useful if you believe the returned speed multiplier
            to be inconsistent with the actual physical IC. Will restore the IC
            to a known point.
    """
    if val < 0 or val > 1:
        raise Exception(f"val {val} out of bounds, must be within [0:1]")
    if INITIALIZED == False:
        raise Exception("speed control IC not initialized")

    incs = round(val*NUMTAPS)
    if reset:
        reset_speed_control()
    diff = abs(incs - CURRENT_TAP)
    for _ in range(diff):
        if incs > CURRENT_TAP:
            increment()
        else:
            decrement()
    return incs/NUMTAPS

def reset_speed_control():
    """
    Decrements chip NUMTAPS - 1 times to guarentee starting at 0 tap of digital pot
    """
    for i in range(NUMTAPS - 1):
        decrement()
    

def init_speed_control():
    """
    Initializes speed control ic
    """
    global INITIALIZED
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(INC_PIN, GPIO.OUT)
    GPIO.setup(UD_PIN, GPIO.OUT)

    GPIO.output(INC_PIN, GPIO.HIGH)
    GPIO.output(UD_PIN, GPIO.LOW) # default decrement ig
    INITIALIZED = True

# util functions
def increment():
    """
    increments by 1
    """
    global CURRENT_TAP
    GPIO.output(UD_PIN, GPIO.HIGH)
    time.sleep(MINSLEEP)
    edgeTrigger()
    CURRENT_TAP = min(CURRENT_TAP + 1, NUMTAPS)

def decrement():
    """
    decrements by 1
    """
    global CURRENT_TAP
    GPIO.output(UD_PIN, GPIO.LOW)
    time.sleep(MINSLEEP)
    edgeTrigger()
    CURRENT_TAP = min(CURRENT_TAP - 1, 0)

def edgeTrigger():
    """
    triggers the INC line once
    """
    GPIO.output(INC_PIN, GPIO.HIGH)
    time.sleep(MINSLEEP)
    GPIO.output(INC_PIN, GPIO.LOW)
    time.sleep(MINSLEEP)

# this is ran upon import to force the initialization of the IC and start at a known state (multiplier is 0)
init_speed_control()
reset_speed_control()

if __name__ == "__main__":
    # can run module directly for testing purposes
    init_speed_control()
    reset_speed_control()
    val = 0
    while True:
        # test to measure IC voltage after attempted speed multiplier
        val = (val + .1) % 1
        print(f"attempted to set speed multiplier to {val} got {set_speed_multiplier(val)} instead")
        time.sleep(2)

        # test to see how many taps there actually are (we already got scammed once)
        # increment()
        # time.sleep(1)        
