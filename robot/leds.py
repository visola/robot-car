import RPi.GPIO as GPIO

WHITE_LED = 17

def initialize():
    print("Initializing LEDS...")
    GPIO.setup(WHITE_LED, GPIO.OUT, initial=GPIO.LOW)
    print("LEDS ready.")


def white_on():
    GPIO.output(WHITE_LED, GPIO.HIGH)

def white_off():
    GPIO.output(WHITE_LED, GPIO.LOW)
