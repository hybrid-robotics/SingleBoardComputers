#!/usr/bin/env python
import datetime
from time import sleep

#	BeagleBone specific imports
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

redLED = "P9_14"
greenLED= "P9_16"
blueLED = "P9_21"
whiteLED = "P9_22"

leds = [
	{ "pin" : redLED, "color" : "Red" },
	{ "pin" : greenLED, "color" : "Green" },
	{ "pin" : blueLED, "color" : "Blue" },
	{ "pin" : whiteLED, "color" : "White" }
]

ledColors = [ "Red", "Green", "Blue", "White" ]

pwmLED = blueLED

#
#	Returns True if s is a number
#
def isNumber(s):
	x = str(s)

	if x.isdigit():
		result = True
	else:
		result = False
	
	return result

def startup ():
	PWM.start(redLED, 0)
	PWM.start(greenLED, 0)
	PWM.start(blueLED, 0)
	PWM.start(whiteLED, 0)

def pwmLED (led, name, level):
	if isNumber(level):
		levelValue = int(level)
	else:
		levelValue = -1

	if (levelValue >= 0) and (levelValue <= 100):
		PWM.set_duty_cycle(led, float(levelValue))

		st = "The " + name + " LED's brightness level has been set to " + str(levelValue) + "%."
	else:
		st = "You have requested an invalid LED level!!\n\nPlease use numbers from 0 to 100."

	return st

startup()


for LED in leds:
	for duty in range(0, 110, 10):
		print (pwmLED(LED["pin"], LED["color"], duty))
		sleep(0.5)

sleep(5)
PWM.cleanup()
