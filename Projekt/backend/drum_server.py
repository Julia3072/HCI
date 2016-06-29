from json import dumps, loads
from math import ceil
from multiprocessing import Process, Manager
from serial import Serial, SerialException
from subprocess import Popen
from sys import maxsize

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


def handle_sound(sid):
    # mapping capacitive sensor to sound
    Popen(["afplay", sound_map[int(sid)]])


def process_lighting(color_id, intensity):
    # red = 1, green = 2, yellow = 3, blue = 4
    # intensity from 0 to 3 lights activated
    serial.write("{}{}\n".format(color_id, intensity).encode('ascii'))


# function wrapper for process
def tick(timeslot, _sd):
    try:

        data = serial.readline()

        sound_id = ceil(int(data) / 2)

        handle_sound(sound_id)

    except ValueError:
        pass
    except (KeyError, SerialException) as e:
        print(e)


# adjust serial port according to arduino connection
serial = Serial("/dev/cu.usbmodem1411", 115200)
song_name = input("Enter mp3 filename (w/o ending): ")
curr_song = Popen(["afplay", "sounds_mp3/{}.mp3".format(song_name)])

with open("sounds_json/{}.json".format(song_name), "r") as song_res:
    song_res = loads(song_res.readlines()[0])

    # loop over timeslots while song is playing
    for i in range(maxsize):

        # break if background song is not playing
        if curr_song.poll() is not None:
            break

        # TODO check lists for close events

        if song_res["red"][0] == i:
            tmp = song_res["red"]
            tmp.pop(0)
            song_res["red"] = tmp
            print(i)
            handle_sound(1)
            process_lighting(1, 3)
        else:
            process_lighting(1, 0)

        p = Process(target=tick, name="Tick", args=(i, song_res))
        p.start()

        # wait 50ms for thread
        p.join(0.05)

        if p.is_alive():
            p.terminate()
            p.join()
