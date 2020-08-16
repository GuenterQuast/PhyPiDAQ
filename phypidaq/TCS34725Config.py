# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys

# import relevant pieces for TCS34725 RGB (color) sensor
import Adafruit_TCS34725 as TCS34725


class TCS34725Config(object):
  ''' TC34725 configuration and interface'''

  def __init__(self, confdict = None):
    if confdict == None: confdict={}
          
# -- number of Channels
    if 'NChannels' in confdict:
      self.NChannels = confdict['NChannels']
    else:
      self.NChannels = 3

    if 'Gain' in confdict:
      gains = (TCS34725.TCS34725_GAIN_1X,
               TCS34725.TCS34725_GAIN_4X,
               TCS34725.TCS34725_GAIN_16X,
               TCS34725.TCS34725_GAIN_60X)
      self.gain = gains(confdict['Gain'])      
    else:
      self.gain = TCS34725.TCS34725_GAIN_60X
        # Possible gain values:
        #  - TCS34725_GAIN_1X
        #  - TCS34725_GAIN_4X  (default)
        #  - TCS34725_GAIN_16X
        #  - TCS34725_GAIN_60X

    if 'IntegrationTime' in confdict:
      IntTs = (TCS34725.TCS34725_INTEGRATIONTIME_2_4MS, 
               TCS34725.TCS34725_INTEGRATIONTIME_24MS,
               TCS34725.TCS34725_INTEGRATIONTIME_50MS,
               TCS34725.TCS34725_INTEGRATIONTIME_101MS,
               TCS34725.TCS34725_INTEGRATIONTIME_154MS,
               TCS34725.TCS34725_INTEGRATIONTIME_700MS)
      maxVals = (1024, 10240, 20480, 43008, 65535, 65535)
      self.IntT = IntTs(confdict['IntegrationTime'])      
      self.maxCount = maxVals(confdict['IntegrationTime'])      
    else:
      self.IntT = TCS34725.TCS34725_INTEGRATIONTIME_2_4MS
      self.maxCount = 1024. # 10 bit
        # Possible integration time values:
        # - TCS34725_INTEGRATIONTIME_2_4MS  = 2.4ms - 1 cycle    - Max Count: 1024 (default)
        # - TCS34725_INTEGRATIONTIME_24MS   = 24ms  - 10 cycles  - Max Count: 10240
        # - TCS34725_INTEGRATIONTIME_50MS   = 50ms  - 20 cycles  - Max Count: 20480
        # - TCS34725_INTEGRATIONTIME_101MS  = 101ms - 42 cycles  - Max Count: 43008
        # - TCS34725_INTEGRATIONTIME_154MS  = 154ms - 64 cycles  - Max Count: 65535
        # - TCS34725_INTEGRATIONTIME_700MS  = 700ms - 256 cycles - Max Count: 65535
 
    if 'I2CADDR' in confdict:
      self.I2CAddr = confdict['I2CADDR']
      print("TCS34725: I2C address set to %x "%(self.I2CAddr) )
    else: 
      self.I2CAddr = 0x29 # use default
     
    if 'busnum' in confdict:
      self.busnum = confdict['busnum']
      print("TCS34725: bus number set to %x "%(self.busnum) )
    else: 
      self.busnum=1 # use default
    
 # provide configuration parameters
    self.ChanNams = ['R', 'G', 'B', 'c']
    self.ChanLims = [[0., 1.]] * self.NChannels
      
  def init(self):
  #Hardware configuration:
    try:
    # Create a TCS34725 instance
      self.tcs = TCS34725.TCS34725(address=self.I2CAddr, busnum=self.busnum,
                        integration_time = self.IntT, gain = self.gain)
    except Exception as e:
      print("TCS34725Config: Error initialising device - exit")
      print(str(e))
      sys.exit(1)

    # Disable interrupts (can enable them by passing true, see the set_interrupt_limits function too).
    self.tcs.set_interrupt(False)

      
  def acquireData(self, buf):

    # Read the R, G, B, C color data.
    r, g, b, c = self.tcs.get_raw_data()
    if self.NChannels == 1:
      buf[0] = c / self.maxCount
    else:
      buf[0] = r / self.maxCount
      buf[1] = g / self.maxCount
      buf[2] = b / self.maxCount
      if self.NChannels > 3:
        buf[3] = c / self.maxCount

    ## there are some additional functions in Adafruit driver:
    #   calculate color temperature 
    ## color_temp = Adafruit_TCS34725.calculate_color_temperature(r, g, b)
    #   calculate lux with another utility function.
    ## lux = Adafruit_TCS34725.calculate_lux(r, g, b)

    # Enable interrupts and put the chip back to low power sleep/disabled.
    #  self.tcs.set_interrupt(True)
    #  self.tcs.disable()
 

  def closeDevice(self):
   # nothing to do here
    pass
