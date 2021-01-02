import logging
import RPi.GPIO as GPIO
import signal
import sys
import time

import controllers
import dispatcher
import drivers
import logger

LOGGER = logging.getLogger("robot-car-main")

terminating = False
def terminate(signum=None, frame=None):
    global terminating
    if terminating:
        return

    terminating = True
    if signum is not None:
        LOGGER.info("Received signal: %d", signum)
    LOGGER.info("Exiting...")
    LOGGER.info("Cleaning up GPIO...")
    GPIO.cleanup()
    LOGGER.info("Sensors done.")
    drivers.cleanup()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, terminate)
    LOGGER.info("Initializing robot...")
    GPIO.setmode(GPIO.BCM)
    drivers.initialize()
    controllers.initialize()

    dispatcher.send(signal="/led/white", on=True)
    dispatcher.connect(terminate, signal="/system/shutdown")

    dispatcher.send("/wheels/forward")
    time.sleep(5)
    dispatcher.send("/wheels/stop")

    try:
        while True:
            if terminating:
                break
            time.sleep(0.1)

    except KeyboardInterrupt:
        LOGGER.info("Interrupted...")
    finally:
        terminate()
