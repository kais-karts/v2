import time
import board
import busio
import serial
import adafruit_gps
import numpy as np
import cv2 as cv

# Setup UART for GPS devices
ser1 = serial.Serial("/dev/serial0", baudrate=9600, timeout=10)
ser2 = serial.Serial("/dev/serial1", baudrate=9600, timeout=10)
gps1 = adafruit_gps.GPS(ser1, debug=False)
gps2 = adafruit_gps.GPS(ser2, debug=False)

# Configure GPS modules
def configure_gps(gps):
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    gps.send_command(b"PMTK220,1000")

configure_gps(gps1)
configure_gps(gps2)

# Coordinate conversion
def latlon_to_meters(lat, lon, lat0, lon0):
    R = 6378137
    dlat = np.radians(lat - lat0)
    dlon = np.radians(lon - lon0)
    x = R * dlon * np.cos(np.radians(lat0))
    y = R * dlat
    return x, y

# Initialization
gps_data1 = []
gps_data2 = []
image = np.zeros((800, 800, 3), dtype=np.uint8)
origin_set = False
lat0 = lon0 = None

# Coordinate transform to image space
def meters_to_img_coords(x, y, scale=1.0):
    cx, cy = 400, 400  # image center
    return int(cx + x * scale), int(cy - y * scale)

# Collect GPS data for 60 seconds
print("Collecting GPS data...")
start = time.monotonic()
while time.monotonic() - start < 60:
    gps1.update()
    gps2.update()

    if gps1.has_fix:
        lat1, lon1 = gps1.latitude, gps1.longitude
        if not origin_set and lat1 is not None and lon1 is not None:
            lat0, lon0 = lat1, lon1
            origin_set = True
        if origin_set:
            x1, y1 = latlon_to_meters(lat1, lon1, lat0, lon0)
            img_x1, img_y1 = meters_to_img_coords(x1, y1, scale=0.5)
            cv.circle(image, (img_x1, img_y1), 4, (0, 0, 255), -1)  # Red for GPS1
            gps_data1.append((lat1, lon1))

    if gps2.has_fix:
        lat2, lon2 = gps2.latitude, gps2.longitude
        if origin_set and lat2 is not None and lon2 is not None:
            x2, y2 = latlon_to_meters(lat2, lon2, lat0, lon0)
            img_x2, img_y2 = meters_to_img_coords(x2, y2, scale=0.5)
            cv.circle(image, (img_x2, img_y2), 4, (0, 255, 0), -1)  # Green for GPS2
            gps_data2.append((lat2, lon2))

    cv.imshow("Live GPS Tracking", image)
    if cv.waitKey(1) == 27:  # ESC to break
        break

cv.destroyAllWindows()

# Save collected data
with open("gps_data1.txt", "w") as f:
    for lat, lon in gps_data1:
        f.write(f"{lat}, {lon}\n")

with open("gps_data2.txt", "w") as f:
    for lat, lon in gps_data2:
        f.write(f"{lat}, {lon}\n")

print("Data collection complete. Plotting saved data...")

# === Displaying Final Result ===
def read_gps_data(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [tuple(map(float, line.strip().split(','))) for line in lines]

def convert_gps_to_meters(gps_data, lat0, lon0):
    return [latlon_to_meters(lat, lon, lat0, lon0) for lat, lon in gps_data]

# Load and convert data
gps_data1 = read_gps_data("gps_data1.txt")
gps_data2 = read_gps_data("gps_data2.txt")

if gps_data1:
    lat0, lon0 = gps_data1[0]

image = np.zeros((800, 800, 3), dtype=np.uint8)

def draw_gps_data_on_image(image, gps_data, color):
    meter_data = convert_gps_to_meters(gps_data, lat0, lon0)
    for x, y in meter_data:
        img_x, img_y = meters_to_img_coords(x, y, scale=0.5)
        cv.circle(image, (img_x, img_y), 4, color, -1)

draw_gps_data_on_image(image, gps_data1, (0, 0, 255))  # Red
draw_gps_data_on_image(image, gps_data2, (0, 255, 0))  # Green

cv.imshow("Final GPS Paths", image)
cv.waitKey(0)
cv.destroyAllWindows()
