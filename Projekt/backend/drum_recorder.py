from serial import Serial, SerialException
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


def handle_sound_ext(sid):
    # mapping capacitive sensor to sound
    subprocess.Popen(["afplay", sound_map[int(sid)]])

    # red = 1, green = 2, yellow = 3, blue = 4
    # intensity from 0 to 3 lights activated
    ser.write("{}{}\n".format(sid, 3).encode('ascii'))


def handle_sound_int(sid, timeslot, sd):
    _sd = sd[color_map[sid]]
    _sd.append(timeslot)
    sd[color_map[sid]] = _sd


def tick(timeslot, _sd):
    data = ser.readline()

    sound_id = math.ceil(int(data) / 2)

    handle_sound_ext(sound_id)
    handle_sound_int(sound_id, timeslot, _sd)


# adjust serial port according to arduino connection
ser = Serial("/dev/cu.usbmodem1411", 115200)

# proxy dict to share across different processes
song_desc = Manager().dict({"song_name": input("Enter mp3 filename (w/o ending): "),
                            "green": [], "red": [], "blue": [], "yellow": []})

curr_song = subprocess.Popen(["afplay", "sounds_mp3/{}.mp3".format(song_desc["song_name"])])

# loop over timeslots while song is playing
for i in range(sys.maxsize):

    # break if background song is not playing
    if curr_song.poll() is not None:
        break

    try:

        p = Process(target=tick, name="Tick", args=(i, song_desc))
        p.start()

        # wait 50ms for thread
        p.join(0.05)

        if p.is_alive():
            p.terminate()
            p.join()

    # timeout as accepted failure
    except (TimeoutError, ValueError):
        pass
    except (KeyError, SerialException) as e:
        print(e)

print(song_desc)

with open("sounds_json/{}.json".format(song_desc["song_name"]), "w") as song_res:
    song_res.write(json.dumps(dict(song_desc)))
