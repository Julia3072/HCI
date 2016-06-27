import serial
import signal
import socket
import subprocess

import sys
import time
from random import randint

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


# playing background song
def play_song(song_nr):
    song_map = {
        1: "sounds_json/sample1.mp3",
        2: "sounds_json/sample2.mp3",
    }
    return subprocess.Popen(["afplay", song_map[song_nr]])


# parse RECV b'0\r\n'
def parse_arduino_str(ard_str):
    return int(str(ard_str).replace("\\n", "").replace("\\r", "").replace("b", "").replace("\'", ""))


signal.signal(signal.SIGALRM, TimeoutError)

# Establish the connection on a specific port
ser = serial.Serial("/dev/cu.usbmodem1411", 115200)
HOST, PORT = '', 3001

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print('Serving HTTP on port %s ...')

time.sleep(5)

song_id = play_song(1)

# TODO CREATE FILE
# TODO WRITE TO FILE
# TODO open sample and loop while playing
for i in range(sys.maxsize):

    try:
        # steps of 10ms
        signal.setitimer(signal.ITIMER_REAL, .01)

        data = ser.readline()
        play_sound(parse_arduino_str(data))

        ser.write("{}{}\n".format(randint(1, 4), randint(0, 3)).encode('ascii'))

        # TODO store data to json with time step

    except TimeoutError:
        pass
    except ValueError:
        print("WRONG DATA INPUT")
    except serial.SerialException:
        print("SERIAL KILL")
