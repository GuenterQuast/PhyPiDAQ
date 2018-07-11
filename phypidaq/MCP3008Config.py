# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys

# import relevant pieces from adafruit
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

class MCP3008Config(object):
  '''set ADC MCP3008 configuration'''

  def __init__(self, confdict = None):
    if confdict==None: confdict={}

    if 'NChannels' in confdict:
      self.NChannels = confdict['NChannels']
    else:
      self.NChannels = 1

  def init(self):
  #Hardware SPI configuration:
    SPI_PORT   = 0
    SPI_DEVICE = 0
    try:
      self.MCP = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT,
                           SPI_DEVICE, max_speed_hz=15600000) )
                                                      # run bus at 15.6 MHz, default is 0.488MHz
    except:
      print("MCP3008Config: Error initialising device - exit")
      sys.exit(1)
 
  def acquireData(self, buf): 
    # read data from ADC
    for i in range(self.NChannels):
      buf[i] = self.MCP.read_adc(i) * 3.3 / 1023

