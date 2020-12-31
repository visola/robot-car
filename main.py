import RPi.GPIO as GPIO
import subprocess
import time

from robot import buttons
from robot import leds
from robot import sensors
from robot import wheels

green_button_pressed_at = 0
green_button_pressed_count = 0

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
    print("Initializing robot...")
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
                print("5s passed... shutting down...")
                wheels.stop()
                subprocess.run(["sudo", "shutdown", "-h", "now"], capture_output=True)
                break

            if started_robot_count != green_button_pressed_count:
                started_robot_count = green_button_pressed_count
                if wheels.current_state == wheels.STATE_STOPPED:
                    print("Moving forward...")
                    wheels.move_forward()
                else:
                    print("Stopping...")
                    wheels.stop()

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Interrupted...")
    finally:
        print("Exiting...")
        print("Cleaning up GPIO...")
        GPIO.cleanup()
        print("Sensors done.")

        wheels.cleanup()
