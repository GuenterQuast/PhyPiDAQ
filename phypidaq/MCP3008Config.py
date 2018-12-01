# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys

# import relevant pieces from adafruit
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

class MCP3008Config(object):
  '''ADC MCP3008 configuration and interface'''

  def __init__(self, confdict = None):
    if confdict==None: confdict={}

    if 'ADCChannels' in confdict:
      self.ADCChannels = confdict['ADCChannels']
    else:
      self.ADCChannels = [0]
    self.NChannels = len(self.ADCChannels)

    if 'DifModeChan' in confdict:
       self.DifModeChan = confdict['DifModeChan']
    else:
      self.DifModeChan = [false] * self.NChannels

    if 'VRef' in confdict:
      self.VRef = confdict['VRef']
    else:
      self.VRef = 5.0

    if 'NBits' in confdict:
      NBits = confdict['NBits']
    else:
      NBits = 10

    self.ADCmax = float( (1 << NBits) - 1)
    self.Vfac = self.VRef / self.ADCmax

  def init(self):
  #Hardware SPI configuration:
    SPI_PORT   = 0
    SPI_DEVICE = 0
    try:
      self.MCP = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE) )
    except Exception as e:
      print("MCP3008Config: Error initialising device - exit")
      print(str(e))
      sys.exit(1)

# provide configuration parameters
    self.ChanNams = []
    self.ChanLims = []
    for i, c  in enumerate(self.ADCChannels):
      isdifferential = self.DifModeChan[i]
      if isdifferential:
        if c%2:
          d= str( c) + '-' + str(c-1) 
        else:
          d= str( c) + '-' + str(c+1) 
      else:
        d = str(c)
      self.ChanNams.append(d) 
      self.ChanLims.append(  [- isdifferential * self.VRef , self.VRef])
      
  def acquireData(self, buf): 
    # read data from ADC
    for i, c  in enumerate(self.ADCChannels):
      if self.DifModeChan[i]:
        # need two readings or pair of channels, e.g.:   v = adc(0-1)  - adc(1-0)
        cb=c - c%2    # get lowest channel of pair
        v = (self.MCP.read_adc_difference(cb)\
                      - self.MCP.read_adc_difference(cb+1)) * self.Vfac
        if c%2:  v *= -1  # correct sign if odd channel number given    
        buf[i] = v 
      else:
        buf[i] = self.MCP.read_adc(c) * self.Vfac

  def closeDevice(self):
   # nothing to do here
   pass
