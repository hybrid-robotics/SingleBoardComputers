#!/usr/bin/env python
'''
	Program:		Bit_bone.py
	Version:		0.1.2
	Date:			24-Oct-2013
	Purpose:		To define useful functions for controlling bits (GPIOs)

	Version:		0.1.5
	Date:			26-Nov-2013
	Purpose:		To define useful functions for controlling bits (GPIOs)

	Dependencies:	None

	Copyright (2013) by Dale Weber, hybotics.pdx@gmail.com, @hybotics (Twitter and App.Net)

	ALL Rights Reserved.
'''
# This is specific to the BeagleBone
import Adafruit_BBIO.GPIO as GPIO

from hybotics import zilch

from time import sleep

'''
	Functions
'''

'''
	Start of classes
'''

'''
	There are several fun and useful functions here.
'''
class Bit ():
	'''
		Bit information
	'''
	name = None
	number = None
	pin = None
	value = None
	state = None
	status = None

	'''
		Create a single bit
	'''
	def __init__ (self, bname, bpin, bstate, bstatus=None):
		'''
			Create a bit
		'''
		self.name = bname.lower()
		self.pin = bpin.upper()
		self.state = bstate
		self.status = bstatus

		'''
			We have no way to set these here:
				 bit number (bitNr = 0 to the number of bits - 1)
				 bit value (bitValue =  bitNr ** 2).

			These will have to be set by an external routine.

			These values will be of most use in programs that use lists of bits.
		'''
		self.number = None
		self.value = None

		# Set the pin to OUTPUT
		GPIO.setup(self.pin, GPIO.OUT)

		# Initialize the bit on or off
		self.bit(self.state)

		return None

	'''
		Set the bit on or off
	'''
	def bit (self, bitState):
		status = True

		if (bitState):
			# Do a bitwise OR of the bit with the current value
			GPIO.output(self.pin, GPIO.HIGH)
			self.state = True
		elif (not bitState):
			GPIO.output(self.pin, GPIO.LOW)
			self.state = False
		else:
			print ("Invalid bit state: " + bitState + "!")
			status = False

		return status

	'''
		Return a dict of bit information. This allows date to be taken out,
			and used in other routines.
	'''
	def bitInfo (self):
		bit = {
			"name" : self.name,
			"number" : self.number,
			"pin" : self.pin,
			"value" : self.value,
			"state" : self.state,
			"status" : self.status
		}

		return bit

	'''
		Returns one of two strings for the bit, depending on its state
	'''
	def bitStateString (self, tvalue, fvalue):
		if self.state:
			st = tvalue
		else:
			st = fvalue

		return st

	'''
		Display the attributes of the bit
	'''
	def display (self):
		status = True
		
		print ("")
		print ("Bit attributes:")
		print ("")
		print ("  Name:       " + zilch(self.name))
		print ("  Pin:        " + zilch(self.pin))
		print ("  Bit Number: " + zilch(str(self.number)))
		print ("  Bit Value:  " + zilch(str(self.value)))
		print ("  State:      " + zilch(self.bitStateString("On", "Off")))
		print ("  Status:     " + zilch(self.status))

		return status

	'''
		Flip a bit
	'''
	def flip (self):
		status = True
		
		# Flip the state of the bit in the state list
		if self.state:
			self.bit(False)
		else:
			self.bit(True)

		return status

	'''
		Set the global bit variables from a bit dict
	'''
	def setinfo (self, bit):
		self.name = bit["name"]
		self.number = bit["number"]
		self.pin = bit["pin"]
		self.value = bit["value"]
		self.state = bit["state"]
		self.status = bit["status"]

		return True

	'''
		Toggle a bit
	'''
	def toggle (self, ms):
		status = True
		seconds = ms / 1000.0

		self.flip()
		sleep(seconds)
		self.flip()

		return status
'''
	End of class Bit
'''

if (__name__ == "__main__"):
	pauseTime = 3
	ms = 250
	holdTime = ms / 1000.0

	print ("")
	print ("Initializing bit ON..")
	myBit = Bit("Green", "P9_11", True, "Dumb, stupid little bit")
	
	myBit.display()
	sleep(pauseSleep)

	print ("Initializing bits OFF..")

	green = Bit("Green", "GPIO1_12", False, "Green LED")			# P8_12, GPIO1_12
	red = Bit("Red", "GPIO0_26", False, "Red LED")					# P8_14, GPIO0_26
	blue = Bit("Blue", "GPIO1_14", False, "Blue LED")				# P8_16, GPIO1_14
	white = Bit("White", "GPIO2_1", False, "White LED")				# P8_18, GPIO2_1

	blue.display()
	green.display()
	sleep(pauseTime)

	print ("")	
	print ("Changing bits..")

	blue.bit(True)
	green.bit(False)
	sleep(holdTime)

	for i in range(10):
		blue.flip()
		green.flip()
		sleep(holdTime)
		blue.flip()
		green.flip()
		sleep(holdTime)

	blue.display()
	green.display()

	blue.display()
	green.display()
	sleep(pauseTime)

	GPIO.cleanup()
