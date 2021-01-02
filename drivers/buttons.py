import logging
import RPi.GPIO as GPIO
import time

import dispatcher

LOGGER = logging.getLogger("robot-car-buttons")

class ButtonDriver(object):
    def __init__(self, name, gpio):
        self.name = name
        self.gpio = gpio
        self.value = False

        GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(
            gpio,
            GPIO.BOTH,
            callback=lambda channel: self.handle_event(channel)
        )

    def handle_event(self, channel):
        new_value = GPIO.input(channel) == GPIO.HIGH

        if self.value == new_value:
            return

        self.value = new_value
        dispatcher.send(signal=f"/button/{self.name}", on=new_value)

def initialize():
    LOGGER.info("Initializing buttons...")
    ButtonDriver("green", 22)
    LOGGER.info("Buttons ready.")
