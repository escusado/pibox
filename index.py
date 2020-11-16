#!/usr/bin/env python3

# by http://toy.codes 2020

import RPi.GPIO as GPIO
import os
import random
import sys
import time
import datetime
from omxplayer.player import OMXPlayer
from pathlib import Path
from itertools import cycle
from pyfiglet import Figlet

LINE_LENGTH = 128
RANDOM_MODE = "Random Mode"
TOP20_MODE = "T o p # 20 M o d e"
STOPPED_STATUS = "Stopped"


class FONTS:
    SEASON = 'small'
    TITLE = 'roman'
    RANDOM = 'cosmike'
    TOP20 = 'alligator2'
    APP = 'basic'


class TERM_COLORS:
    TOP20 = '\033[36m'
    RANDOM = '\033[32m'
    TITLE = '\033[33m'
    ENDC = '\033[0m\r'
    APP = '\033[35m'


directory = "/home/pi/media/"

modes = cycle([RANDOM_MODE, TOP20_MODE])
mode = RANDOM_MODE

player = None

top_episode_list = []
with open('top20.txt') as file:
    for line in file:
        top_episode_list.append(line.strip())
top20_episodes = None

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(10, GPIO.BOTH)


def present():
    print("\n\n\n")

    with open('logo.txt') as file:
        print(file.read())

    print(TERM_COLORS.APP + (Figlet(font=FONTS.APP, width=LINE_LENGTH)
                             ).renderText('Simpsons Machine v0.1') +
          TERM_COLORS.ENDC)

    print(TERM_COLORS.RANDOM + '[by http://toy.codes]' + TERM_COLORS.ENDC)

    time.sleep(5)

    print("\n\n\n")


def get_top():
    next_in_list = next(top20_episodes)
    next_top_episode = [
        i for i in os.listdir(directory) if i.startswith(next_in_list)
    ][0]
    return next_top_episode


def get_random():
    return random.choice(os.listdir(directory))


def play():
    global player

    if player:
        player.quit()

    filename = get_top() if mode == TOP20_MODE else get_random()
    episode = filename.replace('.mp4', '').replace('.mkv', '').split(' - ')
    color = TERM_COLORS.RANDOM
    isTop = ''

    # render top place if any
    if episode[0] in top_episode_list:
        isTop = 'Top# ' + str(20 - top_episode_list.index(episode[0])) + ' : '
        color = TERM_COLORS.TOP20

    print("\n\n\n Playing...")
    print(color + (Figlet(font=FONTS.SEASON, width=LINE_LENGTH)
                   ).renderText(isTop + 's' + episode[0].replace('x', ' e')) +
          TERM_COLORS.ENDC + "\r")

    print(TERM_COLORS.TITLE +
          (Figlet(font=FONTS.TITLE, width=LINE_LENGTH)
           ).renderText(episode[1].replace('ü', 'u').replace('ú', 'u').replace(
               'é', 'e').replace('á', 'a').replace('í', 'i').replace(
                   'ó', 'o').replace('ñ', 'n')) + TERM_COLORS.ENDC)

    player = OMXPlayer(Path(directory + filename))
    player.set_aspect_mode('fill')


def mode_change():
    if player:
        player.quit()
    global mode
    mode = next(modes)
    font = FONTS.RANDOM if mode == RANDOM_MODE else FONTS.TOP20
    color = TERM_COLORS.RANDOM if mode == RANDOM_MODE else TERM_COLORS.TOP20

    global top20_episodes
    if mode == TOP20_MODE:
        top20_episodes = cycle(top_episode_list)

    print("\n\n\nStart...")
    print(color + (Figlet(font=font, width=170)).renderText(mode) +
          TERM_COLORS.ENDC)

    time.sleep(3)
    play()


def check_action(hold_value):
    diff = datetime.datetime.now() - started_press_time
    hold_time = (diff.days * 86400000) + (diff.seconds *
                                          1000) + (diff.microseconds / 1000)
    print(hold_time)
    if hold_value < 50:
        play()
        return

    mode_change()


hold = 0
zero_value_check = 0
started_press_time = None

present()
mode_change()

while True:
    if bool(player) == False:
        play()

    if GPIO.input(10) == 0:
        if hold > 0:
            zero_value_check += 1

        if zero_value_check > 5:
            check_action(hold)
            zero_value_check = 0
            hold = 0

    else:
        hold += 1
        if hold == 1:
            started_press_time = datetime.datetime.now()
