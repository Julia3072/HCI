from json import loads
from math import ceil
from multiprocessing import Process, Manager

from serial import Serial, SerialException
from subprocess import Popen

from sys import maxsize
import time

# TODO completely rewrite

'''
recording drum sounds for reference values
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


# playing sound after cap sensor pressed
def handle_sound(sid):
    Popen(["afplay", sound_map[int(sid)]])


# writes color changes to arduino
def process_lighting(color_id, intensity):
    serial.write("{}{}\n".format(color_id, intensity).encode('ascii'))


# turns of lights after indication from song_ref
def process_lighting_turn_off(color_id):
    time.sleep(1)
    process_lighting(color_id, 0)


def check_light_queues(timeslot, _sref):
    for j in range(1, 5):

        # if sound played within next 20 timeslots
        if len(_sref[color_map[j]]) > 0 and timeslot + 100 > _sref[color_map[j]][0]:
            # update reference and discard fist element
            _sref[color_map[j]] = _sref[color_map[j]][1:-1]

            process_lighting(j, 3)

            # spawn background process to disable light
            Process(target=process_lighting_turn_off, args=(j,)).start()
            return True
    return False


# function wrapper for process
def tick(timeslot, _sref):
    try:

        # if arduino needs lighting update only do this to not overwrite serial
        if check_light_queues(timeslot, _sref):
            time.sleep(0.02)

        # blocks until sound int on serial and plays it
        handle_sound(ceil(int(serial.readline()) / 2))

        # makes sure process does not return early
        time.sleep(0.02)

    except ValueError:
        pass
    except (KeyError, SerialException) as e:
        print(e)


# adjust serial port according to arduino connection
serial = Serial("/dev/cu.usbmodem1411", 115200)
song_name = input("Enter mp3 filename (w/o ending): ")
curr_song = Popen(["afplay", "sounds_mp3/{}.mp3".format(song_name)])

with open("sounds_json/{}.json".format(song_name), "r") as song_ref:
    song_ref = loads(song_ref.readlines()[0])
    # init reference dictionary
    song_ref = Manager().dict({color_map[x]: song_ref[color_map[x]] for x in range(1, 5)})

    # loop over timeslots
    for i in range(maxsize):

        # break if background song is not playing
        if curr_song.poll() is not None:
            break

        p = Process(target=tick, args=(i, song_ref))
        p.start()

        # wait 20ms for thread
        p.join(0.02)

        if p.is_alive():
            p.terminate()
            p.join()
