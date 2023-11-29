#!/usr/bin/env python
import Adafruit_BBIO.PWM as PWM
import time

red = "P9_14"
green = "P9_16"
blue = "P9_21"

PWM.start(red, 0)
PWM.start(green, 0)
PWM.start(blue, 0)

def fade(colorA, colorB, ignore_color):
	PWM.set_duty_cycle(ignore_color, 100)

	for i in range(0, 100):
		PWM.set_duty_cycle(colorA, i)
		PWM.set_duty_cycle(colorB, 100 - i)
		time.sleep(0.05)
    	    	    	    	
while True:
	fade(red, green, blue)
	fade(green, blue, red)
	fade(blue, red, green)
