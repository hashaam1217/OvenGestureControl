from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import threading
import time
import numpy as np
import math
from collections import Counter


app = Flask(__name__)
text = "hello"

@app.route('/')
def index():
    return render_template('index.html')

#def print_result(result: mp.tasks.vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
#    if result.gestures:
#        global text
#        for gesture in result.gestures:
#            category_name = gesture[0].category_name
#            score = gesture[0].score
#            rounded_num = round(score, 4)
#            text = f'Score: {100*rounded_num: .2f}%, Gesture: {category_name} '
#            print(text)

# Global list to store the last ten gestures
last_ten_gestures = []

def print_result(result: mp.tasks.vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global last_ten_gestures
    global text
    rounded_num = 0  # Define rounded_num here
    if result.gestures:
        for gesture in result.gestures:
            category_name = gesture[0].category_name
            score = gesture[0].score
            rounded_num = round(score, 4)  # Update rounded_num here

            # Add the new gesture to the list
            last_ten_gestures.append(category_name)

            # If there are more than ten gestures in the list, remove the oldest one
            if len(last_ten_gestures) > 100:
                last_ten_gestures.pop(0)

    # Find the most common gesture in the last ten gestures
    counter = Counter(last_ten_gestures)
    most_common_gesture = counter.most_common(1)[0][0]
    text = f'Score: {100*rounded_num: .2f}%, Gesture: {most_common_gesture} '
    print(text)

def gen():
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

            # Create an image with the text
            text_image = np.zeros((50, frame.shape[1], 3), np.uint8)
            cv2.putText(text_image, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Stack the text image under the frame
            frame = np.vstack((frame, text_image))

            # Encode the frame to JPEG
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        cap.release()
        cv2.destroyAllWindows()

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)

