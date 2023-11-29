#!/usr/bin/env python

from Adafruit_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialize the PWM device using the default address
pwm = PWM(0x43, debug=True)

pwmFrequency = 50							# PWM Frequency

servoMin = 125  							# Min pulse length out of 4096 (500 uS?)
servoMax = 550  							# Max pulse length out of 4096 (2500 uS?)
servoCenter = (servoMin + servoMax) / 2		# 1500 uS?

def setServoPulseUs (channel, pulseWidth):
	cycleWidth = 1.0 / pwmFrequency
	timePerTick = cycleWidth / 4096
	
	maxNrTicks = pulseWidth / timePerTick

	print ("Cycle width = " + str(cycleWidth) + ", timePerTick = " + str(timePerTick) + ", maxNrTicks = " + str(maxNrTicks))

#	pwm.setPWM(channel, 0, maxNrTicks)

def setServoPulse (channel, pulse):
	pulseLength = 1000000                   # 1,000,000 us per second
	pulseLength /= pwmFrequency             # 60 Hz
	print "%d us per period" % pulseLength
	pulseLength /= 4096                     # 12 bits of resolution
	print "%d us per bit" % pulseLength

	newPulse = pulse * 1000
	newPulse /= pulseLength

#	pwm.setPWM(channel, 0, newPulse)

pwm.setPWMFreq(pwmFrequency)				# Set the PWM frequency

print ("Entering loop..")

while (True):
	print ("Servo Minimum (" + str(servoMin) + ")")
	pwm.setPWM(0, 0, servoMin)
	time.sleep(1)
	print ("Servo Center (" + str(servoCenter) + ")")
	pwm.setPWM(0, 0, servoCenter)
	time.sleep(1)
	print ("Servo Maximum (" + str(servoMax) + ")")
	pwm.setPWM(0, 0, servoMax)
	time.sleep(1)
	print ("Servo Center (" + str(servoCenter) + ")")
	pwm.setPWM(0, 0, servoCenter)
	time.sleep(1)
