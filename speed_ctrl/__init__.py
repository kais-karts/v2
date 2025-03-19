import RPi.GPIO as GPIO
import time


# CONSTANTS

# pins
CS_PIN  = 17
INC_PIN = 27
UD_PIN  = 22

# other
INITIALIZED = False

# external functions
def set_speed_multiplier(val: float) -> float:
    """
    Set the speed multiplier, e.g. how much of the pedal is applied to the actual motor speed controller.
    Returns the attempted multiplier
    Throws err if val out of bounds or not initalized
    Args:
        val (float): Value from 0.0 to 1.0, which multiplies the voltage of the pedal.
    """
    if val < 0 or val > 1:
        raise Exception(f"val {val} out of bounds, must be within [0:1]")
    if INITIALIZED == False:
        raise Exception("speed control IC not initialized")

    val = round(val, 2)
    reset_speed_control()
    incs = int(val*100)
    print("incs, ", incs)
    for i in range(incs):
        increment()
    
    return val

def reset_speed_control():
    """
    Decrements chip 99 times to guarentee starting at 0 tap of digital pot
    """
    for i in range(99):
        decrement()

def init_speed_control():
    """
    Initializes speed control ic
    """
    global INITIALIZED
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(CS_PIN, GPIO.OUT)
    GPIO.setup(INC_PIN, GPIO.OUT)
    GPIO.setup(UD_PIN, GPIO.OUT)

    GPIO.output(INC_PIN, GPIO.HIGH)
    GPIO.output(CS_PIN, GPIO.LOW)
    GPIO.output(UD_PIN, GPIO.LOW) # default decrement ig
    INITIALIZED = True

# util functions
def increment():
    """
    increments by 1
    """
    GPIO.output(UD_PIN, GPIO.HIGH)
    time.sleep(.001)
    edgeTrigger()

def decrement():
    """
    decrements by 1
    """
    GPIO.output(UD_PIN, GPIO.LOW)
    time.sleep(.001)
    edgeTrigger()

def edgeTrigger():
    """
    triggers the INC line once
    """
    GPIO.output(INC_PIN, GPIO.HIGH)
    time.sleep(.001)
    GPIO.output(INC_PIN, GPIO.LOW)
    time.sleep(.001)

# this is ran upon import to force the initialization of the IC and start at a known state (multiplier is 0)
init_speed_control()
reset_speed_control()

if __name__ == "__main__":
    # can run module directly for testing purposes
    # currently this is useful for determining how many actual taps are in the IC lmao (amazon purchase was a scam)
    init_speed_control()
    reset_speed_control()
    val = 0
    while True:
        # val = (val + .1) % 1
        # val = .05
        # print(f"attempted to set speed multiplier to {val} got {set_speed_multiplier(val)} instead")
        #
        increment()
        print(f"increment {val}")
        val += 1
        time.sleep(2)
