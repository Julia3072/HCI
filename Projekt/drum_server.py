import serial
import socket

import subprocess


# mapping capacitive sensor to sound
def play_sound(touch):
    sound_map = {
        1: "sounds/CH.mp3",
        3: "sounds/CL.mp3",
        5: "sounds/RS.mp3",
        7: "sounds/SD0000.mp3"
    }
    subprocess.Popen(["afplay", sound_map[touch]])


# Establish the connection on a specific port
ser = serial.Serial("/dev/cu.usbmodem1421", 9600)
HOST, PORT = '', 3001

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print('Serving HTTP on port %s ...')

while True:
    data = ser.readline()

    try:

        # RECV b'0\r\n'
        touchInput = int(str(data).replace("\\n", "").replace("\\r", "").replace("b", "").replace("\'", ""))

        play_sound(touchInput)

        print(touchInput)

    except ValueError:
        pass
