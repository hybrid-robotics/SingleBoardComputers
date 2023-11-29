#!/usr/bin/env python

from time import sleep
import datetime

from Adafruit_7Segment import SevenSegment
from Adafruit_8x8 import EightByEight, ColorEightByEight
from Adafruit_BMP085 import BMP085

#
#	Bitmaps used for displaying units
#
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

c_bmp = [
	0B01110000,
	0B10001000,
	0B10000000,
	0B10001000,
	0B01110000,
	0B00000000,
	0B00000000,
	0B00000000
]

f_bmp = [
	0B11111000,
	0B10000000,
	0B11100000,
	0B10000000,
	0B10000000,
	0B00000000,
	0B00000000,
	0B00000000
]

m_bmp = [
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

# Draw a bit map (BMP) graphic
def drawBitMap (display, bMap, color=None):
	display.clear()

	if color == None:
		color = 1

	for y in range(8):
		for x in range(7, -1, -1):
			if (bMap[y] & (2 ** x)):
				display.setPixel(7 - x, y, color)

# Draw a bit map (BMP) graphic mirrored
def drawBitMapMirrored (display, bMap, color=None):
	display.clear()

	if color == None:
		color = 1

	for y in range(8):
		for x in range(8):
			if (bMap[y] & (2 ** x)):
				display.setPixel(x, y, color)

def writeFloat (display, value, decimal=2):
	digitCount = 0
	decimalPoint = False

	temp = int(value / 100)

	#	Set first digit of integer portion
	if temp > 9:
		decimalPoint = ((digitCount + 1) == decimal)
		display.writeDigit(0, int(temp / 10), decimalPoint)	# Tens
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

	display.writeDigit(3, int(temp / 10), decimalPoint)					# Tens

	#	Set the second digit of the decimal portion
	digitCount += 1
	decimalPoint = ((digitCount + 1) == decimal)

	display.writeDigit(4, temp % 10, decimalPoint)						# Ones

# ===========================================================================
# Clock Example
# ===========================================================================
#	Yellow 4 digit 7-Segment Display at address 0x70
sevenSeg = SevenSegment(address=0x70)

#	Yellow Matrix 8x8 Display at address 0x71
matrix8x8 = EightByEight(address=0x71)

#	Bi-Color Matrix 8x8 Display at address 0x73
#bicolor8x8 = ColorEightByEight(address=0x73)

matrix8x8.setRotation(3)
#bicolor8x8.setRotation(3)

bmp180 = BMP085(address=0x77)

print "Press CTRL+C to exit"

countLimit = 45
displayAmPm = None
displayCleared = None
displayColor = 3
amTime = None
lastMinute = None
lastHour = None

#	Continually update the time on a 4 char, 7-segment display
while(True):
	count = 0

	while(count < countLimit):
		now = datetime.datetime.now()

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

		if displayCleared or (lastHour != hour):
			#	Set hours
			if hour > 9:
				sevenSeg.writeDigit(0, int(hour / 10))	# Tens
				displayCleared = False
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

		#	Toggle colon at 1 Hz
		sevenSeg.setColon(second % 2)

		#	Wait one second
		sleep(1)

		#	Count seconds
		count += 1

		lastHour = hour
		lastMinute = minute

		displayCleared = False
		#	End of while(count < countLimit)

	#	Turn colon off
	sevenSeg.setColon(False)

	#	Get the Celsius and Fahrenheit temperatures
	celsius = bmp180.readTemperature()
	fahrenheit = (celsius * 1.8) + 32

	#	Display the Celsius temperature
	celsius = int(celsius * 100)

	writeFloat(sevenSeg, celsius, 2)
	drawBitMap(matrix8x8, c_bmp)
#	drawBitMap(bicolor8x8, c_bmp, displayColor)
	sleep(7)

	#	Display the Fahrenheit temperature
	fahrenheit = int(fahrenheit * 100)

	writeFloat(sevenSeg, fahrenheit, 2)
	drawBitMap(matrix8x8, f_bmp)
#	drawBitMap(bicolor8x8, f_bmp, displayColor)
	sleep(7)

	displayCleared = True
	#	End of while(True)
