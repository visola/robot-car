import logging
import RPi.GPIO as GPIO

LOGGER = logging.getLogger("robot-car-leds")

WHITE_LED = 17

def initialize():
    LOGGER.info("Initializing LEDS...")
    GPIO.setup(WHITE_LED, GPIO.OUT, initial=GPIO.LOW)
    LOGGER.info("LEDS ready.")

def white_on():
    GPIO.output(WHITE_LED, GPIO.HIGH)

def white_off():
    GPIO.output(WHITE_LED, GPIO.LOW)
