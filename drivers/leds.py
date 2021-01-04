import logging
import RPi.GPIO as GPIO

import dispatcher

LOGGER = logging.getLogger("robot-car-leds")

WHITE_LED = 17

def initialize():
    LOGGER.info("Initializing LEDS...")
    GPIO.setup(WHITE_LED, GPIO.OUT, initial=GPIO.LOW)
    dispatcher.connect(handle_white_led, signal="/led/white")
    dispatcher.connect(
        lambda: GPIO.output(WHITE_LED, GPIO.LOW),
        signal="/system/shutdown"
    )
    LOGGER.info("LEDS ready.")

def handle_white_led(on=True):
    LOGGER.debug("Led signal received: %r", on)
    GPIO.output(WHITE_LED, GPIO.HIGH if on else GPIO.LOW)
