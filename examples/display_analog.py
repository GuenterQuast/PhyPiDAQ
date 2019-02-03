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

# import display
from phypidaq.Display import *

# create an instance of the device
device = ADS1115Config()
#device = MCP3008Config()

# create instance of graphical display, 0.1 sec update interval
display = Display(interval=0.1)

# initialize device and display
device.init()
display.init()

# reserve space for data (here only one channel)
dat = np.array([0.]) 

print(' starting readout,     type <ctrl-C> to stop')

# start time
T0 = time.time()

try:
# readout loop, stop with <crtl>-C
  while True:
    device.acquireData(dat)
    dT = time.time() - T0
    print('%.2g, %.4g' %(dT, dat) )
    display.show(dat)
except KeyboardInterrupt:
  print('ctrl-C received - ending')
  device.closeDevice()
  display.close()

