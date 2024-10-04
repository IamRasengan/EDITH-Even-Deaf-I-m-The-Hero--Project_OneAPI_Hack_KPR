import os
import cv2

# Directories for saving data and videos
DATA_DIR = 'Dataset'
VIDEO_DIR = 'Videos'

# Create main data directory and video directory if they don't exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

number_of_classes = 5
dataset_size = 200

# Use the appropriate camera index (try 0 if 2 doesn't work)
cap = cv2.VideoCapture(0)
# Check if camera was opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

for j in range(number_of_classes):
    # Create subdirectory for each class in DATA_DIR for images
    class_dir = os.path.join(DATA_DIR, str(j))
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)

    # Create subdirectory for each class in VIDEO_DIR for videos
    video_class_dir = os.path.join(VIDEO_DIR, str(j))
    if not os.path.exists(video_class_dir):
        os.makedirs(video_class_dir)

    print('Collecting data for class {}'.format(j))

    # Set up video writer for saving the video in the video folder
    video_path = os.path.join(video_class_dir, 'video_class_{}.avi'.format(j))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for video
    out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))  # VideoWriter object (20 fps, 640x480 resolution)

    # Wait for the user to press 'q' to start collecting data
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image from camera.")
            break

        # Show instructions to start data collection
        cv2.putText(frame, 'Class {}: Press "Q" to start collecting.'.format(j), (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('frame', frame)

        # Press 'q' to start collecting images for the current class
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image from camera.")
            break

        # Display the current image being collected
        cv2.putText(frame, 'Collecting {}/{}'.format(counter + 1, dataset_size), (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow('frame', frame)

        # Save the image to the appropriate class directory
        cv2.imwrite(os.path.join(class_dir, '{}.jpg'.format(counter)), frame)

        # Save video frames for the first 25 images
        if counter < 200:
            out.write(frame)  # Write frame to video file

        counter += 1

        # Wait for 1 millisecond for window to update, and allow 'q' to break the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    out.release()  # Release the video writer after saving 25 frames

cap.release()
cv2.destroyAllWindows()

