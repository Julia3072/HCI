#!/usr/bin/env python

from json import loads
from json import load
from math import ceil
from multiprocessing import Process, Manager

from serial import Serial, SerialException
from subprocess import Popen
from sys import maxsize, exit
from time import sleep

from QLearning import QLearning
from DifficultyCalculator import calculateDifficultyScore

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
latency_light, latency_correct, latency_double, max_tick = 100, 20, 5, 0.02
heart_rate_bound_low = 70
heart_rate_bound_high = 80


# writes color changes to arduino
def process_lighting(color_id: int, intensity: int):
    serial.write("{}{}\n".format(color_id, intensity).encode('ascii'))


# turns of lights after indication from song_ref
def process_lights_turn_off(color_id: int, timer: int):
    # TODO adapt color turning off - change only one light at a time, at first red1, red2, red3, then wait and blacken
    # TODO maybe priority queue, where the indication of a next light has priority over the turning off
    sleep(timer)
    process_lighting(color_id, 0)


def update_lights(timeslot: int, _sref, _curr_play):
    for j in range(1, 5):

        # if sound played within next 20 timeslots
        if len(_sref[color_map[j]]) > 0 and timeslot + latency_light > _sref[color_map[j]][0]:
            process_lighting(j, 3)

            _curr_play[j - 1] = _sref[color_map[j]][0]

            # update reference and discard fist element
            _sref[color_map[j]] = _sref[color_map[j]][1:-1]

            # spawn background process to disable light
            Process(target=process_lights_turn_off, args=(j, 1)).start()

            # block to not overwrite serial
            sleep(max_tick)


# function wrapper for process
def tick(timeslot: int, _sref, _curr_ply, _n_corr, _n_insg, _heart_avg):
    try:

        # if arduino needs lighting update only do this to not overwrite serial
        update_lights(timeslot, _sref, _curr_ply)

        data_in = str(serial.readline()).replace("b'", "").replace("\\r\\n'", "")

        # is hearth rate
        if '.' in data_in:
            _heart_avg.append(int(data_in.replace(".", "")))

        else:

            data_in = int(ceil(int(data_in) / 2))

            # sufficiently after last played
            if _curr_ply[data_in - 1] + latency_double < timeslot:

                # blocks until sound int on serial and plays it
                Popen(["afplay", sound_map[data_in]])

                _n_insg.value += 1
                # if played in bounds
                if timeslot - latency_correct < _curr_ply[data_in - 1] < timeslot + latency_correct:
                    _n_corr.value += 1
                    _curr_ply[data_in] = -100

        # makes sure process does not return early
        sleep(max_tick)

    except (ValueError, KeyError, SerialException) as e:
        print(e)


# adjust serial port according to arduino connection
serial = Serial("/dev/cu.usbmodem1411", 115200)

# read song list
with open("songList.json") as data_file:
    songListParsed = load(data_file)
songList = songListParsed["songs"]

# init q learning
initialMatrix = [0.0]*len(songList)
for i in range(0, len(songList)):
    initialMatrix[i] = calculateDifficultyScore("sounds_json/{}.json".format(songList[i]))

qLearning = QLearning(initialMatrix)

while True:
    # used for entering a song name
    #song_name = input("Enter mp3 filename (w/o ending): ")
    #if song_name == "exit":
    #    exit(0)

    # get next song
    current_song_index = qLearning.getNext()
    song_name = songList[current_song_index]

    print(songList)
    print(qLearning.getQMatrix())
    print(current_song_index)

    curr_song = Popen(["afplay", "sounds_mp3/{}.mp3".format(song_name)])

    with open("sounds_json/{}.json".format(song_name), "r") as song_ref:
        song_ref = loads(song_ref.readlines()[0])
        # init reference dictionary

        song_ref = Manager().dict({color_map[x]: song_ref[color_map[x]] for x in range(1, 5)})
        sums_ref = sum([len(song_ref[color_map[x]]) for x in range(1, 5)])

        # init scores
        curr_ply = Manager().list([-10000] * 4)
        n_corr, n_insg, heart_avg = Manager().Value('i', 0), Manager().Value('i', 0), Manager().list()

        # loop over timeslots
        for i in range(maxsize):

            # break if background song is not playing
            if curr_song.poll() is not None:
                break

            p = Process(target=tick, args=(i, song_ref, curr_ply, n_corr, n_insg, heart_avg))
            p.start()

            # wait 20ms for thread
            p.join(max_tick)

            if p.is_alive():
                p.terminate()
                p.join()

        n_wrong = n_insg.value - n_corr.value
        print(n_corr.value)
        print(n_insg.value)
        print(sums_ref)

        avg_heart_rate = sum(list(heart_avg)) / len(heart_avg)
        print(avg_heart_rate)

        # amount correctly played subtracted the number of unnecessary touches
        score = int(100 * (n_corr.value / sums_ref) - max((100 * (n_insg.value - sums_ref) / sums_ref), 0))
        # add bonus points based on average heart rate
        if avg_heart_rate < heart_rate_bound_low:
            score -= 5
        if avg_heart_rate > heart_rate_bound_high:
            score += 5

        # make sure 0 <= score <= 100
        score = min(max(score, 0), 100)
        
        # send to Qlearning part
        qLearning.updateQMatrix(current_song_index, score)
        print(score)

        # TODO send to motor
        # serial.write("{}{}\n".format(9, score / 10).encode('ascii'))
