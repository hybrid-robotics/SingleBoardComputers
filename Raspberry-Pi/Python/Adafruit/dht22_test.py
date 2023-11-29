#!/usr/bin/env python

import subprocess
import re
import sys
import time
import datetime

#	Continuously take readings
while(True):
	# Run the DHT program to get the humidity and temperature readings!

	output = subprocess.check_output(["./Adafruit_DHT", "2302", "4"]);
	print ("Output = " + output + "'")

	matches = re.search("Temp =\s+([0-9.]+)", output)

	if (not matches):
		time.sleep(3)
		continue

	#	Get the temperatures
	celsius = float(matches.group(1))
	fahrenheit = (celsius * 1.8) + 32

	# search for humidity printout
	matches = re.search("Hum =\s+([0-9.]+)", output)

	if (not matches):
		time.sleep(3)
		continue

	#	Get the humidity
	humidity = float(matches.group(1))

	print ("Temperature: " + str(celsius) + " C")
	print ("Temperature: " + str(fahrenheit) + " F")
	print ("Humidity:    " + str(humidity) + " %")

	#	Wait 30 seconds before continuing
	time.sleep(30)
