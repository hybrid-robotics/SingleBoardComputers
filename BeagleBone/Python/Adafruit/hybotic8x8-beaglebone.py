#!/usr/bin/python

import time
import datetime
from Adafruit_8x8 import EightByEight, ColorEightByEight
from time import sleep

# ===========================================================================
# 8x8 Pixel Example
# ===========================================================================
InvaderDownBMP = [
  0B00000000,
  0B00011000,
  0B00111100,
  0B01111110,
  0B11011011,
  0B00100100,
  0B01011010,
  0B10100101
]

InvaderUpBMP = [
  0B00011000,
  0B00111100,
  0B01111110,
  0B11011011,
  0B00100100,
  0B01011010,
  0B10100101,
  0B00000000
]

grid = ColorEightByEight(address=0x70)

# Draw a bit map (BMP) graphic
def drawBitMap (bMap):
  for y in range(8):
    for x in range(8):
      if (bMap[y] & (2 ** x)):
        grid.setPixel(x, y, 1)

# Continually update the 8x8 display, one pixel at a time
count = 0
iter = 0

while(count < 10):
  iter += 1
  
  for x in range(8):
    for y in range(8):
      grid.setPixel(x, y, iter % 4 )
      time.sleep(0.02)
  
  count += 1

sleep(3)
grid.clear()

# Draw an X
for x in range(8):
  grid.setPixel(x, x, 1)

x = 0
y = 7

while (x < 8):
  grid.setPixel(x, y, 1)
  
  x += 1
  y -= 1

sleep(5)
grid.clear()

# Draw the Invader
drawBitMap(InvaderDownBMP)

sleep(5)
grid.clear()

# Make the Invader hop!
count = 20
delayTime = 150					# Delay time in ms
sleepTime = delayTime / 1000.0

for i in range(count):
	grid.clear()
	drawBitMap(InvaderDownBMP)
	sleep(sleepTime)

	grid.clear()
	drawBitMap(InvaderUpBMP)
	sleep(sleepTime)

grid.clear()
drawBitMap(InvaderDownBMP)

sleep(5)
grid.clear()
