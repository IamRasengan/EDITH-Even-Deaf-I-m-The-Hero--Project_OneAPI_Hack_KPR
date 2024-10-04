import os
import pickle
import mediapipe as mp
import cv2


# Disable oneDNN optimizations and suppress TensorFlow logging
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disables oneDNN warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'   # Only shows errors, suppress INFO and WARNING

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands=mp_hands.Hands(static_image_mode=True,min_detection_confidence=0.3)

Data_Dir=r'Dataset'
data = []
labels = []

for dir in os.listdir(Data_Dir):
    for img_path in os.listdir(os.path.join(Data_Dir,dir)):
        data_aux = []

        img=cv2.imread(os.path.join(Data_Dir,dir,img_path))
        img_rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        results=hands.process(img_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x)
                    data_aux.append(y)
            data.append(data_aux)
            labels.append(dir)

f = open('data_new.pickle', 'wb')
pickle.dump({'data': data, 'labels': labels}, f)
f.close()