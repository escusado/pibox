# Import Raspberry Pi GPIO library
import RPi.GPIO as GPIO
import datetime
import os
import random
from pyfiglet import Figlet


class bcolors:
    INDEX = '\033[95m'
    TITLE = '\033[33m'
    ENDC = '\033[0m'


directory = "/home/pi/media/"

now = 0


def short_click():
    episode = random.choice(os.listdir(directory)).replace('.mp4', '').replace(
        '.mkv', '').split(' - ')

    print(bcolors.INDEX + (Figlet(font='ogre', width=180)
                           ).renderText(episode[0].replace('x', ' - ')) +
          bcolors.ENDC)
    print(bcolors.TITLE +
          (Figlet(font='nancyj', width=180)).renderText(episode[1]) +
          bcolors.ENDC)

    print("SHORT", episode)


def mid_click():
    print("MID")


def long_click():
    print("LONG")


def button_callback(channel):
    global now
    if GPIO.input(10):
        now = datetime.datetime.now()
    else:
        time_diff = (datetime.datetime.now() - now).microseconds

        if time_diff < 4000:
            return

        if time_diff < 300000:
            short_click()
            return

        if time_diff < 500000:
            mid_click()
            return

        long_click()


# Ignore warning for now
GPIO.setwarnings(False)
# Use physical pin numbering
GPIO.setmode(GPIO.BOARD)
# Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# Setup event on pin 10 rising edge
GPIO.add_event_detect(10, GPIO.BOTH, callback=button_callback)
# Run until someone presses enter
message = input("Press enter to quit\n\n")
# Clean up
GPIO.cleanup()