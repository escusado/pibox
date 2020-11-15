#!/usr/bin/env python3
import RPi.GPIO as GPIO
import os
import random
import sys
import time
from pyfiglet import Figlet

RANDOM_MODE = "Random-Mode"
TOP20_MODE = "Top#20-Mode"


class term_colors:
    SEASON = '\033[95m'
    EPISODE = '\033[36m'
    TITLE = '\033[33m'
    ENDC = '\033[0m\r'


directory = "/home/pi/media/"

mode = sys.argv[1] if len(sys.argv) > 1 else RANDOM_MODE

print("🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀")
print("🚀🚀🚀🚀🚀🚀 Simpsons Machine v0.1 🚀🚀🚀🚀🚀🚀🚀🚀")
print("🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀\n\n\n")
print(term_colors.EPISODE +
      (Figlet(font='cosmike', width=170)).renderText(mode) + term_colors.ENDC)
print("\n\n\n")
time.sleep(2)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(10, GPIO.BOTH)


def short_click():
    print("LONG RESTART IN OTHER MODE")
    os.system("pwd")


def long_click():
    print("LONG RESTART IN OTHER MODE")


def check_action(hold_value):
    print("hold_value", hold_value)

    if hold_value < 20000:
        short_click()
        return

    long_click()


hold = 0
zero_value_check = 0

filename = random.choice(os.listdir(directory))
episode = filename.replace('.mp4', '').replace('.mkv', '').split(' - ')

print(episode)
print(term_colors.SEASON +
      (Figlet(font='ogre', width=170)).renderText('s ' +
                                                  episode[0].split('x')[0]) +
      term_colors.ENDC)

print(term_colors.EPISODE +
      (Figlet(font='ogre', width=170)).renderText('e ' +
                                                  episode[0].split('x')[1]) +
      term_colors.ENDC)

print(term_colors.TITLE + (Figlet(font='roman', width=170)).renderText(
    episode[1].replace('ü', 'u').replace('ú', 'u').replace('é', 'e').replace(
        'á', 'a').replace('í', 'i').replace('ó', 'o').replace('ñ', 'n')) +
      term_colors.ENDC)
time.sleep(2)
os.system("killall omxplayer")
os.system("omxplayer '" + directory + filename + "' &")
print("\n▶ PLAYING")

while True:
    if GPIO.input(10) == 0:
        if hold > 0:
            zero_value_check += 1

        if zero_value_check > 5:
            check_action(hold)
            zero_value_check = 0
            hold = 0

    else:
        hold += 1