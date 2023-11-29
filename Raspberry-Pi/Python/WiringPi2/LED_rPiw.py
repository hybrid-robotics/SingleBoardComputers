#!/usr/bin/env python

'''
	Program:		LED-rPiw.py
	Version:		0.1.2w
	Date:			23-Nov-2013
	Purpose:		To define information and methods for changing the state
						of an LED, and information about it on a Raspberry Pi.

	Dependencies:	class Bits from Bits.py
	
	Copyright (2013) by Dale Weber, hybotics.pdx@gmail.com, @hybotics (Twitter and App.Net)
	
	ALL Rights Reserved.
'''

# Hybotics Bit class
from Bit_rPiw import Bit, setupRPiGPIO

from hybotics import zilch

from time import sleep

'''
	Defines a single LED
'''
class LED (Bit):
	'''
		LED Information
	'''
	name = None
	color = None
	description = None
	bit = None
	status = None
	blinkRate = None
	process = None

	'''
		Constructor
	'''
	def __init__ (self, lname, bpin, bstate, lcolor, ldescr, lblinkRate=None, lprocess=None, lstatus=None):
		self.name = lname.lower()
		self.color = lcolor
		self.description = ldescr
		self.status = lstatus

		# Create the LED companion Bit
		self.bit = Bit(lname, bpin, bstate, self.status)

		'''
			The process and blink rate should NEVER be None, so we have an
				internal process and blink rate we default to if none is
				supplied
		'''
		if (lprocess == None):
			self.process = self.blinkProcess
		else:
			self.process = lprocess

		if (lblinkRate == None):
			self.blinkRate = 250					# 250 ms
		else:
			self.blinkRate = lblinkRate
		
		return None

	'''
	***	Begin LED Management routines
	'''

	'''
		Blink an LED - have not figured out how to do this in a separate
			process yet.
	'''
	def blink (self, bRate):
		if (bRate != None):
			self.status = "blinking at " + str(bRate) + " ms"

			# Convert milliseconds to seconds for sleep()
			self.blinkRate = bRate
			seconds = bRate / 1000.0
			
			# Launch as a separate process or thread, so we don't block
#			status = self.process(self.blinkRate)
		else:
			print ("Invalid blink rate!")
			status = False

		return status

	'''
		Blink process to blink an LED at a set rate
	'''
	def blinkProcess (self, bRate):
		status = True
		blinking = False

		print ("Blinking the " + self.color + " LED..")
		self.blinkRate = bRate

		while (blinking):
			self.bit.flip()
			sleep(self.blinkRate)
			self.bit.flip()
		
		return status

	'''
		Display the LED attributes
	'''
	def display (self):
		status = True

		print ("")
		print ("Attributes for the '" + zilch(self.name) + "' LED:")
		print ("")

		print ("  On GPIO:     " + zilch(str(self.bit.pin)))
		print ("  Bit Number:  " + zilch(str(self.bit.number)))
		print ("  Bit Value:   " + zilch(str(self.bit.value)))
		print ("")
		print ("  Status:      " + zilch(self.status))
		print ("  Color:       " + zilch(self.color))
		print ("")
		print ("  Blink Rate:  " + zilch(str(self.blinkRate)))
		print ("")
		print ("  Description: " + zilch(self.description))

		return status

	'''
		Return a dict of the current LED information, which allows information about the LED to be pulled
			out and used outside the class.
	'''
	def ledInfo (self):
		led = {
			"name" : self.name,
			"bit" : self.bit,
			"color" : self.color,
			"blinkrate" : self.blinkRate,
			"process" : self.process,
			"description" : self.description,
			"status" : self.status
		}

		return led

	'''
		Returns one of two strings for the LED, depending on its state
	'''
	def ledStateString (self, tvalue, fvalue):
		if (self.bit == None) or (self.bit.state == None):
			st = "None"
		elif self.bit.state:
			st = tvalue
		else:
			st = fvalue

		return st

	'''
		Set the global LED variables from an led info dict. This one puts the LED info back into an LED
	'''
	def setInfo (self, led):
		status = True

		self.name = led["name"]
		self.color = led["color"]
		self.blinkRate = led["blinkrate"]
		self.process = led["process"]
		self.description = led["description"]
		self.bit = led["bit"]
		self.status = led["status"]

		return status

	def setBlinkRate (self, bRate):
		status = True
		self.blinkRate = bRate
		
		return status

if (__name__ == "__main__"):
	setupRPiGPIO()

	pauseSleep = 3

	myLED = LED("Yellow", 4, True, "Yellow", "The Yellow LED", 500, None, "LED")

	myLED.display()
	myLED.bit.display()

	sleep(pauseSleep)
