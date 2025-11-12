import cv2
import mediapipe as mp
import numpy as np
import pickle
import customtkinter as ctk
from PIL import Image
import pyttsx3
import time
import os
import threading

# --- MODERN UI DEFINITIONS ---
BACKGROUND_COLOR = "#242424"
PRIMARY_COLOR = "#2E2E2E"
SECONDARY_COLOR = "#3A3A3A"
ACCENT_COLOR = "#1F6AA5"
TEXT_COLOR = "#FFFFFF"

# --- Main App Class ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- FONT DEFINITIONS ---
        self.title_font = ctk.CTkFont(family="Roboto", size=30, weight="bold")
        self.button_font = ctk.CTkFont(family="Roboto", size=18, weight="bold")
        self.label_font = ctk.CTkFont(family="Roboto", size=16, weight="bold")
        self.textbox_font = ctk.CTkFont(family="Roboto", size=14)

        # --- Window Setup ---
        self.title("ASL Hand Sign Converter")
        self.geometry("1100x700")
        self.configure(fg_color=BACKGROUND_COLOR)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Load Icons ---
        self.load_icons()

        # --- App State & Utilities ---
        self.camera_thread = None
        self.model = None
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils
        self.current_sentence = ""
        self.last_prediction = None
        self.prediction_start_time = None
        self.prediction_confidence_duration = 1.0

        # --- Frame Containers & Widget References ---
        self.home_frame = None
        self.learn_frame = None
        self.converter_frame = None
        self.start_button = None
        self.video_label = None

        self.show_home_page()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_icons(self):
        self.camera_icon = ctk.CTkImage(Image.open("icons/camera.png"), size=(24, 24))
        self.book_icon = ctk.CTkImage(Image.open("icons/book.png"), size=(24, 24))
        self.exit_icon = ctk.CTkImage(Image.open("icons/exit.png"), size=(24, 24))
        self.speak_icon = ctk.CTkImage(Image.open("icons/speak.png"), size=(20, 20))

    # --- Page Navigation ---
    def show_frame(self, frame_to_show):
        self.stop_camera_thread()
        if self.home_frame: self.home_frame.grid_forget()
        if self.learn_frame: self.learn_frame.grid_forget()
        if self.converter_frame: self.converter_frame.grid_forget()
        frame_to_show.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    # --- Home Page ---
    def show_home_page(self):
        self.stop_camera_thread()
        if not self.home_frame:
            self.home_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.home_frame.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(self.home_frame, text="ASL Hand Sign Converter", font=self.title_font, text_color=TEXT_COLOR).grid(row=0, column=0, pady=(40, 30), padx=20)
            ctk.CTkButton(self.home_frame, text="Start Converter", image=self.camera_icon, command=self.show_converter_page, font=self.button_font, fg_color=ACCENT_COLOR, hover_color=SECONDARY_COLOR, height=50).grid(row=1, column=0, pady=10, padx=150, sticky="ew")
            ctk.CTkButton(self.home_frame, text="Learn Signs Chart", image=self.book_icon, command=self.show_learn_signs_page, font=self.button_font, fg_color=ACCENT_COLOR, hover_color=SECONDARY_COLOR, height=50).grid(row=2, column=0, pady=10, padx=150, sticky="ew")
            ctk.CTkButton(self.home_frame, text="Exit", image=self.exit_icon, command=self.on_closing, font=self.button_font, fg_color=SECONDARY_COLOR, hover_color="#C0392B", height=50).grid(row=3, column=0, pady=(30, 40), padx=150, sticky="ew")
        self.show_frame(self.home_frame)

    # --- Learn Signs Page ---
    def show_learn_signs_page(self):
        self.stop_camera_thread()
        if not self.learn_frame:
            self.learn_frame = ctk.CTkFrame(self, fg_color=PRIMARY_COLOR, corner_radius=10)
            self.learn_frame.grid_columnconfigure(0, weight=1)
            self.learn_frame.grid_rowconfigure(1, weight=1)
            ctk.CTkLabel(self.learn_frame, text="Learn ASL Alphabet Chart", font=self.title_font, text_color=TEXT_COLOR).grid(row=0, column=0, pady=(20, 20))
            image_path = os.path.join('images', 'asl_chart.jpeg')
            if os.path.exists(image_path):
                chart_image = Image.open(image_path)
                chart_ctk_image = ctk.CTkImage(light_image=chart_image, dark_image=chart_image, size=(800, 600))
                image_label = ctk.CTkLabel(self.learn_frame, image=chart_ctk_image, text="")
                image_label.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
            else:
                ctk.CTkLabel(self.learn_frame, text="Image 'asl_chart.jpeg' not found.", font=self.label_font).grid(row=1, column=0, pady=20)
            ctk.CTkButton(self.learn_frame, text="Back to Home", command=self.show_home_page, font=self.button_font, fg_color=SECONDARY_COLOR, hover_color=ACCENT_COLOR).grid(row=2, column=0, pady=20, padx=200, sticky="ew")
        self.show_frame(self.learn_frame)

    # --- Converter Page ---
    def show_converter_page(self):
        self.load_model()
        if not self.converter_frame:
            self.converter_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.converter_frame.grid_columnconfigure(0, weight=2)
            self.converter_frame.grid_columnconfigure(1, weight=1)
            self.converter_frame.grid_rowconfigure(0, weight=1)
            # Camera Frame
            camera_sub_frame = ctk.CTkFrame(self.converter_frame, fg_color=PRIMARY_COLOR, corner_radius=10)
            camera_sub_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")
            camera_sub_frame.grid_rowconfigure(0, weight=1)
            camera_sub_frame.grid_columnconfigure(0, weight=1)
            self.video_label = ctk.CTkLabel(camera_sub_frame, text="Press 'Start Camera'", font=self.label_font)
            self.video_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            self.start_button = ctk.CTkButton(camera_sub_frame, text="Start Camera", command=self.toggle_camera, font=self.button_font, fg_color=ACCENT_COLOR, hover_color=SECONDARY_COLOR)
            self.start_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
            # Controls Frame
            controls_sub_frame = ctk.CTkFrame(self.converter_frame, fg_color=PRIMARY_COLOR, corner_radius=10)
            controls_sub_frame.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="nsew")
            controls_sub_frame.grid_columnconfigure(0, weight=1)
            controls_sub_frame.grid_rowconfigure(2, weight=1)
            ctk.CTkButton(controls_sub_frame, text="Back to Home", command=self.show_home_page, font=self.button_font, fg_color=SECONDARY_COLOR, hover_color=ACCENT_COLOR).grid(row=0, column=0, pady=15, padx=10, sticky="ew")
            self.output_label = ctk.CTkLabel(controls_sub_frame, text="Translated Text:", font=self.label_font, text_color=TEXT_COLOR)
            self.output_label.grid(row=1, column=0, padx=10, pady=(15, 5), sticky="w")
            self.output_textbox = ctk.CTkTextbox(controls_sub_frame, height=200, font=self.textbox_font, fg_color=SECONDARY_COLOR, text_color=TEXT_COLOR, corner_radius=10)
            self.output_textbox.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
            button_grid = ctk.CTkFrame(controls_sub_frame, fg_color="transparent")
            button_grid.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
            button_grid.grid_columnconfigure((0, 1, 2), weight=1)
            ctk.CTkButton(button_grid, text="Space", command=self.add_space, fg_color=SECONDARY_COLOR, hover_color=ACCENT_COLOR).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
            ctk.CTkButton(button_grid, text="Backspace", command=self.backspace, fg_color=SECONDARY_COLOR, hover_color=ACCENT_COLOR).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            ctk.CTkButton(button_grid, text="Clear", command=self.clear_text, fg_color=SECONDARY_COLOR, hover_color=ACCENT_COLOR).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
            self.speak_button = ctk.CTkButton(controls_sub_frame, text="Speak Text", image=self.speak_icon, command=self.start_speak_thread, font=self.button_font, fg_color=ACCENT_COLOR, hover_color=SECONDARY_COLOR)
            self.speak_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        self.show_frame(self.converter_frame)

    def load_model(self):
        if not self.model:
            try:
                with open('model.pkl', 'rb') as f: self.model = pickle.load(f)
                print("Model loaded.")
            except FileNotFoundError: print("Error: model.pkl not found.")
            except Exception as e: print(f"Error loading model: {e}")

    # --- Thread-Safe Camera Control ---
    def toggle_camera(self):
        if self.camera_thread and self.camera_thread.is_alive():
            self.stop_camera_thread()
        else:
            self.start_camera_thread()

    def start_camera_thread(self):
        if self.camera_thread is None:
            if not self.model:
                self.video_label.configure(text="Error: Model not loaded.")
                return
            self.video_label.configure(text="") 
            self.camera_thread = CameraThread(self)
            self.camera_thread.start()
            self.start_button.configure(text="Stop Camera")
            self.update_gui_feed()

    def stop_camera_thread(self):
        if self.camera_thread is not None:
            self.camera_thread.stop()
            self.camera_thread.join()
            self.camera_thread = None
        if self.start_button is not None:
            self.start_button.configure(text="Start Camera")
        if self.video_label is not None:
            self.video_label.configure(image=None, text="Camera Off")

    def update_gui_feed(self):
        if self.camera_thread and self.camera_thread.is_running and self.camera_thread.frame is not None:
            frame = self.camera_thread.frame
            prediction = "No Hand Detected"
            try:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                        landmarks = []
                        base_x, base_y = hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y
                        for lm in hand_landmarks.landmark:
                            landmarks.extend([lm.x - base_x, lm.y - base_y])
                        pred = self.model.predict(np.array(landmarks).reshape(1, -1))[0]
                        prediction = f"Prediction: {pred.upper()}"
                        self.update_sentence(pred)
                else:
                    self.last_prediction = None
            except Exception:
                prediction = "Processing Error"
            
            cv2.putText(frame, prediction, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img_tk = ctk.CTkImage(light_image=img, dark_image=img, size=(640, 480))
            if self.video_label:
                self.video_label.image = img_tk
                self.video_label.configure(image=img_tk)
        
        if self.camera_thread and self.camera_thread.is_running:
            self.after(20, self.update_gui_feed)

    # --- Text and Speech Logic ---
    def update_sentence(self, prediction):
        if not prediction: return
        if prediction == self.last_prediction:
            if (time.time() - self.prediction_start_time) >= self.prediction_confidence_duration:
                if not self.current_sentence or self.current_sentence[-1].lower() != prediction.lower():
                    self.current_sentence += prediction
                    self.output_textbox.insert(ctk.END, prediction.upper())
                self.last_prediction = None
        else:
            self.last_prediction = prediction
            self.prediction_start_time = time.time()
            
    def add_space(self):
        if not self.current_sentence or self.current_sentence[-1] != ' ':
            self.current_sentence += " "
            self.output_textbox.insert(ctk.END, " ")

    def backspace(self):
        if self.current_sentence:
            self.current_sentence = self.current_sentence[:-1]
            self.output_textbox.delete("end-2c", "end-1c")

    def clear_text(self):
        self.current_sentence = ""
        self.output_textbox.delete("1.0", ctk.END)
    
    def start_speak_thread(self):
        text_to_speak = self.output_textbox.get("1.0", ctk.END).strip()
        if text_to_speak:
            self.speak_button.configure(state="disabled", text="Speaking...")
            speak_thread = threading.Thread(target=self.speak_text, args=(text_to_speak,), daemon=True)
            speak_thread.start()

    def speak_text(self, text):
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
        finally:
            self.speak_button.configure(state="normal", text="Speak Text")

    def on_closing(self):
        self.stop_camera_thread()
        self.destroy()

# --- Dedicated Camera Thread Class ---
class CameraThread(threading.Thread):
    def __init__(self, app_instance):
        super().__init__(daemon=True)
        self.app = app_instance
        self.is_running = False
        self.frame = None
        self.cap = None

    def run(self):
        self.is_running = True
        self.cap = cv2.VideoCapture(1)
        if not self.cap.isOpened():
            print("Error: CameraThread could not open camera.")
            self.is_running = False
            return

        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break
            self.frame = cv2.flip(frame, 1)
        
        self.cap.release()
        print("CameraThread finished.")

    def stop(self):
        self.is_running = False

if __name__ == "__main__":
    app = App()
    app.mainloop()