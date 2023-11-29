#!/usr/bin/env python

import subprocess
import re
import sys
import time
import datetime

from time import sleep
import datetime

from Adafruit_7Segment import SevenSegment
from Adafruit_8x8 import EightByEight, ColorEightByEight
from Adafruit_BMP085 import BMP085

#
#	Bitmaps used for displaying units
#
date_bmp = [
	0B10110110,
	0B01001001,
	0B01001001,
	0B00000100,
	0B00000100,
	0B01111100,
	0B10000100,
	0B01111100
]

year_bmp = [
	0B00000000,
	0B10001000,
	0B10001000,
	0B01110000,
	0B00101011,
	0B00101100,
	0B00101000,
	0B00000000
]

hpa_bmp = [
	0B10001110,
	0B10001001,
	0B11101110,
	0B10101000,
	0B00000100,
	0B00001010,
	0B00011111,
	0B00010001
]

celsius_bmp = [
	0B00000000,
	0B00111100,
	0B01000010,
	0B10000000,
	0B10000000,
	0B01000010,
	0B00111100,
	0B00000000
]

fahrenheit_bmp = [
	0B00000000,
	0B11111100,
	0B10000000,
	0B10000000,
	0B11110000,
	0B10000000,
	0B10000000,
	0B00000000
]

meters_bmp = [
	0B00000000,
	0B00000000,
	0B00000000,
	0B00000000,
	0B11101110,
	0B10111010,
	0B10010010,
	0B10000010
]

am_bmp = [
	0B01110000,
	0B10001010,
	0B10001010,
	0B01110100,
	0B00000000,
	0B00110110,
	0B01001001,
	0B01001001
]

pm_bmp = [
	0B11111100,
	0B10000010,
	0B10000010,
	0B11111100,
	0B10000000,
	0B10110110,
	0B01001001,
	0B01001001
]

percent_bmp = [
	0B01000011,
	0B10100110,
	0B01001100,
	0B00011000,
	0B00110000,
	0B01100010,
	0B11000101,
	0B10000010
]

allon_bmp = [
	0B11111111,
	0B11111111,
	0B11111111,
	0B11111111,
	0B11111111,
	0B11111111,
	0B11111111,
	0B11111111
]

#
# Draw a bit map (BMP) graphic
#
def drawBitMap (display, bMap, color=1):
	display.clear()

	for y in range(8):
		for x in range(7, -1, -1):
			if (bMap[y] & (2 ** x)):
				display.setPixel(7 - x, y, color)

#
# Draw a bit map (BMP) graphic mirrored
#
def drawBitMapMirrored (display, bMap, color=1):
	display.clear()

	for y in range(8):
		for x in range(8):
			if (bMap[y] & (2 ** x)):
				display.setPixel(x, y, color)

#
#	Write a floating point value to the 7-Segment display
#
def writeFloat (display, value, decimal=2, noblank=False):
	digitCount = 0
	decimalPoint = False

	temp = int(value / 100)

	#	Set first digit of integer portion
	if noblank or (temp > 9):
		decimalPoint = ((digitCount + 1) == decimal)
		display.writeDigit(0, int(temp / 10), decimalPoint)		# Tens
	else:
		display.clear()

	#	Set the second digit of the integer portion
	digitCount += 1
	decimalPoint = ((digitCount + 1) == decimal)

	display.writeDigit(1, temp % 10, decimalPoint)				# Ones

	#	Set the first digit of the decimal portion
	temp = value % 100
	digitCount += 1
	decimalPoint = ((digitCount + 1) == decimal)

	display.writeDigit(3, int(temp / 10), decimalPoint)			# Tens

	#	Set the second digit of the decimal portion
	digitCount += 1
	decimalPoint = ((digitCount + 1) == decimal)

	display.writeDigit(4, temp % 10, decimalPoint)				# Ones

#
# ======================================================================================================
# Clock using the DS1307 RTC, 7-segment and matrix 8x8 displays, and 10DOF IMU for temperature readings
# ======================================================================================================
#
#	Green 4 digit 7-Segment Display at address 0x70
sevenSeg = SevenSegment(address=0x70)

#	Green Mini Matrix 8x8 Display at address 0x73
matrix8x8 = EightByEight(address=0x73)

#	Bi-Color Matrix 8x8 Display at address 0x73
#bicolor8x8 = ColorEightByEight(address=0x73)

#	Don't have to change the rotation for the mini 8x8 matrix displays
#matrix8x8.setRotation(3)
#bicolor8x8.setRotation(3)

print "Press CTRL+C to exit"

#	Display test
writeFloat(sevenSeg, 8888, 0, False)
sevenSeg.setColon(True)
drawBitMap(matrix8x8, allon_bmp)
sleep(5)

