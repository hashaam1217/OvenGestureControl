from flask import Flask, render_template, Response, request, jsonify
import cv2
import matplotlib.pyplot as plt
import numpy as np
import io
import threading
import time
import serial
from flask_cors import CORS
import mediapipe as mp
from collections import deque
import webbrowser
import subprocess


variables = { 'soakTemp': 0, 'soakTime': 0, 'reflowTemp': 0, 'reflowTime': 0, 'start': 0, 'stop': 0}
last_twenty = deque(maxlen=50)

# Specify the URL of the YouTube video
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
subprocess.Popen(['/usr/bin/microsoft-edge', "http://127.0.0.1:5001/video_feed"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.Popen(['bash', "./start_script.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

dashboard_url = "http://localhost:3000/dashboard"

app = Flask(__name__)
CORS(app)

def print_result(result: mp.tasks.vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int): #print('Gesture recognition result:', result)
    #print('Gestures:', result.gestures)
    if result.gestures:
        for gesture in result.gestures:
            category_name = gesture[0].category_name
            score = gesture[0].score
            print(f'Gesture: {category_name}, Score: {score*100}%')

            # Add the category name to the deque
            last_twenty.append(category_name)

            # If the deque is full and all category names are the same
            if len(last_twenty) == 50 and len(set(last_twenty)) == 1:
                if last_twenty[49] == "Open_Palm":
                    print("STOP")
                if last_twenty[49] == "Thumb_Up":
                    print("START")
                if last_twenty[49] == "Closed_Fist":
                    subprocess.Popen(['/usr/bin/microsoft-edge', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    time.sleep(5)
                    return



#Flask server
@app.route('/')
def index():
    return render_template('index.html')

#ADD HAND RECOGNITION STUFF HERE
def generate_camera_feed():
    BaseOptions = mp.tasks.BaseOptions
    GestureRecognizer = mp.tasks.vision.GestureRecognizer
    GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    # Initialize MediaPipe Hands.
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.6, min_tracking_confidence=0.6)

    # Initialize MediaPipe DrawingUtils.
    mp_drawing = mp.solutions.drawing_utils

    options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=print_result
    )

    with GestureRecognizer.create_from_options(options) as recognizer:
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the BGR image to RGB before processing.
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))
            recognizer.recognize_async(mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb), timestamp)

            # Process the frame with MediaPipe Hands.
            results = hands.process(frame_rgb)

            # Draw hand landmarks on the frame.
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            ret, jpeg = cv2.imencode('.jpg', frame)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_camera_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/plot.png')
def plot_png():
    fig, ax = plt.subplots()
    # Create your plot here
    output = io.BytesIO()
    fig.savefig(output, format='png')
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/update', methods=['POST'])
def update_files():
    data = request.get_json()  # Get JSON data from the POST request
    print(data)

    # Now you can use this data to update your files
    # For example, let's assume the data is a dictionary with file names and contents
    for var_name, value in data.items():
        if var_name in variables:
            variables[var_name] = int(value)
            print(var_name)
            print(variables[var_name])

        for i in range(1, 101):
            number = variables[var_name]
            number = number + control_bit(var_name)
            str_num = str(number)
            bytes_num = str_num.encode()
            ser.write(bytes_num)
            time.sleep(0.005)
        print(f"output: {bytes_num}")
    return jsonify({'message': 'Variables updated successfully'}), 200


if __name__ == '__main__':
    flask_thread = threading.Thread(target=app.run, kwargs={'port': 5001})
    flask_thread.start()
    flask_thread.join()


    print("end")
