#!/usr/bin/env python
'''
	Program:		LedPlay-rPi.py
	Version:		0.1.2
	Date:			20-Oct-2013
	Purpose:		To define fun functions for controlling a set of 8 GPIOs

	Dependencies:	class LedPlay from the file LedPlay-rPi.py

	Copyright (2013) by Dale Weber, hybotics.pdx@gmail.com, @hybotics (Twitter and App.Net)

	ALL Rights Reserved.
'''

# Raspberry Pi specific
from Bit_rPiw import setupRPiGPIO

from LED_rPiw import LED

from hybotics import zilch

from time import sleep

'''
	Start of classes
'''

'''
	There are several fun and useful functions here.
'''
class LedPlay (LED):
	MAX_LED = 5

	LedNames = [ "Led0", "Led1", "Led2", "Led3", "Led4", "Led5", "Led6", "Led7" ]

	BitPins = [ 4, 17, 18, 27, 22, 23, 24, 25 ]

	BitStates = [ False, True, False, True, False, True, False, True ]

	BitValues = [ 1, 2, 4, 8, 16, 32, 64, 128 ]

	LedColors = [ "Yellow", "Red", "Red", "Red", "Red", "Red", "Red", "Green" ]

	Descriptions = [
		"The 1 bit (LSB)",
		"The 2 bit",
		"The 4 bit",
		"The 8 bit",
		"The 16 bit",
		"The 32 bit",
		"The 64 bit",
		"The 128 bit (MSB)"
	]

	LedBlinkRates = [ 250, 250, 250, 250, 250, 250, 250, 250 ]

	LedProcesses = [ None, None, None, None, None, None, None, None ]

	'''
		Our list of LEDs
	'''
	LEDs = []

	'''
		Create our Bits
	'''
	def __init__ (self):
		'''
			Create the list of LEDs
		'''
		for ledNr in range(self.MAX_LED):
			led = LED(self.LedNames[ledNr], self.BitPins[ledNr], self.BitStates[ledNr], self.LedColors[ledNr], self.Descriptions[ledNr], self.LedBlinkRates[ledNr], self.LedProcesses[ledNr])

			# Set the bit number and value for the LED's bit
			led.bit.number = ledNr
			led.bit.value = 2 ** ledNr
			led.bit.status = led.bit.bitStateString("On", "Off")

			self.LEDs.append(led)

		return None

	'''
		Display ALL the important LED information
	'''
	def displayLeds (self):
		status = True
		
		for index in range(self.MAX_LED):
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
		
		for ledNr in range(self.MAX_LED):
			led = self.LEDs[ledNr]
		
			if (led.bit.state):
				ledTotal += led.bit.value
		
		return ledTotal

	'''
		Find a bit in the Bits list
	'''
	def findLed (self, ledFind):
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
	def flipLed (self, ledNr):
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
	def setLeds (self, value):
		status = True

		if (value < 0) or (value > 255):
			print ("There are only EIGHT LEDs, for a range of 0 to 255!")
			status = False
		else:		
			ledValues = []

			'''
				Find out which bits are ON
			'''
			for ledNr in range(self.MAX_LED):
				led = self.LEDs[ledNr]
				ledValues.append(value & led.bit.value)

			'''
				Set each bit according to whether it is ON, or OFF
			'''
			for ledNr in range(self.MAX_LED):
				led = self.LEDs[ledNr]

				if (ledValues[ledNr] > 0):
					led.bit.bit(True)
				else:
					led.bit.bit(False)

		return status		

	'''
		One cycle of the Knight Rider pattern
	'''
	def oneKnightCycle (self, ms):
		# Forward (bit 0 to bit 7)
		for ledNr in range(0, 5, 1):
			led = self.LEDs[ledNr]
			led.bit.toggle(ms)

		# Reverse it (bit 7 to bit 0)
		for ledNr in range(3, -1, -1):
			led = self.LEDs[ledNr]
			led.bit.toggle(ms)

		return None

	'''
		Do the Knight Rider thing..
	'''
	def KnightRider (self, cycles, ms):
		status = True

		self.setLeds(0)
		self.LEDs[0].bit.toggle(ms)

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
			self.setLeds(startCount)
		
			for count in range(startCount, stopCount, direction):
				self.setLeds(count)
				sleep(seconds)

		return status

	'''
		Counting stuff
	'''
	def Counting (self):
		status = True

		cycleTime = 70							# 70 ms
		startCount = 0
		endCount = 31

		pauseSleep = 3

		print ("")
		print ("Counting from 0 to 31 and back down to 0")

		self.BinaryCounter(startCount, endCount, cycleTime)
	
		startCount = 30
		endCount = 0

		self.BinaryCounter(startCount, endCount, cycleTime)

		sleep(pauseSleep)

		'''
			Count from 7 to 31 and back down to 15
		'''
		print ("")
		print ("Counting from 7 to 31, and back down to 7")
		cycleTime = 125							# 125 ms
		startCount = 7
		endCount = 31

		self.BinaryCounter(startCount, endCount, cycleTime)
	
		startCount = 30
		endCount = 7

		self.BinaryCounter(startCount, endCount, cycleTime)
		
		return status

	'''
		This shows how any pattern of LEDs can be setup easily, and how sequences can easily
			be made
	'''
	def Pattern (self, nrCycles, cycleTime):
		status = True

		print ("")
		print ("Starting the pattern..")
		
		pattern = [
			0b10000001,							# Hex 0x81, Decimal 129
			0b01000010,							# Hex 0x42, Decimal  66
			0b00100100,							# Hex 0x24, Decimal  36
			0b00011000,							# Hex 0x18, Decimal  24
			0b00100100,							# Hex 0x24, Decimal  36
			0b01000010,							# Hex 0x42, Decimal  66
		]

		nrCycles = 5
		cycleTime = 200							# 200 ms
		doingPattern = True

		seconds = cycleTime / 1000.0

		while (doingPattern):
			for value in pattern:
				self.setLeds(value)
				print (" The bits value is hex " + hex(value) + " and decimal " + str(value))
				sleep(seconds)
				
			doingPattern = (nrCycles > 0)
			
			nrCycles -= 1

		return status
