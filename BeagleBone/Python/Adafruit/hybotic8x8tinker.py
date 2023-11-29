#!/usr/bin/python

import time
import datetime
from Adafruit_8x8 import EightByEight, ColorEightByEight
from time import sleep

# ===========================================================================
# 8x8 Pixel Example
# ===========================================================================
InvaderBMPup = [
  0B00011000,
  0B00111100,
  0B01111110,
  0B11011011,
  0B00100100,
  0B01011010,
  0B10100101,
  0B00000000
]

InvaderBMPdown = [
  0B00000000,
  0B00011000,
  0B00111100,
  0B01111110,
  0B11011011,
  0B00100100,
  0B01011010,
  0B10100101
]

grid = ColorEightByEight(address=0x70)

# Draw a bit map graphic
def drawBitMap (bMap):
  for y in range(8):
    for x in range(8):
      if (bMap[y] & (2 ** x)):
        grid.setPixel(x, y, 1)

# Draw the jumping invader
print ("The jumping Invader..")
count = 20
pauseTime = 0.15
grid.clear()

for i in range(count):
  drawBitMap(InvaderBMPdown)
  sleep(pauseTime)
  grid.clear()
  drawBitMap(InvaderBMPup)
  sleep(pauseTime)
  grid.clear()

sleep(3)
grid.clear()
