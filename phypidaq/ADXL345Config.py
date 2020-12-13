# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys
from Adafruit_ADXL345 import *

class ADXL345Config(object):
  '''digital accelerometer ADXL345 configuration and interface'''

  def __init__(self, confdict = None):
    if confdict==None: confdict={}
          
# -- number of Channels
    self.NChannels = 3
    self.ChanNams = ['x','y','z']
    self.ChanUnits= ['m/s²','m/s²', 'm/s²']

    if 'Range' in confdict:
     range = confdict['Range']
    else:
     range = '2G'
    if range == '2G':
      self.rng = ADXL345_RANGE_2_G
      r=2
    elif range == '4G':
      self.rng = ADXL345_RANGE_4_G
      r=4
    elif range == '8G':
      self.rng = ADXL345_RANGE_8_G
      r=8
    elif range == '16G':
      self.rng = ADXL345_RANGE_16_G
      r=16
    else:
      # invalid range, set to 2
      range ='2G'
      self.rng = ADXL345_RANGE_2_G
      r=2
      print("ADXL345: invalid range - set to 2G")

    self.ChanLims = [[-r*10., r*10.],[-r*10., r*10.], [-r*10., r*10.]]

  def init(self):
    bn= 1       # Bus number
    addr = 0x53 # address
    try:
      self.sensor = ADXL345(address=addr, busnum=bn)
    except Exception as e:      
      print("ASXL345: Error setting up device - exit")
      print(str(e))
      sys.exit(1)
    try:
      sensor.set_range(self.rng)
      sensor.set_data_rate(ADXL345_DATARATE_50_HZ) # default is 100_HZ
    except Exception as e:      
      print("ADXL345: Error initialising device - exit")
      print(str(e))
      sys.exit(1)
      
  def acquireData(self, buf):
    buf[0],buf[1], buf[2] = self.sensor.read()

  def closeDevice(self):
   # nothing to do here
    pass

