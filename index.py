# Import Raspberry Pi GPIO library
import RPi.GPIO as GPIO
import datetime

now = 0


def short_click():
    print("SHORT")


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
        print("time_diff", time_diff)
        if time_diff < 1000:
            return

        if time_diff < 10000:
            short_click()
            return

        if time_diff < 30000:
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