from flask import Flask, request, jsonify
import pickle
import numpy as np
import cv2
import mediapipe as mp
import base64
import io
from PIL import Image

from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # Add specific CORS configuration here

# Load the pre-trained model
model_dict = pickle.load(open('model.p', 'rb'))
model = model_dict['model']

# Mediapipe setup for hand detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.7)

labels_dict = {0: 'Indian', 1: 'Hello', 2: 'Bye-Bye', 3: 'I am', 4: 'Teacher', 5: 'Thank you', 6: 'Welcome', 7: 'Sorry', 8: 'Namaste', 9: 'Name', 10: 'Practice', 11: 'Good', 12: 'Bad', 13: 'Weak', 14: 'Thin', 15: 'Strong', 16: 'Peace', 17: 'Question', 18: 'Answer', 19: 'Time'}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    image_b64 = data['image']
    image_data = base64.b64decode(image_b64.split(',')[1])
    image = Image.open(io.BytesIO(image_data))
    image = np.array(image)

    # Process the image using mediapipe
    data_aux = []
    frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x)
                data_aux.append(y)
        if len(data_aux) == 42:
            prediction = model.predict([np.asarray(data_aux)])
            predicted_label = labels_dict[int(prediction[0])]
            return jsonify({"predictions": predicted_label})
    
    return jsonify({"predictions": "No hand detected"})

if __name__ == '__main__':
    app.run(debug=True)
