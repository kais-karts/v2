import time
import board
import busio
import serial
import adafruit_bno055
import adafruit_gps
import matplotlib.pyplot as plt

# Setup I2C for BNO055
i2c = busio.I2C(board.SCL, board.SDA)
bno055 = adafruit_bno055.BNO055_I2C(i2c)

# Setup UART for GPS
ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(ser, debug=False)

# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command(b"PMTK220,1000")

# Collect data for 1 minute
start_time = time.monotonic()
gps_data = []

while time.monotonic() - start_time < 60:
    gps.update()
    if gps.has_fix:
        gps_data.append((gps.latitude, gps.longitude))
    time.sleep(1)

# Plot the collected GPS data
if gps_data:
    latitudes, longitudes = zip(*gps_data)
    plt.figure(figsize=(10, 10))
    plt.scatter(longitudes, latitudes, c='blue', marker='o')
    plt.title('GPS Coordinates')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.show()
else:
    print("No GPS data collected.")
