import logging

from controllers import shutdown

LOGGER = logging.getLogger("robot-car-driver")

def initialize():
    LOGGER.info("Initializing controllers...")
    shutdown.ShutdownListener()
    LOGGER.info("Controllers ready.")
