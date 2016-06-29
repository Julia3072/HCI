import serial
import signal
import subprocess
import math
import sys
import json

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


def handle_sound_int(sid, sdesc, timeslot):
    sdesc[color_map[sid]].append(timeslot)


ser = serial.Serial("/dev/cu.usbmodem1411", 115200)

song_name = input("Enter mp3 filename (w/o ending): ")
curr_song = subprocess.Popen(["afplay", "sounds_json/{}.mp3".format(song_name)])

signal.signal(signal.SIGALRM, TimeoutError)

with open("sounds_json/{}.json".format(song_name), 'r', encoding='utf-8') as song_res:

    song_res = json.loads(song_res.readlines()[0])
    red, blue, green, yellow = list(song_res["red"]), song_res["blue"], song_res["green"], song_res["yellow"]

    print(song_res)

    # loop over timeslots while song is playing
    for i in range(sys.maxsize):

        if curr_song.poll() is not None:
            break

        try:

            # steps of 10ms
            signal.setitimer(signal.ITIMER_REAL, .01)

            if len(red) > 0 and red[0] == i:
                handle_sound_ext(1)
                red.pop(0)
                print(red)

            '''
            data = ser.readline()

            sound_id = math.ceil(int(data) / 2)

            handle_sound_ext(sound_id)
            handle_sound_int(sound_id, song_desc, i)
            '''

        # timeout as accepted failure
        except TimeoutError:
            pass
        except (ValueError, KeyError, serial.SerialException) as e:
            print(e)
