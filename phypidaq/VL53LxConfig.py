# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys

# import relevant pieces for VL53L0X /1X distance sensor
import VL53L1X 
import VL53L0X 

VL53_Ranges = ['short', 'medium', 'long']
VL53L1_mmRanges = [0.,1300., 3000., 4000.]
VL53L0_mmRanges = [1200., 1200., 1200., 2000., 1200.]

class VL53LxConfig(object):
  ''' VL53L1X and FL53L0X configuration and interface'''

  def __init__(self, confdict = None):
    if confdict == None: confdict={}
          
# -- number of Channels
#    if 'NChannels' in confdict:
#      self.NChannels = confdict['NChannels']
#    else:
    self.NChannels = 1 # sensor only has one channel

# sensor type
    if 'type' in confdict:
      self.type = confdict['type']
      print("VL53Lx: sensor set to VL53L%iX "%(self.type) )
            # possible vales: 0, 1 
    else: 
      self.type=1  # VL53LX1 is default

    if 'range' in confdict:
      self.range = confdict['range']
      if self.type==1:
        self.mmranges = VL53L1_mmRanges
      else:
        self.mmranges = VL53L0_mmRanges
      print("VL53Lx: range set to %s "%(self.mmranges[self.range]) )
           # possible vales VL53L1X:  1 short, 2 medium, 3 long
           # possible vales VL53L0X:  0, 1, 2 1.2 m 
           #                          3  2.0 m
           #                          4  1.2 m, high speed (20ms)
    else: 
      self.range=2 # medium range

    if 'I2CADDR' in confdict:
      self.I2CAddr = confdict['I2CADDR']
      print("VL53L1X: I2C address set to %x "%(self.I2CAddr) )
    else: 
      self.I2CAddr = 0x29 # use default
     
    if 'busnum' in confdict:
      self.busnum = confdict['busnum']
      print("VL53L1X: bus number set to %x "%(self.busnum) )
    else: 
      self.busnum=1 # use default

 # provide channel parameters
    self.ChanNams = ['d']
    self.ChanLims = [[0., self.mmranges[self.range] ]] 
      
  def init(self):
  #Hardware configuration:
    try:
     if self.type == 1:
        # Create a VL53L1X instance
        self.vl53 = VL53L1X.VL53L1X(i2c_bus=self.busnum, i2c_address=self.I2CAddr) 
     else:
        # Create a VL53L0X instance
        self.vl53 = VL53L0X.VL53L0X(i2c_bus=self.busnum, i2c_address=self.I2CAddr) 
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
