from flask import Flask, render_template, Response, request, jsonify
import cv2
import matplotlib.pyplot as plt
import numpy as np
import io
import threading
import time
import serial
from flask_cors import CORS

variables = { 'soakTemp': 0, 'soakTime': 0, 'reflowTemp': 0, 'reflowTime': 0 }

# configure the serial port
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser.isOpen()
def control_bit(name):
    match name:
        case "soakTemp":
            return 1000
        case "soakTime":
            return 2000
        case "reflowTemp":
            return 3000
        case "reflowTime":
            return 4000

def print_numbers():
    while True:
        strin = ser.readline()
        byte_string = strin
        string = byte_string.decode('utf-8')  # Decode the byte string into a regular string
        string = string.strip()  # Remove the newline character at the end
        number = int(string)
        print (f"input: {number}")
        time.sleep(1)

def send_numbers():
    print("Hello")
    while True:
        #for i in range(1, 101):
            #number = 1234
            #str_num = str(number)
            #bytes_num = str_num.encode()
            #ser.write(bytes_num)
            #time.sleep(0.005)
            #print(f"output: {bytes_num}")
            #number = 2045
            #str_num = str(number)
            #bytes_num = str_num.encode()
            #ser.write(bytes_num)
            #time.sleep(0.005)
            #print(f"output: {bytes_num}")
            #number = 3238
            #str_num = str(number)
            #bytes_num = str_num.encode()
            #ser.write(bytes_num)
            #time.sleep(0.005)
            #print(f"output: {bytes_num}")
            #number = 4040
            #str_num = str(number)
            #bytes_num = str_num.encode()
            #ser.write(bytes_num)
            #time.sleep(0.005)
            #print(f"output: {bytes_num}")
        #print(number)
        time.sleep(1)

app = Flask(__name__)
CORS(app)
#Flask server
@app.route('/')
def index():
    return render_template('index.html')

#ADD HAND RECOGNITION STUFF HERE
def generate_camera_feed():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

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
    monitor_thread = threading.Thread(target=print_numbers)
    send_thread = threading.Thread(target=send_numbers)
    flask_thread.start()
    monitor_thread.start()
    send_thread.start()

    send_thread.join()
    monitor_thread.join()
    flask_thread.join()


    print("end")
