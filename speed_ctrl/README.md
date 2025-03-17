# Speed Ctrl
## Description
This is the hardware (+ minimal software) to variably divide the voltage going from the Go-Kart's pedal to the motor speed controller.

## Pins
I will claim GPIO pins here

## Development Notes
3/16/2025
Speed controller breakouts arrived, watching [tutorial](https://www.youtube.com/watch?v=Zy50ZGSJLqM) introduces concern of potential amplifier needed to boost power of signal (10mW max power output of X9103). Should have some fail-fast protections in whatever I write (cause error whenever trying to be used when uninitialized, etc). Also will need to make a setup that is persistent across reboots -- no one wants to have to recalibrate cause the program power cycled (aka write to file before returning from function, read state from file)