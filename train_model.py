import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# Load the dataset
DATA_FILE = './data/hand_landmarks.csv'
df = pd.read_csv(DATA_FILE, header=None)

# Separate features (X) and labels (y)
X = df.iloc[:, 1:] # All columns except the first one (landmarks)
y = df.iloc[:, 0]  # The first column (the letter)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Initialize and train the Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
print("Training model...")
model.fit(X_train, y_train)
print("Model training complete.")

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save the trained model to a file
MODEL_PATH = './model.pkl'
with open(MODEL_PATH, 'wb') as f:
    pickle.dump(model, f)

print(f"Model saved to {MODEL_PATH}")