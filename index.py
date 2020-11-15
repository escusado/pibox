# Import Raspberry Pi GPIO library
import RPi.GPIO as GPIO
import datetime
import os
import random
from pyfiglet import Figlet


class term_colors:
    SEASON = '\033[95m'
    EPISODE = '\033[36m'
    TITLE = '\033[33m'
    ENDC = '\033[0m\r'


directory = "/home/pi/media/"

now = 0


def short_click():
    episode = random.choice(os.listdir(directory)).replace('.mp4', '').replace(
        '.mkv', '').split(' - ')

    print(episode)
    print(term_colors.SEASON + (Figlet(font='ogre', width=170)
                                ).renderText('s ' + episode[0].split('x')[0]) +
          term_colors.ENDC)

    print(term_colors.EPISODE +
          (Figlet(font='ogre', width=170)
           ).renderText('e ' + episode[0].split('x')[1]) + term_colors.ENDC)

    print(term_colors.TITLE +
          (Figlet(font='larry3d', width=170)
           ).renderText(episode[1].replace('ü', 'u').replace('ú', 'u').replace(
               'é', 'e').replace('á', 'a').replace('í', 'i').replace(
                   'ó', 'o').replace('ñ', 'n')) + term_colors.ENDC)


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