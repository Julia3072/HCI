#!/usr/bin/env python

from json import loads
from math import ceil
from multiprocessing import Process, Manager
from serial import Serial, SerialException
from subprocess import Popen
from sys import maxsize, exit
from time import sleep

'''
game loop for playing
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
latency_light, max_tick = 100, 0.02


# writes color changes to arduino
def process_lighting(color_id: int, intensity: int):
    serial.write("{}{}\n".format(color_id, intensity).encode('ascii'))


# turns of lights after indication from song_ref
def process_lights_turn_off(color_id: int):
    # TODO adapt color turning off - change only one light at a time, at first red1, red2, red3, then wait and blacken
    # TODO maybe priority queue, where the indication of a next light has priority over the turning off
    sleep(1)
    process_lighting(color_id, 0)


def update_lights(timeslot: int, _sref):
    for j in range(1, 5):

        # if sound played within next 20 timeslots
        if len(_sref[color_map[j]]) > 0 and timeslot + latency_light > _sref[color_map[j]][0]:
            process_lighting(j, 3)

            # update reference and discard fist element
            _sref[color_map[j]] = _sref[color_map[j]][1:-1]

            # spawn background process to disable light
            Process(target=process_lights_turn_off, args=(j,)).start()

            # block to not overwrite serial
            sleep(max_tick)


# function wrapper for process
def tick(timeslot: int, _sref):
    try:

        # if arduino needs lighting update only do this to not overwrite serial
        update_lights(timeslot, _sref)

        data_in = int(ceil(int(serial.readline()) / 2))

        # TODO add to new reference file of song
        # TODO maybe compare to currently first in sound queue
        # blocks until sound int on serial and plays it
        Popen(["afplay", sound_map[data_in]])

        # makes sure process does not return early
        sleep(max_tick)

    except (ValueError, KeyError, SerialException) as e:
        print(e)


# adjust serial port according to arduino connection
serial = Serial("/dev/cu.usbmodem1411", 115200)

while True:
    song_name = input("Enter mp3 filename (w/o ending): ")
    if song_name == "exit":
        exit(0)

    curr_song = Popen(["afplay", "sounds_mp3/{}.mp3".format(song_name)])

    with open("sounds_json/{}.json".format(song_name), "r") as song_ref:
        song_ref = loads(song_ref.readlines()[0])
        # init reference dictionary
        song_ref = Manager().dict({color_map[x]: song_ref[color_map[x]] for x in range(1, 5)})

        # TODO generate array with currently to play sounds

        # loop over timeslots
        for i in range(maxsize):

            # break if background song is not playing
            if curr_song.poll() is not None:
                break

            p = Process(target=tick, args=(i, song_ref))
            p.start()

            # wait 20ms for thread
            p.join(max_tick)

            if p.is_alive():
                p.terminate()
                p.join()
