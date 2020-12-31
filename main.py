import time

from robot import sensors
from robot import wheels

if __name__ == '__main__':
    print("Initializing robot...")
    sensors.initialize()
    wheels.initialize()

    try:
        print("Robot is running...")
        wheels.calibration_mode()

        # while True:
        #     distance = sensors.distance_north()
        #     if distance < 10:
        #         print(f"Distance north: {distance}, turning right...")
        #         wheels.rotate_right()
                
        #     if distance > 10:
                
            
        #     time.sleep(1)

    except KeyboardInterrupt:
        print("Interrupted...")
    finally:
        print("Exiting...")
        sensors.cleanup()
        wheels.cleanup()
