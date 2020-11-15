# Import Raspberry Pi GPIO library
import RPi.GPIO as GPIO


def button_down(channel):
    print("DOWN")


def button_up(channel):
    print("UP")


# Ignore warning for now
GPIO.setwarnings(False)
# Use physical pin numbering
GPIO.setmode(GPIO.BOARD)
# Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# Setup event on pin 10 rising edge
GPIO.add_event_detect(10, GPIO.RISING, callback=button_down)
GPIO.add_event_detect(10, GPIO.LOWERING, callback=button_down)
# Run until someone presses enter
message = input("Press enter to quit\n\n")
# Clean up
GPIO.cleanup()