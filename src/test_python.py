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
while 1 :

    for i in range(1, 101):
        number = 6942
        str_num = str(number)
        bytes_num = str_num.encode()
        ser.write(bytes_num)
        time.sleep(0.005)
    print(f"output: {bytes_num}")
    strin = ser.readline()
    byte_string = strin
    string = byte_string.decode('utf-8')  # Decode the byte string into a regular string
    string = string.strip()  # Remove the newline character at the end
    number = int(string)
    print (f"input: {number}")
