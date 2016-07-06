from json import dump
from math import ceil
from multiprocessing import Process, Manager
from serial import Serial, SerialException
from subprocess import Popen
from sys import maxsize

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


def handle_sound_ext(sid):
    # mapping capacitive sensor to sound
    Popen(["afplay", sound_map[int(sid)]])

    # red = 1, green = 2, yellow = 3, blue = 4
    # intensity from 0 to 3 lights activated
    serial.write("{}{}\n".format(sid, 3).encode('ascii'))


# add color/timeslot to json
def handle_sound_int(sid, timeslot, sd):
    sd[color_map[sid]] = sd[color_map[sid]] + [timeslot]


# function wrapper for process
def tick(timeslot, _sd):
    try:

        data = serial.readline()
        print(data)

        sound_id = ceil(int(data) / 2)

        handle_sound_ext(sound_id)
        handle_sound_int(sound_id, timeslot, _sd)

    except ValueError:
        pass
    except (KeyError, SerialException) as e:
        print(e)


# adjust serial port according to arduino connection
serial = Serial("/dev/cu.usbmodem1411", 115200)

# proxy dict to share across different processes
song_desc = Manager().dict({"song_name": input("Enter mp3 filename (w/o ending): "),
                            "green": [], "red": [], "blue": [], "yellow": []})

curr_song = Popen(["afplay", "sounds_mp3/{}.mp3".format(song_desc["song_name"])])

# loop over timeslots while song is playing
for i in range(maxsize):

    # break if background song is not playing
    if curr_song.poll() is not None:
        break

    p = Process(target=tick, name="Tick", args=(i, song_desc))
    p.start()

    # wait 20ms for thread
    p.join(0.02)

    if p.is_alive():
        p.terminate()
        p.join()

print(song_desc)

with open("sounds_json/{}.json".format(song_desc["song_name"]), "w") as song_res:
    # TODO from dumps to dump test
    song_res.write(dump(dict(song_desc)))
