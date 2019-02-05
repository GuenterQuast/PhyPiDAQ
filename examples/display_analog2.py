#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''display_analog2.py
     illustrates the general usage of package phypidaq
     prints and displays data read from 2 analog channels
'''
import time, numpy as np
# import module controlling readout device
from phypidaq.ADS1115Config import *

# import display
from phypidaq.Display import *

# create device and display ...
device = ADS1115Config( {'ADCChannels': [0,1]} ) # channels 0 and 1
  # dictionary with graphics options
ddict = {'NChannels': 2, 'XYmode': False} 
display = Display( interval=0.1, confdict=ddict) # display 2 channels
# ... and initalize 
device.init()
display.init()

# reserve space for data (two channels)
dat = np.array([0., 0.]) 

print(' starting readout,     type <ctrl-C> to stop')
# start time
T0 = time.time()
try:
# readout loop, stop with <crtl>-C
  while True:
    device.acquireData(dat)
    dT = time.time() - T0
    print('%.2g, %.4g %.4g' %(dT, dat[0], dat[1]) )
    display.show(dat)
except KeyboardInterrupt:
  print('ctrl-C received - ending')
  device.closeDevice()
  display.close()

