#!/usr/bin/env python3
import RPi.GPIO as GPIO
import os
import random
import sys
import time
from omxplayer.player import OMXPlayer
from pathlib import Path
from itertools import cycle
from pyfiglet import Figlet

LINE_LENGTH = 80
RANDOM_MODE = "Random-Mode"
TOP20_MODE = "Top#20-Mode"


class FONTS:
    SEASON = 'ogre'
    EPISODE = 'ogre'
    TITLE = 'roman'
    RANDOM = 'cosmike'
    TOP20 = 'larry3d'


class term_colors:
    SEASON = '\033[95m'
    TITLE = '\033[33m'
    RANDOM = '\033[32m'
    TOP20 = '\033[31m'
    ENDC = '\033[0m\r'


directory = "/home/pi/media/"

modes = cycle([RANDOM_MODE, TOP20_MODE])
mode = RANDOM_MODE

player = None

print("🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀")
print("🚀🚀🚀🚀🚀🚀 Simpsons Machine v0.1 🚀🚀🚀🚀🚀🚀🚀🚀")
print("🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀\n\n\n")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(10, GPIO.BOTH)


def get_top():
    print("top")
    return '07x20 - Bart recorre el mundo.mp4'


def get_random():
    return random.choice(os.listdir(directory))


def play():
    print("PLAY NEXT...")
    global player

    if player:
        player.quit()

    filename = get_top() if mode == TOP20_MODE else get_random()
    episode = filename.replace('.mp4', '').replace('.mkv', '').split(' - ')

    print(episode)
    print(term_colors.SEASON + (Figlet(font=FONTS.SEASON, width=LINE_LENGTH)
                                ).renderText('s ' + episode[0].split('x')[0]) +
          term_colors.ENDC + "\r")

    print(term_colors.EPISODE +
          (Figlet(font=FONTS.EPISODE, width=LINE_LENGTH)
           ).renderText('e ' + episode[0].split('x')[1]) + term_colors.ENDC)

    print(term_colors.TITLE +
          (Figlet(font=FONTS.TITLE, width=LINE_LENGTH)
           ).renderText(episode[1].replace('ü', 'u').replace('ú', 'u').replace(
               'é', 'e').replace('á', 'a').replace('í', 'i').replace(
                   'ó', 'o').replace('ñ', 'n')) + term_colors.ENDC)
    time.sleep(2)

    # player = OMXPlayer(Path(directory + filename))
    # player.set_aspect_mode('fill')
    print("\n▶ PLAYING")


def mode_change():
    global mode
    mode = next(modes)
    print("MODE CHANGE", mode)
    font = FONTS.RANDOM if mode == RANDOM_MODE else FONTS.TOP20
    color = term_colors.RANDOM if mode == RANDOM_MODE else term_colors.TOP20

    print(color + (Figlet(font=font, width=170)).renderText(mode) +
          term_colors.ENDC)
    print("\n\n\n")
    time.sleep(2)
    play()


def check_action(hold_value):
    print("hold_value", hold_value)

    if hold_value < 20000:
        play()
        return

    mode_change()


hold = 0
zero_value_check = 0

mode_change()

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