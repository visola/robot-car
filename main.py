import logging
import RPi.GPIO as GPIO
import subprocess
import time

from robot import buttons
from robot import leds
from robot import sensors
from robot import wheels

green_button_pressed_at = 0
green_button_pressed_count = 0

LOG_FORMAT='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
LOGGER = logging.getLogger("robot-car-main")

def green_button_pressed(pressed):
    global green_button_pressed_at
    global green_button_pressed_count
    if pressed:
        green_button_pressed_count += 1
        leds.white_off()
        green_button_pressed_at = time.time()
    else:
        leds.white_on()
        green_button_pressed_at = 0

if __name__ == '__main__':
    LOGGER.info("Initializing robot...")
    GPIO.setmode(GPIO.BCM)
    buttons.initialize()
    leds.initialize()
    sensors.initialize()
    wheels.initialize()

    buttons.add_green_button_handler(green_button_pressed)
    leds.white_on()

    started_robot_count = 0

    try:
        while True:
            if green_button_pressed_at != 0 and time.time() - green_button_pressed_at > 5:
                LOGGER.info("5s passed... shutting down...")
                wheels.stop()
                leds.white_off()
                subprocess.run(["sudo", "shutdown", "-h", "now"], capture_output=True)
                break

            if started_robot_count != green_button_pressed_count:
                started_robot_count = green_button_pressed_count
                if wheels.current_state == wheels.STATE_STOPPED:
                    LOGGER.info("Moving forward...")
                    wheels.move_forward()
                else:
                    LOGGER.info("Stopping...")
                    wheels.stop()

            time.sleep(0.1)

    except KeyboardInterrupt:
        LOGGER.info("Interrupted...")
    finally:
        LOGGER.info("Exiting...")
        LOGGER.info("Cleaning up GPIO...")
        GPIO.cleanup()
        LOGGER.info("Sensors done.")

        wheels.cleanup()
