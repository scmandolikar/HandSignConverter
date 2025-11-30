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

## 📸 Demo & Screenshots

*Coming soon - Application screenshots and demo video will be added*

## 🎯 Use Cases

- **Accessibility** - Help hearing-impaired individuals communicate
- **ASL Learning** - Interactive tool for learning American Sign Language
- **Healthcare** - Enable communication between deaf patients and medical staff
- **Education** - Classroom aid for special education
- **Customer Service** - Accessibility tool for service counters
- **Research** - Gesture recognition and ML model development

## 💡 How It Works

1. **Video Capture**: Uses OpenCV to capture real-time webcam feed
2. **Hand Detection**: MediaPipe detects and tracks 21 hand landmarks
3. **Feature Extraction**: Extracts coordinate data from detected landmarks
4. **Classification**: Random Forest model classifies the gesture (A-Z)
5. **Output**: Displays recognized letter and speaks via text-to-speech
6. **Sentence Building**: Users can build words and sentences letter by letter

## 🚀 Features Roadmap

- [ ] Support for ASL words and phrases (not just letters)
- [ ] Multi-language sign language support (BSL, ISL, etc.)
- [ ] Mobile app version (iOS/Android)
- [ ] Real-time sentence prediction using NLP
- [ ] Hand gesture speed optimization
- [ ] Export conversation history
- [ ] Integration with video conferencing platforms

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Contribution
- Improve model accuracy with more training data
- Add support for new sign languages
- Enhance GUI with themes and customization
- Optimize real-time performance
- Write comprehensive tests

## 🐛 Known Issues

- Model accuracy depends on lighting conditions (works best in well-lit environments)
- Requires clear background for optimal hand detection
- Real-time processing may lag on older hardware
- Currently supports only 26 ASL alphabet letters

## 📐 Model Information

- **Algorithm**: Random Forest Classifier
- **Training Data**: 26 ASL alphabet letters (A-Z)
- **Features**: 21 hand landmark coordinates (x, y, z)
- **Accuracy**: ~95% on test dataset
- **Model File**: `model.pkl` (included)

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 📚 Resources

- [ASL Alphabet Chart](https://www.startasl.com/asl-alphabet/)
- [MediaPipe Hands Documentation](https://google.github.io/mediapipe/solutions/hands.html)
- [American Sign Language (ASL)](https://en.wikipedia.org/wiki/American_Sign_Language)

## ⭐ Star History

If you find this project useful for learning or research, please consider giving it a star! ⭐

## 📧 Contact & Support

**Sakshath Mandolikar**
- Email: scmandolikar@gmail.com
- GitHub: [@scmandolikar](https://github.com/scmandolikar)
- LinkedIn: [Sakshath Mandolikar](https://www.linkedin.com/in/sushant-mandolikar-71a519256/)

For bug reports and feature requests, please use the [GitHub Issues](https://github.com/scmandolikar/HandSignConverter/issues) page.

---

**Built with ❤️ by Sakshath Mandolikar** | TY BScIT Student | Academic ML Project
