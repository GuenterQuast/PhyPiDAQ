#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import numpy as np

# import module controlling readout device
from phypidaq.BMP280Config import *

# Create a config dictionary, to print all four channels
config_dict = {'NChannels': 3}

# create an instance of the device
device = BMP280Config(config_dict=config_dict)

# Initialize the device
device.init()

# reserve space for data (four channels here)
data = np.array([0., 0., 0.])

print(' starting readout,     type <ctrl-C> to stop')

# read-out interval in s
dt = 2.
# start time
T0 = time.time()

# readout loop, stop with <crtl>-C
while True:
    device.acquireData(data)
    dT = time.time() - T0
    print('%.2g, %.4g°C %.6ghPa %.4gm' %(dT, data[0], data[1], data[2]))
    time.sleep(dt)
