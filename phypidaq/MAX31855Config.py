# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys

# import relevant pieces for MAX31855
import Adafruit_GPIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855

class MAX31855Config(object):
  ''' MAX31855 configuration and interface'''

  def __init__(self, confdict = None):
    if confdict==None: confdict={}
          
# -- number of Channels
    self.NChannels = 1
    
# -- configuration of chip select pin (CE0 or CE1)
    if "CE" in confdict:
        self.ce = confdict["CE"]
    else:
        self.ce = 0

# -- unit configuration MAX31855
    if "Unit" in confdict:
      if confdict["Unit"] == "DEGREES_F":
          self.unit = confdict["Unit"]
          self.ChanLims = [[14., 482.]]
      elif confdict["Unit"] == "KELVIN":
          self.unit = confdict["Unit"]
          self.ChanLims = [[263.15, 523.15]]
      else:
          self.unit = "DEGREES_C"
          self.ChanLims = [[-10., 250.]]
    else:
      self.unit = "DEGREES_C"
      self.ChanLims = [[-10., 250.]]

  def init(self):
  #Hardware configuration:
    try:
    # Create an MAX31855 instance.
      self.MAX31855 = MAX31855.MAX31855(spi=SPI.SpiDev(0, self.ce))
    except Exception as e:
      print("MAX31855Config: Error initialising device - exit")
      print(str(e))
      sys.exit(1)

 # provide configuration parameters
    self.ChanNams = ['MAX31855']

      
  def acquireData(self, buf):
    if self.unit == "KELVIN": # temperature in Kelvin
       buf[0] = self.MAX31855.readTempC()+ 273.15
    elif self.unit == "DEGREES_F": # temperature in degrees Fahrenheit
       buf[0] = (self.MAX31855.readTempC() * 1.8) + 32
    else:
       buf[0] = self.MAX31855.readTempC() # temperature in degrees Celsius
    


  def closeDevice(self):
   # nothing to do here
    pass
