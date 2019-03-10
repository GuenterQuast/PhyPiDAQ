# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys

# import relevant pieces for VL53L1X distance sensor
import VL53L1X 

VL53_Ranges = ['short', 'medium', 'long']
VL53_mmRanges = [1300., 3000., 4000.]

class VL53L1XConfig(object):
  ''' VL53L1X configuration and interface'''

  def __init__(self, confdict = None):
    if confdict == None: confdict={}
          
# -- number of Channels
#    if 'NChannels' in confdict:
#      self.NChannels = confdict['NChannels']
#    else:
    self.NChannels = 1 # sensor only has one channel

    if 'range' in confdict:
      self.range = confdict['range']
      print("VL53L1X: range set to %s "%(VL53_Ranges[i-1]) )
           # possible vales: 1 short, 2 medium, 3 long
    else: 
      self.range=2 # medium range

    if 'I2CADDR' in confdict:
      self.I2CAddr = confdict['I2CADDR']
      print("VL53L1X: I2C address set to %x "%(self.I2CAddr) )
    else: 
      self.I2CAdddr = 0x29 # use default
     
    if 'busnum' in confdict:
      self.busnum = confdict['busnum']
      print("VL53L1X: bus number set to %x "%(self.busnum) )
    else: 
      self.busnum=1 # use default

 # provide channel parameters
    self.ChanNams = ['d']
    self.ChanLims = [[0., VL53_mmRanges[self.range - 1] ]] 
      
  def init(self):
  #Hardware configuration:
    try:
    # Create a VL53L1X instance
      self.vl53 = VL53L1X.VL531L1X(i2c_bus=self.busnum, i2c_address=self.I2CAddr) 
    except Exception as e:
      print("VLC53L1XConfig: Error initialising device - exit")
      print(str(e))
      sys.exit(1)
    try:    
      self.vl53.open() # initialise and configure sensor 
    except Exception as e:
      print("VLC53L1XConfig: Error configuring device - exit")
      print(str(e))
      sys.exit(1)
    self.vl53.start_ranging(self.range) # start measurements
  
  def acquireData(self, buf):
    buf[0] = self.vl53.get_distance() # distance in mm

  def closeDevice(self):
   # nothing to do here
    self.vl53.stop_ranging() # stop measurements
