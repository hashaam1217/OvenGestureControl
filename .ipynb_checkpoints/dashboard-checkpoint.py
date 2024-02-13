import cv2
import mediapipe as mp
import threading
import time
import panel as pn
import numpy as np
from bokeh.plotting import figure

# Initialize Panel
pn.extension()

# Create a Panel pane to display the frame
frame_pane = pn.pane.Bokeh()

def print_result(result: mp.tasks.vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
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

            # Convert the frame to a format that can be displayed by Panel
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.flip(frame, axis=0)
            p = figure(x_range=(0, frame.shape[1]), y_range=(0, frame.shape[0]), width=frame.shape[1], height=frame.shape[0])
            p.image_rgba(image=[cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)], x=0, y=0, dw=frame.shape[1], dh=frame.shape[0])
            frame_pane.object = p

            # Break the loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

def handle_serial_port():
    while True:
        print("Serial port being sent")
        time.sleep(0.5)

# Creating the threads
opencv_thread = threading.Thread(target=main)
serial_port_thread = threading.Thread(target=handle_serial_port)

# Starting the threads
opencv_thread.start()
serial_port_thread.start()

# Incase both threads end
opencv_thread.join()
print("opencv_thread ended")
serial_port_thread.join()
print("serial_port_thread ended")
print("Both threads have ended")

# Serve the Panel app
pn.serve(frame_pane)

