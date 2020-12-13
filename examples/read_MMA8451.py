#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''read data from digital sensor: BMB 180 temperature and pressure
     this script illustrates the general usage of package phypidaq
     pirints data read from a digital sensor  
       (BMP180 Temperature and Pressure Sensor)
'''
import time, numpy as np

# import module controlling readout device
from phypidaq.MMA8451Config import *

# create an instance of the device
device = MMA8451Config()

# initialize the device
device.init()

# reserve space for data (two channels here)
dat = np.array([0., 0., 0.]) 

print(' starting readout,     type <ctrl-C> to stop')

# read-out interval in s
dt = 0.5
# start time
T0 = time.time()

# readout loop, stop with <crtl>-C
while True:
  device.acquireData(dat)
  dT = time.time() - T0

  print('%6.1f, x: %+7.3fm/s²  y: %+7.3fm/s²  z: %+7.3fm/s²'%(dT, dat[0], dat[1], dat[2]) )
  time.sleep(dt)

