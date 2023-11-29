BeagleBone Development in Python
================================

Files:
	Bit_bone.py		Bit low level functions - has device specific code
	
	LED_Bone.py		Contains my LED class for the BeagleBone (Black)

	LedPlay_bone.py		Contains my LedPlay class and some code to demo it. This
					requires my LED class to work.
						
				This class contains fun stuff like a KnightRider function,
					as well as a nice binary up/down counter, and a setBits()
					function that allows you to set any binary value (0 - 255)
					on the 8 LEDs.
							
				These are all 8 bit routines, so they require 8 LEDs to be wired
					up to your BeagleBone (Black).

	README.md		This README	
	
