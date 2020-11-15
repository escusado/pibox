# Import Raspberry Pi GPIO library
import RPi.GPIO as GPIO


def button_callback(channel):
    if GPIO.input(10):
        print("Rising edge detected on 25")
    else:
        print("Falling edge detected on 25")


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