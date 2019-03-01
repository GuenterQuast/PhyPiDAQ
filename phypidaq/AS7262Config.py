# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys

# import relevant pieces for AS7262 color sensor
import as7262 

class AS7262Config(object):
  ''' AS7262 configuration and interface'''

  def __init__(self, confdict = None):
    if confdict == None: confdict={}
          
# -- number of Channels
    self.NChannels = 6

    if 'Gain' in confdict:
      self.gain = confdict['Gain']      
    else:
      self.gain = 64
        # Possible gain values:
        #   1, 3.7, 16 or 64

    if 'IntegrationTime' in confdict:
      self.IntT = confdict['IntegrationTime']      
    else:
      self.IntT = 10.

# not supported by simple as7262 interface
#    if 'I2CADDR' in confdict:
#      self.I2CAddr = confdict['I2CADDR']
#      print("AS7262: I2C address set to %x "%(self.I2CAddr) )
#    else: 
#      self.I2CAdddr = 0x49 # use default
#    if 'busnum' in confdict:
#      self.busnum = confdict['busnum']
#      print("AS7262: bus number set to %x "%(self.busnum) )
#    else: 
#      self.busnum=1 # use default
    
    self.maxVal = 15000. # ~14 bit

 # provide configuration parameters
    self.ChanNams = ['r', 'o', 'y', 'g', 'b', 'v']
    self.ChanLims = [[0., 1.]] * self.NChannels
      
 
  def init(self):
 
    try:
      as7262.soft_reset()
      as7262.set_gain(self.gain)
      as7262.set_integration_time(self.IntT)
      as7262.set_measurement_mode(2) # all six channels
      as7262.set_illumination_led(1)
    except Exception as e:
      print("AS7262Config: Error initialising device - exit")
      print(str(e))
      sys.exit(1)

  def acquireData(self, buf):
    buf[0], buf[1], buf[2], buf[3], buf[4], buf[5] = as7262.get_calibrated_values()
    
    for i in range(self.NChannels):
      buf[i] /= self.maxVal

  def closeDevice(self):
    as7262.set_illumination_led(0) # led off
    as7262.set_measurement_mode(3) # power-on default

