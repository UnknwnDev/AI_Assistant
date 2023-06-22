import cv2
from PIL import Image
import numpy as np
from transformers import pipeline
import threading

# Load the object detection pipeline
object_detection = pipeline("object-detection", model="hustvl/yolos-tiny")

# OpenCV settings
camera = cv2.VideoCapture(2)  # Use the default camera (0)
frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create a lock for thread synchronization
lock = threading.Lock()

# Initialize variables for storing the latest frame and results
latest_frame = None
latest_results = None

# Function to perform object detection on the latest frame
def detect_objects():
    global latest_frame, latest_results

    while True:
        # Acquire the lock to access the latest frame
        with lock:
            if latest_frame is None:
                continue
            frame = latest_frame.copy()

        # Convert OpenCV BGR image to PIL RGB image
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Perform object detection
        results = object_detection(image)

        # Acquire the lock to update the latest results
        with lock:
            latest_results = results

# Start the object detection thread
detection_thread = threading.Thread(target=detect_objects)
detection_thread.daemon = True
detection_thread.start()

while True:
    # Read frame from the camera
    ret, frame = camera.read()

    # Flip the frame vertically
    frame = cv2.flip(frame, 0)

    # Acquire the lock to update the latest frame
    with lock:
        latest_frame = frame.copy()

    # Display the frame with bounding boxes
    with lock:
        if latest_results is not None:
            for result in latest_results:
                label = result["label"]
                bbox = result["box"]
                x, y, w, h = [int(coord) for coord in bbox.values()]

                # Ensure the width and height are positive values
                w = max(0, w)
                h = max(0, h)

                # Calculate the right-bottom corner coordinates
                x2, y2 = x + w, y + h

                # Draw the bounding box on the frame
                cv2.rectangle(frame, (x, y), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the frame with bounding boxes
    cv2.imshow("Object Detection", frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
camera.release()
cv2.destroyAllWindows()
