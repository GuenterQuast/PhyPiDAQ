#!/usr/bin/python3
"""set_MCP4725
   set voltage on DAC MCP4725
"""
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import time, sys
# Import the MCP4725 module.
import Adafruit_MCP4725

# Create a DAC instance.
dac = Adafruit_MCP4725.MCP4725(address=0x60, busnum=1)

V = 0.  # default 0V 
if len(sys.argv) > 1:
  V = float(sys.argv[1])

VB = 5.

print('setting Voltage=%.2f' %(V) )
try:
    dac.set_voltage( int(V/VB * 4095))  # 

except  KeyboardInterrupt:
    print ("error setting Voltage")

finally:
  sys.exit(0)

