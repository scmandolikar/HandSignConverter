import cv2
import mediapipe as mp
import csv
import os
import numpy as np

# Create a directory to store the dataset if it doesn't exist
DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

cap = cv2.VideoCapture(1) # IMPORTANT: Use 1 for external webcam, 0 for built-in

# Number of samples to collect for each sign
NUM_SAMPLES = 500
current_sample = 0
current_letter = ''

# Open a CSV file to write the data
csv_file = open(os.path.join(DATA_DIR, 'hand_landmarks.csv'), 'w', newline='')
writer = csv.writer(csv_file)

print("Starting data collection script. Press a key (a-z) to start collecting data for that letter.")
print("Make the sign in front of the camera. The script will collect 100 samples.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        
        # Normalize and flatten landmarks
        landmarks = []
        base_x, base_y = hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y
        for lm in hand_landmarks.landmark:
            landmarks.append(lm.x - base_x)
            landmarks.append(lm.y - base_y)
        
        # Collect data when a letter is selected
        if current_letter and current_sample < NUM_SAMPLES:
            writer.writerow([current_letter] + landmarks)
            current_sample += 1

    # Display information on the frame
    if current_letter:
        if current_sample < NUM_SAMPLES:
            status = f"Collecting data for '{current_letter.upper()}': {current_sample}/{NUM_SAMPLES}"
        else:
            status = f"Done with '{current_letter.upper()}'. Press another key."
    else:
        status = "Press a key (a-z) to start."
        
    cv2.putText(frame, status, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Data Collection', frame)

    key = cv2.waitKey(20) & 0xFF
    if key == 27:
        break
    # Check if the key is a letter (a-z)
    elif 97 <= key <= 122: # ASCII values for a-z
        current_letter = chr(key)
        current_sample = 0
        print(f"--- Switched to collecting data for letter: {current_letter.upper()} ---")

csv_file.close()
cap.release()
cv2.destroyAllWindows()