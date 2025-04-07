import cv2 as cv
import numpy as np
import time

# read from gps_data.txt in form f"{lat}, {lon}\n"
def read_gps_data(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    gps_data = []
    for line in lines:
        lat, lon = map(float, line.strip().split(','))
        gps_data.append((lat, lon))
    return gps_data

def latlon_to_meters(lat, lon, lat0, lon0):
    R = 6378137  # Radius of the Earth in meters
    dlat = np.radians(lat - lat0)
    dlon = np.radians(lon - lon0)
    x = R * dlon * np.cos(np.radians(lat0))
    y = R * dlat
    return x, y

# convert gps data to meters
def convert_gps_to_meters(gps_data):
    lat0, lon0 = gps_data[0]
    meters_data = []
    for lat, lon in gps_data:
        x, y = latlon_to_meters(lat, lon, lat0, lon0)
        meters_data.append((x, y))
    return meters_data

# display images using opencv as different colored dots being drawn on the image
def draw_gps_data_on_image(image, gps_data, color):
    for x, y in gps_data:
        cv.circle(image, (int(x), int(y)), 5, color, -1)

if __name__ == "__main__":
    # Load the image
    image = np.zeros((600, 800, 3), dtype=np.uint8)  # Create a blank image for demonstration

    # Initial GPS data
    gps_data1 = convert_gps_to_meters(read_gps_data('gps_data1.txt'))
    gps_data2 = convert_gps_to_meters(read_gps_data('gps_data2.txt'))

    # Draw and save live updates
    while True:
        # Clear the image
        image = np.zeros((600, 800, 3), dtype=np.uint8)

        # Read and convert GPS data
        gps_data1 = convert_gps_to_meters(read_gps_data('gps_data1.txt'))
        gps_data2 = convert_gps_to_meters(read_gps_data('gps_data2.txt'))

        # Draw the GPS data on the image
        draw_gps_data_on_image(image, gps_data1, (255, 0, 0))  # Red for gps_data1
        draw_gps_data_on_image(image, gps_data2, (0, 255, 0))  # Green for gps_data2

        # Save the image to a file
        cv.imwrite('live_gps_data.png', image)

        # Show the image
        cv.imshow('GPS Data', image)

        # Break the loop if 'q' is pressed
        if cv.waitKey(1000) & 0xFF == ord('q'):  # Wait for 1 second between updates
            break

    cv.destroyAllWindows()
