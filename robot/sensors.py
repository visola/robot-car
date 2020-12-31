import RPi.GPIO as GPIO
import time

class Sensor(object):
    def __init__(self, name, trigger, echo):
        self.name = name
        self.trigger = trigger
        self.echo = echo

NORTH = Sensor("N", 23, 24)
# NORTWEST = Sensor("NW", 15, 14)
# NORTEAST = Sensor("NE", 17, 27)
# SOUTH = Sensor("S", 22, 10)

SENSORS = [NORTH]

def initialize():
    print("Initializing sensors...")
    for sensor in SENSORS:
        print(f"Initializing sensor: {sensor.name}")
        GPIO.setup(sensor.trigger, GPIO.OUT)
        GPIO.setup(sensor.echo, GPIO.IN)
    print("Sensors initialized.")

def distance(sensor):
	GPIO.output(sensor.trigger, True)
	
	time.sleep(0.00001)
	GPIO.output(sensor.trigger, False)
	
	StartTime = time.time()
	StopTime = time.time()
	
	# save StartTime
	while GPIO.input(sensor.echo) == 0:
		StartTime = time.time()
	
	while GPIO.input(sensor.echo) == 1:
		StopTime = time.time()
	
	return (StopTime - StartTime) * 17150

def distance_north():
    return distance(NORTH)
