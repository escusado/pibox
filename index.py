# Import Raspberry Pi GPIO library
import RPi.GPIO as GPIO
import os
import random
from pyfiglet import Figlet


class term_colors:
    SEASON = '\033[95m'
    EPISODE = '\033[36m'
    TITLE = '\033[33m'
    ENDC = '\033[0m\r'


directory = "/home/pi/media/"

print("🚀 Simpsons Machine v0.1")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(10, GPIO.BOTH)


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
          (Figlet(font='roman', width=170)
           ).renderText(episode[1].replace('ü', 'u').replace('ú', 'u').replace(
               'é', 'e').replace('á', 'a').replace('í', 'i').replace(
                   'ó', 'o').replace('ñ', 'n')) + term_colors.ENDC)


def long_click():
    print("LONG")
    print(term_colors.TITLE +
          (Figlet(font='roman', width=170)).renderText('Top #20') +
          term_colors.ENDC)


def check_action(hold_value):
    print("hold_value", hold_value)

    if hold_value < 20000:
        short_click()
        return

    long_click()


hold = 0
zero_value_check = 0

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