import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys, time, math
# configure the serial port

xsize=1000


def run(data):
    # update the data
    t,y,z = data
    if t>-1:
        xdata.append(t)
        ydata_cel.append(y)
        ydata_far.append(z)
        if t>xsize: # Scroll to the left.
            ax.set_xlim(t-xsize, t)
        line_cel.set_data(xdata, ydata_cel)
        line_far.set_data(xdata, ydata_far)

    return line_cel, line_far

def on_close_figure(event):
    sys.exit(0)

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS
    )
ser.isOpen()

def data_gen():
        t = data_gen.t

        while True:
            t+=1
            strin = ser.readline()
            strin = strin.rstrip()
            strin = strin.decode()

            val=float(strin)
            farenheit=val * 9/5 + 32

            print(strin)

            yield t, val, farenheit


data_gen.t = -1
fig = plt.figure()
fig.canvas.mpl_connect('close_event', on_close_figure)
ax = fig.add_subplot(111)
line_cel, = ax.plot([], [], lw=2)
line_far, = ax.plot([], [], lw=2)
ax.set_ylim(0, 300)
ax.set_xlim(0, xsize)
ax.grid()
xdata, ydata_cel, ydata_far = [], [], []
# Important: Although blit=True makes graphing faster, we need blit=False to prevent
# spurious lines to appear when resizing the stripchart.
ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=100, repeat=False)
plt.show()


