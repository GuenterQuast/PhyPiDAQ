# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys

# import relevant pieces for TCS34725 RGB (color) sensor
import Adafruit_TCS34725 as TCS34725


class TCT34725Config(object):
  ''' TC34725 configuration and interface'''

  def __init__(self, confdict = None):
    if confdict == None: confdict={}
          
# -- number of Channels
    if 'NChannels' in confdict:
      self.NChannels = confdict['NChannels']
    else:
      self.NChannels = 3

    if 'Gain' in confdict:
      self.gain = confdict['Gain']      
    else:
      self.gain = TCS34725_GAIN_4X
        # Possible gain values:
        #  - TCS34725_GAIN_1X
        #  - TCS34725_GAIN_4X  (default)
        #  - TCS34725_GAIN_16X
        #  - TCS34725_GAIN_60X

    if 'IntegrationTime' in confdict:
      self.IntT = confdict['IntegrationTime']      
    else:
      self.IntT = TCS34725_INTEGRATIONTIME_24MS
#      self.IntT = TCS34725_INTEGRATIONTIME_2_4MS
        # Possible integration time values:
        #  - TCS34725_INTEGRATIONTIME_2_4MS  (default)
        #  - TCS34725_INTEGRATIONTIME_24MS
        #  - TCS34725_INTEGRATIONTIME_50MS
        #  - TCS34725_INTEGRATIONTIME_101MS
        #  - TCS34725_INTEGRATIONTIME_154MS
        #  - TCS34725_INTEGRATIONTIME_700MS

    if 'I2CADDR' in confdict:
      self.I2CAddr = confdict['I2CADDR']
      print("TCS34725: I2C address set to %x "%(self.I2CAddr) )
    else: 
      self.I2CAdddr = 0x29 # use default
     
    if 'busnum' in confdict:
      self.busnum = confdict['busnum']
      print("TCS34725: bus number set to %x "%(self.busnum) )
    else: 
      self.busnum=1 # use default
    
    self.maxVal = 65535. # 16 bit
      
  def init(self):
  #Hardware configuration:
    try:
    # Create a TCS34725 instance
      tcs = TCS34725.TCS34725(address=self.I2CAddr, smbus=self.busnum,
                        integration_time = self.IntT, gain = self.gain)
    except Exception as e:
      print("TCS34725Config: Error initialising device - exit")
      print(str(e))
      sys.exit(1)

 # provide configuration parameters
    self.ChanNams = ['R', 'G', 'B', 'c']
    self.ChanLimis = [[0., 1.]] * self.NChannels
      
  def acquireData(self, buf):
    tcs.set_interrupt(False)

    # Disable interrupts (can enable them by passing true, see the set_interrupt_limits function too).
    tcs.set_interrupt(False)

    # Read the R, G, B, C color data.
    r, g, b, c = tcs.get_raw_data()

    buf[0] = r / self.maxVal
    buf[1] = g / self.maxVal
    buf[2] = b / self.maxVal
    if self.NChannels > 3:
      buf[3] = c / self.maxVal

    ## there are some additional functions in Adafruit driver:
    #   calculate color temperature 
    ## color_temp = Adafruit_TCS34725.calculate_color_temperature(r, g, b)
    #   calculate lux with another utility function.
    ## lux = Adafruit_TCS34725.calculate_lux(r, g, b)

    # Enable interrupts and put the chip back to low power sleep/disabled.
    tcs.set_interrupt(True)
    tcs.disable()
 

  def closeDevice(self):
   # nothing to do here
    pass
