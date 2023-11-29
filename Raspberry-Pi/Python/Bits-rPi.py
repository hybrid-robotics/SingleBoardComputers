#!/usr/bin/env python
'''
	Program:		Bits.py
	Version:		0.1.2
	Date:			19-Oct-2013
	Purpose:		To define useful functions for controlling a set of 8 GPIOs

	Dependencies:	None

	Copyright (2013) by Dale Weber, hybotics.pdx@gmail.com, @hybotics (Twitter and App.Net)

	ALL Rights Reserved.
'''
                            
import pprint

from time import sleep

'''
	Start of classes
'''

'''
	There are several fun and useful functions here.
'''
class Bits ():
	pp = None

	'''
		Bit information
	'''
	name = None
	pin = None
	value = None
	state = None
	status = None

	'''
		Our list of bits
	'''
	BitList = []

	'''
		Create our Bits
	'''
	def __init__ (self, bname, bpin, bvalue, bstate):
		'''
			Create a bit
		'''

		self.name = bname
		self.pin = bpin
		self.value = bvalue
		self.state = bstate

		bit = {
			"name" : self.name,
			"pin" : self.pin,
			"value" : self.value,
			"state" : self.state,
			"status" : self.bitString(bstate, "On", "Off")
		}

		self.BitList.append(bit)

		# Set the pin to OUTPUT
		GPIO.setup(self.pin, GPIO.OUT)

		return None

	'''
		Set a single bit on or off, by bit number
	'''
	def bit (self, bitNr, bitState):
		status = True
		currentValue = self.bitsValue()

		if (bitNr < 0) or (bitNr > 7):
			print ("There are only EIGHT bits, numbered 0 through 7!")
			status = False
		else:
			currentValue = self.bitsValue()

			bitValue = self.BitValues[bitNr]
			state = bitState.lower()

			if (state == "on"):
				# Do a bitwise OR of the bit with the current value
				self.BitStates[bitNr] = True
			elif (state == "off"):
				'''
					Do a bitwise *exclusive* OR of the bit with the current value
					
					The bit in currentValue stays the same IF the bit in bitValue is OFF,
						but gets turned OFF IF the bit in bitValue is ON
				'''
				self.BitStates[bitNr] = False
			else:
				print ("Invalid bit state: " + bitState + "!")
				status = False

			if status:
				# Change the state of the bit
				Bits[bitNr].change(state)

				# Update the current value of the bits
				currentValue = self.bitsValue()
			else:
				currentValue = 0


		return ( status, currentValue )

	'''
		Return a dict of bit information. This allows date to be taken out,
			and used in other routines.
	'''
	def bitInfo (self, bitNr):
		status = True
		bit = None

		if (bitNr < 0) or (bitNr > 7):
			print ("There are only 8 bits (0 - 7). " + str(bitNr) + " is invalid!")
			status = False
		else:
			bit = Bits[bitNr]

			self.name = bit["name"]
			self.pin = bit["pin"]
			self.bit = bit["bit"]
			self.value = bit["value"]
			self.state = bit["state"]
			self.color = bit["color"]
			self.blinkRate = bit["blinkrate"]
			self.process = bit["process"]
			self.description = bit["description"]

		return ( status, bit )

	'''
		Returns one of two strings for the bit, depending on its state
	'''
	def bitString (self, bstate, tvalue, fvalue):
		if bstate:
			st = tvalue
		else:
			st = fvalue

		return st

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
	def findBit (self, bitName):
		status = True
		foundIndex = None

		bitIndex = 0
		nrBits = len(Bits)

		while (foundIndex == None) and (bitIndex < nrBits):
			if (self.BitNames[bitNr] == bitName)
				foundIndex = bitIndex

			bitIndex += 1

		status = (foundIndex != None)

		if (not status):
			foundIndex = None

		return ( status, foundIndex )

	'''
		Flip a bit
	'''
	def flip (self, bitNr):
		# Flip the state of the bit in the state list
		if self.BitStates[bitNr]:
			self.bit(bitNr, "off")
		else:
			self.bit(bitNr, "on")

		newValue = self.bitsValue()

		return newValue

	'''
		Set the global bit variables from a bit dict
	'''
	def set (self, bit):
		self.name = bit["name"]
		self.pin = bit["pin"]
		self.bit = bit["bit"]
		self.value = bit["value"]
		self.state = bit["state"]
		self.color = bit["color"]
		self.blinkRate = bit["blinkrate"]
		self.process = bit["process"]
		self.description = bit["descri[tion"]

		return True

	'''
		Allows setting all 8 LEDs to any value, within 0 to 255
	'''
	def setBits (self, value):
		status = True

		if (value < 0) or (value > 255):
			print ("There are only EIGHT LEDs, for a range of 0 to 255!")
			status = False
		else:		
			bitValue = []

			'''
				Find out which bits are "on"
			'''
			for bitNr in range(8):
				bitValue.append(value & self.BitValues[bitNr])

			'''
				Set each bit according to whether it is "on", or "off"
				
				We also update the BitStates list.
			'''
			for bitNr in range(8):
				if (bitValue[bitNr] > 0):
					self.Bits[bitNr].change("on")
					self.BitStates[bitNr] = True
				else:
					self.Bits[bitNr].change("off")
					self.BitStates[bitNr] = False

		return status		

	'''
		Toggle a bit
	'''
	def toggleBit (self, bitNr, ms):
		status = True
		seconds = ms / 1000.0

		self.flip(bitNr)
		sleep(seconds)
		self.flip(bitNr)

		return status

	'''
		One cycle of the Knight Rider pattern
	'''
	def oneKnightCycle (self, onTimeMs):
		for bitNr in range(1, 7, 1):
			self.Bits[bitNr].wink(onTimeMs)

		for bitNr in range(7, -1, -1):
			self.Bits[bitNr].wink(onTimeMs)

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
	cycleTime = 75							# 75 ms
	startCount = 0
	endCount = 255
	print ("")
	print ("Counting from 0 to 255 and back down to 0")
	play.BinaryCounter(startCount, endCount, cycleTime)
	
	'''
		Count in binary DOWN from 254 to 0, with an on time of 100 ms
	'''
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

	'''
		This shows how any pattern of LEDs can be setup easily, and how sequences can easily
			be made
	'''
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
		Display the attributes of bit 5
	'''
	play.Bits[4].display()

	sleep(pauseSleep * 5)

	cycleTime = 750							# 750 ms
	seconds = cycleTime / 1000.0
	
	print ("")
	print ("Setting bits 0, 2, 4, and 6 to ON")
	play.setBits(0)
	play.bit(0, "on")
	sleep(seconds)
	play.bit(2, "on")
	sleep(seconds)
	print ("Flipping bit 2..")
	play.flip(2)
	sleep(seconds)
	print ("Flipping bit 2..")
	play.flip(2)
	sleep(seconds)
	play.bit(4, "on")
	sleep(seconds)
	play.bit(6, "on")
	sleep(seconds)
	print (" The bits value is hex " + hex(value) + " and decimal " + str(play.bitsValue()))

	sleep(pauseSleep * 5)

	print ("")
	print ("Setting bits 0 and 6 to OFF")
	play.bit(0, "off")
	sleep(seconds)
	play.bit(6, "off")
	sleep(seconds)
	print (" The bits value is hex " + hex(value) + " and decimal " + str(play.bitsValue()))

	sleep(pauseSleep * 5)
