#Bidirectional communication using multithreading
import threading

import time
import serial
# configure the serial port
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser.isOpen()

def print_numbers():
    while True:
        strin = ser.readline()
        byte_string = strin
        string = byte_string.decode('utf-8')  # Decode the byte string into a regular string
        string = string.strip()  # Remove the newline character at the end
        number = int(string)
        print (f"input: {number}")

def send_numbers():
    while True:
        for i in range(1, 101):
            number = 1023
            str_num = str(number)
            bytes_num = str_num.encode()
            ser.write(bytes_num)
            time.sleep(0.005)
            print(f"output: {bytes_num}")
            number = 2045
            str_num = str(number)
            bytes_num = str_num.encode()
            ser.write(bytes_num)
            time.sleep(0.005)
            print(f"output: {bytes_num}")
            number = 3238
            str_num = str(number)
            bytes_num = str_num.encode()
            ser.write(bytes_num)
            time.sleep(0.005)
            print(f"output: {bytes_num}")
            number = 4040
            str_num = str(number)
            bytes_num = str_num.encode()
            ser.write(bytes_num)
            time.sleep(0.005)
            print(f"output: {bytes_num}")
        print(number)
        time.sleep(1)

# Create threads
thread2 = threading.Thread(target=send_numbers)
thread1 = threading.Thread(target=print_numbers)

# Start threads
thread2.start()
thread1.start()

# Wait for both threads to finish
thread2.join()
thread1.join()

print("Threads have been joined")

