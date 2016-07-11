#!/usr/bin/env python3

from json import load
from math import ceil
from multiprocessing import Process, Manager
from subprocess import Popen
from sys import maxsize
from time import sleep

from serial import Serial, SerialException

from backend import q_learning
from backend import calculations

"""
game loop for playing
"""

# possible songs for qlearning
song_list = [
    # "ArcticMonkeys_Brianstorm",
    # "RedHotChiliPeppers_DaniCalifornia"
    "FranzFerdinand_TakeMeOut"
    # "BeachBoys_CaliforniaGirls"  # ,
    # "FranzFerdinand_TakeMeOut",
    # "RedHotChiliPeppers_DaniCalifornia"
]

sound_map = {
    1: "sounds/Flam-01.wav",
    2: "sounds/Hat-02.wav",
    3: "sounds/SnrOff-02.wav",
    4: "sounds/Rim-02.wav"
}
color_map = {
    1: "green",
    2: "red",
    3: "yellow",
    4: "blue"
}
latency_light, latency_correct, latency_double, max_tick = 100, 20, 5, 0.02


def process_lighting(color_id: int, intensity: int):
    """
    writes color changes to arduino
    """
    serial.write("{}{}\n".format(color_id, intensity).encode('ascii'))


def process_lights_turn_off(color_id: int, timer: int):
    """
    turns of lights after indication from song_ref
    """
    # TODO adapt color turning off - change only one light at a time, at first red1, red2, red3, then wait and blacken
    # TODO maybe priority queue, where the indication of a next light has priority over the turning off
    sleep(timer)
    process_lighting(color_id, 0)


def update_lights(timeslot: int, _sref, _curr_play):
    """
    set lights on arduino if in reference json
    """

    for j in range(1, 5):

        # if sound played within next 20 timeslots
        if len(_sref[color_map[j]]) > 0 and timeslot + latency_light > _sref[color_map[j]][0]:

            process_lighting(j, 3)

            _curr_play[j - 1] = _sref[color_map[j]][0]

            # update reference and discard fist element
            _sref[color_map[j]] = _sref[color_map[j]][1:]

            # spawn background process to disable light
            Process(target=process_lights_turn_off, args=(j, 1)).start()

            # block to not overwrite serial
            sleep(max_tick)


def tick(timeslot: int, _sref, _curr_ply, _last_ply, _n_corr, _n_insg, _heart_avg):
    """
    function wrapper for process
    """
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
            if _last_ply[data_in - 1] + latency_double < timeslot:

                # blocks until sound int on serial and plays it
                Popen(["afplay", sound_map[data_in]])

                _n_insg.value += 1
                _last_ply[data_in - 1] = timeslot

                # if played in bounds
                if timeslot - latency_correct < _curr_ply[data_in - 1] < timeslot + latency_correct:
                    _n_corr.value += 1
                    _curr_ply[data_in - 1] = -100

    except (ValueError, KeyError, SerialException) as e:
        print(e)
    finally:
        # makes sure process does not return early
        sleep(max_tick)


if __name__ == "__main__":

    # adjust serial port according to arduino connection
    serial = Serial("/dev/cu.usbmodem1421", 115200)

    # init q learning with initial matrix
    qLearning = q_learning.QLearning(
        [calculations.calculate_difficulty_score("songs_json/{}.json".format(song_list[i])) for i in
         range(0, len(song_list))])

    while True:
        # get next song
        current_song_index = qLearning.get_next()
        song_name = song_list[qLearning.get_next()]

        curr_song = Popen(["afplay", "songs/{}.wav".format(song_name)])

        with open("songs_json/{}.json".format(song_name), "r") as song_ref:
            song_ref = load(song_ref)

            # init reference dictionary
            song_ref = Manager().dict({color_map[x]: song_ref[color_map[x]] for x in range(1, 5)})
            sums_ref = sum([len(song_ref[color_map[x]]) for x in range(1, 5)])

            # init scores
            curr_ply, last_ply = Manager().list([-10000] * 4), Manager().list([-10000] * 4)
            n_corr, n_insg, heart_avg = Manager().Value('i', 0), Manager().Value('i', 0), Manager().list()

            # loop over timeslots
            for i in range(maxsize):

                # break if background song is not playing
                if curr_song.poll() is not None:
                    break

                p = Process(target=tick, args=(i, song_ref, curr_ply, last_ply, n_corr, n_insg, heart_avg))
                p.start()

                # wait 20ms for thread
                p.join(max_tick)

                if p.is_alive():
                    p.terminate()
                    p.join()

            score = calculations.calculate_song_score(n_corr.value, n_insg.value, sums_ref, heart_avg)
            print(score)

            # send to Qlearning part
            qLearning.update_q_matrix(current_song_index, score)

            # TODO serial.write("1{}\n".format(score if score >= 10 else "0{}".format(score)).encode('ascii'))
            serial.write("1{}\n".format(99).encode('ascii'))

            sleep(20)
