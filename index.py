#!/usr/bin/env python3
import RPi.GPIO as GPIO
import os
import random
import sys
import time
from omxplayer.player import OMXPlayer
from pathlib import Path
from pyfiglet import Figlet

LINE_LENGTH = 80
RANDOM_MODE = "Random-Mode"
TOP20_MODE = "Top#20-Mode"


class term_colors:
    SEASON = '\033[95m'
    EPISODE = '\033[36m'
    TITLE = '\033[33m'
    ENDC = '\033[0m\r'


directory = "/home/pi/media/"

mode = sys.argv[1] if len(sys.argv) > 1 else RANDOM_MODE

player = None

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


def play():
    print("PLAY NEXT...")
    global player

    if player:
        player.quit()

    filename = random.choice(os.listdir(directory))
    episode = filename.replace('.mp4', '').replace('.mkv', '').split(' - ')

    print(episode)
    print(term_colors.SEASON + (Figlet(font='ogre', width=LINE_LENGTH)
                                ).renderText('s ' + episode[0].split('x')[0]) +
          term_colors.ENDC + "\r")

    print(term_colors.EPISODE +
          (Figlet(font='ogre', width=LINE_LENGTH)
           ).renderText('e ' + episode[0].split('x')[1]) + term_colors.ENDC)

    print(term_colors.TITLE +
          (Figlet(font='roman', width=LINE_LENGTH)
           ).renderText(episode[1].replace('ü', 'u').replace('ú', 'u').replace(
               'é', 'e').replace('á', 'a').replace('í', 'i').replace(
                   'ó', 'o').replace('ñ', 'n')) + term_colors.ENDC)
    time.sleep(2)

    player = OMXPlayer(Path(directory + filename))
    player.set_aspect_mode('fill')
    print("\n▶ PLAYING")


def mode_change():
    print("MODE CHANGE")


def check_action(hold_value):
    print("hold_value", hold_value)

    if hold_value < 20000:
        play()
        return

    mode_change()


hold = 0
zero_value_check = 0

play()

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