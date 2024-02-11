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
    #strin = ser.readline()
    #byte_string = strin
    #string = byte_string.decode('utf-8')  # Decode the byte string into a regular string
    #string = string.strip()  # Remove the newline character at the end
    #number = int(string)
    #print (number)
    #number = 8
    #str_num = str(number)
    #bytes_num = str_num.encode()
    #ser.write(bytes_num)
    #print(bytes_num)

    for number in range(1, 16):  # Loop from 1 to 10
        for i in range(1, 10000):
            str_num = str(number)  # Convert the number to a string
            bytes_num = str_num.encode()  # Convert the string to bytes
            ser.write(bytes_num)  # Write the bytes to the serial port
            print(bytes_num)  # Print the bytes

