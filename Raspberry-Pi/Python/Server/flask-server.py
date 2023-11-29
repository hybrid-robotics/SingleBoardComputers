#!/usr/bin/env python
from flask import Flask, render_template
import datetime

# This is specific to the Raspberry Pi
import RPi.GPIO as GPIO
import RPi.PWM as PWM
from Bit_rPi import Bit, setupRPiGPIO
  
app = Flask(__name__)

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
	PWM.start("P8_13", 100)

@app.route("/")
def rootDir ():
	now = datetime.datetime.now()

	templateData = {
		"title": "My commands and information"
	}

	temp = render_template("root.html", **templateData)
	
	return temp

@app.route("/date")
def currentDateTime():
	now = datetime.datetime.now()
	timeString = now.strftime("%A, %m/%d/%Y at %I:%M %p %Z")

	templateData = {
		"title": "Current date and time",
		"time": timeString
	}

	temp = render_template("datetime.html", **templateData)
	
	return temp

@app.route("/level/<level>")
def pinState (level):
	if isNumber(level):
		levelValue = int(level)
	else:
		levelValue = -1

	if (levelValue >= 0) and (levelValue <= 100):
		PWM.set_duty_cycle("P8_13", float(levelValue))

		st = "The LED's brightness level has been set to " + str(levelValue) + "%."
	else:
		st = "You have requested an invalid LED level!!\n\nPlease use numbers from 0 to 100."

	templateData = {
		"title": "Set LED brightness",
		"str": st
	}

	temp = render_template("brightness.html", **templateData)

	return temp

startup()

if __name__ == "__main__":
	app.run(host="192.168.55.40", port=4040, debug=True)
