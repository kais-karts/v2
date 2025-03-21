import time
import board
import busio
import serial
import adafruit_bno055
import adafruit_gps
import numpy as np
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

def latlon_to_meters(lat, lon, lat0, lon0):
    R = 6378137  # Radius of the Earth in meters
    dlat = np.radians(lat - lat0)
    dlon = np.radians(lon - lon0)
    a = np.sin(dlat / 2) ** 2 + np.cos(np.radians(lat0)) * np.cos(np.radians(lat)) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    x = distance * np.cos(np.radians(lat))
    y = distance * np.sin(np.radians(lat))
    return x, y

# Plot the collected GPS data
if gps_data:
    lat0, lon0 = gps_data[0]
    meter_data = [latlon_to_meters(lat, lon, lat0, lon0) for lat, lon in gps_data]
    x, y = zip(*meter_data)
    plt.figure(figsize=(10, 10))
    plt.scatter(x, y, c='blue', marker='o')
    plt.title('GPS Coordinates in Meters')
    plt.xlabel('X (meters)')
    plt.ylabel('Y (meters)')
    plt.grid(True)
    plt.show()
else:
    print("No GPS data collected.")
