import serial
import signal
import socket
import subprocess

import sys

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
ser = serial.Serial("/dev/cu.usbmodem1421", 9600)
HOST, PORT = '', 3001

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print('Serving HTTP on port %s ...')


# TODO send depending on sample
def update_colors():
    ser.write("0".encode('ascii'))


def process_touch():
    try:
        data = ser.readline()
        play_sound(parse_arduino_str(data))

        # TODO process sound for Q-learning & score
    except ValueError:
        print("WRONG DATA INPUT")


song_id = play_song(int(input("Choose song:\n"
                              "1. sample1\n"
                              "2. sample2\n"
                              "")))

# TODO open sample and loop while playing
for i in range(sys.maxsize):
    try:
        # steps of 100ms
        signal.setitimer(signal.ITIMER_REAL, .1)

        process_touch()
        update_colors()

    except TimeoutError:
        pass
