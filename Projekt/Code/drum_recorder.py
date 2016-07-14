#!/usr/bin/env python3

from json import dump
from math import ceil
from multiprocessing import Process, Manager
from serial import Serial, SerialException
from subprocess import Popen
from sys import maxsize
from time import sleep


from Code import drum_server as ds

'''
recording drum sounds for reference values
'''


def handle_sound_ext(sid):
    """
    mapping capacitive sensor to sound/light
    """
    Popen(["afplay", ds.sound_map[int(sid)]])

    # red = 1, green = 2, yellow = 3, blue = 4
    # intensity from 0 to 3 lights activated
    serial.write("{}{}\n".format(sid, 3).encode('ascii'))


def handle_sound_int(sid, timeslot, sd):
    """
    add color/timeslot to json
    """
    sd[ds.color_map[sid]] = sd[ds.color_map[sid]] + [timeslot]


def tick(timeslot, _sd, _curr_ply):
    """
    function wrapper for process
    """
    try:

        data = serial.readline()
        print(data)

        sound_id = ceil(int(data) / 2)

        # disregard double recognition
        if _curr_ply[sound_id - 1] + ds.latency_double < timeslot:
            _curr_ply[sound_id - 1] = timeslot

            handle_sound_ext(sound_id)
            handle_sound_int(sound_id, timeslot, _sd)

    except ValueError:
        pass
    except (KeyError, SerialException) as e:
        print(e)
    finally:
        sleep(ds.max_tick)


if __name__ == "__main__":

    # adjust serial port according to arduino connection
    serial = Serial("/dev/cu.usbmodem1411", 115200)

    # proxy dict to share across different processes
    song_desc = Manager().dict({"song_name": input("Enter filename (w/o ending): "),
                                "green": [], "red": [], "blue": [], "yellow": []})

    curr_song = Popen(["afplay", "songs/{}.wav".format(song_desc["song_name"])])

    curr_ply = Manager().list([-10000] * 4)

    # TODO save timestamps
    # loop over timeslots while song is playing
    for i in range(maxsize):

        # break if background song is not playing
        if curr_song.poll() is not None:
            break

        p = Process(target=tick, name="Tick", args=(i, song_desc, curr_ply))
        p.start()

        # wait 20ms for thread
        p.join(ds.max_tick)

        if p.is_alive():
            p.terminate()
            p.join()

    print(song_desc)

    with open("songs_json/{}.json".format(song_desc["song_name"]), "w") as song_res:
        dump(dict(song_desc), song_res)
