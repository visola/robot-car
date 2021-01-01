import logging
import RPi.GPIO as GPIO

LOGGER = logging.getLogger("robot-car-buttons")

GREEN_BUTTON = 22

green_button_handlers = []
green_button_value = False

def initialize():
    LOGGER.info("Initializing buttons...")
    GPIO.setup(GREEN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(GREEN_BUTTON,GPIO.BOTH,callback=handle_green_button_press)
    LOGGER.info("Buttons ready.")


def add_green_button_handler(handler):
    green_button_handlers.append(handler)

def handle_green_button_press(channel):
    global green_button_value
    new_value = GPIO.input(channel) == GPIO.HIGH

    if green_button_value == new_value:
        return

    green_button_value = new_value

    for handler in green_button_handlers:
        handler(new_value)
