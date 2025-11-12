# Hand Sign to Text Converter (ASL)

> A real-time Hand Sign to Text Converter built with Python, OpenCV, MediaPipe, and Scikit-learn, featuring a modern GUI and text-to-speech.

This application translates American Sign Language (ASL) gestures from a live webcam feed into text and speech. It uses a custom-trained machine learning model to recognize the 26 letters of the ASL alphabet, allowing users to build words and sentences in real-time.

## ✨ Features

* **Real-Time Translation:** Instantly translates hand signs into text using a webcam.
* **Modern GUI:** A sleek and user-friendly interface built with CustomTkinter, featuring a home page, learning center, and converter.
* **Learn Mode:** A dedicated "Learn Signs" page displaying a chart of the ASL alphabet for new users.
* **Sentence Builder:** Functionality to add spaces, backspace, and clear the screen to form complete sentences.
* **Text-to-Speech:** A "Speak Text" button that vocalizes the translated sentence.
* **Left & Right Hand Support:** The model is trained to recognize gestures from both left and right hands.
* **Portable:** The application is fully portable. The trained model (`model.pkl`) is included and can be run on any system with the required libraries, no retraining needed.

---

## 🛠️ Tech Stack

* **Python:** The core programming language.
* **OpenCV:** For capturing and processing the live webcam feed.
* **MediaPipe:** For high-fidelity, real-time hand landmark detection.
* **Scikit-learn:** For training the Random Forest classification model.
* **CustomTkinter:** For building the modern and responsive graphical user interface.
* **pyttsx3:** For the Text-to-Speech (TTS) functionality.
* **Pillow (PIL):** For handling and displaying images within the GUI.

---

## 🚀 Installation & Usage

Follow these steps to run the project on your local machine.

### Prerequisites

* Python (3.8 or newer)
* A webcam

### Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/scmandolikar/HandSignConverter.git](https://github.com/scmandolikar/HandSignConverter.git)
    cd hand-sign-converter
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Create the environment
    python -m venv venv

    # Activate on Windows
    .\venv\Scripts\activate

    # Activate on macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```
    The application will launch, and you can start using it immediately.

---

## 🧠 Training Your Own Model (Optional)

This project already includes a pre-trained `model.pkl` file. However, if you want to improve accuracy or add new signs, you can train your own model.

1.  **Collect Data:**
    * Run the data collection script:
        ```bash
        python create_dataset.py
        ```
    * Press a letter key (e.g., 'a') to start collecting samples for that sign. Make the sign in front of the camera, varying the angle and position slightly.
    * The script will collect a set number of samples and then stop.
    * Repeat this for all 26 letters of the alphabet.
    * Press `Esc` to quit the script when finished. This creates `data/hand_landmarks.csv`.

2.  **Train the Model:**
    * Run the training script:
        ```bash
        python train_model.py
        ```
    * This script reads the CSV file, trains a new Random Forest classifier, and saves it as `model.pkl`, overwriting the old one. Your application will now use this new model.

## 📂 Project Structure

```
HandSignConverter/
├── data/                     # (Optional) Holds the generated CSV data
├── icons/                    # Icons for the GUI buttons
├── images/                   # Images for the "Learn Signs" page
├── templates/                # HTML for the web app
├── venv/                     # Virtual environment (ignored by Git)
├── app.py                    # Main desktop application script
├── create_dataset.py         # Script to collect training data
├── model.pkl                 # The pre-trained machine learning model
├── train_model.py            # Script to train the model
├── web_app.py                # Flask server script for the web app
├── README.md                 # Project documentation
└── requirements.txt          # List of Python dependencies
```
├── train_model.py            # Script to train the model
├── web_app.py                # Flask server script for the web app
├── README.md                 # Project documentation
└── requirements.txt          # List of Python dependencies