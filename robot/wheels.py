import adafruit_pca9685
import board
import busio
import time

class Wheel(object):
    def __init__(self, name, index, forward, backward):
        self.name = name
        self.index = index
        self.forward = forward
        self.backward = backward

FORWARD=3000
STOPPED=0
BACKWARD=10000

FRONT_LEFT = Wheel("Front Left", 0, BACKWARD, FORWARD)
FRONT_RIGHT = Wheel("Front Right", 1, FORWARD, BACKWARD)
BACK_RIGHT = Wheel("Back Right", 2, FORWARD, BACKWARD)
BACK_LEFT = Wheel("Back Left", 3, BACKWARD, FORWARD)

WHEELS = [FRONT_LEFT, FRONT_RIGHT, BACK_LEFT, BACK_RIGHT]

def initialize():
    print("Initializing wheels...")
    global i2c
    global hat
    
    i2c = busio.I2C(board.SCL, board.SDA)
    hat = adafruit_pca9685.PCA9685(i2c)
    hat.frequency = 50
    print("Wheels ready.")

def cleanup():
    print("Stopping wheels...")
    for wheel in WHEELS:
        hat.channels[wheel.index].duty_cycle = 0

    print("Wheels done.")

def calibration_mode():
    for wheel in WHEELS:
        print(f"Calibraring wheel {wheel.name}")
        print("Moving forward...")
        hat.channels[wheel.index].duty_cycle = wheel.forward
        time.sleep(2)
        print("Stopped...")
        hat.channels[wheel.index].duty_cycle = STOPPED
        time.sleep(2)
        print("Moving backward...")
        hat.channels[wheel.index].duty_cycle = wheel.backward
        time.sleep(2)
        print("Stopped...")
        hat.channels[wheel.index].duty_cycle = STOPPED
        time.sleep(2)

def rotate_right():
    hat.channels[FRONT_RIGHT.index].duty_cycle = 15000
    hat.channels[FRONT_LEFT.index].duty_cycle = 15000
    hat.channels[BACK_RIGHT.index].duty_cycle = 15000
    hat.channels[BACK_LEFT.index].duty_cycle = 15000
