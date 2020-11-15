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
    TITLE = 'banner'
    RANDOM = 'cosmike'
    TOP20 = 'alligator2'


class TERM_COLORS:
    SEASON = '\033[95m'
    EPISODE = '\033[94m'
    TITLE = '\033[33m'
    RANDOM = '\033[32m'
    TOP20 = '\033[35m'
    ENDC = '\033[0m\r'


directory = "/home/pi/media/"

modes = cycle([RANDOM_MODE, TOP20_MODE])
mode = RANDOM_MODE

player = None

top_episode_list = []
# with open('top20.txt') as file:
#     top_episode_list = file.readlines()a
with open('top20.txt') as file:
    for line in file:
        top_episode_list.append(line.strip())

top20_episodes = None

print("🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀")
print("🚀🚀🚀🚀🚀🚀 Simpsons Machine v0.1 🚀🚀🚀🚀🚀🚀🚀🚀")
print("🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀\n\n\n")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(10, GPIO.BOTH)


def get_top():
    next_in_list = next(top20_episodes)
    print("next_in_list", next_in_list)
    next_top_episode = [
        i for i in os.listdir(directory) if i.startswith(next_in_list)
    ][0]
    print("next_top_episode", next_top_episode)
    return next_top_episode


def get_random():
    return random.choice(os.listdir(directory))


def play():
    print("PLAY NEXT...")
    global player

    if player:
        player.quit()

    filename = get_top() if mode == TOP20_MODE else get_random()
    episode = filename.replace('.mp4', '').replace('.mkv', '').split(' - ')

    # render top place if any
    if episode[0] in top_episode_list:
        print(TERM_COLORS.SEASON +
              (Figlet(font=FONTS.SEASON, width=LINE_LENGTH)
               ).renderText('Episode Top#' +
                            str(top_episode_list.index(episode[0]) + 1)) +
              TERM_COLORS.ENDC + "\r")

    print(TERM_COLORS.SEASON +
          (Figlet(font=FONTS.SEASON, width=LINE_LENGTH)
           ).renderText('s ' + episode[0].replace('x', ' e')) +
          TERM_COLORS.ENDC + "\r")

    print(TERM_COLORS.TITLE +
          (Figlet(font=FONTS.TITLE, width=LINE_LENGTH)
           ).renderText(episode[1].replace('ü', 'u').replace('ú', 'u').replace(
               'é', 'e').replace('á', 'a').replace('í', 'i').replace(
                   'ó', 'o').replace('ñ', 'n')) + TERM_COLORS.ENDC)
    time.sleep(2)

    # player = OMXPlayer(Path(directory + filename))
    # player.set_aspect_mode('fill')
    print("\n▶ PLAYING")


def mode_change():
    global mode
    mode = next(modes)
    font = FONTS.RANDOM if mode == RANDOM_MODE else FONTS.TOP20
    color = TERM_COLORS.RANDOM if mode == RANDOM_MODE else TERM_COLORS.TOP20

    global top20_episodes
    if mode == TOP20_MODE:
        top20_episodes = cycle(top_episode_list)

    print(color + (Figlet(font=font, width=170)).renderText(mode) +
          TERM_COLORS.ENDC)
    print("\n\n\n")
    time.sleep(2)
    play()


def check_action(hold_value):
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