#!/usr/bin/env python
'''
	Program:		LEDPlay2_bone.py
	Version:		0.1.2
	Date:			22-Oct-2013
	Purpose:		To define fun functions for controlling a set of 8 GPIOs

	Dependencies:	class LEDPlay2 from the file LEDPlay-rPi.py

	Copyright (2013) by Dale Weber, hybotics.pdx@gmail.com, @hybotics (Twitter and App.Net)

	ALL Rights Reserved.
'''

# For coroutines
from greenlet import greenlet

# Raspberry Pi specific
from LED_bone import LED

# Hybotics utilities
from hybotics import zilch

from time import sleep

'''
	Start of classes
'''

'''
	There are several fun and useful functions here.
'''
class LEDPlay2 (LED):
	LEDNames = [ "Led0", "Led1", "Led2", "Led3", "Led4" ]

	BitPins = [  "P9_14", "P9_15", "P9_16", "P9_21", "P9_22" ]

	BitStates = [ False, False, False, False, False ]

	BitValues = [ 1, 2, 4, 8, 16 ]

	LEDColors = [ "Red", "Red", "Red", "Red", "Red" ]

	Descriptions = [
		"The 1 bit (LSB)",
		"The 2 bit",
		"The 4 bit",
		"The 8 bit",
		"The 16 bit (MSB)"
	]

	LEDBlinkRates = [ 250, 250, 250, 250, 250 ]

	LEDProcesses = [ None, None, None, None, None ]

	'''
		Our list of LEDs
	'''
	maxLEDs = 5
	LEDs = []

	'''
		Status LEDs used for various functions
	'''
	StatusNames = [ "Green", "Yellow", "Red" ]

	StatusPins = [ "P9_11", "P9_12", "P9_13" ]

	StatusColors = [ "Green", "Yellow", "Red" ]

	StatusBlinkRates = [ 200, 150, 75 ]

	StatusDescriptions = [
		"Heartbeat",
		"Green LED",
		"Red LED"
	]

	maxStatusLEDs = 3
	StatusLEDs = []

	'''
		Create our LEDs
	'''
	def __init__ (self):
		'''
			Create the list of regular LEDs
		'''
		for ledNr in range(self.maxLEDs):
			led = LED(self.LEDNames[ledNr], self.BitPins[ledNr], self.BitStates[ledNr], self.LEDColors[ledNr], self.Descriptions[ledNr], self.LEDBlinkRates[ledNr], self.LEDProcesses[ledNr])

			# Set the bit number and value for the LED's bit
			led.bit.number = ledNr
			led.bit.value = 2 ** ledNr
			led.bit.status = led.bit.bitStateString("On", "Off")

			self.LEDs.append(led)

		'''
			Create our Status LEDs
		'''
		for ledNr in range(self.maxStatusLEDs):
			led = LED(self.StatusNames[ledNr], self.StatusPins[ledNr], False, self.StatusColors[ledNr], self.StatusDescriptions[ledNr])

			# Set the bit number and value for the LED's bit
			led.bit.number = ledNr
			led.bit.value = 2 ** ledNr
			led.bit.status = led.bit.bitStateString("On", "Off")

			self.StatusLEDs.append(led)

		return None

	'''
		Display ALL the important LED information
	'''
	def displayLEDs (self):
		status = True
		
		for index in range(self.maxLEDs):
			led = ledStuff.LEDs[index]
			bit = led.bit
		
			print ("")
			print ("Status for LED:")
			print ("")
			print ("  Name:        " + zilch(led.name))
			print ("  Description: " + zilch(led.description))
			print ("  LED Status:  " + zilch(led.status))
			print ("")
			print ("  Bit Number:  " + zilch(str(bit.number)))
			print ("  Bit Value:   " + zilch(str(bit.value)))
			print ("  Bit Status:  " + zilch(bit.status))
			
		return status
		
	'''
		Return the value of the bits that are currently set (the LED is on)
	'''
	def ledsValue (self):
		status = True
		
		ledTotal = 0
		
		for ledNr in range(self.maxLEDs):
			led = self.LEDs[ledNr]
		
			if (led.bit.state):
				ledTotal += led.bit.value
		
		return ledTotal

	'''
		Find a bit in the Bits list
	'''
	def findLED (self, ledFind):
		status = True
		foundNr = None
		
		ledName = ledFind.lower()

		ledNr = 0
		nrLEDs = len(self.LEDs)

		while (foundNr == None) and (ledNr < nrLEDs):
			listName = self.LEDs[ledNr].name.lower()

			if (listName == ledName):
				foundNr = ledNr

			ledNr += 1

		status = (foundNr != None)

		if (not status):
			foundIndex = None

		return ( status, foundNr )

	'''
		Flip a bit, by bit number
	'''
	def flipLED (self, ledNr):
		status = True

		if (ledNr < 0) or (ledNr > 7):
			print ("There are only 8 LEDs, numbered 0 through 7!")
			status = False
		else:
			led = self.LEDs[ledNr]
			
			if led.bit.state:
				led.bit.bit(False)
			else:
				led.bit.bit(True)
				
		return status

	def heartBeat (self, ms):
		status = True

		self.StatusLEDs[0].bit.toggle(ms)
		
		return status

	'''
		Set an LED on or off
	'''
	def ledSet (self, ledNr, ledState):
		status = True

		if (ledNr < 0) or (ledNr > 7):
			print ("There are only 8 LEDs, numbered 0 through 7!")
			status = False
		elif (ledState == None):
			print ("Invalid LED state!")
			status = False
		else:
			led = self.LEDs[ledNr]
			led.bit.bit(ledState)

		return status

	'''
		Allows setting all 8 LEDs to any value, within 0 to 255
	'''
	def setLEDs (self, value):
		status = True

		if (value < 0) or (value > 255):
			print ("There are only EIGHT LEDs, for a range of 0 to 255!")
			status = False
		else:		
			ledValues = []

			'''
				Find out which bits are ON
			'''
			for ledNr in range(self.maxLEDs):
				led = self.LEDs[ledNr]
				ledValues.append(value & led.bit.value)

			'''
				Set each bit according to whether it is ON, or OFF
			'''
			for ledNr in range(self.maxLEDs):
				led = self.LEDs[ledNr]

				if (ledValues[ledNr] > 0):
					led.bit.bit(True)
				else:
					led.bit.bit(False)

		return status		

	'''
		Blink three LEDs at different rates simultaneously
	'''
	def TriBlink (self, cycles):
		status = True

		# List of greenlets for the LEDs
		blinkers = []

		ledNr = 0

		# Create greenlets for each LED, and add them to the list
		while (ledNr < maxStatusLEDs):
			led = self.StatusLEDs[ledNr]

			gr = greenlet(led.blinkProcess)
			blinkers.append(gr)

			ledNr += 1

		nrCycles = 0

		while (nrCycles < cycles):
			ledNr = 0

			while (ledNr < self.maxStatusLEDs):
				blinky = blinkers[ledNr]
				blinky.switch(StatusBlinkRates[ledNr])

			nrCycles += 1

		return status

	'''
		One cycle of the Knight Rider pattern
	'''
	def oneKnightCycle (self, ms):
		# Forward (bit 0 to bit 4)
		for ledNr in range(1, 4, 1):
			led = self.LEDs[ledNr]
			led.bit.toggle(ms)

		# Reverse it (bit 5 to bit 0)
		for ledNr in range(4, -1, -1):
			led = self.LEDs[ledNr]
			led.bit.toggle(ms)

		return None

	'''
		Do the Knight Rider thing..
	'''
	def KnightRider (self, cycles, ms):
		status = True

		self.setLEDs(0)
		self.heartBeat(200)

		if (cycles > 0):
			# Run for a set number of cycles
			for c in range(cycles + 1):
				self.oneKnightCycle(ms)
		elif (cycles == 0):
			# Run infinitely
			while True:
				self.oneKnightCycle(ms)
		else:
			# Can't run negative cycles!
			print ("Negative cycles are not permitted!")
			status = False
			
		return status

	'''
		Eight bit binary up/down counter with a variable start/stop count.
	'''
	def BinaryCounter (self, startCount, endCount, onTimeMs):
		status = True
		stopCount = 0

		if (startCount < 0) or (startCount > 31):
			print ("The starting count is out of range!")
			status = False
		elif (endCount < 0) or (endCount > 31):
			print ("The ending count is out of range!")
			status = False

		if status:
			# Set the count direction (up = 1, down = -1)
			if (startCount < endCount):
				direction = 1
				stopCount = endCount + 1
				dir = "Up"
			elif (startCount > endCount):
				stopCount = endCount - 1
				direction = -1
				dir = "Down"
		
			print ("Starting the Binary " + dir + " Counting sequence..")

			# Convert ms to seconds for sleep()
			seconds = onTimeMs / 1000.0

			# Set the starting count value
			self.setLEDs(startCount)
		
			for count in range(startCount, stopCount, direction):
				self.setLEDs(count)
				sleep(seconds)

		return status

	'''
		Counting stuff
	'''
	def Counting (self, cycleTime):
		status = True

		startCount = 0
		endCount = 31

		pauseSleep = 3

		print ("")
		print ("Counting from 0 to 31 and back down to 0")

		self.BinaryCounter(startCount, endCount, cycleTime)
	
		startCount = 30
		endCount = 0

		self.BinaryCounter(startCount, endCount, cycleTime)

		self.heartBeat(200)
		sleep(pauseSleep)

		'''
			Count from 15 to 31 and back down to 15
		'''
		cycleTime = 250							# 250 ms
		startCount = 15
		endCount = 31

		print ("")
		print ("Counting from 15 to 31, and back down to 15")
		self.BinaryCounter(startCount, endCount, cycleTime)
	
		startCount = 30
		endCount = 15

		self.BinaryCounter(startCount, endCount, cycleTime)
		
		return status
