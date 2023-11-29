#!/usr/bin/env python
import math
from Adafruit_LSM303 import Adafruit_LSM303
from time import sleep

lsm303 = Adafruit_LSM303()

'''
	Round a real (floating point) value to the closest integer
'''
def round (real):
	decimal = real - int(real)
	
	if (decimal >= 0.5):
		result = int(real + 0.5)
	else:
		result = int(real)

	return result

while True:
	readings = lsm303.read()

	accel = readings[0]
	mag = readings[1]

	print ("Accelerometer X, Y, Z: " + str(accel))
	print ("Magnetometer X, Y, Z, orientation: " + str(mag))

	heading = (math.atan2(mag[1], mag[0]) * 180) / math.pi;

	print ("Raw heading: " + str(heading))
 
 	#	Normalize to 0 - 360
 	if (heading < 0): 
		 heading = 360 + heading;

#	heading = math.ceil(heading)
 
	print ("Normalized Heading (0 - 360 degrees): " + str(round(heading)))
	print ("")

	# Output is fun to watch if this is commented out
	sleep(1)
