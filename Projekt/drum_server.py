import serial
import socket

import subprocess

ser = serial.Serial("/dev/cu.usbmodem1421", 9600)
# Establish the connection on a specific port

HOST, PORT = '', 3001

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print('Serving HTTP on port %s ...')

while True:
    data = ser.readline()
    print("RECV {}".format(data))

    try:
        # RECV b'0\r\n'
        data = int(str(data).replace("\\n", "").replace("\\r", "").replace("b", "").replace("\'", ""))

        if data < 2:
            return_code = subprocess.Popen(["afplay", "Oh00.mp3"])
        elif data < 4:
            return_code = subprocess.Popen(["afplay", "RS.mp3"])
        elif data < 6:
            return_code = subprocess.Popen(["afplay", "SD0000.mp3"])
        elif data < 8:
            return_code = subprocess.Popen(["afplay", "CY0000.mp3"])
        elif data < 10:
            return_code = subprocess.Popen(["afplay", "CL.mp3"])
        elif data < 12:
            return_code = subprocess.Popen(["afplay", "CH.mp3"])

        print(data)

    except ValueError:
        pass