'''
	End of clase BitPlay
'''

'''
	This is the Demo function
'''
def Demo ():
	'''
		This is a bit of demo code that makes use of various functions in the
			LedPlay class.

		The real power of this class is in the setLeds() function, which allows
			any pattern of LEDs to be setup instantly.
	'''
	status = True
	
	pauseSleep = 3

	'''
		Create our LedPlay() instance
	'''
	play = LedPlay()

	'''
		Do 10 cycles of the Knight Rider pattern, with an on time of 100 ms
	'''
	# Cycle time in ms
	cycleTime = 100							# 150 ms

	# The number of times to do Knight Rider thing
	nrCycles = 10

	print ("")
	print ("Starting the Knight Rider sequence..")
	play.KnightRider(nrCycles, cycleTime)

	sleep(pauseSleep)

	# Count in binary UP from 0 to 31, then down, then up from 7 to 15 and back down
	play.Counting()

	sleep(pauseSleep)
	
	seconds = cycleTime / 1000.0

	'''
		Display the attributes of bit 5
	'''
	play.LEDs[4].display()

	sleep(pauseSleep * 2)

	cycleTime = 750							# 750 ms
	seconds = cycleTime / 1000.0
	
	print ("")
	print ("Setting bits 0, 2, and 4 to ON")
	play.setLeds(0)
	play.ledSet(0, True)
	sleep(seconds)
	play.ledSet(2, True)
	sleep(seconds)
	play.ledSet(4, True)
	sleep(seconds)
	print ("Flipping LED 2..")
	play.flipLed(2)
	sleep(seconds)
	print ("Flipping LED 2..")
	play.flipLed(2)
	sleep(seconds)
	
	value = play.ledsValue()
	print (" The bits value is hex " + hex(value) + " and decimal " + str(value))

	sleep(pauseSleep * 4)

	print ("")
	print ("Setting bits 0 and 4 to OFF")
	play.ledSet(0, False)
	sleep(seconds)
	play.ledSet(4, False)
	sleep(seconds)
	
	value = play.ledsValue()
	print (" The bits value is hex " + hex(value) + " and decimal " + str(value))

	sleep(pauseSleep * 3)
	
	play.setLeds(0)
	return status

'''
	We're just having fun with LEDs here..
'''
if __name__ == '__main__':
	setupRPiGPIO()

	play = LedPlay()

	cycles = 10
	ms = 300
	
	Demo()
