import serial
import socket
import signal

import subprocess

'''
record drum sounds for reference values
'''


# mapping capacitive sensor to sound
def play_sound(touch):
    sound_map = {
        1: "sounds_mp3/CH.mp3",
        3: "sounds_mp3/CL.mp3",
        5: "sounds_mp3/RS.mp3",
        7: "sounds_mp3/SD0000.mp3"
    }
    subprocess.Popen(["afplay", sound_map[touch]])


# parse RECV b'0\r\n'
def parse_arduino_str(ard_str):
    return int(str(ard_str).replace("\\n", "").replace("\\r", "").replace("b", "").replace("\'", ""))


def tick():
    pass


# Establish the connection on a specific port
ser = serial.Serial("/dev/cu.usbmodem1421", 9600)
HOST, PORT = '', 3001

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print('Serving HTTP on port %s ...')


for i in range(100000):
    try:
        subprocess.call(['python', 'a.py'], timeout=1)
    except subprocess.TimeoutExpired:
        sys.exit(1)



while True:
    try:
        play_sound(parse_arduino_str(ser.readline()))

    except ValueError:
        print("WRONG DATA INPUT: {}".format(data))
