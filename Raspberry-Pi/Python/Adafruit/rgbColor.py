#!/usr/bin//env python
from time import sleep
from Adafruit_TCS34725 import TCS34725

# ===========================================================================
# Example Code
# ===========================================================================

# Initialize the TCS34725 and use default integration time and gain
# tcs34725 = TCS34725(debug=True)
tcs = TCS34725(integrationTime=0xEB, gain=0x01)
tcs.setInterrupt(False)
sleep(1)

rgb = tcs.getRawData()
colorTemp = tcs.calculateColorTemperature(rgb)
lux = tcs.calculateLux(rgb)

print ("Red = " + str(rgb["r"]) + ", Green = " + str(rgb["g"]) + ", Blue = " + str(rgb["b"]) + ", C = " + str(rgb["c"]))
print ("Color Temperature: " + str(colorTemp) + " K")
print ("Luminosity: "+ str(lux) + " lux")

tcs.setInterrupt(True)
sleep(1)

tcs.disable()
