import cv2

# Define a video capture object
vid = cv2.VideoCapture(2)

while True:
    # Capture the video frame by frame
    ret, frame = vid.read()

    # Flip the frame horizontally
    flipped_frame = cv2.flip(frame, 0)

    # Display the resulting frame
    cv2.imshow('frame', flipped_frame)

    # The 'q' button is set as the quitting button
    # You may use any desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop, release the capture object
vid.release()

# Destroy all the windows
cv2.destroyAllWindows()
