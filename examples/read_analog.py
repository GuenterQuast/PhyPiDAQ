#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''read_analog.py
     this script illustrates the general usage of package phypidaq
     pirints data read from an analog channel
'''
import time, numpy as np

# import module controlling readout device
from phypidaq.ADS1115Config import *
#from phypidaq.MCP3008Config import *

# create an instance of the device
device = ADS1115Config()
#device = MCP3008Config()

# initialize the device
device.init()

# reserve space for data (here only one channel)
dat = np.array([0.]) 

print(' starting readout,     type <ctrl-C> to stop')

# read-out interval in s
dt = 1.
# start time
T0 = time.time()

# readout loop, stop with <crtl>-C
while True:
  device.acquireData(dat)
  dT = time.time() - T0
  print('%.2g, %.4g' %(dT, dat) )
  time.sleep(dt)

