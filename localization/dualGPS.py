import time
import board
import busio
import serial
import adafruit_bno055
import adafruit_gps
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

# Setup I2C for BNO055
i2c = busio.I2C(board.SCL, board.SDA)
bno055 = adafruit_bno055.BNO055_I2C(i2c)

# Setup UART for GPS
ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=10)
ser2 = serial.Serial("/dev/serial1", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(ser, debug=False)
gps2 = adafruit_gps.GPS(ser2, debug=False)

# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps2.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command(b"PMTK220,500")
gps2.send_command(b"PMTK220,500")

def latlon_to_meters(lat, lon, lat0, lon0):
    R = 6378137  # Radius of the Earth in meters
    dlat = np.radians(lat - lat0)
    dlon = np.radians(lon - lon0)
    x = R * dlon * np.cos(np.radians(lat0))
    y = R * dlat
    return x, y

# Collect data for 1 minute
start_time = time.monotonic()
gps_data1 = []
gps_data2 = []

image = np.zeros((480, 640, 3), dtype=np.uint8)  # Dummy image for BNO055

while time.monotonic() - start_time < 60:
    gps.update()
    gps2.update()
    #draw gps points on the image
    if gps.has_fix:
        gps_data1.append((gps.latitude, gps.longitude))
        lat, lon = gps.latitude, gps.longitude
        x, y = latlon_to_meters(lat, lon, gps_data1[0][0], gps_data1[0][1])
        cv.circle(image, (int(x), int(y)), 5, (255, 0, 0), -1)  # Draw red circle for GPS2
    if gps2.has_fix:
        gps_data2.append((gps2.latitude, gps2.longitude))
        lat, lon = gps2.latitude, gps2.longitude
        x, y = latlon_to_meters(lat, lon, gps_data2[0][0], gps_data2[0][1])
        cv.circle(image, (x, y), 5, (0, 255, 0), -1)  # Draw green circle for GPS1
    cv.imshow("GPS Points", image)
    key = cv.waitKey(1)
    if key == 27:  # ESC key to exit
        break

# Save both gps data to a file
with open("gps_data1.txt", "w") as f:
    for lat, lon in gps_data1:
        f.write(f"{lat}, {lon}\n")

with open("gps_data2.txt", "w") as f:
    for lat, lon in gps_data2:
        f.write(f"{lat}, {lon}\n")
# Plot the collected GPS data
# if gps_data1:
#     lat0, lon0 = gps_data1[0]
#     meter_data = [latlon_to_meters(lat, lon, lat0, lon0) for lat, lon in gps_data]
#     x, y = zip(*meter_data)
#     plt.figure(figsize=(10, 10))
#     plt.scatter(x, y, c='blue', marker='o')
#     plt.title('GPS Coordinates in Meters')
#     plt.xlabel('X (meters)')
#     plt.ylabel('Y (meters)')
#     plt.grid(True)
#     plt.show()
# else:
#     print("No GPS data collected.")
