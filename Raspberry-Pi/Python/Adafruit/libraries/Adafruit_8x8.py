#!/usr/bin/python

import time
import datetime
from Adafruit_LEDBackpack import LEDBackpack

# ===========================================================================
# 8x8 Pixel Display
# ===========================================================================

class EightByEight:
  disp = None
  rotation = 0

  # Constructor
  def __init__(self, address=0x70, debug=False):
    if (debug):
      print "Initializing a new instance of LEDBackpack at 0x%02X" % address

    self.disp = LEDBackpack(address=address, debug=debug)

  def getRotation(self):
    return self.rotation

  def setRotation(self, rot):
    if rot >= 0 and rot <= 3:
      self.rotation = rot

  def writeRowRaw(self, charNumber, value):
    "Sets a row of pixels using a raw 16-bit value"
    if (charNumber > 7):
      return

    # Set the appropriate row
    self.disp.setBufferRow(charNumber, value)

  def clearPixel(self, x, y):
    "A wrapper function to clear pixels (purely cosmetic)"
    self.setPixel(x, y, 0)

  def setPixel(self, x, y, color=1):
    "Sets a single pixel"

    #	Check for invalid coordinates
    if (x < 0) or (x >= 8) or (y < 0) or (y >= 8):
      return

	#	Check rotation, move pixel around if necessary
    if self.rotation == 1:
      x, y = y, x
      x = 8 - x - 1;
    elif self.rotation == 2:
      x = 8 - x - 1
      y = 8 - y - 1
    elif self.rotation == 3:
      x, y = y, x
      y = 8 - y - 1

#    x += 7   # ATTN: This might be a bug?  On the color matrix, this causes x=0 to draw on the last line instead of the first.
    x %= 8

    # This modification fixes the pixel addressing error
    if (x == 0):
      x = 7
    elif (x > 0):
      x = x - 1
    # End of modification for the pixel addressing error

    # Set the appropriate pixel
    buffer = self.disp.getBuffer()

    if (color):
      self.disp.setBufferRow(y, buffer[y] | 1 << x)
    else:
      self.disp.setBufferRow(y, buffer[y] & ~(1 << x))

  def clear(self):
    "Clears the entire display"
    self.disp.clear()

class ColorEightByEight(EightByEight):
  def setPixel(self, x, y, color=1):
    "Sets a single pixel"

    #	Check for invalid coordinates
    if (x < 0) or (x >= 8) or (y < 0) or (y >= 8):
      return

    #	Check rotation, move pixel around if necessary
    if self.rotation == 1:
      x, y = y, x
      x = 8 - x - 1;
    elif self.rotation == 2:
      x = 8 - x - 1
      y = 8 - y - 1
    elif self.rotation == 3:
      x, y = y, x
      y = 8 - y - 1

    x %= 8

    # This modification fixes the pixel addressing error
    if (x == 0):
      x = 7
    elif (x > 0):
      x = x - 1
    # End of modification for the pixel addressing error

    # Set the appropriate pixel
    buffer = self.disp.getBuffer()

    # TODO : Named color constants?
    # ATNN : This code was mostly taken from the arduino code, but with the addition of clearing the other bit when setting red or green.
    #        The arduino code does not do that, and might have the bug where if you draw red or green, then the other color, it actually draws yellow.
    #        The bug doesn't show up in the examples because it's always clearing.

    if (color == 1):
      #	Green
      self.disp.setBufferRow(y, (buffer[y] | (1 << x)) & ~(1 << (x+8)) )
    elif (color == 2):
      #	Red
      self.disp.setBufferRow(y, (buffer[y] | 1 << (x+8)) & ~(1 << x) )
    elif (color == 3):
      #	Yellow
      self.disp.setBufferRow(y, buffer[y] | (1 << (x+8)) | (1 << x) )
    else:
      self.disp.setBufferRow(y, buffer[y] & ~(1 << x) & ~(1 << (x+8)) )
