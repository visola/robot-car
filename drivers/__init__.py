import logging

from drivers import buttons
from drivers import leds
from drivers import sensors
from drivers import wheels

LOGGER = logging.getLogger("robot-car-driver")

def initialize():
    LOGGER.info("Initializing drivers...")
    buttons.initialize()
    leds.initialize()
    sensors.initialize()
    wheels.initialize()
    LOGGER.info("Drivers initialized.")

def cleanup():
    LOGGER.info("Shutting drivers down...")
    wheels.cleanup()
    LOGGER.info("Drivers off.")
