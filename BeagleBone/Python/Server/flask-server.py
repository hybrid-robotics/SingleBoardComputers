#!/usr/bin/env python
from flask import Flask, render_template
import datetime

#	BeagleBone specific imports
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

from Adafruit_BMP180 import BMP180

bmp180 = BMP180(address=0x77)
  
app = Flask(__name__)

redLED = "P9_14"
greenLED = "P9_16"
blueLED = "P9_21"
whiteLED = "P9_22"

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

@app.route("/")
def rootDir ():
	now = datetime.datetime.now()

	templateData = {
		"title": "My commands and information"
	}

	temp = render_template("root.html", **templateData)
	
	return temp

@app.route("/date")
def currentDateTime ():
	now = datetime.datetime.now()
	timeString = now.strftime("%A, %m/%d/%Y at %I:%M %p %Z")

	templateData = {
		"title": "Current date and time",
		"time": timeString
	}

	temp = render_template("datetime.html", **templateData)
	
	return temp

@app.route("/temp")
def temperature ():
	now = datetime.datetime.now()
	timeString = now.strftime("%A, %m/%d/%Y at %I:%M %p %Z")

	#   Get the Celsius and Fahrenheit temperatures
	celsius = bmp180.readTemperature()
	fahrenheit = (celsius * 1.8) + 32

	templateData = {
		"title": "Current temperature",
		"time": timeString,
		"celsius": celsius,
		"fahrenheit": fahrenheit
	}

	temp = render_template("temperature.html", **templateData)
                            
	return temp            
            
@app.route("/red/<level>")
def redLevel (level):
	return pwmLED(redLED, "Red", level)

@app.route("/green/<level>")
def greenLevel (level):
	return pwmLED(greenLED, "Green", level)
	
@app.route("/blue/<level>")
def blueLevel (level):
	return pwmLED(blueLED, "Blue", level)

@app.route("/white/<level>")
def whiteLevel (level):
	return pwmLED(whiteLED, "White", level)

def pwmLED (led, name, level):
	if isNumber(level):
		levelValue = int(level)
	else:
		levelValue = -1

	if (levelValue >= 0) and (levelValue <= 100):
		PWM.set_duty_cycle(led, float(levelValue))

		if levelValue > 0:
			st = "The " + name + " LED's brightness has been set to " + str(levelValue) + "%."
		elif levelValue == 0:
			st = "The " + name + " LED has been turned off."
	else:
		st = "You have requested an invalid brightness level for the " + name + " LED!!\n\nPlease use numbers from 0 to 100."

	templateData = {
		"title": "Set the " + name + " LED brightness",
		"str": st
	}

	temp = render_template("brightness.html", **templateData)

	return temp

startup()

if __name__ == "__main__":
	app.run(host="192.168.55.60", port=6060)

	PWM.cleanup()
