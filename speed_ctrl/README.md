# Speed Ctrl
## Description
This is the hardware (+ minimal software) to variably divide the voltage going from the Go-Kart's pedal to the motor speed controller.

## Setup
### Hardware
Connect:
GPIO 17 -> CS\
GPIO 27 -> INC\
GPIO 22 -> UD

### Software
Just import the module and call set_speed_multiplier() whenever you wish to change the multiplier. **Note multiplier will start at 0 upon initialization as of now**

## Development Notes
3/19/2025 \
Proof of concept works, whats left to do:
- make it work without needing to reset every call (reset should just be last resort when software not in sync with hardware)
- make number of taps a parameter (dont hard code 100)
- make the proof of concept circuit have buffered input and output with TL082 (input from external power supply, output is wiper to be probed)
- label lines on proof of concept

3/16/2025 \
Im thinking Vh/Rh, VCC  connect to 5v. Vl/Rl, VSS connected to GND. Also all other pins defined in constants for now but just GPIOs.

Speed controller breakouts arrived, watching [tutorial](https://www.youtube.com/watch?v=Zy50ZGSJLqM) introduces concern of potential amplifier needed to boost power of signal (10mW max power output of X9103). Should have some fail-fast protections in whatever I write (cause error whenever trying to be used when uninitialized, etc). Also will need to make a setup that is persistent across reboots -- no one wants to have to recalibrate cause the program power cycled (aka write to file before returning from function, read state from file)
