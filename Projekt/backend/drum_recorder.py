from threading import Timer

import serial
import signal
import subprocess
import math
import sys
import json
from multiprocessing import Process, Manager

'''
record drum sounds for reference values
'''

sound_map = {
    1: "sounds_mp3/CH.mp3",
    2: "sounds_mp3/CL.mp3",
    3: "sounds_mp3/RS.mp3",
    4: "sounds_mp3/SD0000.mp3"
}
color_map = {
    1: "red",
    2: "green",
    3: "yellow",
    4: "blue"
}

itt = 0


def handle_sound_ext(sid):
    # mapping capacitive sensor to sound
    subprocess.Popen(["afplay", sound_map[int(sid)]])

    # red = 1, green = 2, yellow = 3, blue = 4
    # intensity from 0 to 3 lights activated
    ser.write("{}{}\n".format(sid, 3).encode('ascii'))


def handle_sound_int(sid, timeslot, _sd):
    tmp = _sd[color_map[sid]]
    tmp.append(timeslot)
    _sd[color_map[sid]] = tmp
    print(_sd)


def tick(timeslot, _sd):
    data = ser.readline()

    sound_id = math.ceil(int(data) / 2)

    handle_sound_ext(sound_id)
    handle_sound_int(sound_id, timeslot, _sd)


ser = serial.Serial("/dev/cu.usbmodem1411", 115200)

song_desc = Manager().dict()

song_desc["song_name"] = input("Enter mp3 filename (w/o ending): ")
song_desc["red"], song_desc["green"], song_desc["yellow"], song_desc["blue"] = [], [], [], []

curr_song = subprocess.Popen(["afplay", "sounds_json/{}.mp3".format(song_desc["song_name"])])

signal.signal(signal.SIGALRM, TimeoutError)

# loop over timeslots while song is playing
for i in range(sys.maxsize):

    if curr_song.poll() is not None:
        break

    try:

        p = Process(target=tick, name="Tick", args=(i, song_desc))
        p.start()
        # 50ms
        p.join(0.05)

        # If thread is active
        if p.is_alive():
            p.terminate()
            p.join()

    # timeout as accepted failure
    except TimeoutError:
        pass
    except (ValueError, KeyError, serial.SerialException) as e:
        print(e)

print(song_desc)

with open("sounds_json/{}.json".format(song_desc["song_name"]), "w") as song_res:
    song_res.write(json.dumps(dict(song_desc)))
