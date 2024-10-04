import os
import pickle
import cv2
import mediapipe as mp
import numpy as np
import random



# Load the model for sign language to text (mode 1)
model_dict = pickle.load(open(r'model.p', 'rb'))
model = model_dict['model']

# Mediapipe setup for hand detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.5)

# Gesture labels (with added "Pause" and "Clear")
labels_dict = {0: 'Namaste', 1: 'Bye-Bye', 2:'Hello',3:'Sorry',4:'Peace'}

# Buffer to store the detected letters
letter_buffer = []

# Directory containing images for each class (mode 0)
Data_Dir = r'Dataset'



# Function to handle text input (mode 0) and show a corresponding random image
def text_to_image():
    # Ask the user for input (gesture command)
    command = input("Enter a command (A, B, C): ").strip().lower()

    # Map the input command to the corresponding label
    label_key = [key for key, value in labels_dict.items() if value.lower() == command]
    
    if label_key:
        # Get the label index corresponding to the command
        label = label_key[0]
        # Fetch a random image from the respective folder
        image_path = get_random_image_from_text(labels_dict[label])

        if image_path:
            # Load the image using OpenCV
            img = cv2.imread(image_path)
            if img is None:
                print("Error: Couldn't load the image.")
                return

            # Display the random image
            cv2.imshow('Random Gesture Image', img)
            cv2.waitKey(0)  # Wait for a key press before closing the window
            cv2.destroyAllWindows()
        else:
            print("No images found for this label.")
    else:
        print("Invalid command entered.")

# Function to randomly select an image from a specified class folder
def get_random_image_from_text(input_text):
    folder = get_folder_from_text(input_text)
    if folder:
        class_dir = os.path.join(Data_Dir, folder)
        if os.path.exists(class_dir):
            image_files = [f for f in os.listdir(class_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
            if image_files:
                random_image = random.choice(image_files)
                return os.path.join(class_dir, random_image)
            else:
                print(f"No images found in folder {folder}")
        else:
            print(f"Folder {folder} does not exist.")
    else:
        print(f"No matching folder found for input: '{input_text}'")
    return None

# Function to map text input (like 'A', 'B', 'C') to the corresponding folder number
def get_folder_from_text(input_text):
    for folder_num, label in labels_dict.items():
        if label.lower() == input_text.lower():
            return str(folder_num)
    return None

# Function to handle sign language detection (mode 1) and convert it to text with pause functionality
def sign_language_to_text():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    global letter_buffer  # Ensure we can modify the buffer

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image from camera.")
            break

        data_aux = []
        x_ = []
        y_ = []
        H, W, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x)
                    data_aux.append(y)
                    x_.append(x)
                    y_.append(y)
            x1 = int(min(x_) * W)
            y1 = int(min(y_) * H)

            x2 = int(max(x_) * W)
            y2 = int(max(y_) * H) 

            if len(data_aux) == 42:
                prediction = model.predict([np.asarray(data_aux)])
                predicted_character = labels_dict[int(prediction[0])]  
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                cv2.LINE_AA)
        cv2.imshow('Sign Language Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Main program logic

mode = input("Enter 1 for sign language to text or 0 for text to sign language (image): ").strip()

if mode == '1':
    sign_language_to_text()
elif mode == '0':
    text_to_image()
else:
    print("Invalid mode selected. Please enter 1 or 0.")