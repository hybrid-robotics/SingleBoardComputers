#!/usr/bin/env python
'''
	Program:		LedPlay-rPi.py
	Version:		0.1.2
	Date:			20-Oct-2013
	Purpose:		To define fun functions for controlling a set of 8 GPIOs

	Dependencies:	class BitPlay from BitPlay-rPi.py

	Copyright (2013) by Dale Weber, hybotics.pdx@gmail.com, @hybotics (Twitter and App.Net)

	ALL Rights Reserved.
'''
                            
import pprint

from time import sleep

# Raspberry Pi specific
from Bit-rPi import Bit, setupRPiGPIO
'''
	Start of classes
'''

'''
	There are several fun and useful functions here.
'''
class BitsList (Bit):
	BitNames = [ "yellow", "red", "Led2", "Led3", "Led4", "Led5", "Led6", "green" ]

	BitPins = [ 4, 17, 18, 27, 22, 23, 24, 25 ]

	BitStates = [ False, False, False, False, False, False, False, False ]

	BitColors = [ "Yellow", "Red", "Red", "Red", "Red", "Red", "Red", "Green" ]

	BitDescriptions = [
		"The 1 bit (LSB)",
		"The 2 bit",
		"The 4 bit",
		"The 8 bit",
		"The 16 bit",
		"The 32 bit",
		"The 64 bit",
		"The 128 bit (MSB)"
	]

	BitBlinkRates = [ 250, 250, 250, 250, 250, 250, 250, 250]

	BitProcesses = [ None, None, None, None, None, None, None ]

	'''
		Our list of LEDs
	'''
	Bits = []

	'''
		Create our Bits
	'''
	def __init__ (self):
		'''
			Initialize the Raspberry Pi GPIO class
		'''
		self.setupRPiGPIO()

		'''
			Create the list of LEDs
		'''
		for bitNr in range(8):
			bit = Bit(self.BitNames[bitNr], self.BitPins[bitNr], self.BitStates[bitNr], self.BitDescriptions[bitNr], self.BitBlinkRates[bitNr], self.BitProcesses[bitNr])
			bstatus = self.bitStateString("On", "Off")

			bit.status = lstatus

			LEDs.append(led)

			# Set or Reset the bit the LED is attached to
			self.led.bit.bit(BitStates[ledNr])

		return None

	'''
		Return the value of the bits that are currently set (the LED is on)
	'''
	def bitsValue (self):
		status = True
		
		bitValue = 0
		
		for bitNr in range(8):
			if (self.BitStates[bitNr]):
				bitValue += self.BitValues[bitNr]
		
		return bitValue

	'''
		Find a bit in the Bits list
	'''
	def findLED (self, ledName):
		status = True
		foundIndex = None

		ledIndex = 0
		nrLeds = len(self.LEDs)

		while (foundIndex == None) and (ledIndex < nrLeds):
			if (self.LedNames[ledIndex] == ledName)
				foundIndex = ledIndex

			ledIndex += 1

		status = (foundIndex != None)

		if (not status):
			foundIndex = None

		return ( status, foundIndex )

	'''
		Allows setting all 8 LEDs to any value, within 0 to 255
	'''
	def setBits (self, value):
		status = True

		if (value < 0) or (value > 255):
			print ("There are only EIGHT LEDs, for a range of 0 to 255!")
			status = False
		else:		
			bitValues = []

			'''
				Find out which bits are ON
			'''
			for bitNr in range(8):
				bitValues.append(value & self.BitValues[bitNr])

			'''
				Set each bit according to whether it is "on", or "off"
				
				We also update the BitStates list.
			'''
			for bitNr in range(8):
				if (bitValues[bitNr] > 0):
					self.LEDs[bitNr].bit(True)
					self.BitStates[bitNr] = True
				else:
					self.LEDs[bitNr].bit(False)
					self.BitStates[bitNr] = False

		return status		

	'''
		One cycle of the Knight Rider pattern
	'''
	def oneKnightCycle (self, onTimeMs):
		for bitNr in range(1, 7, 1):
			self.LEDs[bitNr].bit.toggle(onTimeMs)

		for bitNr in range(7, -1, -1):
			self.LEDs[bitNr].bit.toggle(onTimeMs)

		return None

	'''
		Do the Knight Rider thing..
	'''
	def KnightRider (self, onTimeMs, cycles):
		status = True
	
		self.Bits[0].wink(onTimeMs)

		if (cycles > 0):
			# Run for a set number of cycles
			for c in range(cycles + 1):
				self.oneKnightCycle(onTimeMs)
		elif (cycles == 0):
			# Run infinitely
			while True:
				self.oneKnightCycle(onTimeMs)
		else:
			# Can't run negative cycles!
			print ("Negative cycles is not permitted!")
			status = False
			
		return status

	'''
		Eight bit binary up/down counter with a variable start/stop count.
	'''
	def BinaryCounter (self, startCount, endCount, onTimeMs):
		status = True
		stopCount = 0

		if (startCount < 0) or (startCount > 255):
			print ("The starting count is out of range!")
			status = False
		elif (endCount < 0) or (endCount > 255):
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
			self.setBits(startCount)
		
			for count in range(startCount, stopCount, direction):
				self.setBits(count)
				sleep(seconds)

		return status

	'''
		This shows how any pattern of LEDs can be setup easily, and how sequences can easily
			be made
	'''
	def Pattern (self, nrCycles, cycleTime):
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
				play.setBits(value)
				print (" The bits value is hex " + hex(value) + " and decimal " + str(play.bitsValue()))
				sleep(seconds)
				
			doingPattern = (nrCycles > 0)
			
			nrCycles -= 1

		# Put our bits to bed
		play.setBits(0)

		sleep(pauseSleep)
	
