from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
import cv2
import base64
import mediapipe as mp
import pickle

# Initialize Flask App
app = Flask(__name__)
CORS(app) # Allows the frontend (browser) to communicate with this backend

# --- Load Your Model and Hand Tracking Utilities ---
# This logic is copied from your desktop app's setup
try:
    model = pickle.load(open('model.pkl', 'rb'))
except FileNotFoundError:
    print("Error: 'model.pkl' not found. Please train the model first.")
    model = None
except Exception as e:
    print(f"An error occurred while loading the model: {e}")
    model = None

mp_hands = mp.solutions.hands
# For the web app, we process one hand at a time
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# --- Define the Main Page Route ---
@app.route('/')
def index():
    # This will render the index.html file from the 'templates' folder
    return render_template('index.html')

# --- Create the Prediction API Endpoint ---
@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    # Receive the image data from the frontend
    data = request.get_json()
    # The image is sent as a Data URL (e.g., "data:image/jpeg;base64,....")
    # We need to strip the header and decode the base64 string
    image_data = data['image'].split(',')[1] 
    
    try:
        # Decode the image
        decoded_image = base64.b64decode(image_data)
        np_arr = np.frombuffer(decoded_image, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception as e:
        return jsonify({'error': f'Image decoding failed: {e}'}), 400

    # --- Process the Image (The "Brain" of the App) ---
    prediction = ""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        landmarks = []
        base_x, base_y = hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y
        for lm in hand_landmarks.landmark:
            landmarks.extend([lm.x - base_x, lm.y - base_y])
        
        # Get the model's prediction
        prediction = model.predict(np.array(landmarks).reshape(1, -1))[0]
    
    # Return the prediction to the frontend as a JSON object
    return jsonify({'prediction': prediction.upper()})

if __name__ == '__main__':
    # Run the server on localhost, port 5000
    app.run(debug=True)