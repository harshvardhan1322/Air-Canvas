import numpy as np
import cv2
from collections import deque

# Callback function for trackbars (does nothing)
def on_trackbar_change(x):
    pass

# Create a window for color settings
cv2.namedWindow("Color Settings")
cv2.createTrackbar("Upper Hue", "Color Settings", 153, 180, on_trackbar_change)
cv2.createTrackbar("Upper Saturation", "Color Settings", 255, 255, on_trackbar_change)
cv2.createTrackbar("Upper Value", "Color Settings", 255, 255, on_trackbar_change)
cv2.createTrackbar("Lower Hue", "Color Settings", 64, 180, on_trackbar_change)
cv2.createTrackbar("Lower Saturation", "Color Settings", 72, 255, on_trackbar_change)
cv2.createTrackbar("Lower Value", "Color Settings", 49, 255, on_trackbar_change)

# Initialize deque structures to store points for each color
blue_points = [deque(maxlen=1024)]
green_points = [deque(maxlen=1024)]
red_points = [deque(maxlen=1024)]
yellow_points = [deque(maxlen=1024)]

# Initialize indices to track the points in the deque
blue_index, green_index, red_index, yellow_index = 0, 0, 0, 0

# Kernel for morphological operations
kernel = np.ones((5, 5), np.uint8)

# Colors for drawing
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
current_color_index = 0

# Create a blank white canvas
canvas = np.ones((471, 636, 3), dtype=np.uint8) * 255
cv2.namedWindow("Canvas")

# Access the webcam
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Flip the frame for a mirror effect
    frame = cv2.flip(frame, 1)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Retrieve HSV range values from trackbars
    upper_hue = cv2.getTrackbarPos("Upper Hue", "Color Settings")
    upper_saturation = cv2.getTrackbarPos("Upper Saturation", "Color Settings")
    upper_value = cv2.getTrackbarPos("Upper Value", "Color Settings")
    lower_hue = cv2.getTrackbarPos("Lower Hue", "Color Settings")
    lower_saturation = cv2.getTrackbarPos("Lower Saturation", "Color Settings")
    lower_value = cv2.getTrackbarPos("Lower Value", "Color Settings")

    upper_hsv = np.array([upper_hue, upper_saturation, upper_value])
    lower_hsv = np.array([lower_hue, lower_saturation, lower_value])

    # Add color selection buttons to the frame
    cv2.rectangle(frame, (40, 1), (140, 65), (122, 122, 122), -1)
    cv2.rectangle(frame, (160, 1), (255, 65), colors[0], -1)
    cv2.rectangle(frame, (275, 1), (370, 65), colors[1], -1)
    cv2.rectangle(frame, (390, 1), (485, 65), colors[2], -1)
    cv2.rectangle(frame, (505, 1), (600, 65), colors[3], -1)

    cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2)

    # Create a mask to detect the pointer
    mask = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None

    if contours:
        # Get the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
        M = cv2.moments(largest_contour)

        if M["m00"] != 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if center[1] <= 65:
                if 40 <= center[0] <= 140:
                    blue_points = [deque(maxlen=1024)]
                    green_points = [deque(maxlen=1024)]
                    red_points = [deque(maxlen=1024)]
                    yellow_points = [deque(maxlen=1024)]
                    blue_index, green_index, red_index, yellow_index = 0, 0, 0, 0
                    canvas[67:, :, :] = 255
                elif 160 <= center[0] <= 255:
                    current_color_index = 0
                elif 275 <= center[0] <= 370:
                    current_color_index = 1
                elif 390 <= center[0] <= 485:
                    current_color_index = 2
                elif 505 <= center[0] <= 600:
                    current_color_index = 3
            else:
                if current_color_index == 0:
                    blue_points[blue_index].appendleft(center)
                elif current_color_index == 1:
                    green_points[green_index].appendleft(center)
                elif current_color_index == 2:
                    red_points[red_index].appendleft(center)
                elif current_color_index == 3:
                    yellow_points[yellow_index].appendleft(center)

    else:
        blue_points.append(deque(maxlen=1024))
        blue_index += 1
        green_points.append(deque(maxlen=1024))
        green_index += 1
        red_points.append(deque(maxlen=1024))
        red_index += 1
        yellow_points.append(deque(maxlen=1024))
        yellow_index += 1

    # Draw the points on the canvas and frame
    point_lists = [blue_points, green_points, red_points, yellow_points]
    for i, points in enumerate(point_lists):
        for j in range(len(points)):
            for k in range(1, len(points[j])):
                if points[j][k - 1] is None or points[j][k] is None:
                    continue
                cv2.line(frame, points[j][k - 1], points[j][k], colors[i], 2)
                cv2.line(canvas, points[j][k - 1], points[j][k], colors[i], 2)

    # Display the frames
    cv2.imshow("Tracking", frame)
    cv2.imshow("Canvas", canvas)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