'''
	End of clase BitPlay
'''

'''
	We're just having fun with bits and LEDs here..
'''

if __name__ == '__main__':
	'''
		This is a bit of demo code that makes use of various functions in the BitPlay class.

		The real power of this class is in the setBits() function, which allows any pattern
			of LEDs to be setup instantly.
	'''

	# Initialize the Raspberry Pi GPIOs
	setupRPiGPIO()

	pauseSleep = 3

	'''
		Create our BitPlay() instance
	'''
	play = BitPlay()

	'''
		Do 5 cycles of the Knight Rider pattern, with an on time of 100 ms
	'''
	# Cycle time in ms
	cycleTime = 75							# 75 ms

	# The number of times to do Knight Rider thing
	nrCycles = 5

	print ("")
	print ("Starting the Knight Rider sequence..")
	play.KnightRider(cycleTime, nrCycles)

	sleep(pauseSleep)

	# Count in binary UP from 0 to 255, with an on time of 100 ms
	cycleTime = 65							# 65 ms
	startCount = 0
	endCount = 255

	print ("")
	print ("Counting from 0 to 255 and back down to 0")

	play.BinaryCounter(startCount, endCount, cycleTime)
	
	startCount = 254
	endCount = 0

	play.BinaryCounter(startCount, endCount, cycleTime)

	sleep(pauseSleep)
	
	'''
		Count from 15 to 63 and back down to 15
	'''
	cycleTime = 200							# 200 ms
	startCount = 15
	endCount = 63

	print ("")
	print ("Counting from 15 to 63, and back down to 15")
	play.BinaryCounter(startCount, endCount, cycleTime)
	
	startCount = 62
	endCount = 15

	play.BinaryCounter(startCount, endCount, cycleTime)

	sleep(pauseSleep)
	
	seconds = cycleTime / 1000.0

	'''
		Display the attributes of bit 5
	'''
	play.Bits[4].display()

	sleep(pauseSleep * 2)

	cycleTime = 750							# 750 ms
	seconds = cycleTime / 1000.0
	
	print ("")
	print ("Setting bits 0, 2, 4, and 6 to ON")
	play.setBitsValue(0)
	play.bit(0, "on")
	sleep(seconds)
	play.bitSet(2, "on")
	sleep(seconds)
	print ("Flipping bit 2..")
	play.flip(2)
	sleep(seconds)
	print ("Flipping bit 2..")
	play.flip(2)
	sleep(seconds)
	play.bitSet(4, "on")
	sleep(seconds)
	play.bitSet(6, "on")
	sleep(seconds)
	print (" The bits value is hex " + hex(value) + " and decimal " + str(play.bitsValue()))

	sleep(pauseSleep * 5)

	print ("")
	print ("Setting bits 0 and 6 to OFF")
	play.bitSet(0, "off")
	sleep(seconds)
	play.bitSet(6, "off")
	sleep(seconds)
	print (" The bits value is hex " + hex(value) + " and decimal " + str(play.bitsValue()))

	sleep(pauseSleep * 5)
