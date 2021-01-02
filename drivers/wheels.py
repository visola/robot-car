import adafruit_pca9685
import board
import busio
import logging
import time

import dispatcher

LOGGER = logging.getLogger("robot-car-wheels")

FORWARD=3000
STOPPED=0
BACKWARD=10000

STATE_FORWARD = 0
STATE_ROTATING_RIGHT = 1
STATE_STOPPED = 2

class Wheel(object):
    def __init__(self, name, index, forward, backward):
        self.name = name
        self.index = index
        self.forward = forward
        self.backward = backward

class WheelController(object):
    def __init__(self, front_left, front_right, back_right, back_left):
        self.front_left = front_left
        self.front_right = front_right
        self.back_right = back_right
        self.back_left = back_left
        self.wheels = [front_left, front_right, back_left, back_right]
        self.current_state = STATE_STOPPED

        dispatcher.connect(
            lambda: self.move_forward(),
            signal = "/wheels/forward"
        )

        dispatcher.connect(
            lambda: self.stop(),
            signal = "/wheels/stop"
        )

    def calibration_mode(self):
        for wheel in self.wheels:
            LOGGER.info(f"Calibraring wheel {wheel.name}")
            LOGGER.info("Moving forward...")
            hat.channels[wheel.index].duty_cycle = wheel.forward
            time.sleep(2)
            LOGGER.info("Stopped...")
            hat.channels[wheel.index].duty_cycle = STOPPED
            time.sleep(2)
            LOGGER.info("Moving backward...")
            hat.channels[wheel.index].duty_cycle = wheel.backward
            time.sleep(2)
            LOGGER.info("Stopped...")
            hat.channels[wheel.index].duty_cycle = STOPPED
            time.sleep(2)

    def move_forward(self):
        hat.channels[self.front_left.index].duty_cycle = self.front_left.forward
        hat.channels[self.front_right.index].duty_cycle = self.front_right.forward
        hat.channels[self.back_left.index].duty_cycle = self.back_left.forward
        hat.channels[self.back_right.index].duty_cycle = self.back_right.forward
        self.current_state = STATE_FORWARD

    def rotate_right(self):
        hat.channels[self.front_left.index].duty_cycle = self.front_left.forward
        hat.channels[self.back_left.index].duty_cycle = self.back_left.forward
        
        hat.channels[self.front_right.index].duty_cycle = self.front_right.backward
        hat.channels[self.back_right.index].duty_cycle = self.back_right.backward

        self.current_state = STATE_ROTATING_RIGHT

    def stop(self):
        hat.channels[self.front_left.index].duty_cycle = STOPPED
        hat.channels[self.back_left.index].duty_cycle = STOPPED
        hat.channels[self.front_right.index].duty_cycle = STOPPED
        hat.channels[self.back_right.index].duty_cycle = STOPPED
        self.current_state = STATE_STOPPED

def initialize():
    LOGGER.info("Initializing wheels...")
    global i2c
    global hat
    global wheel_controller

    i2c = busio.I2C(board.SCL, board.SDA)
    hat = adafruit_pca9685.PCA9685(i2c)
    hat.frequency = 50
    
    wheel_controller = WheelController(
        front_left = Wheel("Front Left", 0, BACKWARD, FORWARD),
        front_right = Wheel("Front Right", 1, FORWARD, BACKWARD),
        back_right = Wheel("Back Right", 2, FORWARD, BACKWARD),
        back_left = Wheel("Back Left", 3, BACKWARD, FORWARD),
    )
    LOGGER.info("Wheels ready.")

def cleanup():
    LOGGER.info("Stopping wheels...")
    for wheel in wheel_controller.wheels:
        hat.channels[wheel.index].duty_cycle = 0

    LOGGER.info("Wheels done.")
