import cv2
import mediapipe as mp
import threading
import time
import tkinter as tk
from tkinter import ttk

def print_result(result: mp.tasks.vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    #print('Gesture recognition result:', result)
    #print('Gestures:', result.gestures)
    if result.gestures:
        for gesture in result.gestures:
            category_name = gesture[0].category_name
            score = gesture[0].score
            print(f'Gesture: {category_name}, Score: {score*100}%')

def main():
    BaseOptions = mp.tasks.BaseOptions
    GestureRecognizer = mp.tasks.vision.GestureRecognizer
    GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    # Initialize MediaPipe Hands.
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # Initialize MediaPipe DrawingUtils.
    mp_drawing = mp.solutions.drawing_utils

    options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=print_result
    )

    with GestureRecognizer.create_from_options(options) as recognizer:
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # Convert the BGR image to RGB before processing.
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))
            recognizer.recognize_async(mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb), timestamp)

            # Process the frame with MediaPipe Hands.
            results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Draw hand landmarks on the frame.
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Display the resulting frame
            cv2.imshow('Frame', frame)

            # Break the loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


#if __name__ == "__main__":
#    main()

def handle_serial_port():
    while True:
        print("Serial port being sent")
        time.sleep(0.5)

# Creating the threads
opencv_thread =         threading.Thread(target=main)
serial_port_thread =    threading.Thread(target=handle_serial_port)

# Starting the threads
#opencv_thread.start()
##serial_port_thread.start()

# Incase both threads end
#opencv_thread.join()
#print("opencv_thread ended")
#serial_port_thread.join()
#print("serial_port_thread ended")
#print("Both threads have ended")
def create_panel():
    # Create the root window
    root = tk.Tk()
    root.title("Gesture Recognition Panel")

    # Create a frame
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Add a button to start the opencv_thread
    start_button = ttk.Button(frame, text="Start", command=opencv_thread.start)
    start_button.grid(row=0, column=0, sticky=tk.W)

    # Add a button to start the serial_port_thread
    start_button = ttk.Button(frame, text="Start Serial Port", command=serial_port_thread.start)
    start_button.grid(row=1, column=0, sticky=tk.W)

    # Add a button to stop the threads
    stop_button = ttk.Button(frame, text="Stop", command=root.destroy)
    stop_button.grid(row=2, column=0, sticky=tk.W)

    # Start the event loop
    root.mainloop()

# Replace your existing thread start calls with a call to create_panel
create_panel()