sevenSeg.setColon(False)

#
#	Settings variables that control the loops and frequency of displays
#
maxSeconds = 45
dateFreq = 15.0
loopCount = 0
displayColor = 3

#
#	Flag variables that cause various things to be displayed when there are changes.
#
displayAmPm = None
displayCleared = None
amTime = None
lastYear = None
lastDate = None
lastMinute = None
lastHour = None

#
#	Continually update the time on a 4 digit 7-segment display
#
while (True):
	now = datetime.datetime.now()

	month = now.month
	day = now.day
	year = now.year

	date = (month * 100) + day

	displayDate = (loopCount / dateFreq) == int(loopCount / dateFreq)

	if displayDate or (lastDate != date):
		writeFloat(sevenSeg, date, 0, True)
		drawBitMap(matrix8x8, date_bmp)
#		drawBitMap(bicolor8x8, date_bmp)

		sleep(5)
		maxSeconds -= 5

	if (lastYear != year):
		writeFloat(sevenSeg, year, 0, True)
		drawBitMap(matrix8x8, year_bmp)
#		drawBitMap(bicolor8x8, year_bmp)

		sleep(5)
		maxSeconds -= 5

	count = 0

	while (count < maxSeconds):
		hour = now.hour

		lastAmTime = amTime

		if hour > 11:
			hour = hour - 12
			amTime = False
		else:
			amTime = True

		if hour == 0:
			hour = 12

		minute = now.minute
		second = now.second

		#	Turn colon on
		sevenSeg.setColon(True)

		if displayCleared or (lastHour != hour):
			#	Set hours
			if hour > 9:
				sevenSeg.writeDigit(0, int(hour / 10))	# Tens
			else:
				#	Clear the 7 segment display
				sevenSeg.clear()
				displayCleared = True

			sevenSeg.writeDigit(1, hour % 10)			# Ones
			
		#	Only display if minute has changed or display was cleared
		if displayCleared or (lastMinute != minute):
			#	Set minutes
			sevenSeg.writeDigit(3, int(minute / 10))	# Tens
			sevenSeg.writeDigit(4, minute % 10)			# Ones

		#	Only display if time has changed from AM to PM or PM to AM, or the display was cleared
		if displayCleared or (lastAmTime != amTime):
			#	Display the am / pm indicator
			if amTime:
				drawBitMap(matrix8x8, am_bmp)
#				drawBitMap(bicolor8x8, am_bmp, displayColor)
			else:
				drawBitMap(matrix8x8, pm_bmp)
#				drawBitMap(bicolor8x8, pm_bmp, displayColor)

		#	Wait one second
		sleep(1)

		#	Count seconds
		count += 1

		lastHour = hour
		lastMinute = minute

		displayCleared = False

		#	Turn colon off
		sevenSeg.setColon(False)
		#	End of while(count < countLimit)

	#	Turn colon off
	sevenSeg.setColon(False)

	# Run the DHT program to get the humidity and temperature readings!
	output = subprocess.check_output(["./Adafruit_DHT", "2302", "4"]);

	matches = re.search("Temp =\s+([0-9.]+)", output)

	if (not matches):
		time.sleep(3)
		continue

	#	Get the temperatures
	celsius = float(matches.group(1))
	fahrenheit = (celsius * 1.8) + 32
      
	#	Search for humidity printout
	matches = re.search("Hum =\s+([0-9.]+)", output)

	if (not matches):
		time.sleep(3)
		continue

	#	Get the humidity
	humidity = float(matches.group(1))

	print ("Temperature: " + str(celsius) + " C")
	print ("Temperature: " + str(fahrenheit) + " F")
	print ("Humidity:    " + str(humidity) + " %")
	print ("")
 
	#	Display the Celsius temperature
	celsius = int(celsius * 100)

	#	Display the Fahrenheit temperature
	fahrenheit = int(fahrenheit * 100)

	writeFloat(sevenSeg, fahrenheit, 2)
	drawBitMap(matrix8x8, fahrenheit_bmp)
#	drawBitMap(bicolor8x8, f_bmp, displayColor)
	sleep(7)

	writeFloat(sevenSeg, celsius, 2)
	drawBitMap(matrix8x8, celsius_bmp)
#	drawBitMap(bicolor8x8, c_bmp, displayColor)
	sleep(7)

	humidity = int(humidity * 100)

	writeFloat(sevenSeg, humidity, 2)
	drawBitMap(matrix8x8, percent_bmp)
	sleep(7)

	maxSeconds = 45
	lastDate = date
	lastYear = year

	displayCleared = True
	displaydate = False

	loopCount += 1
	
	if (loopCount > 65000):
		loopCount = 0
	#	End of while(True)
