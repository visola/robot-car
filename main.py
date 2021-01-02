import logging
import RPi.GPIO as GPIO
import signal
import sys
import time

from pydispatch import dispatcher

import controllers
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

    # started_robot_count = 0
    try:
        x = 0
        while True:
            x += 1
            time.sleep(1)
            # if started_robot_count != green_button_pressed_count:
            #     started_robot_count = green_button_pressed_count
            #     if wheels.current_state == wheels.STATE_STOPPED:
            #         LOGGER.info("Moving forward...")
            #         wheels.move_forward()
            #     else:
            #         LOGGER.info("Stopping...")
            #         wheels.stop()

            # time.sleep(0.1)

    except KeyboardInterrupt:
        LOGGER.info("Interrupted...")
    finally:
        terminate()
