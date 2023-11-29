#!/usr/bin/env python
'''
	Program:		Bit_rPiw.py
	Version:		0.1.2w
	Date:			23-Nov-2013
	Purpose:		To define useful functions for controlling bits (GPIOs). Converted to use WiringPi2

	Dependencies:	WiringPi2

	Copyright (2013) by Dale Weber, hybotics.pdx@gmail.com, @hybotics (Twitter and App.Net)

	ALL Rights Reserved.
'''
# This is specific to the Raspberry Pi
import wiringpi2
wiringpi2.wiringPiSetupSys() # For /sys/class/gpio with GPIO pin numbering
wiringpi2.wiringPiSetupGpio() # For GPIO pin numbering
#import RPi.GPIO as GPIO
'''
wiringpi2.pinMode(1,1) # Set pin 1 to output
wiringpi2.digitalWrite(1,1) # Write 1 HIGH to pin 1
wiringpi2.digitalRead(1) # Read pin 1
'''

from hybotics import zilch

from time import sleep

'''
	Functions
'''

'''
	Initialize the Raspberry Pi GPIOs
'''
def setupRPiGPIO ():
	#	For  GPIO pin numbering
	wiringpi2.wiringPiSetupGpio() # For GPIO pin numbering
#	wiringpi2.wiringPiSetupSys()

	return None
            
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
		self.pin = bpin
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
		wiringpi2.pinMode(self.pin, 1)

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
			wiringpi2.digitalWrite(self.pin, 1)
			self.state = True
		elif (not bitState):
			wiringpi2.digitalWrite(self.pin, 0)
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
	End of clase Bit
'''

if (__name__ == "__main__"):
	setupRPiGPIO()

	pauseSleep = 3
	ms = 250

	print ("")
	print ("Initializing bit ON..")
	myBit = Bit("Red", "p9_11", True, "Dumb, fucked bit")
	
	myBit.display()
	sleep(pauseSleep)

	print ("")	
	print ("Toggling bit..")
	myBit.toggle(ms)
	
	myBit.display()
	sleep(pauseSleep)

	print ("")
	print ("Flipping bit..")
	myBit.flip()
	
	myBit.display()
	sleep(pauseSleep)