'''
	End of clase LEDPlay2
'''

'''
	This is the Demo function
'''
def Demo ():
	'''
		This is a bit of demo code that makes use of various functions in the
			LEDPlay class.

		The real power of this class is in the setLEDs() function, which allows
			any pattern of LEDs to be setup instantly.
	'''
	status = True

	pauseSleep = 3
	
	'''
		Create our LEDPlay() instance
	'''
	play = LEDPlay2()

	'''
		Do 5 cycles of the Knight Rider pattern, with an on time of 100 ms
	'''
	# Cycle time in ms
	cycleTime = 75							# 75 ms

	# The number of times to do Knight Rider thing
	nrCycles = 5

	print ("")
	print ("Starting the Knight Rider sequence..")
	play.KnightRider(nrCycles, cycleTime)

	play.heartBeat(200)
	sleep(pauseSleep)

	# Count in binary UP from 0 to 63, then up from 15 to 31 and back down
	play.Counting(85)

	play.heartBeat(200)
	sleep(pauseSleep)
	
	seconds = cycleTime / 1000.0

	'''
		Display the attributes of bit 5
	'''
	play.LEDs[4].display()

	play.heartBeat(200)
	sleep(pauseSleep * 2)

	cycleTime = 750							# 750 ms
	seconds = cycleTime / 1000.0
	
	print ("")
	print ("Setting bits 0, 2, and 4 to ON")
	play.setLEDs(0)
	play.ledSet(0, True)
	sleep(seconds)
	play.ledSet(2, True)
	sleep(seconds)
	play.ledSet(4, True)
	sleep(seconds)
	print ("Flipping LED 2..")
	play.flipLED(2)
	sleep(seconds)
	print ("Flipping LED 2..")
	play.flipLED(2)
	sleep(seconds)
	
	value = play.ledsValue()
	print ("The bits value is hex " + hex(value) + " and decimal " + str(value))

	play.heartBeat(200)
	sleep(pauseSleep * 4)

	print ("")
	print ("Setting bit 2 OFF")
	play.ledSet(2, False)
	sleep(seconds)
	
	value = play.ledsValue()
	print ("The bits value is hex " + hex(value) + " and decimal " + str(value))

	play.heartBeat(200)
	sleep(pauseSleep * 2)
	
	return status

'''
	We're just having fun with LEDs here..
'''
if __name__ == '__main__':
	play = LEDPlay2()

	cycles = 20
	ms = 300
	
#	play.displayLEDs()

#	Demo()

#	play.KnightRider(cycles, ms)

	play.TriBlink(cycles)
