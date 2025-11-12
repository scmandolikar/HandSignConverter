import cv2

# Use index 1 to test the external webcam
cap = cv2.VideoCapture(1) 

if not cap.isOpened():
    print("❌ Error: Cannot open camera at index 1.") # Updated message
else:
    print("✅ Success! Camera at index 1 is working.") # Updated message
    print("Press 'q' to quit.")

    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to grab frame.")
            break

        cv2.imshow("Camera Test", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()